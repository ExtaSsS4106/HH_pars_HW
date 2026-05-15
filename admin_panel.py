import os
import sys
import django
import random
# Указываем путь к настройкам Django
sys.path.append('/home/exti/Desktop/HDD/some-shit/code/gitReposses/HH_pars_HW')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

# Инициализируем Django
django.setup()

from main.hhru_parser import populars
import json
from main.models import Vacancies, Groups, Specialisation
from main.hhru_parser import hh_pars
import time

def start_parsing(time_out_one_circle: int = 500,
                  time_out: int = 150,
                  pages: int = 0,
                  delay_from: int = 40, 
                  delay_to: int = 120
                  ):
    gr = Groups.objects.all()
    parset_data = []
    
    if isinstance(pages, int):
        pages_range = range(pages + 1) 
    else:
        pages_range = pages
    
    for page in pages_range:
        for i in gr:
            try:
                scraper = hh_pars.VacancyScraper()
                scraper.text = f"{i.spec_id.title} {i.title}"
                scraper.delay = random.randint(delay_from, delay_to)
                scraper.page_end = page
                data = scraper.scrape_vacancies()
                
                for d in data:
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
                        print(f"Вакансия '{d['title']}' добавлена в базу данных.")
                        parset_data.append(d['vacancyId'])
                    else:
                        print(f"Вакансия '{d['title']}' уже существует в базе данных. Пропускаем.")
            except Exception as e:
                print(f"Ошибка при обработке группы '{i.title}': {e}")
            time.sleep(time_out)
        time.sleep(time_out_one_circle)
    
    # Архивируем старые вакансии
    old_vac = Vacancies.objects.exclude(vacancyId__in=parset_data)
    updated_count = old_vac.update(status='archived')
    print(f"Архивировано {updated_count} вакансий")
        
action = input("Начать парсинг вакансий или конкретной? (1 - массовый, 2 - по ID): ")
if action == '1':
    start_parsing()
elif action == '2':
    value = input("Введите ID вакансии: ")
    try:
        vacancy_id = int(value)
        scraper = hh_pars.VacancyScraper()
        scraper.text = vacancy_id  # ID вакансии для поиска
        vacancy_data = scraper.get_vacancia()
        
        if vacancy_data:
            print(f"Данные вакансии: {vacancy_data.get('name', 'Не найдено')}")
        else:
            print("Вакансия не найдена")
    except ValueError:
        print("Ошибка: ID должен быть числом")