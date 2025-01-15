import tkinter as tk
from tkinter import filedialog, messagebox
from app import processar_arquivo
# Função para abrir a janela de seleção de arquivo e processar o arquivo
def selecionar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(
        filetypes=[("Planilhas Excel", "*.xlsx *.xls")]
    )
    if caminho_arquivo:
        arquivo_label.config(text=f"Arquivo selecionado: {caminho_arquivo}")
        return caminho_arquivo
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")
        return None

# Função para processar o arquivo selecionado
def processar():
    caminho_arquivo = selecionar_arquivo()
    if caminho_arquivo:
        messagebox.showinfo("Iniciando", "Iniciando a automação...")
        try:
            processar_arquivo(caminho_arquivo)
            messagebox.showinfo("Concluído", "Processamento concluido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

# Criar a janela principal
janela = tk.Tk()
janela.title("Processar Arquivo Excel")

# Layout
janela.geometry("600x300")
arquivo_label = tk.Label(janela, text="Arraste ou selecione o arquivo.xlsx", width=70, height=3)
arquivo_label.pack(pady=20)

# Botões
botao_processar = tk.Button(janela, text="Processar", command=processar, width=30, height=1)
botao_processar.pack(pady=20)
botao_sair = tk.Button(janela, text="Sair", command=janela.quit, width=10, height=1)
botao_sair.pack(pady=20)

# Iniciar a interface gráfica
janela.mainloop()

