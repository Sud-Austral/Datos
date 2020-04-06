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
