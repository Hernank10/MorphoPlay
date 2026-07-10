from django.urls import path
from . import views_juegos as views

app_name = 'juegos'

urlpatterns = [
    path('', views.juegos_list, name='list'),
    path('<int:juego_id>/', views.juego_detail, name='detail'),
    path('api/verificar/', views.verificar_respuesta, name='verificar'),
]

# URLs para ejercicios periodísticos
urlpatterns += [
    path('periodisticos/', views.ejercicios_periodisticos, name='periodisticos'),
    path('periodisticos/<int:ejercicio_id>/', views.ejercicio_periodistico_detail, name='periodistico_detail'),
    path('api/verificar_ejercicio/', views.verificar_ejercicio, name='verificar_ejercicio'),
]
