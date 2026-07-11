#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MORPHOPLAY - INSTALADOR DE EVALUACIONES Y JUEGOS ILIMITADOS v7.0
Genera evaluaciones y juegos ilimitados con templates, rutas y contenido lúdico
"""

import os
import sys
import subprocess
import json
import random
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

class EvaluacionesJuegosInstaller:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.venv_dir = self.project_dir / "venv"
        self.python_path = None
        
    def run(self):
        print_header("🎮 INSTALADOR DE EVALUACIONES Y JUEGOS ILIMITADOS - v7.0")
        print(f"📁 Directorio: {self.project_dir}\n")
        
        try:
            # Paso 1: Verificar entorno
            self.step_verify_env()
            
            # Paso 2: Crear evaluaciones ilimitadas
            self.step_create_evaluaciones()
            
            # Paso 3: Crear juegos ilimitados
            self.step_create_juegos()
            
            # Paso 4: Crear templates lúdicos
            self.step_create_templates()
            
            # Paso 5: Crear rutas
            self.step_create_urls()
            
            # Paso 6: Verificar instalación
            self.step_verify()
            
            print_header("🎉 EVALUACIONES Y JUEGOS INSTALADOS EXITOSAMENTE")
            self.print_summary()
            
        except KeyboardInterrupt:
            print_error("\nInstalación cancelada")
            sys.exit(1)
        except Exception as e:
            print_error(f"Error: {str(e)}")
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
    
    def step_create_evaluaciones(self):
        print_step("Creando evaluaciones ilimitadas...")
        
        script = """
import django
import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Evaluacion, PreguntaEvaluacion

print("📝 Creando evaluaciones ilimitadas...")

cursos = list(Curso.objects.filter(activo=True))

if not cursos:
    print("⚠️ No hay cursos disponibles")
    exit()

# Bancos de preguntas por categoría
banco_preguntas = {
    "Morfología": [
        {"p": "¿Qué es un lexema?", "opciones": ["Significado básico", "Sufijo", "Prefijo", "Morfema"], "correcta": "Significado básico"},
        {"p": "¿Qué es un prefijo?", "opciones": ["Se añade al inicio", "Se añade al final", "Es la raíz", "Es un morfema"], "correcta": "Se añade al inicio"},
        {"p": "¿Qué es un sufijo?", "opciones": ["Se añade al final", "Se añade al inicio", "Es la raíz", "Es un lexema"], "correcta": "Se añade al final"},
        {"p": "¿Qué es un morfema?", "opciones": ["Parte gramatical", "Raíz", "Prefijo", "Sufijo"], "correcta": "Parte gramatical"},
        {"p": "Ejemplo de prefijo:", "opciones": ["-ito", "pre-", "-ción", "-mente"], "correcta": "pre-"},
    ],
    "Sintaxis": [
        {"p": "¿Qué es el sujeto?", "opciones": ["Quien realiza la acción", "El verbo", "El complemento", "El predicado"], "correcta": "Quien realiza la acción"},
        {"p": "¿Qué es el predicado?", "opciones": ["Lo que se dice del sujeto", "El sujeto", "El complemento", "El verbo"], "correcta": "Lo que se dice del sujeto"},
        {"p": "¿Qué es el complemento directo?", "opciones": ["Recibe la acción", "Indica el destinatario", "Expresa circunstancias", "Modifica al sujeto"], "correcta": "Recibe la acción"},
        {"p": "En 'Vino ayer', 'ayer' es:", "opciones": ["CD", "CI", "CC Tiempo", "Atributo"], "correcta": "CC Tiempo"},
        {"p": "¿Cuál es una oración simple?", "opciones": ["Juan estudia", "Juan estudia y María trabaja", "Dijo que vendría", "Llegó, saludó"], "correcta": "Juan estudia"},
    ],
    "Gramática": [
        {"p": "¿Qué es un verbo?", "opciones": ["Acción o estado", "Sustantivo", "Adjetivo", "Adverbio"], "correcta": "Acción o estado"},
        {"p": "¿Qué es un sustantivo?", "opciones": ["Nombre de persona, lugar o cosa", "Acción", "Cualidad", "Circunstancia"], "correcta": "Nombre de persona, lugar o cosa"},
        {"p": "¿Qué es un adjetivo?", "opciones": ["Modifica al sustantivo", "Modifica al verbo", "Modifica al adverbio", "Es el sujeto"], "correcta": "Modifica al sustantivo"},
        {"p": "¿Qué es un adverbio?", "opciones": ["Modifica al verbo", "Modifica al sustantivo", "Modifica al adjetivo", "Es el complemento"], "correcta": "Modifica al verbo"},
        {"p": "¿Qué es una preposición?", "opciones": ["Relaciona elementos", "Sustituye al sustantivo", "Expresa acción", "Modifica al verbo"], "correcta": "Relaciona elementos"},
    ],
    "Literatura": [
        {"p": "¿Qué es la metáfora?", "opciones": ["Identificación de términos", "Comparación con 'como'", "Exageración", "Atribuir cualidades humanas"], "correcta": "Identificación de términos"},
        {"p": "¿Qué es el símil?", "opciones": ["Comparación con 'como'", "Identificación de términos", "Exageración", "Atribuir cualidades humanas"], "correcta": "Comparación con 'como'"},
        {"p": "¿Qué es la hipérbole?", "opciones": ["Exageración", "Comparación con 'como'", "Identificación de términos", "Atribuir cualidades humanas"], "correcta": "Exageración"},
        {"p": "¿Qué es la personificación?", "opciones": ["Atribuir cualidades humanas", "Exageración", "Comparación con 'como'", "Identificación de términos"], "correcta": "Atribuir cualidades humanas"},
        {"p": "¿Qué es el narrador omnisciente?", "opciones": ["Lo sabe todo", "Observa desde fuera", "Cuenta su historia", "Es inocente"], "correcta": "Lo sabe todo"},
    ],
    "Inglés": [
        {"p": "I ___ to school every day.", "opciones": ["go", "goes", "going", "went"], "correcta": "go"},
        {"p": "She ___ English.", "opciones": ["study", "studies", "studing", "studys"], "correcta": "studies"},
        {"p": "I ___ to Paris last year.", "opciones": ["go", "went", "gone", "going"], "correcta": "went"},
        {"p": "I have never ___ sushi.", "opciones": ["eat", "ate", "eaten", "eating"], "correcta": "eaten"},
        {"p": "I ___ help you.", "opciones": ["will", "am going to", "going to", "go to"], "correcta": "will"},
    ],
    "Bilingüe": [
        {"p": "¿Cuál es el cognado de 'animal'?", "opciones": ["animal", "animale", "anima", "animado"], "correcta": "animal"},
        {"p": "¿Qué significa 'embarrassed'?", "opciones": ["embarazada", "avergonzado", "empezado", "embrujado"], "correcta": "avergonzado"},
        {"p": "¿Cuál es el cognado de 'family'?", "opciones": ["familia", "familiar", "famoso", "falda"], "correcta": "familia"},
        {"p": "¿Qué significa 'carpet'?", "opciones": ["carpeta", "alfombra", "carpintero", "carpa"], "correcta": "alfombra"},
        {"p": "¿Cuál es el cognado de 'excellent'?", "opciones": ["excelente", "excellent", "exelente", "excelent"], "correcta": "excelente"},
    ]
}

# Generar evaluaciones para cada curso
total_evaluaciones = 0
for curso in cursos:
    categoria_nombre = curso.categoria.nombre if curso.categoria else "General"
    
    # Obtener preguntas de la categoría
    preguntas_base = banco_preguntas.get(categoria_nombre, banco_preguntas["Gramática"])
    
    # Crear 5 evaluaciones por curso (o tantas como quieras)
    for i in range(5):
        eval_titulo = f"🎯 Evaluación {i+1}: {categoria_nombre} - Nivel {i+1}"
        
        eval_obj = Evaluacion.objects.create(
            curso=curso,
            titulo=eval_titulo,
            descripcion=f"Evaluación lúdica sobre {categoria_nombre.lower()} - Nivel {i+1}",
            tipo="formativa" if i < 2 else "sumativa",
            puntaje_maximo=100,
            tiempo_limite=15 + (i * 5),
            intentos_permitidos=3,
            orden=i+1
        )
        
        # Seleccionar preguntas aleatorias
        preguntas_seleccionadas = random.sample(preguntas_base, min(5, len(preguntas_base)))
        
        for j, p in enumerate(preguntas_seleccionadas, 1):
            # Mezclar opciones para más variedad
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
        print(f"  ✅ {eval_titulo}")

print(f"\\n✅ {total_evaluaciones} evaluaciones creadas")
"""
        
        self._ejecutar_script(script)
        print_success("Evaluaciones ilimitadas creadas")
    
    def step_create_juegos(self):
        print_step("Creando juegos ilimitados...")
        
        script = """
import django
import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Juego, Categoria, Nivel

print("🎮 Creando juegos ilimitados...")

categorias = list(Categoria.objects.filter(activo=True))
niveles = list(Nivel.objects.filter(activo=True))

if not categorias or not niveles:
    print("⚠️ No hay categorías o niveles disponibles")
    exit()

# Bancos de juegos por categoría
juegos_data = {
    "Morfología": [
        {"titulo": "🏆 Carrera de Prefijos", "desc": "Elige el prefijo correcto", "pregunta": "¿Qué prefijo significa 'no'?", "opciones": ["in-", "pre-", "post-", "sub-"], "correcta": "in-"},
        {"titulo": "🎯 Caza de Sufijos", "desc": "Identifica el sufijo correcto", "pregunta": "¿Qué sufijo forma diminutivos?", "opciones": ["-ito", "-azo", "-ción", "-mente"], "correcta": "-ito"},
        {"titulo": "🧩 Rompecabezas de Palabras", "desc": "Encuentra la raíz", "pregunta": "¿Cuál es la raíz de 'casita'?", "opciones": ["cas", "ita", "casa", "sit"], "correcta": "cas"},
        {"titulo": "🎲 Dados de Morfemas", "desc": "Identifica el morfema", "pregunta": "En 'inútil', 'in-' es:", "opciones": ["Prefijo", "Sufijo", "Raíz", "Lexema"], "correcta": "Prefijo"},
    ],
    "Sintaxis": [
        {"titulo": "🎯 Tiro al Sujeto", "desc": "Identifica el sujeto", "pregunta": "En 'El niño come', el sujeto es:", "opciones": ["El niño", "come", "pan", "El"], "correcta": "El niño"},
        {"titulo": "🧩 Puzzle de Oraciones", "desc": "Arma la oración correcta", "pregunta": "¿Cuál es una oración simple?", "opciones": ["Juan estudia", "Juan estudia y María trabaja", "Dijo que vendría", "Llegó, saludó"], "correcta": "Juan estudia"},
        {"titulo": "🎲 Dados de Complementos", "desc": "Identifica el complemento", "pregunta": "En 'Vino ayer', 'ayer' es:", "opciones": ["CD", "CI", "CC Tiempo", "Atributo"], "correcta": "CC Tiempo"},
        {"titulo": "🏆 Copa del Análisis", "desc": "Analiza la oración", "pregunta": "En 'Doy el libro a Juan', el CI es:", "opciones": ["el libro", "a Juan", "Doy", "Juan"], "correcta": "a Juan"},
    ],
    "Gramática": [
        {"titulo": "🎯 Caza de Verbos", "desc": "Encuentra el verbo", "pregunta": "¿Cuál es el verbo en 'Juan corre'?", "opciones": ["corre", "Juan", "correr", "corriendo"], "correcta": "corre"},
        {"titulo": "🧩 Puzzle de Adjetivos", "desc": "Identifica el adjetivo", "pregunta": "En 'El perro grande', el adjetivo es:", "opciones": ["grande", "perro", "El", "perro grande"], "correcta": "grande"},
        {"titulo": "🎲 Dados de Adverbios", "desc": "Identifica el adverbio", "pregunta": "En 'Corre rápidamente', el adverbio es:", "opciones": ["rápidamente", "corre", "rápido", "correr"], "correcta": "rápidamente"},
        {"titulo": "🏆 Copa de Preposiciones", "desc": "Identifica la preposición", "pregunta": "En 'Voy a casa', la preposición es:", "opciones": ["a", "casa", "Voy", "a casa"], "correcta": "a"},
    ],
    "Literatura": [
        {"titulo": "🎯 Tiro a la Metáfora", "desc": "Identifica la metáfora", "pregunta": "¿Qué figura es 'Sus labios de rubí'?", "opciones": ["Metáfora", "Símil", "Hipérbole", "Personificación"], "correcta": "Metáfora"},
        {"titulo": "🧩 Puzzle de Símiles", "desc": "Identifica el símil", "pregunta": "¿Qué figura es 'Blanco como la nieve'?", "opciones": ["Metáfora", "Símil", "Hipérbole", "Personificación"], "correcta": "Símil"},
        {"titulo": "🎲 Dados Literarios", "desc": "Identifica la figura", "pregunta": "¿Qué figura es 'Te he dicho mil veces'?", "opciones": ["Metáfora", "Símil", "Hipérbole", "Personificación"], "correcta": "Hipérbole"},
        {"titulo": "🏆 Copa del Narrador", "desc": "Identifica el narrador", "pregunta": "El narrador que lo sabe todo es:", "opciones": ["Omnisciente", "Testigo", "Protagonista", "Inocente"], "correcta": "Omnisciente"},
    ],
    "Inglés": [
        {"titulo": "🎯 Caza del Presente", "desc": "Elige el presente", "pregunta": "I ___ to school every day.", "opciones": ["go", "goes", "going", "went"], "correcta": "go"},
        {"titulo": "🧩 Puzzle del Pasado", "desc": "Elige el pasado", "pregunta": "I ___ to Paris last year.", "opciones": ["go", "went", "gone", "going"], "correcta": "went"},
        {"titulo": "🎲 Dados del Perfecto", "desc": "Elige el presente perfecto", "pregunta": "I have never ___ sushi.", "opciones": ["eat", "ate", "eaten", "eating"], "correcta": "eaten"},
        {"titulo": "🏆 Copa del Futuro", "desc": "Elige el futuro", "pregunta": "I ___ help you.", "opciones": ["will", "am going to", "going to", "go to"], "correcta": "will"},
    ],
    "Bilingüe": [
        {"titulo": "🎯 Caza de Cognados", "desc": "Encuentra el cognado", "pregunta": "¿Cuál es el cognado de 'animal'?", "opciones": ["animal", "animale", "anima", "animado"], "correcta": "animal"},
        {"titulo": "🧩 Puzzle de Falsos Amigos", "desc": "Identifica el falso amigo", "pregunta": "¿Qué significa 'embarrassed'?", "opciones": ["embarazada", "avergonzado", "empezado", "embrujado"], "correcta": "avergonzado"},
        {"titulo": "🎲 Dados Bilingües", "desc": "Traduce correctamente", "pregunta": "¿Cuál es el cognado de 'family'?", "opciones": ["familia", "familiar", "famoso", "falda"], "correcta": "familia"},
        {"titulo": "🏆 Copa del Bilingüe", "desc": "Identifica el falso amigo", "pregunta": "¿Qué significa 'carpet'?", "opciones": ["carpeta", "alfombra", "carpintero", "carpa"], "correcta": "alfombra"},
    ]
}

total_juegos = 0
for categoria_nombre, juegos_list in juegos_data.items():
    try:
        cat = Categoria.objects.get(nombre=categoria_nombre)
    except:
        continue
    
    for data in juegos_list:
        nivel = random.choice(niveles)
        juego, created = Juego.objects.get_or_create(
            titulo=data["titulo"],
            defaults={
                "descripcion": data["desc"],
                "pregunta": data["pregunta"],
                "categoria": cat,
                "nivel": nivel,
                "tipo": "opcion",
                "opcion1": data["opciones"][0],
                "opcion2": data["opciones"][1],
                "opcion3": data["opciones"][2],
                "opcion4": data["opciones"][3],
                "respuesta_correcta": data["correcta"],
                "puntos": 10 + random.randint(0, 10),
                "activo": True
            }
        )
        if created:
            print(f"  ✅ {data['titulo']}")
            total_juegos += 1

print(f"\\n✅ {total_juegos} juegos creados")
"""
        
        self._ejecutar_script(script)
        print_success("Juegos ilimitados creados")
    
    def step_create_templates(self):
        print_step("Creando templates lúdicos...")
        
        # Template de juegos
        juegos_dir = self.project_dir / "templates" / "juegos"
        juegos_dir.mkdir(parents=True, exist_ok=True)
        
        # Template de lista de juegos con diseño lúdico
        list_html = """{% extends 'base.html' %}
{% load static %}

{% block title %}🎮 Juegos - MorphoPlay{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col-12">
        <h2>🎮 Juegos Interactivos</h2>
        <p class="text-secondary">¡Aprende jugando con nuestros juegos lúdicos!</p>
    </div>
</div>

<div class="row g-4">
    {% for juego in juegos %}
    <div class="col-md-4 col-lg-3">
        <div class="card h-100">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <span class="badge bg-primary">{{ juego.categoria.nombre|default:"General" }}</span>
                    <span class="badge bg-{% if juego.nivel.nombre == 'Básico' %}success{% elif juego.nivel.nombre == 'Intermedio' %}warning{% elif juego.nivel.nombre == 'Avanzado' %}danger{% else %}info{% endif %}">
                        {{ juego.nivel.nombre|default:"Básico" }}
                    </span>
                </div>
                <h5 class="card-title mt-2">{{ juego.titulo }}</h5>
                <p class="card-text text-secondary small">{{ juego.descripcion|truncatechars:60 }}</p>
                <div class="d-flex justify-content-between align-items-center mt-2">
                    <span class="badge bg-info">{{ juego.puntos }} pts</span>
                    <a href="/juegos/{{ juego.id }}/" class="btn btn-sm btn-primary">
                        <i class="fas fa-play"></i> Jugar
                    </a>
                </div>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12 text-center py-5">
        <i class="fas fa-gamepad fa-3x text-secondary mb-3"></i>
        <h4>No hay juegos disponibles</h4>
    </div>
    {% endfor %}
</div>
{% endblock %}
"""
        (juegos_dir / "list.html").write_text(list_html)
        print_success("Template de lista de juegos lúdico creado")
        
        # Template de detalle de juego con diseño lúdico
        detail_html = """{% extends 'base.html' %}
{% load static %}

{% block title %}{{ juego.titulo }} - MorphoPlay{% endblock %}

{% block extra_css %}
<style>
    .opcion-btn {
        transition: all 0.3s ease;
        min-width: 150px;
        padding: 12px 20px;
        margin: 5px;
        border-radius: 12px;
        font-weight: 500;
        font-size: 1.1rem;
    }
    .opcion-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(124, 58, 237, 0.2);
    }
    .opcion-btn.correct {
        background: #28a745 !important;
        color: white !important;
        border-color: #28a745 !important;
        animation: correctAnim 0.5s ease;
    }
    .opcion-btn.incorrect {
        background: #dc3545 !important;
        color: white !important;
        border-color: #dc3545 !important;
        animation: incorrectAnim 0.5s ease;
    }
    @keyframes correctAnim {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    @keyframes incorrectAnim {
        0% { transform: scale(1); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
        100% { transform: translateX(0); }
    }
    .opcion-btn.disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }
    .game-container {
        max-width: 800px;
        margin: 0 auto;
    }
    .puntuacion-animada {
        animation: pulse 0.5s ease;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    .emoji-big {
        font-size: 3rem;
    }
</style>
{% endblock %}

{% block content %}
<div class="game-container">
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/juegos/">Juegos</a></li>
            <li class="breadcrumb-item active">{{ juego.titulo }}</li>
        </ol>
    </nav>

    <div class="card">
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <span class="badge bg-primary me-2">{{ juego.categoria.nombre|default:"General" }}</span>
                    <span class="badge bg-{% if juego.nivel.nombre == 'Básico' %}success{% elif juego.nivel.nombre == 'Intermedio' %}warning{% elif juego.nivel.nombre == 'Avanzado' %}danger{% else %}info{% endif %}">
                        {{ juego.nivel.nombre|default:"Básico" }}
                    </span>
                </div>
                <div>
                    <span class="badge bg-info">{{ juego.puntos }} puntos</span>
                    {% if user.is_authenticated and progreso.completado %}
                    <span class="badge bg-success">✅ Completado</span>
                    {% endif %}
                </div>
            </div>
        </div>
        <div class="card-body">
            <h4 class="card-title">{{ juego.titulo }}</h4>
            <p class="card-text text-secondary">{{ juego.descripcion }}</p>
            
            {% if juego.pregunta %}
            <div class="alert alert-secondary mt-3">
                <strong>❓ Pregunta:</strong> {{ juego.pregunta }}
            </div>
            {% endif %}

            <div id="interactionArea" class="mt-4">
                <div class="d-flex flex-wrap justify-content-center gap-2">
                    {% for opcion in juego.get_opciones %}
                        {% if opcion %}
                        <button class="btn btn-outline-primary opcion-btn" 
                                data-opt="{{ opcion }}" 
                                data-correct="{{ juego.respuesta_correcta }}">
                            {{ opcion }}
                        </button>
                        {% endif %}
                    {% endfor %}
                </div>
            </div>

            <div id="resultContainer" class="mt-4 text-center" style="display: none;">
                <div id="resultMessage" class="alert"></div>
                <div id="resultDetails" class="mt-2"></div>
            </div>

            <div class="mt-4 d-flex justify-content-between">
                <div>
                    <span class="text-secondary">
                        <i class="fas fa-star"></i> Puntos: {{ juego.puntos }}
                    </span>
                </div>
                <div>
                    <span class="text-secondary">
                        <i class="fas fa-hashtag"></i> Juego #{{ juego.orden|default:juego.id }}
                    </span>
                </div>
            </div>
        </div>
        <div class="card-footer">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    {% if anterior %}
                    <a href="/juegos/{{ anterior.id }}/" class="btn btn-outline-secondary btn-sm">
                        <i class="fas fa-arrow-left"></i> Anterior
                    </a>
                    {% endif %}
                </div>
                <div>
                    <span class="text-secondary small">{{ juego.orden|default:juego.id }}/{{ total_juegos }}</span>
                </div>
                <div>
                    {% if siguiente %}
                    <a href="/juegos/{{ siguiente.id }}/" class="btn btn-outline-secondary btn-sm">
                        Siguiente <i class="fas fa-arrow-right"></i>
                    </a>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
$(document).ready(function() {
    const juegoId = {{ juego.id }};
    let answered = false;
    
    $('.opcion-btn').on('click', function() {
        if (answered) return;
        answered = true;
        
        const $btn = $(this);
        const selected = $btn.data('opt');
        const correct = $btn.data('correct');
        const isCorrect = selected === correct;
        
        $('.opcion-btn').addClass('disabled').prop('disabled', true);
        
        if (isCorrect) {
            $btn.removeClass('btn-outline-primary').addClass('btn-success correct');
        } else {
            $btn.removeClass('btn-outline-primary').addClass('btn-danger incorrect');
            $('.opcion-btn').each(function() {
                if ($(this).data('opt') === correct) {
                    $(this).removeClass('btn-outline-primary').addClass('btn-success correct');
                }
            });
        }
        
        $.ajax({
            url: "/juegos/api/verificar/",
            method: 'POST',
            data: JSON.stringify({
                juego_id: juegoId,
                respuesta: selected
            }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
            },
            success: function(data) {
                showResult(data);
            },
            error: function() {
                showResult({
                    correcto: isCorrect,
                    puntos: isCorrect ? {{ juego.puntos }} : 0,
                    respuesta_correcta: correct,
                    mensaje: isCorrect ? '🎉 ¡Correcto!' : '❌ Incorrecto'
                });
            }
        });
    });
    
    function showResult(data) {
        const container = $('#resultContainer');
        const message = $('#resultMessage');
        const details = $('#resultDetails');
        
        container.show();
        
        if (data.correcto) {
            message.removeClass('alert-danger').addClass('alert-success');
            message.html(`<i class="fas fa-check-circle"></i> ${data.mensaje}`);
            details.html(`
                <div class="puntuacion-animada">
                    <span class="badge bg-success fs-5 p-3">
                        <i class="fas fa-star"></i> +${data.puntos} puntos
                    </span>
                </div>
            `);
        } else {
            message.removeClass('alert-success').addClass('alert-danger');
            message.html(`<i class="fas fa-times-circle"></i> ${data.mensaje}`);
            details.html(`
                <div>
                    <p class="text-secondary">Respuesta correcta:</p>
                    <span class="badge bg-success fs-6 p-2">${data.respuesta_correcta}</span>
                </div>
            `);
        }
        
        if (data.completado) {
            $('.badge.bg-success').text('✅ Completado');
        }
    }
});
</script>
{% endblock %}
"""
        (juegos_dir / "detail.html").write_text(detail_html)
        print_success("Template de detalle de juego lúdico creado")
    
    def step_create_urls(self):
        print_step("Creando URLs para juegos...")
        
        urls_content = """
# URLs para juegos (agregar a morphoplay/urls.py)
# path('juegos/', views.juegos_list, name='juegos_list'),
# path('juegos/<int:juego_id>/', views.juego_detail, name='juego_detail'),
# path('juegos/api/verificar/', views.verificar_respuesta, name='verificar_respuesta'),
"""
        
        urls_file = self.project_dir / "scripts" / "urls_juegos.txt"
        urls_file.parent.mkdir(parents=True, exist_ok=True)
        urls_file.write_text(urls_content)
        print_success("URLs de juegos documentadas")
    
    def step_verify(self):
        print_step("Verificando instalación...")
        
        script = """
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Evaluacion, Juego, Curso

print("📊 VERIFICANDO INSTALACIÓN:")
print(f"📝 Evaluaciones: {Evaluacion.objects.count()}")
print(f"🎮 Juegos: {Juego.objects.count()}")

print("\\n📋 EVALUACIONES POR CURSO:")
for c in Curso.objects.filter(activo=True):
    print(f"  - {c.titulo}: {c.evaluaciones.count()} evaluaciones")
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
        print(f"""
{Colors.GREEN}✅ Evaluaciones y juegos instalados exitosamente!{Colors.END}

📝 Evaluaciones ilimitadas:
  - 5 evaluaciones por curso
  - Preguntas variadas por categoría
  - Niveles progresivos

🎮 Juegos lúdicos:
  - 24+ juegos interactivos
  - Diseño lúdico y divertido
  - Puntuación y progreso

📝 Templates lúdicos:
  - juegos/list.html
  - juegos/detail.html

🌐 Acceso:
  {Colors.CYAN}http://localhost:8000/juegos/{Colors.END}
  {Colors.CYAN}http://localhost:8000/cursos/1/evaluacion/1/{Colors.END}

🚀 Inicia el servidor:
  {Colors.BLUE}source venv/bin/activate{Colors.END}
  {Colors.BLUE}python manage.py runserver 0.0.0.0:8000{Colors.END}
        """)

if __name__ == "__main__":
    installer = EvaluacionesJuegosInstaller()
    installer.run()
