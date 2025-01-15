# Automacao de envio de mensagens
Este programa automatiza o envio de mensagens personalizadas pelo WhatsApp WEB sem a necessidade de serviços externos pagos. Ele lê uma planilha Excel contendo números de telefone e mensagens,  integra-se ao WhatsApp Web para enviar mensagens diretamente aos destinatários.

# Tecnologias:
- Python
- winotify
- datetime
- os
- tkinter
- filedialog
- messagebox
- pandas
- selenium
- selenium.webdriver
- openpyxl
- urllib.parse
- emoji
- selenium.webdriver.chrome.options
- selenium.webdriver.chrome.service

# PRÉ REQUISTOS
1) Instale Python3 (https://www.python.org/downloads/)
![image](https://github.com/user-attachments/assets/0ded5cf5-4d7d-4fe6-96ca-42eee8fce90e)

2) Instale Chrome Driver na pasta do arquivo (https://developer.chrome.com/docs/chromedriver/downloads?hl=pt-br)
  Tutorial do Jonathan da Dev Aprender (https://www.youtube.com/watch?v=Ot10qzrb13c)

3) Use um ambiente virtual:
````Crie um ambiente virtual para gerenciar dependências e evitar problemas de configuração:
python -m venv meu_ambiente
source venv/bin/activate   # No Windows: venv\Scripts\activate
````
4) Instale as dependências:
   
As dependências necessárias para o funcionamento do código são:
winotify: Para mostrar notificações no Windows.
  - Instalação: ````pip install winotify````
pandas: Para manipulação de dados em formato de tabela (DataFrame).
  - Instalação: ````pip install pandas````
selenium: Para automação de navegadores, utilizado para interação com sites.
  - Instalação: ````pip install selenium````
openpyxl: Para ler e escrever arquivos Excel (.xlsx).
  - Instalação: ````pip install openpyxl````
emoji: Para manipular e processar emojis em textos.
  - Instalação: ````pip install emoji````
tkinter: Para criar interfaces gráficas (GUI). Geralmente já está incluído com a instalação padrão do Python.
Além disso, o código utiliza módulos internos do Python, como ````os````, ````datetime````, ````filedialog````, ````messagebox````, ````urllib.parse```` e outros.
