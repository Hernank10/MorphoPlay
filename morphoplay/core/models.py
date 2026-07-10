from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=50, blank=True)
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre

class Nivel(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    orden = models.IntegerField(default=0)
    color = models.CharField(max_length=7, default='#6c5ce7')
    puntos_base = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    nivel = models.ForeignKey(Nivel, on_delete=models.SET_NULL, null=True, blank=True)
    duracion_estimada = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.titulo
    
    def get_lecciones(self):
        return self.lecciones.filter(activo=True).order_by('orden')

class Leccion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"

class Juego(models.Model):
    TIPO_CHOICES = [('opcion', 'Opción múltiple'), ('escritura', 'Escritura creativa')]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    pregunta = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    nivel = models.ForeignKey(Nivel, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='opcion')
    opcion1 = models.CharField(max_length=200, blank=True)
    opcion2 = models.CharField(max_length=200, blank=True)
    opcion3 = models.CharField(max_length=200, blank=True)
    opcion4 = models.CharField(max_length=200, blank=True)
    respuesta_correcta = models.CharField(max_length=200)
    puntos = models.IntegerField(default=10)
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.titulo
    
    def get_opciones(self):
        return [self.opcion1, self.opcion2, self.opcion3, self.opcion4]

class Partida(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    correcto = models.BooleanField(default=False)
    puntuacion_obtenida = models.IntegerField(default=0)
    tiempo_segundos = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.juego.titulo}"

class Progreso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    intentos = models.IntegerField(default=0)
    puntuacion = models.IntegerField(default=0)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    ultimo_intento = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['usuario', 'juego']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.juego.titulo}"

class EstadisticasUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    juegos_completados = models.IntegerField(default=0)
    puntuacion_total = models.IntegerField(default=0)
    racha_actual = models.IntegerField(default=0)
    racha_maxima = models.IntegerField(default=0)
    tiempo_total = models.IntegerField(default=0)
    ultima_actividad = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Estadísticas de {self.usuario.username}"

# =============================================
# MODELOS DE EVALUACIONES
# =============================================

class Evaluacion(models.Model):
    """Evaluación de un curso"""
    TIPO_CHOICES = [
        ('diagnostica', 'Diagnóstica'),
        ('formativa', 'Formativa'),
        ('sumativa', 'Sumativa'),
        ('final', 'Final'),
    ]
    
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='evaluaciones')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='formativa')
    puntaje_maximo = models.IntegerField(default=100)
    tiempo_limite = models.IntegerField(default=0, help_text="Tiempo en minutos (0 = sin límite)")
    intentos_permitidos = models.IntegerField(default=1)
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"
    
    def get_preguntas(self):
        return self.preguntas.filter(activo=True).order_by('orden')
    
    class Meta:
        ordering = ['orden', 'created_at']

class PreguntaEvaluacion(models.Model):
    """Pregunta de una evaluación"""
    TIPO_CHOICES = [
        ('opcion', 'Opción Múltiple'),
        ('verdadero_falso', 'Verdadero/Falso'),
        ('texto', 'Respuesta Texto'),
        ('numerica', 'Respuesta Numérica'),
    ]
    
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='preguntas')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='opcion')
    pregunta = models.TextField()
    opcion1 = models.CharField(max_length=200, blank=True)
    opcion2 = models.CharField(max_length=200, blank=True)
    opcion3 = models.CharField(max_length=200, blank=True)
    opcion4 = models.CharField(max_length=200, blank=True)
    respuesta_correcta = models.TextField()
    puntaje = models.IntegerField(default=10)
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.evaluacion.titulo} - Pregunta {self.orden}"
    
    def get_opciones(self):
        if self.tipo == 'opcion':
            return [self.opcion1, self.opcion2, self.opcion3, self.opcion4]
        return []
    
    class Meta:
        ordering = ['orden', 'created_at']

class IntentoEvaluacion(models.Model):
    """Intento de un usuario en una evaluación"""
    ESTADO_CHOICES = [
        ('iniciado', 'Iniciado'),
        ('completado', 'Completado'),
        ('calificado', 'Calificado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='intentos_evaluacion')
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='intentos')
    puntaje_obtenido = models.IntegerField(default=0)
    respuestas = models.JSONField(default=dict)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='iniciado')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    tiempo_utilizado = models.IntegerField(default=0)
    intento_numero = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ['usuario', 'evaluacion', 'intento_numero']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.evaluacion.titulo} - Intento {self.intento_numero}"
    
    def calcular_puntaje(self):
        """Calcula el puntaje basado en las respuestas"""
        puntaje = 0
        for pregunta in self.evaluacion.get_preguntas():
            respuesta_usuario = self.respuestas.get(str(pregunta.id))
            if respuesta_usuario and respuesta_usuario == pregunta.respuesta_correcta:
                puntaje += pregunta.puntaje
        self.puntaje_obtenido = puntaje
        self.save()
        return puntaje

# ============================================================
# MODELOS DE PROGRESO EN CURSOS Y EVALUACIONES
# ============================================================

class ProgresoCurso(models.Model):
    """Progreso del usuario en un curso"""
    ESTADO_CHOICES = [
        ('no_iniciado', 'No Iniciado'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progreso_cursos')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='progreso_usuarios')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='no_iniciado')
    lecciones_completadas = models.IntegerField(default=0)
    evaluaciones_completadas = models.IntegerField(default=0)
    puntaje_total = models.IntegerField(default=0)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    ultimo_acceso = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['usuario', 'curso']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.curso.titulo}"
    
    def actualizar_progreso(self):
        """Actualiza el progreso del curso"""
        total_lecciones = self.curso.get_lecciones().count()
        total_evaluaciones = self.curso.evaluaciones.count()
        
        if total_lecciones > 0:
            if self.lecciones_completadas == total_lecciones:
                self.estado = 'completado'
                self.fecha_completado = timezone.now()
            elif self.lecciones_completadas > 0:
                self.estado = 'en_progreso'
        
        self.save()
        return self.estado

class IntentoEvaluacion(models.Model):
    """Intento de un usuario en una evaluación"""
    ESTADO_CHOICES = [
        ('iniciado', 'Iniciado'),
        ('completado', 'Completado'),
        ('calificado', 'Calificado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='intentos_evaluacion')
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='intentos')
    puntaje_obtenido = models.IntegerField(default=0)
    respuestas = models.JSONField(default=dict)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='iniciado')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    tiempo_utilizado = models.IntegerField(default=0)
    intento_numero = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['usuario', 'evaluacion', 'intento_numero']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.evaluacion.titulo} - Intento {self.intento_numero}"
    
    def calcular_puntaje(self):
        """Calcula el puntaje basado en las respuestas"""
        puntaje = 0
        for pregunta in self.evaluacion.get_preguntas():
            respuesta_usuario = self.respuestas.get(str(pregunta.id))
            if respuesta_usuario and respuesta_usuario == pregunta.respuesta_correcta:
                puntaje += pregunta.puntaje
        self.puntaje_obtenido = puntaje
        self.save()
        return puntaje
