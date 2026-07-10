#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import EstadisticasUsuario

def crear_usuarios_prueba():
    print("👤 Creando usuarios de prueba...")
    print("=" * 40)
    
    usuarios = [
        {'username': 'alumno1', 'email': 'alumno1@test.com', 'password': 'Test12345!'},
        {'username': 'alumno2', 'email': 'alumno2@test.com', 'password': 'Test12345!'},
        {'username': 'alumno3', 'email': 'alumno3@test.com', 'password': 'Test12345!'},
        {'username': 'profesor', 'email': 'profesor@test.com', 'password': 'Test12345!'},
    ]
    
    creados = 0
    for data in usuarios:
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['username'].capitalize(),
                last_name='Test'
            )
            EstadisticasUsuario.objects.create(usuario=user)
            print(f"  ✅ {data['username']} - Contraseña: {data['password']}")
            creados += 1
        else:
            print(f"  ⏳ {data['username']} ya existe")
    
    print("=" * 40)
    print(f"✅ {creados} usuarios creados exitosamente!")
    print("\n📋 Resumen de usuarios:")
    for u in User.objects.filter(is_superuser=False):
        print(f"  - {u.username}: {u.email}")

if __name__ == "__main__":
    crear_usuarios_prueba()
