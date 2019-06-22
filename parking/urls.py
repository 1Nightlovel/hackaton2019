from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views

from django.conf.urls import url
from .views import login
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'estacionamientos', views.EstacionamientoViewSet)
router.register(r'comunas', views.ComunaViewSet)

urlpatterns = [
    path('',views.index,name='index'),
    path('app',views.app,name='app'),
    path('api/login', login),
    path('api/login/', login),
    path('login/',views.loginweb,name='login'),
    path('register/',views.register,name='register'),
    path('login/iniciar',views.login_iniciar,name="iniciar"),
    path('cerrarsesion/',views.cerrar_sesion,name="cerrar_sesion"),
    path('emailvalidate',views.emailvalidate,name='emailvalidate'),
    path('userlocation',views.userlocation,name='userlocation'),
    path('userroles',views.userroles,name='userroles'),
    path('sendsms',views.sendsms,name='sendsms'),
    path('getcolors',views.getcolors,name='getcolors'),
    path('settel',views.settel,name='settel'),
    path('resend',views.resend,name='resend'),
    path('comprobar',views.comprobar,name='comprobar'),
    path('crear',views.crear,name='crear'),
    path('getgeodata',views.getgeodata,name='getgeodata'),
    path('admincreate',views.admincreate,name='admincreate'),
    path('getdataparking',views.getdataparking,name='getdataparking'),
    path('addGeoToComuna',views.addGeoToComuna,name='addGeoToComuna'), 
    path('csrfget',views.csrfget,name='csrfget'),
    path('whoiam',views.whoiam,name='whoiam'),
    path('credit',views.credit,name='credit'),
    path('parkingdetail',views.parkingdetail,name='parkingdetail'),
    path('addimageparking',views.addimageparking,name='addimageparking'),
    path('smsconfirm',views.smsconfirm,name='smsconfirm'),
    path('myparkings',views.myparkings,name='myparkings'),
    path('qualification',views.qualification,name='qualification'),
    path('qualify',views.qualify,name='qualify'),
    path('startservice',views.startservice,name='startservice'),
    path('stopservice',views.stopservice,name='stopservice'),
    path('parkimetro',views.parkimetro,name='parkimetro'),
    path('cars',views.cars,name='cars'),
    path('lockparking',views.lockparking,name='lockparking'),
    #API
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^', include(router.urls))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)