import re

def clean_price(price_text):
    if isinstance(price_text, str):
        price_text = re.sub(r"[^\d,\.]", "", price_text)
        if price_text and any(char.isdigit() for char in price_text):
            try:
                return float(price_text.replace(",", "."))
            except ValueError:
                pass
    return None
