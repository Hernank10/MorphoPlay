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

# ============================================================
# EJERCICIOS PERIODÍSTICOS
# ============================================================

def ejercicios_periodisticos(request):
    """Vista para mostrar los 100 ejercicios periodísticos"""
    from .models import Juego, Progreso
    from django.db import models
    
    # Obtener todos los ejercicios periodísticos (IDs 1001-1100)
    ejercicios = Juego.objects.filter(id__gte=1001, id__lte=1100, activo=True).order_by('id')
    
    # Estadísticas
    total_ejercicios = ejercicios.count()
    completados = 0
    puntuacion_total = 0
    
    if request.user.is_authenticated:
        progreso = Progreso.objects.filter(
            usuario=request.user,
            juego__in=ejercicios,
            completado=True
        )
        completados = progreso.count()
        puntuacion_total = progreso.aggregate(models.Sum('puntuacion'))['puntuacion__sum'] or 0
    
    # Agrupar por bloques de 10
    bloques = []
    for i in range(0, 100, 10):
        bloque = ejercicios[i:i+10]
        if bloque:
            bloques.append({
                'numero': i//10 + 1,
                'rango': f"{i+1}-{min(i+10, 100)}",
                'ejercicios': bloque
            })
    
    # Obtener categorías y niveles para filtros
    from .models import Categoria, Nivel
    categorias = Categoria.objects.filter(activo=True)
    niveles = Nivel.objects.all()
    
    context = {
        'ejercicios': ejercicios,
        'bloques': bloques,
        'total_ejercicios': total_ejercicios,
        'completados': completados,
        'puntuacion_total': puntuacion_total,
        'porcentaje': int((completados / total_ejercicios) * 100) if total_ejercicios > 0 else 0,
        'categorias': categorias,
        'niveles': niveles,
    }
    
    return render(request, 'ejercicios/periodisticos.html', context)

@login_required
def ejercicio_periodistico_detail(request, ejercicio_id):
    """Vista detallada de un ejercicio periodístico"""
    from .models import Juego, Partida, Progreso, EstadisticasUsuario
    
    ejercicio = get_object_or_404(Juego, id=ejercicio_id, activo=True)
    
    # Verificar que es un ejercicio periodístico
    if ejercicio_id < 1001 or ejercicio_id > 1100:
        messages.warning(request, 'Este no es un ejercicio periodístico')
        return redirect('juegos:periodisticos')
    
    # Obtener progreso del usuario
    progreso = Progreso.objects.filter(usuario=request.user, juego=ejercicio).first()
    
    # Obtener siguiente y anterior
    siguiente = Juego.objects.filter(id__gt=ejercicio_id, id__lte=1100, activo=True).order_by('id').first()
    anterior = Juego.objects.filter(id__lt=ejercicio_id, id__gte=1001, activo=True).order_by('-id').first()
    
    # Obtener todas las partidas del usuario para este ejercicio
    partidas = Partida.objects.filter(usuario=request.user, juego=ejercicio).order_by('-fecha')
    
    context = {
        'ejercicio': ejercicio,
        'progreso': progreso,
        'siguiente': siguiente,
        'anterior': anterior,
        'partidas': partidas,
        'total_ejercicios': Juego.objects.filter(id__gte=1001, id__lte=1100, activo=True).count(),
        'numero_ejercicio': ejercicio_id - 1000,
    }
    
    return render(request, 'ejercicios/detalle.html', context)

@login_required
def verificar_ejercicio(request):
    """Verificar respuesta de un ejercicio periodístico"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    import json
    data = json.loads(request.body)
    ejercicio_id = data.get('ejercicio_id')
    respuesta = data.get('respuesta', '').strip()
    
    from .models import Juego, Partida, Progreso, EstadisticasUsuario
    from django.utils import timezone
    
    ejercicio = get_object_or_404(Juego, id=ejercicio_id, activo=True)
    es_correcto = respuesta.lower() == ejercicio.respuesta_correcta.lower()
    
    # Registrar partida
    partida = Partida.objects.create(
        usuario=request.user,
        juego=ejercicio,
        correcto=es_correcto,
        puntuacion_obtenida=ejercicio.puntos if es_correcto else 0,
    )
    
    # Actualizar progreso
    progreso, created = Progreso.objects.get_or_create(
        usuario=request.user,
        juego=ejercicio
    )
    progreso.intentos += 1
    
    if es_correcto and not progreso.completado:
        progreso.completado = True
        progreso.puntuacion = ejercicio.puntos
        progreso.fecha_completado = timezone.now()
        
        stats, _ = EstadisticasUsuario.objects.get_or_create(usuario=request.user)
        stats.juegos_completados += 1
        stats.puntuacion_total += ejercicio.puntos
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
        'puntos': ejercicio.puntos if es_correcto else 0,
        'respuesta_correcta': ejercicio.respuesta_correcta,
        'completado': progreso.completado,
        'intentos': progreso.intentos,
        'mensaje': '🎉 ¡Correcto!' if es_correcto else '❌ Incorrecto. Intenta de nuevo.'
    })
