"""
URL configuration for DataPipeline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('apiPuntosWifi.urls')),
    #Este es el endpoint que usaremos ipaddress:puerto/graphql
    #Con esto se abrira una vista donde podremos hacer la consultas
    #Sí es local host se verira asi la ruta http://127.0.0.1:8000/graphql
    path("graphql",GraphQLView.as_view(graphiql=True, schema=schema))
]
