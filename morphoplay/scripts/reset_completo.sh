#!/bin/bash
echo "=========================================="
echo "🔄 REINICIANDO MORPHOPLAY COMPLETAMENTE"
echo "=========================================="

# Activar entorno virtual
source venv/bin/activate

# 1. Eliminar base de datos
echo "1. Eliminando base de datos..."
rm -f db.sqlite3

# 2. Eliminar migraciones
echo "2. Eliminando migraciones..."
rm -rf core/migrations/00*.py 2>/dev/null
rm -rf api/migrations/00*.py 2>/dev/null
rm -rf analytics/migrations/00*.py 2>/dev/null
rm -rf recommendations/migrations/00*.py 2>/dev/null
rm -rf certifications/migrations/00*.py 2>/dev/null
rm -rf multiplayer/migrations/00*.py 2>/dev/null
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# 3. Crear migraciones
echo "3. Creando migraciones..."
python manage.py makemigrations core
python manage.py makemigrations

# 4. Aplicar migraciones
echo "4. Aplicando migraciones..."
python manage.py migrate

# 5. Crear superusuario
echo "5. Creando superusuario..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@morphoplay.com', 'admin123')
    print('✅ Admin creado: admin / admin123')
"

# 6. Crear usuarios
echo "6. Creando usuarios..."
python manage.py shell -c "
from django.contrib.auth.models import User
from core.models import EstadisticasUsuario
usuarios = [
    ('demo_user', 'demo@morphoplay.com', 'MorphoPlay2024!'),
    ('alumno1', 'alumno1@test.com', 'Test12345!'),
    ('alumno2', 'alumno2@test.com', 'Test12345!'),
    ('alumno3', 'alumno3@test.com', 'Test12345!'),
    ('profesor', 'profesor@test.com', 'Test12345!'),
]
for u, e, p in usuarios:
    if not User.objects.filter(username=u).exists():
        user = User.objects.create_user(u, e, p)
        EstadisticasUsuario.objects.create(usuario=user)
        print(f'✅ {u} creado')
"

# 7. Cargar juegos
echo "7. Cargando juegos..."
python scripts/cargar_juegos_cursos.py

# 8. Crear datos de estudiantes
echo "8. Creando datos de estudiantes..."
python scripts/crear_datos_estudiantes.py

echo "=========================================="
echo "✅ REINICIO COMPLETO"
echo "=========================================="
echo ""
echo "🔑 Credenciales:"
echo "   admin: admin123 (Superuser)"
echo "   demo_user: MorphoPlay2024!"
echo ""
echo "🚀 Inicia el servidor:"
echo "   python manage.py runserver 0.0.0.0:8000"
