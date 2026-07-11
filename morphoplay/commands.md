# 📚 MORPHOPLAY - COMMANDS REFERENCE

## 🚀 INICIO RÁPIDO

```bash
# 1. Activar entorno
source venv/bin/activate

# 2. Iniciar servidor
python manage.py runserver 0.0.0.0:8000

# 3. Acceder
# http://localhost:8000
# Crear superusuario
python manage.py createsuperuser

# Listar usuarios
python manage.py shell -c "from django.contrib.auth.models import User; print([u.username for u in User.objects.all()])"

# Crear usuario de prueba
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('test', 'test@test.com', 'test123')"
# Crear lecciones para cursos vacíos
python scripts/crear_lecciones_evaluaciones.py

# Listar cursos
python manage.py shell -c "from core.models import Curso; print([f'{c.id}: {c.titulo}' for c in Curso.objects.all()])"
# Generar ejercicios
python manage.py generar_ejercicios --cantidad 10

# Generar y cargar
python manage.py generar_ejercicios --cantidad 5 --cargar

# Listar juegos
python manage.py shell -c "from core.models import Juego; print([f'{j.id}: {j.titulo}' for j in Juego.objects.all()])"
# Listar certificaciones
python manage.py shell -c "from core.models import Certificacion; print([f'{c.usuario.username}: {c.curso.titulo}' for c in Certificacion.objects.all()])"

# Generar certificación manual
python manage.py shell -c "from core.models import Certificacion, Curso, User; c=Curso.objects.first(); u=User.objects.first(); Certificacion.objects.create(usuario=u, curso=c, nivel='basico', codigo='CERT-1234')"
# Respaldo
cp db.sqlite3 db_backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Ver tamaño
ls -lh db.sqlite3

# Resetear BD (CUIDADO!)
rm -f db.sqlite3 && python manage.py migrate
# Panel de administración terminal
python admin_morphoplay.py

# Terminal interactiva
python terminal_morphoplay.py

# Shell de Django
python manage.py shell
