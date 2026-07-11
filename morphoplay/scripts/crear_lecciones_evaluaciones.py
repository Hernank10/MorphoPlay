#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Categoria, Nivel, Leccion, Evaluacion, PreguntaEvaluacion

def crear_lecciones_evaluaciones():
    print("📚 CREANDO LECCIONES Y EVALUACIONES")
    print("=" * 60)
    
    # Obtener cursos
    try:
        curso1 = Curso.objects.get(titulo="Morfología del Castellano")
        curso2 = Curso.objects.get(titulo="Sintaxis del Castellano")
        curso3 = Curso.objects.get(titulo="English Grammar")
        curso4 = Curso.objects.get(titulo="Cognados Español-Inglés")
        curso5 = Curso.objects.get(titulo="Técnicas Narrativas en Literatura")
        curso6 = Curso.objects.get(titulo="Gramática Comparada: Español vs Inglés")
    except Exception as e:
        print(f"❌ Error obteniendo cursos: {e}")
        return
    
    # ============================================================
    # CURSO 1: MORFOLOGÍA DEL CASTELLANO
    # ============================================================
    print("\n📖 Curso: Morfología del Castellano")
    
    # Lecciones (ya existen, pero verificamos)
    lecciones1 = [
        {"titulo": "Introducción a la Morfología", 
         "contenido": "📖 INTRODUCCIÓN A LA MORFOLOGÍA\n\nLa morfología es la parte de la lingüística que estudia la estructura interna de las palabras.\n\n🔍 Conceptos clave:\n• Palabra: Unidad mínima con significado\n• Lexema/Raíz: Parte que contiene el significado básico\n• Morfema: Partes que añaden información gramatical\n\n📝 Ejemplos:\n• cas + ita = casita\n• perr + azo = perrazo\n• in + útil = inútil\n\n💡 Importancia:\nComprender la morfología te ayuda a:\n• Aumentar tu vocabulario\n• Entender palabras desconocidas\n• Mejorar tu ortografía", 
         "orden": 1},
        {"titulo": "Prefijos en Español", 
         "contenido": "🔤 PREFIJOS EN ESPAÑOL\n\nLos prefijos son partículas que se añaden al INICIO de una palabra para modificar su significado.\n\n📋 Clasificación:\n\n1. Negación: in-, des-, a-\n   • inútil, incorrecto, deshacer, amoral\n\n2. Lugar: sub-, super-, ante-, post-\n   • subterráneo, superhéroe, antebrazo\n\n3. Tiempo: pre-, post-, re-\n   • prehistoria, postergar, rehacer\n\n4. Cantidad: bi-, tri-, multi-\n   • bicicleta, triciclo, multipropósito\n\n✏️ Ejercicio:\nIdentifica el prefijo:\n1. subterráneo → ___\n2. rehacer → ___\n3. inútil → ___\n4. anteayer → ___", 
         "orden": 2},
        {"titulo": "Sufijos en Español", 
         "contenido": "🔤 SUFIJOS EN ESPAÑOL\n\nLos sufijos se añaden al FINAL de una palabra para crear nuevas palabras.\n\n📋 Clasificación:\n\n1. Diminutivos: -ito, -illo, -ín\n   • casita, pajarillo, pequeñín\n\n2. Aumentativos: -azo, -ón, -ote\n   • perrazo, hombrón, grandote\n\n3. Profesiones: -ero, -ista, -dor\n   • panadero, dentista, pintor\n\n4. Adjetivos: -oso, -able, -al\n   • cariñoso, amable, nacional\n\n✏️ Ejercicio:\nIdentifica el sufijo:\n1. casita → ___\n2. perrazo → ___\n3. panadero → ___\n4. cariñoso → ___", 
         "orden": 3},
        {"titulo": "Raíces y Formación de Palabras", 
         "contenido": "🌱 RAÍCES Y FORMACIÓN DE PALABRAS\n\nLa raíz es el núcleo semántico de la palabra.\n\n📝 Procesos de formación:\n\n1. Derivación: Añadir prefijos o sufijos\n   • cas + ita = casita\n   • in + útil = inútil\n\n2. Composición: Unir dos o más palabras\n   • abre + latas = abrelatas\n   • saca + corchos = sacacorchos\n\n3. Parasíntesis: Combinación de derivación y composición\n   • quince + añ + era = quinceañera\n\n4. Acortamiento: Reducción de palabras largas\n   • teléfono → tele\n   • bicicleta → bici\n\n📋 Raíces comunes:\n| Raíz | Significado | Derivadas |\n|------|-------------|-----------|\n| cas- | casa | casita, caserío |\n| perr- | perro | perrito, perrera |\n| mar- | mar | marino, maremoto |", 
         "orden": 4}
    ]
    
    for lec in lecciones1:
        obj, created = Leccion.objects.get_or_create(
            curso=curso1,
            titulo=lec["titulo"],
            defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
        )
        if created:
            print(f"  ✅ Lección creada: {lec['titulo']}")
        else:
            print(f"  ⏳ Lección ya existe: {lec['titulo']}")
    
    # Evaluación para Morfología
    eval1, created = Evaluacion.objects.get_or_create(
        curso=curso1,
        titulo="Evaluación de Morfología",
        defaults={
            "descripcion": "Pon a prueba tus conocimientos sobre la morfología del español",
            "tipo": "sumativa",
            "puntaje_maximo": 100,
            "tiempo_limite": 30,
            "intentos_permitidos": 2,
            "orden": 1
        }
    )
    
    if created:
        print(f"  ✅ Evaluación creada: {eval1.titulo}")
        preguntas = [
            {"p": "¿Qué es un prefijo?", "opciones": ["Partícula al inicio", "Partícula al final", "Raíz", "Lexema"], "correcta": "Partícula al inicio", "pts": 10},
            {"p": "Ejemplo de prefijo:", "opciones": ["-ito", "pre-", "-ción", "-mente"], "correcta": "pre-", "pts": 10},
            {"p": "¿Qué sufijo forma diminutivos?", "opciones": ["-azo", "-ito", "-ción", "-mente"], "correcta": "-ito", "pts": 10},
            {"p": "En 'submarino', 'sub-' significa:", "opciones": ["sobre", "debajo", "dentro", "fuera"], "correcta": "debajo", "pts": 10},
            {"p": "¿Qué sufijo forma profesiones?", "opciones": ["-ción", "-ista", "-mente", "-dad"], "correcta": "-ista", "pts": 10},
        ]
        for p in preguntas:
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
        print(f"    ✅ {len(preguntas)} preguntas creadas")
    else:
        print(f"  ⏳ Evaluación ya existe: {eval1.titulo}")

    # ============================================================
    # CURSO 2: SINTAXIS DEL CASTELLANO
    # ============================================================
    print("\n📖 Curso: Sintaxis del Castellano")
    
    lecciones2 = [
        {"titulo": "La Oración y sus Partes", 
         "contenido": "📖 LA ORACIÓN Y SUS PARTES\n\nLa oración es la unidad básica de comunicación con sentido completo.\n\n🔍 Estructura básica:\n\nORACIÓN\n├── SUJETO (quien realiza la acción)\n│   └── Núcleo: sustantivo o pronombre\n└── PREDICADO (lo que se dice del sujeto)\n    └── Núcleo: verbo\n\n📝 Ejemplos:\n| Oración | Sujeto | Predicado |\n|---------|--------|-----------|\n| El niño come pan | El niño | come pan |\n| María estudia mucho | María | estudia mucho |\n\n📋 Tipos de oraciones:\n• Enunciativa: El sol brilla\n• Interrogativa: ¿Llegarás hoy?\n• Exclamativa: ¡Qué bonito!\n• Imperativa: Ven aquí", 
         "orden": 1},
        {"titulo": "El Sujeto", 
         "contenido": "👤 EL SUJETO\n\nEl sujeto es quien realiza la acción del verbo.\n\n📋 Tipos de sujeto:\n\n1. Sujeto Expreso: Aparece explícitamente\n   • El niño juega en el parque.\n\n2. Sujeto Elíptico (Tácito): Se sobreentiende\n   • (Yo) Como en casa.\n   • (Ellos) Llegaron tarde.\n\n3. Sujeto Simple: Un solo núcleo\n   • Juan trabaja.\n\n4. Sujeto Compuesto: Varios núcleos\n   • Juan y María estudian.\n\n🔍 Cómo identificar el sujeto:\n1. Pregunta \"¿Quién?\" antes del verbo\n2. El verbo concuerda en persona y número", 
         "orden": 2},
        {"titulo": "El Predicado", 
         "contenido": "📝 EL PREDICADO\n\nEl predicado es lo que se dice del sujeto.\n\n📋 Tipos de predicado:\n\n1. Predicado Verbal: Verbo predicativo\n   • El niño come pan.\n\n2. Predicado Nominal: Verbo copulativo\n   • Juan es inteligente.\n\n📋 Complementos del Predicado:\n\n• CD (Complemento Directo): Recibe la acción\n  → Veo la casa.\n\n• CI (Complemento Indirecto): Destinatario\n  → Doy el libro a Juan.\n\n• CC (Complemento Circunstancial): Circunstancias\n  → Vino ayer (tiempo)\n  → Trabaja en Madrid (lugar)\n\n• Atributo: Con verbos copulativos\n  → Es alto.", 
         "orden": 3},
        {"titulo": "Complementos del Verbo", 
         "contenido": "🔍 COMPLEMENTOS DEL VERBO\n\nLos complementos completan el significado del verbo.\n\n📋 Tipos de complementos:\n\n1. COMPLEMENTO DIRECTO (CD)\n• ¿Qué? + verbo\n• Ejemplo: Veo la casa → ¿Qué veo? → la casa\n\n2. COMPLEMENTO INDIRECTO (CI)\n• ¿A quién? + verbo\n• Ejemplo: Doy el libro a Juan → ¿A quién? → a Juan\n\n3. COMPLEMENTO CIRCUNSTANCIAL (CC)\n• ¿Dónde? ¿Cuándo? ¿Cómo?\n• Ejemplo: Vino ayer → ¿Cuándo? → ayer\n\n4. COMPLEMENTO PREDICATIVO\n• Modifica al sujeto y al verbo\n• Ejemplo: Llegó cansado\n\n✏️ Ejercicio:\nIdentifica los complementos:\n\"María dio el libro a Juan ayer\"\n• CD: ___\n• CI: ___\n• CC: ___", 
         "orden": 4}
    ]
    
    for lec in lecciones2:
        obj, created = Leccion.objects.get_or_create(
            curso=curso2,
            titulo=lec["titulo"],
            defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
        )
        if created:
            print(f"  ✅ Lección creada: {lec['titulo']}")
    
    # Evaluación para Sintaxis
    eval2, created = Evaluacion.objects.get_or_create(
        curso=curso2,
        titulo="Evaluación de Sintaxis",
        defaults={
            "descripcion": "Pon a prueba tus conocimientos sobre sintaxis",
            "tipo": "sumativa",
            "puntaje_maximo": 100,
            "tiempo_limite": 30,
            "intentos_permitidos": 2,
            "orden": 1
        }
    )
    
    if created:
        print(f"  ✅ Evaluación creada: {eval2.titulo}")
        preguntas = [
            {"p": "¿Qué es el sujeto?", "opciones": ["Quien realiza la acción", "Lo que se dice del verbo", "El núcleo del predicado"], "correcta": "Quien realiza la acción", "pts": 10},
            {"p": "En 'El niño come pan', el sujeto es:", "opciones": ["El niño", "come pan", "pan"], "correcta": "El niño", "pts": 10},
            {"p": "En 'Vino ayer', 'ayer' es:", "opciones": ["CD", "CI", "CC Tiempo"], "correcta": "CC Tiempo", "pts": 10},
            {"p": "¿Cuál es una oración simple?", "opciones": ["Juan estudia", "Juan estudia y María trabaja", "Dijo que vendría"], "correcta": "Juan estudia", "pts": 10},
            {"p": "En 'Doy el libro a Juan', el CI es:", "opciones": ["el libro", "a Juan", "Doy"], "correcta": "a Juan", "pts": 10},
        ]
        for p in preguntas:
            PreguntaEvaluacion.objects.create(
                evaluacion=eval2,
                tipo="opcion",
                pregunta=p["p"],
                opcion1=p["opciones"][0],
                opcion2=p["opciones"][1],
                opcion3=p["opciones"][2],
                opcion4="",
                respuesta_correcta=p["correcta"],
                puntaje=p["pts"],
                orden=1
            )
        print(f"    ✅ {len(preguntas)} preguntas creadas")

    # ============================================================
    # CURSO 3: ENGLISH GRAMMAR
    # ============================================================
    print("\n📖 Curso: English Grammar")
    
    lecciones3 = [
        {"titulo": "Present Simple", 
         "contenido": "📖 PRESENT SIMPLE\n\nThe Present Simple is used for habits, general truths, and permanent situations.\n\n🔍 Structure:\n• Affirmative: Subject + Verb (s/es)\n  → I work / He works\n• Negative: Subject + do/does + not + Verb\n  → I do not work / He does not work\n• Interrogative: Do/Does + Subject + Verb?\n  → Do you work? / Does he work?\n\n📝 Examples:\n• I walk to school every day.\n• She works in a hospital.\n• Water boils at 100°C.\n\n✏️ Exercise:\nComplete:\n1. I ___ (go) to school every day.\n2. She ___ (study) English.\n3. They ___ (not work) on Sundays.", 
         "orden": 1},
        {"titulo": "Past Simple", 
         "contenido": "📖 PAST SIMPLE\n\nThe Past Simple is used for completed actions in the past.\n\n🔍 Structure:\n• Affirmative: Subject + Verb (ed/irregular)\n  → I worked / I went\n• Negative: Subject + did + not + Verb\n  → I did not work\n• Interrogative: Did + Subject + Verb?\n  → Did you work?\n\n📋 Regular Verbs:\n• work → worked\n• live → lived\n• study → studied\n\n📋 Irregular Verbs:\n• go → went\n• eat → ate\n• buy → bought\n\n✏️ Exercise:\nComplete:\n1. She ___ (go) to the cinema yesterday.\n2. I ___ (eat) pizza for dinner.", 
         "orden": 2},
        {"titulo": "Present Perfect", 
         "contenido": "📖 PRESENT PERFECT\n\nThe Present Perfect connects the past with the present.\n\n🔍 Uses:\n1. Experiences: I have visited Paris.\n2. Actions that continue: She has worked here for 5 years.\n3. Recent actions: I have lost my keys.\n\n🔍 Structure:\n• Affirmative: Subject + have/has + Past Participle\n  → I have visited\n• Negative: Subject + have/has + not + PP\n  → I have not visited\n• Interrogative: Have/Has + Subject + PP?\n  → Have you visited?\n\n📋 Key words:\n• ever, never, already, yet, for, since\n\n✏️ Exercise:\nComplete:\n1. I ___ (visit) Paris.\n2. She ___ (work) here for 5 years.", 
         "orden": 3},
        {"titulo": "Future Tenses", 
         "contenido": "📖 FUTURE TENSES\n\nDifferent ways to express the future.\n\n🔍 WILL:\n• Spontaneous decisions\n• Predictions without evidence\n• Promises and offers\nExamples: I will help you. / It will rain.\n\n🔍 GOING TO:\n• Plans and intentions\n• Predictions with evidence\nExamples: I am going to study. / Look! It is going to rain.\n\n🔍 Present Continuous for future:\n• Fixed plans\n  → I am meeting her tomorrow.\n\n✏️ Exercise:\nComplete:\n1. I ___ (help) you. (promise)\n2. She ___ (study) medicine. (plan)\n3. Look at those clouds! It ___ (rain).", 
         "orden": 4}
    ]
    
    for lec in lecciones3:
        obj, created = Leccion.objects.get_or_create(
            curso=curso3,
            titulo=lec["titulo"],
            defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
        )
        if created:
            print(f"  ✅ Lección creada: {lec['titulo']}")
    
    eval3, created = Evaluacion.objects.get_or_create(
        curso=curso3,
        titulo="English Grammar Evaluation",
        defaults={
            "descripcion": "Test your English grammar knowledge",
            "tipo": "sumativa",
            "puntaje_maximo": 100,
            "tiempo_limite": 30,
            "intentos_permitidos": 2,
            "orden": 1
        }
    )
    
    if created:
        print(f"  ✅ Evaluación creada: {eval3.titulo}")
        preguntas = [
            {"p": "I ___ to school every day.", "opciones": ["go", "goes", "going", "went"], "correcta": "go", "pts": 10},
            {"p": "She ___ English.", "opciones": ["study", "studies", "studing", "studys"], "correcta": "studies", "pts": 10},
            {"p": "I ___ to Paris last year.", "opciones": ["go", "went", "gone", "going"], "correcta": "went", "pts": 10},
            {"p": "I have never ___ sushi.", "opciones": ["eat", "ate", "eaten", "eating"], "correcta": "eaten", "pts": 10},
            {"p": "I ___ help you.", "opciones": ["will", "am going to", "going to", "go to"], "correcta": "will", "pts": 10},
        ]
        for p in preguntas:
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
        print(f"    ✅ {len(preguntas)} preguntas creadas")

    # ============================================================
    # RESUMEN FINAL
    # ============================================================
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    
    for curso in Curso.objects.filter(activo=True):
        lecciones = curso.get_lecciones().count()
        evaluaciones = curso.evaluaciones.count()
        preguntas = 0
        for eval in curso.evaluaciones.all():
            preguntas += eval.get_preguntas().count()
        print(f"\n📚 {curso.titulo}")
        print(f"  📖 Lecciones: {lecciones}")
        print(f"  📝 Evaluaciones: {evaluaciones}")
        print(f"  ❓ Preguntas: {preguntas}")

if __name__ == "__main__":
    crear_lecciones_evaluaciones()
