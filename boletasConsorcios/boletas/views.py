# -*- coding: utf-8 -*-
from django.template import RequestContext,Context
from django.shortcuts import *
from .models import *
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,FormView
from django.conf import settings
from django.db.models import Count,Sum
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import connection
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,redirect
from django.contrib import messages
from boletas.utilidades import *
from django import http
import os 
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from datetime import datetime,date,timedelta
from django.utils import timezone
from dateutil.relativedelta import *
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

####################################################
# Funciones que utilizan varios procedimientos
####################################################


def listado_responsables(request):
    try:
        resps = gg_propietario.objects.all()
    except gg_propietario.DoesNotExist:
        raise Http404
    return render_to_response('padrones_representantes.html',{'resps':resps},context_instance=RequestContext(request))

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def padrones_x_responsable(idResp,idPadron=None):
    padrones = gg_unidad_consorcio.objects.filter(id_propietario__pk=idResp,baja='N').order_by('id_propietario__nombre_propietario','codigo')
    if idPadron:
        padrones=padrones.filter(id_unidad=idPadron)
    return padrones

def cuotas_x_padron(idResp,idPadron):
    if idResp is None:
        cuotas = gg_cuota.objects.filter(id_unidad=idPadron)
    else:
        cuotas = gg_cuota.objects.filter(id_unidad=idPadron,id_propietario__pk=idResp)
    return cuotas


def responsable_del_padron(idPadr):
    try:
        resp = gg_unidad_consorcio.objects.filter(id_unidad=idPadr)[0].id_propietario
    except gg_unidad_consorcio.DoesNotExist:
        resp = None

# from django.contrib.auth import authenticate
def puedeVerPadron(request,idPadron):
    usr=request.user
    tipoUsr=request.user.userprofile.tipoUsr

    if tipoUsr==0:
        try:
            idResp = gg_unidad_consorcio.objects.filter(id_unidad=idPadron)[0].id_propietario.id_propietario        
            if not (int(idResp)==int(usr.userprofile.id_propietario)):
                print 'NO TIENE PERMISO!'
                raise http.Http404
        except:
            raise http.Http404    

    else:
        raise http.Http404

def puedeImprimir(request,idc):
    try:
        usr=request.user
        c = gg_cuota.objects.get(id_cuota=idc)                
        return c.saldo > 0.00
    except:
        return False

##############################################
#      Mixin para cargar las Vars de sistema #
##############################################

class VariablesMixin(object):
    def get_context_data(self, **kwargs):
        context = super(VariablesMixin, self).get_context_data(**kwargs)
        context['idMuni'] = settings.MUNI_ID
        context['dirMuni'] = settings.MUNI_DIR
        

        try:
            sinc = Sinc.objects.all().order_by('-fecha','-hora')[0]
        except Sinc.DoesNotExist:
            sinc = None
        try:
            sitio = gg_configuracion.objects.get(id=settings.MUNI_ID)
        except gg_configuracion.DoesNotExist:
            sitio = None

        try:
            idResp= int(self.request.user.userprofile.id_propietario)                
            context['responsable'] = gg_propietario.objects.get(id_propietario=idResp)           
        except:
            context['responsable'] = None
        context['sitio'] = sitio
        context['sinc'] = sinc
        try:            
            unidad = None
            if 'unidad' in self.request.session:
                unidad = self.request.session['unidad']
                context['unidad'] = unidad
        except:
            context['unidad'] = None

        try:            
            consorcio = None
            if 'consorcio' in self.request.session:
                consorcio = self.request.session['consorcio']
                context['consorcio'] = consorcio
        except:
            context['consorcio'] = None

        return context

##########################################
#        Padrones de Responsables        #
##########################################

class ResponsablesView(VariablesMixin,TemplateView):
    template_name = 'padrones_representante.html'
    context_object_name = 'padrones'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResponsablesView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ResponsablesView, self).get_context_data(**kwargs)
        idResp= int(self.request.user.userprofile.id_propietario)
        
        try:            
            unidad = None
            if 'unidad' in self.request.session:
                unidad = self.request.session['unidad']
            p = padrones_x_responsable(idResp,unidad)            
            context['padr'] = p 
            context['padron'] = p[0]
        except gg_propietario.DoesNotExist:
            context['responsable'] = None
        except IndexError:
            context['padr'] = None
            context['padron'] = None
        return context

##########################################
#        Datos Adicionales        #
##########################################

class DatosView(VariablesMixin,TemplateView):
    template_name = 'datos_adicionales.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DatosView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DatosView, self).get_context_data(**kwargs)
        idResp= int(self.request.user.userprofile.id_propietario)
        #file_path = os.path.join(settings.MEDIA_ROOT, 'ejecutado_expensas')
        file_path = os.path.join(settings.MEDIA_ROOT,os.path.join('ejecutado_expensas',settings.MUNI_DIR))
        file_list = [entry for entry in os.listdir(file_path) if os.path.isfile(os.path.join(file_path,entry))]  

        nombres = [os.path.splitext(x)[0] for x in file_list]
        dicc = dict(zip(file_list, nombres))
       
        context['dicc'] = sorted(dicc.iteritems())
       
        return context

class TerminosyCondicView(VariablesMixin,TemplateView):
    template_name = 'terminosCondic.html'

class DocumentacionView(VariablesMixin,TemplateView):
    template_name = 'documentos.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DocumentacionView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DocumentacionView, self).get_context_data(**kwargs)
        idResp= int(self.request.user.userprofile.id_propietario)

        #file_path = os.path.join(settings.MEDIA_ROOT, 'Documentos')
        file_path = os.path.join(settings.MEDIA_ROOT,os.path.join('Documentos',settings.MUNI_DIR))
        file_list = [entry for entry in os.listdir(file_path) if os.path.isfile(os.path.join(file_path,entry))]
        
        nombres = [os.path.splitext(x)[0] for x in file_list]
        dicc = dict(zip(file_list, nombres))
       
        context['dicc'] = sorted(dicc.iteritems())
       
        return context


class InformesView(VariablesMixin,TemplateView):
    template_name = 'informes.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InformesView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InformesView, self).get_context_data(**kwargs)
        idResp= int(self.request.user.userprofile.id_propietario)

        #file_path = os.path.join(settings.MEDIA_ROOT, 'Documentos')
        file_path = os.path.join(settings.MEDIA_ROOT,os.path.join('Informes',settings.MUNI_DIR))
        file_list = [entry for entry in os.listdir(file_path) if os.path.isfile(os.path.join(file_path,entry))]
        
        nombres = [os.path.splitext(x)[0] for x in file_list]
        dicc = dict(zip(file_list, nombres))
       
        context['dicc'] = sorted(dicc.iteritems())
       
        return context

class ObrasView(VariablesMixin,TemplateView):
    template_name = 'obras.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ObrasView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ObrasView, self).get_context_data(**kwargs)
        idResp= int(self.request.user.userprofile.id_propietario)

        #file_path = os.path.join(settings.MEDIA_ROOT, 'Documentos')
        file_path = os.path.join(settings.MEDIA_ROOT,os.path.join('Obras',settings.MUNI_DIR))
        file_list = [entry for entry in os.listdir(file_path) if os.path.isfile(os.path.join(file_path,entry))]
        
        nombres = [os.path.splitext(x)[0] for x in file_list]
        dicc = dict(zip(file_list, nombres))
       
        context['dicc'] = sorted(dicc.iteritems())
       
        return context

##################################################
#      Ver cuotas del Padrón seleccionado        #
##################################################

class BusquedaCuotasView(VariablesMixin,ListView):
    template_name = 'cuotas.html'
    context_object_name = 'cuotas'
 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        idPadron = self.kwargs.get("idp",'0')        
        puedeVerPadron(self.request,idPadron)
        return super(BusquedaCuotasView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        # Tomo el padrón y anio seleccionado y lo filtro para que me muestre las cuotas
        idPadron = self.kwargs.get("idp",'0')
        idResp = int(self.request.user.userprofile.id_propietario)
        
        anio = int(self.kwargs.get("anio",'0'))

        if (anio==0):
            c = cuotas_x_padron(idResp,idPadron).order_by('-fecha_vencim')
        else:
            c = cuotas_x_padron(idResp,idPadron).filter(anio=anio).order_by('-fecha_vencim')
        return c

    def get_context_data(self, **kwargs):
        context = super(BusquedaCuotasView, self).get_context_data(**kwargs)
        # En el contrxto pongo el padrón seleccionado asi saco sus características
        idPadron = self.kwargs.get("idp",'0')        
        idResp = int(self.request.user.userprofile.id_propietario)
        anio = int(self.kwargs.get("anio",'0'))
        context['anio']=anio
        unidad = None
        if 'unidad' in self.request.session:
            unidad = self.request.session['unidad']
        p = padrones_x_responsable(idResp,unidad)        
        context['padr'] = p    
        try:
            p = padrones_x_responsable(idResp,idPadron)[0]                    

        except:
            p = None

        context['padron']=p
        return context

##########################################################################3



def armarCodBar(cod):
    import imprimirPDF
    b  = imprimirPDF.get_image2(cod)
    return b

@login_required
def imprimirPDF(request,idc):   
    
    from Code128 import Code128
    from base64 import b64encode
        
    c = gg_cuota.objects.get(id_cuota=idc)    
    
    puedeVerPadron(request,c.id_unidad.pk)
    if not puedeImprimir(request,idc):
         return HttpResponseRedirect(reverse("padrones_responsable"))

    diasExtra = None
    try:
        sitio = gg_configuracion.objects.get(id=settings.MUNI_ID)
        diasExtra = sitio.diasextravencim

    except gg_configuracion.DoesNotExist:
        sitio = None
        
    if diasExtra == None:
        diasExtra=0

    hoy = date.today()
    
    if (hoy >= c.fecha_vencim):
        vencimiento = hoy + relativedelta(days=diasExtra)   
        vencimiento2 = vencimiento
    else:
        vencimiento = c.fecha_vencim
        if c.fecha_vencim_2==None:
           vencimiento2 = vencimiento + relativedelta(months=1)
        else:
            vencimiento2 = c.fecha_vencim_2   
    
    if sitio.tipoLogin >= 1:
        if (hoy >= vencimiento2):
            vencimiento = hoy + relativedelta(days=diasExtra)   
            vencimiento2 = vencimiento
        elif (hoy > vencimiento):
            vencimiento = vencimiento2
            vencimiento2 = vencimiento2
              
        try:
            conceptos = gg_cuota_detalle.objects.filter(id_cuota__id_liquidacion=c.id_liquidacion,debito_credito__gt=0,id_concepto__id_tipo_concepto=1).values('id_concepto','id_concepto__nombre_concepto').annotate(importe_base=Sum('importe_base')).order_by('id_concepto__nombre_concepto')
            tot_conceptos = gg_cuota_detalle.objects.filter(id_cuota__id_liquidacion=c.id_liquidacion,debito_credito__gt=0,id_concepto__id_tipo_concepto=1).aggregate(importe_base=Sum('importe_base'))['importe_base']
            detalle_cuotas = gg_cuota_detalle.objects.filter(id_cuota__id_liquidacion=c.id_liquidacion,debito_credito__gt=0,id_concepto__id_tipo_concepto=1).values('id_concepto','id_concepto__nombre_concepto','detalle').annotate(importe_base=Sum('importe_base')).order_by('id_concepto__nombre_concepto','detalle')
        except:
            conceptos = None
            tot_conceptos = 0
            detalle_cuotas = None
        template = 'boletas/boleta_tasas2.html'
    else:
        detalle_cuotas = gg_cuota_detalle.objects.filter(id_cuota=idc)
        conceptos = None
        tot_conceptos = 0
        template = 'boletas/boleta_tasas.html'

    context = Context()    
    context['cuota'] = c
    context['idMuni'] = settings.MUNI_ID
    context['dirMuni'] = settings.MUNI_DIR
    context['fecha'] = datetime.now()
    context['vencimiento'] = vencimiento
    context['codseg'] = c.id_propietario.cod_web
    context['sitio'] = sitio
    context['detalle_cuotas'] = detalle_cuotas
    context['codPagoElectronico'] = str(c.id_unidad.id_unidad).rjust(9, "0")
    context['tot_conceptos'] = tot_conceptos

    if ((c.id_unidad.alquilado=='S')and(c.id_unidad.alquilado_imprime=='S')and(c.id_unidad.datos_ocupante_reparto!='')):
        direccion=c.id_unidad.datos_ocupante_reparto
    else:
        direccion=c.id_unidad.domicilio_reparto

    context['direccion'] = direccion
    if ((c.id_unidad.alquilado=='S')and(c.id_unidad.alquilado_imprime=='S')):
        ocupante=c.id_unidad.datos_ocupante
    else:
        ocupante=None

    context['ocupante'] = ocupante


    from easy_pdf.rendering import render_to_pdf_response   

    totales  = calcularPunitorios(request,c,None,0)
    context['vencimiento2'] = vencimiento2  
    context['punit1'] = totales['punit1']
    context['interes1'] = totales['porc1']
    context['punit2'] = totales['punit2']
    context['interes2'] = totales['porc2']

    sAnio=str(c.anio)
    sAnio=sAnio[-2:] #Dos ultimos digitos del anio
    
    cod = ""
    cod += str(sitio.id).rjust(3, "0") #CODIGO DEL MUNICIPIO
    cod += str(c.id_tributo).rjust(1, "0") #TRIBUTO
    cod += str(c.id_unidad.id_unidad).rjust(6, "0") #UNIDAD_CONSORCIO
    cod += sAnio #Anio
    cod += str(c.periodo).rjust(2, "0") #Cuota    
    cod += str(c.id_cuota).rjust(7, "0") #Id Cuota
    cod += str(vencimiento.strftime("%d%m%y")).rjust(6, "0") #Vencimiento
    cod += str(totales['punit1']).replace(".","").rjust(7, "0") #Importe Actualizado
    cod += str(vencimiento2.strftime("%d%m%y")).rjust(6, "0") #Vencimiento2
    cod += str(totales['punit2']).replace(".","").rjust(7, "0") #Importe2 Actualizado
    
    cod += str(digVerificador(cod))
    
    path = 'staticfiles/munis/'+settings.MUNI_DIR+'/'
    
    context['codbar'] = armarCodBar(cod)
    context['codigo'] = cod
    
    return render_to_pdf_response(request, template, context)

##################################################
#      Update de gg_propietario                  #
##################################################
from .forms import PropietarioForm,UnidadForm

class PropietarioUpdateView(VariablesMixin,UpdateView):
    template_name = 'propietario_update.html'
    model = gg_propietario
    success_url = '/padrones/'
    form_class = PropietarioForm

####################################################
class UnidadioUpdateView(VariablesMixin,UpdateView):
    template_name = 'unidad_update.html'
    model = gg_unidad_consorcio
    success_url = '/padrones/'
    form_class = UnidadForm 

####################################################

def calcularPunitorios(request,c,boleta=None,importe=0):
    try:
        cuota = c       
        hoy = date.today()  
        vencimiento = cuota.fecha_vencim

        if cuota.fecha_vencim_2==None:
           vencimiento2 = vencimiento + relativedelta(months=1)
        else:
            vencimiento2 = cuota.fecha_vencim_2           

        fecha = hoy  

  
        if (hoy<=vencimiento):
            fecha=vencimiento                          
        elif ((hoy>vencimiento)and(hoy<=vencimiento2)):
            fecha=vencimiento2
        else:
            fecha=hoy
            vencimiento2=fecha
            
        por1 = punitorios(cuota,vencimiento,fecha)
        por2 = punitorios(cuota,vencimiento,vencimiento2)
        punit1 = cuota.saldo * (1+por1) 
        porc1 = punit1 - cuota.saldo
        punit2 = cuota.saldo * (1+por2)
        porc2 =  punit2 - cuota.saldo       
    except KeyError:
        return HttpResponse('Error') # Error Manejado
    if settings.DEBUG:
        print 'por1:'+str(por1)+' porc1:'+str(porc1)+' punit1:'+str(punit1)+' por2:'+str(por2)+' porc2:'+str(porc2)+' punit2:'+str(punit2)
    return {'punit1': format(punit1, '.2f'), 'porc1': format(porc1, '.2f'),'punit2': format(punit2, '.2f'), 'porc2': format(porc2, '.2f')}

##########################################################################
# Funciones ajax para la liquidacion y cálculo de Punitorios ONLINE

def calcularPunitoriosForm(request,idc):
    try:
        c = gg_cuota.objects.get(id_cuota=idc)
        hoy = date.today() 
        por1 = punitorios(c,c.fecha_vencim,hoy) 
        
    except KeyError:
        return HttpResponse('Error') # Error Manejado
    if request.is_ajax():          
        
        return HttpResponse(str(por1))
    else:
        return HttpResponse('Error') # Error Manejado

def generarPunitoriosLiq(request,idp):   
    if request.is_ajax():         
            datos = request.GET.getlist('cuotas[]')            
            cuotasAct = {}            
            if datos:
                for i in datos:
                    c = gg_cuota.objects.get(id_cuota=i) 
                    total  = calcularPunitorios(request,c,None,0)
                    cuotasAct[i]=total['punit1']
                    
                    # subtotal = subtotal + float(totales['punit1'])
            return HttpResponse(json.dumps(cuotasAct), content_type = "application/json")

def generarLiquidacion(request,idp):   
    if request.is_ajax():         
            padr = cuotas_x_padron(None,idp)[0]
            id_unidad = padr.id_unidad.id_unidad
            datos = request.GET.getlist('cuotas[]')            
            subtotal = 0
            totNom = 0
            totInt = 0
            totales = {}
            if datos:
                for i in datos:
                    c = gg_cuota.objects.get(id_cuota=i)                    
                    total  = calcularPunitorios(request,c,None,0)
                    totales[i]=total                    
                    totInt += float(total['porc1'])
                    totNom += float(total['punit1']) - float(total['porc1'])
                    subtotal += float(total['punit1'])
                # Genero la liquidacion    
                diasExtra = gg_configuracion.objects.get(id=settings.MUNI_ID).diasextravencim
                if diasExtra == None:
                    diasExtra=0
                hoy = date.today() 
                
                venc = hoy + relativedelta(days=diasExtra)   
                liq =gg_web_liq(id_unidad = id_unidad,tipo=1,vencimiento=venc,nominal=totNom,interes = totInt,total = subtotal,\
                    pasado_a_cnv=0,usuario=request.user.username,fecha_punitorios = hoy,punitorios = totInt)
                liq.save()
                for i in datos:
                    c = gg_cuota.objects.get(id_cuota=i)  
                    totNom = float(totales[i]['punit1']) - float(totales[i]['porc1'])
                    totInt = float(totales[i]['porc1'])
                    liq_cta = gg_web_liq_ctas(id_liquidacion = liq,id_cuota=c,tributo=c.id_tributo,nominal=totNom ,interes=totInt)
                    liq_cta.save()
                if liq:                   
                    messages.add_message(request, messages.SUCCESS,u'Se generó la Liquidación Nº %s exitosamente!.'  % (liq.pk))
                
            return HttpResponse(json.dumps(liq.id_liquidacion), content_type = "application/json")

def imprimirPDFLiqWeb(request,id_liquidacion):   
    
    from Code128 import Code128
    from base64 import b64encode
        
    liq = gg_web_liq.objects.get(id_liquidacion=id_liquidacion)    
    liq_ctas = gg_web_liq_ctas.objects.filter(id_liquidacion=id_liquidacion).extra(
                        select = {'total': '(nominal + interes)'},).order_by('-id_cuota')
    
    descrCtas =''                        
    for i in liq_ctas:
        if descrCtas=='':
            descrCtas=(str(i.id_cuota.periodo)+'/'+str(i.id_cuota.anio))
        else:
            descrCtas= descrCtas+' - ' +(str(i.id_cuota.periodo)+'/'+str(i.id_cuota.anio))

    if liq_ctas:
        c = gg_cuota.objects.get(id_cuota=liq_ctas[0].id_cuota.id_cuota)


    diasExtra = None
    try:
        sitio = gg_configuracion.objects.get(id=settings.MUNI_ID)
        diasExtra = sitio.diasextravencim

    except gg_configuracion.DoesNotExist:
        sitio = None
        
    if diasExtra == None:
        diasExtra=0

    hoy = date.today()

    vencimiento = liq.vencimiento
    vencimiento2 = vencimiento
 
    context = Context()    
    context['liq'] = liq
    context['idMuni'] = settings.MUNI_ID
    context['dirMuni'] = settings.MUNI_DIR
    context['vencimiento'] = vencimiento   
    context['sitio'] = sitio
    context['cuota'] = c
    context['descrCtas'] = descrCtas
    
    from easy_pdf.rendering import render_to_pdf_response   
 
    template ='boletas/boleta_liq.html'
    context['liq_ctas'] = liq_ctas
    context['vencimiento2'] = vencimiento2

    cod = ""
    cod += str(sitio.id).rjust(3, "0")#CODIGO DEL MUNICIPIO
    cod += str(9).rjust(1, "0") #Codigo liq web
    #Pongo el 2do vencimiento asi quedan los dos iguales con el importe actualizado
    cod += str(vencimiento.strftime("%d%m%y")).rjust(6, "0") #Vencimiento
    cod += str(liq.total).replace(".","").rjust(7, "0") #Importe Actualizado
    cod += str(vencimiento2.strftime("%d%m%y")).rjust(6, "0") #Vencimiento2
    cod += str(liq.total).replace(".","").rjust(7, "0") #Importe2 Actualizado
    cod += str(liq.id_liquidacion).rjust(9, "0") #Id Liquidacion
    cod += str(liq.fecha.year).rjust(4, "0") #Anio
    cod += str(liq.fecha.month).rjust(2, "0") #Cuota    
    cod += str(digVerificador(cod))
    
    path = 'staticfiles/munis/'+settings.MUNI_DIR+'/'
    
    context['codbar'] = armarCodBar(cod)
    context['codigo'] = cod
    
    return render_to_pdf_response(request, template, context)



##########################################
#        Reserva de Canchas        #
##########################################

def get_horas():
        try:
            config=gg_canchas_configuracion.objects.all()[0]

            inicio = config.hora_inicio
            fin = config.hora_fin
            if not inicio:
                inicio = 9
            if not fin:
                fin = 21
        except:
            inicio = 9
            fin = 21

        horas = {}
        if inicio < fin:
            while inicio < fin:
                horas[inicio] = inicio
                inicio += 1
        return horas

class ReservaCanchasView(VariablesMixin,TemplateView):
    template_name = 'reserva_canchas.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):  
        return super(ReservaCanchasView, self).dispatch(*args, **kwargs)

    # def get_queryset(self):
    #     # Tomo el padrón y anio seleccionado y lo filtro para que me muestre las cuotas
    #     idPadron = self.kwargs.get("idp",'0')
    #     idResp = gg_unidad_consorcio.objects.filter(id_unidad=idPadron)[0].id_propietario.id_propietario
        
    #     anio = int(self.kwargs.get("anio",'0'))

    #     if (anio==0):
    #         c = cuotas_x_padron(idResp,idPadron).order_by('-fecha_vencim')
    #     else:
    #         c = cuotas_x_padron(idResp,idPadron).filter(anio=anio).order_by('-fecha_vencim')
    #     return c

    def get_context_data(self, **kwargs):
        context = super(ReservaCanchasView, self).get_context_data(**kwargs)
        # En el contrxto pongo el padrón seleccionado asi saco sus características
        horas = get_horas()
        canchas_tennis = gg_canchas.objects.filter(estado=0,tipo=0)
        canchas_futbol = gg_canchas.objects.filter(estado=0,tipo=1)
        reservas = gg_canchas_reserva.objects.filter(fecha=date.today()).values()
        fecha = "%(dia)i/%(mes)i/%(anio)i" % { 'dia': datetime.today().day, 'mes': datetime.today().month, 'anio': datetime.today().year }
        context['horas']=horas
        context['fecha']=fecha
        context['reservas']=reservas
        context['canchas_tennis']=canchas_tennis
        context['canchas_futbol']=canchas_futbol
        
        return context

def cancha_libre(request,idResp,cancha,hora):
        turno=1
        dia = date.today().day
        mes = datetime.today().month
        anio = datetime.today().year
        ahora = datetime.today().hour
        
        
        hora_reserva=datetime(anio, mes, dia, int(hora))
        hora_antes=hora_reserva-timedelta(hours=1)
        hora_hoy=datetime(anio, mes, dia, ahora)
        message=''      

        try:            
            cant_lotes_persona = padrones_x_responsable(idResp.id_propietario,None).count()
            #Traigo las reservas de una cancha predeterminada para una hora predeterminada (No puede reservar más de un turno por lote por dia)
            reserva = gg_canchas_reserva.objects.filter(id_cancha=cancha,hora_inicio=hora_reserva,hora_fin=hora_reserva+timedelta(hours=turno),fecha=date.today())
            
            #Traigo las reservas de una persona para una cancha determinada (No puede reservar mas de una cancha por lote por dia)
            reserva_pers = gg_canchas_reserva.objects.filter(id_propietario=idResp,fecha=date.today()).count()

            if reserva:
                message=u'La cancha '+cancha.codigo+' ya se encuentra reservada!!'
                return message  
            
            if request.user.is_staff:
                return message
                
            if reserva_pers >= cant_lotes_persona:
                message=u'No puede reservar más de %s turnos en las Canchas por dia!' % cant_lotes_persona
                return message             
        except Exception, e:            
            print e
            return 'No se pudo realizar la Reserva!'

        
        if request.user.is_staff:
            return message


        if (hora_reserva <= hora_hoy):
            message=u'No puede reservar antes de la hora actual!'
            return message
        
        # elif (hora_antes <= hora_hoy):
        #     message=u'Tiene que reservarse con al menos una hora de anticipación!'
        #     return message

        # Verifico si tiene una sancion y si ya puede o no reservar nuevamente        
        try:
            sanciones = gg_canchas_sancion.objects.filter(id_propietario=idResp,hasta__gte=hora_hoy).order_by('-hasta')[0]
        except:
            sanciones = None
        
        if sanciones:
            message=u'No puede reservar la cancha! (Sanción Pendiente:'+sanciones.motivo+')'
            return message

        if not reserva:
            return ''

        return u'No está libre!!'

def reservarCancha(request,cancha,hora):   
    if request.is_ajax():         
        turno=1
        c = gg_canchas.objects.get(id_cancha=int(cancha))

        if c:            
            idResp= gg_propietario.objects.get(id_propietario=int(request.user.userprofile.id_propietario))
            msj=cancha_libre(request,idResp,c,hora)

            if msj=='':
                dia = date.today().day
                mes = datetime.today().month
                anio = datetime.today().year
                hora_reserva=datetime(anio, mes, dia, int(hora))
                
                reserva =gg_canchas_reserva(id_propietario=idResp,id_cancha=c,hora_inicio=hora_reserva,hora_fin=hora_reserva+timedelta(hours=turno) ,fecha=date.today())
                reserva.save()
                mandarEmailReserva(request,reserva)
                return HttpResponse(json.dumps(''), content_type = "application/json")
            else:
                return HttpResponse(json.dumps(msj), content_type = "application/json")

def cancelarCancha(request,cancha,hora):   
    if request.is_ajax():         
        turno=1
        c = gg_canchas.objects.get(id_cancha=int(cancha))

        if c:            
            idResp= gg_propietario.objects.get(id_propietario=int(request.user.userprofile.id_propietario))
            dia = date.today().day
            mes = datetime.today().month
            anio = datetime.today().year
            ahora = datetime.today().hour
        
            hora_reserva=datetime(anio, mes, dia, int(hora))
            hora_antes=hora_reserva-timedelta(minutes=30)
            hora_hoy=datetime(anio, mes, dia, ahora)
            message=''

            try:
                if request.user.is_staff:
                    reserva = gg_canchas_reserva.objects.filter(id_cancha=c,hora_inicio=hora_reserva,hora_fin=hora_reserva+timedelta(hours=turno),fecha=date.today())[0]
                else:
                    reserva = gg_canchas_reserva.objects.filter(id_propietario=idResp,id_cancha=c,hora_inicio=hora_reserva,hora_fin=hora_reserva+timedelta(hours=turno),fecha=date.today())[0]
            except:
                reserva = None

            if not request.user.is_staff:
                if (hora_hoy >= hora_antes):
                    message=u'Tiene que cancelar con al menos una hora de anticipación!'
            
            if (reserva and (message=='')):                
                reserva.delete()
                return HttpResponse(json.dumps(''), content_type = "application/json")
            else:
                return HttpResponse(json.dumps(message), content_type = "application/json")                

 

def mandarEmailReserva(request,reserva):
    from smtplib import SMTP
    from email.mime.text import MIMEText as text  
    try:
        sitio = gg_configuracion.objects.get(id=settings.MUNI_ID)
        email = sitio.email

    except gg_configuracion.DoesNotExist:
        sitio = None

    if not email:
        email = 'contacto@grupoguadalupe.com.ar'
    to_addr=reserva.id_propietario.email
    if to_addr is None:
        return ''
    if to_addr =='':
        return ''
    cancha = reserva.id_cancha
    from_addr = email
    msg = u'Mail recordatorio de su reserva el día %s.\nCancha: %s - %s .\nTurno: %s hs. a %s hs.\nAnte cualquier inconveniente y/o cancelación comuníquese con Administración.\nAtte. Administración Aires del Llano.' % (reserva.fecha,cancha,cancha.get_tipo_display(),reserva.hora_inicio.hour,reserva.hora_fin.hour)

    m = text(msg.encode('utf-8'))

    m['Subject'] = 'Reserva Canchas (Sistema AutoGestión OnLine)'
    m['From'] = email
    m['To'] = to_addr    
    s = SMTP()
    s.connect('smtp.webfaction.com')
    s.login(str('grupogua_juanmanuel'),str('qwerty'))
    s.sendmail(email, to_addr, m.as_string())
    message="Se envío correctamente el email con la reserva."            
    return message

##################################################################

from .forms import UploadForm,UploadFormGral
from django.utils.text import slugify

class upload_fileView(VariablesMixin,FormView):
    form_class = UploadForm
    success_url = "/"
    template_name = "subirArchivos.html"
 
    def form_valid(self, form):
        archivo = self.request.FILES['archivo']
        destino = self.request.POST['destino']            
        archivo.name = archivo.name.replace(" ", "_").replace("-", "_")                    
        fileName = archivo.name.replace(" ", "_")        
        if destino=='0':        
            newdoc = ArchivosEjecutados(archivo = archivo)
        elif destino=='1':        
            newdoc = ArchivosDoc(archivo = archivo)            
        elif destino=='2':        
            newdoc = ArchivosInformes(archivo = archivo)            
        newdoc.save()
        return super(upload_fileView, self).form_valid(form)

class upload_fileView2(VariablesMixin,FormView):
    form_class = UploadFormGral
    success_url = "/documentacion/"
    template_name = "subirDocumentacion.html"
 
    def form_valid(self, form):
        archivo = self.request.FILES['archivo']        
        fileName = archivo.name
        newdoc = ArchivosDoc(archivo = archivo)            
        newdoc.save()
        return super(upload_fileView2, self).form_valid(form)
# @login_required
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             archivo = request.FILES['archivo']
#             destino = request.POST['destino']            
#             print request.POST
#             print destino
#             print archivo
#             fileName = slugify(archivo.name)
#             if destino=='0':        
#                 newdoc = ArchivosEjecutados(archivo = archivo)
#             else:
#                 newdoc = ArchivosDoc(archivo = archivo)            
#             newdoc.save()
#             return redirect("/datos/")
#     else:
#         form = UploadForm()
#     return render_to_response('subirArchivos.html', {'form': form}, context_instance = RequestContext(request))

@login_required
def delete_file2(request,fileName):
    #file_path = os.path.join(settings.MEDIA_ROOT, 'ejecutado_expensas')
    file_path = os.path.join(settings.MEDIA_ROOT,os.path.join('ejecutado_expensas',settings.MUNI_DIR))
    os.remove(os.path.join(file_path,fileName))
    return redirect("/datos/")

@login_required
def delete_file(request,fileName):
    #file_path = os.path.join(settings.MEDIA_ROOT, 'Documentos')
    file_path = os.path.join(settings.MEDIA_ROOT,os.path.join('Documentos',settings.MUNI_DIR))
    os.remove(os.path.join(file_path,fileName))
    return redirect("/documentacion/")


@login_required
def delete_file3(request,fileName):
    #file_path = os.path.join(settings.MEDIA_ROOT, 'Documentos')
    file_path = os.path.join(settings.MEDIA_ROOT,os.path.join('Obras',settings.MUNI_DIR))
    os.remove(os.path.join(file_path,fileName))
    return redirect("/obras/")