from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('api/data/', views.get_data, name='get_data'),
    path('api/filtered-data/', views.get_filtered_data, name='api_filtered_data'),
]
