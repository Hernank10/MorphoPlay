from django.urls import path
from . import views as views_cursos

app_name = 'cursos'

urlpatterns = [
    path('', views_cursos.cursos_list, name='list'),
    path('<int:curso_id>/', views_cursos.curso_detail, name='detail'),
    path('<int:curso_id>/leccion/<int:leccion_id>/', views_cursos.leccion_detail, name='leccion'),
    path('<int:curso_id>/evaluacion/<int:evaluacion_id>/', views_cursos.evaluacion_detail, name='evaluacion'),
    path('<int:curso_id>/evaluacion/<int:evaluacion_id>/submit/', views_cursos.submit_evaluacion, name='submit_evaluacion'),
]
