#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MORPHOPLAY - INSTALADOR DE CURSOS COMPLETOS v5.0
Carga todos los cursos anteriores con templates, rutas, lecciones y evaluaciones
"""

import os
import sys
import subprocess
import json
from pathlib import Path

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

class CursoInstaller:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.venv_dir = self.project_dir / "venv"
        self.python_path = None
        
    def run(self):
        print_header("📚 INSTALADOR DE CURSOS COMPLETOS - MORPHOPLAY v5.0")
        print(f"📁 Directorio: {self.project_dir}\n")
        
        try:
            # Paso 1: Verificar entorno
            self.step_verify_env()
            
            # Paso 2: Crear cursos
            self.step_create_cursos()
            
            # Paso 3: Crear lecciones
            self.step_create_lecciones()
            
            # Paso 4: Crear evaluaciones
            self.step_create_evaluaciones()
            
            # Paso 5: Crear juegos
            self.step_create_juegos()
            
            # Paso 6: Crear templates
            self.step_create_templates()
            
            # Paso 7: Crear rutas (URLs)
            self.step_create_urls()
            
            # Paso 8: Verificar instalación
            self.step_verify()
            
            print_header("🎉 CURSOS INSTALADOS EXITOSAMENTE")
            self.print_summary()
            
        except KeyboardInterrupt:
            print_error("\nInstalación cancelada")
            sys.exit(1)
        except Exception as e:
            print_error(f"Error: {str(e)}")
            sys.exit(1)
    
    def step_verify_env(self):
        print_step("Verificando entorno...")
        
        # Activar entorno virtual
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
    
    def step_create_cursos(self):
        print_step("Creando cursos...")
        
        script = """
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Categoria, Nivel

print("📚 Creando cursos...")

# Obtener categorías y niveles
categorias = {}
for c in Categoria.objects.all():
    categorias[c.nombre] = c

niveles = {}
for n in Nivel.objects.all():
    niveles[n.nombre] = n

# Datos de cursos
cursos_data = [
    {
        "titulo": "Morfología del Castellano",
        "desc": "Curso completo sobre la estructura de las palabras en español. Aprende prefijos, sufijos, raíces y formación de palabras.",
        "cat": "Morfología",
        "nivel": "Básico",
        "duracion": 10,
        "orden": 1
    },
    {
        "titulo": "Sintaxis del Castellano",
        "desc": "Curso completo sobre la estructura de las oraciones en español. Aprende sujeto, predicado, complementos y análisis sintáctico.",
        "cat": "Sintaxis",
        "nivel": "Intermedio",
        "duracion": 12,
        "orden": 2
    },
    {
        "titulo": "English Grammar",
        "desc": "Curso completo de gramática inglesa para hispanohablantes. Aprende tiempos verbales, estructuras, y uso práctico.",
        "cat": "Inglés",
        "nivel": "Intermedio",
        "duracion": 15,
        "orden": 3
    },
    {
        "titulo": "Cognados Español-Inglés",
        "desc": "Aprende palabras que son similares en español e inglés. ¡Expande tu vocabulario bilingüe!",
        "cat": "Bilingüe",
        "nivel": "Básico",
        "duracion": 8,
        "orden": 4
    },
    {
        "titulo": "Técnicas Narrativas en Literatura",
        "desc": "Explora las técnicas literarias utilizadas por los grandes escritores. Aprende punto de vista, estructura y recursos.",
        "cat": "Literatura",
        "nivel": "Avanzado",
        "duracion": 14,
        "orden": 5
    },
    {
        "titulo": "Gramática Comparada: Español vs Inglés",
        "desc": "Compara las estructuras gramaticales del español y el inglés. Aprende las diferencias clave entre ambos idiomas.",
        "cat": "Bilingüe",
        "nivel": "Avanzado",
        "duracion": 16,
        "orden": 6
    }
]

creados = 0
for data in cursos_data:
    try:
        curso, created = Curso.objects.get_or_create(
            titulo=data["titulo"],
            defaults={
                "descripcion": data["desc"],
                "categoria": categorias.get(data["cat"]),
                "nivel": niveles.get(data["nivel"]),
                "duracion_estimada": data["duracion"],
                "orden": data["orden"],
                "activo": True
            }
        )
        if created:
            print(f"  ✅ {data['titulo']}")
            creados += 1
        else:
            print(f"  ⏳ {data['titulo']} (ya existe)")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")

print(f"✅ {creados} cursos creados/verificados")
"""
        
        self._ejecutar_script(script)
    
    def step_create_lecciones(self):
        print_step("Creando lecciones para todos los cursos...")
        
        script = """
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Leccion

print("📖 Creando lecciones...")

lecciones_data = {
    "Morfología del Castellano": [
        {"titulo": "Introducción a la Morfología", "contenido": "📖 INTRODUCCIÓN A LA MORFOLOGÍA\\n\\nLa morfología es la parte de la lingüística que estudia la estructura interna de las palabras.\\n\\nConceptos clave:\\n• Lexema/Raíz: Parte que contiene el significado básico\\n• Morfema: Partes que añaden información gramatical\\n\\nEjemplos:\\n• cas + ita = casita\\n• perr + azo = perrazo\\n• in + útil = inútil", "orden": 1},
        {"titulo": "Prefijos en Español", "contenido": "🔤 PREFIJOS EN ESPAÑOL\\n\\nLos prefijos se añaden al INICIO de la palabra.\\n\\nTipos:\\n1. Negación: in-, des-, a-\\n2. Lugar: sub-, super-, ante-, post-\\n3. Tiempo: pre-, post-, re-\\n4. Cantidad: bi-, tri-, multi-\\n\\nEjemplos: inútil, subterráneo, prehistoria", "orden": 2},
        {"titulo": "Sufijos en Español", "contenido": "🔤 SUFIJOS EN ESPAÑOL\\n\\nLos sufijos se añaden al FINAL de la palabra.\\n\\nTipos:\\n1. Diminutivos: -ito, -illo, -ín\\n2. Aumentativos: -azo, -ón, -ote\\n3. Profesiones: -ero, -ista, -dor\\n4. Adjetivos: -oso, -able, -al\\n\\nEjemplos: casita, perrazo, panadero", "orden": 3},
        {"titulo": "Raíces y Formación de Palabras", "contenido": "🌱 RAÍCES Y FORMACIÓN DE PALABRAS\\n\\nLa raíz es el núcleo semántico.\\n\\nProcesos:\\n1. Derivación: añadir prefijos/sufijos\\n2. Composición: unir palabras\\n3. Parasíntesis: combinación\\n4. Acortamiento: reducir\\n\\nEjemplos: casita (derivación), abrelatas (composición)", "orden": 4}
    ],
    "Sintaxis del Castellano": [
        {"titulo": "La Oración y sus Partes", "contenido": "📖 LA ORACIÓN Y SUS PARTES\\n\\nLa oración tiene SUJETO y PREDICADO.\\n\\nEjemplo: 'El niño come pan'\\n- Sujeto: El niño\\n- Predicado: come pan", "orden": 1},
        {"titulo": "El Sujeto", "contenido": "👤 EL SUJETO\\n\\nTipos:\\n1. Expreso: aparece explícito\\n2. Elíptico: se sobreentiende\\n3. Simple: un núcleo\\n4. Compuesto: varios núcleos\\n\\nEjemplos:\\n- El niño juega (expreso)\\n- (Yo) como (elíptico)", "orden": 2},
        {"titulo": "El Predicado", "contenido": "📝 EL PREDICADO\\n\\nTipos:\\n1. Verbal: verbo predicativo\\n2. Nominal: verbo copulativo\\n\\nComplementos:\\n- CD: recibe la acción\\n- CI: destinatario\\n- CC: circunstancias\\n- Atributo: con ser/estar", "orden": 3},
        {"titulo": "Análisis Sintáctico", "contenido": "🔍 ANÁLISIS SINTÁCTICO\\n\\nPasos:\\n1. Identificar el verbo\\n2. Identificar el sujeto\\n3. Identificar complementos\\n\\nEjemplo: 'María dio el libro a Juan'\\n- Verbo: dio\\n- Sujeto: María\\n- CD: el libro\\n- CI: a Juan", "orden": 4}
    ],
    "English Grammar": [
        {"titulo": "Present Simple", "contenido": "📖 PRESENT SIMPLE\\n\\nUsos: hábitos y verdades generales.\\n\\nEstructura:\\n- Afirmativo: I work\\n- Negativo: I don't work\\n- Interrogativo: Do you work?\\n\\nEjemplos:\\n- I go to school every day.\\n- Water boils at 100°C.", "orden": 1},
        {"titulo": "Past Simple", "contenido": "📖 PAST SIMPLE\\n\\nUsos: acciones completadas en el pasado.\\n\\nEstructura:\\n- Afirmativo: I worked\\n- Negativo: I didn't work\\n- Interrogativo: Did you work?\\n\\nIrregulares: go→went, eat→ate", "orden": 2},
        {"titulo": "Present Perfect", "contenido": "📖 PRESENT PERFECT\\n\\nUsos: experiencias y acciones que continúan.\\n\\nEstructura:\\n- Afirmativo: I have visited\\n- Negativo: I haven't visited\\n- Interrogativo: Have you visited?\\n\\nPalabras clave: ever, never, already, yet", "orden": 3},
        {"titulo": "Future Tenses", "contenido": "📖 FUTURE TENSES\\n\\nWILL: decisiones espontáneas y predicciones.\\nGOING TO: planes e intenciones.\\n\\nEjemplos:\\n- I will help you.\\n- I am going to study.", "orden": 4}
    ],
    "Cognados Español-Inglés": [
        {"titulo": "Cognados Perfectos", "contenido": "🌟 COGNADOS PERFECTOS\\n\\nPalabras que se escriben igual en ambos idiomas.\\n\\nEjemplos:\\n- animal = animal\\n- color = color\\n- doctor = doctor\\n- importante = important", "orden": 1},
        {"titulo": "Cognados Parciales", "contenido": "🌟 COGNADOS PARCIALES\\n\\nPalabras similares con pequeñas diferencias.\\n\\nEjemplos:\\n- family / familia\\n- different / diferente\\n- excellent / excelente", "orden": 2},
        {"titulo": "Falsos Amigos", "contenido": "⚠️ FALSOS AMIGOS\\n\\nPalabras que parecen iguales pero significan diferente.\\n\\nEjemplos:\\n- embarrassed NO es embarazada\\n- carpet NO es carpeta\\n- exit NO es éxito", "orden": 3}
    ],
    "Técnicas Narrativas en Literatura": [
        {"titulo": "Introducción a la Narrativa", "contenido": "📖 INTRODUCCIÓN A LA NARRATIVA\\n\\nElementos:\\n- Narrador\\n- Personajes\\n- Acción\\n- Tiempo\\n- Espacio", "orden": 1},
        {"titulo": "Punto de Vista Narrativo", "contenido": "👁️ PUNTO DE VISTA\\n\\nTipos:\\n- Primera persona (protagonista)\\n- Segunda persona (tú)\\n- Tercera persona (omnisciente)", "orden": 2},
        {"titulo": "Estructura del Relato", "contenido": "📋 ESTRUCTURA DEL RELATO\\n\\nPartes:\\n1. Planteamiento\\n2. Nudo\\n3. Desenlace", "orden": 3},
        {"titulo": "Recursos Literarios", "contenido": "🎨 RECURSOS LITERARIOS\\n\\nFiguras retóricas:\\n- Metáfora\\n- Símil\\n- Hipérbole\\n- Personificación\\n- Ironía", "orden": 4}
    ],
    "Gramática Comparada: Español vs Inglés": [
        {"titulo": "Orden de las Palabras", "contenido": "📝 ORDEN DE LAS PALABRAS\\n\\nDiferencias:\\n- Español: 'El perro grande'\\n- Inglés: 'The big dog'", "orden": 1},
        {"titulo": "Tiempos Verbales Comparados", "contenido": "⏰ TIEMPOS VERBALES\\n\\nComparación:\\n- Presente: hablo / I speak\\n- Pasado: hablé / I spoke\\n- Futuro: hablaré / I will speak", "orden": 2},
        {"titulo": "Estructuras Comunes", "contenido": "📝 ESTRUCTURAS COMUNES\\n\\nDiferencias clave:\\n- Uso de 'haber' vs 'have'\\n- Verbos reflexivos en español\\n- Subjuntivo en español", "orden": 3},
        {"titulo": "Errores Comunes", "contenido": "❌ ERRORES COMUNES\\n\\nEjemplos:\\n- 'I am agree' → I agree\\n- 'I have 20 years' → I am 20 years old\\n- 'I am hungry' → I am hungry", "orden": 4}
    ]
}

for curso_titulo, lecciones in lecciones_data.items():
    try:
        curso = Curso.objects.get(titulo=curso_titulo)
        for lec in lecciones:
            obj, created = Leccion.objects.get_or_create(
                curso=curso,
                titulo=lec["titulo"],
                defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
            )
            if created:
                print(f"  ✅ {lec['titulo']} ({curso_titulo})")
    except Curso.DoesNotExist:
        print(f"  ⏳ Curso no encontrado: {curso_titulo}")

print("✅ Lecciones creadas/verificadas")
"""
        
        self._ejecutar_script(script)
    
    def step_create_evaluaciones(self):
        print_step("Creando evaluaciones...")
        
        script = """
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Evaluacion, PreguntaEvaluacion

print("📝 Creando evaluaciones...")

cursos = Curso.objects.filter(activo=True)

for curso in cursos:
    # Verificar si ya tiene evaluaciones
    if curso.evaluaciones.count() > 0:
        print(f"  ⏳ {curso.titulo} (ya tiene evaluaciones)")
        continue
    
    # Crear evaluación
    eval_obj = Evaluacion.objects.create(
        curso=curso,
        titulo=f"Evaluación de {curso.titulo}",
        descripcion=f"Pon a prueba tus conocimientos sobre {curso.titulo.lower()}",
        tipo="sumativa",
        puntaje_maximo=100,
        tiempo_limite=30,
        intentos_permitidos=2,
        orden=1
    )
    
    print(f"  ✅ {curso.titulo}")
    
    # Crear preguntas genéricas
    preguntas = [
        {"p": f"¿Cuál es el tema principal de {curso.titulo}?", "opciones": ["Tema 1", "Tema 2", "Tema 3", "Tema 4"], "correcta": "Tema 1"},
        {"p": "¿Qué nivel tiene este curso?", "opciones": ["Básico", "Intermedio", "Avanzado", "Experto"], "correcta": str(curso.nivel)},
        {"p": "¿Cuántas lecciones tiene este curso?", "opciones": ["2", "3", "4", "5"], "correcta": str(curso.get_lecciones().count())},
        {"p": "¿Qué categoría tiene este curso?", "opciones": ["Morfología", "Sintaxis", "Gramática", str(curso.categoria)], "correcta": str(curso.categoria)},
        {"p": "¿Cuántas horas dura este curso?", "opciones": ["5", "10", "15", "20"], "correcta": str(curso.duracion_estimada)},
    ]
    
    for p in preguntas:
        PreguntaEvaluacion.objects.create(
            evaluacion=eval_obj,
            tipo="opcion",
            pregunta=p["p"],
            opcion1=p["opciones"][0],
            opcion2=p["opciones"][1],
            opcion3=p["opciones"][2],
            opcion4=p["opciones"][3],
            respuesta_correcta=p["correcta"],
            puntaje=20,
            orden=1
        )
    
    print(f"    ✅ {len(preguntas)} preguntas creadas")

print("✅ Evaluaciones creadas/verificadas")
"""
        
        self._ejecutar_script(script)
    
    def step_create_juegos(self):
        print_step("Creando juegos...")
        
        script = """
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Juego, Categoria, Nivel

print("🎮 Creando juegos...")

try:
    basico = Nivel.objects.get(nombre="Básico")
    intermedio = Nivel.objects.get(nombre="Intermedio")
    avanzado = Nivel.objects.get(nombre="Avanzado")
except:
    basico = None
    intermedio = None
    avanzado = None

if not basico:
    print("⚠️ No se encontraron niveles")
    exit()

juegos_data = [
    # Morfología
    {"titulo": "Prefijos de Negación", "cat": "Morfología", "nivel": basico, "opciones": ["in-", "pre-", "post-", "sub-"], "correcta": "in-", "pts": 10},
    {"titulo": "Sufijos de Profesión", "cat": "Morfología", "nivel": basico, "opciones": ["-ero", "-ista", "-dor", "-ción"], "correcta": "-ista", "pts": 10},
    {"titulo": "Diminutivos en Español", "cat": "Morfología", "nivel": basico, "opciones": ["casota", "casita", "casona", "casaza"], "correcta": "casita", "pts": 10},
    # Sintaxis
    {"titulo": "Sujeto y Predicado", "cat": "Sintaxis", "nivel": basico, "opciones": ["El niño", "come pan", "pan", "El"], "correcta": "El niño", "pts": 10},
    {"titulo": "Complemento Directo", "cat": "Sintaxis", "nivel": intermedio, "opciones": ["Veo", "la casa", "casa", "la"], "correcta": "la casa", "pts": 15},
    # Inglés
    {"titulo": "Present Simple", "cat": "Inglés", "nivel": basico, "opciones": ["go", "goes", "going", "went"], "correcta": "go", "pts": 10},
    # Bilingüe
    {"titulo": "Cognados Perfectos", "cat": "Bilingüe", "nivel": basico, "opciones": ["animal", "animale", "anima", "animado"], "correcta": "animal", "pts": 10},
    {"titulo": "Falsos Amigos", "cat": "Bilingüe", "nivel": intermedio, "opciones": ["embarazada", "avergonzado", "empezado", "embrujado"], "correcta": "avergonzado", "pts": 15},
]

creados = 0
for data in juegos_data:
    try:
        cat = Categoria.objects.get(nombre=data["cat"])
        juego, created = Juego.objects.get_or_create(
            titulo=data["titulo"],
            defaults={
                "descripcion": data["titulo"],
                "pregunta": f"¿Qué es {data['titulo']}?",
                "categoria": cat,
                "nivel": data["nivel"],
                "tipo": "opcion",
                "opcion1": data["opciones"][0],
                "opcion2": data["opciones"][1],
                "opcion3": data["opciones"][2],
                "opcion4": data["opciones"][3],
                "respuesta_correcta": data["correcta"],
                "puntos": data["pts"],
                "activo": True
            }
        )
        if created:
            print(f"  ✅ {data['titulo']}")
            creados += 1
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")

print(f"✅ {creados} juegos creados/verificados")
"""
        
        self._ejecutar_script(script)
    
    def step_create_templates(self):
        print_step("Creando templates para cursos...")
        
        # Crear templates de cursos si no existen
        templates_dir = self.project_dir / "templates" / "cursos"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Template de lista de cursos
        list_html = """{% extends 'base.html' %}
{% load static %}

{% block title %}📚 Cursos - MorphoPlay{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col-12">
        <h2>📚 Cursos Disponibles</h2>
        <p class="text-secondary">Aprende con nuestros cursos estructurados</p>
    </div>
</div>

<div class="row g-4">
    {% for curso in cursos %}
    <div class="col-md-4">
        <div class="card h-100">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <span class="badge bg-primary">{{ curso.categoria.nombre|default:"General" }}</span>
                    <span class="badge bg-{% if curso.nivel.nombre == 'Básico' %}success{% elif curso.nivel.nombre == 'Intermedio' %}warning{% elif curso.nivel.nombre == 'Avanzado' %}danger{% else %}info{% endif %}">
                        {{ curso.nivel.nombre|default:"Básico" }}
                    </span>
                </div>
                <h5 class="card-title mt-2">{{ curso.titulo }}</h5>
                <p class="card-text text-secondary small">{{ curso.descripcion|truncatechars:100 }}</p>
                <div class="d-flex justify-content-between align-items-center mt-2">
                    <div>
                        <span class="badge bg-info">{{ curso.get_lecciones.count }} lecciones</span>
                        <span class="badge bg-secondary">⏱ {{ curso.duracion_estimada }}h</span>
                    </div>
                    <a href="/cursos/{{ curso.id }}/" class="btn btn-sm btn-primary">
                        <i class="fas fa-eye"></i> Ver Curso
                    </a>
                </div>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12 text-center py-5">
        <i class="fas fa-book-open fa-3x text-secondary mb-3"></i>
        <h4>No hay cursos disponibles</h4>
        <p class="text-secondary">Pronto agregaremos nuevos cursos.</p>
    </div>
    {% endfor %}
</div>
{% endblock %}
"""
        (templates_dir / "list.html").write_text(list_html)
        print_success("Template de lista de cursos creado")
        
        # Template de detalle de curso
        detail_html = """{% extends 'base.html' %}
{% load static %}

{% block title %}{{ curso.titulo }} - MorphoPlay{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="/cursos/">Cursos</a></li>
                <li class="breadcrumb-item active">{{ curso.titulo }}</li>
            </ol>
        </nav>

        <div class="card mb-4">
            <div class="card-body">
                <h2>{{ curso.titulo }}</h2>
                <p class="text-secondary">{{ curso.descripcion }}</p>
                <div class="d-flex flex-wrap gap-2">
                    <span class="badge bg-primary">{{ curso.categoria.nombre|default:"General" }}</span>
                    <span class="badge bg-info">{{ curso.nivel.nombre|default:"Básico" }}</span>
                    <span class="badge bg-secondary">⏱ {{ curso.duracion_estimada }} horas</span>
                    <span class="badge bg-success">
                        {{ progreso.get_estado_display|default:"No iniciado" }}
                    </span>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-8">
                <h4>📖 Lecciones</h4>
                <div class="list-group">
                    {% for leccion in lecciones %}
                    <a href="/cursos/{{ curso.id }}/leccion/{{ leccion.id }}/" 
                       class="list-group-item list-group-item-action">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <span class="badge bg-secondary me-2">{{ forloop.counter }}</span>
                                {{ leccion.titulo }}
                            </div>
                            <i class="fas fa-chevron-right text-secondary"></i>
                        </div>
                    </a>
                    {% empty %}
                    <p class="text-secondary">No hay lecciones disponibles</p>
                    {% endfor %}
                </div>
            </div>

            <div class="col-md-4">
                <h4>📝 Evaluaciones</h4>
                <div class="list-group mb-3">
                    {% for evaluacion in evaluaciones %}
                    <a href="/cursos/{{ curso.id }}/evaluacion/{{ evaluacion.id }}/" 
                       class="list-group-item list-group-item-action">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                {{ evaluacion.titulo }}
                                <span class="badge bg-secondary ms-2">{{ evaluacion.get_tipo_display }}</span>
                            </div>
                            <i class="fas fa-chevron-right text-secondary"></i>
                        </div>
                    </a>
                    {% empty %}
                    <p class="text-secondary">No hay evaluaciones disponibles</p>
                    {% endfor %}
                </div>

                <div class="card">
                    <div class="card-body">
                        <h5>📊 Progreso</h5>
                        <div class="progress mb-2">
                            <div class="progress-bar" style="width: {% widthratio progreso.lecciones_completadas lecciones_count 100 %}%;"></div>
                        </div>
                        <p class="text-secondary small">
                            {{ progreso.lecciones_completadas }}/{{ lecciones_count }} lecciones
                        </p>
                        <span class="badge bg-{% if progreso.estado == 'completado' %}success{% elif progreso.estado == 'en_progreso' %}warning{% else %}secondary{% endif %}">
                            {{ progreso.get_estado_display|default:"No iniciado" }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
        (templates_dir / "detail.html").write_text(detail_html)
        print_success("Template de detalle de curso creado")
        
        # Template de lección
        leccion_html = """{% extends 'base.html' %}
{% load static %}

{% block title %}{{ leccion.titulo }} - {{ curso.titulo }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="/cursos/">Cursos</a></li>
                <li class="breadcrumb-item"><a href="/cursos/{{ curso.id }}/">{{ curso.titulo }}</a></li>
                <li class="breadcrumb-item active">{{ leccion.titulo }}</li>
            </ol>
        </nav>

        <div class="card mb-4">
            <div class="card-header">
                <div class="d-flex justify-content-between align-items-center">
                    <h4 class="mb-0">{{ leccion.titulo }}</h4>
                    <span class="badge bg-secondary">Lección {{ leccion.orden }}</span>
                </div>
            </div>
            <div class="card-body">
                <div class="mt-3">
                    {{ leccion.contenido|linebreaks }}
                </div>
            </div>
        </div>

        <div class="d-flex justify-content-between align-items-center">
            <div>
                {% if anterior %}
                <a href="/cursos/{{ curso.id }}/leccion/{{ anterior.id }}/" class="btn btn-outline-primary">
                    <i class="fas fa-arrow-left"></i> Anterior
                </a>
                {% endif %}
            </div>
            <div>
                <span class="text-secondary">
                    Lección {{ leccion.orden }} de {{ lecciones_count|default:"?" }}
                </span>
            </div>
            <div>
                {% if siguiente %}
                <a href="/cursos/{{ curso.id }}/leccion/{{ siguiente.id }}/" class="btn btn-primary">
                    Siguiente <i class="fas fa-arrow-right"></i>
                </a>
                {% else %}
                <a href="/cursos/{{ curso.id }}/" class="btn btn-success">
                    <i class="fas fa-check"></i> Completar curso
                </a>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
        (templates_dir / "leccion.html").write_text(leccion_html)
        print_success("Template de lección creado")
        
        # Template de evaluación
        evaluacion_html = """{% extends 'base.html' %}
{% load static %}

{% block title %}{{ evaluacion.titulo }} - {{ curso.titulo }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="/cursos/">Cursos</a></li>
                <li class="breadcrumb-item"><a href="/cursos/{{ curso.id }}/">{{ curso.titulo }}</a></li>
                <li class="breadcrumb-item active">{{ evaluacion.titulo }}</li>
            </ol>
        </nav>

        <div class="card mb-4">
            <div class="card-header">
                <div class="d-flex justify-content-between align-items-center">
                    <h4 class="mb-0">{{ evaluacion.titulo }}</h4>
                    <span class="badge bg-primary">{{ evaluacion.get_tipo_display }}</span>
                </div>
            </div>
            <div class="card-body">
                <p class="text-secondary">{{ evaluacion.descripcion }}</p>
                <div class="d-flex gap-3 mb-3">
                    <span class="badge bg-info">⏱ {{ evaluacion.tiempo_limite }} minutos</span>
                    <span class="badge bg-warning text-dark">🎯 {{ evaluacion.puntaje_maximo }} puntos</span>
                    <span class="badge bg-secondary">Intentos restantes: {{ intentos_restantes }}</span>
                </div>
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i>
                    <strong>Instrucciones:</strong> Responde todas las preguntas.
                </div>
            </div>
        </div>

        <form method="post" action="/cursos/{{ curso.id }}/evaluacion/{{ evaluacion.id }}/submit/">
            {% csrf_token %}
            
            {% for pregunta in preguntas %}
            <div class="card mb-3">
                <div class="card-body">
                    <h6 class="card-title">
                        <span class="badge bg-secondary me-2">{{ forloop.counter }}</span>
                        {{ pregunta.pregunta }}
                        <span class="badge bg-info float-end">{{ pregunta.puntaje }} pts</span>
                    </h6>
                    
                    <div class="mt-2">
                        {% if pregunta.tipo == 'opcion' %}
                            {% for opcion in pregunta.get_opciones %}
                            {% if opcion %}
                            <div class="form-check">
                                <input class="form-check-input" type="radio" 
                                       name="pregunta_{{ pregunta.id }}" 
                                       id="pregunta_{{ pregunta.id }}_{{ forloop.counter }}"
                                       value="{{ opcion }}">
                                <label class="form-check-label" for="pregunta_{{ pregunta.id }}_{{ forloop.counter }}">
                                    {{ opcion }}
                                </label>
                            </div>
                            {% endif %}
                            {% endfor %}
                        {% endif %}
                    </div>
                </div>
            </div>
            {% empty %}
            <p class="text-secondary">No hay preguntas en esta evaluación.</p>
            {% endfor %}

            {% if preguntas %}
            <div class="text-center">
                <button type="submit" class="btn btn-success btn-lg">
                    <i class="fas fa-paper-plane"></i> Enviar
                </button>
                <a href="/cursos/{{ curso.id }}/" class="btn btn-outline-secondary btn-lg">
                    <i class="fas fa-times"></i> Cancelar
                </a>
            </div>
            {% endif %}
        </form>
    </div>
</div>
{% endblock %}
"""
        (templates_dir / "evaluacion.html").write_text(evaluacion_html)
        print_success("Template de evaluación creado")
    
    def step_create_urls(self):
        print_step("Creando URLs para cursos...")
        
        urls_content = """
# URLs para cursos (agregar a morphoplay/urls.py)
# path('cursos/', views.cursos_list, name='cursos_list'),
# path('cursos/<int:curso_id>/', views.curso_detail, name='curso_detail'),
# path('cursos/<int:curso_id>/leccion/<int:leccion_id>/', views.leccion_detail, name='leccion'),
# path('cursos/<int:curso_id>/evaluacion/<int:evaluacion_id>/', views.evaluacion_detail, name='evaluacion'),
# path('cursos/<int:curso_id>/evaluacion/<int:evaluacion_id>/submit/', views.submit_evaluacion, name='submit_evaluacion'),
"""
        
        urls_file = self.project_dir / "scripts" / "urls_cursos.txt"
        urls_file.parent.mkdir(parents=True, exist_ok=True)
        urls_file.write_text(urls_content)
        print_success("URLs de cursos documentadas")
    
    def step_verify(self):
        print_step("Verificando instalación...")
        
        script = """
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Leccion, Evaluacion, Juego

print("📊 VERIFICANDO INSTALACIÓN:")
print(f"📚 Cursos: {Curso.objects.count()}")
print(f"📖 Lecciones: {Leccion.objects.count()}")
print(f"📝 Evaluaciones: {Evaluacion.objects.count()}")
print(f"🎮 Juegos: {Juego.objects.count()}")

print("\\n📋 CURSOS:")
for c in Curso.objects.filter(activo=True):
    print(f"  - {c.titulo} ({c.get_lecciones().count()} lecciones, {c.evaluaciones.count()} evaluaciones)")
"""
        
        self._ejecutar_script(script)
    
    def _ejecutar_script(self, script):
        """Ejecuta un script de Python en el entorno adecuado"""
        if self.python_path:
            # Crear archivo temporal
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
{Colors.GREEN}✅ Cursos instalados exitosamente!{Colors.END}

📚 Cursos creados:
  1. Morfología del Castellano (4 lecciones)
  2. Sintaxis del Castellano (4 lecciones)
  3. English Grammar (4 lecciones)
  4. Cognados Español-Inglés (3 lecciones)
  5. Técnicas Narrativas en Literatura (4 lecciones)
  6. Gramática Comparada: Español vs Inglés (4 lecciones)

📝 Templates creados:
  - cursos/list.html
  - cursos/detail.html
  - cursos/leccion.html
  - cursos/evaluacion.html

🎮 Juegos creados:
  - 8 juegos en diferentes categorías

🔑 Credenciales:
  {Colors.YELLOW}Usuario: admin{Colors.END}
  {Colors.YELLOW}Contraseña: admin123{Colors.END}

🌐 Acceso:
  {Colors.CYAN}http://localhost:8000/cursos/{Colors.END}
  {Colors.CYAN}http://localhost:8000/admin{Colors.END}

🚀 Inicia el servidor:
  {Colors.BLUE}source venv/bin/activate{Colors.END}
  {Colors.BLUE}python manage.py runserver 0.0.0.0:8000{Colors.END}
        """)

if __name__ == "__main__":
    installer = CursoInstaller()
    installer.run()
