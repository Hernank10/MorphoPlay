#!/bin/bash
echo "=========================================="
echo "🔑 CONFIGURANDO PERMISOS DE USUARIOS"
echo "=========================================="

# Activar entorno virtual
source venv/bin/activate

# 1. Mostrar usuarios actuales
echo "1. Usuarios actuales:"
python manage.py shell -c "
from django.contrib.auth.models import User
for u in User.objects.all():
    print(f'  {u.username} - Staff: {u.is_staff} - Superuser: {u.is_superuser}')
"

# 2. Dar permisos a profesor
echo ""
echo "2. Dando permisos a profesor..."
python manage.py shell -c "
from django.contrib.auth.models import User
user = User.objects.get(username='profesor')
user.is_staff = True
user.save()
print('✅ profesor ahora es Staff')
"

# 3. Dar permisos a alumno1 (opcional)
echo ""
echo "3. Dando permisos a alumno1..."
python manage.py shell -c "
from django.contrib.auth.models import User
user = User.objects.get(username='alumno1')
user.is_staff = True
user.save()
print('✅ alumno1 ahora es Staff')
"

# 4. Verificar permisos finales
echo ""
echo "4. Permisos finales:"
python manage.py shell -c "
from django.contrib.auth.models import User
print('📋 PERMISOS FINALES:')
print('=' * 50)
for u in User.objects.all():
    admin = '✅' if u.is_staff or u.is_superuser else '❌'
    print(f'{u.username:15} | Staff: {u.is_staff} | Superuser: {u.is_superuser} | Admin: {admin}')
"

echo ""
echo "=========================================="
echo "✅ CONFIGURACIÓN COMPLETA"
echo "=========================================="
echo ""
echo "🔑 Usuarios con acceso al admin:"
echo "   admin    | admin123    | Superuser"
echo "   profesor | Test12345!  | Staff"
echo "   alumno1  | Test12345!  | Staff"
echo ""
echo "📝 Para dar permisos a otros usuarios:"
echo "   python scripts/gestionar_permisos.py"
