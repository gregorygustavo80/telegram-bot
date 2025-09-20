# 🔎 Rastreador de Preços com Notificação no Telegram

Este projeto é um **script em Python** que monitora o preço de um produto da Amazon e envia notificações via **Telegram** quando o valor sobe ou cai.  
Além disso, ele mantém um histórico dos preços em um arquivo local.

---

## 🚀 Funcionalidades

- Faz scraping do preço de um produto usando **Selenium**.
- Compara o preço atual com o último registrado.
- Envia notificação para o **Telegram**:
  - 🔥 Quando o preço **cai**.
  - 🤦‍♂️ Quando o preço **sobe**.
- Salva o histórico de preços em `ultimo_preco.txt`.

---

## 🛠️ Requisitos

- **Python 3.8+**
- Google **Chrome** instalado.
- ChromeDriver compatível com sua versão do navegador.

### Bibliotecas Python
Instale as dependências com:

```bash
pip install -r requirements.txt
````
## ⚙️ Configuração
Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

````
TELEGRAM_TOKEN=seu_token_do_bot
CHAT_ID=seu_chat_id
PRODUCT_URL=https://www.exemplo.com/produto
````
TELEGRAM_TOKEN: token do seu bot do Telegram (criado com o @BotFather
).

CHAT_ID: ID do chat ou grupo onde as notificações serão enviadas.

PRODUCT_URL: URL do produto a ser monitorado.
## ▶️ Como executar

````
python telegram-bot.py
````
O script:

Faz scraping do preço.

Compara com o último valor salvo.

Envia alerta para o Telegram se houver alteração.

Registra o preço em ultimo_preco.txt

## 📂 Estrutura do Projeto
````
📂 projeto-preco
 ┣ 📜 .env         # Script principal
 ┣ 📜  README.md   # Configurações sensíveis
 ┣ 📜  requirements.txt   # Dependências necessárias
 ┗ 📜  telegram-bot.py    # Script principal
 ┣ 📜 ultimo_preco.txt   # Histórico de preços  
````
## 📝 Exemplo de saída no console
````
Último preço: 249.90 Preço atual: 239.90
🔥 O preço caiu! Agora está R$ 239,90 https://www.amazon.com.br/produto
````

## ⚠️ Observações
+ O seletor CSS do preço pode variar dependendo do site.
Atualmente, o script está configurado para páginas da Amazon Brasil:

````
span.a-size-base.a-color-price.a-color-price
````
+ Se usar outro site, ajuste o seletor em scrape_price()
+ Evite rodar o script com frequência muito alta para não ser bloqueado pelo site.