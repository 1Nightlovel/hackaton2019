from django.contrib.auth.models import User
from .models import Estacionamiento,Comuna
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk','url', 'username', 'email', 'is_staff')

class EstacionamientoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model =  Estacionamiento
        fields = ('pk','url','name','user','description','lat','lng','user_defined_price','calle','comuna','on_use','valid')

class ComunaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comuna
        fields = ('pk','url','name')