from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
import re, sys, random
import numpy as np

import pandas as pd

USER_AGENT = {
    0:"Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
    1:"Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
    2:"Mozilla/5.0 (Linux; Android 10; SM-G980F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.96 Mobile Safari/537.36",
    3:"Mozilla/5.0 (Linux; Android 9; SM-G973U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    4:"Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
    5:"Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
    6:"Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36",
    7:"Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
    8:"Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36",
    9:"Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
    10:"Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
    11:"Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    12:"Mozilla/5.0 (Linux; Android 11; Pixel 5 Build/RQ3A.210805.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36",
    13:"Mozilla/5.0 (Linux; Android 10; Google Pixel 4 Build/QD1A.190821.014.C2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
    14:"Mozilla/5.0 (Linux; Android 10; Google Pixel 4 Build/QD1A.190821.014.C2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
    15:"Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 Build/OPD1.170811.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",
    16:"Mozilla/5.0 (Linux; Android 7.1.1; Google Pixel Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/54.0.2840.85 Mobile Safari/537.36",
    17:"Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
    18:"Mozilla/5.0 (Linux; Android 9; J8110 Build/55.0.A.0.552; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36",
    19:"Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",
    20:"Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
    21:"Mozilla/5.0 (Linux; Android 10; HTC Desire 21 pro 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36",
    22:"Mozilla/5.0 (Linux; Android 10; Wildfire U20 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36",
    23:"Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36"
}

factibilidad_entel = 'https://www.entel.cl/validaform/?id=rev_fact_home'

# Constantes
DELAY = 5
REGIONES = {
    "TARAPACA":1,
    "ANTOFAGASTA":2,
    "ATACAMA":3,
    "COQUIMBO":4,
    "VALPARAISO":5,
    "LIBERTADOR GENERAL BERNARDO OHiGGINS":6,
    "MAULE":7,
    "BIO BIO": 8,
    "ARAUCANIA":9,
    "LOS LAGOS":10,
    "AISEN DEL GENERAL CARLOS IBANES DEL CAMPO":11,
    "MAGALLANES Y DE LA ANTARTICA CHILENA":12,
    "METROPOLITANA DE SANTIAGO":13,
    "LOS RIOS":14,
    "ANTARTICA Y PARINACOTA":15
}

NUMEROS = {
    "1":"UNO",
    "10":"DIEZ",
    "11":"ONCE",
    "12":"DOCE",
    "13":"TRECE",
    "14":"CATORCE",
    "2":"DOS",
    "20":"VEINTE",
    "21":"VEINTIUNO",
    "3":"TRES",
    "4":"CUATRO"
}

TELEFONO = "987654321"
try:
    INDEX = int(sys.argv[1])
except IndexError:
    INDEX = 0
# Leer el documento
R = pd.read_csv(sys.argv[3])

# Limpieza y ajuste de datos
pattern = re.compile("[a-zA-Z0-9].*")
R["DIRECCION"] = R["DIRECCION"].map(lambda x: x.replace("PJE", "PASAJE"))
R["DIRECCION"] = R["DIRECCION"].map(lambda x: x.replace("DR", "DOCTOR"))
R["DIRECCION"] = R["DIRECCION"].map(lambda x: x.replace("-", " "))
R["DIRECCION"] = R["DIRECCION"].map(lambda x: x.replace("AV", ""))
for i in range(max([int(i) for i in NUMEROS.keys()])):
    R["DIRECCION"] = R["DIRECCION"].map(lambda x: x.replace(str(i), NUMEROS.get(i, str(i))))
R["DIRECCION"] = R["DIRECCION"].map(lambda x: re.sub("\([a-zA-Z0-9].+\)", '', x).strip())
R["DIRECCION"] = R["DIRECCION"].map(lambda x: re.sub("CASA [a-zA-Z0-9].*\)", '', x).strip())


R["FACTIBILIDAD"] = np.nan
for i in range(INDEX, len(R)):
    driver = webdriver.Firefox(service=Service(sys.argv[5]))
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", USER_AGENT[random.randint(0,23)])
    driver.get(factibilidad_entel)

    region_select = REGIONES[sys.argv[2]]
    comuna = R["REGION"][i]
    calle = R["DIRECCION"][i]
    numero = R["NUMERO"][i]

    print("Index:", i, end=": ")
        
    # Opción REFION
    select_region = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.ID, 'selReg')))#"//input[@type='email']")))
    select_region = Select(select_region)
    select_region.select_by_value(str(region_select))

    # COMUNA
    input_com = driver.find_element(By.ID, "inputSelCom")
    driver.execute_script("arguments[0].style.display = 'block';",input_com)
    for l in comuna:
        sleep(0.1)
        input_com.send_keys(l)

    first_option = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, f'//div[text()="{comuna}"]')))
    WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable(first_option)).click()

    # DIRECCION
    input_calle = WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable(driver.find_element(By.ID, 'selDir')))
    for l in calle:
        sleep(0.1)
        input_calle.send_keys(l)

    try:
        first_option = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, f'//div[text()="{calle}"]')))
        WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable(first_option)).click()
    except TimeoutException:
        print("No se pudo ubicar la dirección")
        print("Sin factibilidad")
        R["FACTIBILIDAD"].loc[i] = "SIN FACTIBILIDAD"
        R.to_csv(sys.argv[4])
        continue
        
        

    # NUMERO
    input_numero = WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable(driver.find_element(By.ID, 'selNum')))
    for l in numero:
        sleep(0.1)
        input_numero.send_keys(l)

    try:
        first_option = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, f'//div[text()="{numero}"]')))
        WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable(first_option)).click()
    except TimeoutException:
        print("No se pudo ubicar el número")
        print("Sin factibilidad")
        R["FACTIBILIDAD"].loc[i] = "SIN FACTIBILIDAD"
        R.to_csv("FACTIBILIDAD.csv")
        continue

    input_telefono = WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable(driver.find_element(By.ID, 'numcontact')))
    for l in TELEFONO:
        sleep(0.1)
        input_telefono.send_keys(l)


    submit_button = driver.find_element(By.ID, 'buttonDireccion')
    submit_button.click()

    try:
        WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.ID, 'jqPlanes_Mono_I')))
        print("Factibilidad")
        R["FACTIBILIDAD"].loc[i] = "CON FACTIBILIDAD"
        R.to_csv("FACTIBILIDAD.csv")
        continue
    except TimeoutException:
        print("No se encontró elemento 'jqPlanes_Mono_I' (Factibilidad)")

    try:
        WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, f'//p[contains(@class, "title-PantallaError")]')))
        print("Sin Factibilidad")
        R["FACTIBILIDAD"].loc[i] = "SIN FACTIBILIDAD"
        R.to_csv("FACTIBILIDAD.csv")
    except TimeoutException:
        print("No se encontró el elemento '//p[contains(@class, \"title-PantallaError\")]' (Sin factibilidad)")
        R["FACTIBILIDAD"].loc[i] = "ERROR (Im not perfect sweety)"
    driver.quit()
    if i % 10 == 0:
        sleep(2.5)
