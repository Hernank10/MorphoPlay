from django.urls import path
from . import views_juegos as views

app_name = 'juegos'

urlpatterns = [
    path('', views.juegos_list, name='list'),
    path('<int:juego_id>/', views.juego_detail, name='detail'),
    path('api/verificar/', views.verificar_respuesta, name='verificar'),
]
