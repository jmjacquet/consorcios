from django import template
from boletas.models import gg_canchas_reserva,gg_propietario
from datetime import datetime,date,timedelta


register = template.Library()

def buscarReserva(reservas,id_cancha,hi):
    for re in reservas:
        if (re['id_cancha_id'] == id_cancha)and(re['hora_inicio']==hi):
            return re

@register.simple_tag
def estaLibre(reservas,responsable,cancha,hora):
    turno=1
    dia = date.today().day
    mes = datetime.today().month
    anio = datetime.today().year
    hora_reserva=datetime(anio, mes, dia, int(hora))
    
    reserva = buscarReserva(reservas,cancha.id_cancha,hora_reserva)
    
    if reserva:
        #Si es el admin        
        if responsable.id_propietario==0:
            resp= gg_propietario.objects.get(id_propietario=int(reserva['id_propietario_id'])) 
            if reserva['id_propietario_id']==responsable.id_propietario:
                detalle='Reserva Admin'
            else:
                detalle='Reserva Usuario'
               
            nombre='<div class="btn-group "> \
            <button type="button" tipo="ocupada_usr"  class="btn ocupada_usr btn-danger btn_reservas dropdown-toggle btn-xs" data-toggle="dropdown">'+detalle+' <b class="caret"></b></button> \
            <ul class="dropdown-menu-reservas dropdown-menu" role="menu">\
                <li><a href="#">'+resp.nombre_propietario[:30]+'...'+'</a></li>\
                <li  class="cancelarReserva"><a href="#">Cancelar Reserva</a></li>\
            </ul></div>'        
        elif reserva['id_propietario_id']==responsable.id_propietario:
            nombre='<div class="btn-group "> \
            <button type="button" tipo="ocupada_usr"  class="btn ocupada_usr btn-info btn_reservas dropdown-toggle btn-xs" data-toggle="dropdown">Reserva Usuario <b class="caret"></b></button> \
            <ul class="dropdown-menu-reservas dropdown-menu" role="menu">\
                <li  class="cancelarReserva"><a href="#">Cancelar Reserva</a></li>\
            </ul></div>'
        else:
            nombre='<button type="button" tipo="ocupada" class="btn ocupada btn-danger btn_reservas btn-xs">Reservada</button>'        
        return nombre
    else:
        return '<button type="button" tipo="libre" class="btn libre btn-success btn_reservas btn-xs">Disponible</button>'


@register.filter
def totales(listado):
    return sum(d.get('importe_base') for d in listado)