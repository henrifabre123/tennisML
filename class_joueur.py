import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast

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

    import matplotlib.pyplot as plt

    def vis_rang(self):
        """Fonction qui plot l'évolution du rang d'un joueur au fil de sa carrière."""
        liste_rang = []
        liste_annee = []

        for year in range(1993, 2022):
            year_data_str = self.infos[str(year)].values[0]
            year_data_dict = ast.literal_eval(year_data_str)

            if 'rang' in year_data_dict:
                liste_rang.append(year_data_dict['rang'])
                liste_annee.append(year)

        plt.figure(figsize=(10, 6))
        plt.plot(liste_annee, liste_rang, marker='o', linestyle='-', color='b', label='Classement')

        # Ajout des étiquettes d'axe et du titre
        plt.xlabel('Année')
        plt.ylabel('Classement')
        plt.title(f'Évolution du classement de {self.nom} (1993-2021)')

        # Ajout de la légende
        plt.legend()

        # Ajout de la grille pour une meilleure lisibilité
        plt.grid(True)

        # Affichage du graphique
        plt.show()



    def vis_stats(self,year):
        """ fonction qui va afficher un graphique spyder des stats du joueur sur l'année demandée """

        if self.infos.empty or str(year) not in self.infos:
            print(f"No data available for {self.nom} in {year}.")
            return

        # Convert the year's data from string to dictionary
        year_data_str = self.infos[str(year)].values[0]
        year_data_dict = ast.literal_eval(year_data_str)

        if not year_data_dict:
            print(f"{self.nom} n'a pas joué cette année")
            return

        # Define the keys to plot
        keys_to_plot = [
            'pourc_return_win_pnt', 'pourc_break_games', 'pourc_break_point_made',
            'pourc_break_point_saved', 'pourc_serv_games_win', 'pourc_serv_in',
            ' % Break Point Saved', ' % Break Points Converted Pressure',
            ' % Deciding Sets Won', ' % Tie Breaks Won'
        ]

        # Filter the data
        filtered_data = {key: year_data_dict[key] for key in keys_to_plot if key in year_data_dict}

        # Generate and show the radar chart
        radar_chart = PlayerRadarChart(filtered_data)
        radar_chart.plot(title=f"statistiques de {self.nom} en {year}")



rafa=joueur("rafael nadal")
rafa.vis_rang()





class PlayerRadarChart:
    def __init__(self, data):
        self.data = data
        self.categories = list(data.keys())
        self.values = list(data.values())
        self.values += self.values[:1]  # Complete the circle
        self.angles = np.linspace(0, 2 * np.pi, len(self.categories), endpoint=False).tolist()
        self.angles += self.angles[:1]  # Ensure the graph starts and ends at the same point

    def plot_on_ax(self, ax, color, label):
        ax.plot(self.angles, self.values, color=color, linewidth=2, linestyle='solid', label=label)
        ax.fill(self.angles, self.values, color=color, alpha=0.25)


    def plot(self, title="Player Radar Chart"):
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        plt.xticks(self.angles[:-1], self.categories)

        ax.plot(self.angles, self.values)
        ax.fill(self.angles, self.values, 'teal', alpha=0.1)

        ax.set_title(title)  # Ajoutez cette ligne pour définir le titre

        plt.show()
