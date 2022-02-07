from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd 
import matplotlib.pyplot as plt
from IPython.display import display
import io, os
import urllib, base64
import gdown
from analysis import graph

def index(request):
    graphic_link = []
    graphic_id = ['graf_quant_dose', 'graf_estados', 'graf_paises', 'graf_faixa_etaria', 'graf_nome_vacina',
    'graf_dose_tomada', 'graf_vacina_etnia', 'graf_vacina_categoria', 'graf_vacina_genero_biologico', 'graf_uf_vacinados']
    graphic_name = ['Quantidade Doses', 'Estados', 'Paises', 'Faixa Etária', 'Nome Vacina', 'Dose Tomada', 'Vacina Etnia', 'Vacina Categoria', 'Vacina Genero Biologico', 'UF Vacinados']
    for graph in graphic_id:
        graphic_link.append(f"img/{graph}.png")
    graphics = {}
    for i in range(len(graphic_id)):
        graphics[graphic_id[i]] = graphic_link[i]
    graphic_buttons = {}
    for i in range(len(graphic_id)):
        graphic_buttons[graphic_id[i]] = graphic_name[i]
    context = {
        'graphics': graphics,
        'graphic_buttons': graphic_buttons,
        'total_cases': 0,
        'total_deaths': 0,
        'total_recovered': 0,
    }
    return render(request, 'index.html', context)
