import random

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
import time
import os

class VacancyScraper:
    def __init__(self):
        self.file_save: bool = False
        self.current_dir: str = os.getcwd()
        self.target: str = f"{self.current_dir}/meta_data"
        self.uri: str = "https://hh.ru/search/vacancy"
        self.text: str = ''
        self.page_end: int = 0
        self.delay: int = random.randint(40, 120)
        
    def get_vacancies_with_playwright(self, page_count):
        with sync_playwright() as p:
            # headless=True - браузер не показывается
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Собираем все перехваченные данные
            api_data: list = []
            
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
            page.goto(f"{self.uri}?page={page_count}{'&text=' + self.text if self.text else ''}")
            
            # Ждём загрузки контента
            page.wait_for_selector("[data-qa='vacancy-serp__vacancy']", timeout=10000)
            page.wait_for_load_state("networkidle", timeout=10000)
            time.sleep(3) 
            # Получаем все карточки вакансий
            vacancies = page.query_selector_all("[data-qa='vacancy-serp__vacancy']")
            


            try:
                html_content = page.content() 
                with open(f"{self.target}/page.html", "w", encoding="utf-8") as f:
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
                            with open(f"{self.target}/initial_state.json", "w", encoding="utf-8") as f:
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
                
            result = []
            try:
                for item in data.get('vacancySearchResult', {}).get('vacancies', []):
                    vacancy_data = {
                        "vacancyId": item.get('vacancyId', 'Не указано'),
                        "title": item.get('name', 'Не указано'),
                        "company": item.get('company', {}).get('name', 'Не указано'),
                        "salary": {item.get('compensation', {}).get('from', 'Не указана') if item.get('compensation') else None},
                        "city": item.get('area', {}).get('name', 'Не указано'),
                        "url": item.get('links', {}).get('desktop', 'Не указано'),
                        "work_schedule": item.get('@workSchedule', 'Не указано'),
                        "publicationTime": item.get('publicationTime', {}).get('@timestamp'),
                        "totalResponsesCount": item.get('totalResponsesCount', 0)
                    }
                    result.append(vacancy_data)
                print(f"✅ Собрано {len(result)} вакансий из JSON")
            except Exception as e:
                """for vac in vacancies:  # Все вакансии
                
                
                    title = vac.query_selector("[data-qa='serp-item__title']")
                    company = vac.query_selector("[data-qa='vacancy-serp__vacancy-employer']")
                    salary = "Не указана"
                    city = vac.query_selector("[data-qa='vacancy-serp__vacancy-address']")
                    work_schedule = vac.query_selector("[data-qa='work-schedule-by-days-text']")
                    vacancyId = title.get_attribute("href").split('/')[-1].split('?')[0] if title else "Не указано"
                
                    vacancy_data = {
                        "vacancyId": vacancyId,
                        "title": title.inner_text() if title else "Не указано",
                        "company": company.inner_text() if company else "Не указано",
                        "salary": salary.inner_text() if salary else "Не указана",
                        "city": city.inner_text() if city else "Не указано",
                        "url": title.get_attribute("href") if title else None,
                        "work_schedule": work_schedule.inner_text() if work_schedule else "Не указано",
                        "publicationTime": None,
                        "totalResponsesCount": 0
                    }
                    result.append(vacancy_data)"""
                print(f"❌ Ошибка при извлечении данных из JSON: {e}")
            # Сохраняем результат
            
            
            print(f"✅ Собрано {len(result)} вакансий")
            browser.close()
            return result

    # Установка: pip install playwright && playwright install chromium
    def scrape_vacancies(self):
        data: list = []
        for page in range(0, self.page_end):
            print(self.text)
            print(f"Обрабатываем страницу {page}...")
            
            max_attempts = 3
            success = False
            
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"  Попытка {attempt} из {max_attempts}...")
                    res = self.get_vacancies_with_playwright(page)
                    
                    if res is None:
                        print(f"Результат None на попытке {attempt}")
                        if attempt == max_attempts:
                            print(f"Пропускаем страницу {page} после {max_attempts} неудачных попыток")
                            success = False
                        continue
                    
                    print(f"Собрано {len(res)} вакансий на странице {page} (попытка {attempt})")
                    
                    for item in res:
                        print(f"Добавляем вакансию: {item['title']} (ID: {item['vacancyId']})")
                        if item not in data:
                            data.append(item)
                            print(f"Вакансия добавлена. Текущий общий счётчик: {len(data)}")
                        else:
                            print(f"Вакансия уже существует в списке. Пропускаем.")
                    
                    success = True
                    break  # Выходим из цикла попыток при успехе
                    
                except Exception as e:
                    print(f"Ошибка на попытке {attempt}: {type(e).__name__}: {str(e)}")
                    
                    if attempt == max_attempts:
                        print(f"Пропускаем страницу {page} после {max_attempts} неудачных попыток")
                        success = False
                    else:
                        wait_time = 5 * attempt  # Увеличиваем задержку с каждой попыткой
                        print(f"Повторная попытка через {wait_time} секунд...")
                        time.sleep(wait_time)
            
            if not success:
                print(f"Страница {page} не обработана, переходим к следующей")
            
            # Задержка между страницами только если страница была обработана
            if success:
                print(f"Задержка перед следующей страницей: {self.delay} секунд")
                time.sleep(self.delay)
            
            print(f"Страница {page} обработана. Всего вакансий: {len(data)}")
        
        print(f"Итого собрано вакансий: {len(data)}")
        
        if self.file_save:
            with open(f"{self.target}/vacancies.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Данные сохранены в {self.target}/vacancies.json")
        
        return data