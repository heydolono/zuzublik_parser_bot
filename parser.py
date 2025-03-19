import requests
import logging
import time
from lxml import html
from dotenv import load_dotenv
from crud import (get_sites, save_price, get_average_prices,
                  update_average_price)
from utils import clean_price
from database import SessionLocal

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

def get_prices(url, xpath):
    logging.info(f"Парсим сайт: {url} с XPath: {xpath}")
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        logging.info(f"Получен ответ от {url}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка запроса к {url}: {e}")
        return None
    tree = html.fromstring(response.content)
    price_elements = tree.xpath(xpath)
    if price_elements:
        prices = []
        for price_element in price_elements:
            price_text = price_element.text_content().strip() if hasattr(price_element, 'text_content') else price_element
            cleaned_price = clean_price(price_text)
            if cleaned_price:
                logging.info(f"Найдена цена: {cleaned_price}")
                prices.append(cleaned_price)
            else:
                logging.warning(f"Не удалось очистить цену: {price_text}")
        return prices if prices else None
    else:
        logging.warning(f"Не удалось найти цены по XPath: {xpath}")
        return None

def run_parsing():
    logging.info("Запуск парсера...")
    session = SessionLocal()
    try:
        sites = get_sites()
        if not sites:
            logging.warning("В базе данных нет сайтов для парсинга")
            return
        for site_id, url, xpath in sites:
            prices = get_prices(url, xpath)
            if prices:
                for price in prices:
                    save_price(site_id, price)
                    logging.info(f"Сохранена цена {price} для {url}")
                update_average_price(session, site_id)
            else:
                logging.warning(f"Цены для {url} не получены.")
            time.sleep(1)
        average_prices = get_average_prices()
        for site, avg_price in average_prices:
            logging.info(f"Средняя цена для {site}: {avg_price}")
    finally:
        session.close()

if __name__ == "__main__":
    run_parsing()
