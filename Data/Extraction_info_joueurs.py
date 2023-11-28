import pandas as pd

""" Le but de ce fichier est de récupérer pour chaque année le top 100 des joueurs,
qui est jusque là mis sous forme d'identifiant et de le relier aux informations du joueurs grâce à son ID"""

Years=['00','10','20','90']


liste_concat=[]
for year in Years:

    #On importe le classement des joueurs par année
    df_ranking= pd.read_csv('atp_rankings_{}s.csv'.format(year))

    #On supprime les joueurs qui ont un rang superieur à 100
    df_ranking = df_ranking[df_ranking['rank'] <= 100]



    #On commence par renommer la colonne du nom du joueur histoire de pouvoir merge via une colonne en commun
    df_ranking=df_ranking.rename(columns={'player':'player_id'})

    liste_concat.append(df_ranking.copy())


df_ranking=pd.concat(liste_concat)


#On importe les données relatives à chaque joueur
df_info_joueurs = pd.read_csv('atp_players.csv')

#On peut ensuite joindre les deux datasets

df_info_joueurs=pd.merge(df_ranking,df_info_joueurs,on='player_id')
df_info_joueurs.sort_values(['ranking_date','rank'],ascending=True,inplace=True)

df_info_joueurs.to_csv('info_rank')
