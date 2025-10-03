import pandas as pd
import zipfile

def separa_corridas(df):
    """Splits the complete dataframe into its individual sequencing samples.

    Parameters:
    df (pandas.core.frame.DataFrame): Database with metabarcoding results after Blast.

    Returns:
    areas (dict): Dictionary with dataframes identified by keys containing the names listed in the sequencing sample list.
    """
    if 'amostra_sequenciamento' in df.columns:
        lista_corridas = list(df['amostra_sequenciamento'].unique())
    elif 'sequencing_sample' in df.columns:
        lista_corridas = list(df['sequencing_sample'].unique())

    corridas = {}
    for corrida in lista_corridas:
        nome_corrida = corrida
        if 'amostra_sequenciamento' in df.columns:
            corridas[nome_corrida] = df[df['amostra_sequenciamento'] == corrida]
        elif 'sequencing_sample' in df.columns:
            corridas[nome_corrida] = df[df['sequencing_sample'] == corrida]

    return corridas


def aplica_threshold(corridas, threshold_perc):
    """Calculates the read threshold for each sequencing sample and removes OTUs/ASVs equal or below it.

    Parameters:
    corridas (dict): Databases for each sequencing sample organized in a dictionary.
    threshold_perc (float): Percentage value for threshold calculation.

    Returns:
    selecionados (dict): Dictionary with dataframes containing selected OTUs/ASVs.
    nao_selecionados (dict): Dictionary with dataframes containing removed OTUs/ASVs.
    df_thresholds (DataFrame): Dataframe with calculated threshold values per sequencing sample.
    """
    thresholds = {}
    selecionados = {}
    nao_selecionados = {}

    for corrida in corridas:
        df = corridas[corrida]
        reads = df['n_reads']
        total_reads = sum(reads)
        threshold = total_reads * threshold_perc / 100

        thresholds[corrida] = threshold

        selecionado = df.loc[df['n_reads'] > threshold]
        selecionados[corrida] = selecionado

        nao_selecionado = df.loc[df['n_reads'] <= threshold]
        nao_selecionados[corrida] = nao_selecionado

    df_thresholds = pd.DataFrame.from_dict(thresholds, orient='index')
    df_thresholds = df_thresholds.rename(columns={0: 'Threshold'})
    return selecionados, nao_selecionados, df_thresholds


def concatena_dfs(dfs):
    """Concatenates dataframes from a dictionary.

    Parameters:
    dfs (dict): Dataframes organized in a dictionary.

    Returns:
    tabelas_concatenadas (DataFrame): Dataframe resulting from the concatenation of the dataframes.
    """
    tabelas = dfs.values()
    tabelas_concatenadas = pd.concat(tabelas, ignore_index=True)
    return tabelas_concatenadas


def define_areas(df):
    """Creates a list of sampling areas.

    Parameters:
    df (DataFrame): Dataframe with taxonomic assignment results and OTUs/ASVs equal or below the read threshold removed.

    Returns:
    lista_areas (list): List of sampling areas.
    """
    if 'area_amostrador' in df.columns:
        lista_amostras = df['area_amostrador'].unique()
    elif 'area_sampler' in df.columns:
        lista_amostras = df['area_sampler'].unique()

    for i in range(len(lista_amostras)):
        lista_amostras[i] = tuple(lista_amostras[i].split('_'))

    lista_areas = []

    for area, amostrador in lista_amostras:
        lista_areas.append(area)

    lista_areas = list(set(lista_areas))

    return lista_areas


def separa_amostradores(df, amostradores):
    """Filters the OTU/ASV table according to the sampler.

    Parameters:
    df (DataFrame): Dataframe with taxonomic assignment results and OTUs/ASVs equal or below the read threshold removed.
    amostradores (list): List with sampler designations.

    Returns:
    amst (dict): Dictionary with dataframes separated by sampler.
    """
    amst = {}
    for amostrador in amostradores:
        if 'area_amostrador' in df.columns:
            amst[amostrador] = df[df['area_amostrador'].str.contains(amostrador)]
        elif 'area_sampler' in df.columns:
            amst[amostrador] = df[df['area_sampler'].str.contains(amostrador)]

    return amst


def conta_ocorrencias_gerais(df, lista_areas):
    """Counts general taxon detections.

    Parameters:
    df (DataFrame): Dataframe with taxonomic assignment results and OTUs/ASVs equal or below the read threshold removed.
    lista_areas (list): List of sampling areas.

    Returns:
    cont_ocorr (DataFrame): Dataframe with general detection counts per taxon.
    """
    contagens = []
    if 'area_amostrador' in df.columns:
        for area in lista_areas:
            amst_areas = df[df['area_amostrador'].str.startswith(area)]

            lista_pontos = list(amst_areas['ponto'].unique())

            for ponto in lista_pontos:
                areas_ponto = amst_areas[amst_areas['ponto'] == ponto]
                taxons = areas_ponto['taxon_final_curada'].to_frame()
                taxons = pd.DataFrame(taxons['taxon_final_curada'].unique())
                contagens.append(taxons)

            cont_ocorr = pd.concat(contagens, ignore_index=True)
            cont_ocorr = cont_ocorr.value_counts()
            cont_ocorr = pd.DataFrame(cont_ocorr)
            cont_ocorr = cont_ocorr.sort_values(by='count', ascending=False).reset_index()
            cont_ocorr = cont_ocorr.rename(columns={0: 'taxon', 'count': f'Detecções'})

    elif 'area_sampler' in df.columns:
        for area in lista_areas:
            amst_areas = df[df['area_sampler'].str.startswith(area)]

            lista_pontos = list(amst_areas['point'].unique())

            for ponto in lista_pontos:
                areas_ponto = amst_areas[amst_areas['point'] == ponto]
                taxons = areas_ponto['final_taxon_curated'].to_frame()
                taxons = pd.DataFrame(taxons['final_taxon_curated'].unique())
                contagens.append(taxons)

        cont_ocorr = pd.concat(contagens, ignore_index=True)
        cont_ocorr = cont_ocorr.value_counts()
        cont_ocorr = pd.DataFrame(cont_ocorr)
        cont_ocorr = cont_ocorr.sort_values(by='count', ascending=False).reset_index()
        cont_ocorr = cont_ocorr.rename(columns={0: 'taxon', 'count': f'Detections'})

    return cont_ocorr


def conta_reads_gerais(df):
    """Counts general taxon reads.

    Parameters:
    df (DataFrame): Dataframe with taxonomic assignment results and OTUs/ASVs equal or below the read threshold removed.

    Returns:
    df_reads_sp (DataFrame): Dataframe with total reads per taxon.
    """
    if 'taxon_final_curada' in df.columns:
        df_read_sp = df[['n_reads', 'taxon_final_curada']]
        df_read_sp = df_read_sp.groupby(by='taxon_final_curada').sum()
        df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
        df_read_sp = df_read_sp.rename(columns={'taxon_final_curada': 'taxon', 'n_reads': 'Reads'})
    elif 'final_taxon_curated' in df.columns:
        df_read_sp = df[['n_reads', 'final_taxon_curated']]
        df_read_sp = df_read_sp.groupby(by='final_taxon_curated').sum()
        df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
        df_read_sp = df_read_sp.rename(columns={'final_taxon_curated': 'taxon', 'n_reads': 'Reads'})

    return df_read_sp


def cria_lista_geral(ocorrencias, reads):
    """Creates a general taxon list.

    Parameters:
    ocorrencias (DataFrame): Dataframe with detection counts for each taxon.
    reads (DataFrame): Dataframe with read counts for each taxon.

    Returns:
    lista_geral (DataFrame): Final dataframe with detection and read counts for each taxon.
    """
    if 'taxon' in ocorrencias.columns:
        lista_geral = ocorrencias.merge(reads, how='outer', on='taxon')
    if 'taxon' in ocorrencias.columns:
        lista_geral = ocorrencias.merge(reads, how='outer', on='taxon')
    return lista_geral


def separa_areas(lista_areas, amostradores=None, df=None):
    """Filters the OTU/ASV table according to the areas.

    Parameters:
    lista_areas (list): List of area designations.
    amostradores (list): List with sampler designations.
    df (DataFrame): Dataframe with taxonomic assignment results and OTUs/ASVs equal or below the read threshold removed.

    Returns:
    amst (dict): Dictionary with dataframes separated by sampler.
    """
    if amostradores is not None:
        areas_amostradores = {}
        for amostrador in amostradores:
            tabela_amst = amostradores[amostrador]
            for area in lista_areas:
                if 'area_amostrador' in tabela_amst.columns:
                    areas_amostradores.setdefault(amostrador, []).append({area: tabela_amst[tabela_amst['area_amostrador'].str.contains(area)]})
                elif 'area_sampler' in tabela_amst.columns:
                    areas_amostradores.setdefault(amostrador, []).append({area: tabela_amst[tabela_amst['area_sampler'].str.contains(area)]})

        return areas_amostradores
    elif df is not None:
        areas = {}
        for area in lista_areas:
            if 'area_amostrador' in df.columns:
                areas[area] = df[df['area_amostrador'].str.contains(area)]
            elif 'area_sampler' in df.columns:
                areas[area] = df[df['area_sampler'].str.contains(area)]

        return areas


def conta_ocorrencias(dfs, amostradores=False, areas=False):
    """Counts taxon detections according to chosen filters (samplers and/or areas).

    Parameters:
    dfs (DataFrame): Filtered dataframes with taxonomic assignment results.
    amostradores (bool): Indicates filtering by sampler.
    areas (bool): Indicates filtering by area.

    Returns:
    ocorr (dict): Dictionary with dataframes containing detection counts per taxon.
    """
    ocorr = {}
    if amostradores and areas:
        for amostrador in dfs:
            tabelas_areas = dfs[amostrador]
            for tabela_area in tabelas_areas:
                for area, tabela in tabela_area.items():
                    if tabela.empty:
                        continue
                    if 'ponto' in tabela.columns:
                        pontos = tabela['ponto'].unique()
                        tabelas_taxons = []
                        for ponto in pontos:
                            df_ponto = tabela.loc[tabela['ponto'] == ponto]
                            taxons = df_ponto['taxon_final_curada'].unique()
                            df_taxons = pd.DataFrame(taxons, columns=[f'taxon'])
                            tabelas_taxons.append(df_taxons)

                        df_taxons = pd.concat(tabelas_taxons).reset_index()

                        df_ocorr = pd.DataFrame(df_taxons['taxon'].value_counts()).reset_index()
                        df_ocorr = df_ocorr.rename(columns={'taxon': 'Taxon', 'count': f'Detecções em {area}'})

                        ocorr.setdefault(amostrador, []).append({area: df_ocorr})
                    elif 'point' in tabela.columns:
                        pontos = tabela['point'].unique()
                        tabelas_taxons = []
                        for ponto in pontos:
                            df_ponto = tabela.loc[tabela['point'] == ponto]
                            taxons = df_ponto['final_taxon_curated'].unique()
                            df_taxons = pd.DataFrame(taxons, columns=[f'taxon'])
                            tabelas_taxons.append(df_taxons)

                        df_taxons = pd.concat(tabelas_taxons).reset_index()

                        df_ocorr = pd.DataFrame(df_taxons['taxon'].value_counts()).reset_index()
                        df_ocorr = df_ocorr.rename(columns={'taxon': 'Taxon', 'count': f'Detections in {area}'})

                        ocorr.setdefault(amostrador, []).append({area: df_ocorr})
        return ocorr

    elif amostradores and not areas:
        for amostrador in dfs:
            tabela = dfs[amostrador]
            if 'ponto' in tabela.columns:
                pontos = tabela['ponto'].unique()
                tabelas_taxons = []
                for ponto in pontos:
                    df_ponto = tabela.loc[tabela['ponto'] == ponto]
                    taxons = df_ponto['taxon_final_curada'].unique()
                    df_taxons = pd.DataFrame(taxons, columns=[f'taxon'])
                    tabelas_taxons.append(df_taxons)
                try:
                    df_taxons = pd.concat(tabelas_taxons).reset_index()
                except ValueError:
                    pass

                df_ocorr = pd.DataFrame(df_taxons['taxon'].value_counts()).reset_index()
                df_ocorr = df_ocorr.rename(columns={'taxon': 'Taxon', 'count': f'Detecções por {amostrador}'})

                ocorr.setdefault(amostrador, df_ocorr)
            elif 'point' in tabela.columns:
                pontos = tabela['point'].unique()
                tabelas_taxons = []
                for ponto in pontos:
                    df_ponto = tabela.loc[tabela['point'] == ponto]
                    taxons = df_ponto['final_taxon_curated'].unique()
                    df_taxons = pd.DataFrame(taxons, columns=[f'taxon'])
                    tabelas_taxons.append(df_taxons)
                try:
                    df_taxons = pd.concat(tabelas_taxons).reset_index()
                except ValueError:
                    pass

                df_ocorr = pd.DataFrame(df_taxons['taxon'].value_counts()).reset_index()
                df_ocorr = df_ocorr.rename(columns={'taxon': 'Taxon', 'count': f'Detections by {amostrador}'})

                ocorr.setdefault(amostrador, df_ocorr)

        return ocorr

    elif not amostradores and areas:
        for area in dfs:
            tabela = dfs[area]
            if 'ponto' in tabela.columns:
                pontos = tabela['ponto'].unique()
                tabelas_taxons = []
                for ponto in pontos:
                    df_ponto = tabela.loc[tabela['ponto'] == ponto]
                    taxons = df_ponto['taxon_final_curada'].unique()
                    df_taxons = pd.DataFrame(taxons, columns=[f'taxon'])
                    tabelas_taxons.append(df_taxons)
                try:
                    df_taxons = pd.concat(tabelas_taxons).reset_index()
                except ValueError:
                    pass

                df_ocorr = pd.DataFrame(df_taxons['taxon'].value_counts()).reset_index()
                df_ocorr = df_ocorr.rename(columns={'taxon': 'Taxon', 'count': f'Detecções em {area}'})

                ocorr.setdefault(area, df_ocorr)
            elif 'point' in tabela.columns:
                pontos = tabela['point'].unique()
                tabelas_taxons = []
                for ponto in pontos:
                    df_ponto = tabela.loc[tabela['point'] == ponto]
                    taxons = df_ponto['final_taxon_curated'].unique()
                    df_taxons = pd.DataFrame(taxons, columns=[f'taxon'])
                    tabelas_taxons.append(df_taxons)
                try:
                    df_taxons = pd.concat(tabelas_taxons).reset_index()
                except ValueError:
                    pass

                df_ocorr = pd.DataFrame(df_taxons['taxon'].value_counts()).reset_index()
                df_ocorr = df_ocorr.rename(columns={'taxon': 'Taxon', 'count': f'Detections in {area}'})

                ocorr.setdefault(area, df_ocorr)

        return ocorr


def calcula_reads_especie(dfs, amostrador=False, area=False):
    """Counts taxon detections according to chosen filters (samplers and/or areas).

    Parameters:
    dfs (DataFrame): Filtered dataframes with taxonomic assignment results.
    amostradores (bool): Indicates filtering by sampler.
    areas (bool): Indicates filtering by area.

    Returns:
    ocorr (dict): Dictionary with dataframes containing detection counts per taxon.
    """
    reads_especie = {}

    if amostrador and area:
        for amostrador in dfs:
            tabelas_areas = dfs[amostrador]
            for tabela_area in tabelas_areas:
                for area, tabela in tabela_area.items():
                    if 'taxon_final_curada' in tabela.columns:
                        df_read_sp = tabela[['n_reads', 'taxon_final_curada']]
                        df_read_sp = df_read_sp.groupby(by='taxon_final_curada').sum()
                        df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
                        df_read_sp = df_read_sp.rename(columns={'taxon_final_curada': 'Taxon', 'n_reads': 'Reads'})
                        reads_especie.setdefault(amostrador, []).append({area: df_read_sp})
                    elif 'final_taxon_curated' in tabela.columns:
                        df_read_sp = tabela[['n_reads', 'final_taxon_curated']]
                        df_read_sp = df_read_sp.groupby(by='final_taxon_curated').sum()
                        df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
                        df_read_sp = df_read_sp.rename(columns={'final_taxon_curated': 'Taxon', 'n_reads': 'Reads'})
                        reads_especie.setdefault(amostrador, []).append({area: df_read_sp})
        return reads_especie

    elif amostrador and not area:
        for amostrador in dfs:
            tabela = dfs[amostrador]
            if 'taxon_final_curada' in tabela.columns:
                df_read_sp = tabela[['n_reads', 'taxon_final_curada']]
                df_read_sp = df_read_sp.groupby(by='taxon_final_curada').sum()
                df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'taxon_final_curada': 'Taxon', 'n_reads': 'Reads'})
                reads_especie.setdefault(amostrador, df_read_sp)
            elif 'final_taxon_curated' in tabela.columns:
                df_read_sp = tabela[['n_reads', 'final_taxon_curated']]
                df_read_sp = df_read_sp.groupby(by='final_taxon_curated').sum()
                df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'final_taxon_curated': 'Taxon', 'n_reads': 'Reads'})
                reads_especie.setdefault(amostrador, df_read_sp)

        return reads_especie

    elif not amostrador and area:
        for area in dfs:
            tabela = dfs[area]
            if 'taxon_final_curada' in tabela.columns:
                df_read_sp = tabela[['n_reads', 'taxon_final_curada']]
                df_read_sp = df_read_sp.groupby(by='taxon_final_curada').sum()
                df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'taxon_final_curada': 'Taxon', 'n_reads': 'Reads'})
                reads_especie.setdefault(area, df_read_sp)
            elif 'final_taxon_curated' in tabela.columns:
                df_read_sp = tabela[['n_reads', 'final_taxon_curated']]
                df_read_sp = df_read_sp.groupby(by='final_taxon_curated').sum()
                df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'final_taxon_curated': 'Taxon', 'n_reads': 'Reads'})
                reads_especie.setdefault(area, df_read_sp)
        return reads_especie


def constroi_tabela_final(df_reads_sp, df_deteccoes, amostradores=False, areas=False):
    """Builds tables with consolidated results.

    Parameters:
    df_reads_sp (dict): Dictionary with dataframes of read counts per taxon.
    df_deteccoes (dict): Dictionary with dataframes of detection counts per taxon.
    amostradores (bool): Indicates filtering by sampler.
    areas (bool): Indicates filtering by area.

    Returns:
    tabelas_finais (dict): Dictionary with dataframes representing the final tables with results displayed according to the filters.
    """
    tabelas_finais = {}

    if amostradores and areas:
        for amostrador in df_reads_sp:
            tabelas_reads = df_reads_sp[amostrador]
            tabelas_ocorr = df_deteccoes[amostrador]
            for tabela_reads in tabelas_reads:
                for tabela_ocorr in tabelas_ocorr:
                    if tabela_ocorr.keys() == tabela_reads.keys():
                        reads_key = list(tabela_reads.keys())[0]
                        ocorr_key = list(tabela_ocorr.keys())[0]
                        tbl_rds = tabela_reads[reads_key]
                        tbl_ocr = tabela_ocorr[ocorr_key]
                        tabela_unida = tbl_rds.merge(tbl_ocr, how='outer', on='Taxon').sort_values('Reads', ascending=False).reset_index(drop=True)

                        tabelas_finais.setdefault(amostrador, []).append({reads_key: tabela_unida})
                    else:
                        continue
        return tabelas_finais

    elif amostradores and not areas:
        for amostrador in df_reads_sp:
            tabela_reads = df_reads_sp[amostrador]
            tabela_ocorr = df_deteccoes[amostrador]
            tabela_unida = tabela_reads.merge(tabela_ocorr, how='outer', on='Taxon').sort_values('Reads', ascending=False).reset_index(drop=True)

            tabelas_finais.setdefault(amostrador, tabela_unida)

        return tabelas_finais

    elif not amostradores and areas:
        for area in df_reads_sp:
            tabela_reads = df_reads_sp[area]
            tabela_ocorr = df_deteccoes[area]
            tabela_unida = tabela_reads.merge(tabela_ocorr, how='outer', on='Taxon').sort_values('Reads', ascending=False).reset_index(drop=True)

            tabelas_finais.setdefault(area, tabela_unida)

        return tabelas_finais


def salva_resultados(tabelas_finais, caminho_salvar, amostrador=False, area=False):
    """Saves result tables.

    Parameters:
    tabelas_finais (dict): Dictionary with dataframes representing the final tables with results displayed according to the filters.
    caminho_salvar (str): Path where the file will be saved.
    amostrador (bool): Indicates filtering by sampler.
    area (bool): Indicates filtering by area.
    """
    if amostrador and area:
        for amostrador in tabelas_finais:
            i = 0
            tbls_fns = tabelas_finais[amostrador]
            for tabela in tbls_fns:
                area = list(tabela.keys())[0]
                tabela_final = tabela[area]

                if '.xlsx' in caminho_salvar:
                    caminho_salvar_tratado = caminho_salvar.replace('.xlsx', '')
                    if i == 0:
                        with pd.ExcelWriter(caminho_salvar_tratado + f'_{amostrador}.xlsx', engine='openpyxl') as arquivo:
                            tabela_final.to_excel(arquivo, sheet_name=area)
                    else:
                        with pd.ExcelWriter(caminho_salvar_tratado + f'_{amostrador}.xlsx', engine='openpyxl', mode='a') as arquivo:
                            tabela_final.to_excel(arquivo, sheet_name=area)

                elif '.zip' in caminho_salvar:
                    caminho_salvar_tratado = caminho_salvar.replace('.zip', '')
                    if i == 0:
                        with zipfile.ZipFile(caminho_salvar_tratado + f'_{amostrador}.zip', "w") as zf:
                            with zf.open(f"{amostrador}_{area}.csv", "w") as buffer:
                                tabela_final.to_csv(buffer, sep=';', encoding='utf-8-sig')
                    else:
                        with zipfile.ZipFile(caminho_salvar_tratado + f'_{amostrador}.zip', "a") as zf:
                            with zf.open(f"{amostrador}_{area}.csv", "w") as buffer:
                                tabela_final.to_csv(buffer, sep=';', encoding='utf-8-sig')
                i += 1


    elif amostrador and not area:
        i = 0

        for amostrador in tabelas_finais:
            tabela_final = tabelas_finais[amostrador]

            if '.xlsx' in caminho_salvar:
                if i == 0:
                    with pd.ExcelWriter(caminho_salvar, engine='openpyxl') as arquivo:
                        tabela_final.to_excel(arquivo, sheet_name=amostrador)
                else:
                    with pd.ExcelWriter(caminho_salvar, engine='openpyxl', mode='a') as arquivo:
                        tabela_final.to_excel(arquivo, sheet_name=amostrador)
            elif '.zip' in caminho_salvar:
                if i == 0:
                    with zipfile.ZipFile(caminho_salvar, "w") as zf:
                        with zf.open(f"{amostrador}.csv", "w") as buffer:
                            tabela_final.to_csv(buffer, sep=';', encoding='utf-8-sig')
                else:
                    with zipfile.ZipFile(caminho_salvar, "a") as zf:
                        with zf.open(f"{amostrador}.csv", "w") as buffer:
                            tabela_final.to_csv(buffer, sep=';', encoding='utf-8-sig')

            i += 1

    elif not amostrador and area:
        i = 0

        for area in tabelas_finais:
            tabela_final = tabelas_finais[area]

            if 'xlsx' in caminho_salvar:
                if i == 0:
                    with pd.ExcelWriter(caminho_salvar, engine='openpyxl') as arquivo:
                        tabela_final.to_excel(arquivo, sheet_name=area)
                else:
                    with pd.ExcelWriter(caminho_salvar, engine='openpyxl', mode='a') as arquivo:
                        tabela_final.to_excel(arquivo, sheet_name=area)
            elif '.zip' in caminho_salvar:
                if i == 0:
                    with zipfile.ZipFile(caminho_salvar, "w") as zf:
                        with zf.open(f"{area}.csv", "w") as buffer:
                            tabela_final.to_csv(buffer, sep=';', encoding='utf-8-sig')
                else:
                    with zipfile.ZipFile(caminho_salvar, "a") as zf:
                        with zf.open(f"{area}.csv", "w") as buffer:
                            tabela_final.to_csv(buffer, sep=';', encoding='utf-8-sig')
            i += 1


def main():
    pass


if __name__ == "__main__":
    main()
