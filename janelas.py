from metabar import separa_corridas, aplica_threshold, concatena_dfs, separa_areas
import tkinter as tk
from tkinter.filedialog import askopenfilename
import pandas as pd


class Janelas:
    def __init__(self):
        self.principal = tk.Tk()
        self.principal.title('Processamento de Metabarcoding')
        self.var_caminho_arquivo = tk.StringVar()

    def inicia_janela(self):
        label_titulo = tk.Label(self.principal, text='Escolha o processo que deseja rodar', borderwidth=2, relief='solid')
        label_titulo.grid(row=0, column=0, padx=10, sticky='nswe', columnspan=3)

        botao_selecionar_funcionalidade = tk.Button(self.principal, text='Processamento da tabela inicial e aplicação do threshold', command=self.proc_inicial_threshold)
        botao_selecionar_funcionalidade.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        botao_selecionar_funcionalidade2 = tk.Button(self.principal, text='Funcionalidade 2', command=self.funcionalidade2)
        botao_selecionar_funcionalidade2.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')

    def proc_inicial_threshold(self):
        global label_arquivo_selecionado
        nova_janela = tk.Toplevel()
        nova_janela.title("Processamento primário e threshold")

        label_novo_titulo = tk.Label(nova_janela, text='Processamento da tabela inicial e aplicação do threshold', borderwidth=2, relief='solid')
        label_novo_titulo.grid(row=0, column=0, padx=10, sticky='nswe', columnspan=3)

        label_selecionar_arquivo = tk.Label(nova_janela, text='Selecione um arquivo:')
        label_selecionar_arquivo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)

        botao_selecionar_arquivo = tk.Button(nova_janela, text='Clique para selecionar', command=self.seleciona_arquivo)
        botao_selecionar_arquivo.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        label_arquivo_selecionado = tk.Label(nova_janela, text='Nenhum arquivo selecionado')
        label_arquivo_selecionado.grid(row=2, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

        nova_janela.focus_set()
        nova_janela.grab_set()

        botao_run = tk.Button(nova_janela, text='Rodar', command=self.roda_analise_primaria)
        botao_run.grid(row=3, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

    def roda_analise_primaria(self):
        df = pd.read_excel(self.var_caminho_arquivo.get())
        self.principal.destroy()

        corridas = list(df['Corrida'].unique())

        dfs_corridas = separa_corridas(df, corridas)

        corridas_tratadas = aplica_threshold(dfs_corridas)

        resultado_tratado_geral = concatena_dfs(corridas_tratadas)
        print(resultado_tratado_geral)
        #resultado_tratado_geral.to_excel(r'resultados_tratados.xlsx', index=False)

    def funcionalidade2(self):
        global label_arquivo_selecionado
        nova_janela = tk.Toplevel()
        nova_janela.title("Funcionalidade 2")

        label_novo_titulo = tk.Label(nova_janela, text='Funcionalidade 2',
                                     borderwidth=2, relief='solid')
        label_novo_titulo.grid(row=0, column=0, padx=10, sticky='nswe', columnspan=3)

        label_selecionar_arquivo = tk.Label(nova_janela, text='Selecione um arquivo:')
        label_selecionar_arquivo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)

        botao_selecionar_arquivo = tk.Button(nova_janela, text='Clique para selecionar', command=self.seleciona_arquivo)
        botao_selecionar_arquivo.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        label_arquivo_selecionado = tk.Label(nova_janela, text='Nenhum arquivo selecionado')
        label_arquivo_selecionado.grid(row=2, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

        nova_janela.focus_set()
        nova_janela.grab_set()

        botao_run = tk.Button(nova_janela, text='Rodar', command=self.roda_analise_secundaria)
        botao_run.grid(row=3, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

    def seleciona_arquivo(self):
        tipos_de_arquivo = [('Arquivo de Excel', '*.xlsx')]
        caminho_arquivo = askopenfilename(title='Selecione um arquivo em Excel para abrir', filetypes=tipos_de_arquivo)
        self.var_caminho_arquivo.set(caminho_arquivo)
        if caminho_arquivo:
            label_arquivo_selecionado['text'] = f'Arquivo Selecionado {caminho_arquivo}'

    def roda_analise_secundaria(self):
        print('Funcionou!!!')
