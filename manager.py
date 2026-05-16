import os
import sys
import django
import random
import threading
import time
from datetime import datetime

# Указываем путь к настройкам Django
sys.path.append('/home/exti/Desktop/HDD/some-shit/code/gitReposses/HH_pars_HW')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

# Инициализируем Django
django.setup()

from main.models import Vacancies, Groups, Specialisation
from main.hhru_parser import hh_pars

class Manager():
    def __init__(self):
        self.is_running = False
        self.current_thread = None
        self.stop_requested = False
        self.parsing_info = {
            'status': 'stopped',
            'current_page': 0,
            'current_group': '',
            'parsed_count': 0,
            'start_time': None,
            'end_time': None
        }
    
    def start_parsing(self, time_out_one_circle: int = 500,
                      time_out: int = 150,
                      pages: int = 0,
                      delay_from: int = 40, 
                      delay_to: int = 120):
        """Запуск парсинга в отдельном потоке"""
        if self.is_running:
            print("❌ Парсинг уже запущен!")
            return False
        
        self.is_running = True
        self.stop_requested = False
        self.parsing_info['status'] = 'running'
        self.parsing_info['start_time'] = datetime.now()
        self.parsing_info['parsed_count'] = 0
        
        # Запускаем в отдельном потоке
        self.current_thread = threading.Thread(
            target=self._parsing_worker,
            args=(time_out_one_circle, time_out, pages, delay_from, delay_to)
        )
        self.current_thread.start()
        print("✅ Парсинг запущен!")
        return True
    
    def stop_parsing(self):
        """Остановка парсинга"""
        if not self.is_running:
            print("❌ Парсинг не запущен!")
            return False
        
        self.stop_requested = True
        self.parsing_info['status'] = 'stopping'
        print("⏹️ Останавливаем парсинг...")
        return True
    
    def _parsing_worker(self, time_out_one_circle, time_out, pages, delay_from, delay_to):
        """Рабочий поток парсинга"""
        try:
            gr = Groups.objects.all()
            parset_data = []
            
            if isinstance(pages, int):
                pages_range = range(pages + 1) 
            else:
                pages_range = pages
            
            for page in pages_range:
                if self.stop_requested:
                    break
                    
                self.parsing_info['current_page'] = page
                print(f"📄 Обработка страницы {page}")
                
                for i in gr:
                    if self.stop_requested:
                        break
                    
                    self.parsing_info['current_group'] = i.title
                    print(f"🔄 Обработка группы: {i.title}")
                    
                    try:

                        # Используем существующий класс VacancyScraper
                        scraper = hh_pars.VacancyScraper()
                        scraper.text = f"{i.spec_id.title} {i.title}"
                        scraper.delay = random.randint(delay_from, delay_to)
                        scraper.page_end = page
                        
                        # Вызываем метод scrape_vacancies()
                        data = scraper.scrape_vacancies()
                        print(page, data)
                        time.sleep(5)
                        
                        for d in data:
                            if self.stop_requested:
                                break
                                
                            if not Vacancies.objects.filter(vacancyId=d['vacancyId']).exists():
                                spec, _ = Specialisation.objects.get_or_create(title=i.spec_id.title)
                                group, _ = Groups.objects.get_or_create(title=i.title, spec_id=spec)
                                Vacancies.objects.create(
                                    title=d['title'],
                                    link=d['url'],
                                    city=d['city'],
                                    salary=str(d['salary']),
                                    work_schedule=d['work_schedule'],
                                    publicationTime=d['publicationTime'] if d['publicationTime'] else 0,
                                    company=d['company'],
                                    vacancyId=d['vacancyId'],
                                    group_id=group,
                                    spec_id=spec,
                                    status='active'
                                )
                                print(f"  ✅ Вакансия '{d['title']}' добавлена.")
                                self.parsing_info['parsed_count'] += 1
                                parset_data.append(d['vacancyId'])
                            else:
                                print(f"  ⚠️ Вакансия '{d['title']}' уже существует.")
                    except Exception as e:
                        print(f"  ❌ Ошибка при обработке группы '{i.title}': {e}")
                    
                    if not self.stop_requested:
                        time.sleep(time_out / 1000)  # переводим мс в секунды
                
                if not self.stop_requested and page < len(pages_range) - 1:
                    print(f"⏳ Пауза {time_out_one_circle} мс перед следующей страницей...")
                    time.sleep(time_out_one_circle / 1000)
            
            # Архивируем старые вакансии
            """if not self.stop_requested:
                old_vac = Vacancies.objects.exclude(vacancyId__in=parset_data)
                updated_count = old_vac.update(status='archived')
                print(f"📦 Архивировано {updated_count} вакансий")"""
            
            self.parsing_info['status'] = 'stopped'
            self.parsing_info['end_time'] = datetime.now()
            print("✅ Парсинг завершен!")
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            self.parsing_info['status'] = 'error'
        finally:
            self.is_running = False
            self.stop_requested = False
    
    def get_status(self):
        """Получить статус парсинга"""
        return self.parsing_info
    
    def parse_single_vacancy(self, vacancy_id):
        """Парсинг одной вакансии"""
        if self.is_running:
            print("❌ Парсинг уже запущен! Остановите текущий процесс.")
            return None
        
        try:
            # Используем существующий класс VacancyScraper для одной вакансии
            scraper = hh_pars.VacancyScraper()
            scraper.text = vacancy_id  # ID вакансии
            vacancy_data = scraper.get_vacancia()  # Используем метод get_vacancia()
            
            if vacancy_data:
                print(f"✅ Данные вакансии: {vacancy_data.get('name', 'Не найдено')}")
                return vacancy_data
            else:
                print("❌ Вакансия не найдена")
                return None
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return None

    def parse_single_vacancy(self, vacancy_id):
        """Парсинг одной вакансии по ID"""
        if self.is_running:
            print("❌ Парсинг уже запущен! Остановите текущий процесс.")
            return None
        
        try:
            # Используем существующий класс VacancyScraper
            scraper = hh_pars.VacancyScraper()
            scraper.text = vacancy_id  # ID вакансии (число)
            
            # Вызываем метод get_vacancia() для получения одной вакансии
            # ВНИМАНИЕ: в вашем классе опечатка - get_vacancia() вместо get_vacancy()
            vacancy_data = scraper.get_vacancia()
            
            if vacancy_data:
                print(f"✅ Данные вакансии найдены:")
                print(f"  Название: {vacancy_data.get('name', 'Не указано')}")
                print(f"  Компания: {vacancy_data.get('company', {}).get('name', 'Не указана')}")
                print(f"  Зарплата: {vacancy_data.get('compensation', {}).get('from', 'Не указана')}")
                
                # Сохраняем в БД если нужно
                # Здесь можно добавить сохранение в базу данных
                
                return vacancy_data
            else:
                print("❌ Вакансия не найдена")
                return None
                
        except TypeError as e:
            print(f"❌ Ошибка типа: {e}")
            print("   Убедитесь, что vacancy_id - это число (int)")
            return None
        except Exception as e:
            print(f"❌ Ошибка при парсинге вакансии: {e}")
            return None
