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
from core.models import Juego, Partida, Progreso, EstadisticasUsuario

def crear_datos_prueba():
    print("🎮 Creando datos de prueba...")
    print("=" * 40)
    
    # Obtener usuario demo
    try:
        usuario = User.objects.get(username='demo_user')
    except User.DoesNotExist:
        print("❌ Usuario demo_user no existe")
        return
    
    # Obtener juegos
    juegos = list(Juego.objects.filter(activo=True))
    if not juegos:
        print("❌ No hay juegos disponibles. Carga los juegos primero.")
        return
    
    print(f"📊 Generando partidas para {usuario.username}...")
    
    partidas_creadas = 0
    for i in range(20):
        juego = random.choice(juegos)
        correcto = random.random() > 0.3
        puntos = juego.puntos if correcto else 0
        tiempo = random.randint(5, 45)
        
        fecha = timezone.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
        
        Partida.objects.create(
            usuario=usuario,
            juego=juego,
            correcto=correcto,
            puntuacion_obtenida=puntos,
            tiempo_segundos=tiempo,
            fecha=fecha
        )
        
        progreso, created = Progreso.objects.get_or_create(
            usuario=usuario,
            juego=juego
        )
        progreso.intentos += 1
        if correcto and not progreso.completado:
            progreso.completado = True
            progreso.puntuacion = puntos
            progreso.fecha_completado = fecha
        progreso.save()
        
        partidas_creadas += 1
    
    # Actualizar estadísticas
    stats, _ = EstadisticasUsuario.objects.get_or_create(usuario=usuario)
    stats.juegos_completados = Progreso.objects.filter(usuario=usuario, completado=True).count()
    stats.puntuacion_total = Partida.objects.filter(usuario=usuario).aggregate(models.Sum('puntuacion_obtenida'))['puntuacion_obtenida__sum'] or 0
    stats.racha_actual = random.randint(0, 15)
    stats.racha_maxima = random.randint(10, 25)
    stats.save()
    
    print("=" * 40)
    print("✅ Datos de prueba creados exitosamente!")
    print(f"\n📊 Estadísticas de {usuario.username}:")
    print(f"  - Partidas: {Partida.objects.filter(usuario=usuario).count()}")
    print(f"  - Juegos completados: {stats.juegos_completados}")
    print(f"  - Puntuación total: {stats.puntuacion_total}")
    print(f"  - Racha actual: {stats.racha_actual}")
    print(f"  - Mejor racha: {stats.racha_maxima}")

if __name__ == "__main__":
    import django.db.models as models
    crear_datos_prueba()
