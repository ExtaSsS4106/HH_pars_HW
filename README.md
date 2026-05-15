# hh.ru Парсер

## Описание

Парсер для сбора и анализа данных о вакансиях с сайта hh.ru. Инструмент позволяет автоматизировать процесс сбора информации о вакансиях, зарплатах, требованиях к кандидатам и других параметрах.

## Возможности

- 📋 Сбор данных о вакансиях с hh.ru
- 💰 Извлечение информации о зарплате и условиях
- 🔍 Поиск по ключевым словам и фильтрам
- 📊 Экспорт данных в различные форматы (CSV, JSON)
- ⚙️ Настраиваемые параметры парсинга
- 🔄 Асинхронная обработка данных

## Требования

- Python 3.8+
- pip (менеджер пакетов Python)
- Доступ в интернет

## Установка

### 1. Клонировать репозиторий

```bash
git clone <repository-url>
cd HH_pars_HW
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

## Использование

### Базовый пример

```python
from parser import HHParser

# Инициализация парсера
parser = HHParser()

# Поиск вакансий
vacancies = parser.search(
    query="Python",
    area=1,  # Москва
    per_page=100
)

# Сохранение результатов
parser.save_to_csv(vacancies, 'vacancies.csv')
```

### Поиск с фильтрами

```python
# Поиск с дополнительными параметрами
vacancies = parser.search(
    query="Data Scientist",
    salary_from=100000,
    salary_to=300000,
    experience="between1And3",
    schedule="fullTime"
)
```

## Структура проекта

```
HH_pars_HW/
├── README.md              # Этот файл
├── requirements.txt       # Зависимости проекта
├── parser/
│   ├── __init__.py
│   ├── main.py            # Основной модуль парсера
│   └── utils.py           # Вспомогательные функции
├── data/                  # Папка для сохранения результатов
└── examples/              # Примеры использования
```

## Примеры команд

### Парсинг вакансий по специальности

```bash
python main.py --query "Python Developer" --area 1 --output vacancies.json
```

### Экспорт в CSV

```bash
python main.py --query "Java" --format csv --output java_jobs.csv
```

## Примечания

- ⚠️ Уважайте правила robots.txt сайта hh.ru
- 🛑 Используйте задержки между запросами
- 📌 Следите за условиями использования сервиса hh.ru

## Лицензия

MIT License

## Контакты и поддержка

Если у вас возникли вопросы или предложения, создайте Issue в репозитории. 