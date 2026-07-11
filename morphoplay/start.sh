#!/bin/bash
# ============================================================
# MORPHOPLAY - INICIO RÁPIDO
# ============================================================

echo "🚀 Iniciando MorphoPlay..."

# Activar entorno virtual
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Entorno virtual activado"
else
    echo "❌ Entorno virtual no encontrado"
    exit 1
fi

# Verificar base de datos
if [ ! -f "db.sqlite3" ]; then
    echo "⚠️  Base de datos no encontrada. Creando..."
    python manage.py migrate
    python manage.py createsuperuser
fi

# Crear respaldo automático
if [ -f "db.sqlite3" ]; then
    BACKUP_FILE="db_backup_$(date +%Y%m%d_%H%M%S).sqlite3"
    cp db.sqlite3 "$BACKUP_FILE"
    echo "✅ Respaldo creado: $BACKUP_FILE"
fi

# Verificar contenido
echo ""
echo "📊 VERIFICANDO CONTENIDO..."
echo "Cursos: $(python manage.py shell -c "from core.models import Curso; print(Curso.objects.count())" 2>/dev/null || echo '?')"
echo "Juegos: $(python manage.py shell -c "from core.models import Juego; print(Juego.objects.count())" 2>/dev/null || echo '?')"
echo "Usuarios: $(python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.count())" 2>/dev/null || echo '?')"

echo ""
echo "🌐 Iniciando servidor en http://localhost:8000"
echo "   Presiona CTRL+C para detener"
echo ""

# Iniciar servidor
python manage.py runserver 0.0.0.0:8000
