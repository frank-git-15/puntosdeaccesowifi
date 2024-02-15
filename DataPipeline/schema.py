#En este archivo se define

import graphene
from graphene_django import DjangoObjectType
from apiPuntosWifi.models import PuntoDeAccesoWifi
from math import radians, sin, cos, sqrt, atan2

#Se importta el modulos Paginator que no ayuda a paginar los resultados
from django.core.paginator import Paginator
from django.db.models import F, FloatField, ExpressionWrapper, Func

from django.db import models



#from django.contrib.gis.db.models.functions import Distance


from django.db.models import Func, F, FloatField
from django.db.models.expressions import RawSQL

class Haversine(Func):
    function = 'HAVING'
    output_field = FloatField()

#Aqui se define que datos del modelo se pueden consultar
class PuntoDeAccesoWifiType(DjangoObjectType):
    class Meta:
        model = PuntoDeAccesoWifi
        fields = ("id","programa","fecha_instalacion","latitud","longitud","colonia","alcaldia","distancia")

#el query es el equivalente a un get, 
#cuando se consulte la api en hello retornara la palabra hello
#Cuando se consulte puntosDeAccesoWifi retornara todos lo puntos de acceso
#cuando se consulte puntoDeAcceso se le debera proporcionar el id y que campos quiere retornar
class Query(graphene.ObjectType):
    hello = graphene.String(default_value = "Hello")
    puntosDeAccesoWifi = graphene.List(PuntoDeAccesoWifiType,page=graphene.Int(),page_size=graphene.Int())
    puntoDeAcceso = graphene.Field(PuntoDeAccesoWifiType,id= graphene.String(required=True))
    puntosdeAccesoPorColonia = graphene.List(PuntoDeAccesoWifiType,colonia= graphene.String(required=True),page=graphene.Int(),page_size=graphene.Int())
    # puntosDeAccesoMasCercanos = graphene.List(PuntoDeAccesoWifiType,latitud = graphene.Float(required=True),longitud = graphene.Float(required=True),page=graphene.Int(),page_size=graphene.Int())
    puntosDeAccesoMasCercanos = graphene.List(PuntoDeAccesoWifiType,latitud = graphene.Float(required=True),longitud = graphene.Float(required=True),page=graphene.Int(),page_size=graphene.Int())
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
    def resolve_puntosdeAccesoPorColonia(self,info,colonia,page,page_size):
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
        


    """
    Para el calculo de la distancia se uso la formula harversine
    R = 6371 Radio de la tierra en kilomentros
    a = sin**2((latitud1Radianes - latitud2Radianes)/2) + cos(latitud1_Radianes) * cos(latitud2) * sin**2( (longitud1_rad - longitud2_rad) / 2)
    c = 2 * asin(sqrt(a))
    distancia  = R * c

    Pero en la consulta se uso una formula simpliflicada para mejorarar la legibilidad y la eficiencia eliminando los cuadrados y usando acos directamente
    es una aproximacion a la formula original
    """
    def resolve_puntosDeAccesoMasCercanos(self,info,latitud,longitud,page,page_size):
        
        try:
            print("Obteniendo puntos..")

            #Aqui se 
            puntoDeAccesoWifi = PuntoDeAccesoWifi.objects.annotate(
                distancia=RawSQL(
                    """
                    6371 * acos(
                        cos(radians(%s)) * cos(radians(latitud)) *
                        cos(radians(longitud) - radians(%s)) +
                        sin(radians(%s)) * sin(radians(latitud))
                    )
                    """,
                    (latitud, longitud, latitud),
                    output_field=FloatField()
                )
            ).order_by('distancia')
            print("Puntos obtenidos")

            print("Ordenando puntos obtenidos")
            puntos_ordenados = puntoDeAccesoWifi
            print("Puntos ordenados")

            paginator = Paginator(puntos_ordenados,page_size)
            current_page = paginator.get_page(page)
            return current_page


            
        except Exception as e:
            print(f"Error en resolve_puntosDeAccesoMasCercanos: {e}")
            return None  # Manejar el error y devolver None si algo sale mal
    
    
    






schema = graphene.Schema(query=Query)