from curl_cffi import requests
from bs4 import BeautifulSoup
import os

url = "https://hh.ru/search/vacancy"

def test_parser():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(f"{url}?page=0", headers=headers)
    print(response.status_code)
    print(response.text[:500])  # Печатаем первые 500 символов ответа для проверки
    with open("tests/page.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
test_parser()