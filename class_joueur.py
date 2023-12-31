import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast
import joblib
from keras.models import load_model
from sklearn.preprocessing import StandardScaler

from pathlib import Path


# onetime things to load
my_file = Path(__file__).parent / "Data/Data_utiles/info_joueurs.csv"
df_infos_joueurs = pd.read_csv(my_file)


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


    def list_rang(self):
        """
        Fonction qui retourne les données pour l'évolution du rang d'un joueur.
        """

        liste_rang = []
        liste_annee = []

        for year in range(1993, 2022):
            year_data_str = self.infos[str(year)].values[0]
            year_data_dict = ast.literal_eval(year_data_str)

            if 'rang' in year_data_dict:
                liste_rang.append(year_data_dict['rang'])
                liste_annee.append(year)

        return {'annees': liste_annee, 'rangs': liste_rang}

    def list_stats(self, year):

        """
        Fonction qui retourne les données pour le graphique radar des stats du joueur.
        """


        if self.infos.empty or str(year) not in self.infos:
            print(f"No data available for {self.nom} in {year}.")
            return None

        # Convert the year's data from string to dictionary
        year_data_str = self.infos[str(year)].values[0]
        year_data_dict = ast.literal_eval(year_data_str)

        if not year_data_dict:
            print(f"{self.nom} n'a pas joué cette année")
            return None

        # Define the keys to plot
        keys_to_plot = [
            'pourc_return_win_pnt', 'pourc_break_games', 'pourc_break_point_made',
            'pourc_break_point_saved', 'pourc_serv_games_win', 'pourc_serv_in',
            ' % Break Point Saved', ' % Break Points Converted Pressure',
            ' % Deciding Sets Won', ' % Tie Breaks Won'
        ]

        # Filter the data
        filtered_data = {key: year_data_dict[key] for key in keys_to_plot if key in year_data_dict}

        return filtered_data

    def vis_rang(self):

        """
        Fonction qui plot l'évolution du rang d'un joueur au fil de sa carrière.
        """

        liste_rang = []
        liste_annee = []

        for year in range(1993, 2022):
            year_data_str = self.infos[str(year)].values[0]
            year_data_dict = ast.literal_eval(year_data_str)

            if 'rang' in year_data_dict:
                liste_rang.append(year_data_dict['rang'])
                liste_annee.append(year)

        plt.figure(figsize=(8, 6))
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
        """
        fonction qui va afficher un graphique spyder des stats du joueur sur l'année demandée
        """

        if self.infos.empty or str(year) not in self.infos:
            print(f"No data available for {self.nom} in {year}.")
            return

        # Convert the year's data from string to dictionary
        year_data_str = self.infos[str(year)].values[0]
        year_data_dict = ast.literal_eval(year_data_str)

        if not year_data_dict:
            print(f"{self.nom} n'a pas joué cette année")
            return

        year_data_dict['winrate']=year_data_dict['win']/year_data_dict['matchs']
        # Define the keys to plot
        keys_to_plot = [
            'pourc_return_win_pnt', 'pourc_break_games', 'pourc_break_point_made',
            'pourc_break_point_saved', 'pourc_serv_games_win', 'winrate',
            ' % Break Point Saved', ' % Break Points Converted Pressure',
            ' % Deciding Sets Won', ' % Tie Breaks Won'
        ]

        # Filter the data
        filtered_data = {key: year_data_dict[key] for key in keys_to_plot if key in year_data_dict}

        # Generate and show the radar chart
        radar_chart = PlayerRadarChart(filtered_data)
        radar_chart.plot(title=f"statistiques de {self.nom} en {year}")


    def prediction_atp_points(self, year):
        """
        fonction qui prédit le score atp d'un joueur sur une saison
        """

        # Convert the year's data from string to dictionary
        year_data_str = self.infos[str(year)].values[0]
        year_data_dict = ast.literal_eval(year_data_str)

        if not year_data_dict:
            print(f"{self.nom} n'a pas joué cette année")
            return

        # Utiliser pathlib pour définir le chemin du fichier
        data_path = Path(__file__).parent / "Data" / "Data_utiles" / "Data_ML" / f"infos_joueurs_{year}.csv"
        df_year = pd.read_csv(data_path)

        X = df_year[df_year['name'] == self.nom].copy()

        # Sélection des colonnes avant la normalisation
        X = X.drop(['Unnamed: 0', 'rang', 'name', 'hand', 'atp_points'], axis=1).copy()
        if len(X.columns)>16:
            X=X.drop(['Return Rating', ' % Serve Return Points Won',
                   ' % 2nd Serve Return Points Won', ' % Return Games Won',
                   ' % Break Points Converted', 'Under Pressure Rating',
                   ' % Break Point Saved', ' % Break Points Converted Pressure',
                   ' % Deciding Sets Won', ' % Tie Breaks Won'], axis=1)
        else:
            X=X.drop([ 'Under Pressure Rating',
                   ' % Break Point Saved', ' % Break Points Converted Pressure',
                   ' % Deciding Sets Won', ' % Tie Breaks Won'], axis=1)

        X = X.reset_index(drop=True)


        data_path = Path(__file__).parent /"Modeles_ML"/"all_players_neural_network_model.keras"
        all_players_neural_network_model = load_model(data_path)

        return all_players_neural_network_model.predict(X)

    def prediction_rang(self,year):

        """
        fonction qui prédit le rang d'un joueur en fonction de ses stats sur cette année
        """

        # Convert the year's data from string to dictionary
        year_data_str = self.infos[str(year)].values[0]
        year_data_dict = ast.literal_eval(year_data_str)

        if not year_data_dict:
            print(f"{self.nom} n'a pas joué cette année")
            return

        # Utiliser pathlib pour définir le chemin du fichier
        data_path = Path(__file__).parent / "Data" / "Data_utiles" / "Data_ML" / f"infos_joueurs_{year}.csv"
        df_year = pd.read_csv(data_path)


        X = df_year[df_year['name'] == self.nom].copy()


        X = X.drop(['Unnamed: 0', 'rang', 'name', 'hand', 'atp_points'], axis=1).copy()

        if len(X.columns)>16:
            X=X.drop(['Return Rating', ' % Serve Return Points Won',
                   ' % 2nd Serve Return Points Won', ' % Return Games Won',
                   ' % Break Points Converted', 'Under Pressure Rating',
                   ' % Break Point Saved', ' % Break Points Converted Pressure',
                   ' % Deciding Sets Won', ' % Tie Breaks Won'], axis=1)
        else:
            X=X.drop([ 'Under Pressure Rating',
                   ' % Break Point Saved', ' % Break Points Converted Pressure',
                   ' % Deciding Sets Won', ' % Tie Breaks Won'], axis=1)

        X = X.reset_index(drop=True)

        data_path = Path(__file__).parent /"Modeles_ML"/"rang_neural_network_model.keras"
        rang_neural_network_model = load_model(data_path)

        return rang_neural_network_model.predict(X)

    def list_rang(self):

        """
        Fonction qui retourne les données pour l'évolution du rang d'un joueur.
        """

        liste_rang = []
        liste_annee = []

        for year in range(1993, 2022):
            year_data_str = self.infos[str(year)].values[0]
            year_data_dict = ast.literal_eval(year_data_str)

            if 'rang' in year_data_dict:
                liste_rang.append(year_data_dict['rang'])
                liste_annee.append(year)

        return {'annees': liste_annee, 'rangs': liste_rang}

    def list_stats(self, year):

        """
        Fonction qui retourne les données pour le graphique radar des stats du joueur.
        """

        if self.infos.empty or str(year) not in self.infos:
            print(f"No data available for {self.nom} in {year}.")
            return None

        # Convert the year's data from string to dictionary
        year_data_str = self.infos[str(year)].values[0]
        year_data_dict = ast.literal_eval(year_data_str)

        if not year_data_dict:
            print(f"{self.nom} n'a pas joué cette année")
            return None

        # Define the keys to plot
        keys_to_plot = [
            'pourc_return_win_pnt', 'pourc_break_games', 'pourc_break_point_made',
            'pourc_break_point_saved', 'pourc_serv_games_win', 'pourc_serv_in',
            ' % Break Point Saved', ' % Break Points Converted Pressure',
            ' % Deciding Sets Won', ' % Tie Breaks Won'
        ]

        # Filter the data
        filtered_data = {key: year_data_dict[key] for key in keys_to_plot if key in year_data_dict}

        return filtered_data

    def a_joue(self, year):

        """
        Fonction qui vérifie si le joueur a joué pendant une année spécifiée.
        """

        year_data_str = self.infos[str(year)].values[0]
        year_data_dict = ast.literal_eval(year_data_str)
        return bool(year_data_dict)




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
        ax.set_xticks(self.angles[:-1])
        ax.set_xticklabels(self.categories, color='grey', size=8)  # Ajout des étiquettes de catégorie


    def plot(self, title="Player Radar Chart"):
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        plt.xticks(self.angles[:-1], self.categories)

        ax.plot(self.angles, self.values)
        ax.fill(self.angles, self.values, 'teal', alpha=0.1)

        ax.set_title(title)  # Ajoutez cette ligne pour définir le titre

        plt.show()
