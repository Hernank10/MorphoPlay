#!/bin/bash
echo "=========================================="
echo "🔧 ARREGLANDO MYSQL EN CODESPACES"
echo "=========================================="

# 1. Detener MySQL
echo "1. Deteniendo MySQL..."
sudo service mysql stop
sudo pkill -f mysql 2>/dev/null
sudo pkill -f mysqld 2>/dev/null
sudo killall -9 mysql 2>/dev/null
sudo killall -9 mysqld 2>/dev/null
sleep 2

# 2. Limpiar archivos
echo "2. Limpiando archivos temporales..."
sudo rm -f /var/run/mysqld/mysqld.pid
sudo rm -f /var/run/mysqld/mysqld.sock
sudo rm -f /var/lib/mysql/mysql.sock
sudo rm -f /tmp/mysql.sock

# 3. Crear directorio
echo "3. Creando directorio de socket..."
sudo mkdir -p /var/run/mysqld
sudo chown mysql:mysql /var/run/mysqld
sudo chmod 755 /var/run/mysqld

# 4. Iniciar MySQL
echo "4. Iniciando MySQL..."
sudo service mysql start
sleep 3

# 5. Verificar estado
echo "5. Verificando estado..."
sudo service mysql status

# 6. Verificar socket
echo "6. Verificando socket..."
if [ -e /var/run/mysqld/mysqld.sock ]; then
    echo "✅ Socket creado correctamente"
    ls -la /var/run/mysqld/mysqld.sock
else
    echo "❌ Socket no encontrado. Intentando solución alternativa..."
    # Configurar MySQL para usar /tmp
    sudo sed -i 's/socket = \/var\/run\/mysqld\/mysqld.sock/socket = \/tmp\/mysql.sock/g' /etc/mysql/my.cnf
    sudo service mysql restart
fi

# 7. Verificar conexión
echo "7. Probando conexión..."
sudo mysql -e "SELECT 1;" 2>/dev/null && echo "✅ Conexión exitosa" || echo "❌ Error de conexión"

echo "=========================================="
echo "✅ PROCESO COMPLETADO"
echo "=========================================="
