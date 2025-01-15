"""
Este programa automatiza o envio de mensagens personalizadas pelo WhatsApp sem a 
necessidade de serviços externos pagos. Ele lê uma planilha Excel contendo números de telefone e mensagens, 
integra-se ao WhatsApp Web para enviar mensagens diretamente aos destinatários. É uma ferramenta prática para 
uso pessoal ou comercial, ideal para comunicação rápida e organizada.
"""
from winotify import Notification, audio
import datetime
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import openpyxl
from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import emoji
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Configurar opções do Chrome
# Esse trecho de código serve para configurar opções personalizadas do navegador Chrome ao usar o Selenium WebDriver. 
# Cada linha possui uma função específica para controlar o comportamento do Chrome durante a automação.
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--user-data-dir=C:/meu_projeto/whatsapp_session")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)

# Configurar o caminho para o ChromeDriver (local do programa)
servico = Service("E:\\Programa de automação\\chromedriver.exe")
# Procurando o arquivo e abrindo-o
def processar_arquivo(caminho_arquivo):
    try:
        if not caminho_arquivo:
            print("Nenhum arquivo selecionado.") # Caso não seja colocado nenhum arquivo
            return
         # Abrir o arquivo Excel
        workbook = openpyxl.load_workbook(caminho_arquivo)
        pagina_clientes = workbook.active
        # Pegando as informações nescessarias (caso necessite mudar o dados que devem ser recolidos, alterar aqui):
        for linha in pagina_clientes.iter_rows(min_row=2):
            try:
                nome = linha[0].value
                telefone = str(int(float(linha[1].value)))
                telefone = telefone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                endereco = linha[2].value
                dia = linha[3].value
                hora = linha[4].value
                cliente = linha[5].value
                # Inicializar o navegador com as configurações definidas dentro do for para que haja repetição
                navegador = webdriver.Chrome(service=servico, options=chrome_options)
                navegador.maximize_window() # Maximizar a janela do navegador

                # Montando mesagem personalizada (ALTERAR MENSAGEM AQUI):    
                mensagem = emoji.emojize(
                    f"Olá, {nome}, tudo bem?:beaming_face_with_smiling_eyes: Estou passando para avisar que tem montagem para o dia {dia.strftime('%d/%m/%Y')} às {hora.strftime('%H:%M')}, no endereço {endereco}. Nome do cliente: {cliente}."
                    )
                # Abrir o WhatsApp Web e criando o link para enviar a mensagem
                link_mensagem_whatsapp = f'https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}'
                navegador.get(link_mensagem_whatsapp)
                sleep(20)
                # Enviando a mensagem
                campo_mensagem = WebDriverWait(navegador, 120).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                )
                campo_mensagem.send_keys(Keys.ENTER)
                sleep(15)
                print(f'Mensagem enviada com sucesso para {nome}')
                # Fechando o navegador
                navegador.quit()
            # Caso ocorra algum erro, sera salvo no arquivo erros.csv
            except Exception as e:
                data_atual = datetime.datetime.now() # Recolher data e horario atual do dispositivo
                # Notificação em tempo real
                notificacao = Notification(
                    app_id='Programa de automação', 
                    title='ERRO DE ENVIO!', msg=f'Houve um problema ao enviar mensagem para {nome}', 
                    duration='long', icon=r'E://Programa de automação/logopy.png'
                ) 
                notificacao.set_audio(audio.LoopingAlarm, loop=False) # Setando um som para a notificação
                notificacao.show() # Mostrar notificação

                print(f"Não foi possível enviar mensagem para {nome}") # Imprimindo erro no console
                with open('erros.csv', 'a', newline='', encoding='utf-8') as arquivo: # Salvando os erros
                    arquivo.write(f'{nome}, {telefone}, {data_atual.strftime('%d-%m-%Y %H:%M')}\n') # No arquivo CSV salvo os erros com data e horario dos erros para serem verificados posteriormente

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}") 
