import os
from decimal import Decimal
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from datetime import datetime

# ---------- Caminhos absolutos ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRECO_FILE = os.path.join(BASE_DIR, "ultimo_preco.txt")
ENV_FILE = os.path.join(BASE_DIR, ".env")

# ---------- Carregar variáveis de ambiente ----------
load_dotenv(ENV_FILE)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PRODUCT_URL = os.getenv("PRODUCT_URL")

# ---------- Funções ----------

def enviar_telegram(msg):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram token ou chat ID não configurados")
        return
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
        if r.status_code != 200:
            print("Erro ao enviar mensagem:", r.status_code, r.text)
    except Exception as e:
        print("Exceção ao enviar Telegram:", e)

def salvar_preco(preco):
    with open(PRECO_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {preco:.2f}\n")

def buscar_ultimo_preco():
    if not os.path.exists(PRECO_FILE):
        return None
    try:
        with open(PRECO_FILE, "r", encoding="utf-8") as f:
            ultimo = f.readlines()[-1].strip()
        preco_str = ultimo.split("-")[-1].strip().replace(",", ".")
        return Decimal(preco_str).quantize(Decimal("0.01"))
    except Exception as e:
        print("Erro ao ler último preço:", e)
        return None

def scrape_price(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    try:
        # Parte inteira
        price_whole = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole"))
        ).text

        # Parte decimal (centavos)
        price_fraction = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-price-fraction"))
        ).text

        # Limpeza
        price_whole = price_whole.replace(".", "").replace("\xa0", "").strip()
        price_fraction = price_fraction.strip()

        price_text = f"{price_whole}.{price_fraction}"
        print("Preço bruto (whole+fraction):", repr(price_text))  # debug

        return Decimal(price_text).quantize(Decimal("0.01"))

    except Exception as e:
        print("Erro ao buscar preço:", e)
        return None
    finally:
        driver.quit()

# ---------- Função principal ----------

def get_price():
    if not PRODUCT_URL:
        print("URL do produto não configurada")
        return

    preco_atual = scrape_price(PRODUCT_URL)
    if preco_atual is None:
        print("Não foi possível obter o preço")
        return

    ultimo_preco = buscar_ultimo_preco()
    print("Último preço:", ultimo_preco, "Preço atual:", preco_atual)

    if ultimo_preco is not None:
        preco_str = str(preco_atual).replace(".", ",")
        if preco_atual < ultimo_preco:
            enviar_telegram(f"🔥 O preço caiu! Agora está R$ {preco_str} {PRODUCT_URL}")
        elif preco_atual > ultimo_preco:
            enviar_telegram(f"🤦‍♂️ O preço subiu! Agora está R$ {preco_str} {PRODUCT_URL}")

    salvar_preco(preco_atual)

# ---------- Execução ----------

if __name__ == "__main__":
    get_price()
