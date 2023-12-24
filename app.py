from shiny import ui, App, render
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast
from class_joueur import joueur
from class_joueur import PlayerRadarChart

df_info_joueurs = pd.read_csv('/Users/henrifabre/myapp/tennisML/tennisML/Data/Data_utiles/info_joueurs.csv')

annees = list(range(1993,2022))
joueurs = list(df_info_joueurs['name'])



app_ui = ui.page_fluid(
    ui.input_selectize("annee", "Selectize (single)", annees, multiple = False),
    ui.input_selectize("joueur", "Selectize (single)", joueurs, multiple = False),
    ui.output_plot("plot1", click=True, dblclick=True, hover=True, brush=True)
)

def server(input, output, session):
    @output
    @render.plot(alt="A histogram")
    def plot1():
        player = joueur(input.joueur())
        fig, ax = plt.subplots()
        player.vis_rang()  # Supposons que vis_rang prend un axe (ax) en paramètre pour le tracé
        return fig
    

app = App(app_ui, server, debug = True)


