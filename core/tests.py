from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Dependencia, Vehiculo

class VehiculoAPITest(APITestCase):
    def setUp(self):
        for g in ['admin','capturista','consulta']:
            Group.objects.get_or_create(name=g)
        self.dep = Dependencia.objects.create(nombre='Dep1')
        self.capturista = User.objects.create_user('capt', password='pass')
        self.capturista.groups.add(Group.objects.get(name='capturista'))
        self.consulta = User.objects.create_user('cons', password='pass')
        self.consulta.groups.add(Group.objects.get(name='consulta'))

    def test_consulta_cannot_create(self):
        self.client.login(username='cons', password='pass')
        data = {
            'numero_economico': '1',
            'dependencia': self.dep.id,
            'serie': 'S1',
        }
        resp = self.client.post('/api/vehiculos/', data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_capturista_can_create(self):
        self.client.login(username='capt', password='pass')
        data = {
            'numero_economico': '1',
            'dependencia': self.dep.id,
            'serie': 'S1',
        }
        resp = self.client.post('/api/vehiculos/', data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
