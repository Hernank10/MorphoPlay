#!/usr/bin/env python
import os
import sys
import random
from datetime import datetime, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from core.models import (
    Categoria, Nivel, Juego, Curso, Leccion, 
    Partida, Progreso, EstadisticasUsuario, ProgresoCurso
)

def crear_datos_estudiantes():
    print("📊 Creando datos para estudiantes...")
    print("=" * 50)
    
    # Obtener estudiantes
    estudiantes = User.objects.filter(
        username__in=['alumno1', 'alumno2', 'alumno3', 'demo_user']
    )
    
    if not estudiantes:
        print("❌ No hay estudiantes. Crea usuarios primero.")
        return
    
    # Obtener juegos
    juegos = list(Juego.objects.filter(activo=True))
    if not juegos:
        print("❌ No hay juegos. Carga juegos primero.")
        return
    
    # Obtener cursos
    cursos = list(Curso.objects.filter(activo=True))
    
    print(f"👤 Estudiantes encontrados: {estudiantes.count()}")
    print(f"🎮 Juegos disponibles: {len(juegos)}")
    print(f"📚 Cursos disponibles: {len(cursos)}")
    print()
    
    for estudiante in estudiantes:
        print(f"📊 Generando datos para {estudiante.username}...")
        
        # 1. Crear partidas aleatorias
        partidas_creadas = 0
        for i in range(random.randint(10, 25)):
            juego = random.choice(juegos)
            correcto = random.random() > 0.3
            puntos = juego.puntos if correcto else 0
            tiempo = random.randint(5, 45)
            
            fecha = timezone.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
            
            Partida.objects.create(
                usuario=estudiante,
                juego=juego,
                correcto=correcto,
                puntuacion_obtenida=puntos,
                tiempo_segundos=tiempo,
                fecha=fecha
            )
            
            progreso, created = Progreso.objects.get_or_create(
                usuario=estudiante,
                juego=juego
            )
            progreso.intentos += 1
            if correcto and not progreso.completado:
                progreso.completado = True
                progreso.puntuacion = puntos
                progreso.fecha_completado = fecha
            progreso.save()
            
            partidas_creadas += 1
        
        # 2. Actualizar estadísticas
        stats, _ = EstadisticasUsuario.objects.get_or_create(usuario=estudiante)
        stats.juegos_completados = Progreso.objects.filter(
            usuario=estudiante, completado=True
        ).count()
        stats.puntuacion_total = Partida.objects.filter(
            usuario=estudiante
        ).aggregate(models.Sum('puntuacion_obtenida'))['puntuacion_obtenida__sum'] or 0
        stats.racha_actual = random.randint(0, 15)
        stats.racha_maxima = random.randint(5, 25)
        stats.save()
        
        # 3. Inscribir en cursos aleatorios
        if cursos:
            for curso in random.sample(cursos, min(2, len(cursos))):
                pc, created = ProgresoCurso.objects.get_or_create(
                    usuario=estudiante,
                    curso=curso
                )
                if created:
                    lecciones = curso.get_lecciones()
                    completadas = random.randint(0, lecciones.count())
                    pc.lecciones_completadas = completadas
                    if completadas == lecciones.count():
                        pc.estado = 'completado'
                        pc.fecha_completado = timezone.now()
                    elif completadas > 0:
                        pc.estado = 'en_progreso'
                    pc.save()
                    print(f"  📚 Inscrito en: {curso.titulo} ({completadas}/{lecciones.count()})")
        
        print(f"  ✅ Partidas: {partidas_creadas}")
        print(f"  ✅ Juegos completados: {stats.juegos_completados}")
        print(f"  ✅ Puntuación: {stats.puntuacion_total}")
        print()
    
    print("=" * 50)
    print("✅ Datos para estudiantes creados exitosamente!")

if __name__ == "__main__":
    import django.db.models as models
    crear_datos_estudiantes()
