from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 MorphoPlay</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    </head>
    <body>
        <nav class="navbar navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/"><i class="fas fa-puzzle-piece"></i> MorphoPlay</a>
                <div>
                    <a href="/admin/" class="btn btn-sm btn-outline-light">Admin</a>
                </div>
            </div>
        </nav>
        <div class="container text-center py-5">
            <h1 class="display-3">🚀 MorphoPlay</h1>
            <p class="lead">Aprende lingüística jugando</p>
            <div class="row mt-4">
                <div class="col-md-4">
                    <div class="card bg-dark text-light">
                        <div class="card-body">
                            <h3>📚 Cursos</h3>
                            <p>Aprende con lecciones estructuradas</p>
                            <a href="/admin/" class="btn btn-primary">Ver Cursos</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card bg-dark text-light">
                        <div class="card-body">
                            <h3>🎮 Juegos</h3>
                            <p>Practica con juegos interactivos</p>
                            <a href="/admin/" class="btn btn-success">Jugar</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card bg-dark text-light">
                        <div class="card-body">
                            <h3>🏆 Certificados</h3>
                            <p>Obtén reconocimiento oficial</p>
                            <a href="/admin/" class="btn btn-warning">Ver Logros</a>
                        </div>
                    </div>
                </div>
            </div>
            <footer class="mt-5 text-muted">
                <p>Django 4.2 · SQLite · MorphoPlay v1.0</p>
            </footer>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Agregar import y URL para juegos
from django.urls import include

urlpatterns += [
    path('juegos/', include('core.urls_juegos')),
]
# URLs de Progreso
from django.urls import include

urlpatterns += [
    path('progreso/', include('core.urls_progreso')),
]
# URLs del Dashboard
from django.urls import include

urlpatterns += [
    path('dashboard/', include('core.urls_dashboard')),
]
