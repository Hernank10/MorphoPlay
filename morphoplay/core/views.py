from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from .models import *

# ============================================================
# VISTAS PRINCIPALES
# ============================================================

def home(request):
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
            stats = request.user.estadisticas
            context['stats'] = stats
        except:
            pass
    
    return render(request, 'core/home.html', context)

# ============================================================
# VISTAS DE AUTENTICACIÓN
# ============================================================

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return render(request, 'accounts/register.html')
        
        user = User.objects.create_user(username, email, password)
        EstadisticasUsuario.objects.create(usuario=user)
        
        login(request, user)
        messages.success(request, '¡Registro exitoso! Bienvenido a MorphoPlay')
        return redirect('home')
    
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('home')

@login_required
def profile(request):
    try:
        stats = request.user.estadisticas
    except:
        stats = None
    return render(request, 'accounts/profile.html', {'estadisticas': stats})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Perfil actualizado')
        return redirect('profile')
    
    return render(request, 'accounts/edit_profile.html')

@login_required
def change_password(request):
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
        messages.success(request, 'Contraseña actualizada')
        return redirect('profile')
    
    return render(request, 'accounts/change_password.html')

# ============================================================
# VISTAS DEL DASHBOARD - CORREGIDAS
# ============================================================

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    usuario = request.user
    
    # Usar get_or_create para evitar error de unicidad
    estadisticas, created = EstadisticasUsuario.objects.get_or_create(
        usuario=usuario,
        defaults={
            'juegos_completados': 0,
            'puntuacion_total': 0,
            'racha_actual': 0,
            'racha_maxima': 0,
            'tiempo_total': 0
        }
    )
    
    ultimas_partidas = Partida.objects.filter(usuario=usuario).order_by('-fecha')[:10]
    
    context = {
        'estadisticas': estadisticas,
        'ultimas_partidas': ultimas_partidas,
    }
    return render(request, 'dashboard/dashboard.html', context)

# ============================================================
# VISTAS DE CURSOS
# ============================================================

def cursos_list(request):
    cursos = Curso.objects.filter(activo=True).select_related('categoria', 'nivel')
    return render(request, 'cursos/list.html', {'cursos': cursos})

@login_required
def curso_detail(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, activo=True)
    progreso, created = ProgresoCurso.objects.get_or_create(usuario=request.user, curso=curso)
    lecciones = curso.get_lecciones()
    evaluaciones = curso.evaluaciones.filter(activo=True).order_by('orden')
    
    context = {
        'curso': curso,
        'progreso': progreso,
        'lecciones': lecciones,
        'evaluaciones': evaluaciones,
    }
    return render(request, 'cursos/detail.html', context)

@login_required
def leccion_detail(request, curso_id, leccion_id):
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
# VISTAS DE JUEGOS
# ============================================================

def juegos_list(request):
    juegos = Juego.objects.filter(activo=True).select_related('categoria', 'nivel')
    categorias = Categoria.objects.filter(activo=True)
    niveles = Nivel.objects.all()
    
    context = {
        'juegos': juegos,
        'categorias': categorias,
        'niveles': niveles,
    }
    return render(request, 'juegos/list.html', context)

@login_required
def juego_detail(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id, activo=True)
    progreso = Progreso.objects.filter(usuario=request.user, juego=juego).first()
    
    context = {
        'juego': juego,
        'progreso': progreso,
    }
    return render(request, 'juegos/detail.html', context)

@login_required
def verificar_respuesta(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    import json
    data = json.loads(request.body)
    juego_id = data.get('juego_id')
    respuesta = data.get('respuesta', '').strip()
    
    juego = get_object_or_404(Juego, id=juego_id, activo=True)
    es_correcto = respuesta.lower() == juego.respuesta_correcta.lower()
    
    partida = Partida.objects.create(
        usuario=request.user,
        juego=juego,
        correcto=es_correcto,
        puntuacion_obtenida=juego.puntos if es_correcto else 0,
    )
    
    progreso, created = Progreso.objects.get_or_create(
        usuario=request.user,
        juego=juego
    )
    progreso.intentos += 1
    
    if es_correcto and not progreso.completado:
        progreso.completado = True
        progreso.puntuacion = juego.puntos
        progreso.fecha_completado = timezone.now()
        
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
        'mensaje': '🎉 ¡Correcto!' if es_correcto else '❌ Incorrecto. Intenta de nuevo.'
    })
