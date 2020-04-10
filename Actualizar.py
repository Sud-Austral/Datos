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
#from datetime import datetime
#************************************Actualizar Database**************************************************
def UpdateDatabase():
    print("Comenzo...")
    try:
        minsal()
        print("Minsal completo...")
    except:
        print("Error a cargar a Minsal")
    try:
        Farmacias()
        print("Farmacias completo...")
    except:
        print("Error a cargar a Farmacias")
    try:
        Chile()    
        print("Chile completo...")
    except:
        print("Error a cargar a Chile")
    try:
        johnsHopkinsCovid19Diario()
        print("Hopkins diario completo...")
    except:
        print("Error a cargar a Hopkins diario")
    try:
        johnsHopkinsCovid19Series()
        print("Hopkins serie (acumulado) completo...")
    except:
        print("Error a cargar a Hopkins Serie")
    try:
        ecdcEuropa()
        print("ECDC Europa completo...")
    except:
        print("Error a cargar a Hopkins Serie")
    try:
        worldometersInfo()
        print("WORLDMETER completo...")
    except:
        print("Error a cargar a Hopkins Worldmeter")
    try:
        ourWorldInData()
        print("OurWorldInData completo...")
    except:
        print("Error a cargar a Hopkins OurWorldInData")
    try:
        EarlyAlert()
        print("EarlyAlert completo...")
    except:
        print("Error a cargar a Hopkins EarlyAlert")
    try:
        KoBoToolbox()
        print("KoBoToolbox completo...")
    except:
        print("Error a cargar a KoBoToolbox") 
    return
#************************************Actualizar Database**************************************************

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
    repoLocal = git.Repo('C:/Users/limc_/Documents/GitHub/Datos')
    print(repoLocal.git.status())
    
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
    os.remove('Chile/covid19_chile.xlsx')
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
    data.to_csv("EarlyAlert/Current_Coronavirus_Cases_and_Deaths." + now.strftime("%d-%m-%Y_%H-%M-%S") + "csv", index=False)
    
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
    data.to_csv("ecdc.europa/ecCurrent_Coronavirus_Cases_and_Deaths." + now.strftime("%d-%m-%Y_%H-%M-%S") + "csv", index=False)
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
        "Apr" : 4
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
    data = pd.read_html(response.content)
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
                "share-of-the-population-that-is-70-years-and-older.csv"      
                ]
    ruta = "C:/Users/limc_/Downloads/"
    try:
        for i in archivos:
            remove(ruta + i)
        """
        remove("C:/Users/limc_/Downloads/covid-19-total-confirmed-cases-vs-total-tests-conducted.csv")
        remove("C:/Users/limc_/Downloads/total-deaths-covid-19.csv")
        remove("C:/Users/limc_/Downloads/covid-19-tests-country.csv")
        remove("C:/Users/limc_/Downloads/total-daily-covid-deaths-per-million.csv")
        remove("C:/Users/limc_/Downloads/total-cases-covid-19.csv")
        remove("C:/Users/limc_/Downloads/total-and-daily-cases-covid-19.csv")
        remove("C:/Users/limc_/Downloads/daily-cases-covid-19.csv")
        remove("C:/Users/limc_/Downloads/physicians-per-1000-people.csv")
        remove("C:/Users/limc_/Downloads/hospital-beds-per-1000-people.csv")
        remove("C:/Users/limc_/Downloads/share-of-the-population-that-is-70-years-and-older.csv")
        """
    except:
        pass
    download_folder = "C:/Users/limc_/Documents/GitHub/Datos"
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
    time.sleep(5)   
    driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div[2]/button").click()
    driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div/nav/ul/li[2]/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
    time.sleep(1)
    """
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
    #ruta = "C:/Users/limc_/Downloads/"
    folder = "C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/"
    for i in archivos:
        shutil.copy(ruta + i, folder + now.strftime("%d-%m-%Y_%H-%M-%S") + i)
        shutil.copy(ruta + i, folder  + i)
        verificarColumnas(pd.read_csv(folder  + i),i)
        
    """
    shutil.copy('C:/Users/limc_/Downloads/full-list-total-tests-for-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/full-list-total-tests-for-covid-19' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/full-list-total-tests-for-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/full-list-total-tests-for-covid-19.csv')
    
    shutil.copy('C:/Users/limc_/Downloads/total-deaths-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-deaths-covid-19' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/total-deaths-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-deaths-covid-19.csv')
    
    shutil.copy('C:/Users/limc_/Downloads/covid-19-tests-country.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/covid-19-tests-country' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/covid-19-tests-country.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/covid-19-tests-country.csv')


    shutil.copy('C:/Users/limc_/Downloads/total-daily-covid-deaths-per-million.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-daily-covid-deaths-per-million' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/total-daily-covid-deaths-per-million.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-daily-covid-deaths-per-million.csv')

    shutil.copy('C:/Users/limc_/Downloads/total-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-cases-covid-19' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/total-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-cases-covid-19.csv')

    shutil.copy('C:/Users/limc_/Downloads/total-and-daily-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-and-daily-cases-covid-19' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/total-and-daily-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-and-daily-cases-covid-19.csv')


    shutil.copy('C:/Users/limc_/Downloads/daily-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/daily-cases-covid-19' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/daily-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/daily-cases-covid-19.csv')

    shutil.copy('C:/Users/limc_/Downloads/physicians-per-1000-people.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/physicians-per-1000-people' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/physicians-per-1000-people.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/physicians-per-1000-people.csv')

    shutil.copy('C:/Users/limc_/Downloads/hospital-beds-per-1000-people.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/hospital-beds-per-1000-people' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/hospital-beds-per-1000-people.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/hospital-beds-per-1000-people.csv')

    shutil.copy('C:/Users/limc_/Downloads/share-of-the-population-that-is-70-years-and-older.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/share-of-the-population-that-is-70-years-and-older' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/share-of-the-population-that-is-70-years-and-older.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/share-of-the-population-that-is-70-years-and-older.csv')
    """
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
    ruta = "Chile/MinCiencia/"
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/Covid-19.csv"
    data = realizarColumna(pd.read_csv(url),3)
    data.to_csv(ruta + "Principal.csv", index=False)

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv"
    data = realizarColumna(pd.read_csv(url),3)
    data.to_csv(ruta +"Producto1.csv", index=False)

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

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv"
    data = realizarColumnaParticular(pd.read_csv(url),"Region")
    data.to_csv(ruta +"Producto3.csv", index=False)

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

    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/recuperados.csv"
    data = realizarColumnaParticular(pd.read_csv(url),"Fecha")
    #data["Estado"] = data["Fecha"]
    del data["Fecha"]

    data.to_csv(ruta +"Producto5.csv", index=False)
    return








#*********************************Metodos ASYNCRONOS ***********************************************************
#************************************ASYNC Actualizar Chile*****************************************************
def ChileASYNC():
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

#************************************ASYNC Actualizar Chile*****************************************************

#************************************ASYNC Actualizar EarlyAlert************************************************
def EarlyAlertASYNC():
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
    data.to_csv("EarlyAlert/Current_Coronavirus_Cases_and_Deaths." + now.strftime("%d-%m-%Y_%H-%M-%S") + "csv", index=False)
    
    guardarRepositorio()
    return
#************************************ASYNC Actualizar EarlyAlert************************************************

#************************************ASYNC Actualizar ecdcEuropa************************************************
def ecdcEuropaASYNC():
    now = datetime.datetime.now()
    url= "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"
    data = pd.read_csv(url)
    data.to_csv("ecdc.europa/Current_Coronavirus_Cases_and_Deaths.csv", index=False)
    data.to_csv("ecdc.europa/ecCurrent_Coronavirus_Cases_and_Deaths." + now.strftime("%d-%m-%Y_%H-%M-%S") + "csv", index=False)
    guardarRepositorio()
    return
#************************************ASYNC Actualizar ecdcEuropa************************************************

#************************************ASYNC Actualizar johnsHopkins**********************************************
#DATO DIARIO
def johnsHopkinsCovid19DiarioASYNC(): 
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
    ultimo.to_csv("Johns_Hopkins-covid19/diario/ultimoRegistro.csv", index=False)
    guardarRepositorio()
    return
#DATO SERIE
def johnsHopkinsCovid19SeriesASYNC():
    
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
   
    merged_left.to_csv("Johns_Hopkins-covid19/series/acumulado.csv", index=False)


    guardarRepositorio()
    return
#************************************Actualizar johnsHopkins*********************************************
#************************************Actualizar worldmeter***********************************************


def worldometersInfoASYNC():
    url  = 'https://www.worldometers.info/coronavirus/'
    response = requests.get(url)
    #print(response.content)
    data = pd.read_html(response.content)
    data_hoy = data[0]     #.to_csv("worldometers.csv", index=False)

    data_aux = pd.read_csv("worldometers.info/Historico/worldometers.csv")
    for i in data_aux.columns[1:10]:
        del data_aux[i]

    merged_left = pd.merge(left=data_hoy, right=data_aux, how='left', left_on='Country,Other', right_on='Country,Other')
    merged_left.to_csv("worldometers.info/worldometers.csv", index=False)

    url  = 'https://www.worldometers.info/world-population/population-by-country/'
    response = requests.get(url)
    #print(response.content)
    data = pd.read_html(response.content)[0]

    data.to_csv("worldometers.info/Poblacion/worldometersPoblacion.csv", index=False)
    
    guardarRepositorio()
    return
#************************************Actualizar worldmeter***********************************************
#************************************KoBoToolbox*********************************************************
def KoBoToolboxASYNC():
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
def ourWorldInDataASYNC():
    now = datetime.datetime.now()
    try:
        remove("C:/Users/limc_/Downloads/tests-vs-confirmed-cases-covid-19.csv")
        remove("C:/Users/limc_/Downloads/total-deaths-covid-19.csv")
        remove("C:/Users/limc_/Downloads/covid-19-tests-country.csv")
        remove("C:/Users/limc_/Downloads/total-daily-covid-deaths-per-million.csv")
        remove("C:/Users/limc_/Downloads/total-cases-covid-19.csv")
        remove("C:/Users/limc_/Downloads/total-and-daily-cases-covid-19.csv")
        remove("C:/Users/limc_/Downloads/daily-cases-covid-19.csv")
        remove("C:/Users/limc_/Downloads/physicians-per-1000-people.csv")
        remove("C:/Users/limc_/Downloads/hospital-beds-per-1000-people.csv")
        remove("C:/Users/limc_/Downloads/share-of-the-population-that-is-70-years-and-older.csv")
    except:
        pass
    download_folder = "C:/Users/limc_/Documents/GitHub/Datos"
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
    time.sleep(5)   
    driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div[2]/button").click()
    driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div/nav/ul/li[2]/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
    time.sleep(1)

    """
    driver.get("https://ourworldindata.org/grapher/covid-19-tests-country")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div/nav/ul/li[2]/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
    time.sleep(1)
    """
    #*********************************************Con mapa sin mapa***********************************************
    driver.get("https://ourworldindata.org/grapher/covid-19-tests-country")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
    time.sleep(1) 
    driver.get("https://ourworldindata.org/grapher/total-deaths-covid-19")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
    time.sleep(1) 

    driver.get("https://ourworldindata.org/grapher/total-daily-covid-deaths-per-million")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
    time.sleep(1) 

    driver.get("https://ourworldindata.org/grapher/total-cases-covid-19")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
    time.sleep(1)  

    driver.get("https://ourworldindata.org/grapher/total-and-daily-cases-covid-19")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
    time.sleep(1)  

    driver.get("https://ourworldindata.org/grapher/daily-cases-covid-19")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
    time.sleep(1)  

    driver.get("https://ourworldindata.org/grapher/physicians-per-1000-people")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
    time.sleep(1)  

    driver.get("https://ourworldindata.org/grapher/hospital-beds-per-1000-people")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
    time.sleep(1)  

    driver.get("https://ourworldindata.org/grapher/share-of-the-population-that-is-70-years-and-older")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[3]/div[2]/nav/ul/li[3]/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/figure/div/div[4]/div/a").click()
    time.sleep(1)  



    driver.close()

    shutil.copy('C:/Users/limc_/Downloads/tests-vs-confirmed-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/tests-vs-confirmed-cases-covid-19' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/tests-vs-confirmed-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/tests-vs-confirmed-cases-covid-19.csv')
    shutil.copy('C:/Users/limc_/Downloads/total-deaths-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-deaths-covid-19' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/total-deaths-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-deaths-covid-19.csv')
    shutil.copy('C:/Users/limc_/Downloads/covid-19-tests-country.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/covid-19-tests-country' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/covid-19-tests-country.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/covid-19-tests-country.csv')


    shutil.copy('C:/Users/limc_/Downloads/total-daily-covid-deaths-per-million.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-daily-covid-deaths-per-million' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/total-daily-covid-deaths-per-million.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-daily-covid-deaths-per-million.csv')

    shutil.copy('C:/Users/limc_/Downloads/total-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-cases-covid-19' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/total-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-cases-covid-19.csv')

    shutil.copy('C:/Users/limc_/Downloads/total-and-daily-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-and-daily-cases-covid-19' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/total-and-daily-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/total-and-daily-cases-covid-19.csv')


    shutil.copy('C:/Users/limc_/Downloads/daily-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/daily-cases-covid-19' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/daily-cases-covid-19.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/daily-cases-covid-19.csv')

    shutil.copy('C:/Users/limc_/Downloads/physicians-per-1000-people.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/physicians-per-1000-people' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/physicians-per-1000-people.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/physicians-per-1000-people.csv')

    shutil.copy('C:/Users/limc_/Downloads/hospital-beds-per-1000-people.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/hospital-beds-per-1000-people' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/hospital-beds-per-1000-people.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/hospital-beds-per-1000-people.csv')

    shutil.copy('C:/Users/limc_/Downloads/share-of-the-population-that-is-70-years-and-older.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/share-of-the-population-that-is-70-years-and-older' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv")
    shutil.copy('C:/Users/limc_/Downloads/share-of-the-population-that-is-70-years-and-older.csv', 'C:/Users/limc_/Documents/GitHub/Datos/ourworldindata.org/share-of-the-population-that-is-70-years-and-older.csv')

    guardarRepositorio()
    return
#************************************Actualizar ourWorldInData*******************************************
