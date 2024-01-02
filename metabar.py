import pandas as pd


def separa_corridas(df, lista_corridas):
    """Separa o dataframe completo nas suas corridas.

    Parameters:
    df (pandas.core.frame.DataFrame): Base de dados com os resultados do metabarcoding após Blast.
    lista_corridas (list, nump.array): Lista com os nomes das corridas.

    Returns:
    areas (dict): Dicionário com os dataframes identificados por chaves com os nomes informados na lista de corridas.
    """

    corridas = {}
    for corrida in lista_corridas:
        nome_corrida = corrida
        corridas[nome_corrida] = df[df['Corrida'] == corrida]

    return corridas


def aplica_threshold(corridas):
    corrs = {}

    for corrida in corridas:
        df = corridas[corrida]
        reads = df['N_reads']
        total_reads = sum(reads)
        threshold = total_reads * 0.05 / 100

        corr = df.loc[df['N_reads'] > threshold]
        corrs[corrida] = corr

    return corrs


def concatena_dfs(dfs):
    tabelas = dfs.values()
    tabelas_concatenadas = pd.concat(tabelas, ignore_index=True)
    return tabelas_concatenadas


def separa_areas(df, lista_areas):
    """Separa o dataframe completo nas 13 áreas.

    Parameters:
    df (pandas.core.frame.DataFrame): Base de dados com os resultados do metabarcoding após Blast.
    lista_areas (list, nump.array): Lista com os nomes/siglas das áreas estudadas.

    Returns:
    areas (dict): Dicionário com os dataframes identificados por chaves com os nomes/siglas informados na lista de areas.
    """

    areas = {}
    for area in lista_areas:
        nome_area = area
        areas[nome_area] = df[df['Amostra'].str.contains(area)]

    return areas


def roda_analise():
    print(df)