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
import datetime
import numpy as np
import wget
import http.client, urllib.request, urllib.parse, urllib.error, base64
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import tweepy
import gc
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
#from datetime import datetime
#************************************Ciclo****************************************************************
def Ciclo():
    now = datetime.datetime.now()
    hora = now.strftime("%H")
    if(hora == "17"):
        UpdateDatabase()
    if(hora == "19"):
        UpdateDatabase() 
    if(hora == "20"):
        UpdateDatabase()
    #if(hora == "20"):
    #    UpdateDatabase()    
    time.sleep(600)
    Ciclo()
#************************************Ciclo****************************************************************
#************************************Actualizar Database**************************************************
def UpdateDatabase():
    print("Comenzo...")
    try:
        datasetFinalTweet()
        print("Twiter completos...")
    except:
        print("Error a cargar Twiter")
    #try:
    #    guardarAnalisisTwitter()
    #    print("Analisis de Twitter completo...")
    #except:
    #    print("Error de analisis de Twitter...")
    #gc.collect()
    try:
        descargarProductos()
        print("Productos avanzados completos...")
    except:
        print("Error a cargar productos avanzados")
    gc.collect()
    try:
        minSal3Carpeta()
        print("3 carpetas del MinSal completos...")
    except:
        print("Error al cargar 3 carpetas del MinSal")
    gc.collect()
    try:
        guardarDataCovid()
        print("Cargar datos de la organización completo...")
    except:
        print("Error a cargar datos de la organización")
    gc.collect()
    try:
        bingNews()
        print("Bing News completo...")
    except:
        print("Error a cargar a Bing News")
    gc.collect()
    try:
        minsal()
        print("Minsal completo...")
    except:
        print("Error a cargar a Minsal")
    gc.collect()
    try:
        Farmacias()
        print("Farmacias completo...")
    except:
        print("Error a cargar a Farmacias")
    gc.collect()
    try:
        Chile()
        print("Chile completo...")
    except:
        print("Error a cargar a Chile")
    gc.collect()
    try:
        johnsHopkinsCovid19Diario()
        print("Hopkins diario completo...")
    except:
        print("Error a cargar a Hopkins diario")
    gc.collect()
    try:
        johnsHopkinsCovid19Series()
        print("Hopkins serie (acumulado) completo...")
    except:
        print("Error a cargar a Hopkins Serie")
    gc.collect()
    try:
        ecdcEuropa()
        print("ECDC Europa completo...")
    except:
        print("Error a cargar a Hopkins Serie")
    gc.collect()
    try:
        worldometersInfo()
        print("WORLDMETER completo...")
    except:
        print("Error a cargar a Hopkins Worldmeter")
    gc.collect()
    try:
        ourWorldInData()
        print("OurWorldInData completo...")
    except:
        print("Error a cargar a OurWorldInData")
    gc.collect()
    try:
        EarlyAlert()
        print("EarlyAlert completo...")
    except:
        print("Error a cargar a Hopkins EarlyAlert")
    gc.collect()
    try:
        KoBoToolbox()
        print("KoBoToolbox completo...")
    except:
        print("Error a cargar a KoBoToolbox")
    gc.collect()
    print("**************************************************************************")
    print("**************************************************************************")
    print("                            Ciclo completo")
    print("**************************************************************************")
    print("**************************************************************************")
    return
#************************************Actualizar Database**************************************************
#************************************Analisis Twitter*******************************************
def getKeys():
    f = open('C://key.json','r')
    keys = f.read()
    jkeys = json.loads(keys)
    return jkeys
#************************************Analisis Twitter*******************************************

#************************************Actualizar Verifica Columnas*****************************************
def verificarColumnas(data, referencia):
    ruta = "GrupoControl/"
    df = data
    ref = pd.read_csv(ruta + referencia)
    existe = False
    columna = 0
    #Eliminar Columnas que sobran
    for col in df.columns:
        for colRef in ref.columns:
            if col == colRef:
                #print("existe la columna" + col)
                existe = True
        if existe == False:
            del df[col]
            #df.to_csv(csvPorVerificar, index = False)
            print("se Eliminó la columna " + col)
        existe = False
    #Agregar columnas faltantes
    for colRef in ref.columns:
        for col in df.columns:
            if col == colRef:
                #print("existe la columna" + col)
                existe = True
        if existe == False:
            df.insert(columna,colRef,'')
            #df.to_csv(csvPorVerificar, index = False)
            print("se agregó la columna " + colRef)
        columna+=1
        existe = False
    return df
#************************************Actualizar Verifica Columnas*****************************************

#************************************Actualizar repositorio***********************************************
def guardarRepositorio():
    #repoLocal = git.Repo( 'C:/Users/mario1/Documents/GitHub/Python/Datos' )
    repoLocal = git.Repo('C:/Users/datos/Documents/GitHub/Datos')
    #print(repoLocal.git.status())

    try:
        repoLocal.git.add(".")
        repoLocal.git.commit(m='Update automatico via Actualizar ' + datetime.datetime.now().strftime("%m-%d-%Y %H-%M-%S"))
        origin = repoLocal.remote(name='origin')
        origin.push()
    except:
        print("Error de GITHUB")

    return
#************************************Actualizar repositorio***********************************************

#************************************Actualizar Chile*****************************************************
def Chile():
    try:
        os.remove('Chile/covid19_chile.xlsx')
    except:
        pass
    wget.download("https://onedrive.live.com/download?resid=9F999E057AD8C646!62083&authkey=!AHatwZn5tIFkoZE", "Chile/covid19_chile.xlsx")
    url_chile = "https://raw.githubusercontent.com/ivanMSC/COVID19_Chile/master/covid19_chile.csv"
    pd.read_csv(url_chile).to_csv("Chile/covid19_chile.csv", index=False)
    url_comunas = "https://raw.githubusercontent.com/ivanMSC/COVID19_Chile/master/covid19_comunas.csv"
    pd.read_csv(url_chile).to_csv("Chile/covid19_comunas.csv", index=False)
    url_old = "https://raw.githubusercontent.com/ivanMSC/COVID19_Chile/master/old/covid19_chile.csv"
    pd.read_csv(url_chile).to_csv("Chile/covid19_chile_old.csv", index=False)
    #data = pd.read_excel("Chile/covid19_chile.xlsx")
    data = pd.read_excel("Chile/covid19_chile.xlsx", sheet_name="Sheet1")
    try:
        del data["Unnamed: 14"]
        del data["Unnamed: 15"]
        del data["Unnamed: 16"]
    except:
        pass

    data["Fecha"] = data["Fecha"].apply(cambiaFecha)
    data = verificarColumnas(data, "covid19_chile.csv")
    data.to_csv("Chile/covid19_chile.csv", index=False)

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
    now = datetime.datetime.now()
    data.to_csv("EarlyAlert/Current_Coronavirus_Cases_and_Deaths.csv", index=False)
    guardarRepositorio()
    return
#************************************Actualizar EarlyAlert************************************************

#************************************Actualizar ecdcEuropa************************************************
def ecdcEuropa():
    now = datetime.datetime.now()
    url= "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"
    data = pd.read_csv(url)
    data = verificarColumnas(data,"Current_Coronavirus_Cases_and_Deaths.csv")
    data.to_csv("ecdc.europa/Current_Coronavirus_Cases_and_Deaths.csv", index=False)
    guardarRepositorio()
    return
#************************************Actualizar ecdcEuropa************************************************

#************************************Actualizar johnsHopkins**********************************************
#DATO DIARIO
def johnsHopkinsCovid19Diario():
    #Carpeta Diario
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
    inicio = datetime.datetime(2020,1,22)
    fin    = datetime.datetime.now()
    lista_fechas = [inicio + timedelta(days=d) for d in range((fin - inicio).days + 1)]
    for i in lista_fechas:
        nombre = i.strftime("%m-%d-%Y.csv")
        nombre2 = "Johns_Hopkins-covid19/diario/"+ str(nombre)
        try:
            ultimo = pd.read_csv(url + nombre)
            ultimo.to_csv(nombre2,index=False)
        except:
            pass
    ultimo = verificarColumnas(ultimo,"ultimoRegistro.csv")
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

    data_confirmed = pd.read_csv("Johns_Hopkins-covid19/series/time_series_covid19_confirmed_global.csv")
    data_recovered = pd.read_csv("Johns_Hopkins-covid19/series/time_series_covid19_recovered_global.csv")
    data_death     = pd.read_csv("Johns_Hopkins-covid19/series/time_series_covid19_deaths_global.csv")

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
            entrada["fecha"] = datetime.datetime(int(formato[2]+"20"),int(formato[0]),int(formato[1])).strftime("%d-%m-%Y")
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
    merged_left = verificarColumnas(merged_left,"acumulado.csv")
    merged_left.to_csv("Johns_Hopkins-covid19/series/acumulado.csv", index=False)


    guardarRepositorio()
    return
#************************************Actualizar johnsHopkins*********************************************
#************************************Actualizar worldmeter***********************************************
def cambioFecha(texto):
    aux = str(texto)
    traductor ={
        "Jan" : 1,
        "Feb" : 2,
        "Mar" : 3,
        "Apr" : 4,
        "May" : 5
    }
    try:
        mes = traductor[aux[:3]]
    except:
        mes = 12
    #datetime.date(2019, 12, 4)
    #dia = int(aux[4:7])
    try:
        dia = int(aux[4:7])
    except:
        return None
    salida = datetime.date(2020,mes,dia)
    return salida.strftime("%d-%m-%Y")

def worldometersInfo():
    url  = 'https://www.worldometers.info/coronavirus/'
    response = requests.get(url)
    #print(response.content)
    #data = pd.read_html(response.content)    
    data = pd.read_html(str(response.content).replace("display:none;",""))
    data_hoy = data[0]     #.to_csv("worldometers.csv", index=False)
    getWorld(data_hoy)

    data_aux = pd.read_csv("worldometers.info/Historico/worldometers.csv")
    for i in data_aux.columns[1:10]:
        del data_aux[i]

    merged_left = pd.merge(left=data_hoy, right=data_aux, how='left', left_on='Country,Other', right_on='Country,Other')
    merged_left = verificarColumnas(merged_left,"worldometers.csv")
    merged_left.to_csv("worldometers.info/worldometers.csv", index=False)

    url  = 'https://www.worldometers.info/world-population/population-by-country/'
    response = requests.get(url)
    #print(response.content)
    data = pd.read_html(response.content)[0]

    data.to_csv("worldometers.info/Poblacion/worldometersPoblacion.csv", index=False)

    guardarRepositorio()
    return

def getWorld(data):
    total = (data[data["Country,Other"] == "World"])["TotalCases"][0]
    archivo = open("Total/total.txt", "w")
    archivo.write(str(total))
    return
#************************************Actualizar worldmeter***********************************************
#************************************KoBoToolbox*********************************************************
def KoBoToolbox():
    url = "https://kc.humanitarianresponse.info/api/v1/forms/520455.csv"

    #response = requests.patch(url, auth=('sudaustral', 'Sudaustral2020+'))
    response = requests.get(url, auth=('sudaustral', 'Sudaustral2020+'))
    decoded_data = codecs.decode(response.content, 'utf-8-sig')
    archivo = open("data_aux.txt", "w")
    archivo.write(decoded_data)
    archivo.close()
    #data = pd.read_csv("data_aux.txt")
    data = pd.read_csv("data_aux.txt",encoding='latin-1')
    data.to_csv("KoBoToolbox/COVID-19DataIntelligenceCHILE.csv",index=False)
    guardarRepositorio()
    return
#************************************KoBoToolbox*********************************************************

#************************************Actualizar ourWorldInData*******************************************
def ourWorldInData():
    now = datetime.datetime.now()
    archivos = ["covid-19-total-confirmed-cases-vs-total-tests-conducted.csv",
                "full-list-total-tests-for-covid-19.csv",
                "total-deaths-covid-19.csv",
                "total-daily-covid-deaths-per-million.csv",
                "total-cases-covid-19.csv",
                "daily-cases-covid-19.csv",
                "physicians-per-1000-people.csv",
                "hospital-beds-per-1000-people.csv",
                "share-of-the-population-that-is-70-years-and-older.csv",
                "total-and-daily-cases-covid-19.csv"
                ]
    ruta = "C:/Users/datos/Downloads/"

    for i in archivos:
        try:
            remove(ruta + i)
        except:
            pass
    download_folder = "C:/Users/datos/Documents/GitHub/Datos"
    options = Options()
    options.set_preference("browser.download.dir", download_folder)
    #options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv") #, "application/json")
    #browser = webdriver.WebDriver(firefox_profile=profile)
    #driver = webdriver.WebDriver(firefox_profile=profile)
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout("60")

    driver.get("https://ourworldindata.org/grapher/tests-vs-confirmed-cases-covid-19")
    try:
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div[2]/button").click()
        driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div/nav/ul/li[2]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
        time.sleep(1)

        driver.get("https://ourworldindata.org/grapher/covid-19-tests-country")
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div/nav/ul/li[2]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
        time.sleep(1)
        """
        #*********************************************Con mapa sin mapa***********************************************
        driver.get("https://ourworldindata.org/grapher/covid-19-tests-country")
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
        time.sleep(1)
        """

        driver.get("https://ourworldindata.org/grapher/total-deaths-covid-19")
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
        time.sleep(1)

        driver.get("https://ourworldindata.org/grapher/total-daily-covid-deaths-per-million")
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
        time.sleep(1)

        driver.get("https://ourworldindata.org/grapher/total-cases-covid-19")
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
        time.sleep(1)

        driver.get("https://ourworldindata.org/grapher/total-and-daily-cases-covid-19")
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
        time.sleep(1)

        driver.get("https://ourworldindata.org/grapher/daily-cases-covid-19")
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
        time.sleep(1)

        driver.get("https://ourworldindata.org/grapher/physicians-per-1000-people")
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
        time.sleep(1)

        driver.get("https://ourworldindata.org/grapher/hospital-beds-per-1000-people")
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
        time.sleep(1)

        driver.get("https://ourworldindata.org/grapher/share-of-the-population-that-is-70-years-and-older")
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
        time.sleep(1)
        driver.close()
    except:
        driver.close()
    #ruta = "C:/Users/datos/Downloads/"
    folder = "C:/Users/datos/Documents/GitHub/Datos/ourworldindata.org/"
    for i in archivos:
        try:
            shutil.copy(ruta + i, folder  + i)
            verificarColumnas(pd.read_csv(folder  + i),i)
        except:
            pass
    guardarRepositorio()
    return
#************************************Actualizar ourWorldInData*******************************************

#************************************Actualizar Farmacias************************************************
def Farmacias():
    url  = "https://farmanet.minsal.cl/index.php/ws/getLocales"
    response = requests.get(url)
    #decoded_data=codecs.decode(response.content, 'utf-8-sig')
    d = json.loads(response.content)
    data = pd.DataFrame.from_dict(d)
    data.to_csv("Farmacia/Farmacias.csv", index=False)
    url  = "https://farmanet.minsal.cl/index.php/ws/getLocalesTurnos"
    response = requests.get(url)
    #decoded_data=codecs.decode(response.content, 'utf-8-sig')
    d = json.loads(response.content)
    data = pd.DataFrame.from_dict(d)
    data.to_csv("Farmacia/FarmaciasTurno.csv", index=False)
#************************************Actualizar Farmacias*******************************************

#************************************Actualizar Minsal*******************************************
#https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/Covid-19.csv Principal
#https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv #Casos totales por comuna incremental:
# Casos totales por comuna
#https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto2/2020-03-30-CasosConfirmados.csv
#https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto2/2020-04-01-CasosConfirmados.csv
#https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto2/2020-04-03-CasosConfirmados.csv
#https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto2/2020-04-06-CasosConfirmados.csv
#https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto2/2020-04-08-CasosConfirmados.csv
#Casos totales por región incremental:
#https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv
#Casos totales por región
#https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto4/2020-03-03-CasosConfirmados-totalRegional.csv
#...
#https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto4/2020-04-09-CasosConfirmados-totalRegional.csv
#Casos totales recuperados
# https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/recuperados.csv

def realizarColumna(data, largo):
    lista = list(data.iterrows())
    data_aux = data
    try:
        del data_aux["Tasa"]
    except:
        pass
    data_aux.columns
    salida = []
    for i in lista:
        #print(i[1])
        try:
            aux = {"Region":i[1]["Region"],"Comuna":i[1]["Comuna"],"Poblacion":i[1]["Poblacion"],"Tasa":i[1]["Tasa"]}
        except:
            aux = {"Region":i[1]["Region"],"Comuna":i[1]["Comuna"],"Poblacion":i[1]["Poblacion"]}
        for j in data_aux.columns[largo:]:
            entrada = aux.copy()
            #entrada[j] =
            entrada["Fecha"] = i[1][j]
            salida.append(entrada.copy())

    return pd.DataFrame(salida)

def realizarColumnaParticular(data, key):
    lista = list(data.iterrows())
    data_aux = data
    data_aux.columns
    salida = []
    for i in lista:
        #print(i[1])
        aux = {key:i[1][key]}
        for j in data_aux.columns[1:]:
            entrada = aux.copy()
            #entrada[j] =
            entrada["fecha"] = j
            entrada["Recuperado"] = i[1][j]
            salida.append(entrada.copy())

    return pd.DataFrame(salida)

def minsal():
    #Ruta para Chile/MinCiencia
    ruta = "Chile/MinCiencia/"
    #Guardar CSV Principal
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/Covid-19.csv"
    try:
        data = realizarColumna(pd.read_csv(url),3)
        data.to_csv(ruta + "Principal.csv", index=False)
    except:
        pass
    #Guardar CSV Producto1
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv"
    data = realizarColumna(pd.read_csv(url),3)
    data.to_csv(ruta +"Producto1.csv", index=False)
    #Guardar CSV Producto2
    salida = []
    inicio = datetime.datetime(2020,3,30)
    fin    = datetime.datetime.now()
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto2/"  #2020-03-30-CasosConfirmados.csv
    lista_fechas = [inicio + datetime.timedelta(days=d) for d in range((fin - inicio).days + 1)]
    for i in lista_fechas:
        try:
            data = pd.read_csv(url + i.strftime("%Y-%m-%d-CasosConfirmados.csv"))
            data["Fecha"] = i.strftime("%d-%m-%Y")
            salida.append(data)
        except:
            pass
    data =pd.concat(salida)
    data.to_csv(ruta +"Producto2.csv", index=False)
    #Guardar CSV Producto3
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv"
    data = realizarColumnaParticular(pd.read_csv(url),"Region")
    data.to_csv(ruta +"Producto3.csv", index=False)
    #Guardar CSV Producto4
    salida = []
    inicio = datetime.datetime(2020,3,3)
    fin    = datetime.datetime.now()
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto4/"  #2020-03-03-CasosConfirmados-totalRegional.csv
    lista_fechas = [inicio + timedelta(days=d) for d in range((fin - inicio).days + 1)]
    for i in lista_fechas:
        try:
            data = pd.read_csv(url + i.strftime("%Y-%m-%d-CasosConfirmados-totalRegional.csv"))
            data["Fecha"] = i.strftime("%d-%m-%Y")
            salida.append(data)
        except:
            pass
    data =pd.concat(salida)
    data.to_csv(ruta +"Producto4.csv", index=False)
    #Guardar CSV Producto5
    #url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/recuperados.csv"
    #data = realizarColumnaParticular(pd.read_csv(url),"Fecha")
    #data["Estado"] = data["Fecha"]
    #del data["Fecha"]
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv"
    pd.read_csv(url).to_csv(ruta +"Producto5_TotalesNacionales.csv", index=False)

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales_T.csv"
    pd.read_csv(url).to_csv(ruta +"Producto5_TotalesNacionales_T.csv", index=False)

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales_std.csv"
    pd.read_csv(url).to_csv(ruta +"Producto5_TotalesNacionales_std.csv", index=False)
    return
#************************************Actualizar Minsal*******************************************
#************************************Actualizar BING NEWS*******************************************
"""
Argentina	AR
Australia	AU
Austria	AT
Belgium	BE
Brazil	BR
Canada	CA
Chile	CL
Denmark	DK
Finland	FI
France	FR
Germany	DE
Hong Kong SAR	HK
India	IN
Indonesia	ID
Italy	IT
Japan	JP
Korea	KR
Malaysia	MY
Mexico	MX
Netherlands	NL
New Zealand	NZ
Norway	NO
China	CN
Poland	PL
Portugal	PT
Philippines	PH
Russia	RU
Saudi Arabia	SA
South Africa	ZA
Spain	ES
Sweden	SE
Switzerland	CH
Taiwan	TW
Turkey	TR
United Kingdom	GB
United States	US
"""
def fechaCorrecta(i):
    año = i[0:4]
    mes = i[5:7]
    dia = i[8:10]
    hora = i[11:13]
    minuto = i[14:16]
    return dia + "-" + mes + "-" + año + " " + hora + ":" + minuto

def reemplazarFinal(i):
    return i.replace("&pid=News","")

def bingNews(pais = "Chile"):
    #pais = "Chile"
    headers = {
        # Request headers
        #'Ocp-Apim-Subscription-Key': 'b091fbaeb9f94255b542befc3ecff8b8',
        'Ocp-Apim-Subscription-Key': 'a9b5b1527a7b43929d7e15a383b1583a',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'q':  'covid-19 coronavirus ' + pais + ' loc:cl FORM=HDRSC4',
        'count': '40',
        'offset': '0',
        'mkt': 'es-CL',
        'safeSearch': 'Moderate',
        "sortBy": "Date"
    })

    #conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
    conn = http.client.HTTPSConnection('dataintelligence.cognitiveservices.azure.com')
    conn.request("GET", "/bing/v7.0/news/search?%s" % params, "{body}", headers)
    response = conn.getresponse()
    #data = response.read()

    decoded_data=codecs.decode(response.read(), 'utf-8-sig')
    d = json.loads(decoded_data)
    conn.close()
    aux =  d['value']
    salida = []
    for i in aux:
        try:
            i["imagen"] = i["image"]["thumbnail"]["contentUrl"]
            i["pais"] = "Chile"
            try:
                i["Fuente"] = i['provider'][0]["name"]
            except:
                pass
            salida.append(i.copy())
        except:
            pass
    data = pd.DataFrame(salida)[["name","url","description","datePublished","imagen","pais","Fuente"]]
    data["datePublished"] = data["datePublished"].apply(fechaCorrecta)
    data["imagen"] = data["imagen"].apply(reemplazarFinal)
    data[::-1].to_csv("bing/news/Chile.csv",index=False)
    return
#************************************Actualizar BING NEWS*******************************************
#************************************Actualizar minCiencia*******************************************
def minCiencia():
    pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/CasosAcumuladosPorComuna.csv").to_csv("Chile/MinCiencia/CasosAcumuladosPorComuna.csv", index=False)
    pd.read_csv("https://raw.github.com/MinCiencia/Datos-COVID19/master/input/CasosGeneroEtario.csv").to_csv("Chile/MinCiencia/CasosGeneroEtario.csv", index=False)
    pd.read_csv("https://raw.github.com/MinCiencia/Datos-COVID19/master/input/FallecidosEtario.csv").to_csv("Chile/MinCiencia/FallecidosEtario.csv", index=False)
    pd.read_csv("https://raw.github.com/MinCiencia/Datos-COVID19/master/input/Fecha_de_inicio_de_Sintomas.csv").to_csv("Chile/MinCiencia/Fecha_de_inicio_de_Sintomas.csv", index=False)
    pd.read_csv("https://raw.github.com/MinCiencia/Datos-COVID19/master/input/HospitalizadosUCIEtario.csv").to_csv("Chile/MinCiencia/HospitalizadosUCIEtario.csv", index=False)
    pd.read_csv("https://raw.github.com/MinCiencia/Datos-COVID19/master/input/PCR.csv").to_csv("Chile/MinCiencia/PCR.csv", index=False)
    pd.read_csv("https://raw.github.com/MinCiencia/Datos-COVID19/master/input/PCREstablecimiento.csv").to_csv("Chile/MinCiencia/PCREstablecimiento.csv", index=False)
    pd.read_csv("https://raw.github.com/MinCiencia/Datos-COVID19/master/input/SemanasEpidemiologicas.csv").to_csv("Chile/MinCiencia/SemanasEpidemiologicas.csv", index=False)
    pd.read_csv("https://raw.github.com/MinCiencia/Datos-COVID19/master/input/Tasadeincidencia.csv").to_csv("Chile/MinCiencia/Tasadeincidencia.csv", index=False)
    pd.read_csv("https://raw.github.com/MinCiencia/Datos-COVID19/master/input/UCI.csv").to_csv("Chile/MinCiencia/UCI.csv", index=False)
    return
#************************************Actualizar minCiencia*******************************************
#************************************Actualizar organizarMinCienciaInput*******************************************
def organizarMinCienciaInput():
    #carpeta InformeEpidemiologico
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/CasosActivosPorComuna.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/InformeEpidemiologico/CasosActivosPorComuna.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/CasosAcumuladosPorComuna.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/InformeEpidemiologico/CasosAcumuladosPorComuna.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/CasosGeneroEtario.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/InformeEpidemiologico/CasosGeneroEtario.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/FechaInicioSintomas.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/InformeEpidemiologico/FechaInicioSintomas.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/SemanasEpidemiologicas.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/InformeEpidemiologico/SemanasEpidemiologicas.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/Tasadeincidencia.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/InformeEpidemiologico/Tasadeincidencia.csv")

    #carpeta InformeSituacionCOVID19
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeSituacionCOVID19/HospitalizadosGeneroEtario.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/InformeSituacionCOVID19/HospitalizadosGeneroEtario.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeSituacionCOVID19/SintomasCasosConfirmados.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/InformeSituacionCOVID19/SintomasCasosConfirmados.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeSituacionCOVID19/SintomasHospitalizados.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/InformeSituacionCOVID19/SintomasHospitalizados.csv")

    #carpeta ReporteDiario
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/FallecidosEtario.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/ReporteDiario/FallecidosEtario.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/HospitalizadosUCIEtario.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/ReporteDiario/HospitalizadosUCIEtario.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/NumeroVentiladores.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/ReporteDiario/NumeroVentiladores.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/PCR.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/ReporteDiario/PCR.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/PCREstablecimiento.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/ReporteDiario/PCREstablecimiento.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/PacientesCriticos.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/ReporteDiario/PacientesCriticos.csv")

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/UCI.csv"
    resultado = pd.read_csv(url)
    resultado.to_csv("Chile/MinCiencia/Input-minCiencia/ReporteDiario/UCI.csv")

    return
#************************************Actualizar organizarMinCienciaInput*******************************************
#************************************Actualizar Datos de la organizacion*******************************************
def guardarDataCovid():
    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62342&parId=9F999E057AD8C646!62390&authkey=!AgJICaWKd7tHakw&app=Excel"
    urllib.request.urlretrieve(url, "datacovidChile/BASE CALCULO COMUNA.xlsx")
    urllib.request.urlretrieve(url, "datacovidChile/BASECALCULOCOMUNA.xlsx")

    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62359&parId=9F999E057AD8C646!62390&authkey=!AgJICaWKd7tHakw&app=Excel"
    urllib.request.urlretrieve(url, "datacovidChile/casos por comuna listos.xlsx")
    urllib.request.urlretrieve(url, "datacovidChile/casosporcomunalistos.xlsx")

    

    #url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62547&parId=9F999E057AD8C646!62390&authkey=!AkePW7UW1KXQkMM&app=Excel"
    #url = "https://qxvv4q.dm.files.1drv.com/y4mj_IHWbFTvvKjCHpBDRss_UvwFqhzjHsZvwVABt1p8w3GnU_73-nxvxxMbxqhOUyE3pKJpmjC3401TTi_aBp3UrwnltzZLdK01n2u9HudTGubVVYFn8qEpLxKO0uUNOHTlyLfumqkkNk3Adc5nGbHc7mTPMaHo2gsieRy_maEOB0wKdJJttbtTG0UFoQDQRtkDbdaE5zmqTp-_tKhWxPnxeiBPOXW-DCdYBbee6JWtcA?access_token=EwD4Aq1DBAAUzl/nWKUlBg14ZGcybuC4/OHFdfEAAeaXxh2P0Jq45PhEnT91RiIT9H9Qsay/vpCPaXPOYRWxAtQngKfJwhf25hrzvQHA7B/oRlywHtxNT5YtfxYc0bN%2bbfd7B0oQl9HRIJ/13IdG1cXH4QFWT7aTO0HsDRUN1yexRfIbUFGvKT7BKi%2bNPFBxINteXv%2b/Rzi9vbBpW7LWrTTyJZW/XsBcHRKgu08%2bbjERtGwNRfvF0KOeL0mtL21BosDQJpwmu8uGN/3ZHEsLoH1i7PS1cEU2T4/Q2ImEMurbH5%2bpWcUDZbrsswO6EC36aqNplKqUdElj8cbv/wRfzSUOgD8H/2QpzAMsGDRvefu264CKTl%2boELH7hzzEwXEDZgAACLH/FacI0jOoyAGnBtjHW0N/AsUBbHNxxQgpdujBTOK/tGI9EUCncPLkyKhKS7GuQ4C9uSsGlKLwX7pnuyocaUeksZDAi8W2G1H5cNbRE8XgUVGe2J%2bD/U0cJ7ZTEhWJyfnpkLt%2b%2b7dZmAucxKwpSD0WoVMwwHvVxV0UHl5F8falaL0FtbK05xKAqHagoL0w45j3/sTo67I%2bVWfhId0VMPjzRa87ZplclrD5UzpwgUhYxrDeljq%2bydaSHbu7aE%2bU6cCuopwioYkvh%2bXk4ck1zCcA26rnH%2bBc0SUtSaWK%2bEduHyurStNTYitEqrmiXNRwWyxnqe4jS9ZQGxvlXer16H6MomengCd4FrQQ6n49FPKm%2bVBgNcdcqH%2b7Poq/TkQVLbzmG1v84/e/J4l05CvwL11CBu6XSZGJEf40qxfyExdGaF6lOGn29q4%2bNEVS48CAe83VuOKDGid8tI8hglGNaF106ItdwgVttHjTw1r7kEeJTj7mhiyFNGS7qDdvTsZ5IZwZkpUI6gU3xgNND4qeyv2f0MMFUw%2b5OK5vTzjOLvemIXYKBqPzbuxGPc%2bOEcbYHDHbOvPMuaRaXZWlVYiU1eBEfm9whNO0FwxZmiDohxYJnVwTAg%3d%3d"
    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62547&parId=9F999E057AD8C646!62390&authkey=!AkePW7UW1KXQkMM&app=Excel"
    urllib.request.urlretrieve(url, "datacovidChile/Covid Chile V2.xlsx")
    urllib.request.urlretrieve(url, "datacovidChile/CovidChileV2.xlsx")

    #url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62361&parId=9F999E057AD8C646!62390&authkey=!AgJICaWKd7tHakw&app=Excel"
    urllib.request.urlretrieve(url, "datacovidChile/Covid Chile V2a.xlsx")
    urllib.request.urlretrieve(url, "datacovidChile/CovidChileV2a.xlsx")

    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62377&parId=9F999E057AD8C646!62371&authkey=!Au8PrBa4C6_6k_M&app=Excel"
    urllib.request.urlretrieve(url, "datacovidhn/00 DATACOVID Trabajo_HN.xlsx")
    urllib.request.urlretrieve(url, "datacovidhn/00DATACOVIDTrabajo_HN.xlsx")

    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62380&parId=9F999E057AD8C646!62371&authkey=!Au8PrBa4C6_6k_M&app=Excel"
    urllib.request.urlretrieve(url, "datacovidhn/00 DATACOVID_HN_CUARENTENA.xlsx")
    urllib.request.urlretrieve(url, "datacovidhn/00DATACOVID_HN_CUARENTENA.xlsx")

    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62388&parId=9F999E057AD8C646!62371&authkey=!Au8PrBa4C6_6k_M&app=Excel"
    urllib.request.urlretrieve(url, "datacovidhn/ALIMENTACION_HN.xlsx")

    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62372&parId=9F999E057AD8C646!62371&authkey=!Au8PrBa4C6_6k_M&app=Excel"
    urllib.request.urlretrieve(url, "datacovidhn/Covid HN.xlsx")
    urllib.request.urlretrieve(url, "datacovidhn/CovidHN.xlsx")

    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62386&parId=9F999E057AD8C646!62371&authkey=!Au8PrBa4C6_6k_M&app=Excel"
    urllib.request.urlretrieve(url, "datacovidhn/FARMACIAS_HN.xlsx")

    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62378&parId=9F999E057AD8C646!62371&authkey=!Au8PrBa4C6_6k_M&app=Excel"
    urllib.request.urlretrieve(url, "datacovidhn/LOCALIZA HN.xlsx")
    urllib.request.urlretrieve(url, "datacovidhn/LOCALIZAHN.xlsx")

    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62384&parId=9F999E057AD8C646!62371&authkey=!Au8PrBa4C6_6k_M&app=Excel"
    urllib.request.urlretrieve(url, "datacovidhn/SALUD_HN.xlsx")

    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!62381&parId=9F999E057AD8C646!62371&authkey=!Au8PrBa4C6_6k_M&app=Excel"
    urllib.request.urlretrieve(url, "datacovidhn/Tabla_INSTALACIONES_Honduras_v1.xlsx")

    #Datos economicos
    #url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!63142&parId=9F999E057AD8C646!63151&authkey=!AkePW7UW1KXQkMM&app=Excel"
    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!63164&parId=9F999E057AD8C646!63151&authkey=!AkePW7UW1KXQkMM&app=Excel"
    urllib.request.urlretrieve(url, "datacovidChile/IndicadoresEconomicos/DOLAR_OBS_ADO.xlsx")

    #url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!63145&parId=9F999E057AD8C646!63151&authkey=!AkePW7UW1KXQkMM&app=Excel"
    url = "https://onedrive.live.com/edit.aspx?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!63164&parId=9F999E057AD8C646!63151&authkey=!AkePW7UW1KXQkMM&app=Excel"
    urllib.request.urlretrieve(url, "datacovidChile/IndicadoresEconomicos/ID_SERIE2.xlsx")

    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!63144&parId=9F999E057AD8C646!63151&authkey=!AkePW7UW1KXQkMM&app=Excel"
    urllib.request.urlretrieve(url, "datacovidChile/IndicadoresEconomicos/IGPA.xlsx")

    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!63143&parId=9F999E057AD8C646!63151&authkey=!AkePW7UW1KXQkMM&app=Excel"
    urllib.request.urlretrieve(url, "datacovidChile/IndicadoresEconomicos/IPSA.xlsx")

    url = "https://onedrive.live.com/download?cid=9f999e057ad8c646&page=view&resid=9F999E057AD8C646!63141&parId=9F999E057AD8C646!63151&authkey=!AkePW7UW1KXQkMM&app=Excel"
    urllib.request.urlretrieve(url, "datacovidChile/IndicadoresEconomicos/UF_IVP_DIARIO.xlsx")

    return
#************************************Actualizar Datos de la organizacion*******************************************
#************************************Actualizar Datos Productos avanzados*******************************************
def descargarProductos():
    archivos = [
                "producto19/CasosActivosPorComuna.csv",
                "producto20/NumeroVentiladores.csv",
                "producto21/SintomasHospitalizados.csv",
                "producto21/SintomasCasosConfirmados.csv",
                "producto24/CamasHospital_Diario.csv"
                ]
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/"
    for i in archivos:
        pd.read_csv(url + i).to_csv("Chile/MinCiencia/Productos/" + i.replace("/","-"), index=False)
    return
#************************************Actualizar Datos Productos avanzados*******************************************
#************************************Actualizar Datos Twiter*******************************************
def APITWEET():
    # Declaramos nuestras Twitter API Keys:
    keys = getKeys()
    #ACCESS_TOKEN = '1230251564616515586-2KqPsCG2mIJp3irRjENgHpCfQUxTUg'
    #ACCESS_TOKEN_SECRET = '6PJfMtYGY7w6csiIX9m1S5jFEKNZ3hE9PVkHKeN1S14iM'
    #CONSUMER_KEY = 'koO4XqTuWFr5ADGcE8kjIkVoU'
    #CONSUMER_SECRET = '3F4sk9qU8zbKBROuLPUUj1uvE2YuhseXPe0ahMQoivg4icN5bL'  
    ACCESS_TOKEN = keys['twitter']['token_acceso']
    ACCESS_TOKEN_SECRET = keys['twitter']['secreto_token_acceso']
    CONSUMER_KEY = keys['twitter']['clave_api']
    CONSUMER_SECRET = keys['twitter']['clave_secreta_api']
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api
#Desuso
def get_stuff(nombre=None):
    api = APITWEET()
    stuff = tweepy.Cursor(api.user_timeline, screen_name = nombre, include_rts = True)
    return stuff
#Desuso
def get_tweets(stuff, n):
    #for status in stuff.items(n):
        #print(status.created_at, status.author.screen_name, status.text)
        #print(status)
        #return status
    #return stuff.items(n)
    return list(stuff.items(n))
    #return stuff.page()

def FechaTweeter(palabra):
    anio = int(palabra[-4:])
    meses = {
        "Jan":1,
        "Feb":2,
        "Mar":3,
        "Apr":4,
        "May":5,
        "Jun":6,
        "Jul":7,
        "Aug":8,
        "Sep":9,
        "Oct":10,
        "Nov":11,
        "Dec":12
    }
    mes = meses[palabra[4:7]]
    dia = int(palabra[8:10])
    hora = int(palabra[11:13])
    minuto = int(palabra[14:16])
    segundo = int(palabra[17:19])
    return datetime.datetime(anio,mes,dia,hora,minuto,segundo) - datetime.timedelta(hours = 4)

def depurarFuenteTweet(palabra):
    salida = palabra.replace('<a href="https://about.twitter.com/products/tweetdeck" rel="nofollow">','').replace("</a>","")
    salida = salida.replace('<a href="http://twitter.com/download/iphone" rel="nofollow">',"")
    salida = salida.replace('<a href="https://studio.twitter.com" rel="nofollow">',"")
    salida = salida.replace('<a href="https://mobile.twitter.com" rel="nofollow">',"")
    salida = salida.replace('<a href="http://twitter.com" rel="nofollow">',"")
    return salida

def get_tweetConFecha(user, api = APITWEET()):
    return list(api.user_timeline(screen_name = user, count= 10))

def definirDatasetPorCuenta(cuenta):
#lista = get_tweetConFecha("colmedchile")
    lista = get_tweetConFecha(cuenta)
    salida = []
    for i in lista:  #get_tweetConFecha("colmedchile"):
        jsonObject = i._json.copy()
        datos = {
                    "Contenido" : jsonObject["text"],
                    "IR" : "https://twitter.com/i/web/status/" + jsonObject["id_str"],
                    "Fecha" : FechaTweeter(jsonObject["created_at"]).strftime("%d/%m/%Y %H:%M:%S"),
                    "Dispositivo" : depurarFuenteTweet(jsonObject["source"]),
                    "Likes" : jsonObject["favorite_count"],
                    "Retweets" : jsonObject["retweet_count"],
                    "Entidad" : jsonObject["user"]["name"],
                    "Hora" : FechaTweeter(jsonObject["created_at"]).strftime("%H:%M:%S"),
                    "Foto": jsonObject["user"]["profile_image_url"].replace("_normal.","."),
                    "FechaAux": FechaTweeter(jsonObject["created_at"])
                }
        salida.append(datos.copy())
    data = pd.DataFrame(salida)
    return data

def datasetFinalTweet():
    cuentas = [
                "colmedchile",
                "ministeriosalud",
                "opsoms",
                "ispch",
                "SuperDeSalud"
                ]
    salida = []
    for i in cuentas:
        salida.append(definirDatasetPorCuenta(i))
    data = pd.concat(salida)
    data = data.sort_values(by=['FechaAux'])
    del data["FechaAux"]
    data.to_csv("Twitter/Tweet.csv", index=False)
    return data


#tweepy.Cursor(api.search, q='#मराठी OR #माझाक्लिक OR #म')
#tweepy.Cursor(api.friends)
#tweepy.Cursor(api.home_timeline)
#tweepy.Cursor(api.search, url)
#tweepy.Cursor(api.friends, user_id=user_id, count=200).items()
#tweepy.Cursor(api.mentions_timeline, user_id=user_id, count=200).items()
#######https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
#************************************Actualizar Datos Twiter*******************************************
#************************************Actualizar Datos MinSal 3 carpetas*******************************************
def minSal3Carpeta():
    minsalud = [
        #InformeEpidemiologico
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/CasosActivosPorComuna.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/CasosActualesPorComuna.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/CasosAcumuladosPorComuna.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/CasosGeneroEtario.csv",
        #Se necesita hacer un buble por fecha
        #"https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/FechaInicioSintomas.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/SemanasEpidemiologicas.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/TasaDeIncidencia.csv",
        #Se necesita hacer un buble por fecha
        #"https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/FechaInicioSintomas_reportadosSEREMI.csv",
        #InformeSituacionCOVID19
        #"https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeSituacionCOVID19/HospitalizadosEtario_Acumulado_Post20200422.csv",
        #"https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeSituacionCOVID19/HospitalizadosGeneroEtario_Acumulado.csv",
        #"https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeSituacionCOVID19/HospitalizadosUCI_Acumulado.csv",
        #"https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeSituacionCOVID19/SintomasCasosConfirmados.csv",
        #"https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeSituacionCOVID19/SintomasHospitalizados.csv",
        #ReporteDiario
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/CamasHospital_Diario.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/FallecidosEtario.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/HospitalizadosUCIEtario.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/NumeroVentiladores.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/PCR.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/PCREstablecimiento.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/PacientesCriticos.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/PacientesVMI.csv",
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/UCI.csv"
        ]
    minsalud.append("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/" + datetime.datetime.now().strftime("%Y-%m-%d-FechaInicioSintomas.csv"))
    minsalud.append("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/" + datetime.datetime.now().strftime("%Y-%m-%d-FechaInicioSintomas_reportadosSEREMI.csv"))
    ruta = "Chile/MinCiencia/Input-minCiencia/"
    #print(datetime.now.strftime("%d %m %Y-"))
    #ruta = ""    2020-05-01-FechaInicioSintomas.csv
    for i in minsalud:
        #print(i)
        archivo = ruta + i.split("/")[-2] + "/" + i.split("/")[-1]
        try:
            data = pd.read_csv(i)    
            data.to_csv(archivo, index=False)
        except:
            print("Error en " + archivo)

    
        
    #url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/Cuarentenas/Cuarentenas-Geo.geojson"
    #urllib.request.urlretrieve(url, ruta + "Cuarentenas/Cuarentenas-Geo.geojson")
    #print(i.split("/")[-2] + "/" + i.split("/")[-1])
#************************************Actualizar Datos MinSal 3 carpetas*******************************************
#************************************Analisis Twitter*******************************************
def authenticate_client():
    key = "3f6e681ce10c430fadc5fa12b5899774"
    endpoint = "https://tweetstopowerbi8.cognitiveservices.azure.com/"
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

def sentiment_analysis_example(client = authenticate_client()):
    data = pd.read_csv("Twitter/Tweet.csv")
    Entidad = list(data.Entidad)
    documents = list(data.Contenido)
    #print(len(client.analyze_sentiment(documents = documents, language="es")))
    #response = client.analyze_sentiment(documents = documents, language="es")[0]
    response = client.analyze_sentiment(documents = documents, language="es")
    salida = []
    for i in range(len(documents)):
        aux = {
                "Entidad" : Entidad[i],
                "Contenido" : documents[i],
                "Sentimiento" : response[i].sentiment,
                "Positivo" : response[i].confidence_scores.positive,
                "Neutral" : response[i].confidence_scores.neutral,
                "Negativo" : response[i].confidence_scores.negative,
                "LargoTexto" : len(documents[i])
                }
        salida.append(aux.copy())
    dataSalida = pd.DataFrame(salida)
    return dataSalida

def guardarAnalisisTwitter():
    sentiment_analysis_example().to_csv("AnalisisTweet.csv", index=False)
    return
#************************************Analisis Twitter*******************************************

