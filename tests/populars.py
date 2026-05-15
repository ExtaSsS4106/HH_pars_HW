from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import json
import re
from collections import Counter

# Загружаем вакансии
titles = []

with open('meta_data/vacancies.json', 'r') as f:
    for i in json.load(f):
        titles.append({'title': i['title'], 'vacancyId': i['vacancyId']})

def preprocess_title(title):
    """Предобработка заголовка"""
    title = title.lower()
    # Удаляем уровни
    levels = r'\b(senior|junior|middle|lead|team\s+lead|стажер|intern|trainee|сеньор|джуниор|мидл|тимлид)\b'
    title = re.sub(levels, '', title)
    # Удаляем слова-роли
    roles = r'\b(разработчик|developer|engineer|программист|специалист|инженер|архитектор)\b'
    title = re.sub(roles, '', title)
    # Удаляем скобки и их содержимое
    title = re.sub(r'\([^)]*\)', '', title)
    # Убираем лишние пробелы
    title = ' '.join(title.split())
    return title

def cluster_job_titles(titles_list, n_clusters=None):
    """Кластеризует заголовки с помощью KMeans"""
    
    # Предобрабатываем заголовки для векторизации
    processed = [preprocess_title(t) for t in titles_list]
    
    # Векторизуем
    vectorizer = TfidfVectorizer(
        lowercase=True,
        token_pattern=r'(?u)\b\w[\w-]+\b',
        max_features=1000000,
        min_df=1
    )
    
    X = vectorizer.fit_transform(processed)
    
    # Определяем количество кластеров
    if n_clusters is None:
        n_clusters = min(8, max(2, len(titles_list) // 3))
    
    # Кластеризация
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    
    # Группируем
    clusters = {}
    for idx, (title, label) in enumerate(zip(titles_list, labels)):
        if label not in clusters:
            clusters[label] = {
                'ids': [],
                'original_titles': [],
                'count': 0,
                'representative': title
            }
        
        vac_id = next((item['vacancyId'] for item in titles if item['title'] == title), None)
        
        clusters[label]['ids'].append(vac_id)
        clusters[label]['original_titles'].append(title)
        clusters[label]['count'] += 1
    
    return clusters

def get_popularity_level(count, total):
    """Определяет уровень популярности"""
    percentage = (count / total) * 100
    if percentage >= 20:
        return "high"
    elif percentage >= 10:
        return "medium"
    elif percentage >= 5:
        return "low"
    else:
        return "rare"

# Получаем список заголовков
job_titles = [item['title'] for item in titles]

# Кластеризуем
clustered_vacancies = cluster_job_titles(job_titles)

# Формируем результаты
total = len(titles)
results = []

for cluster_id, data in clustered_vacancies.items():
    count = data['count']
    percentage = (count / total) * 100
    
    # Нормализованное название кластера (его представитель)
    normalized_title = data['representative']
    
    # Разбиваем на слова для анализа
    words_in_title = normalized_title.split()
    
    results.append({
        'cluster_id': int(cluster_id),
        'normalized_title': normalized_title,
        'words': words_in_title,
        'original_titles': list(set(data['original_titles'])),
        'vacancy_ids': data['ids'],
        'count': count,
        'percentage': round(percentage, 1),
        'popularity': get_popularity_level(count, total)
    })

# Сортируем по популярности
results.sort(key=lambda x: x['count'], reverse=True)

# Сохраняем в JSON
with open('meta_data/popular_vacancies_grouped.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Сохраняем категории ID
def get_vacancy_ids_by_popularity(results, level='high'):
    ids = []
    for group in results:
        if group['popularity'] == level:
            ids.extend(group['vacancy_ids'])
    return ids



print("=" * 60)
print("📊 АНАЛИЗ ПОПУЛЯРНОСТИ ВАКАНСИЙ")
print("=" * 60)
print(f"Всего вакансий: {total}")
print(f"Найдено кластеров: {len(results)}\n")

for i, vac in enumerate(results[:10], 1):
    print(f"{i}. {vac['normalized_title']}")
    print(f"   Встречается: {vac['count']} раз ({vac['percentage']}%)")
    print(f"   Уровень: {vac['popularity']}")
    print(f"   Примеры: {', '.join(vac['original_titles'][:3])}")
    print()

print("=" * 60)
print("📊 ЧАСТОТА ОТДЕЛЬНЫХ СЛОВ:")
print("=" * 60)


print("\n✅ Результаты сохранены в 'meta_data/'")