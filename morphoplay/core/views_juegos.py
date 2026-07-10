from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Juego, Categoria, Nivel, Partida, Progreso, EstadisticasUsuario
import json

def juegos_list(request):
    """Lista de todos los juegos disponibles"""
    categorias = Categoria.objects.filter(activo=True)
    niveles = Nivel.objects.all()
    
    # Obtener filtros
    categoria_id = request.GET.get('categoria')
    nivel_id = request.GET.get('nivel')
    
    juegos = Juego.objects.filter(activo=True)
    
    if categoria_id:
        juegos = juegos.filter(categoria_id=categoria_id)
    if nivel_id:
        juegos = juegos.filter(nivel_id=nivel_id)
    
    context = {
        'juegos': juegos,
        'categorias': categorias,
        'niveles': niveles,
        'categoria_seleccionada': int(categoria_id) if categoria_id else None,
        'nivel_seleccionado': int(nivel_id) if nivel_id else None,
        'total_juegos': juegos.count(),
    }
    return render(request, 'juegos/list.html', context)

@login_required
def juego_detail(request, juego_id):
    """Vista detallada de un juego"""
    juego = get_object_or_404(Juego, id=juego_id, activo=True)
    
    # Obtener progreso del usuario
    progreso = Progreso.objects.filter(usuario=request.user, juego=juego).first()
    
    # Obtener siguiente y anterior juego
    siguiente = Juego.objects.filter(activo=True, orden__gt=juego.orden).first()
    anterior = Juego.objects.filter(activo=True, orden__lt=juego.orden).last()
    
    context = {
        'juego': juego,
        'progreso': progreso,
        'siguiente': siguiente,
        'anterior': anterior,
        'total_juegos': Juego.objects.filter(activo=True).count(),
    }
    return render(request, 'juegos/detail.html', context)

@login_required
def verificar_respuesta(request):
    """Verifica la respuesta de un juego"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    data = json.loads(request.body)
    juego_id = data.get('juego_id')
    respuesta = data.get('respuesta', '').strip()
    
    juego = get_object_or_404(Juego, id=juego_id)
    es_correcto = respuesta.lower() == juego.respuesta_correcta.lower()
    
    # Registrar partida
    partida = Partida.objects.create(
        usuario=request.user,
        juego=juego,
        correcto=es_correcto,
        puntuacion_obtenida=juego.puntos if es_correcto else 0,
    )
    
    # Actualizar progreso
    progreso, created = Progreso.objects.get_or_create(
        usuario=request.user,
        juego=juego
    )
    progreso.intentos += 1
    
    if es_correcto and not progreso.completado:
        progreso.completado = True
        progreso.puntuacion = juego.puntos
        progreso.fecha_completado = timezone.now()
        
        # Actualizar estadísticas
        stats, _ = EstadisticasUsuario.objects.get_or_create(usuario=request.user)
        stats.juegos_completados += 1
        stats.puntuacion_total += juego.puntos
        stats.racha_actual += 1
        
        if stats.racha_actual > stats.racha_maxima:
            stats.racha_maxima = stats.racha_actual
        stats.save()
    else:
        if not es_correcto:
            stats, _ = EstadisticasUsuario.objects.get_or_create(usuario=request.user)
            stats.racha_actual = 0
            stats.save()
    
    progreso.save()
    
    return JsonResponse({
        'correcto': es_correcto,
        'puntos': juego.puntos if es_correcto else 0,
        'respuesta_correcta': juego.respuesta_correcta,
        'completado': progreso.completado,
        'intentos': progreso.intentos,
        'mensaje': '🎉 ¡Correcto!' if es_correcto else '❌ Incorrecto. Intenta de nuevo.'
    })
