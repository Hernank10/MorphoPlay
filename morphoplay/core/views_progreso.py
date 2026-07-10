from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from .models import Juego, Partida, Progreso, EstadisticasUsuario, Curso

@login_required
def mis_partidas(request):
    """Vista de todas las partidas del usuario"""
    partidas = Partida.objects.filter(usuario=request.user).select_related('juego').order_by('-fecha')
    
    # Estadísticas de partidas
    total_partidas = partidas.count()
    total_correctas = partidas.filter(correcto=True).count()
    total_incorrectas = partidas.filter(correcto=False).count()
    porcentaje_aciertos = (total_correctas / total_partidas * 100) if total_partidas > 0 else 0
    puntuacion_total = partidas.aggregate(Sum('puntuacion_obtenida'))['puntuacion_obtenida__sum'] or 0
    
    # Partidas por categoría
    partidas_por_categoria = partidas.values('juego__categoria__nombre').annotate(
        total=Count('id'),
        correctas=Count('id', filter=Q(correcto=True))
    )
    
    context = {
        'partidas': partidas[:20],  # Últimas 20 partidas
        'total_partidas': total_partidas,
        'total_correctas': total_correctas,
        'total_incorrectas': total_incorrectas,
        'porcentaje_aciertos': round(porcentaje_aciertos, 1),
        'puntuacion_total': puntuacion_total,
        'partidas_por_categoria': partidas_por_categoria,
    }
    return render(request, 'progreso/partidas.html', context)

@login_required
def mi_progreso(request):
    """Vista de progreso del usuario"""
    progreso = Progreso.objects.filter(usuario=request.user).select_related('juego', 'juego__categoria', 'juego__nivel')
    
    total_juegos = Juego.objects.filter(activo=True).count()
    completados = progreso.filter(completado=True).count()
    en_progreso = progreso.filter(completado=False, intentos__gt=0).count()
    no_iniciados = total_juegos - completados - en_progreso
    
    # Progreso por categoría
    progreso_categoria = []
    from .models import Categoria
    for cat in Categoria.objects.filter(activo=True):
        juegos_cat = Juego.objects.filter(categoria=cat, activo=True)
        completados_cat = progreso.filter(juego__categoria=cat, completado=True).count()
        if juegos_cat.exists():
            progreso_categoria.append({
                'categoria': cat.nombre,
                'total': juegos_cat.count(),
                'completados': completados_cat,
                'porcentaje': round((completados_cat / juegos_cat.count()) * 100, 1)
            })
    
    # Últimos juegos jugados
    ultimos_juegos = progreso.order_by('-ultimo_intento')[:10]
    
    context = {
        'progreso': progreso[:20],
        'total_juegos': total_juegos,
        'completados': completados,
        'en_progreso': en_progreso,
        'no_iniciados': no_iniciados,
        'porcentaje_total': round((completados / total_juegos) * 100, 1) if total_juegos > 0 else 0,
        'progreso_categoria': progreso_categoria,
        'ultimos_juegos': ultimos_juegos,
    }
    return render(request, 'progreso/progreso.html', context)

@login_required
def crear_partida_manual(request):
    """Crear una partida manualmente (para pruebas)"""
    if request.method == 'POST':
        juego_id = request.POST.get('juego_id')
        correcto = request.POST.get('correcto') == 'on'
        puntuacion = int(request.POST.get('puntuacion', 0))
        tiempo = int(request.POST.get('tiempo', 0))
        
        juego = get_object_or_404(Juego, id=juego_id)
        
        partida = Partida.objects.create(
            usuario=request.user,
            juego=juego,
            correcto=correcto,
            puntuacion_obtenida=puntuacion,
            tiempo_segundos=tiempo,
        )
        
        # Actualizar progreso
        progreso, created = Progreso.objects.get_or_create(
            usuario=request.user,
            juego=juego
        )
        progreso.intentos += 1
        if correcto and not progreso.completado:
            progreso.completado = True
            progreso.puntuacion = puntuacion
            progreso.fecha_completado = timezone.now()
            
            stats, _ = EstadisticasUsuario.objects.get_or_create(usuario=request.user)
            stats.juegos_completados += 1
            stats.puntuacion_total += puntuacion
            stats.save()
        progreso.save()
        
        messages.success(request, f'Partida creada para {juego.titulo}')
        return redirect('progreso:partidas')
    
    juegos = Juego.objects.filter(activo=True)
    return render(request, 'progreso/crear_partida.html', {'juegos': juegos})

@login_required
def ver_partida(request, partida_id):
    """Ver detalle de una partida"""
    partida = get_object_or_404(Partida, id=partida_id, usuario=request.user)
    return render(request, 'progreso/ver_partida.html', {'partida': partida})

@login_required
def estadisticas_completas(request):
    """Estadísticas completas del usuario"""
    stats = get_object_or_404(EstadisticasUsuario, usuario=request.user)
    
    partidas = Partida.objects.filter(usuario=request.user)
    
    # Tiempo promedio por partida
    tiempo_promedio = partidas.aggregate(Avg('tiempo_segundos'))['tiempo_segundos__avg'] or 0
    
    # Mejor racha (desde estadísticas)
    mejor_racha = stats.racha_maxima
    
    # Días activos
    dias_activos = partidas.dates('fecha', 'day').count()
    
    # Partidas por mes
    partidas_por_mes = partidas.extra(
        select={'mes': "strftime('%%Y-%%m', fecha)"}
    ).values('mes').annotate(
        total=Count('id'),
        correctas=Count('id', filter=Q(correcto=True))
    ).order_by('mes')
    
    context = {
        'stats': stats,
        'tiempo_promedio': round(tiempo_promedio, 1),
        'mejor_racha': mejor_racha,
        'dias_activos': dias_activos,
        'partidas_por_mes': partidas_por_mes,
        'total_partidas': partidas.count(),
        'total_correctas': partidas.filter(correcto=True).count(),
        'porcentaje_aciertos': round((partidas.filter(correcto=True).count() / partidas.count()) * 100, 1) if partidas.count() > 0 else 0,
    }
    return render(request, 'progreso/estadisticas.html', context)
