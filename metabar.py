import pandas as pd
import zipfile


def separa_corridas(df):
    """Separa o dataframe completo nas suas corridas.

    Parameters:
    df (pandas.core.frame.DataFrame): Base de dados com os resultados do metabarcoding após Blast.

    Returns:
    areas (dict): Dicionário com os dataframes identificados por chaves com os nomes informados na lista de corridas.
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
    """Filtra tabela de OTUs de acordo com o amostrador.

    Parameters:
    df (DataFrame): Dataframes com resultados da atribuição taxonômica e com retirada das OTUs abaixo do threshold de reads.
    amostradores (list): Lista com denominação dos amostradores.

    Returns:
    amst (dict): Dicionário com dataframes separados por amostrador.
    """
    amst = {}
    for amostrador in amostradores:
        if 'area_amostrador' in df.columns:
            amst[amostrador] = df[df['area_amostrador'].str.contains(amostrador)]
        elif 'area_sampler' in df.columns:
            amst[amostrador] = df[df['area_sampler'].str.contains(amostrador)]

    return amst


def conta_ocorrencias_gerais(df, lista_areas):
    """Conta detecções gerais dos táxons.

    Parameters:
    df (DataFrame): Dataframes com resultados da atribuição taxonômica e com retirada das OTUs abaixo do threshold de reads.
    lista_areas (list): Lista de áreas amostrais.

    Returns:
    cont_ocorr (DataFrame): DataFrame com número de detecções gerais por táxon.
    """
    contagens = []
    if 'area_amostrador' in df.columns:
        for area in lista_areas:
            amst_areas = df[df['area_amostrador'].str.startswith(area)]

            lista_pontos = list(amst_areas['ponto'].unique())

            for ponto in lista_pontos:
                areas_ponto = amst_areas[amst_areas['ponto'] == ponto]
                taxons = areas_ponto['otu_final'].to_frame()
                taxons = pd.DataFrame(taxons['otu_final'].unique())
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
                taxons = areas_ponto['final_otu'].to_frame()
                taxons = pd.DataFrame(taxons['final_otu'].unique())
                contagens.append(taxons)

        cont_ocorr = pd.concat(contagens, ignore_index=True)
        cont_ocorr = cont_ocorr.value_counts()
        cont_ocorr = pd.DataFrame(cont_ocorr)
        cont_ocorr = cont_ocorr.sort_values(by='count', ascending=False).reset_index()
        cont_ocorr = cont_ocorr.rename(columns={0: 'taxon', 'count': f'Detections'})

    return cont_ocorr


def conta_reads_gerais(df):
    """Conta reads gerais dos táxons.

    Parameters:
    df (DataFrame): Dataframes com resultados da atribuição taxonômica e com retirada das OTUs abaixo do threshold de reads.

    Returns:
    df_reads_sp (DataFrame): DataFrame com soma de reads gerais por táxon.
    """
    if 'otu_final' in df.columns:
        df_read_sp = df[['n_reads', 'otu_final']]
        df_read_sp = df_read_sp.groupby(by='otu_final').sum()
        df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
        df_read_sp = df_read_sp.rename(columns={'otu_final': 'taxon', 'n_reads': 'Reads'})
    elif 'final_otu' in df.columns:
        df_read_sp = df[['n_reads', 'final_otu']]
        df_read_sp = df_read_sp.groupby(by='final_otu').sum()
        df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
        df_read_sp = df_read_sp.rename(columns={'final_otu': 'taxon', 'n_reads': 'Reads'})

    return df_read_sp


def cria_lista_geral(ocorrencias, reads):
    """Cria lista de táxons geral.

    Parameters:
    ocorrencias (DataFrame): DataFrame com contagem de detecções para cada táxon.
    reads (DataFrame): DataFrame com contagem de reads para cada táxon.

    Returns:
    lista_geral (DataFrame): Dataframe final com contagens de detecções e reads de cada táxon.
    """
    if 'taxon' in ocorrencias.columns:
        lista_geral = ocorrencias.merge(reads, how='outer', on='taxon')
    if 'taxon' in ocorrencias.columns:
        lista_geral = ocorrencias.merge(reads, how='outer', on='taxon')
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
    """Conta detecções dos táxons de acordo com filtragens escolhidas (amostradores e/ou áreas).

    Parameters:
    dfs (DataFrame): Dataframes com resultados filtrados da atribuição taxonômica
    amostradores (bool): indica filtragem por amostrador.
    areas (bool): indica filtragem por área.

    Returns:
    ocorr (dict): dicionário com DataFrames com número de detecções por táxon.
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
                            taxons = df_ponto['otu_final'].unique()
                            df_taxons = pd.DataFrame(taxons, columns=[f'taxon'])
                            tabelas_taxons.append(df_taxons)

                        df_taxons = pd.concat(tabelas_taxons).reset_index()

                        df_ocorr = pd.DataFrame(df_taxons['taxon'].value_counts()).reset_index()
                        df_ocorr = df_ocorr.rename(columns={'count': f'Detecções em {area}'})

                        ocorr.setdefault(amostrador, []).append({area: df_ocorr})
                    elif 'point' in tabela.columns:
                        pontos = tabela['point'].unique()
                        tabelas_taxons = []
                        for ponto in pontos:
                            df_ponto = tabela.loc[tabela['point'] == ponto]
                            taxons = df_ponto['final_otu'].unique()
                            df_taxons = pd.DataFrame(taxons, columns=[f'taxon'])
                            tabelas_taxons.append(df_taxons)

                        df_taxons = pd.concat(tabelas_taxons).reset_index()

                        df_ocorr = pd.DataFrame(df_taxons['taxon'].value_counts()).reset_index()
                        df_ocorr = df_ocorr.rename(columns={'count': f'Detections in {area}'})

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
                    taxons = df_ponto['otu_final'].unique()
                    df_taxons = pd.DataFrame(taxons, columns=[f'taxon'])
                    tabelas_taxons.append(df_taxons)
                try:
                    df_taxons = pd.concat(tabelas_taxons).reset_index()
                except ValueError:
                    pass

                df_ocorr = pd.DataFrame(df_taxons['taxon'].value_counts())
                df_ocorr = df_ocorr.rename(columns={'count': f'Detecções por {amostrador}'})

                ocorr.setdefault(amostrador, df_ocorr)
            elif 'point' in tabela.columns:
                pontos = tabela['point'].unique()
                tabelas_taxons = []
                for ponto in pontos:
                    df_ponto = tabela.loc[tabela['point'] == ponto]
                    taxons = df_ponto['final_otu'].unique()
                    df_taxons = pd.DataFrame(taxons, columns=[f'taxon'])
                    tabelas_taxons.append(df_taxons)
                try:
                    df_taxons = pd.concat(tabelas_taxons).reset_index()
                except ValueError:
                    pass

                df_ocorr = pd.DataFrame(df_taxons['taxon'].value_counts())
                df_ocorr = df_ocorr.rename(columns={'count': f'Detections by {amostrador}'})

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
                    taxons = df_ponto['otu_final'].unique()
                    df_taxons = pd.DataFrame(taxons, columns=[f'taxon'])
                    tabelas_taxons.append(df_taxons)
                try:
                    df_taxons = pd.concat(tabelas_taxons).reset_index()
                except ValueError:
                    pass

                df_ocorr = pd.DataFrame(df_taxons['taxon'].value_counts())
                df_ocorr = df_ocorr.rename(columns={'count': f'Detecções em {area}'})

                ocorr.setdefault(area, df_ocorr)
            elif 'point' in tabela.columns:
                pontos = tabela['point'].unique()
                tabelas_taxons = []
                for ponto in pontos:
                    df_ponto = tabela.loc[tabela['point'] == ponto]
                    taxons = df_ponto['final_otu'].unique()
                    df_taxons = pd.DataFrame(taxons, columns=[f'taxon'])
                    tabelas_taxons.append(df_taxons)
                try:
                    df_taxons = pd.concat(tabelas_taxons).reset_index()
                except ValueError:
                    pass

                df_ocorr = pd.DataFrame(df_taxons['taxon'].value_counts())
                df_ocorr = df_ocorr.rename(columns={'count': f'Detections in {area}'})

                ocorr.setdefault(area, df_ocorr)

        return ocorr


def calcula_reads_especie(dfs, amostrador=False, area=False):
    """Conta detecções dos táxons de acordo com filtragens escolhidas (amostradores e/ou áreas).

    Parameters:
    dfs (DataFrame): Dataframes filtrados com resultados da atribuição taxonômica
    amostradores (bool): indica filtragem por amostrador.
    areas (bool): indica filtragem por área.

    Returns:
    ocorr (dict): dicionário com DataFrames com número de detecções por táxon.
    """
    reads_especie = {}

    if amostrador and area:
        for amostrador in dfs:
            tabelas_areas = dfs[amostrador]
            for tabela_area in tabelas_areas:
                for area, tabela in tabela_area.items():
                    if 'otu_final' in tabela.columns:
                        df_read_sp = tabela[['n_reads', 'otu_final']]
                        df_read_sp = df_read_sp.groupby(by='otu_final').sum()
                        df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
                        df_read_sp = df_read_sp.rename(columns={'otu_final': 'taxon', 'n_reads': 'Reads'})
                        reads_especie.setdefault(amostrador, []).append({area: df_read_sp})
                    elif 'final_otu' in tabela.columns:
                        df_read_sp = tabela[['n_reads', 'final_otu']]
                        df_read_sp = df_read_sp.groupby(by='final_otu').sum()
                        df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
                        df_read_sp = df_read_sp.rename(columns={'final_otu': 'taxon', 'n_reads': 'Reads'})
                        reads_especie.setdefault(amostrador, []).append({area: df_read_sp})
        return reads_especie

    elif amostrador and not area:
        for amostrador in dfs:
            tabela = dfs[amostrador]
            if 'otu_final' in tabela.columns:
                df_read_sp = tabela[['n_reads', 'otu_final']]
                df_read_sp = df_read_sp.groupby(by='otu_final').sum()
                df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'otu_final': 'taxon', 'n_reads': 'Reads'})
                reads_especie.setdefault(amostrador, df_read_sp)
            elif 'final_otu' in tabela.columns:
                df_read_sp = tabela[['n_reads', 'final_otu']]
                df_read_sp = df_read_sp.groupby(by='final_otu').sum()
                df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'final_otu': 'taxon', 'n_reads': 'Reads'})
                reads_especie.setdefault(amostrador, df_read_sp)

        return reads_especie

    elif not amostrador and area:
        for area in dfs:
            tabela = dfs[area]
            if 'otu_final' in tabela.columns:
                df_read_sp = tabela[['n_reads', 'otu_final']]
                df_read_sp = df_read_sp.groupby(by='otu_final').sum()
                df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'otu_final': 'taxon', 'n_reads': 'Reads'})
                reads_especie.setdefault(area, df_read_sp)
            elif 'final_otu' in tabela.columns:
                df_read_sp = tabela[['n_reads', 'final_otu']]
                df_read_sp = df_read_sp.groupby(by='final_otu').sum()
                df_read_sp = df_read_sp.sort_values(by='n_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'final_otu': 'taxon', 'n_reads': 'Reads'})
                reads_especie.setdefault(area, df_read_sp)

        return reads_especie


def constroi_tabela_final(df_reads_sp, df_deteccoes, amostradores=False, areas=False):
    """Conta detecções dos táxons de acordo com filtragens escolhidas (amostradores e/ou áreas).

    Parameters:
    df_reads_sp (dict): dicionário com DataFrames de número de reads por táxon.
    df_deteccoes (dict): dicionário com DataFrames de número de detecções por táxon.
    amostradores (bool): indica filtragem por amostrador.
    areas (bool): indica filtragem por área.

    Returns:
    tabelas_finais (dict): dicionario com DataFrames que representam as tabelas finais com os resultados apresentados de acordo com as filtragens.
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
                        if 'taxon' in tbl_rds.columns:
                            tabela_unida = tbl_rds.merge(tbl_ocr, how='outer', on='taxon')
                        elif 'taxon' in tbl_rds.columns:
                            tabela_unida = tbl_rds.merge(tbl_ocr, how='outer', on='taxon')
                        tabelas_finais.setdefault(amostrador, []).append({reads_key: tabela_unida})
                    else:
                        continue
        return tabelas_finais

    elif amostradores and not areas:
        for amostrador in df_reads_sp:
            tabela_reads = df_reads_sp[amostrador]
            tabela_ocorr = df_deteccoes[amostrador]
            if 'taxon' in tabela_reads.columns:
                tabela_unida = tabela_reads.merge(tabela_ocorr, how='outer', on='taxon')
            if 'taxon' in tabela_reads.columns:
                tabela_unida = tabela_reads.merge(tabela_ocorr, how='outer', on='taxon')
            tabelas_finais.setdefault(amostrador, tabela_unida)

        return tabelas_finais

    elif not amostradores and areas:
        for area in df_reads_sp:
            tabela_reads = df_reads_sp[area]
            tabela_ocorr = df_deteccoes[area]
            if 'taxon' in tabela_reads.columns:
                tabela_unida = tabela_reads.merge(tabela_ocorr, how='outer', on='taxon')
            if 'taxon' in tabela_reads.columns:
                tabela_unida = tabela_reads.merge(tabela_ocorr, how='outer', on='taxon')
            tabelas_finais.setdefault(area, tabela_unida)

        return tabelas_finais


def salva_resultados(tabelas_finais, caminho_salvar, amostrador=False, area=False):
    """Salva tabelas de resultados.

    Parameters:
    tabelas_finais (dict): dicionario com DataFrames que representam as tabelas finais com os resultados apresentados de acordo com as filtragens.
    caminho_salvar (str): caminho no qual será salvo o arquivo.
    amostrador (bool): indica filtragem por amostrador.
    area (bool): indica filtragem por área.
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
                                tabela_final.to_csv(buffer, sep=';', encoding='utf-8')
                    else:
                        with zipfile.ZipFile(caminho_salvar_tratado + f'_{amostrador}.zip', "a") as zf:
                            with zf.open(f"{amostrador}_{area}.csv", "w") as buffer:
                                tabela_final.to_csv(buffer, sep=';', encoding='utf-8')
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
                            tabela_final.to_csv(buffer, sep=';', encoding='utf-8')
                else:
                    with zipfile.ZipFile(caminho_salvar, "a") as zf:
                        with zf.open(f"{amostrador}.csv", "w") as buffer:
                            tabela_final.to_csv(buffer, sep=';', encoding='utf-8')

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
                            tabela_final.to_csv(buffer, sep=';', encoding='utf-8')
                else:
                    with zipfile.ZipFile(caminho_salvar, "a") as zf:
                        with zf.open(f"{area}.csv", "w") as buffer:
                            tabela_final.to_csv(buffer, sep=';', encoding='utf-8')
            i += 1


def main():
    pass


if __name__ == "__main__":
    main()
