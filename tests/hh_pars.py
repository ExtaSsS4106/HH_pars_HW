from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
import time
def get_vacancies_with_playwright():
    with sync_playwright() as p:
        # headless=True - браузер не показывается
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Собираем все перехваченные данные
        api_data = []
        
        def capture_api(response):
            if "api.hh.ru/vacancies" in response.url:
                try:
                    data = response.json()
                    if 'items' in data:
                        api_data.extend(data['items'])
                        print(f"  Перехвачено {len(data['items'])} вакансий")
                except:
                    pass
        page.on("response", capture_api)
        
        # Устанавливаем заголовки
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        # Переходим на страницу
        page.goto("https://hh.ru/search/vacancy?text=python&area=1&page=0")
        
        # Ждём загрузки контента
        page.wait_for_selector("[data-qa='vacancy-serp__vacancy']", timeout=10000)
        page.wait_for_load_state("networkidle", timeout=10000)
        time.sleep(3) 
        # Получаем все карточки вакансий
        vacancies = page.query_selector_all("[data-qa='vacancy-serp__vacancy']")
        
        result = []
        for vac in vacancies:  # Все вакансии
            title = vac.query_selector("[data-qa='serp-item__title']")
            company = vac.query_selector("[data-qa='vacancy-serp__vacancy-employer']")
            salary = vac.query_selector("[data-qa='vacancy-serp__vacancy-compensation']")
            
            vacancy_data = {
                "title": title.inner_text() if title else "Не указано",
                "company": company.inner_text() if company else "Не указано",
                "salary": salary.inner_text() if salary else "Не указана",
                "url": title.get_attribute("href") if title else None
            }
            result.append(vacancy_data)
        try:
            html_content = page.content() 
            with open("tests/page.html", "w", encoding="utf-8") as f:
                f.write(html_content)  # Сохраняем HTML для отладки
            soup = BeautifulSoup(html_content, 'html.parser')
            template_tag = soup.find('template', id='HH-Lux-InitialState')
            
            if template_tag:
                # Извлекаем JSON из атрибута template_tag.string
                json_str = template_tag.string
                if json_str:
                    try:
                        data = json.loads(json_str)
                        print(f"✅ JSON успешно извлечён!")
                        print(f"📊 Ключи в JSON: {list(data.keys())}")
                        with open("tests/initial_state.json", "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                    except json.JSONDecodeError as e:
                        print(f"❌ Ошибка парсинга JSON: {e}")
                        return None
                else:
                    print("❌ Атрибут data-state не найден в теге <template>")
            else:
                print("❌ Не найден тег <template id='HH-Lux-InitialState'>")
        except Exception as e:
            print(f"Ошибка при сохранении HTML: {e}")
        # Сохраняем результат
        with open("tests/vacancies.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Собрано {len(result)} вакансий")
        browser.close()
        return result

# Установка: pip install playwright && playwright install chromium
get_vacancies_with_playwright()