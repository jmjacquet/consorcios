"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


from django.test import TestCase
from .models import gg_canchas_reserva,gg_propietario,gg_canchas



dia = date.today().day
mes = datetime.today().month
anio = datetime.today().year
ahora = datetime.today().hour
hora_hoy=datetime(anio, mes, dia, ahora)

 class gg_canchas_reservaTestCase(TestCase):
 def setUp(self):
  p1 = gg_propietario.objects.create(id_propietario=99999,nombre_propietario="JUANMA")
  p2 = gg_propietario.objects.create(id_propietario=99998,nombre_propietario="PEPE POMPIN")
  c1 = gg_canchas.objects.create(id_cancha=99,estado=0,tipo=0,codigo='CANCHA 1')
  c2 = gg_canchas.objects.create(id_cancha=98,estado=0,tipo=0,codigo='CANCHA 2')
  r1=gg_canchas_reserva.objects.create(id_propietario=99999,id_cancha=99,hora_inicio=hora_hoy)
  r2=gg_canchas_reserva.objects.create(id_propietario=99998,id_cancha=98,hora_inicio=hora_hoy)

  def test_gg_canchas_reserva_prop(self):
  r1= gg_canchas_reserva.objects.get(id_propietario=99999,id_cancha=99)
  self.assertEqual(r1.id_propietario.nombre_propietario, "JUANMA")  

  def test_gg_canchas_reserva_disponible(self):
  r1= gg_canchas_reserva.objects.get(id_propietario=99999,id_cancha=99)
  self.assertIsNotNone(r1)  
