from django.contrib import admin
from .models import Categoria, Nivel, Curso, Leccion, Juego, Partida, Progreso, EstadisticasUsuario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'orden', 'activo']
    search_fields = ['nombre']

@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'orden', 'color']

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'nivel', 'activo']
    search_fields = ['titulo']

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'orden', 'activo']
    search_fields = ['titulo']

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'nivel', 'tipo', 'puntos', 'activo']
    list_filter = ['categoria', 'nivel', 'tipo', 'activo']
    search_fields = ['titulo']

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'juego', 'correcto', 'fecha']

@admin.register(Progreso)
class ProgresoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'juego', 'completado', 'intentos']

@admin.register(EstadisticasUsuario)
class EstadisticasUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'juegos_completados', 'puntuacion_total']
