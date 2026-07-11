#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

django.setup()

from django.contrib.auth.models import User
from core.models import (
    Categoria, Nivel, Curso, Leccion, Evaluacion, 
    PreguntaEvaluacion, Juego, Partida, Progreso, 
    EstadisticasUsuario, ProgresoCurso, IntentoEvaluacion
)

print("📚 CARGANDO TODOS LOS DATOS DE MORPHOPLAY")
print("=" * 50)

# 1. Crear categorías
print("\n📂 Creando categorías...")
categorias = [
    ('Morfología', 'Estudio de la estructura de las palabras', 'fa-puzzle-piece'),
    ('Sintaxis', 'Estudio de la estructura de las oraciones', 'fa-sitemap'),
    ('Gramática', 'Reglas del lenguaje', 'fa-book'),
    ('Literatura', 'Técnicas literarias', 'fa-feather'),
    ('Inglés', 'Gramática inglesa', 'fa-language'),
    ('Bilingüe', 'Contenido bilingüe', 'fa-globe'),
]

for nombre, desc, icono in categorias:
    cat, created = Categoria.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc, 'icono': icono})
    print(f"  {'✅' if created else '⏳'} {nombre}")

# 2. Crear niveles
print("\n📊 Creando niveles...")
niveles = [
    ('Básico', 1, '#4caf50', 10),
    ('Intermedio', 2, '#ffa726', 15),
    ('Avanzado', 3, '#ef5350', 20),
    ('Experto', 4, '#ab47bc', 25),
]

for nombre, orden, color, puntos in niveles:
    niv, created = Nivel.objects.get_or_create(nombre=nombre, defaults={'orden': orden, 'color': color, 'puntos_base': puntos})
    print(f"  {'✅' if created else '⏳'} {nombre}")

# 3. Crear cursos
print("\n📚 Creando cursos...")
morfologia = Categoria.objects.get(nombre='Morfología')
sintaxis = Categoria.objects.get(nombre='Sintaxis')
ingles = Categoria.objects.get(nombre='Inglés')
bilingue = Categoria.objects.get(nombre='Bilingüe')
literatura = Categoria.objects.get(nombre='Literatura')
basico = Nivel.objects.get(nombre='Básico')
intermedio = Nivel.objects.get(nombre='Intermedio')
avanzado = Nivel.objects.get(nombre='Avanzado')

cursos_data = [
    {'titulo': 'Morfología del Castellano', 'desc': 'Curso completo sobre la estructura de las palabras.', 'cat': morfologia, 'nivel': basico, 'duracion': 10, 'orden': 1},
    {'titulo': 'Sintaxis del Castellano', 'desc': 'Curso completo sobre la estructura de las oraciones.', 'cat': sintaxis, 'nivel': intermedio, 'duracion': 12, 'orden': 2},
    {'titulo': 'English Grammar', 'desc': 'Curso completo de gramática inglesa.', 'cat': ingles, 'nivel': intermedio, 'duracion': 15, 'orden': 3},
    {'titulo': 'Cognados Español-Inglés', 'desc': 'Aprende palabras similares en español e inglés.', 'cat': bilingue, 'nivel': basico, 'duracion': 8, 'orden': 4},
    {'titulo': 'Técnicas Narrativas', 'desc': 'Explora técnicas literarias.', 'cat': literatura, 'nivel': avanzado, 'duracion': 14, 'orden': 5},
    {'titulo': 'Gramática Comparada', 'desc': 'Compara estructuras gramaticales.', 'cat': bilingue, 'nivel': avanzado, 'duracion': 16, 'orden': 6},
]

for data in cursos_data:
    curso, created = Curso.objects.get_or_create(
        titulo=data['titulo'],
        defaults={
            'descripcion': data['desc'],
            'categoria': data['cat'],
            'nivel': data['nivel'],
            'duracion_estimada': data['duracion'],
            'orden': data['orden'],
            'activo': True
        }
    )
    print(f"  {'✅' if created else '⏳'} {curso.titulo}")

# 4. Crear lecciones básicas
print("\n📖 Creando lecciones básicas...")
curso_morfologia = Curso.objects.get(titulo='Morfología del Castellano')
lecciones = [
    {'titulo': 'Introducción a la Morfología', 'contenido': 'La morfología estudia la estructura interna de las palabras.', 'orden': 1},
    {'titulo': 'Prefijos en Español', 'contenido': 'Los prefijos se añaden al INICIO de la palabra.', 'orden': 2},
    {'titulo': 'Sufijos en Español', 'contenido': 'Los sufijos se añaden al FINAL de la palabra.', 'orden': 3},
    {'titulo': 'Raíces y Formación', 'contenido': 'La raíz es el núcleo semántico.', 'orden': 4},
]

for lec in lecciones:
    l, created = Leccion.objects.get_or_create(
        curso=curso_morfologia,
        titulo=lec['titulo'],
        defaults={'contenido': lec['contenido'], 'orden': lec['orden']}
    )
    print(f"  {'✅' if created else '⏳'} {lec['titulo']}")

# 5. Crear juegos básicos
print("\n🎮 Creando juegos básicos...")
juegos_data = [
    {'titulo': 'Prefijos de Negación', 'cat': morfologia, 'opciones': ['in-', 'pre-', 'post-', 'sub-'], 'correcta': 'in-'},
    {'titulo': 'Sufijos de Profesión', 'cat': morfologia, 'opciones': ['-ero', '-ista', '-dor', '-ción'], 'correcta': '-ista'},
    {'titulo': 'Sujeto y Predicado', 'cat': sintaxis, 'opciones': ['El niño', 'come pan', 'pan', 'El'], 'correcta': 'El niño'},
    {'titulo': 'Present Simple', 'cat': ingles, 'opciones': ['go', 'goes', 'going', 'went'], 'correcta': 'go'},
    {'titulo': 'Cognados Perfectos', 'cat': bilingue, 'opciones': ['animal', 'animale', 'anima', 'animado'], 'correcta': 'animal'},
]

for data in juegos_data:
    juego, created = Juego.objects.get_or_create(
        titulo=data['titulo'],
        defaults={
            'descripcion': data['titulo'],
            'pregunta': f'¿Qué es {data["titulo"]}?',
            'categoria': data['cat'],
            'nivel': basico,
            'tipo': 'opcion',
            'opcion1': data['opciones'][0],
            'opcion2': data['opciones'][1],
            'opcion3': data['opciones'][2],
            'opcion4': data['opciones'][3],
            'respuesta_correcta': data['correcta'],
            'puntos': 10,
            'activo': True
        }
    )
    print(f"  {'✅' if created else '⏳'} {juego.titulo}")

# 6. Crear superusuario
print("\n👤 Creando superusuario...")
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@morphoplay.com', 'admin123')
    print("  ✅ admin creado")
else:
    print("  ⏳ admin ya existe")

# 7. Resumen final
print("\n" + "=" * 50)
print("✅ CARGA COMPLETA EXITOSA!")
print(f"📚 Cursos: {Curso.objects.count()}")
print(f"📖 Lecciones: {Leccion.objects.count()}")
print(f"🎮 Juegos: {Juego.objects.count()}")
print(f"📂 Categorías: {Categoria.objects.count()}")
print(f"📊 Niveles: {Nivel.objects.count()}")
print(f"👤 Usuarios: {User.objects.count()}")
