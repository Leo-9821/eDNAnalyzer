from janelas import Janelas

janela = Janelas()
janela.inicia_janela()
janela.principal.mainloop()




#
#
# # Separando mosquitos de moscas
#     df_mosquitos = resultado_tratado_geral[resultado_tratado_geral['Amostra'].str.contains('MQ')]
#     df_moscas = resultado_tratado_geral[resultado_tratado_geral['Amostra'].str.contains('M ')]
#     print(df_mosquitos)
#     print(df_moscas)
#
#     # Criando lista de espécies únicas geral
#     lista_especies = resultado_tratado_geral['Espécie'].unique()
#     df_especies = pd.DataFrame(lista_especies, columns=['Táxon']).sort_values(by='Táxon')
#     print(df_especies)
#     # df_especies.to_excel(r'C:/Users/Leonardo Willian/Desktop/spp.xlsx', index = False)
#
#     # Criando lista de áreas
#     lista_amostras = resultado_tratado_geral['Amostra'].unique()
#
#     for i in range(len(lista_amostras)):
#         lista_amostras[i] = tuple(lista_amostras[i].split('_'))
#
#     lista_areas = []
#
#     for area, parcela in lista_amostras:
#         lista_areas.append(area)
#     lista_areas = list(set(lista_areas))
#     print(lista_areas)
#
#     areas_mq = separa_areas(df_mosquitos, lista_areas)
#     areas_m = separa_areas(df_moscas, lista_areas)
#
#     for area in areas_mq:
#         print(area)
#         print(areas_mq[area])
#
#     for area in areas_m:
#         print(area)
#         print(areas_m[area])
#
#     print(areas_m)
#
#     # Contagem de ocorrências
#     ocorr = []
#
#     for area in areas_m:
#         df_area = areas_m[area]
#         df_area = df_area['Espécie'].value_counts()
#         df_area = pd.DataFrame(df_area)
#         df_area = df_area.reset_index()
#         df_area = df_area.rename(columns={'Espécie': 'Táxon', 'count': f'Detecções em {area}'})
#         ocorr.append(df_area)
#         print(df_area)
#
#
#
#
#
#

#
# detec_12S = pd.concat(corr_12S)
# detec_12S = detec_12S.value_counts('Táxon')
# detec_12S = pd.DataFrame(detec_12S)
# detec_12S = detec_12S.reset_index()
# detec_12S = detec_12S.rename(columns={0: 'Detecções 12S'})
# print(detec_12S)
#
# detec_16S = pd.concat(corr_16S)
# detec_16S = detec_16S.value_counts('Táxon')
# detec_16S = pd.DataFrame(detec_16S)
# detec_16S = detec_16S.reset_index()
# detec_16S = detec_16S.rename(columns={0: 'Detecções 16S'})
# print(detec_16S)
#
# # Calculando reads por espécie
# df_read_sp_12S = df_12S[['N_reads', 'Espécie']]
# df_read_sp_12S = df_read_sp_12S.groupby(by='Espécie').sum()
# df_read_sp_12S = df_read_sp_12S.reset_index()
# df_read_sp_12S = df_read_sp_12S.rename(columns={'Espécie': 'Táxon', 'N_reads': 'Reads 12S'})
# print(df_read_sp_12S)
#
# df_read_sp_16S = df_16S[['N_reads', 'Espécie']]
# df_read_sp_16S = df_read_sp_16S.groupby(by='Espécie').sum()
# df_read_sp_16S = df_read_sp_16S.reset_index()
# df_read_sp_16S = df_read_sp_16S.rename(columns={'Espécie': 'Táxon', 'N_reads': 'Reads 16S'})
# print(df_read_sp_16S)
#
# # Construindo tabela final
#
# final_12S = df_read_sp_12S.merge(detec_12S, how='outer', on='Táxon')
# final_16S = df_read_sp_16S.merge(detec_16S, how='outer', on='Táxon')
#
# result_final = final_12S.merge(final_16S, how='outer', on='Táxon')
# print(result_final)
#
# # Salvando resultado final
# result_final.to_csv(r'C:/Users/Leonardo Willian/Desktop/resultado_agua_cep_metab_0423.csv',
#                     encoding='Latin1', index=False, sep=';')


