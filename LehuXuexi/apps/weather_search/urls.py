from django.urls import path
from . import views

app_name = 'weather_search'

urlpatterns = [
    path('get_select/<str:city>', views.get_select, name='weather_select'),
    path('get_picture/<str:city>/<str:num>', views.get_picture, name='weather_picture'),
    path('search_weather/<str:city_name>', views.search_weather, name='search_weather')
]