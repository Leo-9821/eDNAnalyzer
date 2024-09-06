import pandas as pd
import zipfile


def separa_corridas(df):
    """Separa o dataframe completo nas suas corridas.

    Parameters:
    df (pandas.core.frame.DataFrame): Base de dados com os resultados do metabarcoding após Blast.

    Returns:
    areas (dict): Dicionário com os dataframes identificados por chaves com os nomes informados na lista de corridas.
    """
    if 'Corrida' in df.columns:
        lista_corridas = list(df['Corrida'].unique())
    elif 'Run' in df.columns:
        lista_corridas = list(df['Run'].unique())

    corridas = {}
    for corrida in lista_corridas:
        nome_corrida = corrida
        if 'Corrida' in df.columns:
            corridas[nome_corrida] = df[df['Corrida'] == corrida]
        elif 'Run' in df.columns:
            corridas[nome_corrida] = df[df['Run'] == corrida]

    return corridas


def aplica_threshold(corridas, threshold_perc):
    """Calcula o threshold de reads para cada corrida e retira as OTUs que estiverem abaixo.

    Parameters:
    corridas (dict): Bases de dados para cada corrida organizadas em dicionário.
    threshold_perc (float): valor da porcentagem para cálculo do threshold.

    Returns:
    selecionados (dict): Dicionário com os dataframes com OTUs selecionadas.
    nao_selecionados (dict): Dicionário com dataframes com OTUs eliminadas.
    df_thresholds (DataFrame): Dataframe com os valores dos thresholds calculados por corrida.
    """
    thresholds = {}
    selecionados = {}
    nao_selecionados = {}

    for corrida in corridas:
        df = corridas[corrida]
        reads = df['N_reads']
        total_reads = sum(reads)
        threshold = total_reads * threshold_perc / 100

        thresholds[corrida] = threshold

        selecionado = df.loc[df['N_reads'] > threshold]
        selecionados[corrida] = selecionado

        nao_selecionado = df.loc[df['N_reads'] <= threshold]
        nao_selecionados[corrida] = nao_selecionado

    df_thresholds = pd.DataFrame.from_dict(thresholds, orient='index')
    df_thresholds = df_thresholds.rename(columns={0: 'Threshold'})
    return selecionados, nao_selecionados, df_thresholds


def concatena_dfs(dfs):
    """Concatena dataframes de um dicionário.

    Parameters:
    dfs (dict): Dataframes organizados em um dicionário.

    Returns:
    tabelas_concatenadas (DataFrame): Dataframe resultante da concatenação dos dataframes.
    """
    tabelas = dfs.values()
    tabelas_concatenadas = pd.concat(tabelas, ignore_index=True)
    return tabelas_concatenadas


def define_areas(df):
    """Cria lista de áreas amostrais.

    Parameters:
    df (DataFrame): Dataframes com resultados da atribuição taxonômica e com retirada das OTUs abaixo do threshold de reads.

    Returns:
    lista_areas (list): Lista de áreas amostrais.
    """
    if 'Amostra' in df.columns:
        lista_amostras = df['Amostra'].unique()
    elif 'Sample' in df.columns:
        lista_amostras = df['Sample'].unique()

    for i in range(len(lista_amostras)):
        lista_amostras[i] = tuple(lista_amostras[i].split('_'))

    lista_areas = []

    for area, parcela in lista_amostras:
        lista_areas.append(area)

    lista_areas = list(set(lista_areas))

    return lista_areas


def separa_amostradores(df, amostradores):
    """Filtra tabela de OTUs de acordo com o amostrador.

    Parameters:
    df (DataFrame): Dataframes com resultados da atribuição taxonômica e com retirada das OTUs abaixo do threshold de reads.
    amostradores (list): Lista com denominação dos amostradores.

    Returns:
    amst (dict): Dicionário com dataframes separados por amostrador.
    """
    amst = {}
    for amostrador in amostradores:
        if 'Amostra' in df.columns:
            amst[amostrador] = df[df['Amostra'].str.contains(amostrador)]
        elif 'Sample' in df.columns:
            amst[amostrador] = df[df['Sample'].str.contains(amostrador)]

    return amst


def conta_ocorrencias_gerais(df, lista_areas):
    contagens = []

    for area in lista_areas:
        amst_areas = df[df['Amostra'].str.startswith(area)]

        lista_pontos = list(amst_areas['Ponto'].unique())

        for ponto in lista_pontos:
            areas_ponto = amst_areas[amst_areas['Ponto'] == ponto]
            taxons = areas_ponto['OTUFinal'].to_frame()
            taxons = pd.DataFrame(taxons['OTUFinal'].unique())
            contagens.append(taxons)

    cont_ocorr = pd.concat(contagens, ignore_index=True)
    cont_ocorr = cont_ocorr.value_counts()
    cont_ocorr = pd.DataFrame(cont_ocorr)
    cont_ocorr = cont_ocorr.sort_values(by='count', ascending=False).reset_index()
    cont_ocorr = cont_ocorr.rename(columns={0: 'Táxon', 'count': f'Detecções'})

    return cont_ocorr


def conta_reads_gerais(df):
    if 'OTUFinal' in df.columns:
        df_read_sp = df[['N_reads', 'OTUFinal']]
        df_read_sp = df_read_sp.groupby(by='OTUFinal').sum()
        df_read_sp = df_read_sp.sort_values(by='N_reads', ascending=False).reset_index()
        df_read_sp = df_read_sp.rename(columns={'OTUFinal': 'Táxon', 'N_reads': 'Reads'})
    elif 'FinalOTU' in df.columns:
        df_read_sp = df[['N_reads', 'FinalOTU']]
        df_read_sp = df_read_sp.groupby(by='FinalOTU').sum()
        df_read_sp = df_read_sp.sort_values(by='N_reads', ascending=False).reset_index()
        df_read_sp = df_read_sp.rename(columns={'FinalOTU': 'Taxon', 'N_reads': 'Reads'})

    return df_read_sp


def cria_lista_geral(ocorrencias, reads):
    """Cria lista de táxons geral.

    Parameters:
    ocorrencias (DataFrame): DataFrame com contagem de detecções para cada táxon.
    reads (DataFrame): DataFrame com contagem de reads para cada táxon.

    Returns:
    lista_geral (DataFrame): Dataframe final com contagens de detecções e reads de cada táxon.
    """
    lista_geral = ocorrencias.merge(reads, how='outer', on='Táxon')
    return lista_geral


def separa_areas(lista_areas, amostradores=None, df=None):
    """Filtra tabela de OTUs de acordo com as áreas.

    Parameters:
    lista_areas (list): Lista das denominação das áreas
    amostradores (list): Lista com denominação dos amostradores.
    df (DataFrame): Dataframes com resultados da atribuição taxonômica e com retirada das OTUs abaixo do threshold de reads.

    Returns:
    amst (dict): Dicionário com dataframes separados por amostrador.
    """
    if amostradores is not None:
        areas_amostradores = {}
        for amostrador in amostradores:
            tabela_amst = amostradores[amostrador]
            for area in lista_areas:
                if 'Amostra' in tabela_amst.columns:
                    areas_amostradores.setdefault(amostrador, []).append({area: tabela_amst[tabela_amst['Amostra'].str.contains(area)]})
                elif 'Sample' in tabela_amst.columns:
                    areas_amostradores.setdefault(amostrador, []).append({area: tabela_amst[tabela_amst['Sample'].str.contains(area)]})

        return areas_amostradores
    elif df is not None:
        areas = {}
        for area in lista_areas:
            if 'Amostra' in df.columns:
                areas[area] = df[df['Amostra'].str.contains(area)]
            elif 'Sample' in df.columns:
                areas[area] = df[df['Sample'].str.contains(area)]

        return areas


def conta_ocorrencia_aliquotas(dfs, amostradores=False, areas=False):
    ocorr = {}
    if amostradores and areas:
        for amostrador in dfs:
            tabelas_areas = dfs[amostrador]
            for tabela_area in tabelas_areas:
                for area, tabela in tabela_area.items():
                    if tabela.empty:
                        continue
                    if 'Ponto' in tabela.columns:
                        pontos = tabela['Ponto'].unique()
                        tabelas_taxons = []
                        for ponto in pontos:
                            df_ponto = tabela.loc[tabela['Ponto'] == ponto]
                            taxons = df_ponto['OTUFinal'].unique()
                            df_taxons = pd.DataFrame(taxons, columns=[f'Táxon'])
                            tabelas_taxons.append(df_taxons)

                        df_taxons = pd.concat(tabelas_taxons).reset_index()

                        df_ocorr = pd.DataFrame(df_taxons['Táxon'].value_counts()).reset_index()
                        df_ocorr = df_ocorr.rename(columns={'count': f'Detecções em {area}'})

                        ocorr.setdefault(amostrador, []).append({area: df_ocorr})
                    elif 'Point' in tabela.columns:
                        pontos = tabela['Point'].unique()
                        tabelas_taxons = []
                        for ponto in pontos:
                            df_ponto = tabela.loc[tabela['Point'] == ponto]
                            taxons = df_ponto['FinalOTU'].unique()
                            df_taxons = pd.DataFrame(taxons, columns=[f'Taxon'])
                            tabelas_taxons.append(df_taxons)

                        df_taxons = pd.concat(tabelas_taxons).reset_index()

                        df_ocorr = pd.DataFrame(df_taxons['Taxon'].value_counts()).reset_index()
                        df_ocorr = df_ocorr.rename(columns={'count': f'Detections in {area}'})

                        ocorr.setdefault(amostrador, []).append({area: df_ocorr})
        return ocorr

    elif amostradores and not areas:
        for amostrador in dfs:
            tabela = dfs[amostrador]
            if 'Ponto' in tabela.columns:
                pontos = tabela['Ponto'].unique()
                tabelas_taxons = []
                for ponto in pontos:
                    df_ponto = tabela.loc[tabela['Ponto'] == ponto]
                    taxons = df_ponto['OTUFinal'].unique()
                    df_taxons = pd.DataFrame(taxons, columns=[f'Táxon'])
                    tabelas_taxons.append(df_taxons)
                try:
                    df_taxons = pd.concat(tabelas_taxons).reset_index()
                except ValueError:
                    pass

                df_ocorr = pd.DataFrame(df_taxons['Táxon'].value_counts())
                df_ocorr = df_ocorr.rename(columns={'count': f'Detecções por {amostrador}'})

                ocorr.setdefault(amostrador, df_ocorr)
            elif 'Point' in tabela.columns:
                pontos = tabela['Point'].unique()
                tabelas_taxons = []
                for ponto in pontos:
                    df_ponto = tabela.loc[tabela['Point'] == ponto]
                    taxons = df_ponto['FinalOTU'].unique()
                    df_taxons = pd.DataFrame(taxons, columns=[f'Taxon'])
                    tabelas_taxons.append(df_taxons)
                try:
                    df_taxons = pd.concat(tabelas_taxons).reset_index()
                except ValueError:
                    pass

                df_ocorr = pd.DataFrame(df_taxons['Taxon'].value_counts())
                df_ocorr = df_ocorr.rename(columns={'count': f'Detections by {amostrador}'})

                ocorr.setdefault(amostrador, df_ocorr)

        return ocorr

    elif not amostradores and areas:
        for area in dfs:
            tabela = dfs[area]
            if 'Ponto' in tabela.columns:
                pontos = tabela['Ponto'].unique()
                tabelas_taxons = []
                for ponto in pontos:
                    df_ponto = tabela.loc[tabela['Ponto'] == ponto]
                    taxons = df_ponto['OTUFinal'].unique()
                    df_taxons = pd.DataFrame(taxons, columns=[f'Táxon'])
                    tabelas_taxons.append(df_taxons)
                try:
                    df_taxons = pd.concat(tabelas_taxons).reset_index()
                except ValueError:
                    pass

                df_ocorr = pd.DataFrame(df_taxons['Táxon'].value_counts())
                df_ocorr = df_ocorr.rename(columns={'count': f'Detecções em {area}'})

                ocorr.setdefault(area, df_ocorr)
            elif 'Point' in tabela.columns:
                pontos = tabela['Point'].unique()
                tabelas_taxons = []
                for ponto in pontos:
                    df_ponto = tabela.loc[tabela['Point'] == ponto]
                    taxons = df_ponto['FinalOTU'].unique()
                    df_taxons = pd.DataFrame(taxons, columns=[f'Taxon'])
                    tabelas_taxons.append(df_taxons)
                try:
                    df_taxons = pd.concat(tabelas_taxons).reset_index()
                except ValueError:
                    pass

                df_ocorr = pd.DataFrame(df_taxons['Taxon'].value_counts())
                df_ocorr = df_ocorr.rename(columns={'count': f'Detections in {area}'})

                ocorr.setdefault(area, df_ocorr)

        return ocorr


def conta_ocorrencias(dfs, amostrador=False, area=False):  # Conferir se está funcionando certo, pois pode estar dando resultado errado, a função para alíquotas talvez seja a correta
    ocorr = {}

    if amostrador and area:
        for amostrador in dfs:
            tabelas_areas = dfs[amostrador]
            for tabela_area in tabelas_areas:
                for area, tabela in tabela_area.items():
                    if 'OTUFinal' in tabela.columns:
                        df_area = tabela['OTUFinal'].value_counts()
                        df_area = pd.DataFrame(df_area)
                        df_area = df_area.sort_values(by='count').reset_index()
                        df_area = df_area.rename(columns={'OTUFinal': 'Táxon', 'count': f'Detecções em {area}'})
                        ocorr.setdefault(amostrador, []).append({area: df_area})
                    elif 'FinalOTU' in tabela.columns:
                        df_area = tabela['FinalOTU'].value_counts()
                        df_area = pd.DataFrame(df_area)
                        df_area = df_area.sort_values(by='count').reset_index()
                        df_area = df_area.rename(columns={'FinalOTU': 'Taxon', 'count': f'Detections in {area}'})
                        ocorr.setdefault(amostrador, []).append({area: df_area})

        return ocorr

    elif amostrador and not area:
        for amostrador in dfs:
            tabela = dfs[amostrador]
            if 'OTUFinal' in tabela.columns:
                df_area = tabela['OTUFinal'].value_counts()
                df_area = pd.DataFrame(df_area)
                df_area = df_area.sort_values(by='count').reset_index()
                df_area = df_area.rename(columns={'OTUFinal': 'Táxon', 'count': f'Detecções com {amostrador}'})
                ocorr.setdefault(amostrador, df_area)
            elif 'FinalOTU' in tabela.columns:
                df_area = tabela['FinalOTU'].value_counts()
                df_area = pd.DataFrame(df_area)
                df_area = df_area.sort_values(by='count').reset_index()
                df_area = df_area.rename(columns={'FinalOTU': 'Taxon', 'count': f'Detections by {amostrador}'})
                ocorr.setdefault(amostrador, df_area)


        return ocorr

    elif not amostrador and area:
        for area in dfs:
            tabela = dfs[area]
            if 'OTUFinal' in tabela.columns:
                df_area = tabela['OTUFinal'].value_counts()
                df_area = pd.DataFrame(df_area)
                df_area = df_area.sort_values(by='count').reset_index()
                df_area = df_area.rename(columns={'OTUFinal': 'Táxon', 'count': f'Detecções em {area}'})
                ocorr.setdefault(area, df_area)
            elif 'FinalOTU' in tabela.columns:
                df_area = tabela['FinalOTU'].value_counts()
                df_area = pd.DataFrame(df_area)
                df_area = df_area.sort_values(by='count').reset_index()
                df_area = df_area.rename(columns={'FinalOTU': 'Taxon', 'count': f'Detections in {area}'})
                ocorr.setdefault(area, df_area)

        return ocorr





def calcula_reads_especie(dfs, amostrador=False, area=False):
    reads_especie = {}

    if amostrador and area:
        for amostrador in dfs:
            tabelas_areas = dfs[amostrador]
            for tabela_area in tabelas_areas:
                for area, tabela in tabela_area.items():
                    if 'OTUFinal' in tabela.columns:
                        df_read_sp = tabela[['N_reads', 'OTUFinal']]
                        df_read_sp = df_read_sp.groupby(by='OTUFinal').sum()
                        df_read_sp = df_read_sp.sort_values(by='N_reads', ascending=False).reset_index()
                        df_read_sp = df_read_sp.rename(columns={'OTUFinal': 'Táxon', 'N_reads': 'Reads'})
                        reads_especie.setdefault(amostrador, []).append({area: df_read_sp})
                    elif 'FinalOTU' in tabela.columns:
                        df_read_sp = tabela[['N_reads', 'FinalOTU']]
                        df_read_sp = df_read_sp.groupby(by='FinalOTU').sum()
                        df_read_sp = df_read_sp.sort_values(by='N_reads', ascending=False).reset_index()
                        df_read_sp = df_read_sp.rename(columns={'FinalOTU': 'Taxon', 'N_reads': 'Reads'})
                        reads_especie.setdefault(amostrador, []).append({area: df_read_sp})
        return reads_especie

    elif amostrador and not area:
        for amostrador in dfs:
            tabela = dfs[amostrador]
            if 'OTUFinal' in tabela.columns:
                df_read_sp = tabela[['N_reads', 'OTUFinal']]
                df_read_sp = df_read_sp.groupby(by='OTUFinal').sum()
                df_read_sp = df_read_sp.sort_values(by='N_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'OTUFinal': 'Táxon', 'N_reads': 'Reads'})
                reads_especie.setdefault(amostrador, df_read_sp)
            elif 'FinalOTU' in tabela.columns:
                df_read_sp = tabela[['N_reads', 'FinalOTU']]
                df_read_sp = df_read_sp.groupby(by='FinalOTU').sum()
                df_read_sp = df_read_sp.sort_values(by='N_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'FinalOTU': 'Taxon', 'N_reads': 'Reads'})
                reads_especie.setdefault(amostrador, df_read_sp)

        return reads_especie

    elif not amostrador and area:
        for area in dfs:
            tabela = dfs[area]
            if 'OTUFinal' in tabela.columns:
                df_read_sp = tabela[['N_reads', 'OTUFinal']]
                df_read_sp = df_read_sp.groupby(by='OTUFinal').sum()
                df_read_sp = df_read_sp.sort_values(by='N_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'OTUFinal': 'Táxon', 'N_reads': 'Reads'})
                reads_especie.setdefault(area, df_read_sp)
            elif 'FinalOTU' in tabela.columns:
                df_read_sp = tabela[['N_reads', 'FinalOTU']]
                df_read_sp = df_read_sp.groupby(by='FinalOTU').sum()
                df_read_sp = df_read_sp.sort_values(by='N_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'FinalOTU': 'Taxon', 'N_reads': 'Reads'})
                reads_especie.setdefault(area, df_read_sp)

        return reads_especie


def constroi_tabela_final(df_reads_sp, df_deteccoes, amostradores=False, areas=False):
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
                        if 'Táxon' in tbl_rds.columns:
                            tabela_unida = tbl_rds.merge(tbl_ocr, how='outer', on='Táxon')
                        elif 'Taxon' in tbl_rds.columns:
                            tabela_unida = tbl_rds.merge(tbl_ocr, how='outer', on='Taxon')
                        tabelas_finais.setdefault(amostrador, []).append({reads_key: tabela_unida})
                    else:
                        continue
        return tabelas_finais

    elif amostradores and not areas:
        for amostrador in df_reads_sp:
            tabela_reads = df_reads_sp[amostrador]
            tabela_ocorr = df_deteccoes[amostrador]
            if 'Táxon' in tabela_reads.columns:
                tabela_unida = tabela_reads.merge(tabela_ocorr, how='outer', on='Táxon')
            if 'Taxon' in tabela_reads.columns:
                tabela_unida = tabela_reads.merge(tabela_ocorr, how='outer', on='Taxon')
            tabelas_finais.setdefault(amostrador, tabela_unida)

        return tabelas_finais

    elif not amostradores and areas:
        for area in df_reads_sp:
            tabela_reads = df_reads_sp[area]
            tabela_ocorr = df_deteccoes[area]
            if 'Táxon' in tabela_reads.columns:
                tabela_unida = tabela_reads.merge(tabela_ocorr, how='outer', on='Táxon')
            if 'Taxon' in tabela_reads.columns:
                tabela_unida = tabela_reads.merge(tabela_ocorr, how='outer', on='Taxon')
            tabelas_finais.setdefault(area, tabela_unida)

        return tabelas_finais


def salva_resultados(tabelas_finais, caminho_salvar, amostrador=False, area=False):
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
                                tabela_final.to_csv(buffer, encoding='utf-8')
                    else:
                        with zipfile.ZipFile(caminho_salvar_tratado + f'_{amostrador}.zip', "a") as zf:
                            with zf.open(f"{amostrador}_{area}.csv", "w") as buffer:
                                tabela_final.to_csv(buffer, encoding='utf-8')
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
                            tabela_final.to_csv(buffer, encoding='utf-8')
                else:
                    with zipfile.ZipFile(caminho_salvar, "a") as zf:
                        with zf.open(f"{amostrador}.csv", "w") as buffer:
                            tabela_final.to_csv(buffer, encoding='utf-8')

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
                            tabela_final.to_csv(buffer, encoding='utf-8')
                else:
                    with zipfile.ZipFile(caminho_salvar, "a") as zf:
                        with zf.open(f"{area}.csv", "w") as buffer:
                            tabela_final.to_csv(buffer, encoding='utf-8')
            i += 1


def main():
    pass


if __name__ == "__main__":
    main()
