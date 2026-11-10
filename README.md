# Automacao de envio de mensagens

Este programa automatiza o envio de mensagens personalizadas pelo WhatsApp WEB sem a necessidade de serviços externos pagos. Ele lê uma planilha (Excel, CSV ou link do Google Sheets) contendo números de telefone e mensagens, integrando-se ao WhatsApp Web para enviar mensagens diretamente aos destinatários.

## Novidades da versão 2026
- **Não precisa mais baixar o ChromeDriver**: o Selenium 4 baixa o driver certo sozinho (Selenium Manager).
- Funciona com **Google Chrome ou Microsoft Edge** (usa o Chrome se tiver; senão, o Edge que já vem no Windows).
- O navegador abre **uma vez só** e o login (QR Code) fica salvo para as próximas vezes.
- Aceita **link do Google Sheets** direto na tela, além de `.xlsx` e `.csv`.
- Lê as colunas pelo **nome do cabeçalho**, então a ordem das colunas não importa.
- Coloca o **55** automaticamente nos telefones (`11966437073` → `5511966437073`).
- **Não manda duas vezes** para o mesmo número (`Interface/registros/enviados.csv`).
- **Modo teste**: abre cada conversa com o texto pronto, mas não envia.
- **Intervalo aleatório** entre mensagens, **limite por vez** e botão **Parar**.
- Detecta **número sem WhatsApp** e registra em `Interface/registros/erros.csv`.
- A tela não trava mais durante o envio e mostra o andamento.

## Tecnologias:
- Python 3.10+
- tkinter (interface)
- selenium 4 (WhatsApp Web)
- pandas + openpyxl (planilha)
- emoji
- winotify (notificações no Windows)

## PRÉ-REQUISITOS

### 1) Instale Python 3
[Download do Python](https://www.python.org/downloads/)

### 2) Tenha o Google Chrome ou o Microsoft Edge instalado
Não é mais preciso baixar o ChromeDriver nem colocar nada na pasta.

### 3) Use um ambiente virtual (recomendado):
```bash
python -m venv venv
venv\Scripts\activate        # No Linux/Mac: source venv/bin/activate
```

### 4) Instale as dependências:
```bash
pip install -r requirements.txt
```

### 5) Formato da planilha
A primeira linha precisa ter os nomes das colunas. Obrigatórias: **Telefone** e **Mensagem personalizada**.
As outras são usadas no log e nos registros. Exemplo:

| Lead | Nome | Endereço | Telefone | Tipo de comercio | Tem site? | Site | Mensagem personalizada |
|---|---|---|---|---|---|---|---|
| 1 | Filipi Garage | Estr. São Francisco, 618... | 11966437073 | Oficina | NÃO | | Olá, tudo bem? Sou o Gabriel... |

- Nomes aceitos para cada coluna (maiúsculas e acentos não importam): veja `COLUNAS` no começo do `Interface/app.py`.
- Telefone com ou sem 55, com ou sem parênteses e traço. Linhas sem telefone válido ou sem mensagem são puladas.
- Pode usar emojis direto no texto ou códigos como `:smile:`. Quebras de linha também funcionam.
- **Google Sheets**: compartilhe como "Qualquer pessoa com o link" (leitor) e cole o link na tela.

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

### 3) Execute o programa:
```bash
cd Interface
python SimpleGUI.py
```

### 4) Na tela
1. Clique em **Selecionar planilha** ou cole o **link do Google Sheets**.
2. Ajuste **Máx. por vez** e o **intervalo** entre mensagens.
3. Deixe **Modo teste** marcado na primeira vez: ele abre cada conversa com o texto, sem enviar.
4. Clique em **Processar**. Na primeira vez, escaneie o QR Code do WhatsApp Web com o celular.
5. Para enviar de verdade, desmarque **Modo teste** e processe de novo.

Não mexa no navegador enquanto o programa trabalha. O botão **Registros** abre a pasta com
`enviados.csv` e `erros.csv`. Para reenviar a alguém, apague a linha dele do `enviados.csv`.

---

## Cuidados (leia antes de usar)
- O WhatsApp **não permite automação** em contas comuns e pode **banir o número** se perceber envio em massa,
  muitas mensagens para quem não tem você salvo, ou muitas denúncias de spam.
- Use **lotes pequenos** (ex.: 15 a 30 por dia) e **intervalos longos**. Os padrões do programa já são conservadores.
- Mande só para quem faz sentido receber, sempre com uma forma fácil de recusar ("se não for do seu interesse, é só me avisar"),
  e respeite quem pedir para parar.
- Prefira um número comercial/secundário, não o seu número pessoal principal.
- Telefones fixos (ex.: `1136891375`) só funcionam se a empresa usar WhatsApp Business nesse número; senão vão para `erros.csv`.

---

## Possíveis Erros e Soluções

### 1. "Não consegui abrir nenhum navegador"
**Solução**: instale o Google Chrome ou o Microsoft Edge. Para forçar um deles, mude `NAVEGADOR` no começo do `Interface/app.py` (`"chrome"` ou `"edge"`).

### 2. Pede o QR Code toda vez / erro de perfil em uso
**Problema**: o login fica salvo em `Interface/whatsapp_session` (ou `whatsapp_session_edge`). Se outra janela do programa estiver aberta, o perfil fica bloqueado.
**Solução**: feche todas as janelas abertas pelo programa e tente de novo.

### 3. Dependências não instaladas
```bash
pip install -r requirements.txt
```

### 4. Problema com a planilha
**Problema**: "A planilha precisa das colunas ['telefone', 'mensagem']".
**Solução**: confira os nomes do cabeçalho na primeira linha ou acrescente o nome que você usa em `COLUNAS` no `app.py`.

### 5. Link do Google Sheets não abre
**Solução**: no Google Sheets, clique em Compartilhar → "Qualquer pessoa com o link" → Leitor.

### 6. WhatsApp Web alterou sua interface
**Problema**: o WhatsApp Web pode mudar a página, e o programa para de achar a caixa de texto ou o botão de enviar.
**Solução**: ajuste os seletores `SEL_...` no começo do `Interface/app.py`.

### 7. Segurança
As pastas `whatsapp_session*` guardam o login do seu WhatsApp e `registros/` guarda telefones. As duas estão no `.gitignore`: **nunca** suba essas pastas para o GitHub.

---

## Contribuições
Se você deseja contribuir com melhorias, sinta-se à vontade para:
- Abrir um **issue** relatando problemas ou sugerindo melhorias.
- Criar um **pull request** com novos recursos ou correções.

Obrigado por utilizar este projeto! 🚀
