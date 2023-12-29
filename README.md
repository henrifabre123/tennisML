# Datatennis
### Par Malo Evain, Alexandre Combes et Henri Fabre

## Introduction

Ce projet se penche sur l'étude des déterminants de la performance des joueurs de tennis de haut niveau.

Nous sommes trois étudiants passionnés de sport, désireux d'utiliser nos connaissances en Python pour la data science afin d'analyser la longévité sportive de certains joueurs de tennis au sommet, comparativement à d'autres qui peinent à atteindre le top 20.

## Structure du Projet

1. **Récupération et traitement des données**
   - `Traitement_data.ipynb`
2. **Visualisation et analyse des données**
   - `Visualisation.ipynb`
   - `appv2.py`
3. **Algorithmes de prédiction**
   - Classement ATP d'un joueur sur une année: `prediction_atp_points.py`
   - Rang du joueur sur une année: `prediction_rang.py`

## Données

Les sources de nos données sont multiples :

- Scraping des statistiques sur les services, retours, et performances sous pression des joueurs depuis le site de l'ATP pour les 20 dernières années.
- Exploitation des bases de données de matchs ATP (`atp_matches_201X`) et des classements hebdomadaires (`atp_rankings_10s`) fournies par Jeffrey Sackman.

Les fichiers `atp_rankings` recensent le classement des 100 meilleurs joueurs semaine par semaine sur les 30 dernières années. Les fichiers `atp_matches` détaillent les informations relatives aux matchs : noms des joueurs, étape du tournoi, score, surface de jeu, classement des joueurs au moment du match.

Ces informations nous ont permis de constituer les bases de données `info_joueurs`, offrant un aperçu annuel des performances des joueurs : taux de victoire, statistiques sur les services, les retours, et la gestion de la pression.

## Visualisation

Le travail de visualisation s'articule en deux parties :

- Une analyse des différences de performance entre les joueurs du top 10 et ceux du top 40-50, afin d'identifier les attributs distinctifs d'un joueur professionnel et d'un joueur de classe mondiale.
- Une étude individuelle et comparative des performances des joueurs, présentée vers la fin du fichier `visualisation.ipynb` et au sein de l'application `appv2.py`.

## Modélisation

Notre objectif de modélisation était de prédire le rang final annuel d'un joueur en fonction de ses performances dans les matchs. Nous avons choisi d'utiliser le classement ATP et les points ATP comme indicateurs, en raison de l'inflation significative des points ATP au cours de la dernière décennie.

L'objectif de la partie modélisation, au delà de prédire le rang et le nombre de points de chaque joueur, est surtout de pouvoir comparer des joueurs qui n'ont jamais joué ensemble. En effet, comme les modèles sont entrainés sans tenir compte des années, les seuls critères seront les statistiques de chaque joueur. Il faut vraiment comprendre que le dataset a été "Uniformisé" pour simuler le fait que tous les joueurs aient joué la même année.

Cela amène certains problèmes pour la prédiction du rang. Sur certaines années, des joueurs comme Djokovic ou Nadal ont eu des stats tellement hors normes que le modèle leur prédit un rang légèrement négatif (-0,8) qui peut toute fois s'interpréter comme le fait d'être simplement le meilleur joueur.

Nous avons testé 3 approches différentes pour arriver à nos fins:
- `Régression Ridge`
- `SVM`
- `Réseau de neurones`

Pour conclure nous avons gardé le modèle de réseau de neurones puisqu'il prend le mieux en compte la partie non linéaire de la variable à prédire.
