#!/usr/bin/env python
import os
import sys
import django
import random
from datetime import datetime

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

print("=" * 70)
print("🌐 MORPHOPLAY - 100 CURSOS BILINGÜES CASTELLANO-INGLÉS")
print("=" * 70)
print(f"⏰ Inicio: {datetime.now().strftime('%H:%M:%S')}\n")

# ============================================================
# 1. CREAR CATEGORÍAS Y NIVELES
# ============================================================
print("📂 Creando categorías y niveles...")

categorias_data = [
    ('Bilingüe', 'Contenido bilingüe español-inglés', 'fa-globe'),
    ('Morfología', 'Estudio de la estructura de las palabras', 'fa-puzzle-piece'),
    ('Sintaxis', 'Estudio de la estructura de las oraciones', 'fa-sitemap'),
    ('Gramática', 'Reglas del lenguaje', 'fa-book'),
    ('Literatura', 'Técnicas literarias', 'fa-feather'),
    ('Inglés', 'Gramática inglesa', 'fa-language'),
]

categorias = {}
for nombre, desc, icono in categorias_data:
    cat, created = Categoria.objects.get_or_create(
        nombre=nombre,
        defaults={'descripcion': desc, 'icono': icono}
    )
    categorias[nombre] = cat
    print(f"  {'✅' if created else '⏳'} {nombre}")

niveles_data = [
    ('Básico', 1, '#4caf50', 10),
    ('Intermedio', 2, '#ffa726', 15),
    ('Avanzado', 3, '#ef5350', 20),
    ('Experto', 4, '#ab47bc', 25),
]

niveles = {}
for nombre, orden, color, puntos in niveles_data:
    niv, created = Nivel.objects.get_or_create(
        nombre=nombre,
        defaults={'orden': orden, 'color': color, 'puntos_base': puntos}
    )
    niveles[nombre] = niv
    print(f"  {'✅' if created else '⏳'} {nombre}")

# ============================================================
# 2. GENERAR 100 CURSOS BILINGÜES
# ============================================================
print("\n📚 Generando 100 cursos bilingües...")

# Bancos de temas bilingües
temas_bilingues = [
    # Cognados (1-15)
    "Cognados Perfectos", "Cognados Parciales", "Cognados de Familia", 
    "Cognados de Colores", "Cognados de Animales", "Cognados de Comida",
    "Cognados de Profesiones", "Cognados de Lugares", "Cognados de Tiempo",
    "Cognados de Números", "Cognados de Formas", "Cognados de Materiales",
    "Cognados de Emociones", "Cognados de Acciones", "Cognados de Cualidades",
    
    # Falsos Amigos (16-25)
    "Falsos Amigos: Embarazada/Embarrassed", "Falsos Amigos: Carpeta/Carpet",
    "Falsos Amigos: Éxito/Exit", "Falsos Amigos: Lectura/Lecture",
    "Falsos Amigos: Constipado/Constipated", "Falsos Amigos: Delito/Delight",
    "Falsos Amigos: Molestar/Molest", "Falsos Amigos: Recordar/Record",
    "Falsos Amigos: Soportar/Support", "Falsos Amigos: Realizar/Realize",
    
    # Gramática Comparada (26-45)
    "Orden de Palabras: Español vs Inglés", "Tiempos Verbales Comparados",
    "Uso de Ser/Estar vs Be", "Verbos Reflexivos vs No Reflexivos",
    "Subjuntivo vs Indicativo", "Preposiciones de Lugar",
    "Preposiciones de Tiempo", "Artículos: El/La vs The",
    "Pronombres Personales", "Adjetivos Posesivos",
    "Comparativos y Superlativos", "Oraciones Condicionales",
    "Voz Pasiva vs Activa", "Verb Patterns: Infinitivo vs Gerundio",
    "Phrasal Verbs en Inglés", "Perífrasis Verbales en Español",
    "Concordancia Sujeto-Verbo", "Uso de 'Haber' vs 'Have'",
    "Estructuras de Preguntas", "Negación en ambos idiomas",
    
    # Vocabulario Temático (46-65)
    "Vocabulario de Viajes", "Vocabulario de Negocios", "Vocabulario de Tecnología",
    "Vocabulario de Salud", "Vocabulario de Educación", "Vocabulario de Deportes",
    "Vocabulario de Arte", "Vocabulario de Música", "Vocabulario de Cine",
    "Vocabulario de Gastronomía", "Vocabulario de Moda", "Vocabulario de Arquitectura",
    "Vocabulario de Política", "Vocabulario de Religión", "Vocabulario de Ciencia",
    "Vocabulario de Naturaleza", "Vocabulario de Clima", "Vocabulario de Emociones",
    "Vocabulario de Familia", "Vocabulario de Trabajo",
    
    # Expresiones y Modismos (66-80)
    "Expresiones de Tiempo", "Expresiones de Cantidad", "Expresiones de Emoción",
    "Modismos Comunes en Inglés", "Modismos Comunes en Español",
    "Refranes y Proverbios", "Expresiones Cotidianas",
    "Saludos y Despedidas", "Frases de Cortesía", "Expresiones de Opinión",
    "Expresiones de Acuerdo/Desacuerdo", "Expresiones de Duda",
    "Expresiones de Sorpresa", "Expresiones de Enfado", "Expresiones de Alegría",
    
    # Traducción y Comparación (81-95)
    "Traducción Literal vs Natural", "Interpretación de Textos",
    "Comparación de Estructuras", "Análisis Contrastivo",
    "Errores Frecuentes de Traducción", "Calcos Lingüísticos",
    "Préstamos Léxicos", "Neologismos en ambos idiomas",
    "Diferencias Culturales", "Pragmática Comparada",
    "Cortesía Lingüística", "Registro Formal vs Informal",
    "Lenguaje Coloquial", "Lenguaje Técnico", "Lenguaje Periodístico",
    
    # Evaluación y Práctica (96-100)
    "Evaluación de Competencia Bilingüe", "Práctica de Traducción",
    "Ejercicios de Comparación", "Actividades de Inmersión",
    "Proyecto Final Bilingüe"
]

cursos_creados = 0
cursos_actualizados = 0

for i in range(1, 101):
    # Seleccionar tema
    tema_idx = (i - 1) % len(temas_bilingues)
    tema = temas_bilingues[tema_idx]
    
    # Determinar nivel
    if i <= 25:
        nivel = niveles["Básico"]
        nivel_nombre = "Básico"
    elif i <= 50:
        nivel = niveles["Intermedio"]
        nivel_nombre = "Intermedio"
    elif i <= 75:
        nivel = niveles["Avanzado"]
        nivel_nombre = "Avanzado"
    else:
        nivel = niveles["Experto"]
        nivel_nombre = "Experto"
    
    # Categoría principal: Bilingüe
    categoria = categorias["Bilingüe"]
    
    # Crear curso
    titulo = f"🌐 Curso {i:03d}: {tema} - Nivel {nivel_nombre}"
    
    # Contenido del curso
    contenido_base = f"""
📖 CURSO BILINGÜE: {tema}

🎯 OBJETIVOS:
- Aprender vocabulario bilingüe (español-inglés)
- Comprender diferencias gramaticales
- Practicar traducción y comparación
- Desarrollar competencia comunicativa

📝 TEMAS DEL CURSO:
1. Introducción a {tema}
2. Vocabulario clave en español e inglés
3. Estructuras gramaticales comparadas
4. Ejercicios prácticos de traducción
5. Evaluación final

🌐 EJEMPLOS:
• Español: _______________
• Inglés: _______________

✏️ PRÁCTICA:
Traduce las siguientes frases:
1. _________________________________
2. _________________________________
3. _________________________________
"""
    
    curso, created = Curso.objects.get_or_create(
        titulo=titulo,
        defaults={
            'descripcion': f"Curso bilingüe sobre {tema} - Nivel {nivel_nombre}",
            'categoria': categoria,
            'nivel': nivel,
            'duracion_estimada': 8 + random.randint(0, 8),
            'orden': i,
            'activo': True
        }
    )
    
    if created:
        cursos_creados += 1
    else:
        cursos_actualizados += 1
    
    # ============================================================
    # CREAR 5 LECCIONES POR CURSO
    # ============================================================
    for j in range(1, 6):
        leccion_titulo = f"Lección {j}: {tema} - Parte {j}"
        
        if j == 1:
            contenido = f"📖 INTRODUCCIÓN A {tema.upper()}\n\n🌐 ESPAÑOL: Conceptos básicos sobre {tema}.\n🇬🇧 ENGLISH: Basic concepts about {tema}.\n\n📝 Vocabulario clave:\n• Español: _______\n• Inglés: _______\n\n✏️ Ejercicio: Traduce las palabras."
        elif j == 2:
            contenido = f"📖 VOCABULARIO Y EJEMPLOS\n\n🌐 ESPAÑOL:\n• Palabra 1: _______\n• Palabra 2: _______\n• Palabra 3: _______\n\n🇬🇧 ENGLISH:\n• Word 1: _______\n• Word 2: _______\n• Word 3: _______\n\n📝 Frases de ejemplo:\n• Español: _______\n• Inglés: _______"
        elif j == 3:
            contenido = f"📖 ESTRUCTURAS GRAMATICALES\n\n🌐 ESPAÑOL: Estructura gramatical en español.\n🇬🇧 ENGLISH: Grammatical structure in English.\n\n📝 Comparación:\n• Español: Sujeto + Verbo + Complemento\n• Inglés: Subject + Verb + Object\n\n✏️ Ejercicio: Escribe oraciones en ambos idiomas."
        elif j == 4:
            contenido = f"📖 PRÁCTICA DE TRADUCCIÓN\n\n🌐 ESPAÑOL → 🇬🇧 ENGLISH\nTraduce las siguientes frases:\n1. _______\n2. _______\n3. _______\n\n🇬🇧 ENGLISH → 🌐 ESPAÑOL\nTraduce las siguientes frases:\n1. _______\n2. _______\n3. _______\n\n📝 Revisa tus traducciones."
        else:
            contenido = f"📖 EVALUACIÓN Y REPASO\n\n📝 Resumen de {tema}:\n• Conceptos clave\n• Vocabulario importante\n• Estructuras gramaticales\n\n✏️ Ejercicio final:\n1. _______\n2. _______\n3. _______\n\n🌟 ¡Has completado la lección!"
        
        leccion, created = Leccion.objects.get_or_create(
            curso=curso,
            titulo=leccion_titulo,
            defaults={
                'contenido': contenido,
                'orden': j
            }
        )
    
    # Mostrar progreso cada 10 cursos
    if i % 10 == 0:
        print(f"  ✅ {i} cursos creados...")

print(f"\n✅ {cursos_creados} cursos creados, {cursos_actualizados} actualizados")

# ============================================================
# 3. CREAR EVALUACIONES BILINGÜES
# ============================================================
print("\n📝 Creando evaluaciones bilingües...")

# Banco de preguntas bilingües
preguntas_bilingues = [
    {"p": "¿Cuál es el cognado de 'family' en español?", "opciones": ["familia", "familiar", "famoso", "falda"], "correcta": "familia"},
    {"p": "What is the cognate of 'animal' in Spanish?", "opciones": ["animal", "animale", "anima", "animado"], "correcta": "animal"},
    {"p": "¿Qué significa 'embarrassed' en español?", "opciones": ["embarazada", "avergonzado", "empezado", "embrujado"], "correcta": "avergonzado"},
    {"p": "What does 'carpet' mean in Spanish?", "opciones": ["carpeta", "alfombra", "carpintero", "carpa"], "correcta": "alfombra"},
    {"p": "¿Cuál es el cognado de 'excellent' en español?", "opciones": ["excelente", "excellent", "exelente", "excelent"], "correcta": "excelente"},
    {"p": "What is the Spanish word for 'family'?", "opciones": ["familia", "familia", "famili", "famila"], "correcta": "familia"},
    {"p": "¿Qué significa 'sensible' en inglés?", "opciones": ["sensible", "sensato", "sensitivo", "sensorial"], "correcta": "sensitivo"},
    {"p": "What does 'éxito' mean in English?", "opciones": ["exit", "success", "excited", "excellent"], "correcta": "success"},
    {"p": "¿Cuál es la traducción de 'I am hungry'?", "opciones": ["Tengo hambre", "Estoy hambriento", "Soy hambriento", "Tengo comida"], "correcta": "Tengo hambre"},
    {"p": "What is the translation of 'Tengo frío'?", "opciones": ["I have cold", "I am cold", "I feel cold", "I cold"], "correcta": "I am cold"},
    {"p": "¿Cómo se dice 'I agree' en español?", "opciones": ["Estoy de acuerdo", "Soy de acuerdo", "Tengo acuerdo", "Estoy acuerdo"], "correcta": "Estoy de acuerdo"},
    {"p": "What is the Spanish for 'I am 20 years old'?", "opciones": ["Tengo 20 años", "Soy 20 años", "Estoy 20 años", "Tengo 20 años viejos"], "correcta": "Tengo 20 años"},
    {"p": "¿Cuál es el cognado de 'different'?", "opciones": ["diferente", "differente", "diferent", "differnt"], "correcta": "diferente"},
    {"p": "What is the cognate of 'possible' in Spanish?", "opciones": ["posible", "possible", "posibl", "posible"], "correcta": "posible"},
    {"p": "¿Qué significa 'lecture' en español?", "opciones": ["lectura", "conferencia", "lección", "lector"], "correcta": "conferencia"},
]

total_evaluaciones = 0
for curso in Curso.objects.filter(activo=True)[:100]:
    # 2 evaluaciones por curso
    for eval_num in range(1, 3):
        eval_titulo = f"📝 Evaluación {eval_num}: {curso.titulo[:30]}..."
        
        eval_obj, created = Evaluacion.objects.get_or_create(
            curso=curso,
            titulo=eval_titulo,
            defaults={
                'descripcion': f"Evaluación bilingüe - Nivel {curso.nivel.nombre if curso.nivel else 'Básico'}",
                'tipo': 'formativa' if eval_num == 1 else 'sumativa',
                'puntaje_maximo': 100,
                'tiempo_limite': 15 + eval_num * 10,
                'intentos_permitidos': 2,
                'orden': eval_num
            }
        )
        
        if created:
            # Seleccionar 5 preguntas aleatorias
            preguntas = random.sample(preguntas_bilingues, min(5, len(preguntas_bilingues)))
            
            for j, p in enumerate(preguntas, 1):
                opciones = p["opciones"][:]
                random.shuffle(opciones)
                
                PreguntaEvaluacion.objects.create(
                    evaluacion=eval_obj,
                    tipo="opcion",
                    pregunta=p["p"],
                    opcion1=opciones[0] if len(opciones) > 0 else "",
                    opcion2=opciones[1] if len(opciones) > 1 else "",
                    opcion3=opciones[2] if len(opciones) > 2 else "",
                    opcion4=opciones[3] if len(opciones) > 3 else "",
                    respuesta_correcta=p["correcta"],
                    puntaje=20,
                    orden=j
                )
            
            total_evaluaciones += 1

print(f"✅ {total_evaluaciones} evaluaciones bilingües creadas")

# ============================================================
# 4. CREAR JUEGOS BILINGÜES
# ============================================================
print("\n🎮 Creando juegos bilingües...")

juegos_bilingues = [
    {"titulo": "🌐 Cognados Rápidos", "desc": "Encuentra el cognado correcto", "pregunta": "¿Cuál es el cognado de 'animal'?", "opciones": ["animal", "animale", "anima", "animado"], "correcta": "animal"},
    {"titulo": "🎯 Falsos Amigos", "desc": "Identifica el falso amigo", "pregunta": "¿Qué significa 'embarrassed'?", "opciones": ["embarazada", "avergonzado", "empezado", "embrujado"], "correcta": "avergonzado"},
    {"titulo": "🧩 Traducción Rápida", "desc": "Traduce al inglés", "pregunta": "¿Cómo se dice 'Tengo hambre'?", "opciones": ["I have hungry", "I am hungry", "I hungry", "I do hungry"], "correcta": "I am hungry"},
    {"titulo": "🎲 Cultura y Lengua", "desc": "Aprende expresiones", "pregunta": "¿Qué significa 'It's raining cats and dogs'?", "opciones": ["Llueven gatos y perros", "Llueve mucho", "Está nublado", "Hace sol"], "correcta": "Llueve mucho"},
    {"titulo": "🏆 Competencia Bilingüe", "desc": "Demuestra tu nivel", "pregunta": "¿Cuál es el cognado de 'excellent'?", "opciones": ["excelente", "excellent", "exelente", "excelent"], "correcta": "excelente"},
    {"titulo": "⚡ Verbos Comparados", "desc": "Compara verbos", "pregunta": "¿Cómo se dice 'I agree'?", "opciones": ["Estoy de acuerdo", "Soy de acuerdo", "Tengo acuerdo", "Estoy acuerdo"], "correcta": "Estoy de acuerdo"},
    {"titulo": "🌟 Pronunciación", "desc": "Practica la pronunciación", "pregunta": "¿Cómo se pronuncia 'thought'?", "opciones": ["zot", "fot", "tort", "dot"], "correcta": "zot"},
    {"titulo": "📚 Lectura Bilingüe", "desc": "Comprensión de lectura", "pregunta": "¿Qué significa 'The book is on the table'?", "opciones": ["El libro está en la mesa", "El libro es en la mesa", "El libro tiene la mesa", "El libro está sobre la mesa"], "correcta": "El libro está en la mesa"},
]

categoria_bilingue = Categoria.objects.get(nombre='Bilingüe')
nivel_basico = Nivel.objects.get(nombre='Básico')

total_juegos = 0
for data in juegos_bilingues:
    juego, created = Juego.objects.get_or_create(
        titulo=data["titulo"],
        defaults={
            'descripcion': data["desc"],
            'pregunta': data["pregunta"],
            'categoria': categoria_bilingue,
            'nivel': nivel_basico,
            'tipo': 'opcion',
            'opcion1': data["opciones"][0],
            'opcion2': data["opciones"][1],
            'opcion3': data["opciones"][2],
            'opcion4': data["opciones"][3],
            'respuesta_correcta': data["correcta"],
            'puntos': 10 + random.randint(0, 15),
            'activo': True
        }
    )
    if created:
        total_juegos += 1
        print(f"  ✅ {data['titulo']}")

print(f"✅ {total_juegos} juegos bilingües creados")

# ============================================================
# 5. CREAR USUARIOS DE PRUEBA
# ============================================================
print("\n👤 Creando usuarios de prueba...")

usuarios_data = [
    {'username': 'estudiante1', 'email': 'estudiante1@test.com', 'password': 'MorphoPlay2024!', 'first_name': 'Ana', 'last_name': 'Martínez'},
    {'username': 'estudiante2', 'email': 'estudiante2@test.com', 'password': 'MorphoPlay2024!', 'first_name': 'Carlos', 'last_name': 'González'},
    {'username': 'estudiante3', 'email': 'estudiante3@test.com', 'password': 'MorphoPlay2024!', 'first_name': 'María', 'last_name': 'López'},
]

for data in usuarios_data:
    if not User.objects.filter(username=data['username']).exists():
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        EstadisticasUsuario.objects.create(usuario=user)
        print(f"  ✅ {data['username']} - {data['first_name']} {data['last_name']}")

# Superusuario
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@morphoplay.com', 'admin123')
    print("  ✅ admin - Superusuario")

# ============================================================
# 6. RESUMEN FINAL
# ============================================================
print("\n" + "=" * 70)
print("📊 RESUMEN DE INSTALACIÓN")
print("=" * 70)
print(f"📚 Cursos bilingües: {Curso.objects.count()}")
print(f"📖 Lecciones: {Leccion.objects.count()}")
print(f"📝 Evaluaciones: {Evaluacion.objects.count()}")
print(f"🎮 Juegos: {Juego.objects.count()}")
print(f"📂 Categorías: {Categoria.objects.count()}")
print(f"📊 Niveles: {Nivel.objects.count()}")
print(f"👤 Usuarios: {User.objects.count()}")

print("\n📋 EJEMPLO DE CURSOS BILINGÜES:")
for curso in Curso.objects.filter(categoria__nombre='Bilingüe')[:5]:
    lecciones = curso.get_lecciones().count()
    print(f"  - {curso.titulo} ({lecciones} lecciones)")

print("\n" + "=" * 70)
print("✅ ¡100 CURSOS BILINGÜES INSTALADOS EXITOSAMENTE!")
print(f"⏰ Finalizado: {datetime.now().strftime('%H:%M:%S')}")
print("=" * 70)
print("\n🔑 CREDENCIALES:")
print("  👤 admin / admin123")
print("  👤 estudiante1 / MorphoPlay2024!")
print("  👤 estudiante2 / MorphoPlay2024!")
print("  👤 estudiante3 / MorphoPlay2024!")
print("\n🌐 ACCESO:")
print("  📚 Cursos: http://localhost:8000/cursos/")
print("  🎮 Juegos: http://localhost:8000/juegos/")
print("  🔐 Admin: http://localhost:8000/admin/")
print("\n🚀 Inicia el servidor:")
print("  source venv/bin/activate")
print("  python manage.py runserver 0.0.0.0:8000")
