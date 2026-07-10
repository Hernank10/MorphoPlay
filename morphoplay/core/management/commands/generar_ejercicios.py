from django.core.management.base import BaseCommand
from core.generador_ejercicios import GeneradorEjercicios, generar_y_guardar_fixture
import json
from pathlib import Path

class Command(BaseCommand):
    help = 'Genera ejercicios interactivos ilimitados'

    def add_arguments(self, parser):
        parser.add_argument('--cantidad', type=int, default=10, help='Número de ejercicios')
        parser.add_argument('--tipo', type=str, choices=GeneradorEjercicios.TIPOS, help='Tipo específico')
        parser.add_argument('--tema', type=str, default='gramatica', help='Tema del ejercicio')
        parser.add_argument('--archivo', type=str, default='ejercicios_generados.json', help='Nombre del archivo')
        parser.add_argument('--cargar', action='store_true', help='Cargar automáticamente')

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        tipo = options['tipo']
        tema = options['tema']
        archivo = options['archivo']
        cargar = options['cargar']
        
        self.stdout.write(f"🎯 Generando {cantidad} ejercicios...")
        
        generador = GeneradorEjercicios()
        if tipo:
            ejercicios = generador.generar_batch(cantidad, [tipo], tema)
        else:
            ejercicios = generador.generar_batch(cantidad, None, tema)
        
        self.stdout.write(f"✅ {len(ejercicios)} ejercicios generados")
        
        fixture = generador.a_django_fixture(ejercicios)
        path = Path(f"core/fixtures/{archivo}")
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(fixture, f, ensure_ascii=False, indent=2)
        
        self.stdout.write(f"💾 Fixture guardado en: {path}")
        
        if cargar:
            self.stdout.write("📥 Cargando ejercicios...")
            from django.core.management import call_command
            call_command('loaddata', str(path))
            self.stdout.write(self.style.SUCCESS("✅ Ejercicios cargados"))
        
        self.stdout.write(self.style.SUCCESS("✅ Completado"))
