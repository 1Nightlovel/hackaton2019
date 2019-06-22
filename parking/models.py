from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone
import math
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

def user_directory_path(instance, filename):
    # el archivo sera subido a MEDIA_ROOT/user_<id>/<filename>
    return 'UserImages/user_{0}/{1}'.format(instance.user.id, filename)

def parking_directory_path(instance, filename):
    # el archivo sera subido a MEDIA_ROOT/user_<id>/<filename>
    return 'UserImages/user_{0}/{1}/{2}'.format(instance.estacionamiento.user.id,'estacionamiento'+str(instance.estacionamiento.id), filename)

def imgresize(nw,nh,imagen):
    im = Image.open(imagen)

    width, height = im.size

    output = BytesIO()

    if(width/height < nw/nh): #image height +
        newheight = width*nh/nw
        start = (height - newheight)/2
        im = im.crop((0, start, width, start+newheight))
    
    if(width/height > nw/nh): #image width +
        newwidth = height*nw/nh
        start = (width - newwidth)/2
        im = im.crop((start, 0, start+newwidth, height))
    

    #Resize/modify the image
    im = im.resize( (nw,nh) )

    #after modifications, save it to the output
    im.save(output, format='PNG', quality=100)
    output.seek(0)

    #change the imagefield value to be the newley modifed image value
    return InMemoryUploadedFile(output,'ImageField', "%s.png" % imagen.name.split('.')[0], 'image/png', sys.getsizeof(output), None)

# Create your models here.

class User_comp_data(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username2 = models.CharField(max_length=15 ,null=True)                      #nombre de usuario cambiable
    rut = models.CharField(max_length=9,null=True)
    user_image = models.ImageField(upload_to=user_directory_path)
    user_thumb = models.ImageField(upload_to=user_directory_path)
    lat_last_login = models.FloatField(null=True)                                        #latitud de ubicacion del ultimo login
    lng_last_login = models.FloatField(null=True)                                        #longitud de ubicacion del ultimo login
    ui_color_1 = models.CharField(max_length=23,default='default')
    ui_color_2 = models.CharField(max_length=23,default='default')
    def save(self):
        if(self.user_image!='' and self.user_thumb==''):
            print('en ejecucion el resizado')
            self.user_image = imgresize(800,800,self.user_image)
            self.user_thumb = imgresize(200,200,self.user_image)
        super(User_comp_data,self).save()

class Rol(models.Model):
    name =  models.CharField(max_length=15,null=False)
    granted_to = models.ManyToManyField(User)

class Region(models.Model):
    name = models.CharField(max_length = 30,null = False)

class Ciudad(models.Model):
    name = models.CharField(max_length = 30,null = False)
    region = models.ForeignKey(Region, on_delete = models.CASCADE, null = False)

class Comuna(models.Model):
    name = models.CharField(max_length = 30,null = False)
    ciudad = models.ForeignKey(Ciudad, on_delete = models.CASCADE, null = False)
    geo = models.FileField(upload_to='geo',null = True)
    def __str__(self):
        return self.name

class Estacionamiento(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)             #dueño del estacionamiento
    name = models.CharField(max_length = 30)                              #nombre descriptivo
    description = models.CharField(max_length = 150)                      #descripcion 
    lat = models.FloatField(null = False)                                 #latitud de ubicacion
    lng = models.FloatField(null = False)                                 #longitud de ubicacion
    user_defined_price = models.IntegerField()                          #tarifa definida por usuario
    calle = models.CharField(max_length = 30)
    comuna = models.ForeignKey(Comuna, on_delete = models.CASCADE, null = False)
    on_use = models.BooleanField(null = False ,default = False)
    valid = models.BooleanField(null = False, default = False)
    lock = models.BooleanField(null = False, default = False)
    estrellas = models.FloatField(null=True, default=0) #almacenara el promedio de las calificaciones, sera calculado al momento de ingresar una calificacion, o tal vez luego de validar una calificacion(by admin, por definir)
    def as_json(self):
        return dict(
            id=self.pk, 
            user=self.user.pk,
            name=self.name, 
            description=self.description,
            lat=self.lat,
            lng=self.lng,
            user_defined_price=self.user_defined_price,
            calle=self.calle,
            comuna=self.comuna.name,
            on_use=self.on_use,
            valid=self.valid,
            lock=self.lock,
            calificacion= float(self.estrellas))

class Auto(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)             #dueño del auto
    patente = models.CharField(max_length=30,null=False)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)

class Arriendo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)                   #usuario que arrienda
    parking = models.ForeignKey(Estacionamiento,on_delete=models.CASCADE)     #estacionamiento asociado
    time = models.BigIntegerField(null=True)                                           #tiempo en segundos o minutos (se debe definir)
    start = models.DateTimeField(null=False, default=datetime.now(timezone.utc))                                  #fecha y hora de inicio
    end = models.DateTimeField(null=True)                                              #fecha Y hora de termino
    rate = models.IntegerField()                                              #Tarifa por hora
    price = models.BigIntegerField(null=True)                                          #Precio Final
    car = models.ForeignKey(Auto,on_delete=models.CASCADE)                    #auto que estaciona
    def calcprice(self):
        delta = ((self.end-self.start).total_seconds())/60
        self.time=delta
        if(delta<=30):
            self.price = self.rate
            return self.rate
        if(delta>30):
            dif = delta-30
            fra = dif//10
            self.price = round(self.rate + fra*(self.rate/6))
            return round(self.rate + fra*(self.rate/6))


class Pago(models.Model):
    rent = models.OneToOneField(Arriendo,on_delete=models.CASCADE)      #arriendo asociado

class Imagen(models.Model):
    image = models.ImageField(upload_to=parking_directory_path) #url de imagen
    estacionamiento = models.ForeignKey(Estacionamiento,on_delete=models.CASCADE)

    def save(self):
        self.image = imgresize(1000,600,self.image)
        super(Imagen,self).save()

class TipoTarjeta(models.Model):
    vendor = models.CharField(max_length=25,null=False)

class Tarjeta(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    numero = models.CharField(max_length = 16,null = False)
    ultimos_4_numeros = models.CharField(max_length = 4, null = False)
    fecha_expiracion = models.DateTimeField(null = False)
    codigo_verificacion = models.CharField(max_length = 3, null = False)
    tipo = models.ForeignKey(TipoTarjeta, null = False,on_delete=models.CASCADE) #almacena el tipo de tarjeta, tambien es la clase que identifica el estilo

class NumVerification(models.Model):
    tel = models.CharField(max_length = 8, null = False)
    code = models.CharField(max_length = 4,null = False)
    success = models.BooleanField(default=False,null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)  

class Colors(models.Model):
    color = models.CharField(max_length = 15, null = False)
    rgb = models.CharField(max_length = 15, null = False)

class Calificacion(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    nota = models.IntegerField()
    comentario = models.CharField(max_length = 255, null = True)
    estacionamiento = models.ForeignKey(Estacionamiento, on_delete=models.CASCADE,null=False)
    fecha = models.DateField(default=datetime.now(timezone.utc))
    def as_json(self):
        if(self.user.user_comp_data.user_image != ''):
            image='media/'+str(self.user.user_comp_data.user_thumb)
        else:
            image= 'no foto'
        return dict(
            id = self.pk, 
            user = self.user.first_name+' '+self.user.last_name,
            userimage = image,
            nota = self.nota,
            comentario = self.comentario,
            fecha = self.fecha,
            estacionamiento = self.estacionamiento.pk)
