# Datatennis : Malo Evain, Alexandre Combes et Henri Fabre

# Introduction

Ce projet consiste en une étude des déterminants de la performance des joueurs de tennis du meilleur niveau.

Nous sommes trois étudiants passionnés de sport. Nous voulions mettre à profit ce cours de Python pour la data science pour mieux comprendre pourquoi certains tennismen sont restés au meilleur niveau pendant plus de 10 ans alors que certains peinent à atteindre le top 20. 

Voilà l'articulation du projet : 

$\textbf{
    1. Récupération et traitement des données (fichier Traitement_data.ipynb)
    2. Visualisation et analyse des données (fichiers Visualisation.ipynb et appv2.py)
    3. Algorithme de prédiction du classement ATP d'un joueur sur une année (prediction_atp_points.py), et du rang du joueur sur une année (prediction_rang.py)
}$

### Données : 

Les données extraites viennent de plusieurs sources : 
Nous avons récupérées les databases des matches ATP (atp_matches_201X) de Jeffrey Sackman, ainsi que les classements semaine après semaine sur chaque année (atp_rankings_10s).
Nous avons ensuite scrappé sur le site de l'ATP les statistiques sur les services des joueurs, leur retour et leur capacité à gérer les "breaks", c'est à dire à gagner les points sous pression.
Les fichiers atp_rankings contiennent le classement du top 100 semaine après semaine sur les 30 dernières années. 
Les fichiers atp_matches contiennent des informations sur les matches : nom du gagnant, du perdant, du tournoi, score, stade du tournoi (finale, demies finales..), surface (terre battue, gazon..), classement des joueurs au moment du match.

A partir de ces bases de données nous avons créé les bases de données info_joueurs, qui nous donnent les informations sur les joueurs année après année : winrate, stats sur les services, les retours, sous pression..

### Visualisation :

Le travail de visualisation est décomposé en deux parties : 
- D'une part, un travail sur les différences de performance entre joueurs du top 10 et joueurs du top 40-50, pour identifier les facteurs qui différencient un bon joueur professionnel et un joueur de classe mondiale. Cela est la première partie de visualisation.ipynb
- D'autre part, un travail de visualisation sur les joueurs individuellement, et de comparaison de performance entre les joueurs. Cela correspond à la fin du fichier visualisation.ipynb et à l'app (appv2.py)

### Modélisation : 

Pour la modélisation, nous voulions prédire le rang d'un joueur en fin d'année à l'aune de ses performances au cours de matches. Pour cela, nous avons utilisé à la fois le classement ATP et le nombre de points ATP, car il y a eu une inflation très importante sur la dernière décennie pour les points ATP.