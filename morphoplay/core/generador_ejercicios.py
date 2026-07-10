"""
Generador de Ejercicios Interactivos - MorphoPlay
Permite crear ejercicios de diferentes tipos de manera ilimitada
"""

import random
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class GeneradorEjercicios:
    """Clase principal para generar ejercicios interactivos"""
    
    TIPOS = [
        'opcion_multiple',
        'verdadero_falso',
        'completar',
        'relacionar',
        'ordenar',
        'texto_libre',
        'numerico'
    ]
    
    @staticmethod
    def generar_opcion_multiple(tema: str = "gramatica") -> Dict[str, Any]:
        """Genera una pregunta de opción múltiple"""
        bancos = {
            "morfologia": [
                {"pregunta": "¿Qué es un lexema?", "opciones": ["Significado básico", "Sufijo", "Prefijo", "Morfema"], "correcta": 0},
                {"pregunta": "¿Qué es un morfema?", "opciones": ["Parte gramatical", "Raíz", "Prefijo", "Sufijo"], "correcta": 0}
            ],
            "sintaxis": [
                {"pregunta": "¿Qué es el sujeto?", "opciones": ["Quien realiza la acción", "El verbo", "El complemento", "El predicado"], "correcta": 0}
            ],
            "gramatica": [
                {"pregunta": "¿Qué es un verbo?", "opciones": ["Acción o estado", "Sustantivo", "Adjetivo", "Adverbio"], "correcta": 0}
            ]
        }
        
        tema_bajo = tema.lower()
        banco = bancos.get(tema_bajo, bancos["gramatica"])
        pregunta_data = random.choice(banco)
        
        opciones = pregunta_data["opciones"][:]
        random.shuffle(opciones)
        
        return {
            "tipo": "opcion_multiple",
            "pregunta": pregunta_data["pregunta"],
            "opciones": opciones,
            "respuesta_correcta": pregunta_data["opciones"][pregunta_data["correcta"]],
            "puntos": 10,
            "tema": tema
        }
    
    @staticmethod
    def generar_verdadero_falso(tema: str = "gramatica") -> Dict[str, Any]:
        """Genera una pregunta de Verdadero/Falso"""
        afirmaciones = {
            "morfologia": [
                {"texto": "La morfología estudia la estructura de las palabras", "verdadero": True},
                {"texto": "Los prefijos se añaden al final de la palabra", "verdadero": False}
            ],
            "sintaxis": [
                {"texto": "El sujeto realiza la acción del verbo", "verdadero": True}
            ],
            "gramatica": [
                {"texto": "El verbo es el núcleo del predicado", "verdadero": True}
            ]
        }
        
        tema_bajo = tema.lower()
        banco = afirmaciones.get(tema_bajo, afirmaciones["gramatica"])
        afirmacion = random.choice(banco)
        
        return {
            "tipo": "verdadero_falso",
            "pregunta": afirmacion["texto"],
            "respuesta_correcta": "Verdadero" if afirmacion["verdadero"] else "Falso",
            "opciones": ["Verdadero", "Falso"],
            "puntos": 10,
            "tema": tema
        }
    
    @staticmethod
    def generar_completar(tema: str = "gramatica") -> Dict[str, Any]:
        """Genera una pregunta de completar"""
        ejercicios = {
            "morfologia": [
                {"texto": "La ___ es la parte de la palabra que contiene el significado básico.", "respuesta": "raíz"},
                {"texto": "Los ___ se añaden al inicio de la palabra.", "respuesta": "prefijos"}
            ],
            "sintaxis": [
                {"texto": "El ___ es quien realiza la acción del verbo.", "respuesta": "sujeto"}
            ],
            "gramatica": [
                {"texto": "El ___ es el núcleo del predicado.", "respuesta": "verbo"}
            ]
        }
        
        tema_bajo = tema.lower()
        banco = ejercicios.get(tema_bajo, ejercicios["gramatica"])
        ejercicio = random.choice(banco)
        
        return {
            "tipo": "completar",
            "pregunta": ejercicio["texto"],
            "respuesta_correcta": ejercicio["respuesta"],
            "puntos": 15,
            "tema": tema
        }
    
    @staticmethod
    def generar_relacionar(tema: str = "gramatica") -> Dict[str, Any]:
        """Genera una pregunta de relacionar"""
        pares = {
            "morfologia": [
                {"columna_a": ["Prefijo", "Sufijo", "Raíz"], "columna_b": ["Inicio", "Final", "Significado"], "respuestas": [0, 1, 2]}
            ]
        }
        
        tema_bajo = tema.lower()
        banco = pares.get(tema_bajo, pares["morfologia"])
        ejercicio = random.choice(banco)
        
        return {
            "tipo": "relacionar",
            "pregunta": "Relaciona cada elemento con su definición",
            "columna_a": ejercicio["columna_a"],
            "columna_b": ejercicio["columna_b"],
            "respuesta_correcta": str(ejercicio["respuestas"]),
            "puntos": 20,
            "tema": tema
        }
    
    @staticmethod
    def generar_ordenar(tema: str = "gramatica") -> Dict[str, Any]:
        """Genera una pregunta de ordenar"""
        secuencias = {
            "morfologia": [
                {"elementos": ["Prefijo", "Raíz", "Sufijo"], "correcto": [0, 1, 2]}
            ],
            "sintaxis": [
                {"elementos": ["Sujeto", "Verbo", "Complemento"], "correcto": [0, 1, 2]}
            ]
        }
        
        tema_bajo = tema.lower()
        banco = secuencias.get(tema_bajo, secuencias["morfologia"])
        ejercicio = random.choice(banco)
        
        return {
            "tipo": "ordenar",
            "pregunta": "Ordena los siguientes elementos correctamente",
            "elementos": ejercicio["elementos"],
            "respuesta_correcta": str(ejercicio["correcto"]),
            "puntos": 20,
            "tema": tema
        }
    
    @staticmethod
    def generar_texto_libre(tema: str = "gramatica") -> Dict[str, Any]:
        """Genera una pregunta de texto libre"""
        preguntas = {
            "morfologia": [
                {"pregunta": "Define qué es un prefijo y da un ejemplo.", "palabras_clave": ["prefijo", "inicio"]}
            ]
        }
        
        tema_bajo = tema.lower()
        banco = preguntas.get(tema_bajo, preguntas["morfologia"])
        ejercicio = random.choice(banco)
        
        return {
            "tipo": "texto_libre",
            "pregunta": ejercicio["pregunta"],
            "palabras_clave": ejercicio["palabras_clave"],
            "respuesta_correcta": "Respuesta evaluada por el profesor",
            "puntos": 25,
            "tema": tema
        }
    
    @staticmethod
    def generar_numerico(tema: str = "gramatica") -> Dict[str, Any]:
        """Genera una pregunta numérica"""
        preguntas = {
            "morfologia": [
                {"pregunta": "¿Cuántas partes tiene la palabra 'casita'?", "respuesta": 2}
            ]
        }
        
        tema_bajo = tema.lower()
        banco = preguntas.get(tema_bajo, preguntas["morfologia"])
        ejercicio = random.choice(banco)
        
        return {
            "tipo": "numerico",
            "pregunta": ejercicio["pregunta"],
            "respuesta_correcta": str(ejercicio["respuesta"]),
            "puntos": 15,
            "tema": tema
        }
    
    @classmethod
    def generar_ejercicio(cls, tipo: Optional[str] = None, tema: str = "gramatica") -> Dict[str, Any]:
        """Genera un ejercicio del tipo especificado"""
        if tipo is None:
            tipo = random.choice(cls.TIPOS)
        
        generadores = {
            'opcion_multiple': cls.generar_opcion_multiple,
            'verdadero_falso': cls.generar_verdadero_falso,
            'completar': cls.generar_completar,
            'relacionar': cls.generar_relacionar,
            'ordenar': cls.generar_ordenar,
            'texto_libre': cls.generar_texto_libre,
            'numerico': cls.generar_numerico
        }
        
        generador = generadores.get(tipo, cls.generar_opcion_multiple)
        ejercicio = generador(tema)
        ejercicio["id"] = f"{tipo}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return ejercicio
    
    @classmethod
    def generar_batch(cls, cantidad: int = 10, tipos: Optional[List[str]] = None, tema: str = "gramatica") -> List[Dict[str, Any]]:
        """Genera múltiples ejercicios"""
        ejercicios = []
        tipos_disponibles = tipos or cls.TIPOS
        
        for _ in range(cantidad):
            tipo = random.choice(tipos_disponibles)
            ejercicio = cls.generar_ejercicio(tipo, tema)
            ejercicios.append(ejercicio)
        
        return ejercicios
    
    @classmethod
    def a_django_fixture(cls, ejercicios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convierte ejercicios a fixture de Django"""
        ahora = datetime.now().isoformat()
        
        fixture = []
        for i, ejercicio in enumerate(ejercicios, 2000):
            if ejercicio["tipo"] == "opcion_multiple":
                fixture.append({
                    "model": "core.juego",
                    "pk": i,
                    "fields": {
                        "titulo": f"Ejercicio {i} - {ejercicio['tema'].capitalize()}",
                        "descripcion": f"Ejercicio de {ejercicio['tipo']} sobre {ejercicio['tema']}",
                        "pregunta": ejercicio["pregunta"],
                        "categoria": 4,
                        "nivel": 3,
                        "tipo": "opcion",
                        "opcion1": ejercicio["opciones"][0] if len(ejercicio["opciones"]) > 0 else "",
                        "opcion2": ejercicio["opciones"][1] if len(ejercicio["opciones"]) > 1 else "",
                        "opcion3": ejercicio["opciones"][2] if len(ejercicio["opciones"]) > 2 else "",
                        "opcion4": ejercicio["opciones"][3] if len(ejercicio["opciones"]) > 3 else "",
                        "respuesta_correcta": ejercicio["respuesta_correcta"],
                        "puntos": ejercicio["puntos"],
                        "orden": i - 1999,
                        "activo": True,
                        "created_at": ahora,
                        "updated_at": ahora
                    }
                })
            elif ejercicio["tipo"] == "verdadero_falso":
                fixture.append({
                    "model": "core.juego",
                    "pk": i,
                    "fields": {
                        "titulo": f"Ejercicio {i} - Verdadero/Falso",
                        "descripcion": f"Ejercicio de {ejercicio['tema']}",
                        "pregunta": ejercicio["pregunta"],
                        "categoria": 4,
                        "nivel": 2,
                        "tipo": "opcion",
                        "opcion1": "Verdadero",
                        "opcion2": "Falso",
                        "opcion3": "",
                        "opcion4": "",
                        "respuesta_correcta": ejercicio["respuesta_correcta"],
                        "puntos": ejercicio["puntos"],
                        "orden": i - 1999,
                        "activo": True,
                        "created_at": ahora,
                        "updated_at": ahora
                    }
                })
        
        return fixture


def generar_y_guardar_fixture(cantidad: int = 10, archivo: str = "ejercicios_generados.json"):
    """Genera y guarda un fixture completo"""
    from pathlib import Path
    generador = GeneradorEjercicios()
    ejercicios = generador.generar_batch(cantidad)
    fixture = generador.a_django_fixture(ejercicios)
    
    path = Path(f"core/fixtures/{archivo}")
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(fixture, f, ensure_ascii=False, indent=2)
    
    return str(path)


if __name__ == "__main__":
    path = generar_y_guardar_fixture(5)
    print(f"✅ Ejercicios generados y guardados en: {path}")
