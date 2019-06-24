# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.conf import settings
import os
from views import *
from django.views.generic import RedirectView,TemplateView
import signals
# Uncomment the next two lines to enable the admin:


urlpatterns = patterns('boletas.views',
	
    # url(r'^estudios/$', EstudiosView.as_view(),name="padrones_estudio"),
    
    url(r'^padrones/$', ResponsablesView.as_view(),name="padrones_responsable"),
    url(r'^cuotas/(?P<idp>[^/]+)/$', BusquedaCuotasView.as_view(),name="ver_cuotas"),
    url(r'^cuotas/(?P<idp>[^/]+)/(?P<anio>\d+)/$', BusquedaCuotasView.as_view(),name="buscarCuotasAP"),
    url(r'^punitorios/(?P<idc>\d+)/$',calcularPunitoriosForm,name="calcularPunitorios"),
    url(r'^punitoriosLiq/(?P<idp>\d+)/$',generarPunitoriosLiq,name="generarPunitoriosLiq"),

    url(r'^imprimir/(?P<idc>\d+)/$',imprimirPDF,name="imprimirPDF"),
    url(r'^imprimirLiqWeb/(?P<id_liquidacion>\d+)/$',imprimirPDFLiqWeb,name="imprimirPDFLiqWeb"),

    # url(r'^boletaTGI/$', TemplateView.as_view(template_name="boletas/boleta_tasas.html")),
    # url(r'^boletaDREI/$', TemplateView.as_view(template_name="boletas/boleta_drei.html")),    
    url(r'^propietario/editar/(?P<pk>\d+)/$', PropietarioUpdateView.as_view(), name='propietario_editar'),
    url(r'^unidad/editar/(?P<pk>\d+)/$', UnidadioUpdateView.as_view(), name='unidad_editar'),
    url(r'^liquidacion/(?P<idp>\d+)/$', generarLiquidacion,name="generarLiquidacion"),
    url(r'^datos/$', DatosView.as_view(),name="datos"),
    # url(r'^administrador/$', AdministradorView.as_view(),name="administrador"),
    url(r'^documentacion/$', DocumentacionView.as_view(),name="documentos"),
    # url(r'^informes/$', InformesView.as_view(),name="informes"),
    url(r'^obras/$', ObrasView.as_view(),name="obras"),
    url(r'^terminos/$', TerminosyCondicView.as_view(),name="terminos"),
    url(r'^canchas/$', ReservaCanchasView.as_view(),name="reserva_canchas"),
    url(r'^canchas/reservar/(?P<cancha>\d+)/(?P<hora>\d+)/$', reservarCancha,name="reservarCancha"),
    url(r'^canchas/cancelar/(?P<cancha>\d+)/(?P<hora>\d+)/$', cancelarCancha,name="cancelarCancha"),

    url(r'^uploads/', upload_fileView.as_view(), name="subirArchivos"),
    url(r'^uploads2/', upload_fileView2.as_view(), name="subirDocumentacion"),
    url(r'^delete/Documentos/'+settings.MUNI_DIR+'/(?P<fileName>[\w.]{0,256})$', delete_file, name="delete_file"),
    url(r'^delete/ejecutado_expensas/'+settings.MUNI_DIR+'/(?P<fileName>[\w.]{0,256})$', delete_file2, name="delete_file2"),    
    url(r'^delete/Obras/'+settings.MUNI_DIR+'/(?P<fileName>[\w.]{0,256})$', delete_file3, name="delete_file3"),
    )