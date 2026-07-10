#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Categoria, Nivel, Leccion

def crear_cursos_completos():
    print("📚 Creando cursos completos...")
    print("=" * 50)
    
    try:
        morfologia = Categoria.objects.get(nombre="Morfología")
        sintaxis = Categoria.objects.get(nombre="Sintaxis")
        gramatica = Categoria.objects.get(nombre="Gramática")
        literatura = Categoria.objects.get(nombre="Literatura")
        ingles = Categoria.objects.get(nombre="Inglés")
        bilingue = Categoria.objects.get(nombre="Bilingüe")
        
        basico = Nivel.objects.get(nombre="Básico")
        intermedio = Nivel.objects.get(nombre="Intermedio")
        avanzado = Nivel.objects.get(nombre="Avanzado")
        experto = Nivel.objects.get(nombre="Experto")
        
    except Exception as e:
        print(f"❌ Error obteniendo categorías/niveles: {e}")
        print("Ejecuta primero: python manage.py migrate")
        return
    
    # ============================================================
    # CURSO 1: MORFOLOGÍA DEL CASTELLANO
    # ============================================================
    curso1, created = Curso.objects.get_or_create(
        titulo="Morfología del Castellano",
        defaults={
            "descripcion": "Curso completo sobre la estructura de las palabras en español. Aprende prefijos, sufijos, raíces y formación de palabras.",
            "categoria": morfologia,
            "nivel": basico,
            "duracion_estimada": 10,
            "orden": 1
        }
    )
    
    if created:
        print(f"  ✅ Curso: {curso1.titulo}")
        
        lecciones1 = [
            {
                "titulo": "Introducción a la Morfología",
                "contenido": "📖 ¿Qué es la Morfología?\n\nLa morfología es la parte de la lingüística que estudia la estructura interna de las palabras.\n\n🔍 Conceptos clave:\n• Palabra: Unidad mínima con significado\n• Lexema/Raíz: Parte que contiene el significado básico\n• Morfema: Partes que añaden información gramatical\n\n📝 Ejemplos:\n• cas + ita = casita\n• perr + azo = perrazo\n• in + útil = inútil",
                "orden": 1
            },
            {
                "titulo": "Prefijos en Español",
                "contenido": "🔤 Los Prefijos\n\nLos prefijos son partículas que se añaden al INICIO de una palabra.\n\n📋 Tipos:\n\n1. Negación: in-, des-, a-\n2. Lugar: sub-, super-, ante-, post-\n3. Tiempo: pre-, post-, re-\n4. Cantidad: bi-, tri-, multi-\n\nEjemplos: inútil, subterráneo, prehistoria",
                "orden": 2
            },
            {
                "titulo": "Sufijos en Español",
                "contenido": "🔤 Los Sufijos\n\nLos sufijos se añaden al FINAL de una palabra.\n\n📋 Tipos:\n\n1. Diminutivos: -ito, -illo, -ín\n2. Aumentativos: -azo, -ón, -ote\n3. Profesiones: -ero, -ista, -dor\n4. Adjetivos: -oso, -able, -al\n\nEjemplos: casita, perrazo, panadero",
                "orden": 3
            },
            {
                "titulo": "Raíces y Formación de Palabras",
                "contenido": "🌱 Raíces y Formación de Palabras\n\nLa raíz es el núcleo semántico.\n\nProcesos:\n1. Derivación: añadir prefijos/sufijos\n2. Composición: unir palabras\n3. Parasíntesis: combinación\n4. Acortamiento: reducir\n\nEjemplos:\n- casita (derivación)\n- abrelatas (composición)",
                "orden": 4
            }
        ]
        
        for lec in lecciones1:
            Leccion.objects.get_or_create(
                curso=curso1,
                titulo=lec["titulo"],
                defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
            )
    
    # ============================================================
    # CURSO 2: SINTAXIS DEL CASTELLANO
    # ============================================================
    curso2, created = Curso.objects.get_or_create(
        titulo="Sintaxis del Castellano",
        defaults={
            "descripcion": "Curso completo sobre la estructura de las oraciones en español.",
            "categoria": sintaxis,
            "nivel": intermedio,
            "duracion_estimada": 12,
            "orden": 2
        }
    )
    
    if created:
        print(f"  ✅ Curso: {curso2.titulo}")
        
        lecciones2 = [
            {
                "titulo": "La Oración y sus Partes",
                "contenido": "📖 La Oración\n\nLa oración es la unidad básica de comunicación.\n\nEstructura:\n- SUJETO: quien realiza la acción\n- PREDICADO: lo que se dice del sujeto\n\nEjemplo: 'El niño come pan'\n- Sujeto: El niño\n- Predicado: come pan",
                "orden": 1
            },
            {
                "titulo": "El Sujeto",
                "contenido": "👤 El Sujeto\n\nTipos de sujeto:\n1. Expreso: aparece explícito\n2. Elíptico: se sobreentiende\n3. Simple: un núcleo\n4. Compuesto: varios núcleos\n\nEjemplos:\n- El niño juega (expreso)\n- (Yo) como (elíptico)",
                "orden": 2
            },
            {
                "titulo": "El Predicado",
                "contenido": "📝 El Predicado\n\nTipos de predicado:\n1. Verbal: verbo predicativo\n2. Nominal: verbo copulativo\n\nComplementos:\n- CD: recibe la acción\n- CI: destinatario\n- CC: circunstancias\n- Atributo: con ser/estar",
                "orden": 3
            },
            {
                "titulo": "Análisis Sintáctico",
                "contenido": "🔍 Análisis Sintáctico\n\nPasos:\n1. Identificar el verbo\n2. Identificar el sujeto\n3. Identificar complementos\n\nEjemplo: 'María dio el libro a Juan'\n- Verbo: dio\n- Sujeto: María\n- CD: el libro\n- CI: a Juan",
                "orden": 4
            }
        ]
        
        for lec in lecciones2:
            Leccion.objects.get_or_create(
                curso=curso2,
                titulo=lec["titulo"],
                defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
            )
    
    # ============================================================
    # CURSO 3: ENGLISH GRAMMAR
    # ============================================================
    curso3, created = Curso.objects.get_or_create(
        titulo="English Grammar",
        defaults={
            "descripcion": "Curso completo de gramática inglesa para hispanohablantes.",
            "categoria": ingles,
            "nivel": intermedio,
            "duracion_estimada": 15,
            "orden": 3
        }
    )
    
    if created:
        print(f"  ✅ Curso: {curso3.titulo}")
        
        lecciones3 = [
            {
                "titulo": "Present Simple",
                "contenido": "📖 Present Simple\n\nUsos:\n1. Hábitos y rutinas\n2. Verdades generales\n\nEstructura:\n- Afirmativo: I work\n- Negativo: I don't work\n- Interrogativo: Do you work?\n\nEjemplos:\n- I go to school every day.\n- Water boils at 100°C.",
                "orden": 1
            },
            {
                "titulo": "Past Simple",
                "contenido": "📖 Past Simple\n\nUsos:\n1. Acciones terminadas\n2. Secuencia de acciones\n\nEstructura:\n- Afirmativo: I worked\n- Negativo: I didn't work\n- Interrogativo: Did you work?\n\nIrregulares:\n- go → went\n- eat → ate",
                "orden": 2
            },
            {
                "titulo": "Present Perfect",
                "contenido": "📖 Present Perfect\n\nUsos:\n1. Experiencias pasadas\n2. Acciones que continúan\n\nEstructura:\n- Afirmativo: I have visited\n- Negativo: I haven't visited\n- Interrogativo: Have you visited?\n\nPalabras clave:\n- ever, never, already, yet",
                "orden": 3
            },
            {
                "titulo": "Future Tenses",
                "contenido": "📖 Future Tenses\n\nWILL:\n- Decisiones espontáneas\n- Predicciones\n\nGOING TO:\n- Planes e intenciones\n- Predicciones con evidencia\n\nEjemplos:\n- I will help you.\n- I am going to study.",
                "orden": 4
            }
        ]
        
        for lec in lecciones3:
            Leccion.objects.get_or_create(
                curso=curso3,
                titulo=lec["titulo"],
                defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
            )
    
    # ============================================================
    # CURSO 4: COGNADOS ESPAÑOL-INGLÉS
    # ============================================================
    curso4, created = Curso.objects.get_or_create(
        titulo="Cognados Español-Inglés",
        defaults={
            "descripcion": "Aprende palabras similares en español e inglés. ¡Expande tu vocabulario bilingüe!",
            "categoria": bilingue,
            "nivel": basico,
            "duracion_estimada": 8,
            "orden": 4
        }
    )
    
    if created:
        print(f"  ✅ Curso: {curso4.titulo}")
        
        lecciones4 = [
            {
                "titulo": "Cognados Perfectos",
                "contenido": "🌟 Cognados Perfectos\n\nPalabras que se escriben y significan lo mismo.\n\nEjemplos:\n- animal = animal\n- color = color\n- doctor = doctor\n- importante = important",
                "orden": 1
            },
            {
                "titulo": "Cognados Parciales",
                "contenido": "🌟 Cognados Parciales\n\nPalabras similares con pequeñas diferencias.\n\nEjemplos:\n- family / familia\n- different / diferente\n- excellent / excelente",
                "orden": 2
            },
            {
                "titulo": "Falsos Amigos",
                "contenido": "⚠️ Falsos Amigos\n\n¡Cuidado! Palabras que parecen iguales pero significan diferente.\n\nEjemplos:\n- embarrassed NO es embarazada (es avergonzado)\n- carpet NO es carpeta (es alfombra)\n- exit NO es éxito (es salida)",
                "orden": 3
            }
        ]
        
        for lec in lecciones4:
            Leccion.objects.get_or_create(
                curso=curso4,
                titulo=lec["titulo"],
                defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
            )
    
    # ============================================================
    # CURSO 5: TÉCNICAS NARRATIVAS
    # ============================================================
    curso5, created = Curso.objects.get_or_create(
        titulo="Técnicas Narrativas en Literatura",
        defaults={
            "descripcion": "Explora las técnicas literarias de los grandes escritores.",
            "categoria": literatura,
            "nivel": avanzado,
            "duracion_estimada": 14,
            "orden": 5
        }
    )
    
    if created:
        print(f"  ✅ Curso: {curso5.titulo}")
        
        lecciones5 = [
            {
                "titulo": "Introducción a la Narrativa",
                "contenido": "📖 Introducción a la Narrativa\n\nElementos:\n- Narrador\n- Personajes\n- Acción\n- Tiempo\n- Espacio",
                "orden": 1
            },
            {
                "titulo": "Punto de Vista Narrativo",
                "contenido": "👁️ Punto de Vista\n\nTipos:\n- Primera persona (protagonista)\n- Segunda persona (tú)\n- Tercera persona (omnisciente, limitado, objetivo)",
                "orden": 2
            },
            {
                "titulo": "Estructura del Relato",
                "contenido": "📋 Estructura del Relato\n\nEstructura clásica:\n1. Planteamiento\n2. Nudo (desarrollo)\n3. Desenlace",
                "orden": 3
            }
        ]
        
        for lec in lecciones5:
            Leccion.objects.get_or_create(
                curso=curso5,
                titulo=lec["titulo"],
                defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
            )
    
    # ============================================================
    # CURSO 6: GRAMÁTICA COMPARADA
    # ============================================================
    curso6, created = Curso.objects.get_or_create(
        titulo="Gramática Comparada: Español vs Inglés",
        defaults={
            "descripcion": "Compara las estructuras gramaticales del español y el inglés.",
            "categoria": bilingue,
            "nivel": avanzado,
            "duracion_estimada": 16,
            "orden": 6
        }
    )
    
    if created:
        print(f"  ✅ Curso: {curso6.titulo}")
        
        lecciones6 = [
            {
                "titulo": "Orden de las Palabras",
                "contenido": "📝 Orden de las Palabras\n\nDiferencias:\n- Español: 'El perro grande' (sustantivo + adjetivo)\n- Inglés: 'The big dog' (adjetivo + sustantivo)",
                "orden": 1
            },
            {
                "titulo": "Tiempos Verbales Comparados",
                "contenido": "⏰ Tiempos Verbales\n\nComparación:\n- Presente: yo hablo / I speak\n- Pasado: yo hablé / I spoke\n- Futuro: yo hablaré / I will speak",
                "orden": 2
            },
            {
                "titulo": "Estructuras Comunes",
                "contenido": "📝 Estructuras Comunes\n\nDiferencias clave:\n- Uso de 'haber' vs 'have'\n- Verbos reflexivos en español\n- Subjuntivo en español",
                "orden": 3
            }
        ]
        
        for lec in lecciones6:
            Leccion.objects.get_or_create(
                curso=curso6,
                titulo=lec["titulo"],
                defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
            )
    
    print("\n" + "=" * 50)
    print("✅ Cursos completos creados exitosamente!")
    print(f"📚 Total cursos: {Curso.objects.count()}")
    for curso in Curso.objects.filter(activo=True):
        print(f"  - {curso.titulo} ({curso.get_lecciones().count()} lecciones)")

if __name__ == "__main__":
    crear_cursos_completos()
