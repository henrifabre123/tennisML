import pandas as pd

df_infos_joueurs=pd.read_csv('./Data/Data_utiles/info_joueurs.csv')

class joueur:

    def __init__(self,nom):

        self.nom = nom

        self.infos=df_infos_joueurs[df_infos_joueurs['name']==nom]
        self.id=self.infos['id']

    def __str__(self):
        txt = f"Informations pour {self.nom} \n"
        txt += f"taille : {self.infos['height'].values[0]}\n"
        txt += f"main : {self.infos['hand'].values[0]}"
        return txt






rafa=joueur('rafael nadal')

print(rafa)
