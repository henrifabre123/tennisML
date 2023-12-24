from shiny import ui, App, render
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast
from class_joueur import joueur
from class_joueur import PlayerRadarChart
from pathlib import Path


# onetime things to load
my_file = Path(__file__).parent / "Data/Data_utiles/info_joueurs.csv"

df_info_joueurs = pd.read_csv(my_file)

annees = list(range(1993,2022))
joueurs = list(df_info_joueurs['name'])



app_ui = ui.page_fluid(
    ui.row(
        ui.column(
            4,
            ui.panel_well(
                ui.input_selectize("annee", "Selectize (single)", annees, multiple = False),
                ui.input_selectize("joueur", "Selectize (single)", joueurs, multiple = False)
            ),
        ),
        ui.column(
            8,
            ui.output_plot("plot1", click=True, dblclick=True, hover=True, brush=True) 
        ) 
    )
)

def server(input, output, session):
    @output
    @render.plot(alt="A spider web")
    def plot1():
        player = joueur(input.joueur())
        fig = player.vis_stats(input.annee())  
        return fig
    

app = App(app_ui, server, debug = True)


