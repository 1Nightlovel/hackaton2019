
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
  };

var csrftoken = getCookie('csrftoken');

$.validator.addMethod("minAge", function(value, element, min) {
    var today = new Date();
    var birthDate = new Date(value);
    var age = today.getFullYear() - birthDate.getFullYear();
 
    if (age > min+1) {
        return true;
    }
 
    var m = today.getMonth() - birthDate.getMonth();
 
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
 
    return age >= min;
},"mensaje");

function formatrut(rut){
    var valor = rut.value.replace('.','');
    valor = valor.replace('-','');
    cuerpo = valor.slice(0,-1);
    dv = valor.slice(-1).toUpperCase();
    rut.value = cuerpo + '-'+ dv
     
}

function checkRut(rut) {
    rut = String(rut);
    var valor = rut.replace(".", "").replace(".", "");
    valor = valor.replace("-", "");
    cuerpo = valor.slice(0, -1);
    dv = valor.slice(-1).toUpperCase();
    rut = cuerpo + "-" + dv;
    if (cuerpo.length < 7) {
      return false;
    }
    suma = 0;
    multiplo = 2;
    for (i = 1; i <= cuerpo.length; i++) {
      index = multiplo * valor.charAt(cuerpo.length - i);
      suma = suma + index;
      if (multiplo < 7) {
        multiplo = multiplo + 1;
      } else {
        multiplo = 2;
      }
    }
    dvEsperado = 11 - suma % 11;
    dv = dv == "K" ? 10 : dv;
    dv = dv == 0 ? 11 : dv;
    if (dvEsperado != dv) {
      return false;
    }
    return true;
}

$.validator.addMethod("validRut", function(value, element) {
    if (value){
        element.setCustomValidity('fail');
    }
    else{
        element.setCustomValidity('');
    }
    return checkRut(value);
}, );

$.validator.addMethod('user_exist',function(value,element){
    console.log('valor: '+consultarusername(value));
    return consultarusername(value);
},);

function consultarusername(value){
    var s = false;
    $.ajax({
                type: "POST",
                url: "/uservalidate",
                data: {'username': value, 'csrfmiddlewaretoken': csrftoken},
                dataType: "text", async: true,
                success: function(response) {
                    var response = $.parseJSON( response );
                    s = (response.success);}
    });
    return s;
}

function veerifyusername(element){
    console.log("activate")
    var s = true;
    $.ajax({
                type: "POST",
                url: "/uservalidate",
                data: {'username': value, 'csrfmiddlewaretoken': csrftoken},
                dataType: "text", async: true,
                success: function(response) {
                    var response = $.parseJSON( response );
                    s = (response.success);}
                
    });
    if (s) {
        element.setCustomValidity('');
    }
    else{
        element.setCustomValidity('fail');
    }
}

function verifyusername(element){
    console.log("test");
    element.setCustomValidity('');
}

//esta funciona

$.validator.addMethod('rut_exist',function(value,element){
    console.log('valor: '+consultarrut(value));
    if (value){
        element.setCustomValidity('fail');
    }
    else{
        element.setCustomValidity('');
    }
    
    return consultarrut(value);
},);

function consultarrut(value){
    var s = false;
    $.ajax({
                type: "POST",
                url: "/rutvalidate",
                data: {'rut': value, 'csrfmiddlewaretoken': csrftoken},
                dataType: "text", async: false,
                success: function(response) {
                    var response = $.parseJSON( response );
                    s = (response.success);}
                
    });
    return s;
}

$.validator.addMethod('email_exist',function(value,element){
    console.log('valor: '+consultarrut(value));
    return consultaremail(value);
},);


function consultaremail(value){
    csrftoken = getCookie('csrftoken');
    var s = false;
    $.ajax({
                type: "POST",
                url: "/emailvalidate",
                data: {'email': value, 'csrfmiddlewaretoken': csrftoken},
                dataType: "text", async: false,
                success: function(response) {
                    var response = $.parseJSON( response );
                    s = (response.success);}
                
    });
    return s;
}

$("#formaregistro").validate({
    errorClass:"error",
    highlight: function (element, errorClass, validClass) {
        $(element.form).find("label[for=" + element.id + "]")
        .addClass(errorClass);
    },
    unhighlight: function (element, errorClass, validClass) {
        $(element.form).find("label[for=" + element.id + "]")
        .removeClass(errorClass);
    },
    rules: {
        username:{
            required:true,
            user_exist:true,
 
        },
        correo:{
            required: true,
            email:true,
            email_exist:true
        },
        recorreo:{
            required: true,
            equalTo: "#correo",
        },
        nombre: {
            required:true,
            minlength:4,
            maxlength:20
        },
        apellido: {
            required:true,
            minlength:4,
            maxlength:20
        },
        apellidom: {
            required:true,
            minlength:4,
            maxlength:20
        },
        fnac:{
            required:true,
            minAge:18,
        },
        tel:{
            required:true,
            minlength:4,
            maxlength:20
        },
       
       region:{
           required:true,
       },
       comuna:{
           required:true,
       },
       rut:{
           required:true,
           validRut: true,
           rut_exist:true,
       },
       vivienda:{
           required:true
       },
       foto:{
           required:true
       },
       contrasenia:{
           required:true,
           minlength:8,
            maxlength:20
       },
       recontrasenia:{
            required:true,
            equalTo:'#contrasenia'
       },
       
            
    },
    messages: {
        username:{
            required:'Ingrese nombre de usuario',
            user_exist:'usuario ya existe'
            
        },
        correo:{
            required:"Se requiere un correo",
            email:"Correo invalido",
            email_exist:"El correo ya esta registrado",
        },
        recorreo:{
            required: "Repita su email",
            equalTo: "No coincide",
            email:"Correo invalido"
        },
        nombre:{
            required:"Se requiere un nombre",
            minlength:"Se requiere al menos {0} caracteres ",
            maxlength:"Demaciados caracteres"
        },
        apellido:{
            required:"Se requiere su apellido",
            minlength:"Se requiere al menos {0} caracteres ",
            maxlength:"Demaciados caracteres"
        },
        apellidom:{
            required:"Se requiere su apellido",
            minlength:"Se requiere al menos {0} caracteres ",
            maxlength:"Demaciados caracteres"
        },
        region:{
            required:"Se requiere una region"
        },
        comuna:{
            required:"Se requiere una comuna"
        },
        rut:{
            required:"Se requiere su rut",
            validRut:"Rut no valido",
            rut_exist:"El rut ya esta registrado",
        },
        vivienda:{
            required:"Por favor indique su tipo de vivienda"
        },
        fnac:{
            required:"Por favor indique su fecha de nacimiento",
            minAge:"Debes ser mayor de edad"
        },
        tel:{
            required:"Por favor ingrese su telefono",
            minlength:"Se requieren 9 digitos",
            maxlength:"Se requieren 9 digitos"
        },
        foto:{
            required:"Agregue su foto"
        },
        contrasenia:{
            required:"Introduzca contraseña",
            minlength:"Minimo 8 caracteres",
            maxlength:"Maximo 20 caracteres"
        },
        recontrasenia:{
             required:'Repita contraseña',
             equalTo:'No coincide'
        },
    }      
});

$("#formanumero").validate({
    errorClass:"error",
    highlight: function (element, errorClass, validClass) {
        $(element.form).find("label[for=" + element.id + "]")
        .addClass(errorClass);
        element.setCustomValidity('fail');
    },
    unhighlight: function (element, errorClass, validClass) {
        $(element.form).find("label[for=" + element.id + "]")
        .removeClass(errorClass);
        element.setCustomValidity('');
    },
    rules: {
        nombre: {
            required:true,
            minlength:3,
            maxlength:20
        },
        apellido: {
            required:true,
            minlength:3,
            maxlength:20
        },
        tel:{
            required:true,
            minlength:9,
            maxlength:9
        }
    },
       
    messages: {
        nombre:{
            required:"Se requiere un nombre",
            minlength:"Se requiere al menos {0} caracteres ",
            maxlength:"Demaciados caracteres"
        },
        apellido:{
            required:"Se requiere su apellido",
            minlength:"Se requiere al menos {0} caracteres ",
            maxlength:"Demaciados caracteres"
        },
        tel:{
            required:"Por favor ingrese su telefono",
            minlength:"Se requieren 9 digitos",
            maxlength:"Se requieren 9 digitos"
        },
    }      
});

$("#formaedit").validate({
    errorClass:"error",
    highlight: function (element, errorClass, validClass) {
        $(element.form).find("label[for=" + element.id + "]")
        .addClass(errorClass);
        element.setCustomValidity('fail');
    },
    unhighlight: function (element, errorClass, validClass) {
        $(element.form).find("label[for=" + element.id + "]")
        .removeClass(errorClass);
        element.setCustomValidity('');
    },
    rules: {
        username:{
            required:true,
            minlength:8,
            maxlength:20
        },
        correo:{
            required: true,
            email:true,
            email_exist:true
        },
        foto:{
            required:true
        },
       contrasenia:{
           required:true,
           minlength:8,
            maxlength:20
       },
       recontrasenia:{
            required:true,
            equalTo:'#contrasenia'
       },
       
            
    },
    messages: {
        username:{
            required:'Ingrese nombre de usuario',
            minlength:"Minimo 8 caracteres",
            maxlength:"Maximo 20 caracteres"
        },
        correo:{
            required:"Se requiere un correo",
            email:"Correo invalido",
            email_exist:"El correo ya esta registrado",
        },
        foto:{
            required:"Agregue su foto"
        },
        contrasenia:{
            required:"Introduzca contraseña",
            minlength:"Minimo 8 caracteres",
            maxlength:"Maximo 20 caracteres"
        },
        recontrasenia:{
             required:'Repita contraseña',
             equalTo:'No coincide'
        },
    }      
});

/*
$("#nombre").keypress(function(event){
    var inputValue = event.which;
    if(!(inputValue >= 65 && inputValue <= 120) && (inputValue != 32 && inputValue != 0)) { 
        event.preventDefault(); 
    }
});
*/

$("#nombre").keypress(function(event){
    var inputValue = event.which;
    if(!(inputValue >= 65 && inputValue <= 90)  && !(inputValue >= 97 && inputValue <= 122) && (inputValue != 32 && inputValue != 0) && inputValue != 209 && inputValue != 241) { 
        event.preventDefault(); 
    }
});

$("#apellido").keypress(function(event){
    var inputValue = event.which;
    if(!(inputValue >= 65 && inputValue <= 90)  && !(inputValue >= 97 && inputValue <= 122) && (inputValue != 32 && inputValue != 0) && inputValue != 209 && inputValue != 241) { 
        event.preventDefault(); 
    }
});

$("#teldat").keypress(function(event){
    var inputValue = event.which;
    if(!(inputValue >= 48 && inputValue <= 57)  && inputValue != 0) { 
        event.preventDefault(); 
    }
});

$(function(){

    regiones.regiones.forEach(region => {
        $("#region").append('<option value="'+region.region+'">'+region.region+'</option>')
    });
    console.log('region ready');
})

$(".codeinput").keydown(function(event){
    var inputValue = event.which;
    console.log(inputValue);
    if(!(inputValue >= 48 && inputValue <= 57)  && inputValue != 0) { 
        event.preventDefault(); 
    }
});

$('.codeinput').on('keyup', function(event) {
    var inputValue = event.which;
    if (inputValue==8){
        $(this).val('');
        $(this).prev().focus();
    }
    if(inputValue==46){
        $(this).val('');
    }
    if(inputValue==37){
        $(this).prev().focus();
    }
    if(inputValue==39){
        $(this).next().focus();
    }
    if ($(this).val()) {
        $(this).next().focus();
    }


    
});