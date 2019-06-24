$(document).ready(function() {  

    $(".filtros a").click(function(){
        var obj = $(this);
        $(obj).closest(".btn-group").find(".btn").text($(obj).text() );
        $(obj).closest(".btn-group").find(".btn").val($(obj).attr("val"))
    });

    $('#menuanio').click(function(){

        var anio = $("#anio").val();
        var idp = $("#idp").val();

        var url = "/cuotas/"+idp+"/"+anio;
        $(location).attr('href',url);
    });
    
    $("#menuidp").click(function(){
      //this will find the selected website from the dropdown
        var anio = $("#anio").val();
        var idp = $("#idp").val();

        var url = "/cuotas/"+idp+"/"+anio;
        $(location).attr('href',url);
   });
   

});

