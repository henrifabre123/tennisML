
from shiny import ui, App, render
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast
from class_joueur import joueur
from class_joueur import PlayerRadarChart
from pathlib import Path
from matplotlib.backends.backend_agg import FigureCanvasAgg
import os

running_on_mac = os.name == "macOS"

# Define the device pixel ratio
device_pixel_ratio = 2 if running_on_mac else 1

# onetime things to load
my_file = Path(__file__).parent / "Data/Data_utiles/info_joueurs.csv"

df_info_joueurs = pd.read_csv(my_file)

annees = list(range(1993,2022))
joueurs = list(df_info_joueurs['name'])



app_ui = ui.page_fluid(

    ui.input_selectize("annee", "Selectize (single)", annees, multiple = False),
    ui.input_selectize("joueur", "Selectize (single)", joueurs, multiple = False),
    ui.output_plot("plot_stats"),  

           
)

def server(input, output,session):
    @output
    @render.plot()
    def plot_stats():
        # Créez une instance de la classe joueur
        player_instance = joueur(input.joueur())

        # Obtenez les données pour le graphique d'évolution du rang
        rang_data = player_instance.list_rang()

        fig, ax = plt.subplots(figsize=(10, 6), dpi=device_pixel_ratio)
        ax.plot(rang_data['annees'], rang_data['rangs'], marker='o', linestyle='-', color='b', label='Classement')

        # Ajout des étiquettes d'axe et du titre
        ax.set_xlabel('Année')
        ax.set_ylabel('Classement')
        ax.set_title(f'Évolution du classement de {input.joueur()} (1993-2021)')

        # Ajout de la légende
        ax.legend()

        # Ajout de la grille pour une meilleure lisibilité
        ax.grid(True)

        return fig

    """
    def plot_stats():
        # Créez une instance de la classe joueur
        player_instance = joueur(input.joueur())

        # Obtenez les données pour le graphique radar
        stats_data = player_instance.vis_stats(input.annee())

        if stats_data is not None:
            # Générez et affichez le graphique radar
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)

            categories = list(stats_data.keys())
            values = list(stats_data.values())

            values += values[:1]
            angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
            angles += angles[:1]

            ax.plot(angles, values, color='b', linewidth=2, linestyle='solid', label=f'Statistiques {input.annee()}')
            ax.fill(angles, values, color='b', alpha=0.25)

            plt.xticks(angles[:-1], categories)
            ax.set_title(f"Statistiques de {input.joueur()} en {input.annee()}")
            ax.legend(loc='upper right')

            plt.show()
"""


    

app = App(app_ui, server)


