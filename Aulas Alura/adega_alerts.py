import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
import config



chave_primaria = "8115785474:AAHDHDn9J7d1iXFbfXAA0qYexsDFk27pAFM"
CHAT_ID = "Grupo a ser criado"


# Conexão com o MongoDB

client = MongoClient("mongodb://localhost:27017/")
db = client('adega-alerts')
ofertas = db['Ofertas papai']

# Aqui ele vai buscar as ofertas de cada produto 

def busca_ofertas(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,'html.parser')
    resultados = []
    for item in soup.select('.produto-promo'):
        nome = item.select_one('.nome').get_text(strip=True)
        preco = float(item.select_one('.preco').get_text(strip=True).replace('R$','').replace(',','.'))
        link = item.select_one('a')['href']
        resultados.append({'nome': nome,'preco': preco, 'link': link})
    return resultados


# Ele valida as novas ofertas se ja estão dentro das outras enviadas anteriormente

def processar_ofertas_new(ofertas_novas):
    bot = Bot(token=config.chave_primaria)
    for oferta in ofertas_novas:
        existe = ofertas.find_one({'link': oferta['link'],'preco': oferta['preco']})
        if not existe:
            ofertas.insert_one(oferta)
            mensagem = f'{oferta['nome']}\n R$ {oferta['preco']:.2f}n\ {oferta['link']}'
            bot.send_message(chat_id=config.CHATID, text=mensagem, parse_mode="Markdown")

# Ele cria uma variavel para rodar as tarefas a cada hora

def tarefa():
    urls = ["https://site1.com/promocoes", "https://site2.com/descontos"]
    todas = []
    for url in urls:
        todas += busca_ofertas(url)
    processar_ofertas_new(todas)

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tarefa, 'interval',minutes=60)
    print('Iniciando a Agenda do Job')
    scheduler.start()