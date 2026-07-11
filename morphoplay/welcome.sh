#!/bin/bash
# ============================================================
# MORPHOPLAY - WELCOME SCRIPT
# ============================================================

echo ""
echo "=========================================="
echo "🚀 MORPHOPLAY - BIENVENIDO"
echo "=========================================="
echo ""

# Verificar entorno virtual
if [ -d "venv" ]; then
    echo "✅ Entorno virtual: activo"
else
    echo "⚠️  Entorno virtual: no encontrado"
fi

# Verificar base de datos
if [ -f "db.sqlite3" ]; then
    SIZE=$(ls -lh db.sqlite3 | awk '{print $5}')
    echo "✅ Base de datos: $SIZE"
else
    echo "⚠️  Base de datos: no encontrada"
fi

# Verificar git
if [ -d ".git" ]; then
    BRANCH=$(git branch --show-current)
    COMMITS=$(git log --oneline | wc -l)
    echo "✅ Git: rama $BRANCH ($COMMITS commits)"
else
    echo "⚠️  Git: no inicializado"
fi

# Verificar servidor
if pgrep -f "python manage.py runserver" > /dev/null; then
    echo "✅ Servidor: corriendo en http://localhost:8000"
else
    echo "ℹ️  Servidor: detenido (usar 'mpr' para iniciar)"
fi

echo ""
echo "📋 COMANDOS ÚTILES:"
echo "  mpr   - Iniciar servidor"
echo "  mps   - Abrir shell de Django"
echo "  mpm   - Crear migraciones"
echo "  mpmig - Aplicar migraciones"
echo "  gs    - Ver estado de git"
echo "  info  - Ver información del proyecto"
echo "  backup - Crear respaldo de BD"
echo ""
echo "=========================================="
