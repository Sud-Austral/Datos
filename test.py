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
#DATO SERIE
def johnsHopkinsCovid19Series():
    
    #Carpeta Series
    
    pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv").to_csv("Johns_Hopkins-covid19/series/time_series_covid19_confirmed_US.csv", index=False)
    pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv").to_csv("Johns_Hopkins-covid19/series/time_series_covid19_confirmed_global.csv", index=False)
    pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv").to_csv("Johns_Hopkins-covid19/series/time_series_covid19_deaths_US.csv", index=False)
    pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv").to_csv("Johns_Hopkins-covid19/series/time_series_covid19_deaths_global.csv", index=False)
    pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv").to_csv("Johns_Hopkins-covid19/series/time_series_covid19_recovered_global.csv", index=False)
    
    data_confirmed = pd.read_csv("time_series_covid19_confirmed_global.csv")
    data_recovered = pd.read_csv("time_series_covid19_recovered_global.csv")
    data_death     = pd.read_csv("time_series_covid19_deaths_global.csv")

    data_salida_confirmed = pd.DataFrame() 
    data_salida_recovered = pd.DataFrame()
    data_salida_death = pd.DataFrame()
    data_salida_confirmed["Province/State"] = data_confirmed["Province/State"] 
    data_salida_confirmed["Country/Region"] = data_confirmed["Country/Region"] 
    data_salida_confirmed["Lat"] = data_confirmed["Lat"]
    data_salida_confirmed["Long"] = data_confirmed["Long"]

    data_salida_recovered["Country/Region"] = data_recovered["Country/Region"] 
    data_salida_recovered["Province/State"] = data_recovered["Province/State"] 
    data_salida_death["Country/Region"] = data_death["Country/Region"]

    columna_anterior = ""
    for columna in data_confirmed.columns[4:len(data_confirmed)]:
        if(columna_anterior == ""):
            #print("no se hace nada")
            pass
        else:
            #print(columna + " y " + columna_anterior)

            data_salida_confirmed[columna] = data_confirmed[columna] - data_confirmed[columna_anterior]
            data_salida_recovered[columna] = data_recovered[columna] - data_recovered[columna_anterior]
            data_salida_death[columna]     = data_death[columna]     - data_death[columna_anterior]

        columna_anterior = columna

    entrada = {"Province/State":""}   #,"Country/Region":"","Lat":"","Long":""}
    salida = []

    data_salida = pd.DataFrame(columns=data_salida_confirmed.columns[:4])

    lista_confirmed = list(data_salida_confirmed.iterrows())
    lista_recovered = list(data_salida_recovered.iterrows())
    lista_death = list(data_salida_death.iterrows())

    n = 0
    for i in range(len(lista_confirmed)):
        dias_correlativo = 0
        flag = True
        for columna in data_salida_confirmed.columns[4:]:         
            #print(columna)
            #print(i[1][columna])
            entrada["Province/State"] = lista_confirmed[i][1]["Province/State"]
            entrada["Country/Region"] = lista_confirmed[i][1]["Country/Region"]

            entrada["Lat"] = lista_confirmed[i][1]["Lat"]
            entrada["Long"] = lista_confirmed[i][1]["Long"]
            formato = columna.split("/")
            entrada["fecha"] = datetime.date(int(formato[2]+"20"),int(formato[0]),int(formato[1])).strftime("%d-%m-%Y")
            #print(lista_confirmed[i][1][columna]) 
            #print(entrada["Country/Region"])
            entrada["confirmados"] = lista_confirmed[i][1][columna]
            entrada["fallecidos"] = lista_death[i][1][columna]
            entrada["codigo"] = entrada["Country/Region"] + str(entrada["Province/State"]) + entrada["fecha"]

            if(flag):
                if(entrada["confirmados"] != 0):
                    flag = False;
                    dias_correlativo += 1
            else:
                dias_correlativo += 1
            entrada["dias correlativo"] = dias_correlativo
            salida.append(data_salida.append(entrada,ignore_index=True))
    data_salida = pd.concat(salida)

    entrada = {"Province/State":""}
    salida = []
    data_salida_aux = pd.DataFrame(columns=data_salida_confirmed.columns[:4])
    for i in range(len(lista_recovered)):
        for columna in data_salida_recovered.columns[4:]:
            entrada["Province/State"] = lista_recovered[i][1]["Province/State"]
            entrada["Country/Region"] = lista_recovered[i][1]["Country/Region"]
            formato = columna.split("/")
            entrada["fecha"] = datetime.date(int(formato[2]+"20"),int(formato[0]),int(formato[1])).strftime("%d-%m-%Y")
            entrada["recuperado"] = lista_recovered[i][1][columna]
            entrada["codigo"] = entrada["Country/Region"] + str(entrada["Province/State"]) + entrada["fecha"]
            #print(entrada)
            #print("*****************************************************************")
            salida.append(data_salida_aux.append(entrada, ignore_index=True))
    data_salida_aux = pd.concat(salida)
    del data_salida_aux["Province/State"]
    del data_salida_aux["Country/Region"]
    del data_salida_aux["fecha"]
    del data_salida_aux["Lat"]
    del data_salida_aux["Long"]

    merged_left = pd.merge(left=data_salida, right=data_salida_aux, how='left', left_on='codigo', right_on='codigo')
   
    merged_left.to_csv("Johns_Hopkins-covid19/series/acumulado.csv", index=False)


    guardarRepositorio()
    return
#************************************Actualizar johnsHopkins*********************************************

