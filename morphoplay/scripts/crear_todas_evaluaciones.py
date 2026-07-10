#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Evaluacion, PreguntaEvaluacion

def crear_todas_evaluaciones():
    print("📝 Creando evaluaciones para todos los cursos...")
    print("=" * 60)
    
    cursos = Curso.objects.filter(activo=True)
    
    for curso in cursos:
        print(f"\n📚 Curso: {curso.titulo}")
        
        # Verificar si ya tiene evaluaciones
        if Evaluacion.objects.filter(curso=curso).exists():
            print(f"  ⏳ El curso ya tiene evaluaciones")
            continue
        
        # Crear evaluaciones según el curso
        if "Morfología" in curso.titulo:
            crear_evaluaciones_morfologia(curso)
        elif "Sintaxis" in curso.titulo:
            crear_evaluaciones_sintaxis(curso)
        elif "English" in curso.titulo:
            crear_evaluaciones_ingles(curso)
        elif "Cognados" in curso.titulo:
            crear_evaluaciones_cognados(curso)
        elif "Narrativa" in curso.titulo or "Técnicas Narrativas" in curso.titulo:
            crear_evaluaciones_narrativa(curso)
        elif "Gramática Comparada" in curso.titulo:
            crear_evaluaciones_gramatica_comparada(curso)
        else:
            crear_evaluaciones_genericas(curso)

def crear_evaluaciones_morfologia(curso):
    """Crear evaluaciones para Morfología"""
    print("  📝 Creando evaluaciones de Morfología...")
    
    # Evaluación 1: Conceptos Básicos
    eval1 = Evaluacion.objects.create(
        curso=curso,
        titulo="Conceptos Básicos de Morfología",
        descripcion="Evalúa tus conocimientos sobre los fundamentos de la morfología",
        tipo="formativa",
        puntaje_maximo=100,
        tiempo_limite=20,
        intentos_permitidos=2,
        orden=1
    )
    
    preguntas = [
        {"p": "¿Qué es la morfología?", "opciones": ["Estudio de la estructura de las palabras", "Estudio de la estructura de las oraciones", "Estudio de los sonidos", "Estudio del significado"], "correcta": "Estudio de la estructura de las palabras", "pts": 10},
        {"p": "¿Qué es un lexema?", "opciones": ["Significado básico de la palabra", "Parte que se añade al final", "Parte que se añade al inicio", "Conjunto de palabras"], "correcta": "Significado básico de la palabra", "pts": 10},
        {"p": "¿Qué es un morfema?", "opciones": ["Parte que añade información gramatical", "El significado principal", "Conjunto de palabras", "Estructura de la oración"], "correcta": "Parte que añade información gramatical", "pts": 10},
        {"p": "Ejemplo de prefijo:", "opciones": ["-ito", "pre-", "-ción", "-mente"], "correcta": "pre-", "pts": 10},
        {"p": "Ejemplo de sufijo:", "opciones": ["sub-", "in-", "-ito", "pre-"], "correcta": "-ito", "pts": 10},
    ]
    for p in preguntas:
        PreguntaEvaluacion.objects.create(
            evaluacion=eval1, tipo="opcion", pregunta=p["p"],
            opcion1=p["opciones"][0], opcion2=p["opciones"][1],
            opcion3=p["opciones"][2], opcion4=p["opciones"][3],
            respuesta_correcta=p["correcta"], puntaje=p["pts"], orden=1
        )
    print(f"    ✅ Evaluación 1: {eval1.titulo} ({len(preguntas)} preguntas)")
    
    # Evaluación 2: Prefijos y Sufijos
    eval2 = Evaluacion.objects.create(
        curso=curso,
        titulo="Prefijos y Sufijos",
        descripcion="Evalúa tus conocimientos sobre prefijos y sufijos",
        tipo="sumativa",
        puntaje_maximo=100,
        tiempo_limite=20,
        intentos_permitidos=2,
        orden=2
    )
    
    preguntas = [
        {"p": "¿Qué prefijo significa 'no'?", "opciones": ["sub-", "in-", "pre-", "post-"], "correcta": "in-", "pts": 10},
        {"p": "¿Qué prefijo significa 'debajo'?", "opciones": ["super-", "sub-", "pre-", "post-"], "correcta": "sub-", "pts": 10},
        {"p": "¿Qué sufijo forma diminutivos?", "opciones": ["-azo", "-ito", "-ción", "-mente"], "correcta": "-ito", "pts": 10},
        {"p": "¿Qué sufijo forma aumentativos?", "opciones": ["-ito", "-azo", "-ción", "-mente"], "correcta": "-azo", "pts": 10},
        {"p": "¿Qué sufijo forma profesiones?", "opciones": ["-ción", "-ista", "-mente", "-dad"], "correcta": "-ista", "pts": 10},
    ]
    for p in preguntas:
        PreguntaEvaluacion.objects.create(
            evaluacion=eval2, tipo="opcion", pregunta=p["p"],
            opcion1=p["opciones"][0], opcion2=p["opciones"][1],
            opcion3=p["opciones"][2], opcion4=p["opciones"][3],
            respuesta_correcta=p["correcta"], puntaje=p["pts"], orden=1
        )
    print(f"    ✅ Evaluación 2: {eval2.titulo} ({len(preguntas)} preguntas)")
    
    # Evaluación 3: Formación de Palabras
    eval3 = Evaluacion.objects.create(
        curso=curso,
        titulo="Formación de Palabras",
        descripcion="Evalúa tus conocimientos sobre procesos de formación de palabras",
        tipo="sumativa",
        puntaje_maximo=100,
        tiempo_limite=20,
        intentos_permitidos=2,
        orden=3
    )
    
    preguntas = [
        {"p": "¿Qué proceso forma 'casita'?", "opciones": ["Derivación", "Composición", "Parasíntesis", "Acortamiento"], "correcta": "Derivación", "pts": 10},
        {"p": "¿Qué proceso forma 'abrelatas'?", "opciones": ["Derivación", "Composición", "Parasíntesis", "Acortamiento"], "correcta": "Composición", "pts": 10},
        {"p": "¿Qué proceso forma 'quinceañera'?", "opciones": ["Derivación", "Composición", "Parasíntesis", "Acortamiento"], "correcta": "Parasíntesis", "pts": 10},
        {"p": "¿Qué proceso forma 'tele'?", "opciones": ["Derivación", "Composición", "Parasíntesis", "Acortamiento"], "correcta": "Acortamiento", "pts": 10},
        {"p": "¿Qué es la derivación?", "opciones": ["Añadir prefijos/sufijos", "Unir palabras", "Combinar procesos", "Reducir palabras"], "correcta": "Añadir prefijos/sufijos", "pts": 10},
    ]
    for p in preguntas:
        PreguntaEvaluacion.objects.create(
            evaluacion=eval3, tipo="opcion", pregunta=p["p"],
            opcion1=p["opciones"][0], opcion2=p["opciones"][1],
            opcion3=p["opciones"][2], opcion4=p["opciones"][3],
            respuesta_correcta=p["correcta"], puntaje=p["pts"], orden=1
        )
    print(f"    ✅ Evaluación 3: {eval3.titulo} ({len(preguntas)} preguntas)")

def crear_evaluaciones_sintaxis(curso):
    """Crear evaluaciones para Sintaxis"""
    print("  📝 Creando evaluaciones de Sintaxis...")
    
    eval1 = Evaluacion.objects.create(
        curso=curso,
        titulo="Conceptos Básicos de Sintaxis",
        descripcion="Evalúa tus conocimientos sobre los fundamentos de la sintaxis",
        tipo="formativa",
        puntaje_maximo=100,
        tiempo_limite=20,
        intentos_permitidos=2,
        orden=1
    )
    
    preguntas = [
        {"p": "¿Qué es la sintaxis?", "opciones": ["Estructura de las oraciones", "Estructura de las palabras", "Sonidos del lenguaje", "Significado de palabras"], "correcta": "Estructura de las oraciones", "pts": 10},
        {"p": "¿Qué es el sujeto?", "opciones": ["Quien realiza la acción", "Lo que se dice del verbo", "El núcleo del predicado", "El complemento"], "correcta": "Quien realiza la acción", "pts": 10},
        {"p": "¿Qué es el predicado?", "opciones": ["Quien realiza la acción", "Lo que se dice del sujeto", "El núcleo del sujeto", "El complemento"], "correcta": "Lo que se dice del sujeto", "pts": 10},
        {"p": "¿Qué es el complemento directo?", "opciones": ["Recibe la acción", "Indica el destinatario", "Expresa circunstancias", "Modifica al sujeto"], "correcta": "Recibe la acción", "pts": 10},
        {"p": "¿Qué es el complemento indirecto?", "opciones": ["Recibe la acción", "Indica el destinatario", "Expresa circunstancias", "Modifica al sujeto"], "correcta": "Indica el destinatario", "pts": 10},
    ]
    for p in preguntas:
        PreguntaEvaluacion.objects.create(
            evaluacion=eval1, tipo="opcion", pregunta=p["p"],
            opcion1=p["opciones"][0], opcion2=p["opciones"][1],
            opcion3=p["opciones"][2], opcion4=p["opciones"][3],
            respuesta_correcta=p["correcta"], puntaje=p["pts"], orden=1
        )
    print(f"    ✅ Evaluación 1: {eval1.titulo} ({len(preguntas)} preguntas)")

def crear_evaluaciones_ingles(curso):
    """Crear evaluaciones para Inglés"""
    print("  📝 Creando evaluaciones de Inglés...")
    
    eval1 = Evaluacion.objects.create(
        curso=curso,
        titulo="English Tenses",
        descripcion="Test your knowledge of English tenses",
        tipo="formativa",
        puntaje_maximo=100,
        tiempo_limite=20,
        intentos_permitidos=2,
        orden=1
    )
    
    preguntas = [
        {"p": "I ___ to school every day.", "opciones": ["go", "goes", "going", "went"], "correcta": "go", "pts": 10},
        {"p": "She ___ English.", "opciones": ["study", "studies", "studing", "studys"], "correcta": "studies", "pts": 10},
        {"p": "I ___ to Paris last year.", "opciones": ["go", "went", "gone", "going"], "correcta": "went", "pts": 10},
        {"p": "I have never ___ sushi.", "opciones": ["eat", "ate", "eaten", "eating"], "correcta": "eaten", "pts": 10},
        {"p": "I ___ help you.", "opciones": ["will", "am going to", "going to", "go to"], "correcta": "will", "pts": 10},
    ]
    for p in preguntas:
        PreguntaEvaluacion.objects.create(
            evaluacion=eval1, tipo="opcion", pregunta=p["p"],
            opcion1=p["opciones"][0], opcion2=p["opciones"][1],
            opcion3=p["opciones"][2], opcion4=p["opciones"][3],
            respuesta_correcta=p["correcta"], puntaje=p["pts"], orden=1
        )
    print(f"    ✅ Evaluación 1: {eval1.titulo} ({len(preguntas)} preguntas)")

def crear_evaluaciones_cognados(curso):
    """Crear evaluaciones para Cognados"""
    print("  📝 Creando evaluaciones de Cognados...")
    
    eval1 = Evaluacion.objects.create(
        curso=curso,
        titulo="Cognados y Falsos Amigos",
        descripcion="Evalúa tus conocimientos sobre cognados y falsos amigos",
        tipo="formativa",
        puntaje_maximo=100,
        tiempo_limite=20,
        intentos_permitidos=2,
        orden=1
    )
    
    preguntas = [
        {"p": "¿Cuál es el cognado de 'animal' en español?", "opciones": ["animal", "animale", "anima", "animado"], "correcta": "animal", "pts": 10},
        {"p": "¿Qué significa 'embarrassed' realmente?", "opciones": ["embarazada", "avergonzado", "empezado", "embrujado"], "correcta": "avergonzado", "pts": 10},
        {"p": "¿Cuál es el cognado de 'family' en español?", "opciones": ["familia", "familiar", "famoso", "falda"], "correcta": "familia", "pts": 10},
        {"p": "¿Qué significa 'carpet' realmente?", "opciones": ["carpeta", "alfombra", "carpintero", "carpa"], "correcta": "alfombra", "pts": 10},
        {"p": "¿Cuál es el cognado de 'excellent' en español?", "opciones": ["excelente", "excellent", "exelente", "excelent"], "correcta": "excelente", "pts": 10},
    ]
    for p in preguntas:
        PreguntaEvaluacion.objects.create(
            evaluacion=eval1, tipo="opcion", pregunta=p["p"],
            opcion1=p["opciones"][0], opcion2=p["opciones"][1],
            opcion3=p["opciones"][2], opcion4=p["opciones"][3],
            respuesta_correcta=p["correcta"], puntaje=p["pts"], orden=1
        )
    print(f"    ✅ Evaluación 1: {eval1.titulo} ({len(preguntas)} preguntas)")

def crear_evaluaciones_narrativa(curso):
    """Crear evaluaciones para Narrativa"""
    print("  📝 Creando evaluaciones de Narrativa...")
    
    eval1 = Evaluacion.objects.create(
        curso=curso,
        titulo="Técnicas Narrativas Básicas",
        descripcion="Evalúa tus conocimientos sobre técnicas narrativas",
        tipo="formativa",
        puntaje_maximo=100,
        tiempo_limite=20,
        intentos_permitidos=2,
        orden=1
    )
    
    preguntas = [
        {"p": "¿Qué es la narrativa?", "opciones": ["Arte de contar historias", "Arte de describir", "Arte de argumentar", "Arte de explicar"], "correcta": "Arte de contar historias", "pts": 10},
        {"p": "¿Qué es el narrador omnisciente?", "opciones": ["Lo sabe todo", "Observa desde fuera", "Cuenta su historia", "Es inocente"], "correcta": "Lo sabe todo", "pts": 10},
        {"p": "¿Qué es la elipsis temporal?", "opciones": ["Salto en el tiempo", "Retroceso en el tiempo", "Anticipación", "Descripción"], "correcta": "Salto en el tiempo", "pts": 10},
        {"p": "¿Qué es la analepsis?", "opciones": ["Flashback", "Flashforward", "Elipsis", "Prolepsis"], "correcta": "Flashback", "pts": 10},
        {"p": "¿Qué es la prolepsis?", "opciones": ["Flashback", "Flashforward", "Elipsis", "Analepsis"], "correcta": "Flashforward", "pts": 10},
    ]
    for p in preguntas:
        PreguntaEvaluacion.objects.create(
            evaluacion=eval1, tipo="opcion", pregunta=p["p"],
            opcion1=p["opciones"][0], opcion2=p["opciones"][1],
            opcion3=p["opciones"][2], opcion4=p["opciones"][3],
            respuesta_correcta=p["correcta"], puntaje=p["pts"], orden=1
        )
    print(f"    ✅ Evaluación 1: {eval1.titulo} ({len(preguntas)} preguntas)")

def crear_evaluaciones_gramatica_comparada(curso):
    """Crear evaluaciones para Gramática Comparada"""
    print("  📝 Creando evaluaciones de Gramática Comparada...")
    
    eval1 = Evaluacion.objects.create(
        curso=curso,
        titulo="Comparación Gramatical",
        descripcion="Evalúa tus conocimientos sobre gramática comparada español-inglés",
        tipo="formativa",
        puntaje_maximo=100,
        tiempo_limite=20,
        intentos_permitidos=2,
        orden=1
    )
    
    preguntas = [
        {"p": "¿Cuál es el orden correcto en español?", "opciones": ["Sustantivo + Adjetivo", "Adjetivo + Sustantivo", "Verbo + Sustantivo", "Sustantivo + Verbo"], "correcta": "Sustantivo + Adjetivo", "pts": 10},
        {"p": "¿Cuál es el orden correcto en inglés?", "opciones": ["Sustantivo + Adjetivo", "Adjetivo + Sustantivo", "Verbo + Sustantivo", "Sustantivo + Verbo"], "correcta": "Adjetivo + Sustantivo", "pts": 10},
        {"p": "¿Cómo se dice 'tengo 20 años' en inglés?", "opciones": ["I have 20 years", "I am 20 years old", "I have 20 years old", "I am 20 years"], "correcta": "I am 20 years old", "pts": 10},
        {"p": "¿Cómo se dice 'estoy de acuerdo' en inglés?", "opciones": ["I am agree", "I agree", "I have agree", "I do agree"], "correcta": "I agree", "pts": 10},
        {"p": "¿Cómo se dice 'tengo hambre' en inglés?", "opciones": ["I have hungry", "I am hungry", "I hungry", "I do hungry"], "correcta": "I am hungry", "pts": 10},
    ]
    for p in preguntas:
        PreguntaEvaluacion.objects.create(
            evaluacion=eval1, tipo="opcion", pregunta=p["p"],
            opcion1=p["opciones"][0], opcion2=p["opciones"][1],
            opcion3=p["opciones"][2], opcion4=p["opciones"][3],
            respuesta_correcta=p["correcta"], puntaje=p["pts"], orden=1
        )
    print(f"    ✅ Evaluación 1: {eval1.titulo} ({len(preguntas)} preguntas)")

def crear_evaluaciones_genericas(curso):
    """Crear evaluaciones genéricas para cualquier curso"""
    print("  📝 Creando evaluaciones genéricas...")
    
    eval1 = Evaluacion.objects.create(
        curso=curso,
        titulo="Evaluación General",
        descripcion="Evalúa tus conocimientos sobre el contenido del curso",
        tipo="formativa",
        puntaje_maximo=100,
        tiempo_limite=20,
        intentos_permitidos=2,
        orden=1
    )
    
    preguntas = [
        {"p": "¿Cuál es el tema principal de este curso?", "opciones": ["Lingüística", "Literatura", "Gramática", "Fonética"], "correcta": "Lingüística", "pts": 10},
        {"p": "¿Qué nivel tiene este curso?", "opciones": ["Básico", "Intermedio", "Avanzado", "Experto"], "correcta": str(curso.nivel), "pts": 10},
        {"p": "¿Cuántas lecciones tiene este curso?", "opciones": ["4", "6", "8", "10"], "correcta": str(curso.get_lecciones().count()), "pts": 10},
        {"p": "¿Qué categoría tiene este curso?", "opciones": ["Morfología", "Sintaxis", "Gramática", str(curso.categoria)], "correcta": str(curso.categoria), "pts": 10},
        {"p": "¿Cuántas horas dura este curso?", "opciones": ["5", "10", "15", "20"], "correcta": str(curso.duracion_estimada), "pts": 10},
    ]
    for p in preguntas:
        PreguntaEvaluacion.objects.create(
            evaluacion=eval1, tipo="opcion", pregunta=p["p"],
            opcion1=p["opciones"][0], opcion2=p["opciones"][1],
            opcion3=p["opciones"][2], opcion4=p["opciones"][3],
            respuesta_correcta=p["correcta"], puntaje=p["pts"], orden=1
        )
    print(f"    ✅ Evaluación 1: {eval1.titulo} ({len(preguntas)} preguntas)")

if __name__ == "__main__":
    crear_todas_evaluaciones()
