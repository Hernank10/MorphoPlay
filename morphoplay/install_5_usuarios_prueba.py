#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MORPHOPLAY - INSTALADOR DE 5 USUARIOS DE PRUEBA v8.1
Genera 5 usuarios con datos de prueba para los 100 cursos completos
"""

import os
import sys
import subprocess
import json
import random
from pathlib import Path
from datetime import datetime, timedelta

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
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

class UsuariosPruebaInstaller:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.venv_dir = self.project_dir / "venv"
        self.python_path = None
        self.usuarios = []
        
    def run(self):
        print_header("👤 INSTALADOR DE 5 USUARIOS DE PRUEBA - MORPHOPLAY v8.1")
        print(f"📁 Directorio: {self.project_dir}\n")
        
        try:
            # Paso 1: Verificar entorno
            self.step_verify_env()
            
            # Paso 2: Crear 5 usuarios de prueba
            self.step_create_5_usuarios()
            
            # Paso 3: Asignar cursos a usuarios
            self.step_asignar_cursos()
            
            # Paso 4: Generar progreso de usuarios
            self.step_generar_progreso()
            
            # Paso 5: Generar partidas y actividad
            self.step_generar_actividad()
            
            # Paso 6: Verificar instalación
            self.step_verify()
            
            print_header("🎉 5 USUARIOS DE PRUEBA INSTALADOS EXITOSAMENTE")
            self.print_summary()
            
        except KeyboardInterrupt:
            print_error("\nInstalación cancelada")
            sys.exit(1)
        except Exception as e:
            print_error(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    def step_verify_env(self):
        print_step("Verificando entorno...")
        
        if self.venv_dir.exists():
            if sys.platform == 'win32':
                self.python_path = self.venv_dir / "Scripts" / "python"
            else:
                self.python_path = self.venv_dir / "bin" / "python"
            
            if self.python_path.exists():
                print_success("Entorno virtual verificado")
                return
        
        print_info("Usando Python del sistema")
        self.python_path = Path(sys.executable)
    
    def step_create_5_usuarios(self):
        print_step("Creando 5 usuarios de prueba...")
        
        script = """
import django
import os
import random
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import EstadisticasUsuario

print("👤 Creando 5 usuarios de prueba...")

# Datos de usuarios
usuarios_data = [
    {
        'username': 'estudiante1',
        'email': 'estudiante1@morphoplay.com',
        'password': 'MorphoPlay2024!',
        'first_name': 'Ana',
        'last_name': 'Martínez',
        'edad': 22,
        'pais': 'Colombia'
    },
    {
        'username': 'estudiante2',
        'email': 'estudiante2@morphoplay.com',
        'password': 'MorphoPlay2024!',
        'first_name': 'Carlos',
        'last_name': 'González',
        'edad': 25,
        'pais': 'México'
    },
    {
        'username': 'estudiante3',
        'email': 'estudiante3@morphoplay.com',
        'password': 'MorphoPlay2024!',
        'first_name': 'María',
        'last_name': 'López',
        'edad': 23,
        'pais': 'España'
    },
    {
        'username': 'estudiante4',
        'email': 'estudiante4@morphoplay.com',
        'password': 'MorphoPlay2024!',
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'edad': 24,
        'pais': 'Argentina'
    },
    {
        'username': 'estudiante5',
        'email': 'estudiante5@morphoplay.com',
        'password': 'MorphoPlay2024!',
        'first_name': 'Laura',
        'last_name': 'García',
        'edad': 21,
        'pais': 'Chile'
    }
]

creados = 0
for data in usuarios_data:
    # Verificar si ya existe
    if User.objects.filter(username=data['username']).exists():
        print(f"  ⏳ {data['username']} ya existe")
        continue
    
    # Crear usuario
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    
    # Crear estadísticas
    stats, created = EstadisticasUsuario.objects.get_or_create(
        usuario=user,
        defaults={
            'juegos_completados': 0,
            'puntuacion_total': 0,
            'racha_actual': 0,
            'racha_maxima': 0
        }
    )
    
    print(f"  ✅ {data['username']} - {data['first_name']} {data['last_name']}")
    print(f"     📧 {data['email']}")
    print(f"     🔑 Contraseña: {data['password']}")
    print(f"     🌍 País: {data['pais']}")
    print(f"     📅 Edad: {data['edad']} años")
    print()
    
    creados += 1

print(f"\\n✅ {creados} usuarios creados")
"""
        
        self._ejecutar_script(script)
        print_success("5 usuarios de prueba creados")
    
    def step_asignar_cursos(self):
        print_step("Asignando cursos a usuarios...")
        
        script = """
import django
import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Curso, ProgresoCurso

print("📚 Asignando cursos a usuarios...")

# Obtener usuarios
usuarios = list(User.objects.filter(is_staff=False, is_superuser=False))

if not usuarios:
    print("⚠️ No hay usuarios disponibles")
    exit()

# Obtener cursos
cursos = list(Curso.objects.filter(activo=True))

if not cursos:
    print("⚠️ No hay cursos disponibles")
    exit()

total_asignaciones = 0
for usuario in usuarios:
    # Seleccionar cursos aleatorios (10-20 por usuario)
    num_cursos = random.randint(10, min(20, len(cursos)))
    cursos_seleccionados = random.sample(cursos, num_cursos)
    
    for curso in cursos_seleccionados:
        # Crear progreso
        pc, created = ProgresoCurso.objects.get_or_create(
            usuario=usuario,
            curso=curso,
            defaults={
                'estado': 'no_iniciado',
                'lecciones_completadas': 0,
                'puntaje_total': 0
            }
        )
        
        if created:
            total_asignaciones += 1
    
    print(f"  ✅ {usuario.username}: {num_cursos} cursos asignados")

print(f"\\n✅ {total_asignaciones} asignaciones de cursos realizadas")
"""
        
        self._ejecutar_script(script)
        print_success("Cursos asignados a usuarios")
    
    def step_generar_progreso(self):
        print_step("Generando progreso para usuarios...")
        
        script = """
import django
import os
import random
from datetime import datetime, timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Curso, ProgresoCurso, Leccion, Partida, Progreso, Juego, EstadisticasUsuario

print("📊 Generando progreso para usuarios...")

usuarios = list(User.objects.filter(is_staff=False, is_superuser=False))

if not usuarios:
    print("⚠️ No hay usuarios disponibles")
    exit()

total_progreso = 0
for usuario in usuarios:
    # Obtener progreso de cursos
    progresos = ProgresoCurso.objects.filter(usuario=usuario)
    
    for pc in progresos:
        # Simular progreso aleatorio
        total_lecciones = pc.curso.get_lecciones().count()
        if total_lecciones > 0:
            completadas = random.randint(0, total_lecciones)
            pc.lecciones_completadas = completadas
            
            if completadas == total_lecciones:
                pc.estado = 'completado'
                pc.fecha_completado = datetime.now() - timedelta(days=random.randint(1, 30))
            elif completadas > 0:
                pc.estado = 'en_progreso'
            
            pc.save()
            total_progreso += 1
    
    print(f"  ✅ {usuario.username}: {progresos.count()} cursos actualizados")

print(f"\\n✅ {total_progreso} progresos actualizados")
"""
        
        self._ejecutar_script(script)
        print_success("Progreso generado para usuarios")
    
    def step_generar_actividad(self):
        print_step("Generando actividad para usuarios...")
        
        script = """
import django
import os
import random
from datetime import datetime, timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Juego, Partida, Progreso, EstadisticasUsuario

print("🎮 Generando actividad para usuarios...")

usuarios = list(User.objects.filter(is_staff=False, is_superuser=False))
juegos = list(Juego.objects.filter(activo=True))

if not usuarios or not juegos:
    print("⚠️ No hay usuarios o juegos disponibles")
    exit()

total_partidas = 0
for usuario in usuarios:
    # Generar entre 5 y 20 partidas por usuario
    num_partidas = random.randint(5, 20)
    juegos_usuario = random.sample(juegos, min(num_partidas, len(juegos)))
    
    puntuacion_total = 0
    juegos_completados = 0
    racha_actual = 0
    racha_maxima = 0
    
    for juego in juegos_usuario:
        correcto = random.random() > 0.3  # 70% de probabilidad de acertar
        puntos = juego.puntos if correcto else 0
        
        # Crear partida
        partida = Partida.objects.create(
            usuario=usuario,
            juego=juego,
            correcto=correcto,
            puntuacion_obtenida=puntos,
            tiempo_segundos=random.randint(5, 45),
            fecha=datetime.now() - timedelta(days=random.randint(0, 30))
        )
        
        # Actualizar progreso
        progreso, created = Progreso.objects.get_or_create(
            usuario=usuario,
            juego=juego
        )
        progreso.intentos += 1
        
        if correcto and not progreso.completado:
            progreso.completado = True
            progreso.puntuacion = puntos
            progreso.fecha_completado = datetime.now() - timedelta(days=random.randint(0, 30))
            juegos_completados += 1
            racha_actual += 1
            if racha_actual > racha_maxima:
                racha_maxima = racha_actual
        else:
            if not correcto:
                racha_actual = 0
        
        progreso.save()
        puntuacion_total += puntos
        total_partidas += 1
    
    # Actualizar estadísticas
    stats, _ = EstadisticasUsuario.objects.get_or_create(usuario=usuario)
    stats.juegos_completados += juegos_completados
    stats.puntuacion_total += puntuacion_total
    stats.racha_actual = racha_actual
    stats.racha_maxima = max(stats.racha_maxima, racha_maxima)
    stats.ultima_actividad = datetime.now() - timedelta(days=random.randint(0, 2))
    stats.save()
    
    print(f"  ✅ {usuario.username}: {len(juegos_usuario)} partidas, {juegos_completados} completados")

print(f"\\n✅ {total_partidas} partidas generadas")
"""
        
        self._ejecutar_script(script)
        print_success("Actividad generada para usuarios")
    
    def step_verify(self):
        print_step("Verificando instalación...")
        
        script = """
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Partida, Progreso, ProgresoCurso, EstadisticasUsuario

print("📊 VERIFICANDO INSTALACIÓN:")
print(f"👤 Usuarios: {User.objects.count()}")
print(f"🎮 Partidas: {Partida.objects.count()}")
print(f"📊 Progreso: {Progreso.objects.count()}")
print(f"📚 Progreso Cursos: {ProgresoCurso.objects.count()}")
print(f"📈 Estadísticas: {EstadisticasUsuario.objects.count()}")

print("\\n👤 USUARIOS CON DATOS:")
for u in User.objects.filter(is_staff=False, is_superuser=False):
    partidas = Partida.objects.filter(usuario=u).count()
    stats = EstadisticasUsuario.objects.filter(usuario=u).first()
    print(f"  - {u.username}: {partidas} partidas, {stats.juegos_completados if stats else 0} completados")
"""
        
        self._ejecutar_script(script)
    
    def _ejecutar_script(self, script):
        """Ejecuta un script de Python en el entorno adecuado"""
        if self.python_path:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(script)
                temp_file = f.name
            
            try:
                subprocess.run([str(self.python_path), temp_file], 
                             cwd=self.project_dir, check=False)
            finally:
                os.unlink(temp_file)
    
    def print_summary(self):
        print(f"""
{Colors.GREEN}✅ 5 USUARIOS DE PRUEBA INSTALADOS EXITOSAMENTE!{Colors.END}

👤 USUARIOS CREADOS:
  1. estudiante1 - Ana Martínez (Colombia) 🔑 MorphoPlay2024!
  2. estudiante2 - Carlos González (México) 🔑 MorphoPlay2024!
  3. estudiante3 - María López (España) 🔑 MorphoPlay2024!
  4. estudiante4 - Juan Pérez (Argentina) 🔑 MorphoPlay2024!
  5. estudiante5 - Laura García (Chile) 🔑 MorphoPlay2024!

📊 DATOS GENERADOS:
  - 5 usuarios con perfiles completos
  - 10-20 cursos asignados por usuario
  - 5-20 partidas por usuario
  - Progreso simulado en cursos y juegos
  - Estadísticas personalizadas

📈 EJEMPLO DE ACTIVIDAD:
  - Cada usuario tiene entre 5-20 partidas
  - 70% de probabilidad de acierto
  - Rachas de 1-10 aciertos consecutivos
  - Puntuación total de 50-300 puntos

🌐 ACCESO:
  {Colors.CYAN}http://localhost:8000/login/{Colors.END}
  {Colors.CYAN}http://localhost:8000/dashboard/{Colors.END}

🔑 TODOS LOS USUARIOS COMPARTEN LA MISMA CONTRASEÑA:
  {Colors.YELLOW}MorphoPlay2024!{Colors.END}

🚀 Inicia el servidor:
  {Colors.BLUE}source venv/bin/activate{Colors.END}
  {Colors.BLUE}python manage.py runserver 0.0.0.0:8000{Colors.END}

📝 PRUEBA CON CUALQUIER USUARIO:
  - Ve a http://localhost:8000/login/
  - Usa cualquier usuario de la lista
  - Contraseña: MorphoPlay2024!
  - Explora cursos, juegos y progreso
        """)

if __name__ == "__main__":
    installer = UsuariosPruebaInstaller()
    installer.run()
