"""Tela do programa (Tkinter). Rode com:  python SimpleGUI.py"""
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from app import ARQ_ENVIADOS, REGISTROS, processar_arquivo

mensagens = queue.Queue()   # o envio roda em outra thread; a tela lê o log daqui
parar = threading.Event()
caminho_arquivo = {"valor": ""}


def log(texto):
    mensagens.put(texto)


def atualizar_log():
    while not mensagens.empty():
        caixa_log.insert(tk.END, mensagens.get() + "\n")
        caixa_log.see(tk.END)
    janela.after(300, atualizar_log)


# Função para abrir a janela de seleção de arquivo
def selecionar_arquivo():
    caminho = filedialog.askopenfilename(
        filetypes=[("Planilhas", "*.xlsx *.xls *.csv"), ("Todos os arquivos", "*.*")])
    if caminho:
        caminho_arquivo["valor"] = caminho
        campo_link.delete(0, tk.END)
        arquivo_label.config(text=f"Arquivo selecionado: {caminho}")
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")


def origem_escolhida():
    link = campo_link.get().strip()
    return link if link else caminho_arquivo["valor"]


def ler_numero(campo, padrao):
    try:
        return max(1, int(campo.get()))
    except ValueError:
        return padrao


# Função para processar a planilha (em segundo plano, a tela não trava)
def processar():
    origem = origem_escolhida()
    if not origem:
        messagebox.showwarning("Aviso", "Selecione a planilha ou cole o link do Google Sheets.")
        return
    teste = modo_teste.get()
    limite = ler_numero(campo_limite, 30)
    minimo = ler_numero(campo_min, 40)
    maximo = max(minimo, ler_numero(campo_max, 90))
    aviso = ("MODO TESTE: as conversas serão abertas com o texto pronto, mas nada será enviado.\n\n"
             if teste else "As mensagens serão ENVIADAS de verdade.\n\n")
    if not messagebox.askyesno("Iniciar", aviso + f"Até {limite} contatos, com {minimo} a {maximo}s entre eles.\n"
                               "Não use o mouse no navegador enquanto o programa trabalha.\n\nContinuar?"):
        return
    parar.clear()
    botao_processar.config(state=tk.DISABLED)
    botao_parar.config(state=tk.NORMAL)

    def trabalho():
        try:
            resumo = processar_arquivo(origem, log=log, parar=parar, teste=teste,
                                       intervalo=(minimo, maximo), limite=limite)
            log(f"Concluído! {resumo}")
        except Exception as e:
            log(f"ERRO: {e}")
        finally:
            janela.after(0, lambda: (botao_processar.config(state=tk.NORMAL),
                                     botao_parar.config(state=tk.DISABLED)))
    threading.Thread(target=trabalho, daemon=True).start()


def interromper():
    parar.set()
    log("Parando depois do contato atual...")


def abrir_registros():
    REGISTROS.mkdir(exist_ok=True)
    import os, subprocess, sys
    if sys.platform.startswith("win"):
        os.startfile(REGISTROS)
    else:
        subprocess.Popen(["xdg-open", str(REGISTROS)])


# Criar a janela principal
janela = tk.Tk()
janela.title("Automação de contatos - WhatsApp")
janela.geometry("760x620")

# Layout
arquivo_label = tk.Label(janela, text="Selecione o arquivo .xlsx / .csv ou cole o link do Google Sheets", width=90, height=2)
arquivo_label.pack(pady=(15, 5))
tk.Button(janela, text="Selecionar planilha", command=selecionar_arquivo, width=30).pack()

quadro_link = tk.Frame(janela)
quadro_link.pack(pady=8)
tk.Label(quadro_link, text="ou link do Google Sheets:").pack(side=tk.LEFT)
campo_link = tk.Entry(quadro_link, width=60)
campo_link.pack(side=tk.LEFT, padx=5)

quadro_opcoes = tk.Frame(janela)
quadro_opcoes.pack(pady=5)
tk.Label(quadro_opcoes, text="Máx. por vez:").grid(row=0, column=0)
campo_limite = tk.Entry(quadro_opcoes, width=5); campo_limite.insert(0, "30"); campo_limite.grid(row=0, column=1, padx=(0, 15))
tk.Label(quadro_opcoes, text="Intervalo (s) de").grid(row=0, column=2)
campo_min = tk.Entry(quadro_opcoes, width=5); campo_min.insert(0, "40"); campo_min.grid(row=0, column=3)
tk.Label(quadro_opcoes, text="a").grid(row=0, column=4)
campo_max = tk.Entry(quadro_opcoes, width=5); campo_max.insert(0, "90"); campo_max.grid(row=0, column=5, padx=(0, 15))
modo_teste = tk.BooleanVar(value=True)
tk.Checkbutton(quadro_opcoes, text="Modo teste (não envia)", variable=modo_teste).grid(row=0, column=6)

# Botões
quadro_botoes = tk.Frame(janela)
quadro_botoes.pack(pady=10)
botao_processar = tk.Button(quadro_botoes, text="Processar", command=processar, width=20)
botao_processar.pack(side=tk.LEFT, padx=5)
botao_parar = tk.Button(quadro_botoes, text="Parar", command=interromper, width=10, state=tk.DISABLED)
botao_parar.pack(side=tk.LEFT, padx=5)
tk.Button(quadro_botoes, text="Registros", command=abrir_registros, width=10).pack(side=tk.LEFT, padx=5)
tk.Button(quadro_botoes, text="Sair", command=janela.quit, width=10).pack(side=tk.LEFT, padx=5)

caixa_log = scrolledtext.ScrolledText(janela, height=22, width=95)
caixa_log.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
log(f"Pronto. Números já enviados ficam em {ARQ_ENVIADOS} e não recebem de novo.")

# Iniciar a interface gráfica
atualizar_log()
janela.mainloop()
