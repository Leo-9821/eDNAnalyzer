import pandas as pd


def separa_corridas(df):
    """Separa o dataframe completo nas suas corridas.

    Parameters:
    df (pandas.core.frame.DataFrame): Base de dados com os resultados do metabarcoding após Blast.
    lista_corridas (list, nump.array): Lista com os nomes das corridas.

    Returns:
    areas (dict): Dicionário com os dataframes identificados por chaves com os nomes informados na lista de corridas.
    """

    lista_corridas = list(df['Corrida'].unique())

    corridas = {}
    for corrida in lista_corridas:
        nome_corrida = corrida
        corridas[nome_corrida] = df[df['Corrida'] == corrida]

    return corridas


def aplica_threshold(corridas):
    thresholds = {}
    corrs = {}

    for corrida in corridas:
        df = corridas[corrida]
        reads = df['N_reads']
        total_reads = sum(reads)
        threshold = total_reads * 0.05 / 100

        thresholds[corrida] = threshold

        corr = df.loc[df['N_reads'] > threshold]
        corrs[corrida] = corr

    df_thresholds = pd.DataFrame.from_dict(thresholds, orient='index')
    df_thresholds = df_thresholds.rename(columns={0: 'Threshold'})
    return corrs, df_thresholds


def concatena_dfs(dfs):
    tabelas = dfs.values()
    tabelas_concatenadas = pd.concat(tabelas, ignore_index=True)
    return tabelas_concatenadas


def define_areas(df):
    lista_amostras = df['Amostra'].unique()
    for i in range(len(lista_amostras)):
        lista_amostras[i] = tuple(lista_amostras[i].split('_'))

    lista_areas = []

    for area, parcela in lista_amostras:
        lista_areas.append(area)

    lista_areas = list(set(lista_areas))

    return lista_areas


def separa_amostradores(df, amostradores):
    amst = {}
    for amostrador in amostradores:
        amst[amostrador] = df[df['Amostra'].str.contains(amostrador)]

    return amst


def cria_listas_gerais(dfs):
    listas_gerais = {}

    for df in dfs:
        lista_especies = dfs[df]['OTUFinal'].unique()
        listas_gerais[df] = pd.DataFrame(lista_especies, columns=['Táxon'],).sort_values(by='Táxon').reset_index(drop=True)
    return listas_gerais


def separa_areas(lista_areas, amostradores=None, df=None):
    if amostradores:

        areas_amostradores = {}
        areas = {}
        for amostrador in amostradores:
            tabela_amst = amostradores[amostrador]
            for area in lista_areas:
                areas_amostradores.setdefault(amostrador, []).append({area: tabela_amst[tabela_amst['Amostra'].str.contains(area)]})
        print(areas_amostradores)
        return areas_amostradores
    else:
        areas = {}
        for area in lista_areas:
            areas[area] = df[df['Amostra'].str.contains(area)]

        return areas


def conta_ocorrencias_area(dfs_areas, amostrador=False):
    ocorr_areas = {}
    ocorr = {}

    if amostrador:
        for amostrador in dfs_areas:
            tabelas_areas = dfs_areas[amostrador]
            for area, tabela in tabelas_areas.items():
                df_area = tabela['OTUFinal'].value_counts()
                df_area = pd.DataFrame(df_area)
                df_area = df_area.rename(columns={'OTUFinal': 'Táxon', 'count': f'Detecções em {area}'})
                ocorr[area] = df_area.sort_values(by=f'Detecções em {area}').reset_index()
            ocorr_areas[amostrador] = ocorr

        return ocorr_areas
    else:
        pass


def calcula_reads_especie(dfs_area, amostrador=False):
    reads_especie_amostrador = {}
    reads_especie = {}

    if amostrador:
        for amostrador, area_tabelas in dfs_area.items():
            for area, tabela in area_tabelas.items():
                df_read_sp = tabela[['N_reads', 'OTUFinal']]
                df_read_sp = df_read_sp.groupby(by='OTUFinal').sum()
                df_read_sp = df_read_sp.sort_values(by='N_reads', ascending=False).reset_index()
                df_read_sp = df_read_sp.rename(columns={'OTUFinal': 'Táxon', 'N_reads': 'Reads'})
                reads_especie[area] = df_read_sp
            reads_especie_amostrador[amostrador] = reads_especie
        return reads_especie_amostrador
    else:
        pass


def constroi_tabela_final(df_reads_sp, df_deteccoes):
    tabela_final = df_read_sp.merge(df_deteccoes, how='outer', on='Táxon')
    return tabela_final


########################### def salva_tabela_final(tabela_final):  # Salvando resultado final
#     tabela_final.to_csv(r'C:/Users/Leonardo Willian/Desktop/resultado_agua_cep_metab_0423.csv',
#                         encoding='Latin1', index=False, sep=';')
