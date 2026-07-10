from django.urls import path
from . import views_dashboard as views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_estudiante, name='index'),
    path('estadisticas/', views.dashboard_estadisticas, name='estadisticas'),
    path('cursos/', views.dashboard_cursos, name='cursos'),
    path('logros/', views.dashboard_logros, name='logros'),
]
