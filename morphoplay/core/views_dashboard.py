from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from .models import (
    Curso, Leccion, Evaluacion, Juego, Partida, Progreso, 
    EstadisticasUsuario, ProgresoCurso, IntentoEvaluacion
)

@login_required
def dashboard_estudiante(request):
    """Dashboard principal para estudiantes"""
    usuario = request.user
    
    # Obtener o crear estadísticas del usuario
    stats, created = EstadisticasUsuario.objects.get_or_create(usuario=usuario)
    
    # Cursos inscritos del usuario
    cursos_inscritos = ProgresoCurso.objects.filter(
        usuario=usuario
    ).select_related('curso')
    
    # Cursos disponibles para inscribirse
    cursos_disponibles = Curso.objects.filter(
        activo=True
    ).exclude(
        id__in=cursos_inscritos.values_list('curso_id', flat=True)
    )[:4]
    
    # Últimas partidas
    ultimas_partidas = Partida.objects.filter(
        usuario=usuario
    ).select_related('juego').order_by('-fecha')[:10]
    
    # Progreso en juegos
    progreso_juegos = Progreso.objects.filter(
        usuario=usuario
    ).select_related('juego')[:10]
    
    # Evaluaciones completadas
    evaluaciones_completadas = IntentoEvaluacion.objects.filter(
        usuario=usuario,
        estado='completado'
    ).select_related('evaluacion', 'evaluacion__curso')[:5]
    
    # Estadísticas por categoría
    categorias_stats = []
    from .models import Categoria
    for cat in Categoria.objects.filter(activo=True)[:6]:
        juegos_cat = Juego.objects.filter(categoria=cat, activo=True)
        completados = Progreso.objects.filter(
            usuario=usuario,
            juego__in=juegos_cat,
            completado=True
        ).count()
        if juegos_cat.exists():
            categorias_stats.append({
                'nombre': cat.nombre,
                'icono': cat.icono or 'fa-tag',
                'total': juegos_cat.count(),
                'completados': completados,
                'porcentaje': round((completados / juegos_cat.count()) * 100, 1)
            })
    
    # Últimos logros (simulados)
    logros = [
        {'nombre': 'Primer juego completado', 'icono': '🎯', 'fecha': timezone.now() - timezone.timedelta(days=2)},
        {'nombre': 'Racha de 5 aciertos', 'icono': '🔥', 'fecha': timezone.now() - timezone.timedelta(days=1)},
        {'nombre': '10 juegos completados', 'icono': '⭐', 'fecha': timezone.now() - timezone.timedelta(hours=5)},
        {'nombre': 'Curso completado', 'icono': '🏆', 'fecha': timezone.now() - timezone.timedelta(hours=2)},
    ]
    
    # Actividad reciente (simulada)
    actividades = [
        {'tipo': 'juego', 'nombre': 'Prefijos de Negación', 'puntuacion': 10, 'fecha': timezone.now() - timezone.timedelta(minutes=5)},
        {'tipo': 'leccion', 'nombre': 'Introducción a la Morfología', 'fecha': timezone.now() - timezone.timedelta(minutes=30)},
        {'tipo': 'evaluacion', 'nombre': 'Evaluación de Morfología', 'puntuacion': 85, 'fecha': timezone.now() - timezone.timedelta(hours=1)},
        {'tipo': 'juego', 'nombre': 'Sufijos de Profesión', 'puntuacion': 15, 'fecha': timezone.now() - timezone.timedelta(hours=2)},
    ]
    
    context = {
        'estadisticas': stats,
        'cursos_inscritos': cursos_inscritos,
        'cursos_disponibles': cursos_disponibles,
        'ultimas_partidas': ultimas_partidas,
        'progreso_juegos': progreso_juegos,
        'evaluaciones_completadas': evaluaciones_completadas,
        'categorias_stats': categorias_stats,
        'logros': logros[:4],
        'actividades': actividades,
        'total_juegos': Juego.objects.filter(activo=True).count(),
        'total_cursos': Curso.objects.filter(activo=True).count(),
    }
    
    return render(request, 'dashboard/estudiante.html', context)

@login_required
def dashboard_estadisticas(request):
    """Vista de estadísticas detalladas"""
    usuario = request.user
    stats = get_object_or_404(EstadisticasUsuario, usuario=usuario)
    
    # Partidas por día (últimos 30 días)
    partidas_dias = []
    for i in range(30, -1, -1):
        fecha = timezone.now() - timezone.timedelta(days=i)
        count = Partida.objects.filter(
            usuario=usuario,
            fecha__date=fecha.date()
        ).count()
        partidas_dias.append({
            'fecha': fecha.strftime('%d/%m'),
            'total': count
        })
    
    # Partidas por categoría
    partidas_categoria = []
    from .models import Categoria
    for cat in Categoria.objects.filter(activo=True):
        count = Partida.objects.filter(
            usuario=usuario,
            juego__categoria=cat
        ).count()
        if count > 0:
            partidas_categoria.append({
                'categoria': cat.nombre,
                'total': count
            })
    
    context = {
        'stats': stats,
        'partidas_dias': partidas_dias,
        'partidas_categoria': partidas_categoria,
        'total_partidas': Partida.objects.filter(usuario=usuario).count(),
        'total_correctas': Partida.objects.filter(usuario=usuario, correcto=True).count(),
        'porcentaje_aciertos': round(
            (Partida.objects.filter(usuario=usuario, correcto=True).count() / 
             max(1, Partida.objects.filter(usuario=usuario).count())) * 100, 1
        ),
    }
    
    return render(request, 'dashboard/estadisticas.html', context)

@login_required
def dashboard_cursos(request):
    """Vista de cursos del estudiante"""
    usuario = request.user
    
    cursos_inscritos = ProgresoCurso.objects.filter(
        usuario=usuario
    ).select_related('curso')
    
    context = {
        'cursos_inscritos': cursos_inscritos,
        'cursos_disponibles': Curso.objects.filter(activo=True).exclude(
            id__in=cursos_inscritos.values_list('curso_id', flat=True)
        ),
    }
    
    return render(request, 'dashboard/cursos.html', context)

@login_required
def dashboard_logros(request):
    """Vista de logros del estudiante"""
    # Logros simulados para demostración
    logros = [
        {'nombre': 'Primer paso', 'descripcion': 'Completa tu primer juego', 'icono': '🎯', 'desbloqueado': True, 'fecha': timezone.now() - timezone.timedelta(days=5)},
        {'nombre': 'Aprendiz', 'descripcion': 'Completa 10 juegos', 'icono': '📚', 'desbloqueado': True, 'fecha': timezone.now() - timezone.timedelta(days=3)},
        {'nombre': 'Racha de 5', 'descripcion': 'Alcanza una racha de 5 aciertos', 'icono': '🔥', 'desbloqueado': True, 'fecha': timezone.now() - timezone.timedelta(days=2)},
        {'nombre': 'Estudiante', 'descripcion': 'Completa 25 juegos', 'icono': '🎓', 'desbloqueado': False},
        {'nombre': 'Racha de 10', 'descripcion': 'Alcanza una racha de 10 aciertos', 'icono': '⚡', 'desbloqueado': False},
        {'nombre': 'Experto', 'descripcion': 'Completa 50 juegos', 'icono': '🏆', 'desbloqueado': False},
        {'nombre': 'Versátil', 'descripcion': 'Completa juegos en todas las categorías', 'icono': '🌈', 'desbloqueado': False},
        {'nombre': 'Maestro', 'descripcion': 'Completa 100 juegos', 'icono': '👑', 'desbloqueado': False},
    ]
    
    context = {
        'logros': logros,
        'total_logros': len(logros),
        'desbloqueados': sum(1 for l in logros if l['desbloqueado']),
    }
    
    return render(request, 'dashboard/logros.html', context)
