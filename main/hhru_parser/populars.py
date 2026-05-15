from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import json
import re
from collections import Counter

class PopularVacanciesAnalyzer:
    def __init__(self):

        self.titles = []
        self.file = ''
        self.data_vac = []
        self.file_save: bool = False
        self.out_put: str = 'meta_data/popular_vacancies_grouped.json'


    def preprocess_title(self, title):
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
    def find_optimal_clusters(self, X, max_clusters=15):
        """Находит оптимальное количество кластеров методом локтя"""
        from sklearn.metrics import silhouette_score
        
        best_n = 2
        best_score = -1
        
        for n in range(2, min(max_clusters, X.shape[0] - 1)):
            kmeans = KMeans(n_clusters=n, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X)
            
            if len(set(labels)) > 1:
                score = silhouette_score(X, labels)
                if score > best_score:
                    best_score = score
                    best_n = n
        
        return best_n
    
    def cluster_job_titles(self, titles_list, n_clusters=None):
        """Кластеризует заголовки с помощью KMeans"""
        
        # Предобрабатываем заголовки для векторизации
        processed = [self.preprocess_title(t) for t in titles_list]
        
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
            #n_clusters = min(100, max(2, len(titles_list) // 3))
            n_clusters = self.find_optimal_clusters(X, max_clusters=15)
        
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
            
            vac_id = next((item['vacancyId'] for item in self.titles if item['title'] == title), None)
            
            clusters[label]['ids'].append(vac_id)
            clusters[label]['original_titles'].append(title)
            clusters[label]['count'] += 1

        return clusters

    def get_popularity_level(self, count, total):
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
        
    def analyze(self):
        if self.file != '' and self.file is not None:
            with open(self.file, 'r') as f:
                for i in json.load(f):
                    self.titles.append({'title': i['title'], 'vacancyId': i['vacancyId']})
        elif self.data_vac:
            self.titles = self.data_vac
        else:
            raise ValueError("Нет данных для анализа. Укажите файл или передайте данные напрямую.")
        # Получаем список заголовков
        job_titles = [item['title'] for item in self.titles]

        # Кластеризуем
        clustered_vacancies = self.cluster_job_titles(job_titles)
        # Формируем результаты
        total = len(self.titles)
        results = []

        for i, (cluster_id, data) in enumerate(clustered_vacancies.items()):
            count = data['count']
            percentage = (count / total) * 100
            
            # Нормализованное название кластера (его представитель)
            normalized_title = data['representative']
            
            # Разбиваем на слова для анализа
            words_in_title = normalized_title.split()
            
            results.append({
                'id': i,
                'cluster_id': int(cluster_id),
                'normalized_title': normalized_title,
                'words': words_in_title,
                'original_titles': list(set(data['original_titles'])),
                'vacancy_ids': data['ids'],
                'count': count,
                'percentage': round(percentage, 1),
                'popularity': self.get_popularity_level(count, total)
            })

        # Сортируем по популярности
        results.sort(key=lambda x: x['count'], reverse=True)

        # Сохраняем в JSON
        if self.file_save:
            with open(f"{self.out_put}", 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        return results



