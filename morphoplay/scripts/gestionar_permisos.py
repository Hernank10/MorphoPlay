#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User

def gestionar_permisos():
    print("🔑 GESTIÓN DE PERMISOS DE USUARIOS")
    print("=" * 50)
    
    # Mostrar usuarios actuales
    print("\n📋 Usuarios actuales:")
    for u in User.objects.all():
        admin = '✅' if u.is_staff or u.is_superuser else '❌'
        print(f"  {u.username:15} | Staff: {u.is_staff} | Superuser: {u.is_superuser} | Admin: {admin}")
    
    print("\n" + "=" * 50)
    print("1. Dar permisos de Staff a un usuario")
    print("2. Quitar permisos de Staff a un usuario")
    print("3. Hacer Superuser a un usuario")
    print("4. Ver permisos")
    print("0. Salir")
    
    opcion = input("\nSelecciona una opción: ").strip()
    
    if opcion == '1':
        username = input("Usuario: ").strip()
        try:
            user = User.objects.get(username=username)
            user.is_staff = True
            user.save()
            print(f"✅ {username} ahora es Staff")
        except User.DoesNotExist:
            print(f"❌ Usuario {username} no existe")
    
    elif opcion == '2':
        username = input("Usuario: ").strip()
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                print(f"❌ No se puede quitar permisos a un Superuser")
            else:
                user.is_staff = False
                user.save()
                print(f"✅ Permisos de Staff quitados a {username}")
        except User.DoesNotExist:
            print(f"❌ Usuario {username} no existe")
    
    elif opcion == '3':
        username = input("Usuario: ").strip()
        try:
            user = User.objects.get(username=username)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print(f"✅ {username} ahora es Superuser")
        except User.DoesNotExist:
            print(f"❌ Usuario {username} no existe")
    
    elif opcion == '4':
        print("\n📋 PERMISOS DE USUARIOS:")
        print("=" * 50)
        for u in User.objects.all():
            admin = '✅' if u.is_staff or u.is_superuser else '❌'
            print(f"  {u.username:15} | Staff: {u.is_staff} | Superuser: {u.is_superuser} | Admin: {admin}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    gestionar_permisos()
