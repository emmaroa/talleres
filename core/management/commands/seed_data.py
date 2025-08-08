from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from core.models import Dependencia, Vehiculo

class Command(BaseCommand):
    help = 'Create initial groups, users and sample data'

    def handle(self, *args, **options):
        groups = ['admin', 'capturista', 'consulta']
        for g in groups:
            Group.objects.get_or_create(name=g)

        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', password='admin')
            admin_group = Group.objects.get(name='admin')
            admin_user.groups.add(admin_group)
            self.stdout.write('Created admin user')

        if not User.objects.filter(username='capturista').exists():
            user = User.objects.create_user('capturista', password='capturista')
            user.groups.add(Group.objects.get(name='capturista'))
            self.stdout.write('Created capturista user')

        if not User.objects.filter(username='consulta').exists():
            user = User.objects.create_user('consulta', password='consulta')
            user.groups.add(Group.objects.get(name='consulta'))
            self.stdout.write('Created consulta user')

        deps = ['Conservación de Vialidades', 'Servicios Públicos', 'Seguridad']
        for nombre in deps:
            Dependencia.objects.get_or_create(nombre=nombre)

        if Vehiculo.objects.count() == 0:
            dep = Dependencia.objects.first()
            for i in range(1,11):
                Vehiculo.objects.create(
                    numero_economico=f'VEH-{i:03}',
                    descripcion=f'Vehiculo {i}',
                    dependencia=dep,
                    placas=f'ABC{i:03}',
                    serie=f'SERIE{i:03}',
                    factura='F123',
                    resguardante='Juan Perez',
                )
            self.stdout.write('Created sample vehicles')
