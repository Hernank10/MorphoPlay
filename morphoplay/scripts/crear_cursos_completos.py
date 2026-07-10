#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Categoria, Nivel, Leccion, Evaluacion, PreguntaEvaluacion

def crear_cursos_completos():
    print("📚 Creando cursos completos con lecciones y evaluaciones...")
    print("=" * 60)
    
    try:
        morfologia = Categoria.objects.get(nombre="Morfología")
        sintaxis = Categoria.objects.get(nombre="Sintaxis")
        gramatica = Categoria.objects.get(nombre="Gramática")
        literatura = Categoria.objects.get(nombre="Literatura")
        ingles = Categoria.objects.get(nombre="Inglés")
        bilingue = Categoria.objects.get(nombre="Bilingüe")
        
        basico = Nivel.objects.get(nombre="Básico")
        intermedio = Nivel.objects.get(nombre="Intermedio")
        avanzado = Nivel.objects.get(nombre="Avanzado")
        experto = Nivel.objects.get(nombre="Experto")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # ============================================================
    # CURSO 1: MORFOLOGÍA DEL CASTELLANO
    # ============================================================
    curso1, created = Curso.objects.get_or_create(
        titulo="Morfología del Castellano",
        defaults={
            "descripcion": "Curso completo sobre la estructura de las palabras en español.",
            "categoria": morfologia,
            "nivel": basico,
            "duracion_estimada": 12,
            "orden": 1
        }
    )
    
    if created:
        print(f"  ✅ Curso creado: {curso1.titulo}")
        
        lecciones = [
            {"titulo": "Introducción a la Morfología", "contenido": "La morfología estudia la estructura interna de las palabras.", "orden": 1},
            {"titulo": "Prefijos en Español", "contenido": "Los prefijos se añaden al INICIO de la palabra. Ej: in-, sub-, pre-", "orden": 2},
            {"titulo": "Sufijos en Español", "contenido": "Los sufijos se añaden al FINAL de la palabra. Ej: -ito, -ero, -ción", "orden": 3},
            {"titulo": "Raíces y Formación de Palabras", "contenido": "La raíz es el núcleo semántico. Procesos: derivación, composición.", "orden": 4}
        ]
        
        for lec in lecciones:
            Leccion.objects.get_or_create(
                curso=curso1,
                titulo=lec["titulo"],
                defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
            )
        
        # Evaluación
        eval1 = Evaluacion.objects.create(
            curso=curso1,
            titulo="Evaluación de Morfología",
            descripcion="Pon a prueba tus conocimientos sobre morfología",
            tipo="sumativa",
            puntaje_maximo=100,
            tiempo_limite=30,
            intentos_permitidos=2
        )
        
        preguntas = [
            {"p": "¿Qué es un prefijo?", "opciones": ["Partícula al inicio", "Partícula al final", "Raíz", "Lexema"], "correcta": "Partícula al inicio", "pts": 10},
            {"p": "Ejemplo de prefijo:", "opciones": ["-ito", "pre-", "-ción", "-mente"], "correcta": "pre-", "pts": 10},
            {"p": "¿Qué sufijo forma diminutivos?", "opciones": ["-azo", "-ito", "-ción", "-mente"], "correcta": "-ito", "pts": 10},
            {"p": "En 'submarino', 'sub-' significa:", "opciones": ["sobre", "debajo", "dentro", "fuera"], "correcta": "debajo", "pts": 10},
            {"p": "¿Qué sufijo forma profesiones?", "opciones": ["-ción", "-ista", "-mente", "-dad"], "correcta": "-ista", "pts": 10},
        ]
        
        for i, p in enumerate(preguntas, 1):
            PreguntaEvaluacion.objects.create(
                evaluacion=eval1,
                tipo="opcion",
                pregunta=p["p"],
                opcion1=p["opciones"][0],
                opcion2=p["opciones"][1],
                opcion3=p["opciones"][2],
                opcion4=p["opciones"][3],
                respuesta_correcta=p["correcta"],
                puntaje=p["pts"],
                orden=i
            )
    
    # ============================================================
    # CURSO 2: SINTAXIS DEL CASTELLANO
    # ============================================================
    curso2, created = Curso.objects.get_or_create(
        titulo="Sintaxis del Castellano",
        defaults={
            "descripcion": "Curso completo sobre la estructura de las oraciones en español.",
            "categoria": sintaxis,
            "nivel": intermedio,
            "duracion_estimada": 14,
            "orden": 2
        }
    )
    
    if created:
        print(f"  ✅ Curso creado: {curso2.titulo}")
        
        lecciones = [
            {"titulo": "La Oración y sus Partes", "contenido": "La oración tiene SUJETO y PREDICADO.", "orden": 1},
            {"titulo": "El Sujeto", "contenido": "Tipos: expreso, elíptico, simple, compuesto.", "orden": 2},
            {"titulo": "El Predicado", "contenido": "Tipos: verbal y nominal. Complementos: CD, CI, CC.", "orden": 3},
            {"titulo": "Análisis Sintáctico", "contenido": "Pasos: identificar verbo, sujeto y complementos.", "orden": 4}
        ]
        
        for lec in lecciones:
            Leccion.objects.get_or_create(
                curso=curso2,
                titulo=lec["titulo"],
                defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
            )
        
        eval2 = Evaluacion.objects.create(
            curso=curso2,
            titulo="Evaluación de Sintaxis",
            descripcion="Pon a prueba tus conocimientos sobre sintaxis",
            tipo="sumativa",
            puntaje_maximo=100,
            tiempo_limite=30,
            intentos_permitidos=2
        )
        
        preguntas = [
            {"p": "¿Qué es el sujeto?", "opciones": ["Quien realiza la acción", "Lo que se dice del verbo", "El núcleo del predicado", "El complemento"], "correcta": "Quien realiza la acción", "pts": 10},
            {"p": "En 'El niño come pan', el sujeto es:", "opciones": ["El niño", "come pan", "pan", "El"], "correcta": "El niño", "pts": 10},
            {"p": "En 'Vino ayer', 'ayer' es:", "opciones": ["CD", "CI", "CC Tiempo", "Atributo"], "correcta": "CC Tiempo", "pts": 10},
            {"p": "¿Cuál es una oración simple?", "opciones": ["Juan estudia", "Juan estudia y María trabaja", "Dijo que vendría", "Llegó, saludó"], "correcta": "Juan estudia", "pts": 10},
            {"p": "En 'Doy el libro a Juan', el CI es:", "opciones": ["el libro", "a Juan", "Doy", "Juan"], "correcta": "a Juan", "pts": 10},
        ]
        
        for i, p in enumerate(preguntas, 1):
            PreguntaEvaluacion.objects.create(
                evaluacion=eval2,
                tipo="opcion",
                pregunta=p["p"],
                opcion1=p["opciones"][0],
                opcion2=p["opciones"][1],
                opcion3=p["opciones"][2],
                opcion4=p["opciones"][3],
                respuesta_correcta=p["correcta"],
                puntaje=p["pts"],
                orden=i
            )
    
    # ============================================================
    # CURSO 3: ENGLISH GRAMMAR
    # ============================================================
    curso3, created = Curso.objects.get_or_create(
        titulo="English Grammar",
        defaults={
            "descripcion": "Curso completo de gramática inglesa para hispanohablantes.",
            "categoria": ingles,
            "nivel": intermedio,
            "duracion_estimada": 16,
            "orden": 3
        }
    )
    
    if created:
        print(f"  ✅ Curso creado: {curso3.titulo}")
        
        lecciones = [
            {"titulo": "Present Simple", "contenido": "I go, You go, He/She goes. Usos: hábitos y verdades generales.", "orden": 1},
            {"titulo": "Past Simple", "contenido": "I went, You went. Verbos regulares e irregulares.", "orden": 2},
            {"titulo": "Present Perfect", "contenido": "I have visited. Usos: experiencias, acciones que continúan.", "orden": 3},
            {"titulo": "Future Tenses", "contenido": "Will vs Going to. Usos y diferencias.", "orden": 4}
        ]
        
        for lec in lecciones:
            Leccion.objects.get_or_create(
                curso=curso3,
                titulo=lec["titulo"],
                defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
            )
        
        eval3 = Evaluacion.objects.create(
            curso=curso3,
            titulo="English Grammar Evaluation",
            descripcion="Test your English grammar knowledge",
            tipo="sumativa",
            puntaje_maximo=100,
            tiempo_limite=30,
            intentos_permitidos=2
        )
        
        preguntas = [
            {"p": "I ___ to school every day.", "opciones": ["go", "goes", "going", "went"], "correcta": "go", "pts": 10},
            {"p": "She ___ English.", "opciones": ["study", "studies", "studing", "studys"], "correcta": "studies", "pts": 10},
            {"p": "I ___ to Paris last year.", "opciones": ["go", "went", "gone", "going"], "correcta": "went", "pts": 10},
            {"p": "I have never ___ sushi.", "opciones": ["eat", "ate", "eaten", "eating"], "correcta": "eaten", "pts": 10},
            {"p": "I ___ help you.", "opciones": ["will", "am going to", "going to", "go to"], "correcta": "will", "pts": 10},
        ]
        
        for i, p in enumerate(preguntas, 1):
            PreguntaEvaluacion.objects.create(
                evaluacion=eval3,
                tipo="opcion",
                pregunta=p["p"],
                opcion1=p["opciones"][0],
                opcion2=p["opciones"][1],
                opcion3=p["opciones"][2],
                opcion4=p["opciones"][3],
                respuesta_correcta=p["correcta"],
                puntaje=p["pts"],
                orden=i
            )
    
    print("\n" + "=" * 60)
    print("✅ Cursos creados exitosamente!")
    print(f"📚 Total cursos: {Curso.objects.count()}")

if __name__ == "__main__":
    crear_cursos_completos()
