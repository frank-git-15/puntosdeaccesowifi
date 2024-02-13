#En este archivo se define

import graphene
from graphene_django import DjangoObjectType
from apiPuntosWifi.models import PuntoDeAccesoWifi
from django.core.paginator import Paginator

#Aqui se define que datos del modelo se pueden consultar
class PuntoDeAccesoWifiType(DjangoObjectType):
    class Meta:
        model = PuntoDeAccesoWifi
        fields = ("id","programa","fecha_instalacion","colonia","alcaldia")

#el query es el equivalente a un get, 
#cuando se consulte la api en hello retornara la palabra hello
#Cuando se consulte puntosDeAccesoWifi retornara todos lo puntos de acceso
#cuando se consulte puntoDeAcceso se le debera proporcionar el id y que campos quiere retornar
class Query(graphene.ObjectType):
    hello = graphene.String(default_value = "Hello")
    puntosDeAccesoWifi = graphene.List(PuntoDeAccesoWifiType,page=graphene.Int(),page_size=graphene.Int())
    puntoDeAcceso = graphene.Field(PuntoDeAccesoWifiType,id= graphene.String(required=True))
    puntosdeAccesoPorColonia = graphene.List(PuntoDeAccesoWifiType,colonia= graphene.String(required=True),page=graphene.Int(),page_size=graphene.Int())

    def resolve_puntosDeAccesoWifi(self,info,page,page_size):
        #Aqui se realiza la consulta a base de datos para eso usamos el modelo PuntoDeAccesoWifi 
        #que es el modelo de la base de datos, consultamos todos lo objetos
        try:
            queryset = PuntoDeAccesoWifi.objects.all()

            #Paginar los resultados
            #Se dividen los resultados de la consulta en el tamaño de pagina deseada
            paginator = Paginator(queryset,page_size)

            #Se obtiene la pagina deseada
            paginated_query = paginator.get_page(page)


            return paginated_query
        except PuntoDeAccesoWifi.DoesNotExist:
            return []

        return PuntoDeAccesoWifi.objects.all()
    def resolve_puntoDeAcceso(self,info,id):
        try:
            return PuntoDeAccesoWifi.objects.get(id=id)
        except PuntoDeAccesoWifi.DoesNotExist:
            return None
    def resolve_puntosdeAccesoPorColonia(self,info,colonia,page_size,page):
        try:

            queryset = PuntoDeAccesoWifi.objects.filter(colonia=colonia)
            #Paginar los resultados
            #Se dividen los resultados de la consulta en el tamaño de pagina deseada
            paginator = Paginator(queryset,page_size)

            #Se obtiene la pagina deseada
            paginated_query = paginator.get_page(page)

            return paginated_query



        except PuntoDeAccesoWifi.DoesNotExist:
            return []






schema = graphene.Schema(query=Query)