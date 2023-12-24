from shiny import render, ui
from shiny.express import input
import pandas as pd


ui.panel_title("Comparison of players")
ui.input_slider("n", "N", 0, 100, 20)


@render.text
def txt():
    return f"n*2 is {input.n() * 2}"
