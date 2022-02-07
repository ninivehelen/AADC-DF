from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from analysis.models import Graphic

#from . import graph

#class Graphic_list(ListView):
#
#    template_name = "templates/index.html" 
#    model = Graphic 
#    context_object_name = "Graphic"

def Graphic_list(request): 
  graphics = Graphic.objetos.all()
  print(graphics)
 
  # Incluímos no contexto 
  context = { 
    'graphics': graphics
  } 
 
  return render( 
    request,  
    "/templates/index.html",  
    context
  )


