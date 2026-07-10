#!/usr/bin/env python
import os
import sys
import pymysql
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')

# Instalar pymysql como MySQLdb
pymysql.install_as_MySQLdb()

import django
django.setup()

from django.db import connection
from django.core.management import call_command

def main():
    print("🗄️ Configurando MorphoPlay con MySQL...")
    print("=" * 40)
    
    # Verificar conexión
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()[0]
            print(f"✅ Conectado a MySQL: {version}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\n📝 Verifica que:")
        print("  1. MySQL está corriendo: sudo service mysql status")
        print("  2. .env está configurado correctamente")
        print("  3. El usuario y base de datos existen")
        return
    
    # Ejecutar migraciones
    print("\n📝 Ejecutando migraciones...")
    try:
        call_command('migrate', interactive=False)
        print("✅ Migraciones completadas")
    except Exception as e:
        print(f"❌ Error en migraciones: {e}")
        return
    
    # Crear superusuario
    print("\n👤 Creando superusuario...")
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@morphoplay.com', 'admin123')
        print("✅ Superusuario creado: admin / admin123")
    else:
        print("ℹ️ Superusuario ya existe")
    
    print("=" * 40)
    print("✅ Configuración completa!")
    print("\n🔑 Credenciales:")
    print("   Admin: admin / admin123")
    print("   DB: morphoplay_db / morphoplay_user / morphoplay_pass")

if __name__ == "__main__":
    main()
