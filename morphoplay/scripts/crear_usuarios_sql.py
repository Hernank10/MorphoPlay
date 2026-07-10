#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection
from core.models import EstadisticasUsuario, Categoria, Nivel, Juego

def crear_usuarios_sql():
    print("👤 Creando usuarios de prueba en la base de datos...")
    print("=" * 50)
    
    # Lista de usuarios de prueba
    usuarios = [
        {
            'username': 'demo_user',
            'email': 'demo@morphoplay.com',
            'password': 'MorphoPlay2024!',
            'first_name': 'Demo',
            'last_name': 'User',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'alumno1',
            'email': 'alumno1@test.com',
            'password': 'Test12345!',
            'first_name': 'Alumno',
            'last_name': 'Uno',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'alumno2',
            'email': 'alumno2@test.com',
            'password': 'Test12345!',
            'first_name': 'Alumno',
            'last_name': 'Dos',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'alumno3',
            'email': 'alumno3@test.com',
            'password': 'Test12345!',
            'first_name': 'Alumno',
            'last_name': 'Tres',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'profesor',
            'email': 'profesor@test.com',
            'password': 'Test12345!',
            'first_name': 'Profesor',
            'last_name': 'Test',
            'is_staff': True,
            'is_superuser': False
        },
        {
            'username': 'admin_test',
            'email': 'admin@test.com',
            'password': 'AdminTest123!',
            'first_name': 'Admin',
            'last_name': 'Test',
            'is_staff': True,
            'is_superuser': True
        }
    ]
    
    creados = 0
    existentes = 0
    
    for data in usuarios:
        # Verificar si el usuario ya existe
        if User.objects.filter(username=data['username']).exists():
            print(f"  ⏳ Usuario {data['username']} ya existe")
            existentes += 1
            continue
        
        # Crear usuario
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        
        # Asignar permisos especiales
        user.is_staff = data['is_staff']
        user.is_superuser = data['is_superuser']
        user.save()
        
        # Crear estadísticas para el usuario
        EstadisticasUsuario.objects.create(usuario=user)
        
        print(f"  ✅ {data['username']} - Contraseña: {data['password']}")
        creados += 1
    
    print("=" * 50)
    print(f"✅ {creados} usuarios creados, {existentes} ya existían")
    
    # Mostrar resumen
    print("\n📋 Resumen de usuarios en la base de datos:")
    print(f"  Total usuarios: {User.objects.count()}")
    for u in User.objects.all().order_by('id'):
        stats = "⭐ Admin" if u.is_superuser else "👨‍🏫 Staff" if u.is_staff else "👤 Usuario"
        print(f"  - {u.username} ({u.email}) - {stats}")

if __name__ == "__main__":
    crear_usuarios_sql()
