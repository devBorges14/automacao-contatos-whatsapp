"""
Este programa automatiza o envio de mensagens personalizadas pelo WhatsApp Web sem a
necessidade de serviços externos pagos. Ele lê uma planilha (Excel, CSV ou link do Google
Sheets) com telefones e mensagens e envia cada mensagem pelo WhatsApp Web, no seu navegador.

Versão 2026:
- Selenium 4 com Selenium Manager: NÃO precisa mais baixar o chromedriver.exe.
- Abre o navegador UMA vez e faz login (QR Code) só na primeira vez; a sessão fica salva.
- Lê as colunas pelo NOME do cabeçalho (Nome, Telefone, Mensagem personalizada...).
- Coloca o 55 automaticamente nos telefones brasileiros.
- Não manda duas vezes para o mesmo número (registros/enviados.csv).
- Intervalo aleatório entre mensagens e limite por execução, para não parecer robô.
- Modo teste: abre cada conversa com o texto pronto, mas NÃO aperta enviar.
"""
from __future__ import annotations

import csv
import datetime
import random
import re
import time
import unicodedata
from pathlib import Path
from urllib.parse import quote

import emoji
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait

try:  # notificação do Windows (opcional: em outros sistemas o programa funciona sem ela)
    from winotify import Notification, audio
except ImportError:
    Notification = None

# Pastas do programa (funciona em qualquer computador, sem caminho fixo)
PASTA = Path(__file__).resolve().parent
NAVEGADOR = "auto"   # "auto" (Chrome; se não tiver, Edge), "chrome" ou "edge"
PERFIL_CHROME = PASTA / "whatsapp_session"        # login do WhatsApp fica salvo aqui
PERFIL_EDGE = PASTA / "whatsapp_session_edge"
REGISTROS = PASTA / "registros"
ARQ_ENVIADOS = REGISTROS / "enviados.csv"
ARQ_ERROS = REGISTROS / "erros.csv"
ICONE = PASTA.parent / "logopy.png"

# Nomes aceitos para cada coluna da planilha (sem acento, minúsculo). Para usar outra
# planilha, basta acrescentar o nome do cabeçalho aqui.
COLUNAS = {
    "lead": ["lead", "id", "lead_id"],
    "nome": ["nome", "empresa", "cliente"],
    "telefone": ["telefone", "celular", "whatsapp", "fone", "numero"],
    "mensagem": ["mensagem personalizada", "mensagem", "mensagem_sugerida", "texto"],
}

# Seletores do WhatsApp Web (se o WhatsApp mudar a página, ajuste só aqui)
SEL_LISTA_CONVERSAS = "#pane-side, div[aria-label='Lista de conversas'], div[aria-label='Chat list']"
SEL_CAIXA_TEXTO = "footer div[contenteditable='true']"
SEL_BOTAO_ENVIAR = "button[aria-label='Enviar'], button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']"
TEXTOS_NUMERO_INVALIDO = ["inválido", "invalido", "invalid", "não está no whatsapp", "isn't on whatsapp"]


# ------------------------------------------------------------------ planilha
def _sem_acento(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in texto if not unicodedata.combining(c)).strip().lower()


def normalizar_telefone(valor) -> str | None:
    """'(11) 96643-7073', '11966437073', '11966437073.0' -> '5511966437073'."""
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        return None
    texto = re.sub(r"\.0$", "", str(valor).strip())
    digitos = re.sub(r"\D", "", texto).lstrip("0")
    if len(digitos) in (10, 11):            # DDD + número
        digitos = "55" + digitos
    if digitos.startswith("55") and len(digitos) in (12, 13):
        return digitos
    return None


def ler_planilha(origem: str) -> list[dict]:
    """Lê .xlsx/.xls, .csv ou um link do Google Sheets e devolve uma lista de contatos."""
    origem = origem.strip()
    link = re.search(r"docs\.google\.com/spreadsheets/d/([\w-]+)", origem)
    if link:
        # A planilha precisa estar compartilhada como "Qualquer pessoa com o link"
        url = f"https://docs.google.com/spreadsheets/d/{link.group(1)}/export?format=xlsx"
        tabela = pd.read_excel(url, dtype=str)
    elif origem.lower().endswith(".csv"):
        tabela = pd.read_csv(origem, dtype=str, sep=None, engine="python", encoding="utf-8-sig")
    else:
        tabela = pd.read_excel(origem, dtype=str)
    tabela = tabela.dropna(how="all")  # ignora linhas totalmente vazias

    # Descobre qual coluna é qual pelo nome do cabeçalho
    cabecalhos = {_sem_acento(c): c for c in tabela.columns}
    mapa = {}
    for campo, nomes in COLUNAS.items():
        for n in nomes:
            if n in cabecalhos:
                mapa[campo] = cabecalhos[n]
                break
    faltando = [c for c in ("telefone", "mensagem") if c not in mapa]
    if faltando:
        raise ValueError(f"A planilha precisa das colunas {faltando}. Colunas encontradas: {list(tabela.columns)}")

    contatos = []
    for i, linha in tabela.iterrows():
        def pegar(campo):
            valor = linha.get(mapa.get(campo, ""), "")
            return "" if pd.isna(valor) else str(valor).strip()
        contatos.append({
            "linha": i + 2,  # número da linha como aparece no Excel
            "lead": pegar("lead"),
            "nome": pegar("nome") or f"linha {i + 2}",
            "telefone_original": pegar("telefone"),
            "telefone": normalizar_telefone(pegar("telefone")),
            "mensagem": emoji.emojize(pegar("mensagem"), language="alias"),
        })
    return contatos


# ------------------------------------------------------------------ registros
def numeros_ja_enviados() -> set[str]:
    if not ARQ_ENVIADOS.exists():
        return set()
    with ARQ_ENVIADOS.open(encoding="utf-8") as f:
        return {linha["telefone"] for linha in csv.DictReader(f, delimiter=";")}


def registrar(arquivo: Path, contato: dict, detalhe: str = "") -> None:
    REGISTROS.mkdir(exist_ok=True)
    novo = not arquivo.exists()
    with arquivo.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        if novo:
            w.writerow(["data", "lead", "nome", "telefone", "detalhe"])
        w.writerow([datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), contato["lead"],
                    contato["nome"], contato["telefone"] or contato["telefone_original"], detalhe])


def notificar_erro(nome: str) -> None:
    if Notification is None:
        return
    try:
        n = Notification(app_id="Programa de automação", title="ERRO DE ENVIO!",
                         msg=f"Houve um problema ao enviar mensagem para {nome}", duration="short",
                         icon=str(ICONE) if ICONE.exists() else "")
        n.set_audio(audio.Default, loop=False)
        n.show()
    except Exception:
        pass


# ------------------------------------------------------------------ WhatsApp Web
class WhatsApp:
    def __init__(self, log=print):
        self.log = log
        self.navegador = None

    @staticmethod
    def _opcoes(classe, perfil: Path):
        opcoes = classe()
        opcoes.add_argument(f"--user-data-dir={perfil}")
        opcoes.add_argument("--lang=pt-BR")
        opcoes.add_argument("--start-maximized")
        opcoes.add_experimental_option("excludeSwitches", ["enable-automation"])
        opcoes.add_experimental_option("useAutomationExtension", False)
        return opcoes

    def _iniciar_navegador(self):
        """Selenium Manager baixa sozinho o driver compatível com o navegador instalado.
        NAVEGADOR = "auto" tenta o Chrome e, se não houver, usa o Edge (vem com o Windows)."""
        tentativas = {"chrome": [("Chrome", webdriver.Chrome, Options, PERFIL_CHROME)],
                      "edge": [("Edge", webdriver.Edge, EdgeOptions, PERFIL_EDGE)]}
        ordem = tentativas.get(NAVEGADOR) or tentativas["chrome"] + tentativas["edge"]
        erros = []
        for nome, classe, opcoes, perfil in ordem:
            try:
                driver = classe(options=self._opcoes(opcoes, perfil))
                self.log(f"Navegador: {nome}")
                return driver
            except WebDriverException as e:
                erros.append(f"{nome}: {str(e).splitlines()[0]}")
        raise RuntimeError("Não consegui abrir nenhum navegador. Instale o Google Chrome ou o Microsoft Edge.\n"
                           + "\n".join(erros))

    def abrir(self, tempo_login: int = 180) -> None:
        self.navegador = self._iniciar_navegador()
        self.navegador.get("https://web.whatsapp.com/")
        self.log("Abrindo o WhatsApp Web... se aparecer o QR Code, escaneie com o celular.")
        try:
            WebDriverWait(self.navegador, tempo_login).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, SEL_LISTA_CONVERSAS))
        except TimeoutException:
            raise RuntimeError("O login no WhatsApp Web não foi concluído a tempo.")
        self.log("WhatsApp Web conectado.")

    def _situacao_conversa(self, d):
        """Espera até a conversa abrir (caixa de texto) ou aparecer aviso de número inválido."""
        caixas = d.find_elements(By.CSS_SELECTOR, SEL_CAIXA_TEXTO)
        if caixas:
            return ("ok", caixas[-1])
        for dialogo in d.find_elements(By.CSS_SELECTOR, "div[role='dialog'], div[data-animate-modal-popup='true']"):
            texto = _sem_acento(dialogo.text)
            if any(_sem_acento(t) in texto for t in TEXTOS_NUMERO_INVALIDO):
                return ("invalido", None)
        return False

    def enviar(self, telefone: str, mensagem: str, teste: bool = False) -> tuple[bool, str]:
        self.navegador.get(f"https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}")
        try:
            situacao, caixa = WebDriverWait(self.navegador, 60, ignored_exceptions=(StaleElementReferenceException,)
                                            ).until(self._situacao_conversa)
        except TimeoutException:
            return False, "a conversa não abriu em 60s"
        if situacao == "invalido":
            return False, "número não tem WhatsApp ou é inválido"
        time.sleep(random.uniform(2, 4))  # dá tempo do texto aparecer, como uma pessoa faria
        if teste:
            return True, "modo teste: conversa aberta, NÃO enviada"

        botoes = self.navegador.find_elements(By.CSS_SELECTOR, SEL_BOTAO_ENVIAR)
        if botoes:
            botoes[0].click()
        else:
            caixa.send_keys(Keys.ENTER)
        # Confirma que saiu: a caixa de texto fica vazia depois do envio
        def caixa_vazia(d):
            caixas = d.find_elements(By.CSS_SELECTOR, SEL_CAIXA_TEXTO)
            return not caixas or not caixas[-1].text.strip()
        try:
            WebDriverWait(self.navegador, 20, ignored_exceptions=(StaleElementReferenceException,)).until(caixa_vazia)
        except TimeoutException:
            return False, "a mensagem ficou na caixa de texto e não foi enviada"
        time.sleep(random.uniform(3, 5))  # espera o envio terminar antes de trocar de conversa
        return True, "enviada"

    def fechar(self) -> None:
        if self.navegador:
            try:
                self.navegador.quit()
            except WebDriverException:
                pass
            self.navegador = None


# ------------------------------------------------------------------ fluxo principal
def processar_arquivo(caminho_arquivo, log=print, parar=None, teste=False,
                      intervalo=(40, 90), limite=30) -> dict:
    """Lê a planilha e envia as mensagens. `parar` é um threading.Event para interromper."""
    if not caminho_arquivo:
        log("Nenhum arquivo selecionado.")
        return {}
    contatos = ler_planilha(caminho_arquivo)
    ja_enviados = numeros_ja_enviados()
    fila, vistos, resumo = [], set(), {"enviadas": 0, "erros": 0, "puladas": 0}

    for c in contatos:
        motivo = None
        if not c["mensagem"]:
            motivo = "sem mensagem"
        elif not c["telefone"]:
            motivo = f"telefone inválido ({c['telefone_original'] or 'vazio'})"
        elif c["telefone"] in ja_enviados:
            motivo = "já enviado antes (registros/enviados.csv)"
        elif c["telefone"] in vistos:
            motivo = "telefone repetido na planilha"
        if motivo:
            resumo["puladas"] += 1
            log(f"Pulando {c['nome']} (linha {c['linha']}): {motivo}")
            continue
        vistos.add(c["telefone"])
        fila.append(c)

    if len(fila) > limite:
        log(f"{len(fila)} contatos na fila; enviando os {limite} primeiros (limite por execução).")
        fila = fila[:limite]
    if not fila:
        log("Nada para enviar.")
        return resumo
    log(f"{len(fila)} mensagem(ns) para {'ABRIR (modo teste)' if teste else 'enviar'}.")

    whatsapp = WhatsApp(log)
    try:
        whatsapp.abrir()
        for n, c in enumerate(fila, 1):
            if parar is not None and parar.is_set():
                log("Envio interrompido pelo usuário.")
                break
            log(f"[{n}/{len(fila)}] {c['nome']} ({c['telefone']})...")
            try:
                ok, detalhe = whatsapp.enviar(c["telefone"], c["mensagem"], teste)
            except WebDriverException as e:
                ok, detalhe = False, f"erro do navegador: {e.msg if hasattr(e, 'msg') else e}"
            if ok:
                log(f"   OK: {detalhe}")
                if not teste:
                    registrar(ARQ_ENVIADOS, c, detalhe)
                    resumo["enviadas"] += 1
            else:
                log(f"   ERRO: {detalhe}")
                registrar(ARQ_ERROS, c, detalhe)
                notificar_erro(c["nome"])
                resumo["erros"] += 1
            if n < len(fila):
                espera = random.uniform(*intervalo) if not teste else 5
                log(f"   aguardando {espera:.0f}s antes da próxima...")
                fim = time.time() + espera
                while time.time() < fim and not (parar is not None and parar.is_set()):
                    time.sleep(0.5)
    finally:
        whatsapp.fechar()
    log(f"Fim: {resumo['enviadas']} enviadas, {resumo['erros']} erros, {resumo['puladas']} puladas.")
    return resumo
