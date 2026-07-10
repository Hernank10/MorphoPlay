#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Juego, Categoria, Nivel

def cargar_juegos():
    print("🎮 Cargando 30 juegos interactivos...")
    
    try:
        morfologia = Categoria.objects.get(nombre="Morfología")
        sintaxis = Categoria.objects.get(nombre="Sintaxis")
        gramatica = Categoria.objects.get(nombre="Gramática")
        ingles = Categoria.objects.get(nombre="Inglés")
        bilingue = Categoria.objects.get(nombre="Bilingüe")
        
        basico = Nivel.objects.get(nombre="Básico")
        intermedio = Nivel.objects.get(nombre="Intermedio")
        avanzado = Nivel.objects.get(nombre="Avanzado")
        experto = Nivel.objects.get(nombre="Experto")
        
    except Exception as e:
        print(f"❌ Error obteniendo categorías/niveles: {e}")
        return
    
    juegos_data = [
        # ============================================================
        # 🇪🇸 MORFOLOGÍA (Juegos 1-10)
        # ============================================================
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
            "titulo": "Prefijos de Lugar",
            "desc": "Elige el prefijo que indica posición",
            "pregunta": "¿Qué prefijo significa 'debajo de'?",
            "cat": morfologia,
            "nivel": basico,
            "opciones": ["super-", "sub-", "pre-", "post-"],
            "correcta": "sub-",
            "puntos": 10,
            "orden": 4
        },
        {
            "titulo": "Sufijos de Lugar",
            "desc": "Identifica el sufijo que indica lugar",
            "pregunta": "¿Qué sufijo forma palabras que indican lugar?",
            "cat": morfologia,
            "nivel": basico,
            "opciones": ["-ero", "-ción", "-mente", "-dor"],
            "correcta": "-ero",
            "puntos": 10,
            "orden": 5
        },
        {
            "titulo": "Aumentativos",
            "desc": "Elige el aumentativo correcto",
            "pregunta": "¿Cuál es el aumentativo de 'perro'?",
            "cat": morfologia,
            "nivel": basico,
            "opciones": ["perrito", "perrazo", "perrucho", "perrillo"],
            "correcta": "perrazo",
            "puntos": 10,
            "orden": 6
        },
        {
            "titulo": "Familias de Palabras",
            "desc": "Identifica palabras de la misma familia",
            "pregunta": "¿Cuál NO pertenece a la familia de 'mar'?",
            "cat": morfologia,
            "nivel": intermedio,
            "opciones": ["marino", "maremoto", "marea", "martillo"],
            "correcta": "martillo",
            "puntos": 15,
            "orden": 7
        },
        {
            "titulo": "Sufijos Verbales",
            "desc": "Identifica el sufijo verbal correcto",
            "pregunta": "Verbo a partir de 'moderno'",
            "cat": morfologia,
            "nivel": intermedio,
            "opciones": ["modernizar", "modernear", "modernar", "modernizar"],
            "correcta": "modernizar",
            "puntos": 15,
            "orden": 8
        },
        {
            "titulo": "Sufijos de Adjetivos",
            "desc": "Forma adjetivos con el sufijo correcto",
            "pregunta": "Adjetivo derivado de 'cuidado' (con -oso)",
            "cat": morfologia,
            "nivel": intermedio,
            "opciones": ["cuidadoso", "cuidadores", "cuidante", "cuidador"],
            "correcta": "cuidadoso",
            "puntos": 15,
            "orden": 9
        },
        {
            "titulo": "Prefijos y Sufijos",
            "desc": "Identifica la estructura de palabras compuestas",
            "pregunta": "En 'inmoralidad', ¿qué es 'in-'?",
            "cat": morfologia,
            "nivel": avanzado,
            "opciones": ["Prefijo", "Sufijo", "Raíz", "Lexema"],
            "correcta": "Prefijo",
            "puntos": 20,
            "orden": 10
        },
        
        # ============================================================
        # 🔍 SINTAXIS (Juegos 11-20)
        # ============================================================
        {
            "titulo": "Sujeto y Predicado",
            "desc": "Identifica el sujeto de la oración",
            "pregunta": "En 'El niño come pan', ¿cuál es el sujeto?",
            "cat": sintaxis,
            "nivel": basico,
            "opciones": ["El niño", "come pan", "pan", "El"],
            "correcta": "El niño",
            "puntos": 10,
            "orden": 11
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
            "orden": 12
        },
        {
            "titulo": "Oración Simple",
            "desc": "Identifica oraciones simples",
            "pregunta": "¿Cuál es una oración simple?",
            "cat": sintaxis,
            "nivel": basico,
            "opciones": ["Juan estudia", "Juan estudia y María trabaja", "Dijo que vendría", "Llegó, saludó"],
            "correcta": "Juan estudia",
            "puntos": 10,
            "orden": 13
        },
        {
            "titulo": "Oración Compuesta",
            "desc": "Identifica oraciones compuestas",
            "pregunta": "¿Cuál es una oración compuesta?",
            "cat": sintaxis,
            "nivel": intermedio,
            "opciones": ["El sol brilla", "Juan estudia y María trabaja", "Llegó temprano", "Estudia mucho"],
            "correcta": "Juan estudia y María trabaja",
            "puntos": 15,
            "orden": 14
        },
        {
            "titulo": "Sintagma Nominal",
            "desc": "Identifica el sintagma nominal",
            "pregunta": "En 'El perro grande', ¿cuál es el SN?",
            "cat": sintaxis,
            "nivel": intermedio,
            "opciones": ["El perro grande", "perro", "El perro", "grande"],
            "correcta": "El perro grande",
            "puntos": 15,
            "orden": 15
        },
        {
            "titulo": "Complemento Indirecto",
            "desc": "Identifica el complemento indirecto",
            "pregunta": "En 'Doy el libro a Juan', ¿cuál es el CI?",
            "cat": sintaxis,
            "nivel": avanzado,
            "opciones": ["Doy", "el libro", "a Juan", "Juan"],
            "correcta": "a Juan",
            "puntos": 20,
            "orden": 16
        },
        {
            "titulo": "Complemento Circunstancial",
            "desc": "Identifica el complemento circunstancial",
            "pregunta": "En 'Vino ayer', ¿cuál es el CC?",
            "cat": sintaxis,
            "nivel": avanzado,
            "opciones": ["Vino", "ayer", "Vino ayer", "a"],
            "correcta": "ayer",
            "puntos": 20,
            "orden": 17
        },
        {
            "titulo": "Oración Pasiva",
            "desc": "Identifica la voz pasiva",
            "pregunta": "¿Cuál es una oración en voz pasiva?",
            "cat": sintaxis,
            "nivel": avanzado,
            "opciones": ["Juan escribe la carta", "La carta fue escrita", "Juan está escribiendo", "La carta es escrita"],
            "correcta": "La carta fue escrita",
            "puntos": 20,
            "orden": 18
        },
        {
            "titulo": "Oración Subordinada",
            "desc": "Identifica la subordinada",
            "pregunta": "En 'Dijo que vendría', ¿cuál es la subordinada?",
            "cat": sintaxis,
            "nivel": avanzado,
            "opciones": ["Dijo", "que vendría", "vendría", "Dijo que"],
            "correcta": "que vendría",
            "puntos": 20,
            "orden": 19
        },
        {
            "titulo": "Análisis Sintáctico",
            "desc": "Analiza la estructura de la oración",
            "pregunta": "En 'Los niños juegan en el parque', ¿qué función tiene 'en el parque'?",
            "cat": sintaxis,
            "nivel": experto,
            "opciones": ["CC Lugar", "CD", "CI", "Atributo"],
            "correcta": "CC Lugar",
            "puntos": 25,
            "orden": 20
        },
        
        # ============================================================
        # 🇬🇧 INGLÉS (Juegos 21-25)
        # ============================================================
        {
            "titulo": "Present Simple",
            "desc": "Elige la forma correcta del presente simple",
            "pregunta": "I ___ to school every day.",
            "cat": ingles,
            "nivel": basico,
            "opciones": ["go", "goes", "going", "went"],
            "correcta": "go",
            "puntos": 10,
            "orden": 21
        },
        {
            "titulo": "Past Simple",
            "desc": "Elige la forma correcta del pasado simple",
            "pregunta": "She ___ to the cinema yesterday.",
            "cat": ingles,
            "nivel": intermedio,
            "opciones": ["go", "went", "gone", "going"],
            "correcta": "went",
            "puntos": 15,
            "orden": 22
        },
        {
            "titulo": "Present Perfect",
            "desc": "Elige la forma correcta del presente perfecto",
            "pregunta": "I have ___ visited Paris.",
            "cat": ingles,
            "nivel": intermedio,
            "opciones": ["ever", "never", "already", "yet"],
            "correcta": "never",
            "puntos": 15,
            "orden": 23
        },
        {
            "titulo": "Adverbs of Frequency",
            "desc": "Elige el adverbio de frecuencia correcto",
            "pregunta": "I ___ eat breakfast at 7:00 AM.",
            "cat": ingles,
            "nivel": intermedio,
            "opciones": ["always", "never", "sometimes", "rarely"],
            "correcta": "always",
            "puntos": 15,
            "orden": 24
        },
        {
            "titulo": "Comparatives",
            "desc": "Elige la forma comparativa correcta",
            "pregunta": "My house is ___ than yours.",
            "cat": ingles,
            "nivel": avanzado,
            "opciones": ["big", "bigger", "biggest", "more big"],
            "correcta": "bigger",
            "puntos": 20,
            "orden": 25
        },
        
        # ============================================================
        # 🌐 BILINGÜE (Juegos 26-30)
        # ============================================================
        {
            "titulo": "Cognados Perfectos",
            "desc": "Encuentra el cognado perfecto",
            "pregunta": "¿Cuál es el cognado de 'animal' en español?",
            "cat": bilingue,
            "nivel": basico,
            "opciones": ["animal", "animale", "anima", "animado"],
            "correcta": "animal",
            "puntos": 10,
            "orden": 26
        },
        {
            "titulo": "Falsos Amigos I",
            "desc": "¡Cuidado con los falsos amigos!",
            "pregunta": "¿Qué significa 'embarrassed' en español?",
            "cat": bilingue,
            "nivel": intermedio,
            "opciones": ["embarazada", "avergonzado", "empezado", "embrujado"],
            "correcta": "avergonzado",
            "puntos": 15,
            "orden": 27
        },
        {
            "titulo": "Sufijos Paralelos",
            "desc": "Encuentra el sufijo equivalente",
            "pregunta": "El sufijo '-ción' en español equivale a:",
            "cat": bilingue,
            "nivel": intermedio,
            "opciones": ["-tion", "-sion", "-tion/sion", "-ción"],
            "correcta": "-tion",
            "puntos": 15,
            "orden": 28
        },
        {
            "titulo": "Cognados en Acción",
            "desc": "Encuentra el cognado correcto",
            "pregunta": "¿Cuál es el cognado de 'excellent' en español?",
            "cat": bilingue,
            "nivel": intermedio,
            "opciones": ["excelente", "excellent", "exelente", "excelent"],
            "correcta": "excelente",
            "puntos": 15,
            "orden": 29
        },
        {
            "titulo": "Falsos Amigos II",
            "desc": "¡Más falsos amigos!",
            "pregunta": "¿Qué significa 'sensible' en inglés?",
            "cat": bilingue,
            "nivel": avanzado,
            "opciones": ["sensible", "sensato", "sensitivo", "sensorial"],
            "correcta": "sensitivo",
            "puntos": 20,
            "orden": 30
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
            print(f"  ✅ {data['orden']:2d}. {data['titulo']}")
    
    print(f"\n✅ Total juegos cargados: {creados} nuevos")
    print(f"📊 Total juegos en la base de datos: {Juego.objects.count()}")

if __name__ == "__main__":
    cargar_juegos()
