# Datatennis
### Par Malo Evain, Alexandre Combes et Henri Fabre

## Introduction

Ce projet se penche sur l'étude des déterminants de la performance des joueurs de tennis de haut niveau.

Nous sommes trois étudiants passionnés de sport, désireux d'utiliser nos connaissances en Python pour la data science afin d'analyser la longévité sportive de certains joueurs de tennis au sommet, comparativement à d'autres qui peinent à atteindre le top 20.

## Structure du Projet

1. **Récupération et traitement des données**
   - `Traitement_data.ipynb`
   - `scrapping.py`et `Extraction_info_retours.py` dans le dossier `./Data/Scrapping`
2. **Visualisation et analyse des données**
   - `Visualisation.ipynb`
   - `appv2.py`
3. **Algorithmes de prédiction**
   - Classement ATP d'un joueur sur une année: `prediction_atp_points.py`
   - Rang du joueur sur une année: `prediction_rang.py`
   - Les modèles entrainés sont stockés dans le dossier `Modeles_ML`

## Données

## Sources de nos Données

Notre projet s'appuie sur des données hétérogènes, obtenues par différents moyens :

- **Scraping de Statistiques ATP** : Pour les 20 dernières années, nous avons extrait des statistiques détaillées sur les services, retours, et performances sous pression des joueurs depuis le site officiel de l'ATP. Ce processus n'a pas été sans difficultés. En effet, le site de l'ATP utilise JavaScript pour afficher dynamiquement ces données, ce qui a nécessité l'emploi de Selenium et de son Chromedriver. L'utilisation de Selenium était indispensable pour simuler un navigateur et attendre le chargement complet des scripts JavaScript. Tous nos scripts de scraping sont organisés dans le répertoire `./Data/Scrapping`, et les données récolltées se trouvent dans `./Data/Data_utiles`. Etant donné le temps d'exécution des scripts de scrapping, nous avons préféré inclure directement les données et ne pas inclure le scrapping dans le notebook `Traitement_data.ipynb`.

- **Exploitation de Bases de Données ATP** : Nous avons également intégré des données issues des bases de données de matchs ATP (`atp_matches_201X`) et des classements hebdomadaires (`atp_rankings_10s`), gracieusement fournies par Jeffrey Sackman. Ces bases de données ont été cruciales pour compléter notre analyse et offrir une perspective plus large sur les performances des joueurs.


Les fichiers `atp_rankings` recensent le classement des 100 meilleurs joueurs semaine par semaine sur les 30 dernières années. Les fichiers `atp_matches` détaillent les informations relatives aux matchs : noms des joueurs, étape du tournoi, score, surface de jeu, classement des joueurs au moment du match.

Ces informations nous ont permis de constituer les bases de données `info_joueurs`, offrant un aperçu annuel des performances des joueurs : taux de victoire, statistiques sur les services, les retours, et la gestion de la pression. La constitution de cette base de donnée est expliquée en détail dans `Visualisation.ipynb`

## Visualisation

Le travail de visualisation s'articule en deux parties :

- Une analyse des différences de performance entre les joueurs du top 10 et ceux du top 40-50, afin d'identifier les attributs distinctifs d'un joueur professionnel et d'un joueur de classe mondiale.
- Une étude individuelle et comparative des performances des joueurs, présentée vers la fin du fichier `visualisation.ipynb` et au sein de l'application `appv2.py`.
- L'application a été codée avec la librairie Tkinter. Nous avons tenté une première approche avec Shiny pour Python mais cette librairie est trop récente. Nous manquions de documentation et nous n'avons pas réussi à résoudre un problème de pixel des Mac. Ainsi nous sommes revenus à une librairie plus classique, celle de Tkinter.

## Modélisation

Notre objectif de modélisation était de prédire le rang final annuel d'un joueur en fonction de ses performances dans les matchs. Nous avons choisi d'utiliser le classement ATP et les points ATP comme indicateurs, en raison de l'inflation significative des points ATP au cours de la dernière décennie.

L'objectif de la partie modélisation, au delà de prédire le rang et le nombre de points de chaque joueur, est surtout de pouvoir comparer des joueurs qui n'ont jamais joué ensemble. En effet, comme les modèles sont entrainés sans tenir compte des années, les seuls critères seront les statistiques de chaque joueur. Il faut vraiment comprendre que le dataset a été "Uniformisé" pour simuler le fait que tous les joueurs aient joué la même année.

Cela amène certains problèmes pour la prédiction du rang. Sur certaines années, des joueurs comme Djokovic ou Nadal ont eu des stats tellement hors normes que le modèle leur prédit un rang légèrement négatif (-0,8) qui peut toute fois s'interpréter comme le fait d'être simplement le meilleur joueur.

Nous avons testé 3 approches différentes pour arriver à nos fins:
- `Régression Ridge`
- `SVM`
- `Réseau de neurones`

Pour conclure nous avons gardé le modèle de réseau de neurones puisqu'il prend le mieux en compte la partie non linéaire de la variable à prédire.

## Conclusion

Ce projet nous a permis de constater que le principal atout des joueurs du top 10 est la régularité sur tous les plans : physiques, mentaux, tactiques. Ils savent s'appuyer sur les fondamentaux du jeu du tennis pour faire la différence face à des joueurs moins bien classés. Les différences entre joueurs du top 10 s'expliquent surtout par des styles de jeu différents. 

### Pour aller plus loin : 
Notre analyse aurait pu être étayée par une analyse plus précise du style de jeu de chaque joueur, notamment en fonction de la surface des matches (terre battue, gazon, quick). Cela nous aurait permis ensuite de créer un modèle de prédiction des matches, mais cela s'éloigne de notre objectif de départ qui était centré sur les caractéristiques de jeu des joueurs du top niveau. 
Nous aurions pu aussi de changer d'échelle, pour étudier à l'échelle d'un match les performances des joueurs de top niveau, plutôt que sur un année. Mais entrer dans une telle analyse aurait requis une masse de données bien plus importante (de l'ordre de l'information coup par coup), et nous aurait demandé de passer par des APIs payantes, ce qui nous a bloqué. 
