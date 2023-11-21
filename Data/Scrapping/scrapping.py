from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd


#cService = webdriver.ChromeService(executable_path='/Users/maloevain/Desktop/ENSAE2/S1/python/Projet/chromedriver')
#driver = webdriver.Chrome(service = cService)

"""*******************************************************************************************************************"""

"""On commence par créer une liste des meilleurs serveurs de tous les temps"""

cService = webdriver.ChromeService(executable_path='/Users/maloevain/Desktop/ENSAE2/S1/python/Projet/chromedriver')
driver = webdriver.Chrome(service = cService)

driver.get('https://www.atptour.com/en/stats/service-games-won')
players=driver.find_elements(By.XPATH, '//tr[@class="stats-listing-row"]')

meilleurs_serveurs_alltime = []

for serveur in players:

    serveur_info_elements = serveur.find_elements(By.XPATH, './/td')

    serveur_info = ['all time']

    for i in range(4,len(serveur_info_elements)):
        serveur_info.append(serveur_info_elements[i].text)

    meilleurs_serveurs_alltime.append(serveur_info)

driver.quit()

"""*******************************************************************************************************************"""

"On va ensuite récolter les informations des meilleurs serveurs sur chaque année depuis 1991"


serveur_list_1991_2022=[]

for year in range(2016,2023):

    cService = webdriver.ChromeService(executable_path='/Users/maloevain/Desktop/ENSAE2/S1/python/Projet/chromedriver')
    driver = webdriver.Chrome(service = cService)

    url= 'https://www.atptour.com/en/stats/service-games-won/{}/all/all/'.format(year)
    driver.get(url)

    players=driver.find_elements(By.XPATH, '//tr[@class="stats-listing-row"]')

    serveurs_list=[]

    for serveur in players:

        serveur_info_elements = serveur.find_elements(By.XPATH, './/td')

        serveur_info = [year]

        for i in range(4,len(serveur_info_elements)):
            serveur_info.append(serveur_info_elements[i].text)


        serveur_list_1991_2022.append(serveur_info)

    driver.quit()


df=pd.DataFrame(serveur_list_1991_2022+meilleurs_serveurs_alltime,columns=["year","Name","Percentage","Games Won","Totale Games","Matches"])

print(df.head())
print(df.tail())
df.to_csv('serveur_list')
