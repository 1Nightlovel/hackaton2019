from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout, login as auth_login
from django.http import JsonResponse
from .models import Rol,User_comp_data,NumVerification,Estacionamiento,Comuna,Imagen,Calificacion,Arriendo,Auto
from .models import Colors as ColorDB
from django.core import serializers
from django.forms.models import model_to_dict
import requests 
from django.middleware.csrf import get_token
import base64
from django.core.files.base import ContentFile
import unidecode
from datetime import datetime, timezone

#randomstring
from django.utils.crypto import get_random_string
#rest api
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes
from rest_framework import viewsets,generics
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from .serializers import UserSerializer,EstacionamientoSerializer,ComunaSerializer
from django.core import serializers


#SMS

def sendsms(mtext,number):
    print('mensaje : '+mtext+' enviado a: '+number)
    url = 'https://api.connectus.cl/api_v1/send_sms'
    params = dict()
    params['dst_number'] = int('56'+str(number)) #remember int not string
    params['sms_content'] = mtext
    response = requests.post(url, params=params, auth=('1912d7e15a774149840ab47fd210d1aa', 'f60eeb35a49e426ebe2f91eef7671154'))
    print(response.text)

#code generation

def randomstring():
    return get_random_string(length=4, allowed_chars='1234567890')

#username generator function
def usernamegenerate(nom,ape):
    return nom[:3]+str(datetime.now())+ape[:3]+get_random_string(length=2,allowed_chars='PARKING123XYZ')

# Views

#view de envio de sms para inicio de sesion (solo Android, no se ha implementado en web)
@csrf_exempt
def smsconfirm(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    success = False
    reason = ''
    user = authenticate(username=username, password=password)
    user = request.user
    print(user.username)
    if not user:
        return JsonResponse({'success':success,'reason': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    else:
        code = randomstring()
        verify = NumVerification.objects.get(tel=username)
        verify.code = code
        verify.save()
        sendsms('tu codigo para inicio de sesión es: '+code,username)
        success = True
    return JsonResponse({'success':success,'reason':reason})

#view de visualizacion de tarjetas
def credit(request):
    return render(request,'cards.html',{"username":request.user.username})

#inicio de operacion de arriendo
@api_view(['post'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
@permission_classes((IsAuthenticated,))
def startservice(request):
    success = False
    reason = ''
    arriendoID = ''
    user = request.user
    auto = request.POST.get('auto','')
    estacionamiento = request.POST.get('estacionamiento','')
    if(Estacionamiento.objects.filter(id=estacionamiento).exists()):
        e = Estacionamiento.objects.get(id=estacionamiento)
        if(not e.on_use):
            if(Auto.objects.filter(id=auto).exists()):
                car = Auto.objects.get(id=auto)
                if(car.user == user):
                    arr = Arriendo.objects.filter(user = user)
                    if(not arr.filter(end = None).exists()):
                        arriendo = Arriendo(user = user, parking = e, rate = e.user_defined_price, car = car)
                        arriendo.save()
                        success = True
                        e.on_use = True
                        e.save()
                        arriendoID = arriendo.id
                    else:
                        reason = 'already have a parking operation active'
                else:
                    reason = 'is not your car'
            else:
                reason = 'car does not exist'
        else:
            reason = 'parking on use'
    else:
        reason = 'parking does not exist'
    return JsonResponse({'success': success,'reason':reason,'arriendo':arriendoID})

#termino de operacion de arriendo (recibe el id del arriendo)
@api_view(['post'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
@permission_classes((IsAuthenticated,))
def stopservice(request):
    success = False
    reason = ''
    user = request.user
    price = None
    arriendo = request.POST.get('arriendo','')
    if(Arriendo.objects.filter(id=arriendo).exists()):
        ar = Arriendo.objects.get(id=arriendo)
        if(ar.user == user):
            ar.end = datetime.now(timezone.utc)
            ar.save()
            ar.calcprice()
            ar.save()
            ar.parking.on_use = False
            ar.parking.save()
            price = ar.price
            success = True
        else:
            reason = 'is not your operation'
    else:
        reason = 'operation does not exist'
    return JsonResponse({'success':success,'reason':reason,'price':price})

#obtener lista de mis estacionamientos (Android)
@csrf_exempt
@api_view(['post'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
@permission_classes((IsAuthenticated,))
def myparkings(request):
    success = False
    reason = ''
    user = request.user
    est = Estacionamiento.objects.filter(user=user)
    jsonresult = [ob.as_json() for ob in est]
    success = True
    return JsonResponse({'success':success,'reason':reason,'estacionamientos':jsonresult})

#lista de calificaciones y comentarios de un estacionamiento (recibe id del estacionamiento, mobile y web, se debe señalar si es mobile)
@api_view(['post'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
def qualification(request):
    success = False
    reason = ''
    cal = []
    idp = int(request.POST.get('id','')) #id parking
    is_mobile = request.POST.get('is_mobile',False)
    if(idp==''):
        reason = 'no provide data'
    else:
        if(Estacionamiento.objects.filter(id=idp).exists()):
            lista = Calificacion.objects.filter(estacionamiento=Estacionamiento.objects.get(id=idp))
            cal = [ob.as_json() for ob in lista]
            success = True
        else:
            reason = 'does not exist'
    return JsonResponse({'success':success,'reason':reason,'calificaciones':cal})

#view para calificar estacionamiento recibe id de estacinamiento nota y comentario (web y Android)
@api_view(['post'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
@permission_classes((IsAuthenticated,))
def qualify(request):
    success = False
    reason = ''
    idp = int(request.POST.get('id',''))
    nota = int(request.POST.get('nota',''))
    comentario = request.POST.get('comentario','')
    user = request.user
    if(not user.is_anonymous):
        if(Estacionamiento.objects.filter(id=idp).exists()):
            if(nota!='' and (nota<=10 and nota>0)):
                es = Estacionamiento.objects.get(id=idp)
                cal = Calificacion(user=user,nota=nota,comentario=comentario,estacionamiento=es)
                cal.save()
                success = True
                if(Calificacion.objects.filter(estacionamiento=idp).exists()):
                    lista = Calificacion.objects.filter(estacionamiento=idp)
                    suma = 0
                    divisor = 0
                    for nota in lista:
                        suma = suma+int(nota.nota)
                        divisor = divisor+1
                    promedio = float(suma/divisor)
                    es.estrellas = promedio
                    es.save()
            else:
                reason = 'invalid nota'
        else:
            reason = 'parking not exist'
    else:
        reason = 'user anonymous'
    return JsonResponse({'success':success,'reason':reason})

#View para la obtencion de informacion de un estacionamiento recibe el id del estacionamiento y si es un request mobile (web y Android)
@api_view(['post'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
def parkingdetail(request):
    success = False
    reason = ''
    idp = int(request.POST.get('id','')) #id parking
    is_mobile = request.POST.get('is_mobile',False)
    print(idp)
    more = False
    is_owner = False
    allowed_this = False
    myrent = False
    if(idp==''):
        return JsonResponse({'success':success,'reason':"not provide data"})
    else:
        if(Estacionamiento.objects.filter(id=idp).exists()):
            e=Estacionamiento.objects.get(id=idp)
            user = request.user
            if(not user.is_anonymous):
                est = Estacionamiento.objects.filter(user = user)
                if(e in est):
                    is_owner=True
                else:
                    arr = Arriendo.objects.filter(user=user)
                    if((not arr.filter(end=None).exists()) and not e.lock):
                        print('no existen arriendos sin finalizar')
                        allowed_this = not e.on_use
                        print(allowed_this)
                    else:
                        if(arr.filter(end=None).exists()):
                            a = arr.filter(end=None)[0]
                            if(a.parking.id==e.id):
                                allowed_this = True
                                myrent = True
                            print('existen arriendos aun sin finalizar')
            if(Imagen.objects.filter(estacionamiento=e).exists()):
                im=Imagen.objects.filter(estacionamiento=e)
                if(im.count()>1):
                    more = True
            else:
                im=None
            if(is_mobile=='yes'):
                print('solicitud mobile')
                urls = []
                if(im!=None):
                    print('tiene almenos una foto')
                    for foto in im:
                        urls.append('media/'+str(foto.image))
                    success = True
                    reason = 'funciona todo bien'
                else:
                    success = True
                    print('no tiene foto')
                    urls.append('media/sinimagen.png')
                    reason = 'no tiene foto, fuera de eso esta todo funcionando'
                return JsonResponse({'success':success,'reason':reason,'urls':urls,'nombre':e.name,'reputacion':e.estrellas,'descripcion':e.description,'lock':e.lock,'price':e.user_defined_price,'on_use':e.on_use,"is_owner":is_owner,'allowed_this':allowed_this,"myrent":myrent})
            else:  #si no es peticion mobile  
                return render(request,'parkingdetail.html',{"im":im,"more":more,"is_owner":is_owner,'allowed_this':allowed_this,"myrent":myrent,"idest":e.id,'locked':e.lock,'nota':round(e.estrellas*10)})
        else:
            print('no existe el estacionamiento')
            return JsonResponse({'success':success,'reason':"parking does not exist"})

#agregar imagen a estacionamiento (solo propietario)
@api_view(['post'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
@permission_classes((IsAuthenticated,))
def addimageparking(request):
    if(request.method == 'POST'):
        success = False
        reason = ''
        user = request.user
        if(not user.is_anonymous):
            est = Estacionamiento.objects.filter(user=user)
            idp = request.POST.get('id','')
            img = request.FILES.get('img',False)
            print(idp)
            print(img)
            if(idp=='' or img==False):
                reason='please send all data'
            else:
                if(Estacionamiento.objects.filter(id=idp).exists()):
                    e = Estacionamiento.objects.get(id=idp)
                    if(e in est):
                        foto=Imagen(image=img,estacionamiento=e)
                        foto.save()
                        success=True
                        reason='image add to parking: '+str(e.id)+' for user: '+user.username
                    else:
                        reason='not have permissions'
                else:
                    reason= 'id provided does not exist'
        return JsonResponse({'success': success, 'reason':reason})
    else:
        return JsonResponse({'success':False, 'reason': "not allow GET method"})

def reColor(name):
    if(name[:3]=='rgb'):
        return name
    else:
        if(name==''):
            return ColorDB.objects.get(color='default').rgb
        else:
            return ColorDB.objects.get(color=name).rgb
            
def index(request):
    return render(request,"inicio.html",{})

#view de obtencion de token csrf (para uso en android de ser necesario) // en desuso
@csrf_exempt
@api_view(['post'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
@permission_classes((IsAuthenticated,))
def csrfget(request):
    csrf_token = get_token(request)
    user=request.user
    return JsonResponse({'csrf':csrf_token,'tu eres':user.username})

#view de consulta de identidad, para comprobar metodos de autenticacion 
@api_view(['post','get'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
@permission_classes((IsAuthenticated,))
def whoiam(request):
    user=request.user
    return JsonResponse({'tu eres':user.username,'tu sesion es: ': request.session.session_key})

#view de la pagina de la aplicacion
def app(request):
    administrator = False
    user=request.user
    if (user.is_anonymous):
        return render(request,'index.html',{'lastlat':'null','lastlng':'null','maincolor':reColor('default'),'administrator' : administrator})
    else:
        admin = Rol.objects.get(name='is_admin')
        if(user in admin.granted_to.all()):
            administrator = True
        if (user.user_comp_data.lng_last_login ==""):
            lat = 'null'
            lng = 'null'
        else:
            lat = user.user_comp_data.lat_last_login
            lng = user.user_comp_data.lng_last_login
            if(lat == None or lng == None):
                lat = 'null'
                lng = 'null'
        return render(request,'index.html',{'lastlat' :lat ,'lastlng' : lng,'maincolor':reColor(user.user_comp_data.ui_color_1),'administrator' : administrator,'userimage':user.user_comp_data.user_thumb})

#view de la pagina de login web
def loginweb(request):
    user = request.user
    if (user.is_anonymous):
        return render(request,'login.html',{})
    else:
        return redirect("app")

#view de conteo de tiempo de operacion de estacionamiento y previsuaizacion de costo (solo con fines de muestra no es el calculo final del costo)
def parkimetro(request):
    user = request.user
    if (not user.is_anonymous):
        return render(request,'parkimetro.html',{})
    else:
        return JsonResponse({'fail':'not autenticated'})

#view para operacion de logueo
def login_iniciar(request):
    numero = request.POST.get('telefono','')
    verification = NumVerification.objects.get(tel=numero)
    user =  verification.user
    contrasenia = request.POST.get('password','')
    user = authenticate(request,username=user.username,password=contrasenia)

    if user is not None:
        auth_login(request, user)
        request.session['usuario'] = user.first_name+" "+user.last_name
        return redirect("app")
    else:
        return redirect("login")

#view de registro
def register(request):
    user = request.user
    if (user.is_anonymous):
        return render(request,'register.html')
    else:
        return redirect("app")

#operacion de cierre de sesion
@login_required(login_url='login')
def cerrar_sesion(request):
    del request.user
    logout(request)
    return redirect('index')

#view para comprobacion por ajax de existencia previa del email a registrar (actualmente no en uso)
def emailvalidate(request):
	success = False
	if request.method == 'POST':
		correo = request.POST.get('email', None)
		if User.objects.filter(email=correo).exists():
			success = False
		else:
			success = True
	return JsonResponse({'success': success})

#view N°1 para la creacion de un nuevo usuario, se registra el numero de telefono y se envia un codigo de verificación
@csrf_exempt #delete when the auth mixing is finnish
def settel(request):
    success = False
    reason = ''
    if (request.method == 'POST'):
        tel = request.POST.get('tel','')
        code = randomstring()
        if not NumVerification.objects.filter(tel=tel).exists():
            verify = NumVerification(tel=tel,code=code)
            verify.save()
            sendsms("tu codigo de activacion es: "+verify.code,verify.tel)
            success=True
        else:
            verify = NumVerification.objects.get(tel=tel)
            if (verify.success):
                reason='alreadyexist'
            else:
                sendsms("tu codigo de activacion es: "+verify.code,verify.tel)
                success=True

    return JsonResponse({'success':success,'reason':reason})

#view para el reenvio del codigo de activacion
@csrf_exempt
def resend(request):
    success = False
    reason = ''
    if (request.method == 'POST'):
        tel = request.POST.get('tel','')
        if (NumVerification.objects.filter(tel=tel).exists()):
            verify = NumVerification.objects.get(tel=tel)
            if(not verify.success):
                sendsms("tu codigo de activacion es: "+verify.code,verify.tel)
                success=True
            else:
                reason='alreadyvalidate'
        else:
            reason='phoneunregistered'
    return JsonResponse({'success':success,'reason':reason})

#view N°2 para la creacion de un nuevo usuario, se comprueba el codigo enviado por sms y se crea el usuario con datos temporales ( se loguea con el usuario temporal )
@csrf_exempt #delete when the auth mixing is finnish
def comprobar(request):
    success = False
    reason=''
    username=''
    if (request.method == 'POST'):
        apellido = request.POST.get('apellido','')
        nombre = request.POST.get('nombre','')
        tel = request.POST.get('tel','')
        code = request.POST.get('code','')
        if (NumVerification.objects.filter(tel=tel).exists()):
            verify = NumVerification.objects.get(tel=tel)
            print(code)
            print(verify.code)
            if (code == verify.code):
                verify.success = True
                verify.save()
                username = usernamegenerate(nombre,apellido)
                user = User(first_name=nombre,last_name=apellido,username=username)
                user.set_password(verify.code)
                user.save()
                permiso_arrendador = Rol.objects.get(name='is_arrendador')
                permiso_arrendatario = Rol.objects.get(name='is_arrendatario')
                permiso_arrendador.granted_to.add(user)
                permiso_arrendatario.granted_to.add(user)
                permiso_arrendador.save()
                permiso_arrendatario.save()
                verify.user = user
                verify.save()
                userdata = User_comp_data(user=user,username2=(nombre[:2]+'.'+apellido),ui_color_1='default',ui_color_2='default2')
                userdata.save()
                print('usuario: '+userdata.user.username)
                success=True
                user = authenticate(request,username=username,password=verify.code)
                print(user)
                print(username)
                print(verify.code)
                if user is not None:
                    auth_login(request, user)
                    request.session['usuario'] = user.first_name+" "+user.last_name
                else:
                    print('jhbjan')
        else:
            reason ='phoneunregistered'
    print('sending response')
    return JsonResponse({'success':success,'reason':reason})

#view N°3 para la creacion de un nuevo usuario, se reciben los datos finales del usuario y se configuran (al hacerlo se cierra la sesion)
@api_view(['post'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
@permission_classes((IsAuthenticated,))
def crear(request):
    success = False
    reason = ''
    if (request.method == 'POST'):
        username = request.POST.get('username','')
        contrasenia = request.POST.get('contrasenia','')
        correo = request.POST.get('correo','')
        foto = request.FILES.get('foto',False)
        print('valor de foto:')
        print(foto)
        if(not foto):
            print('paso al if')
            fotodata = request.POST.get('foto','')
            foto = ContentFile(base64.b64decode(fotodata),name = username+'.jpg')
            print('termino el if')
        user = request.user
        print(user.username)
        ready = Rol.objects.get(name='is_ready')
        if(user not in ready.granted_to.all()):
            print('seteando datos')
            user.email = correo
            user.is_active = True
            user.user_comp_data.username2=username
            user.user_comp_data.save()
            user.set_password(contrasenia)
            user.save()
            if (foto!=None):
                user.user_comp_data.user_image = foto
                user.user_comp_data.save()
            success =  True
            ready = Rol.objects.get(name='is_ready')
            ready.granted_to.add(user)
            ready.save()
        else:
            reason = 'el usuario ya completo el registro'
    else:
        reason = 'not post request'
    return JsonResponse({'success':success,'reason':reason})

#view administrativa usada para agregar datos georefereciales a cada comuna (aun existe con el fin de acualizar datos de ser necesario)
@csrf_exempt  
def addGeoToComuna(request):
#    comuns = Comuna.objects.all()   #eliminación de acentuación en base de datos
#    for comu in comuns:
#        print(comu)
#        comu.name=unidecode.unidecode(comu.name)
#        print(comu)
#        comu.save()
    success = False
    reason = ""
    if(request.method == 'POST'):
        comuna = ''
        load_to = []
        for g in request.FILES.getlist('geo'):
            comuna = (g.name[:-8]).replace('_',' ')
            print(comuna)
            if(Comuna.objects.filter(name__contains=comuna).exists()):
                comunatarget = Comuna.objects.get(name__contains=comuna)
                comunatarget.geo = g
                comunatarget.save()
                success = True
                load_to.append(comuna)

    return JsonResponse({'success':success,'reason':reason,'load to':load_to})

#view para la creacion de un nuevo estacionamiento (anteriormente administrativa actualmente tambien para el usuario final)
@login_required(login_url='login')
def admincreate(request):
    success=False
    reason=''
    if(request.method == 'POST'):
        user = request.user
        admin = Rol.objects.get(name='is_admin')
        if (user in admin.granted_to.all()):
            title = request.POST.get('title','')
            description = request.POST.get('descripcion','')
            lat = request.POST.get('lat','')
            lng = request.POST.get('lng','')
            price = request.POST.get('precio','')
            calle = request.POST.get('calle','')
            response = requests.post('https://nominatim.openstreetmap.org/reverse.php?format=json&lat='+str(lat)+'&lon='+str(lng))
            print('https://nominatim.openstreetmap.org/reverse.php?format=json&lat='+str(lat)+'&lon='+str(lng))
            geodata = response.json()
            direccion = geodata['address']
            if('city' in direccion):
                com = direccion['city']
            else:
                com = direccion['town']
            print(com)
            com = unidecode.unidecode(com)
            print(com)
            comuna=Comuna.objects.get(name=com)
            estacionamiento = Estacionamiento(user=user, name=title, description=description, lat=lat, lng=lng, user_defined_price=price, calle=calle, comuna=comuna)
            estacionamiento.save()
            success = True
        else:
            reason='you are not administrator'
    else:
        reason= 'is not a POST request'
    return JsonResponse({'success':success, 'reason':reason})


#view de envio de datos de estacionamiento, para la visualizacion en el mapa (web y Android)
@csrf_exempt
def getdataparking(request):
    success=False
    reason=''
    if(request.method == 'POST'):
        estacionamientos = Estacionamiento.objects.all()
        lat = request.POST.get('lat','')
        lng = request.POST.get('lng','')
        print(lat)
        print(lng)
        result=[]
        far=[]
        locked=[]
        for est in estacionamientos:
            if(est.lock):
                locked.append(est)
            else:
                print(((((float(est.lat)-float(lat))**2)+((float(est.lng)-float(lng))**2))**0.5))
                if(((((float(est.lat)-float(lat))**2)+((float(est.lng)-float(lng))**2))**0.5)<=0.00448465347):
                    result.append(est)
                else:
                    far.append(est)

        jsonresult = [ob.as_json() for ob in result]
        jsonresult2 = [ob.as_json() for ob in far]
        jsonresult3 = [ob.as_json() for ob in locked]
        success=True
    else:
        jsonresult = None
    return JsonResponse({'success':success, 'reason':reason, 'result':jsonresult, 'far':jsonresult2,'locked':jsonresult3})

#view para la obtencion de los colores de la interfaz grafica configurados por el usuario (aun no se implementa la funcion para el seteo)
def getcolors(request):
    success = False
    if (request.method == 'POST'):
        user = request.user
        colors=[]
        if (user.is_anonymous):
            colors.append(reColor('default'))
            colors.append(reColor('default2'))
            success = True
        else:
            colors.append(reColor(user.user_comp_data.ui_color_1))
            colors.append(reColor(user.user_comp_data.ui_color_2))
            success = True
        return JsonResponse({'success': success, 'colors':colors})

#view para el envio de los roles del usuario que ha iniciado sesion
def userroles(request):
    success = False
    if (request.method == 'POST'):
        user = request.user
        permisos=[]
        if (user.is_anonymous):
            success = False
        else:
            roles = user.rol_set.all()
            if (user.is_superuser):
                permisos.append('eres superusuario')
            for permiso in roles:
                permisos.append(permiso.name)

            success = True
        return JsonResponse({'success': success,'permisos':permisos})

#view para la recepcion de la ubicacion geografica del usuario al momento del inicio de sesion (aun no implementado en Android)
def userlocation(request):
    success = False
    if request.method == 'POST':
        lat = request.POST.get('lat', None)
        lng = request.POST.get('lng', None)
        user = request.user
        if (user.is_anonymous):
            success = False
        else:
            userdata = user.user_comp_data
            userdata.lat_last_login = lat
            userdata.lng_last_login = lng
            userdata.save()
            success = True
        return JsonResponse({'success': success})

#view que recibe una ubicacion geografica y envia la direccion (cuando esta esa informacion disponible), usa los servicios de openstreetmap
def getgeodata(request):
    success = False
    if (request.method == 'POST'):
        lat = request.POST.get('lat', None)
        lng = request.POST.get('lng', None)
        response = requests.post('https://nominatim.openstreetmap.org/reverse.php?format=json&lat='+str(lat)+'&lon='+str(lng))
        print('https://nominatim.openstreetmap.org/reverse.php?format=json&lat='+str(lat)+'&lon='+str(lng))
        geodata = response.json()
        direccion = geodata['address']
        if('city' in direccion):
            comuna = direccion['city']
        else:
            comuna = direccion['town']
        if('road' in direccion):
            calle = direccion['road']
        else:
            calle = 'Sin informacion'
        if ("house_number" in direccion):
            numero = direccion["house_number"]
        else:
            numero = 'null'
        success = True
        print(numero)
    return JsonResponse({'success': success, 'comuna':comuna, 'calle':calle, 'numero':numero})

#view para el envio de datos de patentes registradas por el usuario
def cars(request):
    return render(request,'cars.html',{"username":request.user.username})

#view para el bloqueo y desbloqueo de un estacionamiento (por parte del dueño), recibe el id y la operacion (op= 'lock' o 'unlock') que se desea
@api_view(['post'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
@permission_classes((IsAuthenticated,))
def lockparking(request):
    reason = ''
    success = False
    user = request.user
    parking = request.POST.get('idp','')
    operation = request.POST.get('op','')
    operation = operation.lower()
    if(operation==''):
        e = Estacionamiento.objects.get(pk=parking)
        return JsonResponse({'lock_status':e.lock})
    if(operation != 'lock' and operation != 'unlock'):
        reason = 'invalid operation'
    else:
        e = Estacionamiento.objects.get(pk=parking)
        est = Estacionamiento.objects.filter(user=user)
        if(not e in est):
            reason = 'is not your parking'
        else:
            if(operation == 'lock'):
                e.lock = True
                e.save()
                success = True
            if(operation == 'unlock'):
                e.lock = False
                e.save()
                success = True
            reason = 'the parking '+str(e.id)+' locked status is: '+str(e.lock)
    
    return JsonResponse({'success':success,'reason':reason})

#API

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class EstacionamientoViewSet(viewsets.ModelViewSet):
    queryset = Estacionamiento.objects.all()
    serializer_class = EstacionamientoSerializer

class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer

#login via token auth
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    success = False
    numero = request.data.get("username")
    password = request.data.get("password")
    code = request.POST.get('code','')
    if(NumVerification.objects.filter(tel=numero)!=None):
        verification = NumVerification.objects.get(tel=numero)
        username =  (verification.user).username
        if(code =='' and verification.code != password):
            return Response({'success':success,'reason': 'Invalid Code'},
                        status=HTTP_400_BAD_REQUEST)
        if(code != verification.code):
            return Response({'success':success,'reason': 'Invalid Code'},
                        status=HTTP_400_BAD_REQUEST)
    else:
        return Response({'success':success,'reason': 'Invalid Credentials'},
                        status=HTTP_400_BAD_REQUEST)
    if username is None or password is None:
        return Response({'success':success,'reason': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'success':success,'reason': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    else:
        usuario = User.objects.get(username=username)
    token, _ = Token.objects.get_or_create(user=user)
    success = True
    return Response({'success':success,'reason':'user logged', 'token': token.key , 'username': user.username,'firstname': user.first_name, 'lastname':user.last_name, 'email':user.email, 'lastlogin':user.last_login},
                    status=HTTP_200_OK)


