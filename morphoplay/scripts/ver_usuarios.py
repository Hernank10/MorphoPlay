#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import EstadisticasUsuario

def ver_usuarios():
    print("=" * 60)
    print("📋 USUARIOS REGISTRADOS")
    print("=" * 60)
    print(f"{'ID':<4} {'Usuario':<15} {'Email':<30} {'Tipo':<10} {'Juegos':<8} {'Puntos':<8}")
    print("-" * 60)
    
    for u in User.objects.all().order_by('id'):
        tipo = 'Admin' if u.is_superuser else 'Staff' if u.is_staff else 'Usuario'
        stats = EstadisticasUsuario.objects.filter(usuario=u).first()
        juegos = stats.juegos_completados if stats else 0
        puntos = stats.puntuacion_total if stats else 0
        print(f"{u.id:<4} {u.username:<15} {u.email:<30} {tipo:<10} {juegos:<8} {puntos:<8}")
    
    print("=" * 60)
    print(f"Total: {User.objects.count()} usuarios")

if __name__ == "__main__":
    ver_usuarios()
