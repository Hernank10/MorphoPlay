#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Leccion

def agregar_lecciones():
    print("📚 Agregando lecciones al curso de Redacción Periodística...")
    print("=" * 60)
    
    try:
        curso = Curso.objects.get(titulo="Curso de Redacción Periodística")
    except Curso.DoesNotExist:
        print("❌ Curso no encontrado")
        return
    
    print(f"✅ Curso encontrado: {curso.titulo}")
    
    lecciones_data = [
        {
            "titulo": "Introducción a la Redacción Periodística",
            "contenido": "📖 INTRODUCCION A LA REDACCIÓN PERIODISTICA\n\nLa redaccion periodistica es el arte de contar historias reales de manera clara, precisa y atractiva.\n\nElementos fundamentales:\n- Claridad: El mensaje debe ser entendido por todos\n- Precision: Los hechos deben ser exactos y verificables\n- Brevedad: Decir lo necesario sin rodeos\n- Atractivo: Captar y mantener la atencion del lector\n\nTipos de textos periodisticos:\n1. Noticia: Informacion objetiva de un hecho\n2. Reportaje: Investigacion profunda de un tema\n3. Cronica: Relato con estilo literario\n4. Entrevista: Dialogo con una fuente\n5. Editorial: Opinion institucional\n6. Columna: Opinion personal",
            "orden": 1
        },
        {
            "titulo": "La Pirámide Invertida",
            "contenido": "📐 LA PIRAMIDE INVERTIDA\n\nLa piramide invertida es la estructura mas utilizada en el periodismo.\n\nEstructura:\n1. LEAD (lo mas importante)\n2. DESARROLLO (informacion secundaria)\n3. DETALLES (informacion adicional)\n4. CONTEXTO (informacion de fondo)\n\nCaracteristicas:\n- La informacion mas relevante al inicio\n- Los detalles menos importantes al final\n- Permite recortar sin perder lo esencial\n- Facilita la lectura rapida\n\nEjemplo:\nEl gobierno anuncio hoy un nuevo plan de salud que beneficiara a 2 millones de personas. La medida incluye la construccion de 50 centros de atencion primaria en zonas vulnerables y la contratacion de 3.000 profesionales de la salud. El plan comenzara a implementarse en enero de 2026.",
            "orden": 2
        },
        {
            "titulo": "El Lead Periodístico",
            "contenido": "📝 EL LEAD PERIODISTICO\n\nEl lead (o entrada) es el primer parrafo de la noticia. Debe captar la atencion y resumir lo esencial.\n\nTipos de lead:\n\n1. Lead Directo\nResponde a las 5W: Que?, Quien?, Cuando?, Donde?, Por que?\nEjemplo: El presidente anuncio ayer en Bogota un nuevo plan de salud.\n\n2. Lead de Resumen\nSintetiza lo mas importante en una oracion.\nEjemplo: 2 millones de colombianos se beneficiaran del nuevo plan de salud.\n\n3. Lead de Contraste\nEnfrenta dos ideas opuestas.\nEjemplo: Mientras el gobierno anuncia un plan de salud, los hospitales estan colapsados.\n\n4. Lead de Suspenso\nCrea expectativa.\nEjemplo: Nadie esperaba el anuncio que cambiaria el sistema de salud.\n\n5. Lead de Cita\nComienza con una declaracion textual.\nEjemplo: Este es el plan de salud mas ambicioso de la historia, afirmo el presidente.\n\nConsejos para un lead efectivo:\n- Maximo 25 palabras\n- Incluir la informacion mas relevante\n- Usar verbos de accion\n- Evitar tecnicismos innecesarios",
            "orden": 3
        },
        {
            "titulo": "Fuentes Periodísticas",
            "contenido": "🔍 FUENTES PERIODISTICAS\n\nLas fuentes son el fundamento de todo trabajo periodistico.\n\nTipos de fuentes:\n\n1. Por su naturaleza:\n- Fuentes directas: Testigos presenciales\n- Fuentes indirectas: Documentos, informes\n- Fuentes oficiales: Instituciones, gobierno\n- Fuentes extraoficiales: Anonimas, confidenciales\n\n2. Por su numero:\n- Fuente unica: Una sola persona\n- Multiples fuentes: Varias personas\n\nBuenas practicas:\n- Verificar siempre la credibilidad de la fuente\n- Contrastar la informacion con al menos dos fuentes\n- Citar correctamente a las fuentes\n- Proteger la identidad de las fuentes cuando sea necesario\n- No prometer anonimato si no se puede garantizar\n\nComo citar fuentes:\n- Directa: Texto exacto, dijo Juan Perez.\n- Indirecta: Juan Perez afirmo que el plan es viable.\n- Referencia: Segun el informe del Ministerio...",
            "orden": 4
        },
        {
            "titulo": "Titulares y Subtítulos",
            "contenido": "📰 TITULARES Y SUBTITULOS\n\nEl titular es la puerta de entrada a la noticia. Debe ser preciso, atractivo y claro.\n\nCaracteristicas de un buen titular:\n- Breve: Maximo 10 palabras\n- Preciso: Decir lo esencial\n- Atractivo: Captar la atencion\n- Claro: Sin ambiguedades\n\nTipos de titulares:\n1. Titular informativo: Resume el hecho\n   Gobierno anuncia nuevo plan de salud\n\n2. Titular de pregunta: Genera curiosidad\n   Como afectara el nuevo plan de salud?\n\n3. Titular de citas: Usa declaraciones\n   Es el mejor plan de salud, afirma ministro\n\n4. Titular de llamado: Exhorta al lector\n   Conoce los detalles del nuevo plan\n\nSubtitulos:\n- Amplian la informacion del titular\n- Contextualizan la noticia\n- No repiten el titular\n\nEjemplo:\nTitular: Colombia tendra el plan de salud mas ambicioso\nSubtitulo: El gobierno invertira 5 billones de pesos en infraestructura hospitalaria",
            "orden": 5
        },
        {
            "titulo": "Estructura de la Noticia",
            "contenido": "📋 ESTRUCTURA DE LA NOTICIA\n\nLa noticia tiene una estructura definida que facilita su comprension.\n\nPartes de la noticia:\n\n1. Titular\n- Atrae la atencion\n- Resume lo esencial\n\n2. Lead (Entrada)\n- Primer parrafo\n- Contiene la informacion mas importante\n- Responde a las 5W\n\n3. Cuerpo de la noticia\n- Desarrolla la informacion\n- Incluye citas y detalles\n- Sigue la piramide invertida\n\n4. Cierre\n- Informacion adicional\n- Contexto\n- Puede incluir datos de contacto\n\nEjemplo:\n\nTitular: Nuevo plan de salud llegara a 2 millones de colombianos\n\nLead: El gobierno nacional anuncio hoy un ambicioso plan de salud que beneficiara a 2 millones de ciudadanos en zonas vulnerables.\n\nCuerpo: La iniciativa contempla la construccion de 50 centros de atencion primaria y la contratacion de 3.000 profesionales de la salud. El ministro de Salud, Juan Perez, destaco que este es el plan mas importante de los ultimos 20 anos.\n\nCierre: El plan comenzara a implementarse en enero de 2026 y tiene una inversion estimada de 5 billones de pesos.",
            "orden": 6
        },
        {
            "titulo": "Ética Periodística",
            "contenido": "⚖️ ETICA PERIODISTICA\n\nLa etica es fundamental en el periodismo. El periodista tiene la responsabilidad de informar con verdad y respeto.\n\nPrincipios eticos:\n\n1. Veracidad\n- Informar con hechos verificados\n- No inventar ni manipular\n- Corregir errores publicamente\n\n2. Objetividad\n- Presentar todos los puntos de vista\n- No tomar partido\n- Ser equilibrado\n\n3. Responsabilidad\n- Consecuencias de lo que se publica\n- Proteger a las victimas\n- No causar dano innecesario\n\n4. Independencia\n- No aceptar presiones\n- No tener conflictos de interes\n- Ser autonomo\n\n5. Transparencia\n- Revelar las fuentes cuando sea posible\n- Explicar el proceso\n- Ser honesto con el publico\n\nSituaciones eticas complejas:\n- Fuentes anonimas\n- Imagenes sensibles\n- Privacidad vs interes publico\n- Conflictos de interes",
            "orden": 7
        },
        {
            "titulo": "Entrevista Periodística",
            "contenido": "🎤 ENTREVISTA PERIODISTICA\n\nLa entrevista es una herramienta fundamental para obtener informacion de fuentes.\n\nTipos de entrevista:\n\n1. Por su formato:\n- Presencial: Cara a cara\n- Telefonica: Por telefono\n- Escrita: Por correo o mensajes\n- Virtual: Videollamada\n\n2. Por su objetivo:\n- Informativa: Obtener datos\n- De opinion: Conocer puntos de vista\n- De perfil: Retratar a una persona\n\nPreparacion:\n1. Investigar al entrevistado\n2. Preparar preguntas\n3. Definir objetivos\n4. Elegir el formato adecuado\n\nConsejos para entrevistar:\n- Escuchar activamente\n- Hacer preguntas abiertas\n- No interrumpir\n- Tomar notas o grabar\n- Ser respetuoso\n- Hacer preguntas de seguimiento\n\nEjemplo de preguntas:\n- Que opina sobre...?\n- Como se sintio cuando...?\n- Que espera del futuro?\n- Que mensaje daria a...?",
            "orden": 8
        },
        {
            "titulo": "Reportaje y Crónica",
            "contenido": "📖 REPORTAJE Y CRONICA\n\nEl reportaje y la cronica son generos periodisticos que profundizan en los temas.\n\nReportaje:\n- Investigacion profunda\n- Contexto y analisis\n- Multiples fuentes\n- Estructura flexible\n\nTipos de reportaje:\n1. Informativo: Hechos y datos\n2. Interpretativo: Analisis y contexto\n3. De investigacion: Revelaciones\n4. Narrativo: Con estilo literario\n\nCronica:\n- Relato de eventos\n- Estilo literario\n- Punto de vista del autor\n- Secuencia temporal\n\nDiferencias:\nReportaje: Profundidad, Contexto, Analisis, Objetividad\nCronica: Inmediatez, Secuencia, Narracion, Subjetividad\n\nEjemplo de cronica:\nLa tarde comenzo como cualquier otra en la plaza principal. Los vendedores ambulantes ofrecian sus productos, los ninos jugaban y los ancianos conversaban en las bancas. De repente, un grito rompio la rutina...",
            "orden": 9
        },
        {
            "titulo": "Edición y Corrección de Estilo",
            "contenido": "✍️ EDICION Y CORRECCION DE ESTILO\n\nLa edicion es el proceso de pulir el texto periodistico para que sea claro, preciso y atractivo.\n\nProceso de edicion:\n\n1. Revision de contenido\n- Verificar hechos\n- Confirmar fuentes\n- Evaluar relevancia\n\n2. Correccion de estilo\n- Eliminar redundancias\n- Mejorar la redaccion\n- Ajustar el tono\n\n3. Revision gramatical\n- Ortografia\n- Sintaxis\n- Puntuacion\n\nLista de verificacion:\n- El titular es claro y atractivo?\n- El lead responde a las 5W?\n- La informacion esta jerarquizada?\n- Las fuentes estan citadas correctamente?\n- El texto es conciso y claro?\n- Hay errores gramaticales?\n- El tono es adecuado?\n\nConsejos de edicion:\n- Leer en voz alta\n- Dejar reposar el texto\n- Pedir una segunda opinion\n- Usar herramientas de correccion\n- No tener miedo de cortar\n\nErrores comunes:\n- Oraciones demasiado largas\n- Adjetivos innecesarios\n- Verbos pasivos\n- Repeticiones\n- Jerga excesiva",
            "orden": 10
        }
    ]
    
    creadas = 0
    for data in lecciones_data:
        leccion, created = Leccion.objects.get_or_create(
            curso=curso,
            titulo=data["titulo"],
            defaults={
                "contenido": data["contenido"],
                "orden": data["orden"]
            }
        )
        if created:
            creadas += 1
            print(f"  ✅ Leccion creada: {data['titulo']}")
        else:
            print(f"  ⏳ Leccion ya existe: {data['titulo']}")
    
    print("\n" + "=" * 60)
    print(f"✅ {creadas} lecciones agregadas al curso")
    print(f"📊 Total lecciones en el curso: {curso.get_lecciones().count()}")

if __name__ == "__main__":
    agregar_lecciones()
