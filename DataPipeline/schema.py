import graphene
from graphene_django import DjangoObjectType
from apiPuntosWifi.models import PuntoDeAccesoWifi

#Aqui se define que datos del modelo se pueden consultar
class PuntoDeAccesoWifiType(DjangoObjectType):
    class Meta:
        model = PuntoDeAccesoWifi
        fields = ("id","programa","fecha_instalacion","latitud","longitud","colonia","alcaldia")

#el query es el equivalente a un get, 
#cuando se consulte la api en hello retornara la palabra hello
#Cuando se consulte puntosDeAccesoWifi retornara todos lo puntos de acceso
class Query(graphene.ObjectType):
    hello = graphene.String(default_value = "Hello")
    puntosDeAccesoWifi = graphene.List(PuntoDeAccesoWifiType)

    def resolve_puntosDeAccesoWifi(self,info):
        #Aqui se realiza la consulta a base de datos para eso usamos el modelo PuntoDeAccesoWifi 
        #que es el modelo de la base de datos, consultamos todos lo objetos
        return PuntoDeAccesoWifi.objects.all()






schema = graphene.Schema(query=Query)