from django.db import models
from django.db.models import Model
# Create your models here.

class Graphic(Model):
    nome = models.CharField(max_length=255, null = True)
    imageGraphic = models.ImageField()
    objetos  =  models.Manager()
