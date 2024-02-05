from metabar import *
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pandas as pd


class Janelas:
    def __init__(self):
        self.principal = tk.Tk()
        self.principal.resizable(0,0)
        self.principal.title('Processamento de Metabarcoding')
        self.var_caminho_arquivo = tk.StringVar()
        self.principal.rowconfigure(0, weight=1)
        self.principal.columnconfigure([0, 1], weight=1)

    def inicia_janela(self):
        label_titulo = tk.Label(self.principal, text='Escolha o processo que deseja rodar', font=('Arial', 16, 'bold'), borderwidth=2, relief='solid')
        label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky='nswe', columnspan=3)

        botao_selecionar_funcionalidade = tk.Button(self.principal, text='Processamento da tabela inicial e aplicação do threshold', font=('Arial', 16), command=self.proc_inicial_threshold)
        botao_selecionar_funcionalidade.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        botao_selecionar_funcionalidade2 = tk.Button(self.principal, text='Criação de tabelas com resultados consolidados', font=('Arial', 16), command=self.proc_tabelas_consolidadas)
        botao_selecionar_funcionalidade2.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')

    def proc_inicial_threshold(self):
        global label_arquivo_selecionado
        nova_janela = tk.Toplevel()
        nova_janela.resizable(0, 0)
        nova_janela.rowconfigure(0, weight=1)
        nova_janela.columnconfigure([0, 1], weight=1)
        nova_janela.title("Processamento primário e threshold")

        label_novo_titulo = tk.Label(nova_janela, text='Processamento da tabela inicial e aplicação do threshold', font=('Arial', 16, 'bold'), borderwidth=2, relief='solid')
        label_novo_titulo.grid(row=0, column=0, padx=10, pady=5, sticky='nswe', columnspan=3)

        label_selecionar_arquivo = tk.Label(nova_janela, text='Selecione um arquivo:', font=('Arial', 14))
        label_selecionar_arquivo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)

        botao_selecionar_arquivo = tk.Button(nova_janela, text='Clique para selecionar', font=('Arial', 14), command=self.seleciona_arquivo)
        botao_selecionar_arquivo.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        label_arquivo_selecionado = tk.Label(nova_janela, text='Nenhum arquivo selecionado', font=('Arial', 14))
        label_arquivo_selecionado.grid(row=2, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

        nova_janela.focus_set()
        nova_janela.grab_set()

        botao_run = tk.Button(nova_janela, text='Rodar', font=('Arial', 14), command=self.roda_analise_primaria)
        botao_run.grid(row=3, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

    def roda_analise_primaria(self):
        df = pd.read_excel(self.var_caminho_arquivo.get())
        self.principal.destroy()

        dfs_corridas = separa_corridas(df)

        corridas_tratadas, thresholds = aplica_threshold(dfs_corridas)

        resultado_tratado_geral = concatena_dfs(corridas_tratadas)

        caminho_salvar_resultado = asksaveasfilename(title='Salve a tabela de resultados', initialfile='resultados_tratados', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        resultado_tratado_geral.to_excel(caminho_salvar_resultado + ".xlsx", index=False)

        caminho_salvar_thresholds = asksaveasfilename(title='Salve a tabela dos thresholds', initialfile='thresholds', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        thresholds.to_excel(caminho_salvar_thresholds + ".xlsx")

    def proc_tabelas_consolidadas(self):
        global label_arquivo_selecionado
        nova_janela = tk.Toplevel()
        nova_janela.resizable(0,0)
        nova_janela.rowconfigure(0, weight=1)
        nova_janela.columnconfigure(0, weight=1)
        nova_janela.title("Criação de tabelas com resultados consolidados")

        label_novo_titulo = tk.Label(nova_janela, text='Criação de tabelas com resultados consolidados', font=('Arial', 16, 'bold'), borderwidth=2,  relief='solid')
        label_novo_titulo.grid(row=0, column=0, padx=10, pady=5, ipadx=3, columnspan=3)

        frame = tk.Frame(nova_janela)
        frame.grid(row=1, column=0)

        frame_selecao_arquivo = tk.LabelFrame(frame, text='Seleção de Arquivo', font=('Arial', 15))
        frame_selecao_arquivo.grid(row=1, column=0)

        label_selecionar_arquivo = tk.Label(frame_selecao_arquivo, text='Selecione um arquivo:', font=('Arial', 14))
        label_selecionar_arquivo.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        botao_selecionar_arquivo = tk.Button(frame_selecao_arquivo, text='Clique para selecionar', font=('Arial', 14), command=self.seleciona_arquivo)
        botao_selecionar_arquivo.grid(row=1, column=2, padx=10, pady=10)

        label_arquivo_selecionado = tk.Label(frame_selecao_arquivo, text='Nenhum arquivo selecionado', font=('Arial', 14))
        label_arquivo_selecionado.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

        nova_janela.focus_set()
        nova_janela.grab_set()

        frame_separacao = tk.LabelFrame(frame, text='Separação dos dados', font=('Arial', 15))
        frame_separacao.grid(row=2, column=0)

        label_separacoes = tk.Label(frame_separacao, text='Você deseja separar sua tabela em:', justify="left", font=('Arial', 14))
        label_separacoes.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        var_amostrador = tk.BooleanVar(frame_separacao)
        botao_amostrador = tk.Checkbutton(frame_separacao, text='Amostrador', variable=var_amostrador, font=('Arial', 14))
        botao_amostrador.grid(row=1, column=2, sticky='w')

        var_area = tk.BooleanVar(frame_separacao)
        botao_area = tk.Checkbutton(frame_separacao, text='Área', variable=var_area, font=('Arial', 14))
        botao_area.grid(row=2, column=2, sticky='w')

        frame_aliquotas = tk.LabelFrame(frame, text='Alíquotas', font=('Arial', 15))
        frame_aliquotas.grid(row=3, column=0)

        var_aliquota = tk.BooleanVar(frame_aliquotas)
        botao_area = tk.Checkbutton(frame_aliquotas, text='Caso tenha separado seus pontos amostrais em \nalíquotas selecione essa opção', variable=var_aliquota, font=('Arial', 14))
        botao_area.grid(row=0, column=0, columnspan=3, sticky='w')

        frame_amostradores = tk.LabelFrame(frame, text='Definição dos amostradores', font=('Arial', 15))
        frame_amostradores.grid(row=4, column=0)

        label_amostradores = tk.Label(frame_amostradores, text='Insira ao lado seus amostradores\ncomo você identificou em sua tabela\n(um por linha):', justify="left", font=('Arial', 14))
        label_amostradores.grid(row=1, column=0, padx=10, pady=10)

        caixa_amostradores = tk.Text(frame_amostradores, font=('Arial', 14), width=10, height=5)
        caixa_amostradores.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

        botao_run = tk.Button(nova_janela, text='Rodar',  font=('Arial', 14), width=44, command=lambda: self.roda_analise_secundaria(caixa_amostradores, var_amostrador, var_area, var_aliquota))
        botao_run.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

    def seleciona_arquivo(self):
        tipos_de_arquivo = [('Arquivo de Excel', '*.xlsx')]
        caminho_arquivo = askopenfilename(title='Selecione um arquivo em Excel para abrir', filetypes=tipos_de_arquivo)
        self.var_caminho_arquivo.set(caminho_arquivo)
        if caminho_arquivo:
            label_arquivo_selecionado['text'] = f'Arquivo Selecionado {caminho_arquivo}'

    def roda_analise_secundaria(self, caixa_amostradores, var_amostrador, var_area, var_aliquotas):
        texto_amostradores = caixa_amostradores.get('1.0', tk.END)
        lista_amostradores = texto_amostradores.split('\n')
        lista_amostradores.pop(-1)

        df = pd.read_excel(self.var_caminho_arquivo.get())
        self.principal.destroy()

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

            caminho_lista_geral = asksaveasfilename(title='Salve as listas gerais', initialfile='listas_gerais', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))

            salva_listas_gerais(listas_gerais, caminho_lista_geral, amostrador=True, area=True)

            caminho_resultado = asksaveasfilename(title='Salve os resultados', initialfile='resultados', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))

            salva_resultados(tabelas_finais, caminho_resultado, amostrador=True, area=True)


