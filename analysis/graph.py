from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd 
import matplotlib.pyplot as plt
from IPython.display import display
import io, os
import urllib, base64
import gdown
from analysis.models import Graphic

#from cep_df import cep_df

# Checa se existe os dados em .csv
arquivo_csv = "aadc/csv/Covid_DF.csv"
if not os.path.isfile(arquivo_csv):
    os.makedirs("aadc/csv", exist_ok=True)
    gdown.download("https://drive.google.com/u/0/uc?id=1vKiEsNMtWXLhK9h9Og2VpzXEonQOIfas", arquivo_csv, quiet=False)

dados = pd.read_csv(arquivo_csv, sep = ';')

colunas_selecionadas =  ['paciente_idade', 'paciente_enumsexobiologico', 'paciente_racacor_valor', 'paciente_endereco_nmmunicipio', 'paciente_endereco_nmpais', 'paciente_endereco_uf', 'estalecimento_nofantasia', 'vacina_grupoatendimento_nome', 'vacina_categoria_nome', 'vacina_descricao_dose', 'vacina_nome', 'paciente_endereco_cep']

# Novo Dataframe com as colunas selecionadas
dados_vacina = dados.filter(items = colunas_selecionadas)

# Idades inconsistentes foram substituidas pela média aritmética da coluna 'paciente_idade'
dados_vacina.loc[dados_vacina['paciente_idade'].isnull()] = dados_vacina['paciente_idade'].mean()

# Dados nulos das outras colunas foram substituidos por 'Não informado'
dados_vacina.fillna("Não informado", inplace = True)

# Soma de valores nulos em cada coluna
#print(dados_vacina.isnull().sum())

# Drop paciente_racacor_valor = 50.59404737212269]
dados_vacina.drop(dados_vacina.loc[dados_vacina['paciente_racacor_valor'] == 50.59404737212269].index, inplace=True)

#Alteração na UF do paciente
dados_vacina.loc[dados_vacina['paciente_endereco_uf'] == 'XX'] = 'Não informado'


####################### Quantidade de pessoas que tomaram a 1°, 2° e 3° dose #######################

def graf_quant_dose123(name):
    # Filtrando dados do DataFrame

    colunas = ['vacina_descricao_dose']
    vacina_dose = dados.filter(items=colunas)
    
    # Removendo dados de não informado
    vacina_dose.drop(vacina_dose.loc[vacina_dose['vacina_descricao_dose'] == 'Não informado'].index, inplace=True)
 
    graf = vacina_dose.value_counts()

    labels = ['1° Dose', '2° Dose', 'Dose única']
    #plt.style.use("ggplot")
    explode = (0.1, 0.0, 0.0)
    graf.plot.pie(figsize=(7, 5), autopct='%1.1f%%', shadow=True, startangle = 90, ylabel='', title = 'Porcentagem de pessoas que tomaram a 1° dose, 2° dose e a dose única.\n', subplots=True, labels = labels, explode=explode) 

    #plt.legend( bbox_to_anchor=(1, 0, 0.5, 1), loc='center left', labels = labels)
    #plt.show() 
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(f"aadc/static/img/{name}.png", format = 'png')
    plt.close(fig)

#######################Classificação por região geográfica.(estados do Brasil)#######################

def graf_regiao_geografica_estados(name):

    # Filtrando dados do DataFrame
    colunas = ['paciente_endereco_uf']
    dados_regiao_geografica = dados.filter(items=colunas)

    # Gráfico UF do paciente 
    graf = dados_regiao_geografica['paciente_endereco_uf'].value_counts()

    graf.plot.bar(figsize=(7, 5), title = 'Localização geográfica das pessoas que se vacinaram no DF\n', xlabel= 'Estados', ylabel = 'Quantidade de pessoas')
    #plt.show() 
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(f"aadc/static/img/{name}.png", format = 'png')
    plt.close(fig)


####################### Classificação por região geográfica. (paises) #######################

def graf_regiao_geografica_paises(name):

    label = 'Ruanda', 'Venezuela', 'Bolívia' ,  'Congo', 'Japão', 'Andorra','Colômbia', 'Gibraltar', 'Portugal', 'São Tomé e Príncipe'

    # Filtrando dados do DataFrame
    colunas = ['paciente_endereco_nmpais']
    regiao_geografica_paises = dados.filter(items=colunas)

    # Gráfico país do paciente 
    graf_paises = (regiao_geografica_paises['paciente_endereco_nmpais'].value_counts())

    # Países estrangeiros 
    graf_paises_estrangeiros = regiao_geografica_paises[(regiao_geografica_paises['paciente_endereco_nmpais'] != 'BRASIL') & (regiao_geografica_paises['paciente_endereco_nmpais'] != 'Não informado')].value_counts()

    # Criação do gráfico
    fig, axs = plt.subplots(1,2)
    axs[0].set_title('Países')
    axs[0].pie(graf_paises, shadow=True, startangle=90)
    axs[1].set_title('Países estrangeiros')
    axs[1].pie(graf_paises_estrangeiros, labels=label, shadow=True, startangle=90)
  
    #Django
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(f"aadc/static/img/{name}.png", format = 'png')
    plt.close(fig)

####################### Faixa etária das pessoas que tomaram a vacina. #######################

def faixa_etaria(name):

  # Filtrando dados do DataFrame
    colunas = ['paciente_idade']
    idade = dados.filter(items=colunas)
    #idade = dados_vacina['paciente_idade']
 
    # Alteração na idade  do paciente
    idade.drop(idade.loc[idade['paciente_idade'] == 'Não informado'].index, inplace=True)
    
    # Criação do gráfico
    
    idade.plot.hist(bins=30, figsize=(7, 5), color= 'green') 

    #Django
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(f"aadc/static/img/{name}.png", format = 'png')
    plt.close(fig)

####################### Classificação por vacina (Pfizer..) #######################
def name_vacina(name):
    # Filtrando dados do DataFrame
    colunas = ['vacina_nome']
    vacinas = dados.filter(items=colunas)

    vacinas = vacinas.replace('Vacina Covid-19 - Covishield', 'Covishield')
    vacinas = vacinas.replace('Covid-19-Coronavac-Sinovac/Butantan', 'Sinovac/Butantan')
    vacinas = vacinas.replace('Vacina covid-19 - BNT162b2 - BioNTech/Fosun Pharma/Pfizer', 'Pfizer')
    vacinas = vacinas.replace('Covid-19-AstraZeneca', 'AstraZeneca')
    vacinas = vacinas.replace('Vacina covid-19 - Ad26.COV2.S - Janssen-Cilag', 'Janssen-Cilag')

    # Gráfico
    graf = vacinas.value_counts()
    graf.plot.bar(title='Vacinas utilizadas x Quantidade', figsize=(7, 5),)
    #print(graf)

    #Django
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(f"aadc/static/img/{name}.png", format = 'png')
    plt.close(fig)

####################### Classificação por Etnia #######################
def vacina_etnia(name):
    #Filtrando as colunas
    dados_limpos = dados[ dados['paciente_racacor_valor'] == 'SEM INFORMACAO' ].index
    dados.drop(dados_limpos , inplace=True)
    graf = (dados['paciente_racacor_valor'].value_counts())
    #Criando o grafico
    graf.plot.bar(title = 'Etnia\n',xlabel= 'Vacinas', ylabel = 'Frequência', color= "ORANGE", figsize=(7, 5),)

    #Django
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(f"aadc/static/img/{name}.png", format = 'png')
    plt.close(fig)
   
####################### Classificação por Grupo de vacinados #######################

def vacina_categoria(name):
    #Filtrando as colunas
    graf = (dados['vacina_categoria_nome'].value_counts())
    #Criando o grafico
    graf.plot.bar(figsize=(7, 5), title = 'Categorias mais vacinadas no DF\n', xlabel= 'Vacinas', ylabel = 'Frequência', color = "green")

    #Django
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(f"aadc/static/img/{name}.png", format = 'png')
    plt.close(fig)

####################### Classificação por genero biologico #######################

def vacina_genero_biologico(name):
    #Filtrando coluna
    graf = (dados['paciente_enumsexobiologico'].value_counts())
    #Criando o gráfico
    graf.plot.pie(figsize=(7, 5), title = 'Gênero que mais se vacinou no  DF\n', autopct='%1.1f%%',xlabel= 'Vacinas', ylabel = 'Porcentagem')

    #Django
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(f"aadc/static/img/{name}.png", format = 'png')
    plt.close(fig)

####################### Classificação por UF dos vacinados #######################
def uf_dos_vacinados(name):
    #Filtrando coluna
    graf = (dados['paciente_endereco_uf'].value_counts())
    #Criando o gráfico
    graf.plot.bar(figsize=(7, 5), title = 'UF dos pacientes que foram vacinados no DF\n', xlabel= 'Vacinas', ylabel = 'Frequência', color = "Yellow")

    #Django
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(f"aadc/static/img/{name}.png", format = 'png')
    plt.close(fig)
  
####################### Classificação das doses ja tomadas #######################
def dose_tomada(name):
    #Filtrando as colunas
    graf = (dados['vacina_descricao_dose'].value_counts())
    #Criando os gráficos
    graf.plot.barh(figsize=(7, 5), title = 'Quantidade das doses já tomadas DF\n', xlabel= 'Vacinas', ylabel = 'Frequência', color="purple")

    #Django
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(f"aadc/static/img/{name}.png", format = 'png')
    plt.close(fig)

# Chamando as funções 
Quantidade_doses = Graphic(imageGraphic = graf_quant_dose123("graf_quant_dose"))
Quantidade_doses.save()
Região_geografica_estados = Graphic(imageGraphic = graf_regiao_geografica_estados("graf_estados"))
Região_geografica_estados.save()
Região_geografica_paises = Graphic(imageGraphic = graf_regiao_geografica_paises("graf_paises"))
Região_geografica_paises.save()
Faixa_Etaria = Graphic(imageGraphic = faixa_etaria("graf_faixa_etaria"))
Faixa_Etaria.save()
Nome_vacina = Graphic(imageGraphic = name_vacina("graf_nome_vacina"))
Nome_vacina.save()
Vacina_etnia = Graphic(imageGraphic = vacina_etnia("graf_vacina_etnia"))
Vacina_etnia.save()
Vacina_Categoria = Graphic(imageGraphic = vacina_categoria("graf_vacina_categoria"))
Vacina_Categoria.save()
Vacina_Genero = Graphic(imageGraphic = vacina_genero_biologico("graf_vacina_genero_biologico"))
Vacina_Genero.save()
Uf_Vacinados = Graphic(imageGraphic = uf_dos_vacinados("graf_uf_vacinados"))
Uf_Vacinados.save()
Dose_Tomada = Graphic(imageGraphic = dose_tomada("graf_dose_tomada"))
Dose_Tomada.save()






#graf_regiao_geografica_df()
#exportar_dados()
