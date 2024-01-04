from tkinter.filedialog import askdirectory


def salva_arquivo(arquivo):
    arq = asksaveasfile(initialfile=arquivo, defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])