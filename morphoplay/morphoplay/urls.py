from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('accounts/', include('core.urls_accounts')),
    path('dashboard/', include('core.urls_dashboard')),
    path('juegos/', include('core.urls_juegos')),
    path('cursos/', include('core.urls_cursos')),
    path('progreso/', include('core.urls_progreso')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
