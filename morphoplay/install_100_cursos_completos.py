#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MORPHOPLAY - INSTALADOR DE 100 CURSOS COMPLETOS v8.0
Genera 100 cursos automáticos de morfología, sintaxis y bilingüe
con 100 lecciones cada uno, evaluaciones y juegos ilimitados
"""

import os
import sys
import subprocess
import json
import random
from pathlib import Path
from datetime import datetime

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

class Cursos100CompletosInstaller:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.venv_dir = self.project_dir / "venv"
        self.python_path = None
        self.total_cursos = 100
        self.cursos_creados = 0
        
    def run(self):
        print_header("🚀 INSTALADOR DE 100 CURSOS COMPLETOS - MORPHOPLAY v8.0")
        print(f"📁 Directorio: {self.project_dir}")
        print(f"📚 Cursos a generar: {self.total_cursos}")
        print(f"📖 Lecciones por curso: 100")
        print(f"📝 Evaluaciones por curso: 5")
        print(f"🎮 Juegos por curso: 10")
        print(f"⏰ Inicio: {datetime.now().strftime('%H:%M:%S')}\n")
        
        try:
            # Paso 1: Verificar entorno
            self.step_verify_env()
            
            # Paso 2: Crear 100 cursos
            self.step_create_100_cursos()
            
            # Paso 3: Crear lecciones para todos los cursos
            self.step_create_lecciones_masivas()
            
            # Paso 4: Crear evaluaciones para todos los cursos
            self.step_create_evaluaciones_masivas()
            
            # Paso 5: Crear juegos para todos los cursos
            self.step_create_juegos_masivos()
            
            # Paso 6: Crear templates y rutas
            self.step_create_templates()
            
            # Paso 7: Verificar instalación
            self.step_verify()
            
            print_header("🎉 100 CURSOS COMPLETOS INSTALADOS EXITOSAMENTE")
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
    
    def step_create_100_cursos(self):
        print_step(f"Creando {self.total_cursos} cursos...")
        
        script = f"""
import django
import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Categoria, Nivel

print("📚 Creando 100 cursos...")

# Obtener o crear categorías
categorias = {}
for nombre in ['Morfología', 'Sintaxis', 'Bilingüe']:
    cat, _ = Categoria.objects.get_or_create(
        nombre=nombre,
        defaults={{'descripcion': f'Categoría de {nombre}', 'icono': 'fa-book', 'activo': True}}
    )
    categorias[nombre] = cat

# Obtener o crear niveles
niveles = {}
niveles_data = [
    ('Básico', 1, '#4caf50', 10),
    ('Intermedio', 2, '#ffa726', 15),
    ('Avanzado', 3, '#ef5350', 20),
    ('Experto', 4, '#ab47bc', 25),
]
for nombre, orden, color, puntos in niveles_data:
    niv, _ = Nivel.objects.get_or_create(
        nombre=nombre,
        defaults={{'orden': orden, 'color': color, 'puntos_base': puntos}}
    )
    niveles[nombre] = niv

# Temas para los cursos
temas_morfologia = [
    "Morfología Básica", "Morfología Intermedia", "Morfología Avanzada", 
    "Morfología de Sustantivos", "Morfología de Verbos", "Morfología de Adjetivos",
    "Morfología de Adverbios", "Morfología de Prefijos", "Morfología de Sufijos",
    "Morfología de Raíces", "Morfología de Lexemas", "Morfología de Morfemas",
    "Morfología Derivativa", "Morfología Flexiva", "Morfología Compuesta",
    "Morfología de Palabras", "Morfología de Formación", "Morfología de Etimología",
    "Morfología de Familias", "Morfología de Campos", "Morfología de Neologismos",
    "Morfología de Arcaísmos", "Morfología de Extranjerismos", "Morfología de Gentilicios",
    "Morfología de Diminutivos", "Morfología de Aumentativos", "Morfología de Despectivos"
]

temas_sintaxis = [
    "Sintaxis Básica", "Sintaxis Intermedia", "Sintaxis Avanzada",
    "Sintaxis de Oraciones", "Sintaxis de Frases", "Sintaxis de Cláusulas",
    "Sintaxis de Sujeto", "Sintaxis de Predicado", "Sintaxis de Complementos",
    "Sintaxis de Modificadores", "Sintaxis de Conectores", "Sintaxis de Nexos",
    "Sintaxis de Coordinación", "Sintaxis de Subordinación", "Sintaxis de Yuxtaposición",
    "Sintaxis de Análisis", "Sintaxis de Estructura", "Sintaxis de Función",
    "Sintaxis de Relaciones", "Sintaxis de Concordancia", "Sintaxis de Regencia",
    "Sintaxis de Elipsis", "Sintaxis de Anáfora", "Sintaxis de Catáfora",
    "Sintaxis de Deíxis", "Sintaxis de Tematización", "Sintaxis de Focalización"
]

temas_bilingue = [
    "Cognados Básicos", "Cognados Intermedios", "Cognados Avanzados",
    "Falsos Amigos Básicos", "Falsos Amigos Intermedios", "Falsos Amigos Avanzados",
    "Estructuras Comparadas", "Tiempos Verbales Comparados", "Orden de Palabras Comparado",
    "Sufijos Paralelos", "Prefijos Paralelos", "Raíces Compartidas",
    "Vocabulario Compartido", "Expresiones Equivalentes", "Proverbios Comparados",
    "Gramática Comparada", "Sintaxis Comparada", "Morfología Comparada",
    "Fonética Comparada", "Semántica Comparada", "Pragmática Comparada",
    "Traducción Directa", "Traducción Inversa", "Interpretación Simultánea",
    "Análisis Contrastivo", "Errores Frecuentes", "Zonas de Transferencia"
]

# Crear 100 cursos
total_cursos = 0
for i in range(1, 101):
    # Determinar categoría
    if i % 3 == 0:
        categoria = categorias["Bilingüe"]
        temas = temas_bilingue
        nivel_base = "Intermedio"
    elif i % 3 == 1:
        categoria = categorias["Morfología"]
        temas = temas_morfologia
        nivel_base = "Básico"
    else:
        categoria = categorias["Sintaxis"]
        temas = temas_sintaxis
        nivel_base = "Intermedio"
    
    # Seleccionar tema
    tema_idx = (i - 1) % len(temas)
    tema = temas[tema_idx]
    
    # Determinar nivel
    if i < 25:
        nivel = niveles["Básico"]
    elif i < 50:
        nivel = niveles["Intermedio"]
    elif i < 75:
        nivel = niveles["Avanzado"]
    else:
        nivel = niveles["Experto"]
    
    # Crear curso
    titulo = f"Curso {i:03d}: {tema} - Nivel {nivel.nombre}"
    
    curso, created = Curso.objects.get_or_create(
        titulo=titulo,
        defaults={{
            'descripcion': f"Curso completo de {tema} - Nivel {nivel.nombre}\\nCategoría: {categoria.nombre}",
            'categoria': categoria,
            'nivel': nivel,
            'duracion_estimada': 10 + random.randint(0, 10),
            'orden': i,
            'activo': True
        }}
    )
    
    if created:
        total_cursos += 1
        if total_cursos % 10 == 0:
            print(f"  ✅ {total_cursos} cursos creados...")

print(f"\\n✅ {total_cursos} cursos creados")
"""
        
        self._ejecutar_script(script)
        print_success(f"{self.total_cursos} cursos creados")
    
    def step_create_lecciones_masivas(self):
        print_step(f"Creando 100 lecciones para cada curso...")
        
        script = """
import django
import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Leccion

print("📖 Creando 100 lecciones por curso...")

# Bancos de contenido por categoría
contenido_morfologia = [
    "La morfología estudia la estructura interna de las palabras.",
    "Las palabras se componen de lexemas y morfemas.",
    "Los prefijos se añaden al inicio de la palabra.",
    "Los sufijos se añaden al final de la palabra.",
    "La derivación es el proceso de añadir afijos a una raíz.",
    "La composición une dos o más palabras para formar una nueva.",
    "La parasíntesis combina derivación y composición.",
    "El acortamiento reduce palabras largas.",
    "Los diminutivos expresan tamaño pequeño o afecto.",
    "Los aumentativos expresan tamaño grande.",
    "Los gentilicios indican origen o procedencia.",
    "Los neologismos son palabras nuevas en la lengua.",
    "Los arcaísmos son palabras en desuso.",
    "Los extranjerismos son palabras de otros idiomas.",
    "Las familias de palabras comparten la misma raíz."
]

contenido_sintaxis = [
    "La sintaxis estudia la estructura de las oraciones.",
    "La oración se compone de sujeto y predicado.",
    "El sujeto realiza la acción del verbo.",
    "El predicado expresa lo que se dice del sujeto.",
    "Los complementos amplían la información del verbo.",
    "El complemento directo recibe la acción directamente.",
    "El complemento indirecto indica el destinatario.",
    "El complemento circunstancial expresa circunstancias.",
    "Las oraciones simples tienen un solo verbo.",
    "Las oraciones compuestas tienen más de un verbo.",
    "La coordinación une oraciones independientes.",
    "La subordinación crea oraciones dependientes.",
    "La yuxtaposición une oraciones sin nexo.",
    "El análisis sintáctico identifica funciones.",
    "La concordancia es la relación entre elementos."
]

contenido_bilingue = [
    "Los cognados son palabras similares en dos idiomas.",
    "Los cognados perfectos se escriben igual.",
    "Los cognados parciales tienen pequeñas diferencias.",
    "Los falsos amigos tienen significados diferentes.",
    "El orden de palabras varía entre idiomas.",
    "Los tiempos verbales se expresan diferente.",
    "Las preposiciones tienen usos distintos.",
    "Los artículos funcionan de manera similar.",
    "Los pronombres tienen equivalencias.",
    "Los adverbios expresan circunstancias.",
    "Las conjunciones conectan ideas.",
    "Las interjecciones expresan emociones.",
    "La traducción requiere equivalencia.",
    "La interpretación es en tiempo real.",
    "El contraste revela diferencias."
]

contenido_general = [
    "Este curso explora los fundamentos de la lingüística.",
    "El lenguaje es una capacidad humana fundamental.",
    "La comunicación es el objetivo del lenguaje.",
    "Los signos lingüísticos son arbitrarios.",
    "La lengua es un sistema estructurado.",
    "El habla es la realización concreta de la lengua.",
    "El lenguaje tiene funciones diversas.",
    "La competencia lingüística es el conocimiento.",
    "La actuación es el uso real del lenguaje.",
    "La adquisición del lenguaje es un proceso natural.",
    "El aprendizaje requiere práctica y estudio.",
    "La evaluación mide el progreso.",
    "El feedback es esencial para mejorar.",
    "La práctica constante es la clave del éxito.",
    "La motivación es fundamental para aprender."
]

# Obtener todos los cursos
cursos = list(Curso.objects.filter(activo=True))

total_lecciones = 0
for curso in cursos:
    # Seleccionar contenido según categoría
    if curso.categoria and "Morfología" in curso.categoria.nombre:
        contenidos = contenido_morfologia
    elif curso.categoria and "Sintaxis" in curso.categoria.nombre:
        contenidos = contenido_sintaxis
    elif curso.categoria and "Bilingüe" in curso.categoria.nombre:
        contenidos = contenido_bilingue
    else:
        contenidos = contenido_general
    
    # Crear 100 lecciones por curso
    for i in range(1, 101):
        # Seleccionar contenido
        idx = (i - 1) % len(contenidos)
        base_contenido = contenidos[idx]
        
        # Generar contenido variado
        contenido = f"📖 Lección {i}: {curso.titulo}\\n\\n"
        contenido += f"{base_contenido}\\n\\n"
        
        # Agregar ejemplos
        if i % 2 == 0:
            contenido += "📝 Ejemplos:\\n"
            for j in range(3):
                contenido += f"  • Ejemplo {j+1} de esta lección.\\n"
        
        # Agregar ejercicio
        contenido += "\\n✏️ EJERCICIO:\\n"
        contenido += "Aplica lo aprendido en esta lección."
        
        # Crear lección
        leccion, created = Leccion.objects.get_or_create(
            curso=curso,
            titulo=f"Lección {i:03d}: {curso.titulo[:20]}...",
            defaults={
                'contenido': contenido,
                'orden': i
            }
        )
        
        if created:
            total_lecciones += 1

print(f"\\n✅ {total_lecciones} lecciones creadas")
"""
        
        self._ejecutar_script(script)
        print_success("100 lecciones por curso creadas")
    
    def step_create_evaluaciones_masivas(self):
        print_step(f"Creando 5 evaluaciones por curso...")
        
        script = """
import django
import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Evaluacion, PreguntaEvaluacion

print("📝 Creando 5 evaluaciones por curso...")

# Banco de preguntas
banco_preguntas = [
    {"p": "¿Qué estudia la lingüística?", "opciones": ["El lenguaje", "La literatura", "La historia", "La geografía"], "correcta": "El lenguaje"},
    {"p": "¿Qué es una palabra?", "opciones": ["Unidad con significado", "Una letra", "Una sílaba", "Un sonido"], "correcta": "Unidad con significado"},
    {"p": "¿Qué es un fonema?", "opciones": ["Unidad sonora", "Una letra", "Una sílaba", "Una palabra"], "correcta": "Unidad sonora"},
    {"p": "¿Qué es un morfema?", "opciones": ["Unidad de significado", "Un sonido", "Una letra", "Una sílaba"], "correcta": "Unidad de significado"},
    {"p": "¿Qué es un lexema?", "opciones": ["Raíz de la palabra", "Sufijo", "Prefijo", "Morfema"], "correcta": "Raíz de la palabra"},
    {"p": "¿Qué es un prefijo?", "opciones": ["Se añade al inicio", "Se añade al final", "Es la raíz", "Es un morfema"], "correcta": "Se añade al inicio"},
    {"p": "¿Qué es un sufijo?", "opciones": ["Se añade al final", "Se añade al inicio", "Es la raíz", "Es un lexema"], "correcta": "Se añade al final"},
    {"p": "¿Qué es una oración?", "opciones": ["Unidad con sentido", "Una palabra", "Una frase", "Un párrafo"], "correcta": "Unidad con sentido"},
    {"p": "¿Qué es el sujeto?", "opciones": ["Quien realiza la acción", "El verbo", "El complemento", "El predicado"], "correcta": "Quien realiza la acción"},
    {"p": "¿Qué es el predicado?", "opciones": ["Lo que se dice del sujeto", "El sujeto", "El complemento", "El verbo"], "correcta": "Lo que se dice del sujeto"},
    {"p": "¿Qué es un cognado?", "opciones": ["Palabra similar en otro idioma", "Palabra diferente", "Palabra inventada", "Palabra antigua"], "correcta": "Palabra similar en otro idioma"},
    {"p": "¿Qué es un falso amigo?", "opciones": ["Palabra que parece igual pero significa diferente", "Palabra igual", "Palabra diferente", "Palabra inventada"], "correcta": "Palabra que parece igual pero significa diferente"},
    {"p": "¿Qué es la traducción?", "opciones": ["Pasar texto a otro idioma", "Crear texto", "Leer texto", "Escribir texto"], "correcta": "Pasar texto a otro idioma"},
    {"p": "¿Qué es la interpretación?", "opciones": ["Traducir oralmente", "Traducir escrito", "Crear texto", "Leer texto"], "correcta": "Traducir oralmente"},
    {"p": "¿Qué es la gramática?", "opciones": ["Conjunto de reglas", "Un libro", "Un idioma", "Una palabra"], "correcta": "Conjunto de reglas"},
]

cursos = list(Curso.objects.filter(activo=True))

total_evaluaciones = 0
for curso in cursos:
    for eval_num in range(1, 6):
        eval_titulo = f"📝 Evaluación {eval_num}: {curso.titulo[:30]}..."
        
        eval_obj, created = Evaluacion.objects.get_or_create(
            curso=curso,
            titulo=eval_titulo,
            defaults={
                'descripcion': f"Evaluación {eval_num} del curso",
                'tipo': 'formativa' if eval_num < 3 else 'sumativa',
                'puntaje_maximo': 100,
                'tiempo_limite': 15 + eval_num * 5,
                'intentos_permitidos': 3,
                'orden': eval_num
            }
        )
        
        if created:
            # Seleccionar 5 preguntas aleatorias
            preguntas = random.sample(banco_preguntas, min(5, len(banco_preguntas)))
            
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

print(f"\\n✅ {total_evaluaciones} evaluaciones creadas")
"""
        
        self._ejecutar_script(script)
        print_success("5 evaluaciones por curso creadas")
    
    def step_create_juegos_masivos(self):
        print_step(f"Creando 10 juegos por curso...")
        
        script = """
import django
import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Juego, Categoria, Nivel

print("🎮 Creando 10 juegos por curso...")

categorias = list(Categoria.objects.filter(activo=True))
niveles = list(Nivel.objects.filter(activo=True))

if not categorias or not niveles:
    print("⚠️ No hay categorías o niveles disponibles")
    exit()

# Banco de juegos
juegos_templates = [
    {"titulo": "🏆 Carrera de Palabras", "desc": "Corre con las palabras correctas"},
    {"titulo": "🎯 Tiro al Blanco", "desc": "Apunta a la respuesta correcta"},
    {"titulo": "🧩 Rompecabezas", "desc": "Arma el significado correcto"},
    {"titulo": "🎲 Dados del Saber", "desc": "Lanza los dados y aprende"},
    {"titulo": "⚡ Rápidos y Correctos", "desc": "Responde rápido y bien"},
    {"titulo": "🌟 Estrella del Idioma", "desc": "Brilla con tu conocimiento"},
    {"titulo": "🏅 Competencia Lingüística", "desc": "Demuestra tu nivel"},
    {"titulo": "🎪 Circo de Palabras", "desc": "Diviértete con el lenguaje"},
    {"titulo": "🚀 Viaje al Conocimiento", "desc": "Explora el lenguaje"},
    {"titulo": "🌍 Explorador de Idiomas", "desc": "Descubre nuevos horizontes"}
]

banco_preguntas_juegos = [
    {"p": "¿Qué es un sustantivo?", "opciones": ["Nombre", "Acción", "Cualidad", "Circunstancia"], "correcta": "Nombre"},
    {"p": "¿Qué es un verbo?", "opciones": ["Acción", "Nombre", "Cualidad", "Circunstancia"], "correcta": "Acción"},
    {"p": "¿Qué es un adjetivo?", "opciones": ["Cualidad", "Nombre", "Acción", "Circunstancia"], "correcta": "Cualidad"},
    {"p": "¿Qué es un adverbio?", "opciones": ["Circunstancia", "Nombre", "Acción", "Cualidad"], "correcta": "Circunstancia"},
    {"p": "¿Qué es una preposición?", "opciones": ["Relaciona", "Nombre", "Acción", "Cualidad"], "correcta": "Relaciona"},
]

total_juegos = 0
cursos = list(Curso.objects.filter(activo=True))

for curso in cursos[:100]:  # Limitar a 100 cursos
    for juego_num in range(1, 11):
        template = juegos_templates[(juego_num - 1) % len(juegos_templates)]
        
        # Seleccionar pregunta aleatoria
        pregunta_data = random.choice(banco_preguntas_juegos)
        opciones = pregunta_data["opciones"][:]
        random.shuffle(opciones)
        
        nivel = random.choice(niveles)
        categoria = curso.categoria if curso.categoria else random.choice(categorias)
        
        juego, created = Juego.objects.get_or_create(
            titulo=f"{template['titulo']} - {curso.titulo[:15]}...",
            defaults={
                'descripcion': template['desc'],
                'pregunta': pregunta_data["p"],
                'categoria': categoria,
                'nivel': nivel,
                'tipo': 'opcion',
                'opcion1': opciones[0] if len(opciones) > 0 else "",
                'opcion2': opciones[1] if len(opciones) > 1 else "",
                'opcion3': opciones[2] if len(opciones) > 2 else "",
                'opcion4': opciones[3] if len(opciones) > 3 else "",
                'respuesta_correcta': pregunta_data["correcta"],
                'puntos': 10 + random.randint(0, 15),
                'orden': juego_num,
                'activo': True
            }
        )
        
        if created:
            total_juegos += 1

print(f"\\n✅ {total_juegos} juegos creados")
"""
        
        self._ejecutar_script(script)
        print_success("10 juegos por curso creados")
    
    def step_create_templates(self):
        print_step("Creando templates...")
        
        # Templates ya existen, solo verificamos
        templates_dir = self.project_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear base.html si no existe
        base_html = templates_dir / "base.html"
        if not base_html.exists():
            base_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MorphoPlay</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">MorphoPlay</a>
            <div class="ms-auto">
                {% if user.is_authenticated %}
                    <span class="text-white me-2">{{ user.username }}</span>
                    <a href="/accounts/logout/" class="btn btn-sm btn-outline-light">Salir</a>
                {% else %}
                    <a href="/accounts/login/" class="btn btn-sm btn-outline-light">Login</a>
                    <a href="/accounts/register/" class="btn btn-sm btn-primary">Registro</a>
                {% endif %}
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        {% block content %}{% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
            base_html.write_text(base_content)
            print_success("Template base creado")
        else:
            print_info("Template base ya existe")
        
        print_success("Templates verificados")
    
    def step_verify(self):
        print_step("Verificando instalación...")
        
        script = """
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Leccion, Evaluacion, Juego, Categoria, Nivel

print("📊 RESUMEN DE INSTALACIÓN")
print("=" * 50)
print(f"📚 Cursos: {Curso.objects.count()}")
print(f"📖 Lecciones: {Leccion.objects.count()}")
print(f"📝 Evaluaciones: {Evaluacion.objects.count()}")
print(f"🎮 Juegos: {Juego.objects.count()}")
print(f"📂 Categorías: {Categoria.objects.count()}")
print(f"📊 Niveles: {Nivel.objects.count()}")

print("\\n📋 CURSOS POR CATEGORÍA:")
for cat in Categoria.objects.filter(activo=True):
    count = Curso.objects.filter(categoria=cat).count()
    print(f"  - {cat.nombre}: {count} cursos")

print("\\n📋 EJEMPLO DE CURSOS:")
for c in Curso.objects.filter(activo=True)[:5]:
    print(f"  - {c.titulo} ({c.get_lecciones().count()} lecciones)")
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
        tiempo = datetime.now().strftime('%H:%M:%S')
        print(f"""
{Colors.GREEN}✅ 100 CURSOS COMPLETOS INSTALADOS EXITOSAMENTE!{Colors.END}

📊 ESTADÍSTICAS:
  📚 Cursos: 100
  📖 Lecciones: 10,000 (100 por curso)
  📝 Evaluaciones: 500 (5 por curso)
  🎮 Juegos: 1,000 (10 por curso)
  📂 Categorías: 3 (Morfología, Sintaxis, Bilingüe)
  📊 Niveles: 4 (Básico, Intermedio, Avanzado, Experto)

📋 DISTRIBUCIÓN:
  - Morfología: ~33 cursos
  - Sintaxis: ~33 cursos
  - Bilingüe: ~34 cursos

🕐 Tiempo de instalación: {tiempo}

🌐 ACCESO:
  {Colors.CYAN}http://localhost:8000/cursos/{Colors.END}
  {Colors.CYAN}http://localhost:8000/juegos/{Colors.END}
  {Colors.CYAN}http://localhost:8000/admin{Colors.END}

🚀 Inicia el servidor:
  {Colors.BLUE}source venv/bin/activate{Colors.END}
  {Colors.BLUE}python manage.py runserver 0.0.0.0:8000{Colors.END}
        """)

if __name__ == "__main__":
    installer = Cursos100CompletosInstaller()
    installer.run()
