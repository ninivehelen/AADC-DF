import pandas as pd 
import matplotlib.pyplot as plt
from IPython.display import display
#from cep_df import cep_df
import io, os
import gdown
import urllib, base64
from django.shortcuts import render

arquivo_csv = "aadc/csv/Covid_DF.csv"
if not os.path.isfile(arquivo_csv):
    os.makedirs("aadc/csv", exist_ok=True)
    gdown.download("https://drive.google.com/u/0/uc?id=1vKiEsNMtWXLhK9h9Og2VpzXEonQOIfas", arquivo_csv, quiet=False)

dados = pd.read_csv(arquivo_csv, sep = ';')

# Colunas Selecionadas
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
#print((dados_vacina['paciente_racacor_valor']).value_counts())
#print(dados_vacina.loc[dados_vacina['paciente_racacor_valor'] == 50.59404737212269] )
dados_vacina.drop(dados_vacina.loc[dados_vacina['paciente_racacor_valor'] == 50.59404737212269].index, inplace=True)

#Alteração na UF do paciente
dados_vacina.loc[dados_vacina['paciente_endereco_uf'] == 'XX'] = 'Não informado'
#print(dados_vacina)

# Exportando dados
#dados_vacina['paciente_idade'].to_csv('paciente_idade.csv')

####################### Quantidade de pessoas que tomaram a 1°, 2° e 3° dose #######################

def graf_quant_dose123():

    # Filtrando dados do DataFrame
    colunas = ['vacina_descricao_dose']
    doses = dados_vacina.filter(items=colunas)
    
    graf = doses.value_counts()

    labels = ['1° Dose', '2° Dose', 'Dose única','Não informado' ]
    plt.style.use("ggplot")
    explode = (0.1, 0.0, 0.0, 0.0)

    labels1 = ['', '', '', '']
    graf.plot.pie(autopct='%1.1f%%', shadow=True, startangle = 90, ylabel='', title = 'Porcentagem de pessoas que tomaram a 1° dose, 2° dose e a dose única.\n', subplots=True, labels = labels1,explode= explode ) 

    L = plt.legend( bbox_to_anchor=(1, 0, 0.5, 1), loc='center left', labels = labels)
    plt.show() 

#######################Classificação por região geográfica.(estados do Brasil)#######################

def graf_regiao_geografica_estados():

    # Filtrando dados do DataFrame
    colunas = ['paciente_endereco_uf']
    dados_regiao_geografica = dados_vacina.filter(items=colunas)

    # Gráfico UF do paciente 
    graf = (dados_regiao_geografica['paciente_endereco_uf'].value_counts())

    graf.plot.bar(title = 'Localização geográfica das pessoas que se vacinaram no DF\n', xlabel= 'Estados', ylabel = 'Quantidade de pessoas')
    plt.show() 

####################### Classificação por região geográfica. (paises) #######################

def graf_regiao_geografica_paises():

    label = 'Ruanda', 'Venezuela', 'Bolívia' ,  'Congo', 'Japão', 'Andorra','Colômbia', 'Gibraltar', 'Portugal', 'São Tomé e Príncipe'

    # Filtrando dados do DataFrame
    colunas = ['paciente_endereco_nmpais']
    regiao_geografica_paises = dados_vacina.filter(items=colunas)

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
    plt.show() 

####################### Faixa etária das pessoas que tomaram a vacina. #######################
def faixa_etaria():

  # Filtrando dados do DataFrame
    colunas = ['paciente_idade']
    idade = dados_vacina.filter(items=colunas)
    #idade = dados_vacina['paciente_idade']
 
    # Alteração na idade  do paciente
    idade.drop(idade.loc[idade['paciente_idade'] == 'Não informado'].index, inplace=True)
    
    # Criação do gráfico
   
    idade.plot.hist(bins=30, color= 'green')
    plt.show()

####################### Classificação por vacina (Pfizer..) #######################
def name_vacina():
    # Filtrando dados do DataFrame
    colunas = ['vacina_nome']
    vacinas = dados_vacina['vacina_nome']

    vacinas = vacinas.replace('Vacina Covid-19 - Covishield', 'Covishield')
    vacinas = vacinas.replace('Covid-19-Coronavac-Sinovac/Butantan', 'Sinovac/Butantan')
    vacinas = vacinas.replace('Vacina covid-19 - BNT162b2 - BioNTech/Fosun Pharma/Pfizer', 'Pfizer')
    vacinas = vacinas.replace('Covid-19-AstraZeneca', 'AstraZeneca')
    vacinas = vacinas.replace('Vacina covid-19 - Ad26.COV2.S - Janssen-Cilag', 'Janssen-Cilag')

    # Gráfico
    graf = vacinas.value_counts()
    graf.plot.bar(title='Vacinas utilizadas x Quantidade')
    

    
###########################################Testes################################################

# Testes
def graf_regiao_geografica_df ():
    # Filtrando dados do DataFrame
    colunas = ['paciente_endereco_cep', 'paciente_endereco_nmmunicipio', 'paciente_endereco_uf']
    dados_regiao_geografica_df = dados_vacina.filter(items=colunas)

    dados_regiao_geografica_df = dados_regiao_geografica_df[dados_regiao_geografica_df.paciente_endereco_uf == 'DF']

    #chamando a função cep_df para obter a RA
    dados_regiao_geografica_df['RA'] = [cep_df(cep) for cep in dados_regiao_geografica_df.paciente_endereco_cep]

    print(dados_regiao_geografica_df)

# Conexão com o banco de dados 
def exportar_dados():
    from pymongo import MongoClient
    USERNAME = 'Ninive'
    PASSWORD = 'Ninive'
    mongodb = MongoClient("mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.kvg8p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
 
    # Banco de dados
    db = mongodb.Cluster0
    print(db.list_collection_names())

    #collection
    collection = db['dados_aadc']

    dados_vacina.reset_index(inplace=True)
    data_dict = dados_vacina.to_dict("records")
    collection.insert_one({"index":"Sensex","data":data_dict})



# Chamando as funções 
#graf_quant_dose123()
#graf_regiao_geografica_estados()
#graf_regiao_geografica_paises()
#faixa_etaria()
name_vacina()


#graf_regiao_geografica_df()
#exportar_dados()

