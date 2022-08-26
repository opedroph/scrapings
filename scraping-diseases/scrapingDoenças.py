from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import csv


#se nao tiver funcionando troca para ../chromedriver.exe abaixo
navegador = webdriver.Chrome(executable_path='chromedriver.exe')
urlBase = 'https://www.fleury.com.br'
allLinksDiseases = []
diseases = []
header = ['name', 'symptoms']

def getDiseasesLinks():
    numberPage = 1
    try:
        while numberPage <= 3: #o certo seria fazer isso pra ele funcionar em quantas paginas tivessem sem previsa fornecer o numero, but ok
            url = urlBase+'/manual-de-doencas?limit=50&page='+str(numberPage)
            navegador.get(url)
            sleep(3) #o site por algum motivo carrega sempre uma pagina antes de atualizar, por isso o sleep
            html = BeautifulSoup(navegador.page_source, 'html.parser')
            ulDiseases = html.find('ul',attrs={'id':'list-text-list-page'})
            tagADisiases = ulDiseases.findAll('a')
            for i in tagADisiases:
                allLinksDiseases.append(i.get('href'))
            numberPage+=1
    except:
        print('erro')



def gettingDiseases(): #belo nome 
    for disiase in allLinksDiseases:
        navegador.get(urlBase+disiase)
        sleep(3) 
        html = BeautifulSoup(navegador.page_source, 'html.parser')
        name = html.find('h1', attrs={'class':'typographycomponentstyle__H1-sc-1oox73n-1 fRLjlH'}).text
        symptoms = html.find('p', attrs={'class':'typographycomponentstyle__Body-sc-1oox73n-8 zFBaQ'}).text
        diseases.append({'name':name, 'symptoms':symptoms})





    
def getDataDiseases(): 
    
    getDiseasesLinks()
    gettingDiseases()

    with open('diseasesList.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = header)
        writer.writeheader()
        writer.writerows(diseases) 
                                             
    


getDataDiseases()



