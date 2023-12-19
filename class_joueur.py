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


    #méthode pour print les stats d'un joueur
    def afficher_infos_annee(self, annee):
        if annee in self.infos.columns:
            infos_annee = self.infos[annee].to_dict()
            print(f"{self.__str__()} en {annee}:")
            for cle, valeur in infos_annee.items():
                print(f"{cle}: {valeur}")
        else:
            print(f"Aucune information disponible pour {self.nom} en {annee}")



rafa=joueur('rafael nadal')

print(rafa)
