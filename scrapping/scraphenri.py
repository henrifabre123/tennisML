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

   # Utiliser un sélecteur XPath différent pour extraire les en-têtes de colonnes
    headers = [th.text.strip() if th.text else '' for th in table.xpath('.//thead//th[contains(@id, "Link")]/div[@class="sorting-inner"]/div[@class="sorting-label"]')]
    print(headers)

    # Extraire les données du tableau
    data = []
    for row in table.xpath('.//tbody//tr'):
        row_data = [td.text.strip() if td.text else '' for td in row.xpath('.//td')]
        print("Row data:", row_data)
        data.append(row_data)

    # Créer un DataFrame Pandas
    df = pd.DataFrame(data, columns=headers)



    return df

# Utilisation de la fonction pour l'année 2022
scrape_return_stats(2022)
