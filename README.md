# Automacao de envio de mensagens

Este programa automatiza o envio de mensagens personalizadas pelo WhatsApp WEB sem a necessidade de serviços externos pagos. Ele lê uma planilha Excel contendo números de telefone e mensagens, integrando-se ao WhatsApp Web para enviar mensagens diretamente aos destinatários.

## Tecnologias:
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

## PRÉ-REQUISITOS

### 1) Instale Python 3  
[Download do Python](https://www.python.org/downloads/)

### 2) Instale Chrome Driver na pasta do arquivo  
[Baixar ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads?hl=pt-br)  
[Tutorial do Jonathan da Dev Aprender](https://www.youtube.com/watch?v=Ot10qzrb13c)

- <a href="https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/driver_location/">Documentação de ERROS possíveis do ChromeDriver<a>
### 3) Use um ambiente virtual:
Crie um ambiente virtual para gerenciar dependências e evitar problemas de configuração:
```bash
python -m venv meu_ambiente
source venv/bin/activate   # No Windows: venv\Scripts\activate
```

### 4) Instale as dependências:
Para instalar todas as dependências de uma vez, use:
```bash
pip install -r requirements.txt
```

As dependências necessárias para o funcionamento do código são:

- **winotify**: Para mostrar notificações no Windows.
  - Instalação: `pip install winotify`
- **pandas**: Para manipulação de dados em formato de tabela (DataFrame).
  - Instalação: `pip install pandas`
- **selenium**: Para automação de navegadores, utilizado para interação com sites.
  - Instalação: `pip install selenium`
- **openpyxl**: Para ler e escrever arquivos Excel (.xlsx).
  - Instalação: `pip install openpyxl`
- **emoji**: Para manipular e processar emojis em textos.
  - Instalação: `pip install emoji`
- **tkinter**: Para criar interfaces gráficas (GUI). Geralmente já está incluído na instalação padrão do Python.

Além disso, o código utiliza módulos internos do Python, como `os`, `datetime`, `filedialog`, `messagebox`, `urllib.parse`, entre outros.

### 5) Verifique se a planilha está no formato correto:
Caso precise ajustar, o formato correto está entre as linhas 53 e 59 do código:
```plaintext
nome         telefone       endereco               dia         hora        cliente
João Silva  5511963082543  Rua das flores        2024-12-25  14:00:00   Miguel
Maria        5511963082543  Praça Miguel Ortega  2024-11-10  08:00:00   Silvia
Gabriel      5511963082543  Alvezedo Lima        2025-01-13  16:00:00   José
```

### 6) Verifique se os números estão no formato correto:
Formato Brasileiro: `5511*********`

---

## Possíveis Erros e Soluções

### 1. Caminho do ChromeDriver
**Problema**: O caminho especificado para o `chromedriver.exe` pode não ser válido no sistema do usuário, resultando em erro de "chromedriver not found".  
**Solução**: Certifique-se de que o caminho está correto e ajuste-o conforme necessário.

### 2. Diretório de dados do usuário (user-data-dir)
**Problema**: O Chrome pode não encontrar ou ter permissões para o diretório especificado.  
**Solução**: Ajuste o código para usar um diretório genérico.
```python
chrome_options.add_argument(f"user-data-dir={os.path.join(os.getenv('APPDATA'), 'whatsapp_session')}")
```

### 3. Versão do ChromeDriver e do Google Chrome
**Problema**: O ChromeDriver precisa ser compatível com a versão do Chrome instalado.  
**Solução**: Baixe a versão correta do ChromeDriver conforme o navegador.

### 4. Dependências não instaladas
**Problema**: O usuário pode não ter todas as bibliotecas necessárias.  
**Solução**: Rode novamente:
```bash
pip install -r requirements.txt
```

### 5. Problema com o arquivo Excel
**Problema**: Se a planilha não estiver formatada corretamente, o código pode falhar.  
**Solução**: Verifique se as colunas e dados estão corretos antes de rodar o script.

### 6. WhatsApp Web alterou sua interface
**Problema**: O WhatsApp Web pode mudar sua estrutura, fazendo com que o código pare de funcionar.  
**Solução**: Atualize o código regularmente para se adaptar às mudanças.
---

## Como Rodar

### 1) Clone o repositório:
```bash
git clone https://github.com/devBorges14/automacao-contatos-whatsapp.git
```

### 2) Instale as dependências:
```bash
pip install -r requirements.txt
```

### 3) Configurar o ChromeDriver:
Baixe o ChromeDriver adequado para sua versão do Chrome em:
[Baixar ChromeDriver](https://sites.google.com/chromium.org/driver/)

Coloque o `chromedriver.exe` no diretório especificado ou ajuste o caminho no código, caso necessário.

### 4) Execute o programa:
Abra o terminal na pasta onde o arquivo `SimpleGUI.py` está localizado e execute:
```bash
python SimpleGUI.py
```

### 5) Selecione a planilha com os contatos:
Certifique-se de que o arquivo contém números válidos e está no formato correto antes de iniciar o envio das mensagens.

---

## Contribuições
Se você deseja contribuir com melhorias, sinta-se à vontade para:
- Abrir um **issue** relatando problemas ou sugerindo melhorias.
- Criar um **pull request** com novos recursos ou correções.

Obrigado por utilizar este projeto! 🚀

