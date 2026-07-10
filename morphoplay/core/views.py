from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from .models import (
    Categoria, Nivel, Juego, Partida, Progreso, EstadisticasUsuario,
    Curso, Leccion, Evaluacion, PreguntaEvaluacion, IntentoEvaluacion, ProgresoCurso
)

def home(request):
    """Página principal"""
    total_juegos = Juego.objects.filter(activo=True).count()
    total_cursos = Curso.objects.filter(activo=True).count()
    total_categorias = Categoria.objects.filter(activo=True).count()
    
    juegos_destacados = Juego.objects.filter(activo=True).order_by('?')[:6]
    cursos_destacados = Curso.objects.filter(activo=True).order_by('?')[:3]
    categorias = Categoria.objects.filter(activo=True)[:6]
    
    context = {
        'total_juegos': total_juegos,
        'total_cursos': total_cursos,
        'total_categorias': total_categorias,
        'juegos_destacados': juegos_destacados,
        'cursos_destacados': cursos_destacados,
        'categorias': categorias,
    }
    
    if request.user.is_authenticated:
        try:
            stats, created = EstadisticasUsuario.objects.get_or_create(usuario=request.user)
            context['stats'] = stats
        except Exception as e:
            context['stats'] = None
        
        ultimas_partidas = Partida.objects.filter(usuario=request.user).order_by('-fecha')[:5]
        context['ultimas_partidas'] = ultimas_partidas
    
    return render(request, 'core/home.html', context)

def register(request):
    """Registro de usuarios"""
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado')
            return render(request, 'accounts/register.html')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Crear estadísticas iniciales
        EstadisticasUsuario.objects.get_or_create(usuario=user)
        
        messages.success(request, 'Registro exitoso. ¡Bienvenido!')
        login(request, user)
        return redirect('dashboard:dashboard')
    
    return render(request, 'accounts/register.html')

def login_view(request):
    """Inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido de vuelta, {user.username}!')
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    messages.info(request, 'Sesión cerrada exitosamente')
    return redirect('home')

@login_required
def profile(request):
    """Perfil del usuario"""
    try:
        stats = request.user.estadisticas
    except:
        stats = None
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'estadisticas': stats,
    })

@login_required
def edit_profile(request):
    """Editar perfil"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Perfil actualizado exitosamente')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/edit_profile.html')

@login_required
def change_password(request):
    """Cambiar contraseña"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'Contraseña actual incorrecta')
            return render(request, 'accounts/change_password.html')
        
        if new_password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'accounts/change_password.html')
        
        if len(new_password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return render(request, 'accounts/change_password.html')
        
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Contraseña actualizada exitosamente')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/change_password.html')

# =============================================
# VISTAS DEL DASHBOARD
# =============================================

@login_required
def dashboard(request):
    """Dashboard del usuario"""
    usuario = request.user
    
    try:
        estadisticas = usuario.estadisticas
    except:
        estadisticas = EstadisticasUsuario.objects.create(usuario=usuario)
    
    ultimas_partidas = Partida.objects.filter(usuario=usuario).order_by('-fecha')[:10]
    progreso_cursos = ProgresoCurso.objects.filter(usuario=usuario).select_related('curso')
    
    total_juegos = Juego.objects.filter(activo=True).count()
    juegos_completados_porcentaje = int((estadisticas.juegos_completados / max(1, total_juegos)) * 100)
    
    context = {
        'estadisticas': estadisticas,
        'ultimas_partidas': ultimas_partidas,
        'progreso_cursos': progreso_cursos,
        'total_juegos': total_juegos,
        'juegos_completados_porcentaje': juegos_completados_porcentaje,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def dashboard_stats(request):
    """Estadísticas del dashboard (API)"""
    usuario = request.user
    estadisticas = usuario.estadisticas
    
    progreso_categoria = []
    for categoria in Categoria.objects.filter(activo=True):
        juegos_categoria = Juego.objects.filter(categoria=categoria, activo=True)
        completados = Progreso.objects.filter(
            usuario=usuario,
            juego__in=juegos_categoria,
            completado=True
        ).count()
        progreso_categoria.append({
            'categoria': categoria.nombre,
            'total': juegos_categoria.count(),
            'completados': completados,
            'porcentaje': int((completados / max(1, juegos_categoria.count())) * 100)
        })
    
    return JsonResponse({
        'juegos_completados': estadisticas.juegos_completados,
        'puntuacion_total': estadisticas.puntuacion_total,
        'racha_actual': estadisticas.racha_actual,
        'racha_maxima': estadisticas.racha_maxima,
        'progreso_categoria': progreso_categoria,
        'ultima_actividad': estadisticas.ultima_actividad.isoformat(),
    })

def cursos_list(request):
    """Lista de cursos"""
    cursos = Curso.objects.filter(activo=True).select_related('categoria', 'nivel')
    return render(request, 'cursos/list.html', {'cursos': cursos})

@login_required
def curso_detail(request, curso_id):
    """Detalle de un curso"""
    curso = get_object_or_404(Curso, id=curso_id, activo=True)
    progreso, created = ProgresoCurso.objects.get_or_create(usuario=request.user, curso=curso)
    lecciones = curso.get_lecciones()
    evaluaciones = curso.evaluaciones.filter(activo=True).order_by('orden')
    
    context = {
        'curso': curso,
        'progreso': progreso,
        'lecciones': lecciones,
        'evaluaciones': evaluaciones,
        'lecciones_count': lecciones.count(),
        'evaluaciones_count': evaluaciones.count(),
    }
    return render(request, 'cursos/detail.html', context)

@login_required
def leccion_detail(request, curso_id, leccion_id):
    """Detalle de una lección"""
    curso = get_object_or_404(Curso, id=curso_id, activo=True)
    leccion = get_object_or_404(Leccion, id=leccion_id, curso=curso, activo=True)
    progreso, _ = ProgresoCurso.objects.get_or_create(usuario=request.user, curso=curso)
    
    anterior = curso.get_lecciones().filter(orden__lt=leccion.orden).last()
    siguiente = curso.get_lecciones().filter(orden__gt=leccion.orden).first()
    
    context = {
        'curso': curso,
        'leccion': leccion,
        'anterior': anterior,
        'siguiente': siguiente,
        'progreso': progreso,
    }
    return render(request, 'cursos/leccion.html', context)

@login_required
def evaluacion_detail(request, curso_id, evaluacion_id):
    """Detalle de una evaluación"""
    curso = get_object_or_404(Curso, id=curso_id, activo=True)
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id, curso=curso, activo=True)
    
    intentos_anteriores = IntentoEvaluacion.objects.filter(
        usuario=request.user, evaluacion=evaluacion
    ).count()
    
    if intentos_anteriores >= evaluacion.intentos_permitidos:
        messages.warning(request, 'Ya has completado todos los intentos permitidos')
        return redirect('cursos:detail', curso_id=curso.id)
    
    intento_actual = IntentoEvaluacion.objects.filter(
        usuario=request.user, evaluacion=evaluacion, estado='iniciado'
    ).first()
    
    if not intento_actual:
        intento_actual = IntentoEvaluacion.objects.create(
            usuario=request.user,
            evaluacion=evaluacion,
            intento_numero=intentos_anteriores + 1
        )
    
    preguntas = evaluacion.get_preguntas()
    
    context = {
        'curso': curso,
        'evaluacion': evaluacion,
        'intento': intento_actual,
        'preguntas': preguntas,
        'tiempo_limite': evaluacion.tiempo_limite,
        'intentos_restantes': evaluacion.intentos_permitidos - intentos_anteriores,
    }
    return render(request, 'cursos/evaluacion.html', context)

@login_required
def submit_evaluacion(request, curso_id, evaluacion_id):
    """Enviar evaluación"""
    if request.method != 'POST':
        return redirect('cursos:detail', curso_id=curso_id)
    
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id, activo=True)
    intento = get_object_or_404(IntentoEvaluacion, usuario=request.user, evaluacion=evaluacion, estado='iniciado')
    
    respuestas = {}
    for pregunta in evaluacion.get_preguntas():
        respuesta = request.POST.get(f'pregunta_{pregunta.id}')
        if respuesta:
            respuestas[str(pregunta.id)] = respuesta
    
    intento.respuestas = respuestas
    intento.estado = 'completado'
    intento.fecha_completado = timezone.now()
    intento.save()
    
    puntaje = intento.calcular_puntaje()
    messages.success(request, f'Evaluación completada. Puntaje: {puntaje}/{evaluacion.puntaje_maximo}')
    return redirect('cursos:detail', curso_id=curso_id)

# ============================================================
# VISTAS PARA EJERCICIOS PERIODÍSTICOS
# ============================================================

def ejercicios_periodisticos(request):
    """Vista para mostrar los 100 ejercicios periodísticos"""
    from .models import Juego
    
    # Obtener todos los ejercicios periodísticos (IDs 1001-1100)
    ejercicios = Juego.objects.filter(id__gte=1001, id__lte=1100, activo=True).order_by('id')
    
    # Estadísticas
    total_ejercicios = ejercicios.count()
    completados = 0
    puntuacion_total = 0
    
    if request.user.is_authenticated:
        from .models import Progreso
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
    
    context = {
        'ejercicios': ejercicios,
        'bloques': bloques,
        'total_ejercicios': total_ejercicios,
        'completados': completados,
        'puntuacion_total': puntuacion_total,
        'porcentaje': int((completados / total_ejercicios) * 100) if total_ejercicios > 0 else 0,
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
        return redirect('ejercicios_periodisticos')
    
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
