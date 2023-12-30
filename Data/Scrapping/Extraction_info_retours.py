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
    # URL de la page
    url = f'https://www.atptour.com/en/stats/leaderboard?boardType=return&timeFrame={year}&surface=all&versusRank=all&formerNo1=false'

    # Obtenir le contenu de la page
    content = get_page_content(url)

    # Parser le contenu de la page
    tree = html.fromstring(content)

    # Sélectionner le tableau des statistiques
    table = tree.xpath('//div[contains(@class, "leaderboard")]//table')[0]

    # Extraire les données
    data = []
    for row in table.xpath('.//tbody/tr'):
        # Extraire le rang, le nom du joueur et les statistiques
        rank = row.xpath('.//td[1]/text()')[0].strip()
        player_name = row.xpath('.//td[2]//div[@class="name"]/text()')[0].strip()
        stats = [td.text.strip() for td in row.xpath('.//td[position()>2]')]

        # Ajouter les données à la liste
        data.append([rank, player_name] + stats)

    # Créer un DataFrame
    columns = ['Rank', 'Name', 'Return Rating', '% 1st Serve Return Points Won', '% 2nd Serve Return Points Won', '% Return Games Won', '% Break Points Converted']
    df = pd.DataFrame(data, columns=columns)
    df['Year'] = year

    return df


def scrape_pressure_stats(year):
    # Construire l'URL avec l'année spécifiée
    url = f'https://www.atptour.com/en/stats/leaderboard?boardType=pressure&timeFrame={year}&surface=all&versusRank=all&formerNo1=false'
   # Obtenir le contenu de la page
    content = get_page_content(url)

    # Parser le contenu de la page
    tree = html.fromstring(content)

    # Sélectionner le tableau des statistiques
    table = tree.xpath('//div[contains(@class, "leaderboard")]//table')[0]

    # Extraire les données
    data = []
    for row in table.xpath('.//tbody/tr'):
        # Extraire le rang, le nom du joueur et les statistiques
        rank = row.xpath('.//td[1]/text()')[0].strip()
        player_name = row.xpath('.//td[2]//div[@class="name"]/text()')[0].strip()
        stats = [td.text.strip() for td in row.xpath('.//td[position()>2]')]

        # Ajouter les données à la liste
        data.append([rank, player_name] + stats)

    # Créer un DataFrame
    columns = ['Rank', 'Name', 'Return Rating', '% 1st Serve Return Points Won', '% 2nd Serve Return Points Won', '% Return Games Won', '% Break Points Converted']
    df = pd.DataFrame(data, columns=columns)
    df['Year'] = year

    return df


# Utilisation de la fonction pour l'année 2022
#scrape_return_stats(2022)

#Test de la fonction under pressure
#scrape_pressure_stats(2022)

"""""
data_pressure = pd.concat([scrape_pressure_stats(i) for i in range(1991, 2022)], ignore_index=True)
data_pressure.to_csv('stats_under_pressure_1991_2022.csv', index=False)

data_return = pd.concat([scrape_return_stats(i) for i in range(1991, 2022)], ignore_index=True)
data_return.to_csv('stats_under_pressure_1991_2022.csv', index=False)
"""