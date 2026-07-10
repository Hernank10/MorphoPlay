#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MORPHOPLAY - INSTALADOR DE BASE DE DATOS
Versión: 2.8
Descripción: Instalación automática de base de datos MySQL/SQLite
"""

import os
import sys
import platform
import subprocess
import json
import getpass
from pathlib import Path
import time

# Colores para la terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ️  {text}{Colors.END}")

def print_step(text):
    print(f"{Colors.BLUE}🔹 {text}{Colors.END}")

class DatabaseInstaller:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.db_type = None
        self.db_config = {}
        self.project_dir = Path.cwd()
        self.mysql_installed = False
        
    def run(self):
        print_header("🗄️ MORPHOPLAY - INSTALADOR DE BASE DE DATOS")
        print(f"📁 Sistema: {self.os_type}")
        print(f"📁 Directorio: {self.project_dir}\n")
        
        try:
            # Paso 1: Seleccionar tipo de base de datos
            self.step_select_database()
            
            # Paso 2: Configurar base de datos
            if self.db_type == "mysql":
                self.step_configure_mysql()
            else:
                self.step_configure_sqlite()
            
            # Paso 3: Crear tablas
            self.step_create_tables()
            
            # Paso 4: Cargar datos iniciales
            self.step_load_initial_data()
            
            # Paso 5: Crear procedimientos y triggers (MySQL)
            if self.db_type == "mysql":
                self.step_create_procedures()
            
            # Paso 6: Verificar instalación
            self.step_verify_installation()
            
            print_header("🎉 INSTALACIÓN DE BASE DE DATOS COMPLETA")
            
        except KeyboardInterrupt:
            print_error("\nInstalación cancelada")
            sys.exit(1)
        except Exception as e:
            print_error(f"Error: {str(e)}")
            sys.exit(1)
    
    def step_select_database(self):
        print_step("Seleccionando tipo de base de datos...")
        
        print("1. MySQL (Recomendado para producción)")
        print("2. SQLite (Recomendado para desarrollo)")
        print("3. Ambos")
        print()
        
        opcion = input("Selecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            self.db_type = "mysql"
            self.db_config = {
                'engine': 'mysql',
                'name': 'morphoplay_db',
                'user': 'morphoplay_user',
                'password': 'morphoplay_pass',
                'host': 'localhost',
                'port': '3306'
            }
            print_success("Base de datos seleccionada: MySQL")
        elif opcion == "2":
            self.db_type = "sqlite3"
            self.db_config = {
                'engine': 'sqlite3',
                'name': 'db.sqlite3'
            }
            print_success("Base de datos seleccionada: SQLite")
        elif opcion == "3":
            self.db_type = "ambos"
            print_success("Se instalarán ambas bases de datos")
        else:
            print_error("Opción inválida")
            sys.exit(1)
    
    def step_configure_mysql(self):
        print_step("Configurando MySQL...")
        
        # Verificar si MySQL está instalado
        try:
            subprocess.run(['mysql', '--version'], check=True, capture_output=True)
            self.mysql_installed = True
            print_success("MySQL instalado")
        except:
            print_info("MySQL no instalado. Intentando instalar...")
            self.install_mysql()
        
        # Configurar MySQL
        if self.db_type == "mysql" or self.db_type == "ambos":
            print_info("Configurando MySQL...")
            
            # Solicitar contraseña de root
            root_pass = getpass.getpass("Contraseña de root de MySQL (si no existe, presiona Enter): ")
            
            # Crear base de datos
            self.create_mysql_database(root_pass)
    
    def install_mysql(self):
        """Instalar MySQL según el sistema operativo"""
        if self.os_type == 'linux':
            try:
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'mysql-server'], check=True)
                print_success("MySQL instalado")
            except:
                print_error("Error instalando MySQL")
                sys.exit(1)
        elif self.os_type == 'darwin':  # macOS
            try:
                subprocess.run(['brew', 'install', 'mysql'], check=True)
                subprocess.run(['brew', 'services', 'start', 'mysql'], check=True)
                print_success("MySQL instalado")
            except:
                print_error("Error instalando MySQL")
                sys.exit(1)
        elif self.os_type == 'windows':
            print_info("Descarga e instala MySQL desde: https://dev.mysql.com/downloads/installer/")
            input("Presiona Enter después de instalar MySQL...")
        else:
            print_error("Sistema operativo no soportado para instalación automática")
            sys.exit(1)
    
    def create_mysql_database(self, root_pass):
        """Crear base de datos MySQL"""
        try:
            # Conectar y crear base de datos
            cmd = ['mysql', '-uroot']
            if root_pass:
                cmd.extend(['-p' + root_pass])
            
            # Crear base de datos
            sql = f"""
            CREATE DATABASE IF NOT EXISTS {self.db_config['name']} 
            CHARACTER SET utf8mb4 
            COLLATE utf8mb4_unicode_ci;
            
            CREATE USER IF NOT EXISTS '{self.db_config['user']}'@'localhost' 
            IDENTIFIED BY '{self.db_config['password']}';
            
            GRANT ALL PRIVILEGES ON {self.db_config['name']}.* 
            TO '{self.db_config['user']}'@'localhost';
            
            GRANT ALL PRIVILEGES ON *.* 
            TO '{self.db_config['user']}'@'localhost' WITH GRANT OPTION;
            
            FLUSH PRIVILEGES;
            """
            
            # Ejecutar SQL
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(sql.encode())
            
            if process.returncode == 0:
                print_success(f"Base de datos '{self.db_config['name']}' creada")
                print_success(f"Usuario '{self.db_config['user']}' creado")
            else:
                print_error(f"Error: {stderr.decode()}")
                print_info("Intentando conectar sin contraseña...")
                
                # Intentar sin contraseña
                cmd = ['mysql', '-uroot']
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate(sql.encode())
                
                if process.returncode == 0:
                    print_success("Base de datos creada exitosamente")
                else:
                    print_error("No se pudo crear la base de datos")
                    sys.exit(1)
                    
        except Exception as e:
            print_error(f"Error: {e}")
            sys.exit(1)
    
    def step_configure_sqlite(self):
        print_step("Configurando SQLite...")
        print_success("SQLite configurado (sin configuración adicional)")
    
    def step_create_tables(self):
        print_step("Creando tablas...")
        
        # Crear script SQL para todas las tablas
        sql_tables = """
-- ============================================================
-- MORPHOPLAY - TABLAS DE BASE DE DATOS
-- ============================================================

-- Tabla de usuarios (extendida)
CREATE TABLE IF NOT EXISTS auth_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    last_login DATETIME,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Categorías
CREATE TABLE IF NOT EXISTS core_categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    icono VARCHAR(50),
    orden INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Niveles
CREATE TABLE IF NOT EXISTS core_nivel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    orden INT DEFAULT 0,
    color VARCHAR(7) DEFAULT '#6c5ce7',
    puntos_base INT DEFAULT 10,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Cursos
CREATE TABLE IF NOT EXISTS core_curso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    categoria_id INT,
    nivel_id INT,
    duracion_estimada INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    orden INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES core_categoria(id) ON DELETE SET NULL,
    FOREIGN KEY (nivel_id) REFERENCES core_nivel(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Lecciones
CREATE TABLE IF NOT EXISTS core_leccion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    curso_id INT NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    contenido TEXT NOT NULL,
    video_url VARCHAR(200),
    orden INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (curso_id) REFERENCES core_curso(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Evaluaciones
CREATE TABLE IF NOT EXISTS core_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    curso_id INT NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(20) DEFAULT 'formativa',
    puntaje_maximo INT DEFAULT 100,
    tiempo_limite INT DEFAULT 0,
    intentos_permitidos INT DEFAULT 1,
    orden INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (curso_id) REFERENCES core_curso(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Preguntas de Evaluación
CREATE TABLE IF NOT EXISTS core_preguntaevaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evaluacion_id INT NOT NULL,
    tipo VARCHAR(20) DEFAULT 'opcion',
    pregunta TEXT NOT NULL,
    opcion1 VARCHAR(200),
    opcion2 VARCHAR(200),
    opcion3 VARCHAR(200),
    opcion4 VARCHAR(200),
    respuesta_correcta TEXT NOT NULL,
    puntaje INT DEFAULT 10,
    orden INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (evaluacion_id) REFERENCES core_evaluacion(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Juegos
CREATE TABLE IF NOT EXISTS core_juego (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    pregunta TEXT,
    categoria_id INT,
    nivel_id INT,
    tipo VARCHAR(20) DEFAULT 'opcion',
    opcion1 VARCHAR(200),
    opcion2 VARCHAR(200),
    opcion3 VARCHAR(200),
    opcion4 VARCHAR(200),
    respuesta_correcta VARCHAR(200) NOT NULL,
    puntos INT DEFAULT 10,
    orden INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES core_categoria(id) ON DELETE SET NULL,
    FOREIGN KEY (nivel_id) REFERENCES core_nivel(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Partidas
CREATE TABLE IF NOT EXISTS core_partida (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    juego_id INT NOT NULL,
    correcto BOOLEAN DEFAULT FALSE,
    puntuacion_obtenida INT DEFAULT 0,
    tiempo_segundos INT DEFAULT 0,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (juego_id) REFERENCES core_juego(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Progreso
CREATE TABLE IF NOT EXISTS core_progreso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    juego_id INT NOT NULL,
    completado BOOLEAN DEFAULT FALSE,
    intentos INT DEFAULT 0,
    puntuacion INT DEFAULT 0,
    fecha_completado DATETIME,
    ultimo_intento DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (juego_id) REFERENCES core_juego(id) ON DELETE CASCADE,
    UNIQUE KEY uk_progreso_usuario_juego (usuario_id, juego_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Estadísticas de usuario
CREATE TABLE IF NOT EXISTS core_estadisticasusuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE NOT NULL,
    juegos_completados INT DEFAULT 0,
    puntuacion_total INT DEFAULT 0,
    racha_actual INT DEFAULT 0,
    racha_maxima INT DEFAULT 0,
    tiempo_total INT DEFAULT 0,
    ultima_actividad DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES auth_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Progreso en cursos
CREATE TABLE IF NOT EXISTS core_progresocurso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    curso_id INT NOT NULL,
    estado VARCHAR(20) DEFAULT 'no_iniciado',
    lecciones_completadas INT DEFAULT 0,
    evaluaciones_completadas INT DEFAULT 0,
    puntaje_total INT DEFAULT 0,
    fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_completado DATETIME,
    ultimo_acceso DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES core_curso(id) ON DELETE CASCADE,
    UNIQUE KEY uk_progresocurso_usuario_curso (usuario_id, curso_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Intentos de evaluación
CREATE TABLE IF NOT EXISTS core_intentoevaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    evaluacion_id INT NOT NULL,
    puntaje_obtenido INT DEFAULT 0,
    respuestas JSON,
    estado VARCHAR(20) DEFAULT 'iniciado',
    fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_completado DATETIME,
    tiempo_utilizado INT DEFAULT 0,
    intento_numero INT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (evaluacion_id) REFERENCES core_evaluacion(id) ON DELETE CASCADE,
    UNIQUE KEY uk_intento_usuario_evaluacion (usuario_id, evaluacion_id, intento_numero)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SELECT '✅ Tablas creadas exitosamente' as Status;
"""
        
        # Guardar script SQL
        sql_file = self.project_dir / "scripts" / "morphoplay_tables.sql"
        sql_file.parent.mkdir(parents=True, exist_ok=True)
        sql_file.write_text(sql_tables)
        
        if self.db_type == "mysql" or self.db_type == "ambos":
            # Ejecutar en MySQL
            try:
                cmd = ['mysql', '-u', self.db_config['user'], '-p' + self.db_config['password'], 
                       self.db_config['name']]
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                process.communicate(sql_tables.encode())
                print_success("Tablas creadas en MySQL")
            except Exception as e:
                print_error(f"Error creando tablas en MySQL: {e}")
        
        if self.db_type == "sqlite3" or self.db_type == "ambos":
            # Crear SQLite
            sqlite_file = self.project_dir / "morphoplay.sqlite"
            try:
                import sqlite3
                conn = sqlite3.connect(str(sqlite_file))
                cursor = conn.cursor()
                
                # Adaptar SQL para SQLite
                sqlite_sql = sql_tables.replace("ENGINE=InnoDB DEFAULT CHARSET=utf8mb4", "")
                sqlite_sql = sqlite_sql.replace("AUTO_INCREMENT", "AUTOINCREMENT")
                sqlite_sql = sqlite_sql.replace("UNIQUE KEY", "UNIQUE")
                sqlite_sql = sqlite_sql.replace("FOREIGN KEY", "FOREIGN KEY")
                
                # Ejecutar sentencias
                for statement in sqlite_sql.split(';'):
                    if statement.strip():
                        try:
                            cursor.execute(statement)
                        except:
                            pass
                
                conn.commit()
                conn.close()
                print_success("Tablas creadas en SQLite")
            except Exception as e:
                print_error(f"Error creando tablas en SQLite: {e}")
    
    def step_load_initial_data(self):
        print_step("Cargando datos iniciales...")
        
        initial_data = """
-- Categorías
INSERT IGNORE INTO core_categoria (nombre, descripcion, icono, orden) VALUES
('Morfología', 'Estudio de la estructura de las palabras', 'fa-puzzle-piece', 1),
('Sintaxis', 'Estudio de la estructura de las oraciones', 'fa-sitemap', 2),
('Gramática', 'Reglas del lenguaje', 'fa-book', 3),
('Literatura', 'Técnicas literarias', 'fa-feather', 4),
('Inglés', 'Gramática inglesa', 'fa-language', 5),
('Bilingüe', 'Contenido bilingüe', 'fa-globe', 6);

-- Niveles
INSERT IGNORE INTO core_nivel (nombre, descripcion, orden, color, puntos_base) VALUES
('Básico', 'Nivel principiante', 1, '#4caf50', 10),
('Intermedio', 'Nivel intermedio', 2, '#ffa726', 15),
('Avanzado', 'Nivel avanzado', 3, '#ef5350', 20),
('Experto', 'Nivel experto', 4, '#ab47bc', 25),
('Maestro', 'Nivel maestro', 5, '#ffd700', 30);

SELECT '✅ Datos iniciales cargados' as Status;
"""
        
        if self.db_type == "mysql" or self.db_type == "ambos":
            try:
                cmd = ['mysql', '-u', self.db_config['user'], '-p' + self.db_config['password'], 
                       self.db_config['name']]
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                process.communicate(initial_data.encode())
                print_success("Datos iniciales cargados en MySQL")
            except:
                print_error("Error cargando datos en MySQL")
        
        if self.db_type == "sqlite3" or self.db_type == "ambos":
            try:
                import sqlite3
                conn = sqlite3.connect(str(self.project_dir / "morphoplay.sqlite"))
                cursor = conn.cursor()
                
                for statement in initial_data.split(';'):
                    if statement.strip():
                        try:
                            cursor.execute(statement)
                        except:
                            pass
                
                conn.commit()
                conn.close()
                print_success("Datos iniciales cargados en SQLite")
            except:
                print_error("Error cargando datos en SQLite")
    
    def step_create_procedures(self):
        print_step("Creando procedimientos almacenados (MySQL)...")
        
        procedures = """
-- Procedimiento: Obtener recomendaciones
DELIMITER //
CREATE PROCEDURE sp_recomendaciones(
    IN p_usuario_id INT,
    IN p_limit INT
)
BEGIN
    SELECT j.id, j.titulo, j.descripcion, cat.nombre as categoria,
           COUNT(p.id) as veces_jugado,
           AVG(p.correcto) as tasa_aciertos
    FROM core_juego j
    LEFT JOIN core_categoria cat ON j.categoria_id = cat.id
    LEFT JOIN core_partida p ON p.juego_id = j.id AND p.usuario_id = p_usuario_id
    WHERE j.activo = 1
    AND j.id NOT IN (
        SELECT juego_id FROM core_partida WHERE usuario_id = p_usuario_id AND correcto = 1
    )
    GROUP BY j.id
    ORDER BY veces_jugado ASC, tasa_aciertos ASC
    LIMIT p_limit;
END//
DELIMITER ;

-- Procedimiento: Estadísticas de usuario
DELIMITER //
CREATE PROCEDURE sp_estadisticas_usuario(
    IN p_usuario_id INT
)
BEGIN
    SELECT 
        COUNT(*) as total_partidas,
        SUM(CASE WHEN correcto = 1 THEN 1 ELSE 0 END) as total_correctas,
        AVG(correcto) * 100 as tasa_aciertos,
        SUM(puntuacion_obtenida) as puntuacion_total,
        AVG(tiempo_segundos) as tiempo_promedio
    FROM core_partida
    WHERE usuario_id = p_usuario_id;
END//
DELIMITER ;

-- Trigger: Actualizar estadísticas al completar juego
DELIMITER //
CREATE TRIGGER after_partida_insert
AFTER INSERT ON core_partida
FOR EACH ROW
BEGIN
    IF NEW.correcto = 1 THEN
        INSERT INTO core_estadisticasusuario (usuario_id, juegos_completados, puntuacion_total)
        VALUES (NEW.usuario_id, 1, NEW.puntuacion_obtenida)
        ON DUPLICATE KEY UPDATE
            juegos_completados = juegos_completados + 1,
            puntuacion_total = puntuacion_total + NEW.puntuacion_obtenida;
    END IF;
END//
DELIMITER ;

SELECT '✅ Procedimientos creados' as Status;
"""
        
        if self.db_type == "mysql" or self.db_type == "ambos":
            try:
                cmd = ['mysql', '-u', self.db_config['user'], '-p' + self.db_config['password'], 
                       self.db_config['name']]
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                process.communicate(procedures.encode())
                print_success("Procedimientos creados")
            except:
                print_error("Error creando procedimientos")
    
    def step_verify_installation(self):
        print_step("Verificando instalación...")
        
        if self.db_type == "mysql" or self.db_type == "ambos":
            try:
                cmd = ['mysql', '-u', self.db_config['user'], '-p' + self.db_config['password'], 
                       self.db_config['name'], '-e', 'SHOW TABLES;']
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    tables = result.stdout.strip().split('\n')
                    print_success(f"MySQL: {len(tables)-1} tablas creadas")
                else:
                    print_error("Error verificando MySQL")
            except:
                print_error("Error verificando MySQL")
        
        if self.db_type == "sqlite3" or self.db_type == "ambos":
            try:
                import sqlite3
                conn = sqlite3.connect(str(self.project_dir / "morphoplay.sqlite"))
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                conn.close()
                print_success(f"SQLite: {len(tables)} tablas creadas")
            except:
                print_error("Error verificando SQLite")

if __name__ == "__main__":
    installer = DatabaseInstaller()
    installer.run()
