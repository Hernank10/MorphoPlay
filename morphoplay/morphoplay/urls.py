from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/edit/', views.edit_profile, name='edit_profile'),
    path('accounts/password/change/', views.change_password, name='change_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cursos/', views.cursos_list, name='cursos_list'),
    path('cursos/<int:curso_id>/', views.curso_detail, name='curso_detail'),
    path('cursos/<int:curso_id>/leccion/<int:leccion_id>/', views.leccion_detail, name='leccion'),
    path('cursos/<int:curso_id>/evaluacion/<int:evaluacion_id>/', views.evaluacion_detail, name='evaluacion'),
    path('cursos/<int:curso_id>/evaluacion/<int:evaluacion_id>/submit/', views.submit_evaluacion, name='submit_evaluacion'),
    path('juegos/', views.juegos_list, name='juegos_list'),
    path('juegos/<int:juego_id>/', views.juego_detail, name='juego_detail'),
    path('juegos/api/verificar/', views.verificar_respuesta, name='verificar_respuesta'),
]
