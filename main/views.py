import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Specialisation, Groups, Vacancies
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from manager import Manager
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

manager = Manager()

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def admin(request):
    return render(request, 'admin/admin.html')

@login_required(login_url='/login')
@csrf_exempt
@require_http_methods(["POST"])
def start_parsing(request):
    try:
        data = json.loads(request.body)
        
        success = manager.start_parsing(
            time_out_one_circle=data.get('time_out_first_circle', 500),
            time_out=data.get('time_out', 150),
            pages=data.get('pages', 0),
            delay_from=data.get('delay_from', 40),
            delay_to=data.get('delay_to', 120)
        )
        print(data)
        return JsonResponse({
            'success': success,
            'status': manager.get_status()
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='/login')
@csrf_exempt
@require_http_methods(["POST"])
def stop_parsing(request):
    success = manager.stop_parsing()
    return JsonResponse({
        'success': success,
        'status': manager.get_status()
    })

@login_required(login_url='/login')
@require_http_methods(["GET"])
def parsing_status(request):
    return JsonResponse(manager.get_status())

@login_required(login_url='/login')
@csrf_exempt
@require_http_methods(["POST"])
def parse_single_vacancy(request):
    try:
        data = json.loads(request.body)
        vacancy_id = data.get('vacancy_id')
        
        if not vacancy_id:
            return JsonResponse({'success': False, 'error': 'vacancy_id required'})
        
        result = manager.parse_single_vacancy(vacancy_id)
        
        return JsonResponse({
            'success': result is not None,
            'data': result
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def home(request):
    spec = Specialisation.objects.all().distinct().order_by('title')
    cities = Vacancies.objects.filter(city__isnull=False).exclude(city='').values_list('city', flat=True).distinct().order_by('city')
    spec_list = []
    context = {
        'professions': spec_list,
        'cities': list(cities),
    }
    for s in spec:
        vac_exists = Vacancies.objects.filter(spec_id__title=s).exists()
        if vac_exists:
            spec_list.append(s.title)
    return render(request, 'main/home.html', context)

def get_data(request):
    """Получение всех данных"""
    data = []
    vac_ids = []
    
    for city in Vacancies.objects.values_list('city', flat=True).distinct():
        city_data = {'city': city, 'professions': []}
        
        for spec in Specialisation.objects.filter(groups__vacancies__city=city).distinct():
            prof_data = {'profession': spec.title, 'count': 0, 'groups': []}
            
            for group in Groups.objects.filter(spec_id=spec, vacancies__city=city).distinct():
                vacancies = Vacancies.objects.filter(group_id=group, city=city, status='active')
                count = vacancies.count()
                
                prof_data['count'] += count
                prof_data['groups'].append({
                    'groupe': group.title,
                    'count': count
                })
                for v in vacancies:
                    vac_ids.append(v.vacancyId)
            
            if prof_data['groups']:
                city_data['professions'].append(prof_data)
        
        if city_data['professions']:
            data.append(city_data)
    
    # Убираем дубликаты
    unique_ids = []
    seen = set()
    for vac_id in vac_ids:
        if vac_id not in seen:
            seen.add(vac_id)
            unique_ids.append(vac_id)
    
    # Пагинация
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    
    all_vacancies = Vacancies.objects.filter(vacancyId__in=unique_ids, status='active').order_by('-publicationTime')
    paginator = Paginator(all_vacancies, 10)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    vacancies_list = [{
        'id': v.vacancyId,
        'title': v.title,
        'groupe': v.group_id.title if v.group_id else 'Без группы',
        'company': v.company,
        'salary': str(v.salary).replace("{", "").replace("}", "").replace("'", ""),
        'location': v.city,
        'link': v.link,
        'publicationTime': datetime.datetime.fromtimestamp(v.publicationTime).strftime('%d.%m.%Y')
    } for v in page_obj]
    
    return JsonResponse({
        'data': data,
        'vacancies_list': vacancies_list,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'per_page': per_page,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous()
        }
    }, safe=False)


def get_filtered_data(request):
    """Получение отфильтрованных данных с пагинацией"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        params = json.loads(request.body)
        city = params.get('city')
        profession = params.get('profession')
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        
        # Фильтруем города
        if city and city != 'Все города':
            cities = [city]
        else:
            cities = Vacancies.objects.values_list('city', flat=True).distinct()
        
        data = []
        vac_ids = []
        
        for city_name in cities:
            if not city_name:
                continue
                
            city_data = {'city': city_name, 'professions': []}
            
            # Фильтруем профессии
            specs = Specialisation.objects.filter(groups__vacancies__city=city_name)
            if profession and profession != 'Все профессии':
                specs = specs.filter(title=profession)
            specs = specs.distinct()
            
            for spec in specs:
                prof_data = {'profession': spec.title, 'count': 0, 'groups': []}
                
                for group in Groups.objects.filter(spec_id=spec, vacancies__city=city_name).distinct():
                    vacancies = Vacancies.objects.filter(
                        group_id=group, 
                        city=city_name, 
                        status='active'
                    )
                    count = vacancies.count()
                    
                    prof_data['count'] += count
                    prof_data['groups'].append({
                        'groupe': group.title,
                        'count': count
                    })
                    
                    for v in vacancies:
                        vac_ids.append(v.vacancyId)
                
                if prof_data['groups']:
                    city_data['professions'].append(prof_data)
            
            if city_data['professions']:
                data.append(city_data)
        
        # Убираем дубликаты
        unique_ids = []
        seen = set()
        for vac_id in vac_ids:
            if vac_id not in seen:
                seen.add(vac_id)
                unique_ids.append(vac_id)
        
        # Пагинация
        all_vacancies = Vacancies.objects.filter(vacancyId__in=unique_ids, status='active').order_by('-publicationTime')
        paginator = Paginator(all_vacancies, per_page)
        
        try:
            page_obj = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.page(1)
        
        vacancies_list = [{
            'id': v.vacancyId,
            'title': v.title,
            'groupe': v.group_id.title if v.group_id else 'Без группы',
            'company': v.company,
            'salary': str(v.salary).replace("{", "").replace("}", "").replace("'", ""),
            'location': v.city,
            'link': v.link,
            'publicationTime': datetime.datetime.fromtimestamp(v.publicationTime).strftime('%d.%m.%Y')

        } for v in page_obj]
        
        return JsonResponse({
            'data': data,
            'vacancies_list': vacancies_list,
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'per_page': per_page,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous()
            }
        }, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)