from django.contrib import admin
from . import models
# Register your models here.

#Registramos nuestro modelo que nuestra tabla en la base de datos al admin de nuestro django
admin.site.register(models.PuntoDeAccesoWifi)

