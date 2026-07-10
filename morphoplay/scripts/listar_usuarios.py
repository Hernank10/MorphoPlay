#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import EstadisticasUsuario

def listar_usuarios():
    print("=" * 70)
    print("📋 USUARIOS REGISTRADOS")
    print("=" * 70)
    print(f"{'ID':<4} {'Usuario':<15} {'Email':<30} {'Tipo':<12} {'Juegos':<8} {'Puntos':<8}")
    print("-" * 80)
    
    for u in User.objects.all().order_by('id'):
        stats = EstadisticasUsuario.objects.filter(usuario=u).first()
        juegos = stats.juegos_completados if stats else 0
        puntos = stats.puntuacion_total if stats else 0
        tipo = 'Admin' if u.is_superuser else 'Staff' if u.is_staff else 'Usuario'
        print(f"{u.id:<4} {u.username:<15} {u.email[:28]:<30} {tipo:<12} {juegos:<8} {puntos:<8}")
    
    print("=" * 70)
    print(f"Total: {User.objects.count()} usuarios")

if __name__ == "__main__":
    listar_usuarios()
