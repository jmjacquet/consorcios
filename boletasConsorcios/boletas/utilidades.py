# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import decimal
from django.contrib import messages
from django.conf import settings
from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger',}

TIPO_LOGIN = (    
    (0, 'Barrio/Lote/Manzana'),
    (1, 'Usuario/Contrasenia'),
    (2, 'Consorcio/codUnidad/ContraseniaUnidad')
)

TIPO_CANCHA = (
    (0, 'Tennis'),
    (1, u'Fútbol'),
)
ESTADO = (
    (0, 'Disponible'),
    (1, 'Mantenimiento'),   
)

TIPOUSR = (
    (0, 'Contribuyente'),
    (1, 'Administrador'),
)

ESTADO_CUOTA = (
    (1, 'PENDIENTE'),   
    (2, 'PAGADA'),   
    (3, 'CONVENIO'),   
)

TRIBUTO_CUOTA = (
    (1, 'CUOTA ORD. MANTENIM.'),   
    (2, 'CONVENIO'),   
    (3, 'CONCEPTOS VARIOS'),   
)

ANIOS = (
    ('2025', '2025'),
    ('2024', '2024'),
    ('2023', '2023'),
    ('2022', '2022'),
    ('2021', '2021'),
    ('2020', '2020'),
    ('2019', '2019'),
	('2018', '2018'),
    ('2017', '2017'),
    ('2016', '2016'),
    ('2015', '2015'),
    ('2014', '2014'),
    ('2013', '2013'),
    ('2012', '2012'),
    ('2011', '2011'),
    ('2010', '2010'),
)

MESES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
)

PERIODOS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
)



def digVerificador(num):
    lista = list(num)
    pares= lista[1::2]
    impares= lista[0::2]
    
    totPares = 0
    totImpares = 0

    for i in pares:
        totPares=totPares+int(i*3)

    for i in impares:
        totImpares=totImpares+int(i)
 
    final = totImpares+totPares

    while (final > 9):
        cad=str(final)
        tot=0
        for i in cad:
            tot=tot+int(i)
        final=tot

    return final

def punitorios(cuota,vencimiento,fecha_punit):
    from .models import gg_configuracion
    porc = 0
    try:      
        fecha_punit = fecha_punit
        tipo_interes = gg_configuracion.objects.get(id=settings.MUNI_ID).tipo_punitorios
        interes = gg_configuracion.objects.get(id=settings.MUNI_ID).punitorios
        dias=0
        meses=0

        #Si no tiene definido el interés, lo busco en la configuración
        if interes == None:           
           interes = gg_configuracion.objects.get(id=settings.MUNI_ID).punitorios
           
        if tipo_interes == None:            
           tipo_interes = gg_configuracion.objects.get(id=settings.MUNI_ID).tipo_punitorios

        # if tipo_interes == 10:
        #     from .models import TributoInteres
        #     try:
        #         tributo_interes = TributoInteres.objects.get(id_tributo=cuota.tributo.id_tributo,hasta__gte=vencimiento,desde__lte=vencimiento)
        #         interes = tributo_interes.interes
        #         tipo_interes = tributo_interes.tipo_interes   
        #     except TributoInteres.DoesNotExist:
               
        #         tipo_interes = None
        #         interes = None 

        if tipo_interes == None:
           tipo_interes = 1 
        
        if interes == None:
           interes = 0 
        
        #DIARIO
        if tipo_interes == 2:
            try:
                dias = (fecha_punit - vencimiento).days
            except:
                dias = 0
            if dias < 0:
                dias = 0 
            porc =  (interes/30) * dias
            
        #MENSUAL
        elif tipo_interes == 1:
            try:
                meses = (fecha_punit - vencimiento).days / 30
            except:
                meses = 0
            if meses < 0:
                meses = 0 
            porc =  (interes * meses)        
        else:
            try:
                dias = (fecha_punit - vencimiento).days
            except:
                dias = 0
            if dias < 0:
                dias = 0 
            porc =  (interes / 30 ) * dias

        if porc < 0:
            porc = 0
        
        if settings.DEBUG:
            print 'Interes:'+str(interes)+' TipoInteres:'+str(tipo_interes)+' Meses:'+str(meses)+' Dias:'+str(dias)+' Porc: '+str(porc)+' Venc: '+str(vencimiento)+' FechaPunit: '+str(fecha_punit)
    except KeyError:
        return HttpResponse('Error') # incorrect post
    return porc

