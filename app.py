from shiny import ui, App
import pandas as pd

df_info_joueurs = pd.read_csv('/Users/henrifabre/myapp/tennisML/tennisML/Data/Data_utiles/info_joueurs.csv')

annees = list(range(1993,2022))


app_ui = ui.page_fluid(
    ui.input_selectize("x2", "Selectize (single)", annees, multiple = True)
)


app = App(app_ui, None)


