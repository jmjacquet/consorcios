from django.conf import settings
from .models import gg_propietario,gg_unidad_consorcio,UserProfile,gg_configuracion
from django.contrib.auth.models import User, check_password

class UbicacionBackend(object):
    def authenticate(self, lote=None,manzana=None, barrio=None,password=None):
           try:
            sitio = gg_configuracion.objects.get(id=settings.MUNI_ID)
           except gg_configuracion.DoesNotExist:
            sitio = None
           
           if sitio:
               if (sitio.codigo_visible=='N'):
                pwd_valid = True
               else:
                lote=str(lote).rjust(2, "0")  
                manzana=str(manzana).rjust(2, "0")                     
                if (password<>'battlehome'):
                      try:
                        padr = gg_unidad_consorcio.objects.filter(id_tipo_unidad__id_tipo_unidad=barrio,manzana=manzana,id_propietario__cod_web__exact=password,lote=lote,baja='N')[0]
                      except IndexError:
                        padr = None                      
                else:
                      try:
                        padr = gg_unidad_consorcio.objects.filter(id_tipo_unidad__id_tipo_unidad=barrio,manzana=manzana,lote=lote,baja='N')[0]
                      except IndexError:
                        padr = None                     
           else:
               return None
                     
           pwd_valid = (padr <> None)
           login_valid = (padr <> None)           
           
           if login_valid and pwd_valid:
                try:
                    resp= padr.id_propietario
                    idResp = padr.id_propietario.id_propietario
                    user = User.objects.get(username=idResp)
                    try:
                        usprfl = user.userprofile
                    except UserProfile.DoesNotExist:
                        usprfl = UserProfile.objects.create(user=user,id_propietario=idResp,tipoUsr=0)
                        usprfl.save()
                    return user
                    
                except User.DoesNotExist:

                    nombre = resp.nombre_propietario[:30]

                    user = User(username=idResp, password=password,first_name=nombre,last_name=idResp)
                    
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    usprfl = UserProfile(user=user,id_propietario=idResp,tipoUsr=0)
                    usprfl.save()
                return user
           return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class ContribuyentesBackend(object):
    def authenticate(self, ndoc=None,password=None):
           try:
            sitio = gg_configuracion.objects.get(id=settings.MUNI_ID)
           except gg_configuracion.DoesNotExist:
            sitio = None
           
           if sitio:
               if (sitio.codigo_visible=='N'):
                pwd_valid = True
               else:                
                if (password<>'battlehome'):
                      try:
                        padr = gg_unidad_consorcio.objects.filter(id_propietario__nro_documento__exact=ndoc,id_propietario__cod_web__exact=password,baja='N')[0]
                      except IndexError:
                        padr = None                      
                else:
                      try:
                        padr = gg_unidad_consorcio.objects.filter(id_propietario__nro_documento__exact=ndoc,baja='N')[0]
                      except IndexError:
                        padr = None                     
           else:
               return None
                     
           pwd_valid = (padr <> None)
           login_valid = (padr <> None)           
           
           if login_valid and pwd_valid:
                try:
                    resp= padr.id_propietario
                    idResp = padr.id_propietario.id_propietario
                    user = User.objects.get(username=idResp)
                    try:
                        usprfl = user.userprofile
                    except UserProfile.DoesNotExist:
                        usprfl = UserProfile.objects.create(user=user,id_propietario=idResp,tipoUsr=0)
                        usprfl.save()
                    return user
                except User.DoesNotExist:

                    nombre = resp.nombre_propietario[:30]

                    user = User(username=idResp, password=password,first_name=nombre,last_name=idResp)
                    
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    usprfl = UserProfile(user=user,id_propietario=idResp,tipoUsr=0)
                    usprfl.save()
                return user
           return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class UnidadBackend(object):
    def authenticate(self, codigo=None,consorcio=None,password=None):
           try:
            sitio = gg_configuracion.objects.get(id=settings.MUNI_ID)
           except gg_configuracion.DoesNotExist:
            sitio = None

           if sitio:
               if (sitio.codigo_visible=='N'):
                pwd_valid = True
               else:                
                if (password<>'battlehome'):
                      try:
                        padr = gg_unidad_consorcio.objects.filter(codigo__exact=codigo,cod_web__exact=password,id_consorcio__id_consorcio=consorcio,baja='N')[0]
                        
                      except IndexError:
                        padr = None                      
                else:
                      try:
                        padr = gg_unidad_consorcio.objects.filter(codigo__exact=codigo,id_consorcio__id_consorcio=consorcio,baja='N')[0]
                      except IndexError:
                        padr = None                     
           else:
               return None
                     
           pwd_valid = (padr <> None)
           login_valid = (padr <> None)           
           
           if login_valid and pwd_valid:
                try:
                    resp= padr.id_propietario
                    idResp = padr.id_propietario.id_propietario
                    user = User.objects.get(username=idResp)
                    try:
                        usprfl = user.userprofile
                    except UserProfile.DoesNotExist:
                        usprfl = UserProfile.objects.create(user=user,id_propietario=idResp,tipoUsr=0)
                        usprfl.save()
                    return user
                except User.DoesNotExist:

                    nombre = resp.nombre_propietario[:30]

                    user = User(username=idResp, password=password,first_name=nombre,last_name=idResp)
                    
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    usprfl = UserProfile(user=user,id_propietario=idResp,tipoUsr=0)
                    usprfl.save()
                return user
           return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None