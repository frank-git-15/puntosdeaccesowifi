from django.db import models

# Create your models here.

#Este es el modelo que usaremos, tiene lo mismo campos que estan en la tabla de la base de datos
#Definimos una funcion __str__ para poder ver el id de cada row por defecto en el admin de django http://127.0.0.1:8000/admin
class PuntoDeAccesoWifi(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    programa = models.CharField(max_length=50)
    fecha_instalacion = models.DateField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    colonia = models.CharField(max_length = 100)
    alcaldia = models.CharField(max_length = 50)

    def __str__(self) -> str:
        return self.id
s

