#!/bin/bash
# Script para gestionar usuarios de MorphoPlay

echo "=========================================="
echo "👤 GESTIÓN DE USUARIOS MORPHOPLAY"
echo "=========================================="
echo ""
echo "1. Ver todos los usuarios"
echo "2. Crear usuario de prueba"
echo "3. Crear todos los usuarios de prueba"
echo "4. Eliminar un usuario"
echo "5. Salir"
echo ""
read -p "Selecciona una opción: " opcion

case $opcion in
    1)
        python manage.py list_users
        ;;
    2)
        read -p "Usuario: " username
        read -p "Email: " email
        read -sp "Contraseña: " password
        echo ""
        python manage.py shell -c "
from django.contrib.auth.models import User
from core.models import EstadisticasUsuario
if not User.objects.filter(username='$username').exists():
    user = User.objects.create_user('$username', '$email', '$password')
    EstadisticasUsuario.objects.create(usuario=user)
    print('✅ Usuario creado')
else:
    print('❌ Usuario ya existe')
"
        ;;
    3)
        python scripts/crear_todos_usuarios.py
        ;;
    4)
        read -p "Usuario a eliminar: " username
        python manage.py shell -c "
from django.contrib.auth.models import User
from core.models import EstadisticasUsuario
try:
    u = User.objects.get(username='$username')
    u.delete()
    print('✅ Usuario eliminado')
except User.DoesNotExist:
    print('❌ Usuario no encontrado')
"
        ;;
    5)
        exit 0
        ;;
    *)
        echo "Opción inválida"
        ;;
esac
