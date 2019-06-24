# -*- coding: utf-8 -*-

from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.shortcuts import *
from settings import *
from django.core.urlresolvers import reverse
from django.contrib import messages
from boletas.models import gg_configuracion,gg_cuota,gg_tipo_unidad,gg_consorcio,gg_unidad_consorcio
from django.db.models import Q

LOGIN_REDIRECT_URL='/'

def login(request):
    error = None
    LOGIN_REDIRECT_URL='/'

    if request.user.is_authenticated():
      return HttpResponseRedirect(LOGIN_REDIRECT_URL)
   
    barrios = gg_tipo_unidad.objects.filter(baja='N')
    consorcios = gg_consorcio.objects.filter(baja='N')
   
    try:
        sitio = gg_configuracion.objects.get(id=MUNI_ID)
    except gg_configuracion.DoesNotExist:
        sitio = None

    if sitio <> None:
      unico_padr = (sitio.ver_unico_padron == 'S')
      
    if sitio.mantenimiento == 1:
        return render_to_response('mantenimiento.html', {'dirMuni':MUNI_DIR,'sitio':sitio},context_instance=RequestContext(request))

    if request.method == 'POST':        
        if sitio.tipoLogin==1:
          user = authenticate(ndoc=request.POST['ndoc'],password=request.POST['password'])
        elif sitio.tipoLogin==2:
          user = authenticate(codigo=request.POST['codigo'],consorcio=request.POST['consorcio'],password=request.POST['password'])
        else:  
          user = authenticate(lote=request.POST['lote'],manzana=request.POST['manzana'],barrio=request.POST['barrio'], password=request.POST['password'])
        if user is not None:
          if user.is_active:
            django_login(request, user)
            LOGIN_REDIRECT_URL = reverse('padrones_responsable')
            
            if user.userprofile.tipoUsr==0:
                request.session["usuario"] = request.user.username
                if unico_padr:
                  try:
                        padr = gg_unidad_consorcio.objects.filter(codigo__exact=request.POST['codigo'],id_consorcio__id_consorcio=request.POST['consorcio'])[0]
                        request.session["unidad"] = padr.id_unidad
                        LOGIN_REDIRECT_URL = reverse('ver_cuotas', kwargs={'idp':padr.id_unidad})                      
                  except IndexError:
                    padr = None                    
            return HttpResponseRedirect(LOGIN_REDIRECT_URL)
          else:
          ## invalid login
           error = u"Contraseña/Código incorrectos."
        else:
          ## invalid login
           error = u"Contraseña/Código incorrectos."
          #return direct_to_template(request, 'invalid_login.html')
    if error:
      messages.add_message(request, messages.ERROR,u'%s' % (error))    
   
    template = 'index.html'      
            

    return render_to_response(template, {'dirMuni':MUNI_DIR,'sitio':sitio,'barrios':barrios,'consorcios':consorcios},context_instance=RequestContext(request))

def logout(request):
    request.session.clear()
    django_logout(request)
    return HttpResponseRedirect(LOGIN_URL)

def volverHome(request):
    LOGIN_REDIRECT_URL='/'
    if not request.user.is_authenticated():
      return HttpResponseRedirect(LOGIN_URL)
    try:
        LOGIN_REDIRECT_URL = reverse('padrones_responsable')
    except:
      return HttpResponseRedirect(LOGIN_URL)
    return HttpResponseRedirect(LOGIN_REDIRECT_URL)



# def volverHome(request):
#     LOGIN_REDIRECT_URL='/login'
#     if not request.user.is_active:
#       return HttpResponseRedirect(LOGIN_URL)
#     return HttpResponseRedirect(LOGIN_REDIRECT_URL)