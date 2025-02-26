import time
from time import sleep

from gspread import service_account
from lxml.etree import XPath
from pyasn1.debug import scope
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.expected_conditions import WebDriverOrWebElement
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import gspread
from oauth2client.service_account import ServiceAccountCredentials

url = 'https://www.superprof.com.br/'
clicar_opcoes = '//*[@id="sp-vue-container"]/header/div[1]/div[2]/div/div'
clicar_conectar = '//*[@id="sp-vue-container"]/header/div[4]/div[2]/div[3]/div[1]/div/div[1]/span'

def setup_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    return driver

def setup_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name( r'C:\Users\gusta\OneDrive\Desktop\Projeto Python\Analise_Investidor_Inteligente\Automações\original-glider-450303-c3-4d8504f3c3fa.json',scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key('1uNzIGfIR336MTSPrtav4WgUAaDeDIlsYps-hu-sGIW0').sheet1
    return  sheet


def extract_data(driver,url,clicar_opcoes,clicar_conectar):
    driver.get(url)
    try:
        primeiro_elemento = WebDriverWait(driver,10,poll_frequency=0.5).until(
            EC.element_to_be_clickable((By.XPATH,clicar_opcoes))
        )
        primeiro_elemento.click()
        time.sleep(2)
        print('Clicado com Sucesso nos 3 tracinhos')
        segundo_elemento = WebDriverWait(driver,10,poll_frequency=0.5).until(
            EC.element_to_be_clickable((By.XPATH,clicar_conectar))
        )
        segundo_elemento.click()
        print('Clicado com Sucesso em Conectar')
    except TimeoutException as e:
        print('Não foi possivel clicar em algo')
    except Exception as e:
        print(f'Ocorreu um erro: {str(e)}')


    title = driver.title
    return [url,title]

if __name__ == '__main__':
    driver = setup_driver()
    try:
        data = extract_data(driver,url,clicar_opcoes,clicar_conectar)
        print('Clicou em Conectar')
    except Exception as e:
        print(f'Ocorreu um erro: {str(e)}')

    while True:
        time.sleep(1) 


### só teste
