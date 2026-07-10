#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

def crear_estructura():
    print("🗄️ Creando estructura en MySQL...")
    print("=" * 40)
    
    try:
        # Verificar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            result = cursor.fetchone()
            if result:
                db_name = result[0]
                print(f"✅ Conectado a: {db_name}")
            else:
                print("⚠️ No se pudo obtener el nombre de la base de datos")
        
        # Ejecutar migraciones
        print("📝 Ejecutando migraciones...")
        call_command('migrate', interactive=False)
        
        # Crear superusuario si no existe
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@morphoplay.com', 'admin123')
            print("✅ Superusuario creado: admin / admin123")
        else:
            print("ℹ️ Superusuario ya existe")
        
        print("=" * 40)
        print("✅ Estructura creada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_estructura()
