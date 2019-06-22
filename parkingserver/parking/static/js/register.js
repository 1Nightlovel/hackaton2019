const textfs = document.querySelectorAll('.mdc-text-field')

for (const textf of textfs) {
    mdc.textField.MDCTextField.attachTo(textf);
}


const buttons = document.querySelectorAll('.mdc-button');

for (const button of buttons) {
    mdc.ripple.MDCRipple.attachTo(button);
}

console.log('carga');

function readyshow(cosa){
    if($('#step'+(parseInt(cosa)+2)).hasClass('show')){
        console.log('locked')
    }
    else{
        if(!$('#step'+cosa).hasClass('lock') ){
            $('#step'+cosa).toggleClass('ready');
            $('#step'+cosa).toggleClass('show');
            $('#step'+(parseInt(cosa)+1)).toggleClass('unready');
            $('#step'+(parseInt(cosa)+1)).toggleClass('show');
        }
    }
}

function unreadyshow(cosa){
    if($('#step'+(parseInt(cosa)-2)).hasClass('show')){
        console.log('locked')
    }
    else{
        if(!$('#step'+cosa).hasClass('lock') ){
            $('#step'+cosa).toggleClass('unready');
            $('#step'+cosa).toggleClass('show');
            if(cosa>1){
                $('#step'+(parseInt(cosa)-1)).toggleClass('ready');
                $('#step'+(parseInt(cosa)-1)).toggleClass('show');
            }
    }
    }
}

function step1next(){
    $('#next1').prop('disabled',true);
    if($('#teldat').valid() && $('#nombre').valid() && $('#apellido').valid()){
        var tel = $('#teldat').val();
        var nom = $('#nombre').val();
        var ape = $('#apellido').val();
        if(tel.toString().length==9 && nom!='' && ape!='')
        console.log(tel);
        $.post("/settel",{'csrfmiddlewaretoken': csrftoken,'tel':tel},function(data){
            console.log(data.success);
            console.log(data.reason);
            s = data.success;

            if (tel!=''){
                if (s){
                    readyshow('1');
                    $('#step2').removeClass('lock')
                    $("#teldat").prop('disabled', true);
                    $("#nombre").prop('disabled', true);
                    $("#apellido").prop('disabled', true);
                    $("#cancel1").prop('disabled', true);
                    $("#next1").prop('disabled', true);
                }
                else{
                    alert("ya existe");
                    $('#next1').prop('disabled',false);
                }
            }
            else{
                alert("en blanco")
            }
            
        });
    }
    else{
        alert("verifica los datos")
    }
    
}
function cancel1(){
    if (($('#teldat').val()!='') || ($('#nombre').val()!='') || ($('#apellido').val()!='')){
        $('#teldat').val('');
        $('#nombre').val('');
        $('#apellido').val('');
    }
    else{
        unreadyshow(1);
    }
}
function step2next(){
    $('#next2').prop('disabled',true);
    var tel = $('#teldat').val();
    var code =$('#inco1').val()+$('#inco2').val()+$('#inco3').val()+$('#inco4').val()
    var nom = $('#nombre').val();
    var ape = $('#apellido').val();
    console.log(code);
    if (code.length==4  && nom!='' && ape!=''){
        $.post("/comprobar",{'csrfmiddlewaretoken': csrftoken,'code':code,'tel':tel, 'nombre':nom,'apellido':ape},function(data){
            console.log(data.success);
            s = data.success;
            if (s){
                readyshow('2');
                $('#step3').removeClass('lock')
                $("#next2").prop('disabled', true);
                $("#inco1").prop('disabled', true);
                $("#inco2").prop('disabled', true);
                $("#inco3").prop('disabled', true);
                $("#inco4").prop('disabled', true);
            }
            else{
                alert(data.reason);
                $('#next2').prop('disabled',false);
            }
        });
    }
    else{
        alert('codigo incorrecto');
    }
    console.log(csrftoken);
}

$('#foto').change(function(){    
    //on change event  
    formdatastep3 = new FormData();
    if($(this).prop('files').length > 0)
    {
        file =$(this).prop('files')[0];
        formdatastep3.append('foto', file);
    }
});

function step3next(){
    $('#next3').prop('disabled',true);
    if ($('#username')[0].checkValidity() && $('#correo')[0].checkValidity() && $('#contrasenia')[0].checkValidity() && $('#recontrasenia')[0].checkValidity()){
        var username = $('#username').val();
        var correo = $('#username').val();
        var contrasenia = $('#contrasenia').val();
        formdatastep3.append('csrfmiddlewaretoken', csrftoken);
        formdatastep3.append('username',username);
        formdatastep3.append('correo',correo);
        formdatastep3.append('contrasenia', contrasenia);
        $.post({url: "/crear",processData: false, contentType: false,data: formdatastep3,success:function(data){
            console.log(data.success);
            s = data.success;
            if (s){
                readyshow('3');
                $("#username").prop('disabled', true);
                $("#correo").prop('disabled', true);
                $("#contrasenia").prop('disabled', true);
                $("#recontrasenia").prop('disabled', true);
                $("#foto").prop('disabled', true);
            }
            else{
                alert(data.reason);
                $('#next3').prop('disabled',false);
            }
        }});
    }
    else{
        alert('verifique los datos');
    }
    
    
}

function resend(){
    var tel = $('#teldat').val();
    $.post("/resend",{'csrfmiddlewaretoken': csrftoken,'tel':tel,},function(data){
        console.log(data.success);
        s = data.success;
        if (s){

        }
        else{
            alert(data.reason);
        }
    });
}