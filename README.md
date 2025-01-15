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
PARA INSTALAMENTO GERAL USE:
````pip install -r requirements.txt````

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

# ERROS que podem acontecer

1. Caminho do chromedriver
Problema: O caminho especificado para o chromedriver no código (E:\\Programa de automação\\chromedriver.exe) pode não ser válido no sistema de outro usuário. Isso pode resultar em um erro de "chromedriver not found".
Solução: Certifique-se de que o caminho para o chromedriver.exe seja relativo ou forneça instruções para o usuário configurar o caminho corretamente. O código pode ser alterado para permitir que o usuário insira o caminho para o chromedriver ou detecte automaticamente a localização do chromedriver se ele estiver no mesmo diretório do script.
2. Diretório de dados do usuário (user-data-dir)
Problema: O caminho do diretório de dados do usuário no Chrome (C:/meu_projeto/whatsapp_session) pode não existir ou não ser acessível para outro usuário. Além disso, o Chrome pode precisar de permissões para gravar nesse diretório.
Solução: Usar um diretório mais genérico ou permitir que o usuário defina o diretório. O caminho pode ser configurado para um diretório dentro da pasta do programa ou do usuário atual.
python
````chrome_options.add_argument(f"user-data-dir={os.path.join(os.getenv('APPDATA'), 'whatsapp_session')}")````
3. Versão do ChromeDriver e do Google Chrome
Problema: O chromedriver precisa ser compatível com a versão do Google Chrome do usuário. Se a versão do chromedriver não for compatível com o Chrome instalado no computador do usuário, o Selenium não funcionará corretamente.
Solução: Certifique-se de que o usuário tenha a versão correta do chromedriver para o navegador instalado. O chromedriver pode ser atualizado para a versão mais recente, ou você pode incluir uma verificação de versão do Chrome e instruções para o usuário fazer o download correto.
4. Permissões de Acesso
Problema: O script pode precisar de permissões administrativas para acessar alguns diretórios ou executar o ChromeDriver.
Solução: Se necessário, adicione verificações para garantir que o script tenha as permissões necessárias ou instrua o usuário a executar o script com permissões elevadas.
5. Dependências não instaladas
Problema: O usuário pode não ter as dependências Python instaladas no sistema, como selenium, openpyxl, winotify, entre outras.
````bash pip install -r requirements.txt````
6. Versão do Python
Problema: O código pode não funcionar corretamente em versões muito antigas ou muito novas do Python, ou se o Python não estiver instalado corretamente.
Solução: Certifique-se de que o Python esteja instalado corretamente e que a versão do Python seja compatível com as bibliotecas. O código deve funcionar com Python 3.6 ou superior, que é a versão mais comum para automações como essa.
7. Problema com o arquivo Excel
Problema: Se o arquivo Excel não estiver no formato esperado (por exemplo, faltando colunas ou dados mal formatados), o código pode falhar ao tentar acessar dados nas células.
Solução: Verifique se o arquivo Excel está no formato correto. Adicione validações para garantir que os dados estejam no formato esperado antes de tentar processá-los.
8. Mensagens e Emojis
Problema: Caso o nome ou qualquer outro dado extraído do Excel contenha caracteres especiais ou não seja processado corretamente, isso pode resultar em falhas ao montar a mensagem.
Solução: Trate os erros de codificação de texto e garanta que todos os caracteres especiais (como acentos e emojis) sejam corretamente codificados ao gerar a URL.
9. Erro ao enviar mensagens
Problema: O WhatsApp Web pode mudar seu layout ou exigir novos elementos de interação, causando falhas ao tentar enviar mensagens.
Solução: Realize testes regulares para verificar a integridade do código com atualizações do WhatsApp Web e ajuste o código conforme necessário.
Conclusão:
Para garantir que outro usuário consiga executar o código corretamente, você deve:

Garantir que o caminho do chromedriver seja configurável.
Verificar se o diretório de dados do usuário está correto.
Garantir que as dependências estejam instaladas corretamente.
Instruir o usuário a configurar o ambiente corretamente (como o Python, versões de bibliotecas e permissões de acesso).
