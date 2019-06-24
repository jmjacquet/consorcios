# -*- coding: utf-8 -*-
from django import forms
from .models import gg_propietario,gg_canchas_sancion,gg_canchas,gg_canchas_reserva,gg_tipo_unidad,gg_configuracion,gg_unidad_consorcio,gg_consorcio

from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
import datetime
from .utilidades import MESES,ANIOS
from django.contrib import admin
from django.conf import settings
from django.forms.widgets import TextInput,NumberInput

class SancionAdmin(admin.ModelAdmin):
    list_display = ('id_propietario','hasta', 'motivo')
    list_display_links = ('id_propietario', )
    search_fields = ['id_propietario']

class CanchaForm(ModelForm):    
    id_cancha = forms.IntegerField(label='Id Cancha',widget=forms.NumberInput(attrs={'readonly':'readonly'})) 
    
    class Meta:
        model = gg_canchas
        fields = ['id_cancha','estado','tipo','codigo','hora_inicio','hora_fin']


class CanchaAdmin(admin.ModelAdmin):
    list_display = ('codigo','tipo','estado')
    list_display_links = ('codigo',)
    search_fields = ['codigo','tipo','estado']
    form = CanchaForm

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id','id_propietario','id_cancha','hora_inicio','hora_fin','usada')
    list_display_links = ('id',)
    search_fields = ['id_propietario','usada']

class PropietarioForm(ModelForm):    
    codigo = forms.CharField(max_length=10,label='Código',widget=forms.TextInput(attrs={'readonly':'readonly'}),required=False) 
    nombre_propietario = forms.CharField(max_length=100,label='Denominación',widget=forms.TextInput(attrs={'size': 100,'readonly':'readonly'}),required=False)     
    telefono = forms.CharField(max_length=50,label='Teléfono',required=False,widget=forms.TextInput(attrs={'size': 100},))     
    cod_web = forms.CharField(widget=forms.PasswordInput(render_value = True),max_length=10,label='Contraseña',required=False) 
    cod_web_confirm = forms.CharField(widget=forms.PasswordInput(render_value = True),max_length=10,label='Confirmar Contraseña',required=False) 
    email = forms.EmailField(max_length=50,label='E-Mail Contacto',required=False) 
    
    def clean(self):
        '''Required custom validation for the form.'''
        super(forms.ModelForm,self).clean()
        if 'cod_web' in self.cleaned_data and 'cod_web_confirm' in self.cleaned_data:
            if self.cleaned_data['cod_web'] != self.cleaned_data['cod_web_confirm']:
                self._errors['cod_web'] = [u'Debe ingresar la misma contraseña.']
                self._errors['cod_web_confirm'] = [u'Debe ingresar la misma contraseña.']
        return self.cleaned_data

    class Meta:
        model = gg_propietario
        fields = ['codigo', 'nombre_propietario', 'telefono','email', 'cod_web','cod_web_confirm']

class UnidadForm(ModelForm):    
    cod_web = forms.CharField(widget=forms.PasswordInput(render_value = True),max_length=10,label='Contraseña',required=False) 
    cod_web_confirm = forms.CharField(widget=forms.PasswordInput(render_value = True),max_length=10,label='Confirmar Contraseña',required=False) 
  
    def clean(self):
        '''Required custom validation for the form.'''
        super(forms.ModelForm,self).clean()
        if 'cod_web' in self.cleaned_data and 'cod_web_confirm' in self.cleaned_data:
            if self.cleaned_data['cod_web'] != self.cleaned_data['cod_web_confirm']:
                self._errors['cod_web'] = [u'Debe ingresar la misma contraseña.']
                self._errors['cod_web_confirm'] = [u'Debe ingresar la misma contraseña.']
        return self.cleaned_data

    class Meta:
        model = gg_unidad_consorcio
        fields = ['cod_web','cod_web_confirm']

try:
    sitio = gg_configuracion.objects.get(id=settings.MUNI_ID)
except gg_configuracion.DoesNotExist:
    sitio = None

class PropietarioAdmin(admin.ModelAdmin):
    form = PropietarioForm
    search_fields = ['nombre_propietario','email']
    ordering = ['nombre_propietario']

if sitio.tipoLogin==1:
    admin.site.register(gg_propietario) 
else:
    admin.site.register(gg_propietario,PropietarioAdmin) 
    admin.site.register(gg_canchas_sancion,SancionAdmin)
    admin.site.register(gg_canchas,CanchaAdmin)
    admin.site.register(gg_canchas_reserva,ReservaAdmin)

admin.site.register(gg_tipo_unidad)


CHOICES = (('0', 'Ejecutado Expensas',), 
            ('1', 'Documentación Extra',),
            ('2', 'Documentación Obras',))

class UploadForm(forms.Form):
      
    destino = forms.ChoiceField(choices=CHOICES,label='Seleccione el Tipo de Archivo')
    archivo = forms.FileField(
        label='Seleccione un archivo'
    )  

class IngresoForm(forms.Form):         
    usuario = forms.IntegerField(max_value=999999999,min_value=0,label='Usuario') 
    password = forms.CharField(max_length=50)
    def clean(self):
        super(forms.Form,self).clean()
        try:
            ndoc=self.cleaned_data['ndoc'] 
        except:
            self._errors['ndoc'] = [u'Debe cargar al menos 6 dígitos del Documento.']
            return self.cleaned_data
        
        if (ndoc<=99999):
                self._errors['ndoc'] = [u'Debe cargar al menos 6 dígitos del Documento.']        

        return self.cleaned_data



class UploadFormGral(forms.Form):    
    archivo = forms.FileField(label='Seleccione un archivo',required=True)  
    def clean(self):
        archivo = self.cleaned_data.get('archivo')
        # 5MB - 5242880
        if archivo:
            if archivo._size > 1048576:            
                self._errors["archivo"] = [u"El archivo no debe superar los 1024KB! (1MB)"]



class UploadFormExpensas(forms.Form):    
    consorcios = forms.ModelChoiceField(queryset=gg_consorcio.objects.filter(baja='N',id_tipo_consorcio__gt=0),label='Seleccione el Consorcio')
    archivo = forms.FileField(label='Seleccione un archivo',required=True)  

    def clean(self):
        archivo = self.cleaned_data.get('archivo')
        # 5MB - 5242880

        if archivo:
            if archivo._size > 1048576:            
                self._errors["archivo"] = [u"El archivo no debe superar los 1024KB! (1MB)"]

       