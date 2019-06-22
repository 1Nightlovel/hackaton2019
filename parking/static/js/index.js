function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
};

var csrftoken = getCookie('csrftoken');

navigator.geolocation.getCurrentPosition(function(location) {
  lat=location.coords.latitude;
  lng=location.coords.longitude;

  var s = false;
  $.ajax({
              type: "POST",
              url: "/userlocation",
              data: {'lat': lat,'lng':lng, 'csrfmiddlewaretoken': csrftoken},
              dataType: "text", async: true,
              success: function(response) {
                  var response = $.parseJSON( response );
                  s = (response.success);}
              
  });
  
});

//document.body.requestFullscreen();
window.scrollTo( 0, 1 );
const list = document.querySelector('.mdc-drawer');

const drawer = new mdc.drawer.MDCDrawer.attachTo(list);

const topAppBarElement = document.querySelector('.mdc-top-app-bar');

const barra = new mdc.topAppBar.MDCTopAppBar.attachTo(topAppBarElement);

const fabRippleel = document.querySelector('.mdc-fab');

const fabRipple = new mdc.ripple.MDCRipple.attachTo(fabRippleel);

const list2 = document.querySelector('#contentdrawer');

const contentdrawer = new mdc.drawer.MDCDrawer.attachTo(list2);

const lockdia = document.getElementById('lockconfirm');

const dialock = new mdc.dialog.MDCDialog.attachTo(lockdia);

//barra.setScrollTarget(document.querySelector('.mapa'));

barra.listen('MDCTopAppBar:nav', () => {
  console.log('menu buton click')
  drawer.open = !drawer.open;
});

const dialogs = document.querySelectorAll('.mdc-dialog');

for (const dialog of dialogs) {
  mdc.dialog.MDCDialog.attachTo(dialog);
}

const snackbarel = document.querySelector('.mdc-snackbar');

const snackbar = new mdc.snackbar.MDCSnackbar.attachTo(snackbarel);

window.onload = function(){
  snackbar.open();
}

var s = false;
var permisos=[];

//var testing....

$.post("/userroles",{'csrfmiddlewaretoken': csrftoken},function(data){
  console.log(data.success);
  console.log(data.permisos);
  permisos = data.permisos;
  s = data.success;
});

var p = 0;

//$.post("/sendsms",{'csrfmiddlewaretoken': csrftoken},function(data){
//  console.log("enviado");
//});


snackbar.listen('MDCSnackbar:closed', _ => {
  if (s){
    if (permisos.length != p){
      snackbar.labelText = permisos[p];
      p = p+1;
      snackbar.open();
    }
  }
});

function openCardsPanel(){
  if(!contentdrawer.open){
    $('#contentdrawer').css('width','300px')
    $('#secondarycontent').load("/credit");
    contentdrawer.open=true;
  }
  else{
    contentdrawer.open=false;
  }
  
}
function openCarsPanel(){
  if(!contentdrawer.open){
    $('#contentdrawer').css('width','300px')
    $('#secondarycontent').load("/cars");
    contentdrawer.open=true;
  }
  else{
    contentdrawer.open=false;
  }
  
}