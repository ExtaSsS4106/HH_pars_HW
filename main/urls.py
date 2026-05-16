from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('admin_panel', views.admin, name='adminPanel'),
    path('api/data/', views.get_data, name='get_data'),
    path('api/filtered-data/', views.get_filtered_data, name='api_filtered_data'),
    
    path('api/start-parsing/', views.start_parsing, name='start_parsing'),
    path('api/stop-parsing/', views.stop_parsing, name='stop_parsing'),
    path('api/parsing-status/', views.parsing_status, name='parsing_status'),
    path('api/parse-single/', views.parse_single_vacancy, name='parse_single'),
]
