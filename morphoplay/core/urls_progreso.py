from django.urls import path
from . import views_progreso as views

app_name = 'progreso'

urlpatterns = [
    path('partidas/', views.mis_partidas, name='partidas'),
    path('progreso/', views.mi_progreso, name='progreso'),
    path('partidas/crear/', views.crear_partida_manual, name='crear_partida'),
    path('partidas/<int:partida_id>/', views.ver_partida, name='ver_partida'),
    path('estadisticas/', views.estadisticas_completas, name='estadisticas'),
]
