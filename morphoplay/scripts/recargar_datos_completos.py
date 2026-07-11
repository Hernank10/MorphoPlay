#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import (
    Categoria, Nivel, Curso, Leccion, Juego, 
    Evaluacion, PreguntaEvaluacion, EstadisticasUsuario
)

def recargar_datos():
    print("🔄 RECARGANDO TODOS LOS DATOS DE MORPHOPLAY")
    print("=" * 60)
    
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
        cat, created = Categoria.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': desc, 'icono': icono}
        )
        print(f"  {'✅' if created else '⏳'} {nombre}")
    
    # 2. Crear niveles
    print("\n📊 Creando niveles...")
    niveles = [
        ('Básico', 1, '#4caf50', 10),
        ('Intermedio', 2, '#ffa726', 15),
        ('Avanzado', 3, '#ef5350', 20),
        ('Experto', 4, '#ab47bc', 25),
        ('Maestro', 5, '#ffd700', 30),
    ]
    
    for nombre, orden, color, puntos in niveles:
        niv, created = Nivel.objects.get_or_create(
            nombre=nombre,
            defaults={'orden': orden, 'color': color, 'puntos_base': puntos}
        )
        print(f"  {'✅' if created else '⏳'} {nombre}")
    
    # 3. Crear usuarios si no existen
    print("\n👤 Creando usuarios...")
    usuarios = [
        ('admin', 'admin@morphoplay.com', 'admin123', True, True),
        ('demo_user', 'demo@morphoplay.com', 'MorphoPlay2024!', False, False),
        ('alumno1', 'alumno1@test.com', 'Test12345!', False, False),
        ('alumno2', 'alumno2@test.com', 'Test12345!', False, False),
        ('alumno3', 'alumno3@test.com', 'Test12345!', False, False),
    ]
    
    for username, email, password, is_staff, is_superuser in usuarios:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, email, password)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
            EstadisticasUsuario.objects.create(usuario=user)
            print(f"  ✅ {username} creado")
        else:
            print(f"  ⏳ {username} ya existe")
    
    # 4. Crear cursos
    print("\n📚 Creando cursos...")
    morfologia = Categoria.objects.get(nombre='Morfología')
    sintaxis = Categoria.objects.get(nombre='Sintaxis')
    gramatica = Categoria.objects.get(nombre='Gramática')
    literatura = Categoria.objects.get(nombre='Literatura')
    ingles = Categoria.objects.get(nombre='Inglés')
    bilingue = Categoria.objects.get(nombre='Bilingüe')
    
    basico = Nivel.objects.get(nombre='Básico')
    intermedio = Nivel.objects.get(nombre='Intermedio')
    avanzado = Nivel.objects.get(nombre='Avanzado')
    experto = Nivel.objects.get(nombre='Experto')
    
    cursos_data = [
        {
            'titulo': 'Morfología del Castellano',
            'desc': 'Curso completo sobre la estructura de las palabras en español.',
            'cat': morfologia,
            'nivel': basico,
            'duracion': 10,
            'orden': 1
        },
        {
            'titulo': 'Sintaxis del Castellano',
            'desc': 'Curso completo sobre la estructura de las oraciones en español.',
            'cat': sintaxis,
            'nivel': intermedio,
            'duracion': 12,
            'orden': 2
        },
        {
            'titulo': 'English Grammar',
            'desc': 'Curso completo de gramática inglesa para hispanohablantes.',
            'cat': ingles,
            'nivel': intermedio,
            'duracion': 15,
            'orden': 3
        },
        {
            'titulo': 'Cognados Español-Inglés',
            'desc': 'Aprende palabras similares en español e inglés.',
            'cat': bilingue,
            'nivel': basico,
            'duracion': 8,
            'orden': 4
        },
        {
            'titulo': 'Técnicas Narrativas en Literatura',
            'desc': 'Explora las técnicas literarias de los grandes escritores.',
            'cat': literatura,
            'nivel': avanzado,
            'duracion': 14,
            'orden': 5
        },
        {
            'titulo': 'Gramática Comparada: Español vs Inglés',
            'desc': 'Compara las estructuras gramaticales del español y el inglés.',
            'cat': bilingue,
            'nivel': avanzado,
            'duracion': 16,
            'orden': 6
        }
    ]
    
    for data in cursos_data:
        curso, created = Curso.objects.get_or_create(
            titulo=data['titulo'],
            defaults={
                'descripcion': data['desc'],
                'categoria': data['cat'],
                'nivel': data['nivel'],
                'duracion_estimada': data['duracion'],
                'orden': data['orden']
            }
        )
        print(f"  {'✅' if created else '⏳'} {curso.titulo}")
    
    # 5. Crear lecciones para el primer curso
    print("\n📖 Creando lecciones...")
    curso_morfologia = Curso.objects.get(titulo='Morfología del Castellano')
    
    lecciones = [
        {"titulo": "Introducción a la Morfología", "contenido": "La morfología estudia la estructura interna de las palabras.", "orden": 1},
        {"titulo": "Prefijos en Español", "contenido": "Los prefijos se añaden al INICIO de la palabra. Ej: in-, sub-, pre-", "orden": 2},
        {"titulo": "Sufijos en Español", "contenido": "Los sufijos se añaden al FINAL de la palabra. Ej: -ito, -ero, -ción", "orden": 3},
        {"titulo": "Raíces y Formación de Palabras", "contenido": "La raíz es el núcleo semántico. Procesos: derivación, composición.", "orden": 4},
    ]
    
    for lec in lecciones:
        leccion, created = Leccion.objects.get_or_create(
            curso=curso_morfologia,
            titulo=lec["titulo"],
            defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
        )
        print(f"  {'✅' if created else '⏳'} {lec['titulo']}")
    
    # 6. Crear juegos
    print("\n🎮 Creando juegos...")
    juegos_data = [
        {
            'titulo': 'Prefijos de Negación',
            'desc': 'Elige el prefijo que indica negación o ausencia',
            'pregunta': '¿Qué prefijo significa "no" o "sin"?',
            'cat': morfologia,
            'nivel': basico,
            'opciones': ['in-', 'pre-', 'post-', 'sub-'],
            'correcta': 'in-',
            'puntos': 10,
            'orden': 1
        },
        {
            'titulo': 'Sufijos de Profesión',
            'desc': 'Identifica el sufijo que forma profesiones',
            'pregunta': '¿Qué sufijo forma profesiones como "maestro"?',
            'cat': morfologia,
            'nivel': basico,
            'opciones': ['-ero', '-ista', '-dor', '-ción'],
            'correcta': '-ista',
            'puntos': 10,
            'orden': 2
        },
        {
            'titulo': 'Diminutivos en Español',
            'desc': 'Elige el diminutivo correcto',
            'pregunta': '¿Cuál es el diminutivo de "casa"?',
            'cat': morfologia,
            'nivel': basico,
            'opciones': ['casota', 'casita', 'casona', 'casaza'],
            'correcta': 'casita',
            'puntos': 10,
            'orden': 3
        },
        {
            'titulo': 'Sujeto y Predicado',
            'desc': 'Identifica el sujeto de la oración',
            'pregunta': 'En "El niño come pan", ¿cuál es el sujeto?',
            'cat': sintaxis,
            'nivel': basico,
            'opciones': ['El niño', 'come pan', 'pan', 'El'],
            'correcta': 'El niño',
            'puntos': 10,
            'orden': 4
        },
        {
            'titulo': 'Complemento Directo',
            'desc': 'Identifica el complemento directo',
            'pregunta': 'En "Veo la casa", ¿cuál es el CD?',
            'cat': sintaxis,
            'nivel': intermedio,
            'opciones': ['Veo', 'la casa', 'casa', 'la'],
            'correcta': 'la casa',
            'puntos': 15,
            'orden': 5
        },
        {
            'titulo': 'Present Simple',
            'desc': 'Elige la forma correcta del presente simple',
            'pregunta': 'I ___ to school every day.',
            'cat': ingles,
            'nivel': basico,
            'opciones': ['go', 'goes', 'going', 'went'],
            'correcta': 'go',
            'puntos': 10,
            'orden': 6
        },
        {
            'titulo': 'Cognados Perfectos',
            'desc': 'Encuentra el cognado perfecto',
            'pregunta': '¿Cuál es el cognado de "animal" en español?',
            'cat': bilingue,
            'nivel': basico,
            'opciones': ['animal', 'animale', 'anima', 'animado'],
            'correcta': 'animal',
            'puntos': 10,
            'orden': 7
        }
    ]
    
    for data in juegos_data:
        juego, created = Juego.objects.get_or_create(
            titulo=data['titulo'],
            defaults={
                'descripcion': data['desc'],
                'pregunta': data['pregunta'],
                'categoria': data['cat'],
                'nivel': data['nivel'],
                'tipo': 'opcion',
                'opcion1': data['opciones'][0],
                'opcion2': data['opciones'][1],
                'opcion3': data['opciones'][2],
                'opcion4': data['opciones'][3],
                'respuesta_correcta': data['correcta'],
                'puntos': data['puntos'],
                'orden': data['orden']
            }
        )
        print(f"  {'✅' if created else '⏳'} {juego.titulo}")
    
    # 7. Crear evaluaciones
    print("\n📝 Creando evaluaciones...")
    
    eval1, created = Evaluacion.objects.get_or_create(
        curso=curso_morfologia,
        titulo='Evaluación de Morfología',
        defaults={
            'descripcion': 'Pon a prueba tus conocimientos sobre morfología',
            'tipo': 'sumativa',
            'puntaje_maximo': 100,
            'tiempo_limite': 30,
            'intentos_permitidos': 2,
            'orden': 1
        }
    )
    print(f"  {'✅' if created else '⏳'} {eval1.titulo}")
    
    if created:
        preguntas = [
            {'p': '¿Qué es un prefijo?', 'opciones': ['Partícula al inicio', 'Partícula al final', 'Raíz', 'Lexema'], 'correcta': 'Partícula al inicio', 'pts': 10},
            {'p': 'Ejemplo de prefijo:', 'opciones': ['-ito', 'pre-', '-ción', '-mente'], 'correcta': 'pre-', 'pts': 10},
            {'p': '¿Qué sufijo forma diminutivos?', 'opciones': ['-azo', '-ito', '-ción', '-mente'], 'correcta': '-ito', 'pts': 10},
            {'p': 'En "submarino", "sub-" significa:', 'opciones': ['sobre', 'debajo', 'dentro', 'fuera'], 'correcta': 'debajo', 'pts': 10},
            {'p': '¿Qué sufijo forma profesiones?', 'opciones': ['-ción', '-ista', '-mente', '-dad'], 'correcta': '-ista', 'pts': 10},
        ]
        for i, p in enumerate(preguntas, 1):
            PreguntaEvaluacion.objects.create(
                evaluacion=eval1,
                tipo='opcion',
                pregunta=p['p'],
                opcion1=p['opciones'][0],
                opcion2=p['opciones'][1],
                opcion3=p['opciones'][2],
                opcion4=p['opciones'][3],
                respuesta_correcta=p['correcta'],
                puntaje=p['pts'],
                orden=i
            )
        print(f"    ✅ {len(preguntas)} preguntas creadas")
    
    print("\n" + "=" * 60)
    print("✅ TODOS LOS DATOS RECARGADOS EXITOSAMENTE!")
    print(f"📚 Cursos: {Curso.objects.count()}")
    print(f"📖 Lecciones: {Leccion.objects.count()}")
    print(f"🎮 Juegos: {Juego.objects.count()}")
    print(f"📝 Evaluaciones: {Evaluacion.objects.count()}")
    print(f"👤 Usuarios: {User.objects.count()}")

if __name__ == "__main__":
    recargar_datos()
