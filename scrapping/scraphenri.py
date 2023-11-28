import time
import requests
from lxml import html
import pandas as pd
from selenium import webdriver

def get_page_content(url, wait_time=10):
    # Utiliser Selenium pour laisser le temps à la page de charger
    driver = webdriver.Chrome()
    driver.get(url)

    # Attendre que la page se charge
    time.sleep(wait_time)

    # Utiliser requests pour obtenir le contenu de la page après le chargement
    page_content = driver.page_source

    # Fermer le navigateur Selenium
    driver.quit()

    return page_content

def scrape_return_stats(year):
    # Construire l'URL avec l'année spécifiée
    url = f'https://www.atptour.com/en/stats/leaderboard?boardType=return&timeFrame={year}&surface=all&versusRank=all&formerNo1=false'

    # Obtenir le contenu de la page
    content = get_page_content(url)

    # Utiliser lxml pour créer un objet ElementTree à partir du contenu de la page
    tree = html.fromstring(content)

    # Utiliser l'XPath pour extraire le tableau
    table = tree.xpath('//div[@id="statsListingTableContent"]/table')[0]



    data = []
    for row in table.xpath('.//tbody//tr'):
        player_name_elements = row.xpath('.//td[2]/div/a[@class="stats-player-name"]/text()')
        player_name = player_name_elements[0].strip() if player_name_elements else 'N/A'
        
        # Extraire les autres données de la ligne
        row_data = [player_name] + [td.text.strip() if td.text else '' for td in row.xpath('.//td')[1:]]  # Ajouter le nom du joueur en première colonne
        #print("Row data:", row_data)
        data.append(row_data)

    # Créer un DataFrame Pandas
    df = pd.DataFrame(data, columns = ['Name',' ','Return Rating','% 1 Serve Return Points Won','% 2nd Serve Return Points Won','% Return Games Won','% Break Points Converted'])
    df['Year'] = year


    return df

# Utilisation de la fonction pour l'année 2022
scrape_return_stats(2022)
