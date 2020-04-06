from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import json  
import codecs
import pandas as pd
import os
import shutil
from datetime import datetime, timedelta, date
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from os import remove
import git
from datetime import datetime


#************************************Actualizar repositorio***********************************************
def guardarRepositorio():
    repoLocal = git.Repo( 'C:/Users/limc_/Documents/GitHub/Datos' )
    print(repoLocal.git.status())
    repoLocal.git.add(".")
    try:
        repoLocal.git.commit(m='Update automatico via python')
    except:
        pass
    origin = repoLocal.remote(name='origin')
    origin.push()
    return True
#************************************Actualizar repositorio***********************************************

#************************************Actualizar Chile*****************************************************
def Chile():
    url_chile = "https://raw.githubusercontent.com/ivanMSC/COVID19_Chile/master/covid19_chile.csv"
    pd.read_csv(url_chile).to_csv("Chile/covid19_chile.csv", index=False)
    url_comunas = "https://raw.githubusercontent.com/ivanMSC/COVID19_Chile/master/covid19_comunas.csv"
    pd.read_csv(url_chile).to_csv("Chile/covid19_comunas.csv", index=False)
    url_old = "https://raw.githubusercontent.com/ivanMSC/COVID19_Chile/master/old/covid19_chile.csv"
    pd.read_csv(url_chile).to_csv("Chile/covid19_chile_old.csv", index=False)    
    data = pd.read_excel("Chile/covid19_chile.xlsx")
    del data["Unnamed: 14"]
    del data["Unnamed: 15"]
    del data["Unnamed: 16"]
    data["Fecha"] = data["Fecha"].apply(cambiaFecha)
    data.to_csv("covid19_chile.csv", index=False)
    
    guardarRepositorio()    
    return

def cambiaFecha(texto):
    if(type(texto) == datetime):
        return texto.strftime("%m-%d-%Y")
    else:
        return texto
#************************************Actualizar Chile*****************************************************

#************************************Actualizar EarlyAlert************************************************
def EarlyAlert():
    url  = 'https://services9.arcgis.com/Rha9bYQCF0JEy8bJ/ArcGIS/rest/services/Current_Coronavirus_Cases_and_Deaths/FeatureServer/0/1?f=pjson'
    response = requests.get(url)
    decoded_data=codecs.decode(response.content, 'utf-8-sig')
    d = json.loads(decoded_data)
    #print(d["feature"]["attributes"])
    flag = True
    n = 1
    salida = []
    while flag:
        try:
            url  = 'https://services9.arcgis.com/Rha9bYQCF0JEy8bJ/ArcGIS/rest/services/Current_Coronavirus_Cases_and_Deaths/FeatureServer/0/'+str(n)+'?f=pjson'
            response = requests.get(url)
            decoded_data=codecs.decode(response.content, 'utf-8-sig')
            d = json.loads(decoded_data)
            #print(d["feature"]["attributes"])
            salida.append(d["feature"]["attributes"])
            n += 1
        except:
            flag = False
    data = pd.DataFrame.from_dict(salida)
    #data.head()
    now = datetime.now()

    data.to_csv("EarlyAlert/Current_Coronavirus_Cases_and_Deaths.csv", index=False)
    data.to_csv("EarlyAlert/Current_Coronavirus_Cases_and_Deaths." + now.strftime("%d-%m-%Y_%H-%M-%S") + "csv", index=False)
    
    guardarRepositorio()
    return
#************************************Actualizar EarlyAlert************************************************

#************************************Actualizar ecdcEuropa************************************************
def ecdcEuropa():
    now = datetime.now()
    url= "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"
    data = pd.read_csv(url)
    data.to_csv("ecdc.europa/Current_Coronavirus_Cases_and_Deaths.csv", index=False)
    data.to_csv("ecdc.europa/ecCurrent_Coronavirus_Cases_and_Deaths." + now.strftime("%d-%m-%Y_%H-%M-%S") + "csv", index=False)
    guardarRepositorio()
    return
#************************************Actualizar ecdcEuropa************************************************

#************************************Actualizar johnsHopkins**********************************************
#DATO DIARIO
def johnsHopkinsCovid19Diario(): 
    #Carpeta Diario
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" 
    inicio = datetime(2020,1,22)
    fin    = datetime.now()
    lista_fechas = [inicio + timedelta(days=d) for d in range((fin - inicio).days + 1)] 
    for i in lista_fechas:
        nombre = i.strftime("%m-%d-%Y.csv")
        nombre2 = "Johns_Hopkins-covid19/diario/"+ str(nombre)
        try:
            ultimo = pd.read_csv(url + nombre)
            ultimo.to_csv(nombre2,index=False)
        except:
            pass
    ultimo.to_csv("Johns_Hopkins-covid19/diario/ultimoRegistro.csv", index=False)
    guardarRepositorio()
    return

