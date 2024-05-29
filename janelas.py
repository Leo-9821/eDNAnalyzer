from metabar import *
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pandas as pd
from PIL import Image, ImageTk


class Janelas:
    def __init__(self):
        self.idioma = tk.Tk()
        self.idioma.resizable(0,0)
        self.idioma.title('eDNAnalyzer')
        self.var_caminho_arquivo = tk.StringVar()
        self.idioma.rowconfigure(0, weight=1)
        self.idioma.columnconfigure([0, 1], weight=1)

    def inicia_janela(self):
        label_titulo = tk.Label(self.idioma, text='Choose a language', font=('Arial', 16, 'bold'), borderwidth=2, relief='solid')
        label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky='nswe', columnspan=4)

        bandeira_brasil = ImageTk.PhotoImage(Image.open('./img/bandeira-nacional-brasil.jpg').resize((50, 33)))
        bandeira_uk = ImageTk.PhotoImage(Image.open('img/Flag-United-Kingdom.jpg').resize((50, 33)))

        botao_ptbr = tk.Button(self.idioma, text='Português \nbrasileiro', font=('Arial', 12), image=bandeira_brasil, compound='top', height=85, width=95, command=lambda: self.janela_principal('pt-br'))
        botao_ptbr.image = bandeira_brasil
        botao_ptbr.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        botao_english = tk.Button(self.idioma, text='English', font=('Arial', 12), image=bandeira_uk, compound='top', height=85, width=95, command=lambda: self.janela_principal('eng'))
        botao_english.image = bandeira_uk
        botao_english.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

    def janela_principal(self, idioma):
        principal = tk.Toplevel()
        principal.resizable(0, 0)
        principal.rowconfigure(0, weight=1)
        principal.columnconfigure([0, 1], weight=1)

        if idioma == 'eng':
            principal.title("Primary processing and threshold")

            label_titulo = tk.Label(principal, text='Choose the process to run', font=('Arial', 16, 'bold'), borderwidth=2, relief='solid')
            label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky='nswe', columnspan=3)

            botao_selecionar_funcionalidade = tk.Button(principal, text='Initial processing and threshold application', font=('Arial', 16), command=lambda: self.proc_inicial_threshold('eng'))
            botao_selecionar_funcionalidade.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

            botao_selecionar_funcionalidade2 = tk.Button(principal, text='Build table of consolidated results', font=('Arial', 16), command=lambda: self.proc_tabelas_consolidadas('eng'))
            botao_selecionar_funcionalidade2.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')
        elif idioma == 'pt-br':
            principal.title("Processamento primário e threshold")

            label_titulo = tk.Label(principal, text='Escolha um processo para rodar', font=('Arial', 16, 'bold'),
                                    borderwidth=2, relief='solid')
            label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky='nswe', columnspan=3)

            botao_selecionar_funcionalidade = tk.Button(principal, text='Processamento inicial e aplicação do threshold',
                                                        font=('Arial', 16), command=lambda: self.proc_inicial_threshold('pt-br'))
            botao_selecionar_funcionalidade.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

            botao_selecionar_funcionalidade2 = tk.Button(principal, text='Construção das tabelas de resultado final',
                                                         font=('Arial', 16), command=lambda: self.proc_tabelas_consolidadas('pt-br'))
            botao_selecionar_funcionalidade2.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')

    def proc_inicial_threshold(self, idioma):
        global label_arquivo_selecionado
        nova_janela = tk.Toplevel()
        nova_janela.resizable(0, 0)
        nova_janela.rowconfigure(0, weight=1)
        nova_janela.columnconfigure([0, 1], weight=1)

        if idioma == 'eng':
            nova_janela.title("Primary processing and threshold")

            label_novo_titulo = tk.Label(nova_janela, text='Initial processing and threshold application', font=('Arial', 16, 'bold'), borderwidth=2, relief='solid')
            label_novo_titulo.grid(row=0, column=0, padx=10, pady=5, sticky='nswe', columnspan=3)

            label_selecionar_arquivo = tk.Label(nova_janela, text='Choose a file', font=('Arial', 14))
            label_selecionar_arquivo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)

            botao_selecionar_arquivo = tk.Button(nova_janela, text='Click to choose', font=('Arial', 14), command=lambda: self.seleciona_arquivo('eng'))
            botao_selecionar_arquivo.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

            label_arquivo_selecionado = tk.Label(nova_janela, text='No file chosen', font=('Arial', 14))
            label_arquivo_selecionado.grid(row=2, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

            nova_janela.focus_set()
            nova_janela.grab_set()

            label_threshold = tk.Label(nova_janela, text='Indicate the threshold in percentage: \n(default value 0.05)', font=('Arial', 14))
            label_threshold.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

            caixa_threshold = tk.Entry(nova_janela, font=('Arial', 14))
            caixa_threshold.grid(row=3, column=2, padx=10, pady=10, sticky='nsew')

            botao_run = tk.Button(nova_janela, text='Run', font=('Arial', 14), command=lambda: self.roda_analise_primaria(caixa_threshold, 'eng'))
            botao_run.grid(row=4, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)
        elif idioma == 'pt-br':
            nova_janela.title("Processamento primário e threshold")

            label_novo_titulo = tk.Label(nova_janela, text='Processamento inicial e aplicação de threshold',
                                         font=('Arial', 16, 'bold'), borderwidth=2, relief='solid')
            label_novo_titulo.grid(row=0, column=0, padx=10, pady=5, sticky='nswe', columnspan=3)

            label_selecionar_arquivo = tk.Label(nova_janela, text='Selecione um arquivo:', font=('Arial', 14))
            label_selecionar_arquivo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)

            botao_selecionar_arquivo = tk.Button(nova_janela, text='Clique para selecionar', font=('Arial', 14),
                                                 command=lambda: self.seleciona_arquivo('pt-br'))
            botao_selecionar_arquivo.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

            label_arquivo_selecionado = tk.Label(nova_janela, text='Nenhum arquivo selecionado', font=('Arial', 14))
            label_arquivo_selecionado.grid(row=2, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

            nova_janela.focus_set()
            nova_janela.grab_set()

            label_threshold = tk.Label(nova_janela, text='Indique o threshold em porcentagem: \n(use ponto como separador decimal, valor padrão 0.05)',
                                       font=('Arial', 14))
            label_threshold.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

            caixa_threshold = tk.Entry(nova_janela, font=('Arial', 14))
            caixa_threshold.grid(row=3, column=2, padx=10, pady=10, sticky='nsew')

            botao_run = tk.Button(nova_janela, text='Rodar', font=('Arial', 14),
                                  command=lambda: self.roda_analise_primaria(caixa_threshold, 'pt-br'))
            botao_run.grid(row=4, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

    def roda_analise_primaria(self,  caixa_threshold, idioma):

        df = pd.read_excel(self.var_caminho_arquivo.get())

        string_threshold = caixa_threshold.get()

        if string_threshold == '':
            threshold = 0.05
        else:
            threshold = float(string_threshold)

        dfs_corridas = separa_corridas(df)

        selecionados, nao_selecionados, thresholds = aplica_threshold(dfs_corridas, threshold)

        resultado_tratado_geral = concatena_dfs(selecionados)
        nao_selecionados_geral = concatena_dfs(nao_selecionados)

        if idioma == 'eng':
            caminho_salvar_resultado = asksaveasfilename(title='Save the results table', initialfile='processed_results', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            resultado_tratado_geral.to_excel(caminho_salvar_resultado + ".xlsx", index=False)

            caminho_salvar_resultado = asksaveasfilename(title='Save the table with deleted OTUs', initialfile='deleted_otus', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            nao_selecionados_geral.to_excel(caminho_salvar_resultado + ".xlsx", index=False)

            caminho_salvar_thresholds = asksaveasfilename(title='Save the thresholds table', initialfile='thresholds', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            thresholds.to_excel(caminho_salvar_thresholds + ".xlsx")
        elif idioma == 'pt-br':
            caminho_salvar_resultado = asksaveasfilename(title='Salve as tabelas dos resultados',
                                                         initialfile='resultados_processados',
                                                         filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            resultado_tratado_geral.to_excel(caminho_salvar_resultado + ".xlsx", index=False)

            caminho_salvar_resultado = asksaveasfilename(title='Salve tabelas com as OTUs excluídas',
                                                         initialfile='otus_excluídas',
                                                         filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            nao_selecionados_geral.to_excel(caminho_salvar_resultado + ".xlsx", index=False)

            caminho_salvar_thresholds = asksaveasfilename(title='Salve a tabela de thresholds', initialfile='thresholds',
                                                          filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            thresholds.to_excel(caminho_salvar_thresholds + ".xlsx")

    def proc_tabelas_consolidadas(self, idioma):
        global label_arquivo_selecionado
        nova_janela = tk.Toplevel()
        nova_janela.resizable(0,0)
        nova_janela.rowconfigure(0, weight=1)
        nova_janela.columnconfigure(0, weight=1)

        if idioma == 'eng':
            nova_janela.title("Build table of consolidated results")

            label_novo_titulo = tk.Label(nova_janela, text='Build table of consolidated results', font=('Arial', 16, 'bold'), borderwidth=2,  relief='solid')
            label_novo_titulo.grid(row=0, column=0, padx=10, pady=5, ipadx=3, columnspan=3)

            frame = tk.Frame(nova_janela)
            frame.grid(row=1, column=0)

            frame_selecao_arquivo = tk.LabelFrame(frame, text='File choice', font=('Arial', 15))
            frame_selecao_arquivo.grid(row=1, column=0)

            label_selecionar_arquivo = tk.Label(frame_selecao_arquivo, text='Choose a file:', font=('Arial', 14))
            label_selecionar_arquivo.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

            botao_selecionar_arquivo = tk.Button(frame_selecao_arquivo, text='Click to choose', font=('Arial', 14), command=lambda: self.seleciona_arquivo('eng'))
            botao_selecionar_arquivo.grid(row=1, column=2, padx=10, pady=10)

            label_arquivo_selecionado = tk.Label(frame_selecao_arquivo, text='No file chosen', font=('Arial', 14))
            label_arquivo_selecionado.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

            nova_janela.focus_set()
            nova_janela.grab_set()

            frame_separacao = tk.LabelFrame(frame, text='Data filtering', font=('Arial', 15))
            frame_separacao.grid(row=2, column=0)

            label_separacoes = tk.Label(frame_separacao, text='Filter table by:', justify="left", font=('Arial', 14))
            label_separacoes.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

            var_amostrador = tk.BooleanVar(frame_separacao)
            botao_amostrador = tk.Checkbutton(frame_separacao, text='Sampler', variable=var_amostrador, font=('Arial', 14))
            botao_amostrador.grid(row=1, column=2, sticky='w')

            var_area = tk.BooleanVar(frame_separacao)
            botao_area = tk.Checkbutton(frame_separacao, text='Area', variable=var_area, font=('Arial', 14))
            botao_area.grid(row=2, column=2, sticky='w')

            frame_aliquotas = tk.LabelFrame(frame, text='Aliquots', font=('Arial', 15))
            frame_aliquotas.grid(row=3, column=0)

            var_aliquota = tk.BooleanVar(frame_aliquotas)
            botao_area = tk.Checkbutton(frame_aliquotas, text='If you have separated your sample \npoints into aliquots, select this option', variable=var_aliquota, font=('Arial', 14))
            botao_area.grid(row=0, column=0, columnspan=3, sticky='w')

            frame_amostradores = tk.LabelFrame(frame, text='Samplers definition', font=('Arial', 15))
            frame_amostradores.grid(row=4, column=0)

            label_amostradores = tk.Label(frame_amostradores, text='Insert your samplers as you identified \nthem in your table (one per row):', justify="left", font=('Arial', 14))
            label_amostradores.grid(row=1, column=0, padx=10, pady=10)

            caixa_amostradores = tk.Text(frame_amostradores, font=('Arial', 14), width=10, height=5)
            caixa_amostradores.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

            botao_run = tk.Button(nova_janela, text='Run',  font=('Arial', 14), width=44, command=lambda: self.roda_analise_secundaria(caixa_amostradores, var_amostrador, var_area, var_aliquota, 'eng'))
            botao_run.grid(row=2, column=0, padx=10, pady=10, columnspan=3)
        elif idioma == 'pt-br':
            nova_janela.title("Construção das tabelas de resultado final")

            label_novo_titulo = tk.Label(nova_janela, text='Construção das tabelas de resultado final',
                                         font=('Arial', 16, 'bold'), borderwidth=2, relief='solid')
            label_novo_titulo.grid(row=0, column=0, padx=10, pady=5, ipadx=3, columnspan=3)

            frame = tk.Frame(nova_janela)
            frame.grid(row=1, column=0)

            frame_selecao_arquivo = tk.LabelFrame(frame, text='Seleção de arquivo', font=('Arial', 15))
            frame_selecao_arquivo.grid(row=1, column=0)

            label_selecionar_arquivo = tk.Label(frame_selecao_arquivo, text='Selecione um artigo:', font=('Arial', 14))
            label_selecionar_arquivo.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

            botao_selecionar_arquivo = tk.Button(frame_selecao_arquivo, text='Clique para selecionar', font=('Arial', 14),
                                                 command=lambda: self.seleciona_arquivo('pt-br'))
            botao_selecionar_arquivo.grid(row=1, column=2, padx=10, pady=10)

            label_arquivo_selecionado = tk.Label(frame_selecao_arquivo, text='Nenhum arquivo selecionado', font=('Arial', 14))
            label_arquivo_selecionado.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

            nova_janela.focus_set()
            nova_janela.grab_set()

            frame_separacao = tk.LabelFrame(frame, text='Filtragem de dados', font=('Arial', 15))
            frame_separacao.grid(row=2, column=0)

            label_separacoes = tk.Label(frame_separacao, text='Filrar tabela por:', justify="left", font=('Arial', 14))
            label_separacoes.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

            var_amostrador = tk.BooleanVar(frame_separacao)
            botao_amostrador = tk.Checkbutton(frame_separacao, text='Amostrador', variable=var_amostrador,
                                              font=('Arial', 14))
            botao_amostrador.grid(row=1, column=2, sticky='w')

            var_area = tk.BooleanVar(frame_separacao)
            botao_area = tk.Checkbutton(frame_separacao, text='Área', variable=var_area, font=('Arial', 14))
            botao_area.grid(row=2, column=2, sticky='w')

            frame_aliquotas = tk.LabelFrame(frame, text='Alíquotas', font=('Arial', 15))
            frame_aliquotas.grid(row=3, column=0)

            var_aliquota = tk.BooleanVar(frame_aliquotas)
            botao_area = tk.Checkbutton(frame_aliquotas,
                                        text='Se você separou suas pontos \namostrais em alíquotas, selecione essa opção',
                                        variable=var_aliquota, font=('Arial', 14))
            botao_area.grid(row=0, column=0, columnspan=3, sticky='w')

            frame_amostradores = tk.LabelFrame(frame, text='Definição dos amostradores', font=('Arial', 15))
            frame_amostradores.grid(row=4, column=0)

            label_amostradores = tk.Label(frame_amostradores,
                                          text='Insira seus amostradores como \nidentificou na tabela (um por linha):',
                                          justify="left", font=('Arial', 14))
            label_amostradores.grid(row=1, column=0, padx=10, pady=10)

            caixa_amostradores = tk.Text(frame_amostradores, font=('Arial', 14), width=10, height=5)
            caixa_amostradores.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

            botao_run = tk.Button(nova_janela, text='Rodar', font=('Arial', 14), width=44,
                                  command=lambda: self.roda_analise_secundaria(caixa_amostradores, var_amostrador,
                                                                               var_area, var_aliquota, 'pt-br'))
            botao_run.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

    def seleciona_arquivo(self, idioma):
        if idioma == 'eng':
            tipos_de_arquivo = [('Excel file', '*.xlsx')]
            caminho_arquivo = askopenfilename(title='Choose an Excel file', filetypes=tipos_de_arquivo)
            self.var_caminho_arquivo.set(caminho_arquivo)
            if caminho_arquivo:
                label_arquivo_selecionado['text'] = f'Chosen file {caminho_arquivo}'
        elif idioma == 'pt-br':
            tipos_de_arquivo = [('Arquivo de Excel', '*.xlsx')]
            caminho_arquivo = askopenfilename(title='Escolha um arquivo Excel', filetypes=tipos_de_arquivo)
            self.var_caminho_arquivo.set(caminho_arquivo)
            if caminho_arquivo:
                label_arquivo_selecionado['text'] = f'Arquivo selecionado {caminho_arquivo}'

    def roda_analise_secundaria(self, caixa_amostradores, var_amostrador, var_area, var_aliquotas, idioma):
        texto_amostradores = caixa_amostradores.get('1.0', tk.END)
        lista_amostradores = texto_amostradores.split('\n')
        lista_amostradores.pop(-1)

        df = pd.read_excel(self.var_caminho_arquivo.get())

        var_amostrador = var_amostrador.get()
        var_area = var_area.get()
        var_aliquotas = var_aliquotas.get()

        if var_amostrador and not var_area:
            amostradores = separa_amostradores(df, lista_amostradores)

            if not var_aliquotas:
                ocorrencias = conta_ocorrencias(amostradores, amostrador=True)
            else:
                ocorrencias = conta_ocorrencia_aliquotas(amostradores, amostradores=True)

            reads_especie = calcula_reads_especie(amostradores, amostrador=True)

            tabelas_finais = constroi_tabela_final(reads_especie, ocorrencias, amostradores=True)

            if idioma == 'eng':
                caminho_resultado = asksaveasfilename(title='Save results', initialfile='results', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            elif idioma == 'pt-br':
                caminho_resultado = asksaveasfilename(title='Salve os resultados', initialfile='resultados', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))


            salva_resultados(tabelas_finais, caminho_resultado, amostrador=True)

        elif var_area and not var_amostrador:
            lista_areas = define_areas(df)

            areas = separa_areas(lista_areas, df=df)

            if not var_aliquotas:
                ocorrencias = conta_ocorrencias(areas, area=True)
            else:
                ocorrencias = conta_ocorrencia_aliquotas(areas, areas=True)

            reads_especie = calcula_reads_especie(areas, area=True)

            tabelas_finais = constroi_tabela_final(reads_especie, ocorrencias, areas=True)

            if idioma == 'eng':
                caminho_resultado = asksaveasfilename(title='Save results', initialfile='results', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            elif idioma == 'pt-br':
                caminho_resultado = asksaveasfilename(title='Salve os resultados', initialfile='resultados', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))

            salva_resultados(tabelas_finais, caminho_resultado, area=True)

        elif var_amostrador and var_area:
            amostradores = separa_amostradores(df, lista_amostradores)

            listas_gerais = cria_listas_gerais(amostradores)

            lista_areas = define_areas(df)

            areas = separa_areas(lista_areas, amostradores=amostradores)

            if not var_aliquotas:
                ocorrencias_area = conta_ocorrencias(areas, amostrador=True, area=True)
            else:
                ocorrencias_area = conta_ocorrencia_aliquotas(areas, amostradores=True, areas=True)

            reads_especie = calcula_reads_especie(areas, amostrador=True, area=True)

            tabelas_finais = constroi_tabela_final(reads_especie, ocorrencias_area, amostradores=True, areas=True)

            if idioma == 'eng':
                caminho_lista_geral = asksaveasfilename(title='Save general lists', initialfile='general_list', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            elif idioma == 'pt-br':
                caminho_lista_geral = asksaveasfilename(title='Salves as listas gerais', initialfile='listas_gerais', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))

            salva_listas_gerais(listas_gerais, caminho_lista_geral, amostrador=True, area=True)

            if idioma == 'eng':
                caminho_resultado = asksaveasfilename(title='Save results', initialfile='results', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            elif idioma == 'pt-br':
                caminho_resultado = asksaveasfilename(title='Salve os resultados', initialfile='resultados', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))

            salva_resultados(tabelas_finais, caminho_resultado, amostrador=True, area=True)


def main():
    janela = Janelas()
    janela.inicia_janela()
    janela.idioma.mainloop()


if __name__ == "__main__":
    main()
