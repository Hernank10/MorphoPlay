from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import EstadisticasUsuario

class Command(BaseCommand):
    help = 'Lista todos los usuarios registrados'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('📋 USUARIOS REGISTRADOS')
        self.stdout.write('=' * 60)
        self.stdout.write(f"{'ID':<4} {'Usuario':<15} {'Email':<30} {'Tipo':<10} {'Juegos':<8} {'Puntos':<8}")
        self.stdout.write('-' * 60)
        
        for u in User.objects.all().order_by('id'):
            tipo = 'Admin' if u.is_superuser else 'Staff' if u.is_staff else 'Usuario'
            stats = EstadisticasUsuario.objects.filter(usuario=u).first()
            juegos = stats.juegos_completados if stats else 0
            puntos = stats.puntuacion_total if stats else 0
            self.stdout.write(f"{u.id:<4} {u.username:<15} {u.email:<30} {tipo:<10} {juegos:<8} {puntos:<8}")
        
        self.stdout.write('=' * 60)
        self.stdout.write(f'Total: {User.objects.count()} usuarios')
