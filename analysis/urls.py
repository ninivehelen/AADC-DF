from . import views 
from django.urls import path
from django.views.generic import TemplateView 

app_name = 'analysis' 
 
# urlpatterns contém a lista de roteamentos de URLs 
urlpatterns = [ 
  # GET / 
  path('', TemplateView.as_view(template_name="index.html")),
  path('',views.Graphic_list,name='Graphic_list')
] 