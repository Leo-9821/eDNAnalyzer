import pandas as pd
from openpyxl import Workbook


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
        for amostrador in amostradores:
            tabela_amst = amostradores[amostrador]
            for area in lista_areas:
                areas_amostradores.setdefault(amostrador, []).append({area: tabela_amst[tabela_amst['Amostra'].str.contains(area)]})

        return areas_amostradores
    else:
        areas = {}
        for area in lista_areas:
            areas[area] = df[df['Amostra'].str.contains(area)]

        return areas


def conta_ocorrencias_area(dfs_areas, amostrador=False):
    ocorr_areas = {}

    if amostrador:
        for amostrador in dfs_areas:
            tabelas_areas = dfs_areas[amostrador]
            for tabela_area in tabelas_areas:
                for area, tabela in tabela_area.items():
                    df_area = tabela['OTUFinal'].value_counts()
                    df_area = pd.DataFrame(df_area)
                    df_area = df_area.sort_values(by='count').reset_index()
                    df_area = df_area.rename(columns={'OTUFinal': 'Táxon', 'count': f'Detecções em {area}'})
                    ocorr_areas.setdefault(amostrador, []).append({area: df_area})

        return ocorr_areas
    else:
        pass


def calcula_reads_especie(dfs_areas, amostrador=False):
    reads_especie_amostrador = {}

    if amostrador:
        for amostrador in dfs_areas:
            tabelas_areas = dfs_areas[amostrador]
            for tabela_area in tabelas_areas:
                for area, tabela in tabela_area.items():
                    df_read_sp = tabela[['N_reads', 'OTUFinal']]
                    df_read_sp = df_read_sp.groupby(by='OTUFinal').sum()
                    df_read_sp = df_read_sp.sort_values(by='N_reads', ascending=False).reset_index()
                    df_read_sp = df_read_sp.rename(columns={'OTUFinal': 'Táxon', 'N_reads': 'Reads'})
                    reads_especie_amostrador.setdefault(amostrador, []).append({area: df_read_sp})

        return reads_especie_amostrador
    else:
        pass


def constroi_tabela_final(df_reads_sp, df_deteccoes, amostrador=False):
    tabelas_finais = {}

    if amostrador:
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
                        tabela_unida = tbl_rds.merge(tbl_ocr, how='outer', on='Táxon')
                        tabelas_finais.setdefault(amostrador, []).append({reads_key: tabela_unida})
                    else:
                        continue
        return tabelas_finais
    else:
        pass


def salva_listas_gerais(listas_gerais, caminho_salvar, amostrador=False):
    i = 0

    if amostrador:
        for amostrador in listas_gerais:
            lista_geral = listas_gerais[amostrador]

            if i == 0:
                with pd.ExcelWriter(caminho_salvar + f'.xlsx', engine='openpyxl') as arquivo:
                    lista_geral.to_excel(arquivo, sheet_name=amostrador)
            else:
                with pd.ExcelWriter(caminho_salvar + f'.xlsx', engine='openpyxl', mode='a') as arquivo:
                    lista_geral.to_excel(arquivo, sheet_name=amostrador)

            i += 1
    else:
        pass


def salva_resultados(tabelas_finais, caminho_salvar, amostrador=False):


    if amostrador:
        for amostrador in tabelas_finais:
            i = 0
            tbls_fns = tabelas_finais[amostrador]
            for tabela in tbls_fns:
                area = list(tabela.keys())[0]
                tabela_final = tabela[area]

                if i == 0:
                    with pd.ExcelWriter(caminho_salvar + f'_{amostrador}.xlsx', engine='openpyxl') as arquivo:
                        tabela_final.to_excel(arquivo, sheet_name=area)
                else:
                    with pd.ExcelWriter(caminho_salvar + f'_{amostrador}.xlsx', engine='openpyxl', mode='a') as arquivo:
                        tabela_final.to_excel(arquivo, sheet_name=area)

                i += 1
    else:
        pass


