#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Evaluacion, PreguntaEvaluacion, Juego

def crear_evaluaciones_periodisticas():
    print("📝 Creando evaluaciones con los 100 ejercicios periodísticos...")
    print("=" * 60)
    
    # Obtener o crear un curso para periodismo
    curso, created = Curso.objects.get_or_create(
        titulo="Curso de Redacción Periodística",
        defaults={
            "descripcion": "Curso completo de redacción periodística con 100 ejercicios prácticos",
            "categoria_id": 4,  # Literatura
            "nivel_id": 3,      # Avanzado
            "duracion_estimada": 20,
            "orden": 8
        }
    )
    
    if created:
        print(f"  ✅ Curso creado: {curso.titulo}")
    else:
        print(f"  ⏳ Curso ya existe: {curso.titulo}")
    
    # Obtener los juegos periodísticos (IDs 1001-1100)
    ejercicios = Juego.objects.filter(id__gte=1001, id__lte=1100, activo=True).order_by('id')
    
    if not ejercicios:
        print("❌ No se encontraron ejercicios periodísticos. Carga primero el archivo JSON.")
        return
    
    print(f"📊 Ejercicios encontrados: {ejercicios.count()}")
    
    # Crear evaluaciones agrupadas (10 evaluaciones de 10 preguntas cada una)
    evaluaciones_creadas = 0
    preguntas_creadas = 0
    
    for i in range(0, 10):
        bloque = ejercicios[i*10:(i+1)*10]
        if not bloque:
            break
        
        # Crear evaluación para este bloque
        eval_nombre = f"Evaluación Periodística - Bloque {i+1} (Técnicas {i*10+1}-{(i+1)*10})"
        
        evaluacion, created = Evaluacion.objects.get_or_create(
            curso=curso,
            titulo=eval_nombre,
            defaults={
                "descripcion": f"Evaluación de las técnicas {i*10+1} a {(i+1)*10} de redacción periodística",
                "tipo": "sumativa",
                "puntaje_maximo": 100,
                "tiempo_limite": 20,
                "intentos_permitidos": 2,
                "orden": i+1
            }
        )
        
        if created:
            print(f"  ✅ Evaluación creada: {eval_nombre}")
            evaluaciones_creadas += 1
        else:
            print(f"  ⏳ Evaluación ya existe: {eval_nombre}")
            # Si ya existe, eliminar preguntas anteriores para recrearlas
            PreguntaEvaluacion.objects.filter(evaluacion=evaluacion).delete()
        
        # Crear preguntas para esta evaluación
        for idx, juego in enumerate(bloque, 1):
            # Verificar que el juego tiene opciones
            opciones = juego.get_opciones()
            if not opciones or not any(opciones):
                print(f"    ⚠️ Juego {juego.id} no tiene opciones válidas")
                continue
            
            pregunta, created = PreguntaEvaluacion.objects.get_or_create(
                evaluacion=evaluacion,
                pregunta=juego.pregunta or f"Pregunta sobre {juego.titulo}",
                defaults={
                    "tipo": "opcion",
                    "opcion1": opciones[0] if len(opciones) > 0 else "",
                    "opcion2": opciones[1] if len(opciones) > 1 else "",
                    "opcion3": opciones[2] if len(opciones) > 2 else "",
                    "opcion4": opciones[3] if len(opciones) > 3 else "",
                    "respuesta_correcta": juego.respuesta_correcta,
                    "puntaje": 10,
                    "orden": idx
                }
            )
            
            if created:
                preguntas_creadas += 1
        
        print(f"    ✅ {preguntas_creadas - (i*10)} preguntas creadas")
    
    print("\n" + "=" * 60)
    print("✅ Evaluaciones creadas exitosamente!")
    print(f"📚 Curso: {curso.titulo}")
    print(f"📝 Evaluaciones creadas: {evaluaciones_creadas}")
    print(f"❓ Preguntas creadas: {preguntas_creadas}")
    print(f"📊 Total preguntas por evaluación: 10")
    
    # Mostrar resumen
    print("\n📋 Resumen de evaluaciones:")
    for eval in Evaluacion.objects.filter(curso=curso).order_by('orden'):
        preguntas = PreguntaEvaluacion.objects.filter(evaluacion=eval).count()
        print(f"  - {eval.titulo}: {preguntas} preguntas")

if __name__ == "__main__":
    crear_evaluaciones_periodisticas()
