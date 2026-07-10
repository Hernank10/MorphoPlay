#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Evaluacion, PreguntaEvaluacion

def agregar_evaluaciones_morfologia():
    print("📝 Agregando evaluaciones al curso de Morfología del Castellano...")
    print("=" * 60)
    
    try:
        curso = Curso.objects.get(titulo="Morfología del Castellano")
    except Curso.DoesNotExist:
        print("❌ Curso no encontrado")
        return
    
    print(f"✅ Curso encontrado: {curso.titulo}")
    
    # Evaluación 1: Conceptos Básicos
    eval1, created = Evaluacion.objects.get_or_create(
        curso=curso,
        titulo="Evaluación de Conceptos Básicos de Morfología",
        defaults={
            "descripcion": "Evalúa tus conocimientos sobre los conceptos fundamentales de la morfología",
            "tipo": "formativa",
            "puntaje_maximo": 100,
            "tiempo_limite": 20,
            "intentos_permitidos": 2,
            "orden": 1
        }
    )
    
    if created:
        print(f"  ✅ Evaluación creada: {eval1.titulo}")
        
        preguntas1 = [
            {
                "p": "¿Qué es la morfología?",
                "opciones": [
                    "Estudio de la estructura de las palabras",
                    "Estudio de la estructura de las oraciones",
                    "Estudio de los sonidos del lenguaje",
                    "Estudio del significado de las palabras"
                ],
                "correcta": "Estudio de la estructura de las palabras",
                "pts": 10
            },
            {
                "p": "¿Qué es un lexema o raíz?",
                "opciones": [
                    "La parte de la palabra que contiene el significado básico",
                    "La parte que se añade al final de la palabra",
                    "La parte que se añade al inicio de la palabra",
                    "El conjunto de todas las palabras"
                ],
                "correcta": "La parte de la palabra que contiene el significado básico",
                "pts": 10
            },
            {
                "p": "¿Qué es un morfema?",
                "opciones": [
                    "Parte que añade información gramatical",
                    "El significado principal de la palabra",
                    "El conjunto de todas las palabras",
                    "La estructura de la oración"
                ],
                "correcta": "Parte que añade información gramatical",
                "pts": 10
            },
            {
                "p": "Ejemplo de prefijo:",
                "opciones": ["-ito", "pre-", "-ción", "-mente"],
                "correcta": "pre-",
                "pts": 10
            },
            {
                "p": "Ejemplo de sufijo:",
                "opciones": ["sub-", "in-", "-ito", "pre-"],
                "correcta": "-ito",
                "pts": 10
            },
            {
                "p": "En la palabra 'casita', ¿cuál es la raíz?",
                "opciones": ["cas", "ita", "casa", "sit"],
                "correcta": "cas",
                "pts": 10
            },
            {
                "p": "En la palabra 'inútil', ¿cuál es el prefijo?",
                "opciones": ["in-", "-útil", "inútil", "-til"],
                "correcta": "in-",
                "pts": 10
            },
            {
                "p": "¿Qué tipo de palabra es 'submarino'?",
                "opciones": ["Derivada con prefijo", "Derivada con sufijo", "Compuesta", "Parasintética"],
                "correcta": "Derivada con prefijo",
                "pts": 10
            },
            {
                "p": "¿Qué tipo de palabra es 'abrelatas'?",
                "opciones": ["Derivada", "Compuesta", "Parasintética", "Acortamiento"],
                "correcta": "Compuesta",
                "pts": 10
            },
            {
                "p": "¿Qué tipo de palabra es 'tele' (de teléfono)?",
                "opciones": ["Derivada", "Compuesta", "Parasintética", "Acortamiento"],
                "correcta": "Acortamiento",
                "pts": 10
            }
        ]
        
        for p in preguntas1:
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
                orden=1
            )
        print(f"    ✅ {len(preguntas1)} preguntas agregadas")
    
    # Evaluación 2: Prefijos y Sufijos
    eval2, created = Evaluacion.objects.get_or_create(
        curso=curso,
        titulo="Evaluación de Prefijos y Sufijos",
        defaults={
            "descripcion": "Evalúa tus conocimientos sobre prefijos y sufijos en español",
            "tipo": "sumativa",
            "puntaje_maximo": 100,
            "tiempo_limite": 20,
            "intentos_permitidos": 2,
            "orden": 2
        }
    )
    
    if created:
        print(f"  ✅ Evaluación creada: {eval2.titulo}")
        
        preguntas2 = [
            {
                "p": "¿Qué prefijo significa 'no' o 'sin'?",
                "opciones": ["sub-", "in-", "pre-", "post-"],
                "correcta": "in-",
                "pts": 10
            },
            {
                "p": "¿Qué prefijo significa 'debajo de'?",
                "opciones": ["super-", "sub-", "pre-", "post-"],
                "correcta": "sub-",
                "pts": 10
            },
            {
                "p": "¿Qué sufijo forma diminutivos?",
                "opciones": ["-azo", "-ito", "-ción", "-mente"],
                "correcta": "-ito",
                "pts": 10
            },
            {
                "p": "¿Qué sufijo forma aumentativos?",
                "opciones": ["-ito", "-azo", "-ción", "-mente"],
                "correcta": "-azo",
                "pts": 10
            },
            {
                "p": "¿Qué sufijo forma profesiones?",
                "opciones": ["-ción", "-ista", "-mente", "-dad"],
                "correcta": "-ista",
                "pts": 10
            },
            {
                "p": "¿Qué prefijo significa 'antes de'?",
                "opciones": ["post-", "pre-", "sub-", "super-"],
                "correcta": "pre-",
                "pts": 10
            },
            {
                "p": "¿Qué prefijo significa 'después de'?",
                "opciones": ["pre-", "post-", "sub-", "super-"],
                "correcta": "post-",
                "pts": 10
            },
            {
                "p": "¿Qué sufijo forma adjetivos?",
                "opciones": ["-ción", "-ista", "-oso", "-dad"],
                "correcta": "-oso",
                "pts": 10
            },
            {
                "p": "En 'subterráneo', ¿qué significa el prefijo?",
                "opciones": ["Sobre", "Debajo", "Dentro", "Fuera"],
                "correcta": "Debajo",
                "pts": 10
            },
            {
                "p": "En 'prehistoria', ¿qué significa el prefijo?",
                "opciones": ["Antes de", "Después de", "Durante", "Sin"],
                "correcta": "Antes de",
                "pts": 10
            }
        ]
        
        for p in preguntas2:
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
                orden=1
            )
        print(f"    ✅ {len(preguntas2)} preguntas agregadas")
    
    # Evaluación 3: Formación de Palabras
    eval3, created = Evaluacion.objects.get_or_create(
        curso=curso,
        titulo="Evaluación de Formación de Palabras",
        defaults={
            "descripcion": "Evalúa tus conocimientos sobre los procesos de formación de palabras",
            "tipo": "sumativa",
            "puntaje_maximo": 100,
            "tiempo_limite": 20,
            "intentos_permitidos": 2,
            "orden": 3
        }
    )
    
    if created:
        print(f"  ✅ Evaluación creada: {eval3.titulo}")
        
        preguntas3 = [
            {
                "p": "¿Qué proceso forma 'casita'?",
                "opciones": ["Derivación", "Composición", "Parasíntesis", "Acortamiento"],
                "correcta": "Derivación",
                "pts": 10
            },
            {
                "p": "¿Qué proceso forma 'abrelatas'?",
                "opciones": ["Derivación", "Composición", "Parasíntesis", "Acortamiento"],
                "correcta": "Composición",
                "pts": 10
            },
            {
                "p": "¿Qué proceso forma 'quinceañera'?",
                "opciones": ["Derivación", "Composición", "Parasíntesis", "Acortamiento"],
                "correcta": "Parasíntesis",
                "pts": 10
            },
            {
                "p": "¿Qué proceso forma 'tele' (de teléfono)?",
                "opciones": ["Derivación", "Composición", "Parasíntesis", "Acortamiento"],
                "correcta": "Acortamiento",
                "pts": 10
            },
            {
                "p": "¿Qué proceso forma 'inútil'?",
                "opciones": ["Derivación con prefijo", "Derivación con sufijo", "Composición", "Parasíntesis"],
                "correcta": "Derivación con prefijo",
                "pts": 10
            },
            {
                "p": "¿Qué proceso forma 'peligroso'?",
                "opciones": ["Derivación con prefijo", "Derivación con sufijo", "Composición", "Parasíntesis"],
                "correcta": "Derivación con sufijo",
                "pts": 10
            },
            {
                "p": "¿Qué es la derivación?",
                "opciones": [
                    "Añadir prefijos o sufijos a una raíz",
                    "Unir dos o más palabras",
                    "Combinar derivación y composición",
                    "Reducir palabras largas"
                ],
                "correcta": "Añadir prefijos o sufijos a una raíz",
                "pts": 10
            },
            {
                "p": "¿Qué es la composición?",
                "opciones": [
                    "Añadir prefijos o sufijos a una raíz",
                    "Unir dos o más palabras",
                    "Combinar derivación y composición",
                    "Reducir palabras largas"
                ],
                "correcta": "Unir dos o más palabras",
                "pts": 10
            },
            {
                "p": "¿Qué es la parasíntesis?",
                "opciones": [
                    "Añadir prefijos o sufijos a una raíz",
                    "Unir dos o más palabras",
                    "Combinar derivación y composición",
                    "Reducir palabras largas"
                ],
                "correcta": "Combinar derivación y composição",
                "pts": 10
            },
            {
                "p": "¿Qué es el acortamiento?",
                "opciones": [
                    "Añadir prefijos o sufijos a una raíz",
                    "Unir dos o más palabras",
                    "Combinar derivación y composición",
                    "Reducir palabras largas"
                ],
                "correcta": "Reducir palabras largas",
                "pts": 10
            }
        ]
        
        for p in preguntas3:
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
                orden=1
            )
        print(f"    ✅ {len(preguntas3)} preguntas agregadas")
    
    print("\n" + "=" * 60)
    print("✅ Evaluaciones agregadas exitosamente!")
    print(f"📊 Total evaluaciones en el curso: {Evaluacion.objects.filter(curso=curso).count()}")

if __name__ == "__main__":
    agregar_evaluaciones_morfologia()
