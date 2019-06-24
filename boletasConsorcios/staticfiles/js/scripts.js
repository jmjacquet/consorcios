$(document).ready(function(){           
// alertify.defaults.transition = "slide";
alertify.defaults.theme.ok = "btn btn-primary";
alertify.defaults.theme.cancel = "btn btn-default";
alertify.defaults.theme.input = "form-control";

$("#email").click(function(){
      var $cod = $("input[name='codigo']").val();
      var $con = $("input[name='consorcio']").val();
      if ($usr == '')
              {alertify.alert('Recuperar Contraseña','Verifique que haya cargado correctamente el campo Código en el formulario.');}
      else{  
      $.ajax({
          url: "/mandarEmailPasswd/"+$usr,
          type: "get", // or "get"       
          success: function(data) {
                alertify.alert('Recuperar Contraseña',data);
        }});}    
     });


var btn_reservas = document.querySelectorAll('button.libre');
var closable = alertify.dialog('confirm').setting('closable');
            //grab the dialog instance and set multiple settings at once.

for (var i = 0; i < btn_reservas.length; i++) {
  btn_reservas[i].addEventListener('click', function(event) {
      event.preventDefault();      
      var cancha = $(this).closest('td').attr('cancha');
      var hora = $(this).closest('tr').attr('hora');  

      alerta= alertify.dialog('confirm')
          .set({
            'labels':{ok:'Reservar', cancel:'Cancelar'},
            'message': '¿Desea Reservar la Cancha '+cancha+' para las '+hora+':00 hs.?' ,
            transition:'fade',
            'onok': function(){ 
              
              $.ajax({
                url: "/canchas/reservar/"+cancha+"/"+hora,
                type: "get",
                dataType: 'json',
                success: function(data) {
                  alertify.set('notifier','position', 'top-right');
                  
                  if (data.length == 0)
                  {             
                   alerta2=alertify.dialog('confirm').set({
                    'labels':{ok:'Aceptar', cancel:'Cancelar'},
                    'message': 'Se reservó la Cancha '+cancha+' para las '+hora+':00 hs.! (Se envió un e-mail con la confirmación de la misma).' ,
                    transition:'fade',
                    'onok': function(){ location.reload();}});
                    alerta2.setting('modal', true);
                    alerta2.setHeader('Reserva de Canchas');
                    alerta2.show();                    
                  }
                  else
                  {
                    alerta3=alertify.dialog('confirm').set({
                    'labels':{ok:'Aceptar', cancel:'Cancelar'},
                    'message': data ,
                    transition:'fade',
                    'onok': function(){ location.reload();}});
                    alerta3.setting('modal', true);
                    alerta3.setHeader('Reserva de Canchas');
                    alerta3.show();                       
                  };
                   
                   
                   }});            

            },
            'oncancel': function(data){ 
               
            }
          });
          alerta.setting('modal', true);
          alerta.setHeader('Reserva de Canchas');
          alerta.show();
  });
};

var btn_reservados = document.querySelectorAll('.cancelarReserva');
for (var i = 0; i < btn_reservados.length; i++) {
  btn_reservados[i].addEventListener('click', function(event) {
      event.preventDefault();      
      var cancha = $(this).closest('td').attr('cancha');
      var hora = $(this).closest('tr').attr('hora');  

      alerta= alertify.dialog('confirm')
          .set({
            'labels':{ok:'Aceptar', cancel:'Cancelar'},
            'message': '¿Desea Cancelar la reserva de la Cancha '+cancha+' para las '+hora+':00 hs.?' ,
            transition:'fade',
            'onok': function(){ 
              
              $.ajax({
                url: "/canchas/cancelar/"+cancha+"/"+hora,
                type: "get",
                dataType: 'json',
                success: function(data) {
                  alertify.set('notifier','position', 'top-right');
                  if (data.length == 0)
                  {             
                   alerta2=alertify.dialog('confirm').set({
                    'labels':{ok:'Aceptar', cancel:'Cancelar'},
                    'message': 'Se canceló la Reserva de la Cancha '+cancha+' para las '+hora+':00 hs.!' ,
                    transition:'fade',
                    'onok': function(){ location.reload();}});
                    alerta2.setting('modal', true);
                    alerta2.setHeader('Cancelar Reserva de Canchas');
                    alerta2.show();                    
                  }
                  else
                  {
                    alerta3=alertify.dialog('confirm').set({
                    'labels':{ok:'Aceptar', cancel:'Cancelar'},
                    'message': data ,
                    transition:'fade',
                    'onok': function(){ location.reload();}});
                    alerta3.setting('modal', true);
                    alerta3.setHeader('Cancelar Reserva de Canchas');
                    alerta3.show();                       
                  };                  
                   
                   }});            

            },
            'oncancel': function(data){ 
               
            }
          });
          alerta.setting('modal', true);
          alerta.setHeader('Cancelar Reserva de Canchas');
          alerta.show();
  });
};

    
});

