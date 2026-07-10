#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Categoria, Nivel, Leccion, Evaluacion, PreguntaEvaluacion

def crear_curso_narrativa_colombiana():
    print("📚 Creando curso: 100 Técnicas de Redacción Morfosintáctica")
    print("=" * 60)
    
    try:
        literatura = Categoria.objects.get(nombre="Literatura")
        avanzado = Nivel.objects.get(nombre="Avanzado")
        experto = Nivel.objects.get(nombre="Experto")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Crear el curso
    curso, created = Curso.objects.get_or_create(
        titulo="100 Técnicas de Redacción Morfosintáctica - Narrativa Colombiana",
        defaults={
            "descripcion": """📖 Curso completo de técnicas de redacción morfosintáctica aplicadas a la narrativa de la novela colombiana.

🎯 Objetivos del curso:
• Dominar 100 técnicas de redacción narrativa
• Aplicar estructuras morfosintácticas avanzadas
• Analizar y crear textos narrativos
• Desarrollar estilo propio

📚 Autores colombianos de referencia:
• Gabriel García Márquez
• Álvaro Mutis
• Laura Restrepo
• Fernando Vallejo
• Andrés Caicedo

📖 Técnicas que aprenderás:
• Uso de la elipsis temporal
• Prolepsis y analepsis
• Monólogo interior
• Flujo de conciencia
• Y 95 técnicas más...""",
            "categoria": literatura,
            "nivel": experto,
            "duracion_estimada": 40,
            "orden": 7
        }
    )
    
    if created:
        print(f"  ✅ Curso creado: {curso.titulo}")
    else:
        print(f"  ⏳ Curso ya existe: {curso.titulo}")
        return
    
    # ============================================================
    # LECCIONES - 10 bloques de 10 técnicas cada uno
    # ============================================================
    
    tecnicas = [
        # Bloque 1: Fundamentos Narrativos (1-10)
        {
            "titulo": "Técnicas de Estructura Narrativa I",
            "contenido": """📖 TÉCNICAS 1-10: ESTRUCTURA NARRATIVA

🔍 1. **Elipsis Temporal**
Salto temporal sin explicación. García Márquez: "Muchos años después, frente al pelotón de fusilamiento..."

📝 2. **Analepsis (Flashback)**
Retroceso en el tiempo. Ejemplo: "Recordaba aquella tarde en Macondo..."

⏰ 3. **Prolepsis (Flashforward)**
Anticipación de eventos futuros. "Tres años después, todo había cambiado..."

📋 4. **Estructura Circular**
Inicio y final en el mismo punto. "Cien años de soledad" comienza y termina con los Buendía.

🎭 5. **Multiperspectivismo**
Varios puntos de vista narrativos. "La hojarasca" de García Márquez.

🔀 6. **Narración No Lineal**
Saltos cronológicos intencionales.

💭 7. **Monólogo Interior**
Pensamientos del personaje sin filtro.

🌊 8. **Flujo de Conciencia**
Corriente de pensamientos sin estructura.

🗣️ 9. **Estilo Indirecto Libre**
Mezcla de narrador y personaje.

🔄 10. **Técnica del Espejo**
Reflejo de situaciones simétricas.

📝 EJERCICIO PRÁCTICO:
Escribe un párrafo usando al menos 3 de estas técnicas.""",
            "orden": 1
        },
        {
            "titulo": "Técnicas de Descripción I",
            "contenido": """📖 TÉCNICAS 11-20: DESCRIPCIÓN

🔍 11. **Descripción Detallada**
Minucia en los detalles.

🎨 12. **Sinestesia**
Mezcla de sentidos. "Olor a color".

🌿 13. **Realismo Mágico**
Lo fantástico como cotidiano.

📸 14. **Fotografía Literaria**
Descripción como imagen congelada.

💨 15. **Descripción Cinética**
Movimiento en la descripción.

🎵 16. **Ritmo Descriptivo**
Cadencia en la descripción.

🌅 17. **Paisaje Interior**
Reflejo del estado anímico.

🌀 18. **Descripción Espiral**
De lo general a lo particular.

🔮 19. **Sugerencia Descriptiva**
Insinuar en lugar de decir.

📝 20. **Catálogo Descriptivo**
Lista de elementos.

📝 EJERCICIO PRÁCTICO:
Describe un paisaje usando 3 técnicas diferentes.""",
            "orden": 2
        },
        {
            "titulo": "Técnicas de Diálogo I",
            "contenido": """📖 TÉCNICAS 21-30: DIÁLOGO

🗣️ 21. **Diálogo Directo**
Palabras textuales con guiones.

💬 22. **Diálogo Indirecto**
Resumen de lo dicho.

🎭 23. **Subtexto**
Lo no dicho en el diálogo.

⏸️ 24. **Silencio Significativo**
Pausas cargadas de significado.

🔄 25. **Diálogo Circular**
Conversaciones que vuelven al inicio.

📝 26. **Elipsis Dialógica**
Saltos en la conversación.

🎯 27. **Diálogo Teleológico**
Conversación con propósito.

🌊 28. **Monólogo Dramático**
Personaje habla solo.

🗣️ 29. **Estilo Indirecto Libre en Diálogo**
Mezcla de narrador y personaje.

📝 30. **Diálogo Coral**
Múltiples voces.

📝 EJERCICIO PRÁCTICO:
Escribe un diálogo usando 4 técnicas.""",
            "orden": 3
        },
        {
            "titulo": "Técnicas de Personajes I",
            "contenido": """📖 TÉCNICAS 31-40: PERSONAJES

🎭 31. **Caracterización Indirecta**
Revelar al personaje a través de acciones.

📝 32. **Retrato Psicológico**
Profundidad interior del personaje.

🔄 33. **Arco de Transformación**
Evolución del personaje.

🔀 34. **Doble Personalidad**
Personaje con facetas contradictorias.

💭 35. **Pensamiento como Acción**
Los pensamientos mueven la trama.

🎭 36. **Personaje Arquetípico**
Modelos universales.

🌀 37. **Espejismo del Personaje**
Apariencia vs realidad.

📚 38. **Antecedentes del Personaje**
Historia previa.

🔮 39. **Futuro del Personaje**
Proyección del personaje.

📝 40. **Galería de Personajes**
Conjunto de personajes interrelacionados.

📝 EJERCICIO PRÁCTICO:
Crea un personaje usando 3 técnicas de caracterización.""",
            "orden": 4
        },
        {
            "titulo": "Técnicas de Tiempo y Espacio I",
            "contenido": """📖 TÉCNICAS 41-50: TIEMPO Y ESPACIO

⏰ 41. **Tiempo Cronológico**
Orden temporal lineal.

🌀 42. **Tiempo Circular**
El tiempo vuelve sobre sí mismo.

⏳ 43. **Tiempo Detenido**
Congelar el momento.

🚀 44. **Tiempo Acelerado**
Compresión temporal.

🐢 45. **Tiempo Dilatado**
Expansión del tiempo.

📍 46. **Espacio Simbólico**
Lugares con significado.

🏠 47. **Espacio Íntimo**
Interior de los personajes.

🌍 48. **Espacio Público**
Calles, plazas, ciudades.

🔀 49. **Espacio y Memoria**
Lugares como recuerdos.

📝 50. **Mapa Literario**
Creación de geografía ficticia.

📝 EJERCICIO PRÁCTICO:
Describe un espacio con carga simbólica.""",
            "orden": 5
        },
        {
            "titulo": "Técnicas de Estilo I",
            "contenido": """📖 TÉCNICAS 51-60: ESTILO

✍️ 51. **Estilo Periodístico**
Objetividad y precisión.

📖 52. **Estilo Poético**
Lirismo y musicalidad.

📝 53. **Estilo Barroco**
Exuberancia y ornamentación.

📋 54. **Estilo Minimalista**
Precisión y economía.

🎵 55. **Ritmo Sintáctico**
Cadencia en la oración.

🔀 56. **Variedad Sintáctica**
Diversidad en estructuras.

📝 57. **Parataxis vs Hipotaxis**
Coordinación vs subordinación.

🎭 58. **Estilo Directo**
Sin intermediarios.

🔄 59. **Estilo Indirecto**
Mediado por el narrador.

📝 60. **Estilo Telegráfico**
Frases cortas y concisas.

📝 EJERCICIO PRÁCTICO:
Escribe un texto usando 2 estilos diferentes.""",
            "orden": 6
        },
        {
            "titulo": "Técnicas de Narración I",
            "contenido": """📖 TÉCNICAS 61-70: NARRACIÓN

📖 61. **Narrador Omnisciente**
Lo sabe todo.

👁️ 62. **Narrador Testigo**
Observa desde fuera.

🎭 63. **Narrador Protagonista**
Cuenta su propia historia.

📝 64. **Narrador Equisciente**
Sabe lo que sabe el personaje.

🎯 65. **Narrador Inocente**
Percepción infantil.

🔄 66. **Narrador Múltiple**
Varias voces narrativas.

🌀 67. **Narrador en Espiral**
Conocimiento que crece.

📝 68. **Narrador Fragmentario**
Historias inconexas.

🔮 69. **Narrador Profético**
Conoce el futuro.

📝 70. **Narrador Reflexivo**
Se cuestiona a sí mismo.

📝 EJERCICIO PRÁCTICO:
Escribe un fragmento con narrador diferente al habitual.""",
            "orden": 7
        },
        {
            "titulo": "Técnicas de Trama I",
            "contenido": """📖 TÉCNICAS 71-80: TRAMA

🔄 71. **Trama Circular**
Inicio y final conectados.

⚡ 72. **Trama de Suspenso**
Misterio y expectativa.

🎭 73. **Trama de Conflicto**
Enfrentamiento de fuerzas.

📝 74. **Trama de Búsqueda**
Personaje tras un objetivo.

🌀 75. **Trama de Transformación**
Cambio del personaje.

🔀 76. **Subtramas**
Historias secundarias.

📋 77. **Trama Episódica**
Capítulos independientes.

🎯 78. **Trama Teleológica**
Con un fin claro.

📝 79. **Trama de Descubrimiento**
Revelaciones constantes.

🔄 80. **Trama de Retorno**
Vuelta al punto inicial.

📝 EJERCICIO PRÁCTICO:
Diseña una trama usando 3 técnicas.""",
            "orden": 8
        },
        {
            "titulo": "Técnicas de Ambiente I",
            "contenido": """📖 TÉCNICAS 81-90: AMBIENTE

🌧️ 81. **Atmósfera Emocional**
Ambiente cargado de sentimientos.

🎨 82. **Color como Significado**
Uso simbólico del color.

🔊 83. **Sonido Ambiental**
Audición del entorno.

🌡️ 84. **Clima como Metáfora**
El clima refleja la historia.

📝 85. **Olfato Narrativo**
Olor como elemento narrativo.

✋ 86. **Tacto Literario**
Sensaciones táctiles.

👅 87. **Gusto en la Narración**
Sabores en la literatura.

🌙 88. **Luz y Sombra**
Juego de iluminación.

🌀 89. **Espacio Cerrado vs Abierto**
Confinamiento y libertad.

📝 90. **Ambiente Histórico**
Contexto de época.

📝 EJERCICIO PRÁCTICO:
Crea un ambiente usando 3 sentidos.""",
            "orden": 9
        },
        {
            "titulo": "Técnicas Avanzadas I",
            "contenido": """📖 TÉCNICAS 91-100: AVANZADAS

🔄 91. **Metaliteratura**
Literatura sobre literatura.

🎭 92. **Bricolaje Narrativo**
Mezcla de géneros.

📝 93. **Intertextualidad**
Diálogo con otras obras.

🌀 94. **Estructura en Abismo**
Historias dentro de historias.

🔀 95. **Falsificación Narrativa**
Mentiras del narrador.

📋 96. **Fragmentarismo**
Texto roto y discontinuo.

🎯 97. **Hipérbole Estilística**
Exageración como recurso.

📝 98. **Ironía Estructural**
Doble sentido en la estructura.

🔄 99. **Metáfora Extendida**
Imagen que atraviesa el texto.

🎭 100. **Síntesis Final**
Convergencia de todas las técnicas.

📝 EJERCICIO PRÁCTICO:
Escribe un cuento breve usando 5 técnicas avanzadas.""",
            "orden": 10
        }
    ]
    
    for lec in tecnicas:
        Leccion.objects.get_or_create(
            curso=curso,
            titulo=lec["titulo"],
            defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
        )
    
    print(f"  ✅ {len(tecnicas)} lecciones creadas")
    
    # ============================================================
    # EVALUACIONES
    # ============================================================
    
    # Evaluación 1: Conceptos Básicos
    eval1, created = Evaluacion.objects.get_or_create(
        curso=curso,
        titulo="Evaluación de Conceptos Básicos",
        defaults={
            "descripcion": "Evalúa tu comprensión de las técnicas narrativas fundamentales",
            "tipo": "sumativa",
            "puntaje_maximo": 100,
            "tiempo_limite": 30,
            "intentos_permitidos": 2,
            "orden": 1
        }
    )
    
    if created:
        preguntas = [
            {"p": "¿Qué técnica consiste en saltar en el tiempo sin explicación?", "opciones": ["Elipsis", "Analepsis", "Prolepsis", "Flashback"], "correcta": "Elipsis"},
            {"p": "¿Qué autor colombiano es conocido por el realismo mágico?", "opciones": ["Gabriel García Márquez", "Álvaro Mutis", "Laura Restrepo", "Fernando Vallejo"], "correcta": "Gabriel García Márquez"},
            {"p": "¿Qué técnica usa el pensamiento del personaje sin filtro?", "opciones": ["Monólogo interior", "Flujo de conciencia", "Estilo directo", "Narrador omnisciente"], "correcta": "Monólogo interior"},
            {"p": "¿Qué significa 'prolepsis'?", "opciones": ["Flashback", "Flashforward", "Elipsis", "Analepsis"], "correcta": "Flashforward"},
            {"p": "¿Qué técnica mezcla narrador y personaje?", "opciones": ["Estilo indirecto libre", "Monólogo interior", "Flujo de conciencia", "Narrador omnisciente"], "correcta": "Estilo indirecto libre"},
        ]
        for i, p in enumerate(preguntas, 1):
            PreguntaEvaluacion.objects.create(
                evaluacion=eval1,
                tipo="opcion",
                pregunta=p["p"],
                opcion1=p["opciones"][0],
                opcion2=p["opciones"][1],
                opcion3=p["opciones"][2],
                opcion4=p["opciones"][3],
                respuesta_correcta=p["correcta"],
                puntaje=20,
                orden=i
            )
        print(f"  ✅ Evaluación 1 creada: {eval1.titulo}")
    
    # Evaluación 2: Técnicas Avanzadas
    eval2, created = Evaluacion.objects.get_or_create(
        curso=curso,
        titulo="Evaluación de Técnicas Avanzadas",
        defaults={
            "descripcion": "Evalúa tu dominio de técnicas narrativas avanzadas",
            "tipo": "sumativa",
            "puntaje_maximo": 100,
            "tiempo_limite": 30,
            "intentos_permitidos": 2,
            "orden": 2
        }
    )
    
    if created:
        preguntas2 = [
            {"p": "¿Qué técnica crea historias dentro de historias?", "opciones": ["Estructura en abismo", "Metaliteratura", "Bricolaje", "Intertextualidad"], "correcta": "Estructura en abismo"},
            {"p": "¿Qué técnica es literatura sobre literatura?", "opciones": ["Metaliteratura", "Intertextualidad", "Bricolaje", "Fragmentarismo"], "correcta": "Metaliteratura"},
            {"p": "¿Qué técnica usa el diálogo con otras obras?", "opciones": ["Intertextualidad", "Metaliteratura", "Bricolaje", "Estructura en abismo"], "correcta": "Intertextualidad"},
            {"p": "¿Qué técnica mezcla géneros narrativos?", "opciones": ["Bricolaje", "Fragmentarismo", "Metaliteratura", "Intertextualidad"], "correcta": "Bricolaje"},
            {"p": "¿Qué técnica es texto roto y discontinuo?", "opciones": ["Fragmentarismo", "Bricolaje", "Metaliteratura", "Intertextualidad"], "correcta": "Fragmentarismo"},
        ]
        for i, p in enumerate(preguntas2, 1):
            PreguntaEvaluacion.objects.create(
                evaluacion=eval2,
                tipo="opcion",
                pregunta=p["p"],
                opcion1=p["opciones"][0],
                opcion2=p["opciones"][1],
                opcion3=p["opciones"][2],
                opcion4=p["opciones"][3],
                respuesta_correcta=p["correcta"],
                puntaje=20,
                orden=i
            )
        print(f"  ✅ Evaluación 2 creada: {eval2.titulo}")
    
    print("\n" + "=" * 60)
    print("✅ Curso completo creado exitosamente!")
    print(f"📚 Curso: {curso.titulo}")
    print(f"📖 Lecciones: {curso.get_lecciones().count()}")
    print(f"📝 Evaluaciones: {curso.evaluaciones.count()}")

if __name__ == "__main__":
    crear_curso_narrativa_colombiana()
