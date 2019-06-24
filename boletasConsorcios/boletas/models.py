# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from .utilidades import ESTADO,TIPO_CANCHA,TIPOUSR,ESTADO_CUOTA,TRIBUTO_CUOTA,TIPO_LOGIN
from django.contrib.auth.models import User
from datetime import datetime,date
from dateutil.relativedelta import *
from django.conf import settings
import os 

def mandarEmailContrasenia(prop):
    from smtplib import SMTP
    from email.mime.text import MIMEText as text  
        
    to_addr=prop.email
    if to_addr is None:
        return ''
    if to_addr =='':
        return ''
    if prop.cod_web is None:
        return ''
   
    try:
        sitio = gg_configuracion.objects.get(id=settings.MUNI_ID)
        email = sitio.email

    except gg_configuracion.DoesNotExist:
        sitio = None

    if not email:
        email = 'contacto@grupoguadalupe.com.ar'
        
    msg = u'Mail recordatorio de su cambio de password.\n Su nuevo password es: %s .\nAtte. %s' % (str(prop.cod_web),str(sitio.nombre))

    m = text(msg.encode('utf-8'))

    m['Subject'] = 'Cambio de Password (Sistema Aires del Llano OnLine)'
    m['From'] = email
    m['To'] = to_addr    
    s = SMTP()
    s.connect('smtp.webfaction.com')
    s.login(str('grupogua_juanmanuel'),str('qwerty'))
    s.sendmail(email, to_addr, m.as_string())
    message="Se envio correctamente el email con la reserva."            
    return message


class gg_consorcio(models.Model):
    id_consorcio = models.IntegerField(db_column='ID_CONSORCIO',primary_key=True) # Field name made lowercase.
    id_tipo_consorcio = models.IntegerField(db_column='ID_TIPO_CONSORCIO',blank=True, null=True) # Field name made lowercase.    
    codigo = models.CharField(db_column='CODIGO', max_length=20, blank=True, null=True) # Field name made lowercase.
    nombre_consorcio = models.CharField(db_column='NOMBRE_CONSORCIO', max_length=100, blank=True, null=True) # Field name made lowercase.    
    nombre_web = models.CharField(db_column='NOMBRE_WEB', max_length=30, blank=True, null=True) # Field name made lowercase.    
    baja = models.CharField(db_column='BAJA', max_length=1, blank=True, null=True) # Field name made lowercase.    
    class Meta:
        db_table = 'gg_consorcio'
        
    def __unicode__(self):
        return u'%s - %s' % (self.codigo,self.nombre_consorcio)

class gg_concepto(models.Model):
    id_concepto = models.IntegerField(db_column='ID_CONCEPTO',primary_key=True) # Field name made lowercase.
    id_tipo_concepto = models.IntegerField(db_column='ID_TIPO_CONCEPTO') # Field name made lowercase.
    id_consorcio = models.ForeignKey('gg_consorcio',db_column='ID_CONSORCIO') # Field name made lowercase.
    id_tipo_unidad = models.IntegerField(db_column='ID_TIPO_UNIDAD', blank=True, null=True) # Field name made lowercase.
    id_proveedor = models.IntegerField(db_column='ID_PROVEEDOR', blank=True, null=True) # Field name made lowercase.
    orden = models.IntegerField(db_column='ORDEN', blank=True, null=True) # Field name made lowercase.
    nombre_concepto = models.CharField(db_column='NOMBRE_CONCEPTO', max_length=200, blank=True) # Field name made lowercase.
    monto = models.DecimalField(db_column='MONTO', max_digits=15, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    porcentaje = models.DecimalField(db_column='PORCENTAJE', max_digits=15, decimal_places=4, blank=True, null=True) # Field name made lowercase.
    enero = models.CharField(db_column='ENERO', max_length=1, blank=True) # Field name made lowercase.
    febrero = models.CharField(db_column='FEBRERO', max_length=1, blank=True) # Field name made lowercase.
    marzo = models.CharField(db_column='MARZO', max_length=1, blank=True) # Field name made lowercase.
    abril = models.CharField(db_column='ABRIL', max_length=1, blank=True) # Field name made lowercase.
    mayo = models.CharField(db_column='MAYO', max_length=1, blank=True) # Field name made lowercase.
    junio = models.CharField(db_column='JUNIO', max_length=1, blank=True) # Field name made lowercase.
    julio = models.CharField(db_column='JULIO', max_length=1, blank=True) # Field name made lowercase.
    agosto = models.CharField(db_column='AGOSTO', max_length=1, blank=True) # Field name made lowercase.
    septiembre = models.CharField(db_column='SEPTIEMBRE', max_length=1, blank=True) # Field name made lowercase.
    octubre = models.CharField(db_column='OCTUBRE', max_length=1, blank=True) # Field name made lowercase.
    noviembre = models.CharField(db_column='NOVIEMBRE', max_length=1, blank=True) # Field name made lowercase.
    diciembre = models.CharField(db_column='DICIEMBRE', max_length=1, blank=True) # Field name made lowercase.
    baja = models.CharField(db_column='BAJA', max_length=1, blank=True) # Field name made lowercase.
    codigo = models.CharField(db_column='CODIGO', max_length=20, blank=True) # Field name made lowercase.
    id_tributo = models.IntegerField(db_column='ID_TRIBUTO', blank=True, null=True) # Field name made lowercase.
    id_tipo_calculo = models.IntegerField(db_column='ID_TIPO_CALCULO', blank=True, null=True) # Field name made lowercase.
    class Meta:
        db_table = 'gg_concepto'
        
    def __unicode__(self):
        return u'%s' % (self.nombre_concepto)

class gg_propietario(models.Model):
    id_propietario = models.IntegerField(u'Propietario',db_column='ID_PROPIETARIO', primary_key=True) # Field name made lowercase.
    id_tipo_doc = models.IntegerField(db_column='ID_TIPO_DOC', blank=True, null=True) # Field name made lowercase.
    id_tipo_iva = models.IntegerField(db_column='ID_TIPO_IVA', blank=True, null=True) # Field name made lowercase.
    id_provincia = models.IntegerField(db_column='ID_PROVINCIA', blank=True, null=True) # Field name made lowercase.
    id_pais = models.IntegerField(db_column='ID_PAIS', blank=True, null=True) # Field name made lowercase.
    codigo = models.CharField(db_column='CODIGO', max_length=10, blank=True) # Field name made lowercase.
    nombre_propietario = models.CharField(db_column='NOMBRE_PROPIETARIO', max_length=100) # Field name made lowercase.
    nro_documento = models.DecimalField(db_column='NRO_DOCUMENTO', max_digits=18, decimal_places=0, blank=True, null=True) # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=200, blank=True) # Field name made lowercase.
    localidad = models.CharField(db_column='LOCALIDAD', max_length=100, blank=True) # Field name made lowercase.
    codigo_postal = models.CharField(db_column='CODIGO_POSTAL', max_length=10, blank=True) # Field name made lowercase.
    fecha_nac = models.DateField(db_column='FECHA_NAC', blank=True, null=True) # Field name made lowercase.
    sexo = models.CharField(db_column='SEXO', max_length=1, blank=True) # Field name made lowercase.
    cuit_cuil = models.CharField(db_column='CUIT_CUIL', max_length=30, blank=True) # Field name made lowercase.
    telefono = models.CharField(db_column='TELEFONO', max_length=100, blank=True) # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, blank=True) # Field name made lowercase.
    cod_web = models.CharField(db_column='COD_WEB', max_length=10, blank=True) # Field name made lowercase.
    baja = models.CharField(db_column='BAJA', max_length=1, blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'gg_propietario'
        verbose_name = u'Propietario'
        verbose_name_plural = u'Propietarios'  

    def __unicode__(self):
        return u'%s - %s' % (self.nombre_propietario,self.nro_documento)

    def save(self):
        if self.id_propietario:
            prop_ant = gg_propietario.objects.get(pk=self.id_propietario)

            if (prop_ant.cod_web <> self.cod_web):
                mandarEmailContrasenia(self)
        super(gg_propietario, self).save()    

class gg_tipo_unidad(models.Model):
    id_tipo_unidad = models.IntegerField(db_column='ID_TIPO_UNIDAD', primary_key=True) # Field name made lowercase.
    nombre_tipo_unidad = models.CharField(db_column='NOMBRE_UNIDAD', max_length=30, blank=True) # Field name made lowercase.
    baja = models.CharField(db_column='BAJA', max_length=1, blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'gg_tipo_unidad'
        verbose_name = u'Tipo Unidad'
        verbose_name_plural = u'Tipos de Unidad'
    
    def __unicode__(self):
        return u'%s' % (self.nombre_tipo_unidad)

class gg_unidad_consorcio(models.Model):
    id_unidad = models.IntegerField(db_column='ID_UNIDAD', primary_key=True) # Field name made lowercase.
    id_tipo_unidad = models.ForeignKey('gg_tipo_unidad', db_column='ID_TIPO_UNIDAD',db_index=True)
    id_consorcio = models.ForeignKey('gg_consorcio',db_column='ID_CONSORCIO') # Field name made lowercase.
    id_propietario = models.ForeignKey('gg_propietario', db_column='ID_PROPIETARIO',db_index=True)
    codigo = models.CharField(db_column='CODIGO', max_length=10, blank=True) # Field name made lowercase.
    nombre_unidad = models.CharField(db_column='NOMBRE_UNIDAD', max_length=30, blank=True) # Field name made lowercase.
    alquilado = models.CharField(db_column='ALQUILADO', max_length=1, blank=True) # Field name made lowercase.
    datos_ocupante = models.CharField(db_column='DATOS_OCUPANTE', max_length=100, blank=True) # Field name made lowercase.
    domicilio_reparto = models.CharField(db_column='DOMICILIO_REPARTO', max_length=1000, blank=True) # Field name made lowercase.
    boleta_separada = models.CharField(db_column='BOLETA_SEPARADA', max_length=1, blank=True) # Field name made lowercase.
    porcentaje = models.DecimalField(db_column='PORCENTAJE', max_digits=15, decimal_places=4, blank=True, null=True) # Field name made lowercase.
    superficie = models.DecimalField(db_column='SUPERFICIE', max_digits=15, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    baja = models.CharField(db_column='BAJA', max_length=1, blank=True) # Field name made lowercase.
    detalle = models.CharField(db_column='DETALLE', max_length=2000, blank=True) # Field name made lowercase.
    torre = models.CharField(db_column='TORRE', max_length=50, blank=True) # Field name made lowercase.
    piso = models.CharField(db_column='PISO', max_length=50, blank=True) # Field name made lowercase.
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=50, blank=True) # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=50, blank=True) # Field name made lowercase.
    manzana = models.CharField(db_column='MANZANA', max_length=50, blank=True) # Field name made lowercase.
    lote = models.CharField(db_column='LOTE', max_length=50, blank=True) # Field name made lowercase.
    cod_web = models.CharField(db_column='COD_WEB', max_length=10, blank=True) 
    alquilado_imprime = models.CharField(db_column='ALQUILADO_IMPRIME', max_length=1)  # Field name made lowercase.
    datos_ocupante_reparto = models.CharField(db_column='DATOS_OCUPANTE_REPARTO', max_length=1000)  # Field name made lowercase.
    class Meta:
        db_table = 'gg_unidad_consorcio'

class gg_cuota(models.Model):
    id_cuota = models.IntegerField(db_column='ID_CUOTA', primary_key=True) # Field name made lowercase.
    id_unidad = models.ForeignKey('gg_unidad_consorcio', db_column='ID_UNIDAD',db_index=True)
    id_liquidacion = models.IntegerField(db_column='ID_LIQUIDACION', blank=True, null=True) # Field name made lowercase.
    id_propietario = models.ForeignKey('gg_propietario', db_column='ID_PROPIETARIO',db_index=True)
    anio = models.IntegerField(db_column='ANIO', blank=True, null=True) # Field name made lowercase.
    periodo = models.IntegerField(db_column='PERIODO', blank=True, null=True) # Field name made lowercase.
    importe_base = models.DecimalField(db_column='IMPORTE_BASE', max_digits=15, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    importe_base_2 = models.DecimalField(db_column='IMPORTE_BASE_2', max_digits=15, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    importe_base_3 = models.DecimalField(db_column='IMPORTE_BASE_3', max_digits=15, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    fecha_vencim = models.DateField(db_column='FECHA_VENCIM', blank=True, null=True) # Field name made lowercase.
    fecha_vencim_2 = models.DateField(db_column='FECHA_VENCIM_2', blank=True, null=True) # Field name made lowercase.
    fecha_vencim_3 = models.DateField(db_column='FECHA_VENCIM_3', blank=True, null=True) # Field name made lowercase.
    saldo = models.DecimalField(db_column='SALDO', max_digits=15, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    detalle = models.CharField(db_column='DETALLE', max_length=500, blank=True) # Field name made lowercase.
    id_estado = models.IntegerField(db_column='ID_ESTADO',choices=ESTADO_CUOTA,default=1) # Field name made lowercase.
    fecha = models.DateField(db_column='FECHA', blank=True, null=True) # Field name made lowercase.
    usuario = models.CharField(db_column='USUARIO', max_length=10, blank=True) # Field name made lowercase.
    codigo_barra = models.CharField(db_column='CODIGO_BARRA', max_length=100, blank=True) # Field name made lowercase.
    id_tributo = models.IntegerField(db_column='ID_TRIBUTO',choices=TRIBUTO_CUOTA,default=1) # Field name made lowercase.
    id_plan = models.IntegerField(db_column='ID_PLAN', blank=True, null=True) # Field name made lowercase.
    fecha_pago = models.DateField(db_column='FECHA_PAGO', blank=True, null=True)
    id_consorcio = models.ForeignKey('gg_consorcio',db_column='ID_CONSORCIO') # Field name made lowercase.
    judiciales = models.CharField(db_column='JUDICIALES', max_length=1, blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'gg_cuota'

class gg_cuota_detalle(models.Model):
    id_cuota_detalle = models.IntegerField(db_column='ID_CUOTA_DETALLE', primary_key=True) # Field name made lowercase.
    id_cuota = models.ForeignKey('gg_cuota', db_column='ID_CUOTA',db_index=True)
    id_concepto = models.ForeignKey('gg_concepto', db_column='ID_CONCEPTO',db_index=True)
    detalle = models.CharField(db_column='DETALLE', max_length=500, blank=True) # Field name made lowercase.
    importe_base = models.DecimalField(db_column='IMPORTE_BASE', max_digits=15, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    nro_recibo = models.IntegerField(db_column='NRO_RECIBO', blank=True, null=True) # Field name made lowercase.
    fecha = models.DateField(db_column='FECHA', blank=True, null=True) # Field name made lowercase.
    usuario = models.CharField(db_column='USUARIO', max_length=20, blank=True) # Field name made lowercase.
    debito_credito = models.IntegerField(db_column='DEBITO_CREDITO', blank=True, null=True) # Field name made lowercase.
    id_pago = models.IntegerField(db_column='ID_PAGO', blank=True, null=True) # Field name made lowercase.
    orden = models.IntegerField(db_column='ORDEN', blank=True, null=True) # Field name made lowercase.
    class Meta:
        db_table = 'gg_cuota_detalle'

class gg_web_liq(models.Model):
    id_liquidacion = models.AutoField(primary_key=True)
    id_unidad = models.IntegerField()
    tipo = models.IntegerField('Tipo Liquidacion', default=1)
    vencimiento = models.DateField()
    nominal = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=10, decimal_places=2)   
    total = models.DecimalField(max_digits=10, decimal_places=2)   
    pasado_a_cnv = models.IntegerField(default=0)  
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    usuario = models.CharField(max_length=30)
    fecha_punitorios = models.DateField(blank=True, null=True)
    punitorios = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'gg_web_liq'

class gg_web_liq_ctas(models.Model):
    id_liquidacion = models.ForeignKey('gg_web_liq', db_column='id_liquidacion')
    id_cuota =  models.ForeignKey('gg_cuota', db_column='ID_CUOTA',null=True)
    tributo = models.IntegerField()
    nominal = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=10, decimal_places=2)   

    class Meta:
        db_table = 'gg_web_liq_ctas'

# Tabla de configuración de Canchas
class gg_canchas_configuracion(models.Model):
    hora_inicio = models.IntegerField() # Field name made lowercase.
    hora_fin = models.IntegerField() # Field name made lowercase.
    
    class Meta:
        db_table = 'gg_canchas_configuracion'
    
class gg_canchas(models.Model):
    id_cancha = models.IntegerField( primary_key=True) # Field name made lowercase.
    estado = models.IntegerField('Estado',choices=ESTADO,default=0) # Field name made lowercase.
    tipo = models.IntegerField(u'Tipo Cancha',choices=TIPO_CANCHA,default=0) # Field name made lowercase.    
    codigo = models.CharField(u'Código/Denominación',max_length=30, blank=True) # Field name made lowercase.
    hora_inicio = models.TimeField(blank=True, null=True) # Field name made lowercase.
    hora_fin = models.TimeField(blank=True, null=True) # Field name made lowercase.
    
    def __unicode__(self):
        return u'%s' % (self.codigo)

    class Meta:
        db_table = 'gg_canchas' 
        verbose_name = u'Cancha'
        verbose_name_plural = u'Canchas'  
        
   
class gg_canchas_sancion(models.Model):
    id_propietario = models.ForeignKey('gg_propietario',verbose_name='Propietario', db_index=True)
    hasta = models.DateTimeField(u'¿Hasta cuando?',help_text=(u'¿Cuándo termina la sanción?'))
    motivo = models.CharField((u'Razón'), max_length=255, blank=True, null=True,help_text=(u'Breve razón de la sanción.'))

    def __unicode__(self):
        return u'%s - %s - %s' % (self.id_propietario,self.hasta,self.motivo)

    class Meta:
        db_table = 'gg_canchas_sancion'
        verbose_name = u'Sanción'
        verbose_name_plural = u'Sanciones'
    
class gg_canchas_reserva(models.Model):
    id_propietario = models.ForeignKey('gg_propietario',verbose_name='Propietario', db_index=True)
    id_cancha = models.ForeignKey('gg_canchas',verbose_name='Cancha', db_index=True)
    hora_inicio = models.DateTimeField('Desde') # Field name made lowercase.
    hora_fin = models.DateTimeField('Hasta',blank=True, null=True) # Field name made lowercase.
    fecha = models.DateField('Fecha')
    usada = models.BooleanField(u'La Cancha fué utilizada',default=True)

    def __unicode__(self):
        return u'%s - %s (%s - %s)' % (self.id_propietario,self.id_cancha,self.hora_inicio,self.hora_fin)

    class Meta:
        db_table = 'gg_canchas_reserva'
        verbose_name = u'Reserva'
        verbose_name_plural = u'Reservas'

#Tabla de la Base de Configuracion
class gg_configuracion(models.Model):
    id = models.IntegerField(primary_key=True,db_index=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    varios1 = models.CharField(max_length=100, blank=True)    
    punitorios = models.DecimalField(max_digits=15, decimal_places=4)
    tipo_punitorios = models.IntegerField()
    linea1 = models.CharField(max_length=100, blank=True)
    linea2 = models.CharField(max_length=100, blank=True)
    link_retorno = models.CharField(max_length=100, blank=True)
    mantenimiento = models.IntegerField()
    ncuerpo1 = models.CharField(max_length=20, blank=True)
    ncuerpo2 = models.CharField(max_length=20, blank=True)
    ncuerpo3 = models.CharField(max_length=20, blank=True)
    codigo_visible = models.CharField(max_length=1, blank=True)
    diasextravencim = models.IntegerField(db_column='diasExtraVencim', blank=True, null=True) # Field name made lowercase.
    alicuota_unidad = models.CharField(max_length=10, blank=True)
    alicuota_coeficiente = models.DecimalField(max_digits=15, decimal_places=2)
    detalleContrib = models.CharField(max_length=300, blank=True)
    ver_unico_padron = models.CharField(max_length=1, blank=True,default='N')
    liquidacion_web = models.CharField(max_length=1, blank=True,default='S')
    email = models.CharField(max_length=50, blank=True) # Field name made lowercase.
    tipoLogin = models.IntegerField(choices=TIPO_LOGIN,default=0)
    boleta_pie = models.TextField(max_length=5000, blank=True) # Field name made lowercase.
    codPagoElectronico = models.CharField(max_length=1, blank=True,default='N')
    class Meta:
        db_table = 'gg_configuracion'
    
    def __unicode__(self):
        return u'%s' % (self.nombre)

#Tabla de Usuario con datos Extra
class UserProfile(models.Model):
    id_propietario = models.IntegerField(blank=True, null=True)
    tipoUsr = models.IntegerField(choices=TIPOUSR,default=0)
    user = models.OneToOneField(User)

    class Meta:
        db_table = 'user_profile'

    def __unicode__(self):
        return self.user.username

class Sinc(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(db_index=True)
    hora = models.TimeField()
    ultimo_id = models.IntegerField()
    class Meta:
        db_table = 'sinc'

class ArchivosEjecutados(models.Model):
    archivo = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,os.path.join('ejecutado_expensas',settings.MUNI_DIR)),max_length=500)

class ArchivosDoc(models.Model):
    archivo = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,os.path.join('Documentos',settings.MUNI_DIR)),max_length=500)

class ArchivosInformes(models.Model):
    archivo = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,os.path.join('Obras',settings.MUNI_DIR)),max_length=500)


