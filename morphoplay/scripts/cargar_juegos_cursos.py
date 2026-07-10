#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Categoria, Nivel, Juego, Curso, Leccion, Evaluacion, PreguntaEvaluacion

def cargar_datos():
    print("📚 Cargando datos iniciales...")
    print("=" * 40)
    
    # 1. Crear categorías si no existen
    categorias = [
        ('Morfología', 'Estudio de la estructura de las palabras', 'fa-puzzle-piece'),
        ('Sintaxis', 'Estudio de la estructura de las oraciones', 'fa-sitemap'),
        ('Gramática', 'Reglas del lenguaje', 'fa-book'),
        ('Literatura', 'Técnicas literarias', 'fa-feather'),
        ('Inglés', 'Gramática inglesa', 'fa-language'),
        ('Bilingüe', 'Contenido bilingüe español-inglés', 'fa-globe'),
    ]
    
    for nombre, desc, icono in categorias:
        cat, created = Categoria.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': desc, 'icono': icono}
        )
        if created:
            print(f"  ✅ Categoría creada: {nombre}")
    
    # 2. Crear niveles si no existen
    niveles = [
        ('Básico', 1, '#4caf50', 10),
        ('Intermedio', 2, '#ffa726', 15),
        ('Avanzado', 3, '#ef5350', 20),
        ('Experto', 4, '#ab47bc', 25),
    ]
    
    for nombre, orden, color, puntos in niveles:
        niv, created = Nivel.objects.get_or_create(
            nombre=nombre,
            defaults={'orden': orden, 'color': color, 'puntos_base': puntos}
        )
        if created:
            print(f"  ✅ Nivel creado: {nombre}")
    
    # 3. Crear juegos
    morfologia = Categoria.objects.get(nombre='Morfología')
    sintaxis = Categoria.objects.get(nombre='Sintaxis')
    ingles = Categoria.objects.get(nombre='Inglés')
    bilingue = Categoria.objects.get(nombre='Bilingüe')
    basico = Nivel.objects.get(nombre='Básico')
    intermedio = Nivel.objects.get(nombre='Intermedio')
    avanzado = Nivel.objects.get(nombre='Avanzado')
    
    juegos_data = [
        {
            "titulo": "Prefijos de Negación",
            "desc": "Elige el prefijo que indica negación o ausencia",
            "pregunta": "¿Qué prefijo significa 'no' o 'sin'?",
            "cat": morfologia,
            "nivel": basico,
            "opciones": ["in-", "pre-", "post-", "sub-"],
            "correcta": "in-",
            "puntos": 10,
            "orden": 1
        },
        {
            "titulo": "Sufijos de Profesión",
            "desc": "Identifica el sufijo que forma profesiones",
            "pregunta": "¿Qué sufijo forma profesiones como 'maestro'?",
            "cat": morfologia,
            "nivel": basico,
            "opciones": ["-ero", "-ista", "-dor", "-ción"],
            "correcta": "-ista",
            "puntos": 10,
            "orden": 2
        },
        {
            "titulo": "Diminutivos en Español",
            "desc": "Elige el diminutivo correcto",
            "pregunta": "¿Cuál es el diminutivo de 'casa'?",
            "cat": morfologia,
            "nivel": basico,
            "opciones": ["casota", "casita", "casona", "casaza"],
            "correcta": "casita",
            "puntos": 10,
            "orden": 3
        },
        {
            "titulo": "Sujeto y Predicado",
            "desc": "Identifica el sujeto de la oración",
            "pregunta": "En 'El niño come pan', ¿cuál es el sujeto?",
            "cat": sintaxis,
            "nivel": basico,
            "opciones": ["El niño", "come pan", "pan", "El"],
            "correcta": "El niño",
            "puntos": 10,
            "orden": 4
        },
        {
            "titulo": "Complemento Directo",
            "desc": "Identifica el complemento directo",
            "pregunta": "En 'Veo la casa', ¿cuál es el CD?",
            "cat": sintaxis,
            "nivel": intermedio,
            "opciones": ["Veo", "la casa", "casa", "la"],
            "correcta": "la casa",
            "puntos": 15,
            "orden": 5
        },
        {
            "titulo": "Present Simple",
            "desc": "Elige la forma correcta del presente simple",
            "pregunta": "I ___ to school every day.",
            "cat": ingles,
            "nivel": basico,
            "opciones": ["go", "goes", "going", "went"],
            "correcta": "go",
            "puntos": 10,
            "orden": 6
        },
        {
            "titulo": "Cognados Perfectos",
            "desc": "Encuentra el cognado perfecto",
            "pregunta": "¿Cuál es el cognado de 'animal' en español?",
            "cat": bilingue,
            "nivel": basico,
            "opciones": ["animal", "animale", "anima", "animado"],
            "correcta": "animal",
            "puntos": 10,
            "orden": 7
        },
        {
            "titulo": "Falsos Amigos",
            "desc": "¡Cuidado con los falsos amigos!",
            "pregunta": "¿Qué significa 'embarrassed' en español?",
            "cat": bilingue,
            "nivel": intermedio,
            "opciones": ["embarazada", "avergonzado", "empezado", "embrujado"],
            "correcta": "avergonzado",
            "puntos": 15,
            "orden": 8
        }
    ]
    
    creados = 0
    for data in juegos_data:
        juego, created = Juego.objects.get_or_create(
            titulo=data["titulo"],
            defaults={
                "descripcion": data["desc"],
                "pregunta": data["pregunta"],
                "categoria": data["cat"],
                "nivel": data["nivel"],
                "tipo": "opcion",
                "opcion1": data["opciones"][0],
                "opcion2": data["opciones"][1],
                "opcion3": data["opciones"][2],
                "opcion4": data["opciones"][3],
                "respuesta_correcta": data["correcta"],
                "puntos": data["puntos"],
                "orden": data["orden"]
            }
        )
        if created:
            creados += 1
            print(f"  ✅ Juego creado: {data['titulo']}")
    
    print("=" * 40)
    print(f"✅ {creados} juegos cargados")
    print(f"📊 Total juegos: {Juego.objects.count()}")
    print(f"📚 Categorías: {Categoria.objects.count()}")
    print(f"📊 Niveles: {Nivel.objects.count()}")

if __name__ == "__main__":
    cargar_datos()
