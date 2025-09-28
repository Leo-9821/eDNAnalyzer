from metabar import *
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk
import pandas as pd
from PIL import Image, ImageTk
import os
import psutil
import time
import threading
import queue


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Janelas:
    def __init__(self):
        self.idioma = tk.Tk()
        self.idioma.resizable(False, False)
        self.idioma.title('eDNAnalyzer')
        self.var_caminho_arquivo = tk.StringVar()
        self.idioma.rowconfigure(0, weight=1)
        self.idioma.columnconfigure([0, 1], weight=1)
        self.logo = ImageTk.PhotoImage(Image.open(resource_path('img/logo_ednanalyzer_sem_nome.png')))
        self.idioma.iconphoto(True, self.logo)

    def inicia_janela(self):
        """Initialize the first window for language selection."""

        label_titulo = tk.Label(self.idioma, text='Choose a language', font=('Arial', 16, 'bold'), borderwidth=2, relief='solid')
        label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky='nswe', columnspan=4)

        bandeira_brasil = ImageTk.PhotoImage(Image.open(resource_path('img/bandeira-nacional-brasil.jpg')).resize((50, 33)))
        bandeira_uk = ImageTk.PhotoImage(Image.open(resource_path('img/flag-usa.png')).resize((50, 33)))

        botao_ptbr = tk.Button(self.idioma, text='Portuguese \n(pt-BR)', font=('Arial', 12), image=bandeira_brasil, compound='top', height=85, width=95, command=lambda: self.janela_principal('pt-br'))
        botao_ptbr.image = bandeira_brasil
        botao_ptbr.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        botao_english = tk.Button(self.idioma, text='English \n(en-US)', font=('Arial', 12), image=bandeira_uk, compound='top', height=85, width=95, command=lambda: self.janela_principal('eng'))
        botao_english.image = bandeira_uk
        botao_english.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

    def janela_principal(self, idioma):
        """Initialize the window for process selection and manual access.

        Parameters:
        idioma (str): Indicates the chosen language, Portuguese ("pt-br") or English ("eng-us").
        """
        principal = tk.Toplevel()
        principal.resizable(0, 0)
        principal.rowconfigure(0, weight=1)
        principal.columnconfigure([0, 1], weight=1)

        if idioma == 'eng':
            principal.title("Choosing the process")

            botao_selecionar_funcionalidade3 = tk.Button(principal, text='Open manual', font=('Arial', 16),
                                                         command=lambda: self.abrir_manual('eng'))
            botao_selecionar_funcionalidade3.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

            label_titulo = tk.Label(principal, text='Choose the process to run', font=('Arial', 16, 'bold'), borderwidth=2, relief='solid')
            label_titulo.grid(row=1, column=0, padx=10, pady=5, sticky='nswe', columnspan=3)

            botao_selecionar_funcionalidade = tk.Button(principal, text='Threshold application', font=('Arial', 16), command=lambda: self.proc_inicial_threshold('eng'))
            botao_selecionar_funcionalidade.grid(row=2, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

            botao_selecionar_funcionalidade2 = tk.Button(principal, text='Results consolidation', font=('Arial', 16), command=lambda: self.proc_tabelas_consolidadas('eng'))
            botao_selecionar_funcionalidade2.grid(row=3, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

        elif idioma == 'pt-br':
            principal.title("Escolhendo o processo")

            botao_selecionar_funcionalidade3 = tk.Button(principal, text='Abrir manual',
                                                         font=('Arial', 16),
                                                         command=lambda: self.abrir_manual('pt-br'))
            botao_selecionar_funcionalidade3.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

            label_titulo = tk.Label(principal, text='Escolha um processo para rodar', font=('Arial', 16, 'bold'),
                                    borderwidth=2, relief='solid')
            label_titulo.grid(row=1, column=0, padx=10, pady=5, sticky='nswe', columnspan=3)

            botao_selecionar_funcionalidade = tk.Button(principal, text='Aplicação do threshold',
                                                        font=('Arial', 16), command=lambda: self.proc_inicial_threshold('pt-br'))
            botao_selecionar_funcionalidade.grid(row=2, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

            botao_selecionar_funcionalidade2 = tk.Button(principal, text='Consolidação dos resultados',
                                                         font=('Arial', 16), command=lambda: self.proc_tabelas_consolidadas('pt-br'))
            botao_selecionar_funcionalidade2.grid(row=3, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

    def abrir_manual(self, idioma):
        """Open the program manual file.

        Parameters:
        idioma (str): Indicates the chosen language, Portuguese ("pt-br") or English ("eng-us").
        """
        if idioma == 'pt-br':
            os.startfile(resource_path('manual_eDNAnalyzer_pt_br.pdf'))
        elif idioma == 'eng':
            os.startfile(resource_path('manual_eDNAnalyzer_eng.pdf'))

    def proc_inicial_threshold(self, idioma):
        """Open the threshold application process window.

        Parameters:
        idioma (str): Indicates the chosen language, Portuguese ("pt-br") or English ("eng-us").
        """
        global label_arquivo_selecionado
        nova_janela = tk.Toplevel()
        nova_janela.resizable(0, 0)
        nova_janela.rowconfigure(0, weight=1)
        nova_janela.columnconfigure([0, 1], weight=1)

        if idioma == 'eng':
            nova_janela.title("Threshold application")

            frame = tk.Frame(nova_janela)
            frame.grid(row=0, column=0)

            frame_titulo = tk.LabelFrame(frame, font=('Arial', 15), borderwidth=0, highlightthickness=0)
            frame_titulo.grid(row=0, column=0, sticky='nsew')
            frame_titulo.rowconfigure(0, weight=1)
            frame_titulo.columnconfigure([1, 2], weight=1)

            botao_voltar = tk.Button(frame_titulo, text='\u2b8c', font=('Arial', 14, 'bold'),
                                     command=lambda: nova_janela.destroy())
            botao_voltar.grid(row=0, column=0, sticky='w')

            label_novo_titulo = tk.Label(frame_titulo, text='Threshold application', font=('Arial', 16, 'bold'), borderwidth=2, relief='solid')
            label_novo_titulo.grid(row=0, column=1, padx=10, pady=5, sticky='nswe', columnspan=3)

            frame_selecao_arquivo = tk.LabelFrame(frame, font=('Arial', 15))
            frame_selecao_arquivo.grid(row=1, column=0)

            botao_selecionar_arquivo = tk.Button(frame_selecao_arquivo, text='Load a file', font=('Arial', 14), command=lambda: self.seleciona_arquivo('eng'))
            botao_selecionar_arquivo.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

            label_arquivo_selecionado = tk.Label(frame_selecao_arquivo, text='No file loaded', font=('Arial', 14))
            label_arquivo_selecionado.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

            nova_janela.focus_set()
            nova_janela.grab_set()

            frame_threshold = tk.LabelFrame(frame, text='Threshold selection', font=('Arial', 15))
            frame_threshold.grid(row=2, column=0, padx=10)

            label_threshold = tk.Label(frame_threshold, text='Indicate the threshold in percentage: \n(default value 0.05)', font=('Arial', 14))
            label_threshold.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

            caixa_threshold = tk.Entry(frame_threshold, width=10, font=('Arial', 14))
            caixa_threshold.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

            label_threshold = tk.Label(frame_threshold,
                                       text='%',
                                       font=('Arial', 14))
            label_threshold.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

            botao_run = tk.Button(nova_janela, text='RUN', font=('Arial', 14, 'bold'), command=lambda: self.roda_analise_primaria(caixa_threshold, 'eng', nova_janela))
            botao_run.grid(row=3, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

        elif idioma == 'pt-br':
            nova_janela.title("Aplicação do threshold")

            frame = tk.Frame(nova_janela)
            frame.grid(row=0, column=0)

            frame_titulo = tk.LabelFrame(frame, font=('Arial', 15), borderwidth=0, highlightthickness=0)
            frame_titulo.grid(row=0, column=0, sticky='nsew')
            frame_titulo.rowconfigure(0, weight=1)
            frame_titulo.columnconfigure([1, 2], weight=1)

            botao_voltar = tk.Button(frame_titulo, text='\u2b8c', font=('Arial', 14, 'bold'),
                                     command=lambda: nova_janela.destroy())
            botao_voltar.grid(row=0, column=0, sticky='w')

            label_novo_titulo = tk.Label(frame_titulo, text='Aplicação do threshold',
                                         font=('Arial', 16, 'bold'), borderwidth=2, relief='solid')
            label_novo_titulo.grid(row=0, column=1, padx=10, pady=5, sticky='nswe', columnspan=2)

            frame_selecao_arquivo = tk.LabelFrame(frame, font=('Arial', 15))
            frame_selecao_arquivo.grid(row=1, column=0)

            botao_selecionar_arquivo = tk.Button(frame_selecao_arquivo, text='Carregue um arquivo', font=('Arial', 14),
                                                 command=lambda: self.seleciona_arquivo('pt-br'))
            botao_selecionar_arquivo.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

            label_arquivo_selecionado = tk.Label(frame_selecao_arquivo, text='Nenhum arquivo carregado', font=('Arial', 14))
            label_arquivo_selecionado.grid(row=2, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

            nova_janela.focus_set()
            nova_janela.grab_set()

            frame_threshold = tk.LabelFrame(frame, text='Seleção de threshold', font=('Arial', 15))
            frame_threshold.grid(row=2, column=0, padx=10)

            label_threshold = tk.Label(frame_threshold, text='Indique o threshold em porcentagem: \n(use ponto como separador decimal, valor padrão 0.05)',
                                       font=('Arial', 14))
            label_threshold.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

            caixa_threshold = tk.Entry(frame_threshold, width=10, font=('Arial', 14))
            caixa_threshold.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

            label_threshold = tk.Label(frame_threshold,
                                       text='%',
                                       font=('Arial', 14))
            label_threshold.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

            botao_run = tk.Button(nova_janela, text='RODAR', font=('Arial', 14, 'bold'),
                                    command=lambda: self.roda_analise_primaria(caixa_threshold, 'pt-br', nova_janela))
            botao_run.grid(row=3, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

    # FIXME ajeitar docstrings
    def roda_analise_primaria(self, caixa_threshold, idioma, contexto):
        """Run threshold processing for OTUS/ASVs usando threading."""
        self.fila_resultados = queue.Queue()

        progressbar = ttk.Progressbar(contexto, mode='indeterminate')
        progressbar.grid(row=4, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)
        progressbar.start()

        botao_run = contexto.grid_slaves(row=3, column=0)[0]
        botao_run.config(state='disabled')

        caminho_arquivo = self.var_caminho_arquivo.get()
        string_threshold = caixa_threshold.get()

        thread_processamento = threading.Thread(
            target=self._processamento_primario_thread,
            args=(caminho_arquivo, string_threshold, idioma, contexto)
        )
        thread_processamento.daemon = True
        thread_processamento.start()

        contexto.after(100, self._verifica_processamento_primario, progressbar, botao_run, idioma, contexto)

    # FIXME ajeitar docstrings
    def _processamento_primario_thread(self, caminho_arquivo, string_threshold, idioma, contexto):
        """Função que roda em thread separada para o processamento pesado."""
        try:
            if '.xlsx' in caminho_arquivo:
                df = pd.read_excel(caminho_arquivo)
            elif '.csv' in caminho_arquivo:
                df = pd.read_csv(caminho_arquivo, sep=None, engine='python', encoding='utf-8-sig')

            threshold = 0.05 if string_threshold == '' else float(string_threshold)

            dfs_corridas = separa_corridas(df)
            selecionados, nao_selecionados, thresholds = aplica_threshold(dfs_corridas, threshold)

            resultado_tratado_geral = concatena_dfs(selecionados)
            nao_selecionados_geral = concatena_dfs(nao_selecionados)

            self.fila_resultados.put(('sucesso', resultado_tratado_geral, nao_selecionados_geral, thresholds))

        except UnboundLocalError:
            self.fila_resultados.put(('erro', 'UnboundLocalError'))
        except ValueError:
            self.fila_resultados.put(('erro', 'ValueError'))
        except Exception as e:
            print(f"Erro: {e}")
            self.fila_resultados.put(('erro', 'Exception'))

    # FIXME ajeitar docstrings
    def _verifica_processamento_primario(self, progressbar, botao_run, idioma, contexto):
        """Verifica periodicamente se o processamento terminou."""
        try:
            resultado = self.fila_resultados.get_nowait()
            status, *dados = resultado

            progressbar.stop()
            progressbar.grid_forget()

            botao_run.config(state='normal')

            if status == 'sucesso':
                resultado_tratado_geral, nao_selecionados_geral, thresholds = dados

                if idioma == 'eng':
                    msg_fim = tk.Label(contexto, text='Processing completed successfully!',
                                       font=('Arial', 14, 'bold'), fg='#009900')
                else:
                    msg_fim = tk.Label(contexto, text='Processamento concluído com sucesso!',
                                       font=('Arial', 14, 'bold'), fg='#009900')
                msg_fim.grid(row=5, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

                self._salvar_arquivos_primarios(resultado_tratado_geral, nao_selecionados_geral, thresholds, idioma)

            else:
                tipo_erro = dados[0]
                self._mostrar_erro_primario(tipo_erro, idioma, contexto)

        except queue.Empty:
            contexto.after(100, self._verifica_processamento_primario, progressbar, botao_run, idioma, contexto)

    # FIXME ajeitar docstrings
    def _mostrar_erro_primario(self, tipo_erro, idioma, contexto):
        """Mostra mensagens de erro."""
        if idioma == 'eng':
            if tipo_erro == 'UnboundLocalError':
                texto = 'ERROR: No file loaded or invalid input!'
            elif tipo_erro == 'ValueError':
                texto = 'ERROR: Invalid threshold value!'
            else:
                texto = 'An ERROR occurred!'
        else:
            if tipo_erro == 'UnboundLocalError':
                texto = 'ERRO: Nenhum arquivo carregado ou input inválido!'
            elif tipo_erro == 'ValueError':
                texto = 'ERRO: Valor inválido para threshold!'
            else:
                texto = 'Houve algum ERRO!'

        msg_erro = tk.Label(contexto, text=texto, font=('Arial', 14, 'bold'), fg='#ff0000')
        msg_erro.grid(row=5, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

    # FIXME ajeitar docstrings
    def _salvar_arquivos_primarios(self, resultado_tratado_geral, nao_selecionados_geral, thresholds, idioma):
        """Função para salvar os arquivos (pode ser otimizada se necessário)."""

        if idioma == 'eng':
            caminho_salvar_resultado = asksaveasfilename(title='Save the results table',
                                                         initialfile='processed_results',
                                                         defaultextension='.*',
                                                         filetypes=(("Excel files", "*.xlsx"), ("CSV files", "*.csv"),
                                                                    ("All files", "*.*")))

            resultado_tratado_geral['final_otu/asv_curated'] = ''

            if ".xlsx" in caminho_salvar_resultado:
                resultado_tratado_geral.to_excel(caminho_salvar_resultado, index=False)
            elif ".csv" in caminho_salvar_resultado:
                resultado_tratado_geral.to_csv(caminho_salvar_resultado, sep=';', encoding='utf-8-sig', index=False)

            caminho_salvar_resultado = asksaveasfilename(title='Save the table with deleted OTUS/ASVs',
                                                         initialfile='deleted_otus_asvs',
                                                         defaultextension='.*',
                                                         filetypes=(("Excel files", "*.xlsx"), ("CSV files", "*.csv"),
                                                                    ("All files", "*.*")))
            if ".xlsx" in caminho_salvar_resultado:
                nao_selecionados_geral.to_excel(caminho_salvar_resultado, index=False)
            elif ".csv" in caminho_salvar_resultado:
                nao_selecionados_geral.to_csv(caminho_salvar_resultado, sep=';', encoding='utf-8-sig', index=False)

            caminho_salvar_thresholds = asksaveasfilename(title='Save the thresholds table',
                                                          initialfile='thresholds',
                                                          defaultextension='.*',
                                                          filetypes=(("Excel files", "*.xlsx"), ("CSV files", "*.csv"),
                                                                     ("All files", "*.*")))
            if ".xlsx" in caminho_salvar_resultado:
                thresholds.to_excel(caminho_salvar_thresholds)
            elif ".csv" in caminho_salvar_resultado:
                thresholds.to_csv(caminho_salvar_thresholds, sep=';', encoding='utf-8-sig')
        elif idioma == 'pt-br':
            caminho_salvar_resultado = asksaveasfilename(title='Salve as tabelas dos resultados',
                                                         initialfile='resultados_processados',
                                                         defaultextension='.*',
                                                         filetypes=(("Excel files", "*.xlsx"), ("CSV files", "*.csv"),
                                                                    ("All files", "*.*")))

            resultado_tratado_geral['otu/asv_final_curada'] = ''

            if ".xlsx" in caminho_salvar_resultado:
                resultado_tratado_geral.to_excel(caminho_salvar_resultado, index=False)
            elif ".csv" in caminho_salvar_resultado:
                resultado_tratado_geral.to_csv(caminho_salvar_resultado, sep=';', encoding='utf-8-sig', index=False)

            caminho_salvar_resultado = asksaveasfilename(title='Salve tabelas com as OTUS/ASVs excluídas',
                                                         initialfile='otus_asvs_excluídas',
                                                         defaultextension='.*',
                                                         filetypes=(("Excel files", "*.xlsx"), ("CSV files", "*.csv"),
                                                                    ("All files", "*.*")))

            if ".xlsx" in caminho_salvar_resultado:
                nao_selecionados_geral.to_excel(caminho_salvar_resultado, index=False)
            elif ".csv" in caminho_salvar_resultado:
                nao_selecionados_geral.to_csv(caminho_salvar_resultado, sep=';', encoding='utf-8-sig', index=False)

            caminho_salvar_thresholds = asksaveasfilename(title='Salve a tabela de thresholds',
                                                          initialfile='thresholds',
                                                          defaultextension='.*',
                                                          filetypes=(("Excel files", "*.xlsx"), ("CSV files", "*.csv"),
                                                                     ("All files", "*.*")))

            if ".xlsx" in caminho_salvar_resultado:
                thresholds.to_excel(caminho_salvar_thresholds)
            elif ".csv" in caminho_salvar_resultado:
                thresholds.to_csv(caminho_salvar_thresholds, sep=';', encoding='utf-8-sig')

    def proc_tabelas_consolidadas(self, idioma):
        """Run the results consolidation process.

        Parameters:
        idioma (str): Indicates the chosen language, Portuguese ("pt-br") or English ("eng-us").
        """
        global label_arquivo_selecionado
        nova_janela = tk.Toplevel()
        nova_janela.resizable(0,0)
        nova_janela.rowconfigure(0, weight=1)
        nova_janela.columnconfigure(0, weight=1)

        if idioma == 'eng':
            nova_janela.title("Results consolidation")

            frame = tk.Frame(nova_janela)
            frame.grid(row=0, column=0, sticky='nsew')
            frame.columnconfigure(0, weight=1)

            frame_titulo = tk.LabelFrame(frame, font=('Arial', 15), borderwidth=0, highlightthickness=0)
            frame_titulo.grid(row=0, column=0, sticky='nsew')
            frame_titulo.rowconfigure(0, weight=1)
            frame_titulo.columnconfigure([1, 2], weight=1)

            botao_voltar = tk.Button(frame_titulo, text='\u2b8c', font=('Arial', 14, 'bold'),
                                     command=lambda: nova_janela.destroy())
            botao_voltar.grid(row=0, column=0, sticky='w')

            label_novo_titulo = tk.Label(frame_titulo, text='Results consolidation', font=('Arial', 16, 'bold'), borderwidth=2,  relief='solid')
            label_novo_titulo.grid(row=0, column=1, padx=10, pady=5, sticky='nsew', columnspan=2)

            frame_selecao_arquivo = tk.LabelFrame(frame, font=('Arial', 15))
            frame_selecao_arquivo.grid(row=1, column=0)

            botao_selecionar_arquivo = tk.Button(frame_selecao_arquivo, text='Load a file', font=('Arial', 14), command=lambda: self.seleciona_arquivo('eng'))
            botao_selecionar_arquivo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

            label_arquivo_selecionado = tk.Label(frame_selecao_arquivo, text='No file loaded', font=('Arial', 14))
            label_arquivo_selecionado.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

            nova_janela.focus_set()
            nova_janela.grab_set()

            frame_separacao = tk.LabelFrame(frame, text='Data filtering', font=('Arial', 15))
            frame_separacao.grid(row=2, column=0)

            label_separacoes = tk.Label(frame_separacao, text='Filter table by:', justify="left", font=('Arial', 14))
            label_separacoes.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

            var_amostrador = tk.BooleanVar(frame_separacao)
            botao_amostrador = tk.Checkbutton(frame_separacao, text='Sampler', variable=var_amostrador, font=('Arial', 14, 'bold'))
            botao_amostrador.grid(row=1, column=2, sticky='w')

            var_area = tk.BooleanVar(frame_separacao)
            botao_area = tk.Checkbutton(frame_separacao, text='Area', variable=var_area, font=('Arial', 14, 'bold'))
            botao_area.grid(row=2, column=2, sticky='w')

            frame_amostradores = tk.LabelFrame(frame, text='Samplers definition', font=('Arial', 15))
            frame_amostradores.grid(row=3, column=0)

            label_amostradores = tk.Label(frame_amostradores, text='Insert the samplers ID as identified \n in the table (one per row):', justify="left", font=('Arial', 14))
            label_amostradores.grid(row=1, column=0, padx=10, pady=10)

            caixa_amostradores = tk.Text(frame_amostradores, font=('Arial', 14), width=10, height=5)
            caixa_amostradores.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

            botao_run = tk.Button(nova_janela, text='RUN',  font=('Arial', 14, 'bold'), width=44, command=lambda: self.roda_analise_secundaria(caixa_amostradores, var_amostrador, var_area, 'eng', nova_janela))
            botao_run.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

        elif idioma == 'pt-br':
            nova_janela.title("Consolidação dos resultados")

            frame = tk.Frame(nova_janela)
            frame.grid(row=0, column=0, sticky='nsew')
            frame.columnconfigure(0, weight=1)

            frame_titulo = tk.LabelFrame(frame, font=('Arial', 15), borderwidth=0, highlightthickness=0)
            frame_titulo.grid(row=0, column=0, sticky='nsew')
            frame_titulo.rowconfigure(0, weight=1)
            frame_titulo.columnconfigure([1, 2], weight=1)

            botao_voltar = tk.Button(frame_titulo, text='\u2b8c', font=('Arial', 14, 'bold'),
                                     command=lambda: nova_janela.destroy())
            botao_voltar.grid(row=0, column=0, sticky='w')

            label_novo_titulo = tk.Label(frame_titulo, text='Consolidação dos resultados',
                                         font=('Arial', 16, 'bold'), borderwidth=2, relief='solid')
            label_novo_titulo.grid(row=0, column=1, padx=10, pady=5, sticky='nsew', columnspan=2)

            frame = tk.Frame(nova_janela)
            frame.grid(row=1, column=0)

            frame_selecao_arquivo = tk.LabelFrame(frame, font=('Arial', 15))
            frame_selecao_arquivo.grid(row=1, column=0)

            botao_selecionar_arquivo = tk.Button(frame_selecao_arquivo, text='Carregue um arquivo', font=('Arial', 14),
                                                 command=lambda: self.seleciona_arquivo('pt-br'))
            botao_selecionar_arquivo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

            label_arquivo_selecionado = tk.Label(frame_selecao_arquivo, text='Nenhum arquivo carregado', font=('Arial', 14))
            label_arquivo_selecionado.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

            nova_janela.focus_set()
            nova_janela.grab_set()

            frame_separacao = tk.LabelFrame(frame, text='Filtragem de dados', font=('Arial', 15))
            frame_separacao.grid(row=2, column=0)

            label_separacoes = tk.Label(frame_separacao, text='Filrar tabela por:', justify="left", font=('Arial', 14))
            label_separacoes.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

            var_amostrador = tk.BooleanVar(frame_separacao)
            botao_amostrador = tk.Checkbutton(frame_separacao, text='Amostrador', variable=var_amostrador,
                                              font=('Arial', 14, 'bold'))
            botao_amostrador.grid(row=1, column=2, sticky='w')

            var_area = tk.BooleanVar(frame_separacao)
            botao_area = tk.Checkbutton(frame_separacao, text='Área', variable=var_area, font=('Arial', 14, 'bold'))
            botao_area.grid(row=2, column=2, sticky='w')

            frame_amostradores = tk.LabelFrame(frame, text='Definição dos amostradores', font=('Arial', 15))
            frame_amostradores.grid(row=3, column=0)

            label_amostradores = tk.Label(frame_amostradores,
                                          text='Insira o ID dos amostradores como \nidentificado na tabela (um por linha):',
                                          justify="left", font=('Arial', 14))
            label_amostradores.grid(row=1, column=0, padx=10, pady=10)

            caixa_amostradores = tk.Text(frame_amostradores, font=('Arial', 14), width=10, height=5)
            caixa_amostradores.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

            botao_run = tk.Button(nova_janela, text='RODAR', font=('Arial', 14, 'bold'), width=44,
                                  command=lambda: self.roda_analise_secundaria(caixa_amostradores, var_amostrador,
                                                                               var_area, 'pt-br', nova_janela))
            botao_run.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

    def seleciona_arquivo(self, idioma):
        """Open a dialog box for selecting the input file.

        Parameters:
        idioma (str): Indicates the chosen language, Portuguese ("pt-br") or English ("eng-us").
        """
        if idioma == 'eng':
            tipos_de_arquivo = [('Excel file', '*.xlsx'), ('CSV file', '*.csv')]
            caminho_arquivo = askopenfilename(title='Load a file', filetypes=tipos_de_arquivo)
            self.var_caminho_arquivo.set(caminho_arquivo)
            if caminho_arquivo:
                label_arquivo_selecionado['text'] = f'Loaded file {caminho_arquivo}'
        elif idioma == 'pt-br':
            tipos_de_arquivo = [('Arquivo de Excel', '*.xlsx'), ('Arquivo CSV', '*.csv')]
            caminho_arquivo = askopenfilename(title='Carregue um arquivo', filetypes=tipos_de_arquivo)
            self.var_caminho_arquivo.set(caminho_arquivo)
            if caminho_arquivo:
                label_arquivo_selecionado['text'] = f'Arquivo carregado {caminho_arquivo}'

    # FIXME ajeitar docstrings
    def roda_analise_secundaria(self, caixa_amostradores, var_amostrador, var_area, idioma, contexto):
        """Run the second process of the program using threading."""
        self.fila_resultados_secundaria = queue.Queue()

        progressbar = ttk.Progressbar(contexto, mode='indeterminate')
        progressbar.grid(row=4, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)
        progressbar.start()

        botao_run = contexto.grid_slaves(row=2, column=0)[0]
        botao_run.config(state='disabled')

        texto_amostradores = caixa_amostradores.get('1.0', tk.END)
        lista_amostradores = texto_amostradores.split('\n')
        lista_amostradores.pop(-1)  # Remove última linha vazia

        var_amostrador_val = var_amostrador.get()
        var_area_val = var_area.get()

        thread_processamento = threading.Thread(
            target=self._processamento_secundario_thread,
            args=(lista_amostradores, var_amostrador_val, var_area_val, idioma)
        )
        thread_processamento.daemon = True
        thread_processamento.start()

        contexto.after(100, self._verifica_processamento_secundario, progressbar, botao_run, idioma, contexto)

    # FIXME ajeitar docstrings
    def _processamento_secundario_thread(self, lista_amostradores, var_amostrador, var_area, idioma):
        """Função que roda em thread separada para o processamento secundário."""
        try:
            if '.xlsx' in self.var_caminho_arquivo.get():
                df = pd.read_excel(self.var_caminho_arquivo.get())
            elif '.csv' in self.var_caminho_arquivo.get():
                df = pd.read_csv(self.var_caminho_arquivo.get(), sep=None, encoding='utf-8-sig', engine='python')

            lista_areas = define_areas(df)

            ocorrencias_geral = conta_ocorrencias_gerais(df, lista_areas)
            reads_gerais = conta_reads_gerais(df)
            lista_geral = cria_lista_geral(ocorrencias_geral, reads_gerais)

            # PROCESSAMENTO ESPECÍFICO
            if var_amostrador and not var_area:
                amostradores = separa_amostradores(df, lista_amostradores)
                ocorrencias = conta_ocorrencias(amostradores, amostradores=True)
                reads_especie = calcula_reads_especie(amostradores, amostrador=True)
                tabelas_finais = constroi_tabela_final(reads_especie, ocorrencias, amostradores=True)

            elif var_area and not var_amostrador:
                areas = separa_areas(lista_areas, df=df)
                ocorrencias = conta_ocorrencias(areas, areas=True)
                reads_especie = calcula_reads_especie(areas, area=True)
                tabelas_finais = constroi_tabela_final(reads_especie, ocorrencias, areas=True)

            elif var_amostrador and var_area:
                amostradores = separa_amostradores(df, lista_amostradores)
                lista_areas = define_areas(df)
                areas = separa_areas(lista_areas, amostradores=amostradores)
                ocorrencias_area = conta_ocorrencias(areas, amostradores=True, areas=True)
                reads_especie = calcula_reads_especie(areas, amostrador=True, area=True)
                tabelas_finais = constroi_tabela_final(reads_especie, ocorrencias_area, amostradores=True, areas=True)
            else:
                tabelas_finais = None

            self.fila_resultados_secundaria.put(('sucesso', lista_geral, tabelas_finais, var_amostrador, var_area))

        except (UnboundLocalError, KeyError) as e:
            self.fila_resultados_secundaria.put(('erro', 'UnboundLocalError'))
        except Exception as e:
            print(f"Erro: {e}")
            self.fila_resultados_secundaria.put(('erro', 'Exception'))

    # FIXME ajeitar docstrings
    def _verifica_processamento_secundario(self, progressbar, botao_run, idioma, contexto):
        """Verifica periodicamente se o processamento secundário terminou."""
        try:
            resultado = self.fila_resultados_secundaria.get_nowait()
            status, *dados = resultado

            progressbar.stop()
            progressbar.grid_forget()
            botao_run.config(state='normal')

            if status == 'sucesso':
                lista_geral, tabelas_finais, var_amostrador, var_area = dados

                if idioma == 'eng':
                    msg_fim = tk.Label(contexto, text='Processing completed successfully!',
                                       font=('Arial', 14, 'bold'), fg='#009900')
                else:
                    msg_fim = tk.Label(contexto, text='Processamento concluído com sucesso!',
                                       font=('Arial', 14, 'bold'), fg='#009900')
                msg_fim.grid(row=5, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

                self._salvar_arquivos_secundarios(lista_geral, tabelas_finais, var_amostrador, var_area, idioma)

            else:
                tipo_erro = dados[0]
                self._mostrar_erro_secundario(tipo_erro, idioma, contexto)

        except queue.Empty:
            contexto.after(100, self._verifica_processamento_secundario, progressbar, botao_run, idioma, contexto)

    # FIXME ajeitar docstrings
    def _mostrar_erro_secundario(self, tipo_erro, idioma, contexto):
        """Mostra mensagens de erro para o processamento secundário."""
        if idioma == 'eng':
            if tipo_erro == 'UnboundLocalError':
                texto = 'ERROR: No file loaded, invalid input or invalid samplers entered!'
            else:
                texto = 'An ERROR occurred!'
        else:
            if tipo_erro == 'UnboundLocalError':
                texto = 'ERRO: Nenhum arquivo carregado, input inválido ou amostradores informados inválidos!'
            else:
                texto = 'Houve algum ERRO!'

        msg_erro = tk.Label(contexto, text=texto, font=('Arial', 14, 'bold'), fg='#ff0000')
        msg_erro.grid(row=5, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

    # FIXME ajeitar docstrings
    def _salvar_arquivos_secundarios(self, lista_geral, tabelas_finais, var_amostrador, var_area, idioma):
        """Salva os arquivos resultantes do processamento secundário."""
        if idioma == 'eng':
            caminho_lista_geral = asksaveasfilename(title='Save general list', initialfile='general_list',
                                                    defaultextension='.*', filetypes=(
                    ("Excel files", "*.xlsx"), ("CSV file", "*.csv"), ("All files", "*.*")))
        elif idioma == 'pt-br':
            caminho_lista_geral = asksaveasfilename(title='Salve lista geral', initialfile='lista_geral',
                                                    defaultextension='.*', filetypes=(
                    ("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")))

        if caminho_lista_geral:
            if '.xlsx' in caminho_lista_geral:
                lista_geral.to_excel(caminho_lista_geral)
            elif '.csv' in caminho_lista_geral:
                lista_geral.to_csv(caminho_lista_geral, sep=';', encoding='utf-8-sig')

        # Diálogo para resultados específicos (se aplicável)
        if var_amostrador or var_area:
            if idioma == 'eng':
                caminho_resultado = asksaveasfilename(title='Save results', initialfile='results',
                                                      defaultextension='.*', filetypes=(
                        ("Excel files", "*.xlsx"), ("ZIP for CSV files", "*.zip"), ("All files", "*.*")))
            elif idioma == 'pt-br':
                caminho_resultado = asksaveasfilename(title='Salve os resultados', initialfile='resultados',
                                                      defaultextension='.*', filetypes=(
                        ("Excel files", "*.xlsx"), ("ZIP for CSV files", "*.zip"), ("All files", "*.*")))

            if caminho_resultado:
                if var_amostrador and not var_area:
                    salva_resultados(tabelas_finais, caminho_resultado, amostrador=True)
                elif var_area and not var_amostrador:
                    salva_resultados(tabelas_finais, caminho_resultado, area=True)
                elif var_amostrador and var_area:
                    salva_resultados(tabelas_finais, caminho_resultado, amostrador=True, area=True)


def main():
    """Initialize the graphical interface and run the program."""
    janela = Janelas()
    janela.inicia_janela()
    janela.idioma.mainloop()


if __name__ == "__main__":
    main()
