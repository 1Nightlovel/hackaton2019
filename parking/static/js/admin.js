
const dialogadminel = document.getElementById('dialogadmin');
const dialogaddel = document.getElementById('dialogadd');

const dialogadmin = new mdc.dialog.MDCDialog.attachTo(dialogadminel);
const dialogadd = new mdc.dialog.MDCDialog.attachTo(dialogaddel);

//

const tfcomunael = document.getElementById('tfcomuna');
const tfcomuna = new  mdc.textField.MDCTextField.attachTo(tfcomunael);

const tfcalleel = document.getElementById('tfcalle');
const tfcalle = new  mdc.textField.MDCTextField.attachTo(tfcalleel);

const tfnumeroel = document.getElementById('tfnumero');
const tfnumero = new  mdc.textField.MDCTextField.attachTo(tfnumeroel);

const tftitleel = document.getElementById('tftitle');
const tftitle = new  mdc.textField.MDCTextField.attachTo(tftitleel);

const tfprecioel = document.getElementById('tfprecio');
const tfprecio = new  mdc.textField.MDCTextField.attachTo(tfprecioel);

const tfdescripcionel = document.getElementById('tfdescripcion');
const tfdescripcion = new  mdc.textField.MDCTextField.attachTo(tfdescripcionel);

function openAdminPanel(){
    dialogadmin.open();
}
function openAdminAddPanel(){
    $.post("/getgeodata",{'csrfmiddlewaretoken': csrftoken,'lat':lat,'lng':lng},function(data){
        console.log(data.success);
        console.log(data.reason);
        s = data.success;
        if(s){

            $('#comuna').val(data.comuna);
            $('#tflabelcomuna').addClass('mdc-floating-label--float-above');
            $("#comuna").prop('disabled', true);    
            $('#calle').val(data.calle);
            $('#tflabelcalle').addClass('mdc-floating-label--float-above');

            if(data.numero!='null'){
                $('#numero').val(data.numero);
                $('#tflabelnumero').addClass('mdc-floating-label--float-above');
            }
            else{
                $('#numero').val('');
                $('#tflabelnumero').removeClass('mdc-floating-label--float-above');
            }
            dialogadd.open();
        }        
    });
    
}

const buttons = document.querySelectorAll('.mdc-button');

for (const button of buttons) {
    mdc.ripple.MDCRipple.attachTo(button);
}

function  createform(){
    formdata= new FormData();
    formdata.append('csrfmiddlewaretoken', csrftoken);
    formdata.append('lat', lat);
    formdata.append('lng', lng);
    formdata.append('title', $('#title').val());
    formdata.append('calle', $('#calle').val());
    formdata.append('numero', $('#cnumero').val());
    formdata.append('precio', $('#precio').val());
    formdata.append('descripcion', $('#descripcion').val());
    return formdata;
}

function adminAddParking(){
    datatosend=createform()
    $.post({url:"/admincreate",processData: false, contentType: false,data:datatosend,success:function(data){
        console.log(data.success);
        console.log(data.reason);
        s = data.success;
        if(s){
            alert('creado')
        }        
    }});
    
}