import requests
from bs4 import BeautifulSoup
from datetime import datetime

partidas = {}

#PEGA TODAS AS PARTIDAS DA COPA DOMUNDO E O HORARIO DE CADA UM
def getPartidas():
    page = requests.get('https://www.futeboleiro.com/copa-do-mundo-2022/calendario/')
    soup = BeautifulSoup(page.content, 'html.parser')
    
    divPartidas = soup.find_all("div", class_="games-overview-table__container")
    #print(divPartidas)
    for divPartida in divPartidas[0]:
        #print('--------', divPartida)
        for i, partida in enumerate(divPartida.find_all("div", class_="wp-block-e2-games-overview-table-row games-overview-table__row grid__container")):
            #print(partida.prettify())
            dateTime = partida.find("div", attrs={'class': 'games-overview-table__date date-time'}).text.split('–')
            data = dateTime[0].split("/")
            hora = dateTime[1].split(':')
            data = datetime(int(data[2]), int(data[1]), int(data[0]), int(hora[0]), int(hora[1]))
            if i == 0:
                partida = partida.find("div", attrs={'class': 'games-overview-table__teams'}).text.split(' – ')           
                partida_renamed = f'{partida[0]} vs {partida[1]}'
                partidas[i] = {'selecoes': partida_renamed, 'horario': data}
            else:
                partidas[i] = {'selecoes': partida.find("div", attrs={'class': 'games-overview-table__teams'}).text, 'horario': data}
                
    return partidas
    

