
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Juego, Categoria, Nivel

print("🎮 Creando juegos...")

try:
    basico = Nivel.objects.get(nombre="Básico")
except:
    basico = None

if basico:
    juegos_data = [
        {"titulo": "Prefijos de Lugar", "cat": "Morfología", "opciones": ["super-", "sub-", "pre-", "post-"], "correcta": "sub-"},
        {"titulo": "Sufijos de Adjetivos", "cat": "Morfología", "opciones": ["-oso", "-able", "-al", "-ico"], "correcta": "-oso"},
        {"titulo": "Complemento Circunstancial", "cat": "Sintaxis", "opciones": ["CD", "CI", "CC Tiempo", "Atributo"], "correcta": "CC Tiempo"},
        {"titulo": "Tiempos Verbales", "cat": "Gramática", "opciones": ["Presente", "Pretérito", "Futuro", "Condicional"], "correcta": "Futuro"},
        {"titulo": "Figuras Literarias", "cat": "Literatura", "opciones": ["Metáfora", "Símil", "Hipérbole", "Personificación"], "correcta": "Metáfora"},
        {"titulo": "Adverbs of Frequency", "cat": "Inglés", "opciones": ["always", "never", "sometimes", "rarely"], "correcta": "always"},
        {"titulo": "Cognados en Acción", "cat": "Bilingüe", "opciones": ["excelente", "excellent", "exelente", "excelent"], "correcta": "excelente"},
    ]
    
    for data in juegos_data:
        try:
            cat = Categoria.objects.get(nombre=data["cat"])
            obj, created = Juego.objects.get_or_create(
                titulo=data["titulo"],
                defaults={
                    "descripcion": data["titulo"],
                    "pregunta": f"¿Qué es {data['titulo']}?",
                    "categoria": cat,
                    "nivel": basico,
                    "tipo": "opcion",
                    "opcion1": data["opciones"][0],
                    "opcion2": data["opciones"][1],
                    "opcion3": data["opciones"][2],
                    "opcion4": data["opciones"][3],
                    "respuesta_correcta": data["correcta"],
                    "puntos": 10
                }
            )
            if created:
                print(f"  ✅ {data['titulo']}")
        except:
            pass
