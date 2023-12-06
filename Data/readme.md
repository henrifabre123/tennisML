Les données extraites viennent de plusieurs sources : 
Nous avons récupérées les databases des matches ATP (atp_matches_201X) de Jeffrey Sackman, ainsi que les classements semaine après semaine sur chaque année (atp_rankings_10s).
Nous avons ensuite scrappé sur le site de l'ATP les statistiques sur les services des joueurs, leur retour et leur capacité à gérer les "breaks", c'est à dire à gagner les points sous pression.
Les fichiers atp_rankings contiennent le classement du top 100 semaine après semaine sur les 30 dernières années. 
Les fichiers atp_matches contiennent des informations sur les matches : nom du gagnant, du perdant, du tournoi, score, stade du tournoi (finale, demies finales..), surface (terre battue, gazon..), classsement des joueurs au moment du match.

A partir de ces bases de données nous avons créé les bases de données info_joueurs, qui nous donnent les informations sur les joueurs année après année : winrate selon la surface, stats sur les services, les retours


