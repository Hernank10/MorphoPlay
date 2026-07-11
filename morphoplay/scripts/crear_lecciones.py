
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morphoplay.settings')
django.setup()

from core.models import Curso, Leccion
from django.db.models import Count

print("📚 Creando lecciones...")

cursos = Curso.objects.filter(activo=True)

for curso in cursos:
    if curso.get_lecciones().count() == 0:
        print(f"  {curso.titulo}")
        
        if "Cognados" in curso.titulo:
            lecciones = [
                {"titulo": "Cognados Perfectos", "contenido": "Palabras iguales o similares.", "orden": 1},
                {"titulo": "Falsos Amigos", "contenido": "Palabras engañosas.", "orden": 2}
            ]
        elif "Técnicas Narrativas" in curso.titulo:
            lecciones = [
                {"titulo": "El Narrador", "contenido": "Tipos de narradores.", "orden": 1},
                {"titulo": "Estructura", "contenido": "Planteamiento, nudo, desenlace.", "orden": 2}
            ]
        else:
            continue
        
        for lec in lecciones:
            Leccion.objects.get_or_create(
                curso=curso,
                titulo=lec["titulo"],
                defaults={"contenido": lec["contenido"], "orden": lec["orden"]}
            )
            print(f"    ✅ {lec['titulo']}")
