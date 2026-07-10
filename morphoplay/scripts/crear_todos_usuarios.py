#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import EstadisticasUsuario

def main():
    print("=" * 50)
    print("👤 CREANDO TODOS LOS USUARIOS DE PRUEBA")
    print("=" * 50)
    
    usuarios = [
        {'username': 'demo_user', 'email': 'demo@morphoplay.com', 'password': 'MorphoPlay2024!', 'first_name': 'Demo', 'last_name': 'User', 'staff': False, 'superuser': False},
        {'username': 'alumno1', 'email': 'alumno1@test.com', 'password': 'Test12345!', 'first_name': 'Alumno', 'last_name': 'Uno', 'staff': False, 'superuser': False},
        {'username': 'alumno2', 'email': 'alumno2@test.com', 'password': 'Test12345!', 'first_name': 'Alumno', 'last_name': 'Dos', 'staff': False, 'superuser': False},
        {'username': 'alumno3', 'email': 'alumno3@test.com', 'password': 'Test12345!', 'first_name': 'Alumno', 'last_name': 'Tres', 'staff': False, 'superuser': False},
        {'username': 'profesor', 'email': 'profesor@test.com', 'password': 'Test12345!', 'first_name': 'Profesor', 'last_name': 'Test', 'staff': True, 'superuser': False},
        {'username': 'admin_test', 'email': 'admin@test.com', 'password': 'AdminTest123!', 'first_name': 'Admin', 'last_name': 'Test', 'staff': True, 'superuser': True},
    ]
    
    creados = 0
    existentes = 0
    
    for data in usuarios:
        if User.objects.filter(username=data['username']).exists():
            print(f"  ⏳ {data['username']} ya existe")
            existentes += 1
            continue
        
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.is_staff = data['staff']
        user.is_superuser = data['superuser']
        user.save()
        
        EstadisticasUsuario.objects.create(usuario=user)
        print(f"  ✅ {data['username']} - Contraseña: {data['password']}")
        creados += 1
    
    print("=" * 50)
    print(f"✅ {creados} usuarios creados, {existentes} ya existían")
    print(f"📋 Total usuarios: {User.objects.count()}")
    
    print("\n🔑 CREDENCIALES DE PRUEBA:")
    print("-" * 30)
    for u in usuarios:
        print(f"  {u['username']:12} | {u['password']:15} | {'Admin' if u['superuser'] else 'Staff' if u['staff'] else 'Usuario'}")

if __name__ == "__main__":
    main()
