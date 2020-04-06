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
