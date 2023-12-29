import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from class_joueur import joueur  # Supposons que votre classe joueur est dans un fichier joueur.py
from pathlib import Path
import ast

# onetime things to load
my_file = Path(__file__).parent / "Data/Data_utiles/info_joueurs.csv"

df_info_joueurs = pd.read_csv(my_file)


class JoueurApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application Joueur")

        # Création du widget de sélection de l'année
        self.label_annee = tk.Label(root, text="Sélectionnez une année :")
        self.label_annee.pack(pady=10)

        self.selected_annee = tk.StringVar()
        self.selected_annee.set("2022")  # Année par défaut, à adapter selon vos besoins

        self.annee_menu = ttk.Combobox(root, textvariable=self.selected_annee, values=[str(year) for year in range(1993, 2023)])
        self.annee_menu.pack(pady=10)

        # Bouton pour afficher les joueurs de l'année sélectionnée
        self.button_afficher_joueurs = tk.Button(root, text="Afficher les joueurs", command=self.afficher_joueurs)
        self.button_afficher_joueurs.pack(pady=10)

        # Label pour afficher les résultats
        self.label_resultats = tk.Label(root, text="")
        self.label_resultats.pack(pady=10)

        # Bouton pour afficher le graphique vis_rang
        self.button_vis_rang = tk.Button(root, text="Afficher vis_rang", command=self.plot_vis_rang, state=tk.DISABLED)
        self.button_vis_rang.pack(pady=10)

        # Bouton pour afficher le graphique vis_stats
        self.button_vis_stats = tk.Button(root, text="Afficher vis_stats", command=self.plot_vis_stats, state=tk.DISABLED)
        self.button_vis_stats.pack(pady=10)

        # Variable pour stocker les joueurs de l'année sélectionnée
        self.joueurs_annee = None

    def afficher_joueurs(self):
        # Récupérer l'année sélectionnée
        year = int(self.selected_annee.get())

        # Filtrer les joueurs qui ont joué cette année
        self.joueurs_annee = [nom for nom in df_info_joueurs['name'] if joueur(nom).a_joue(year)]

        # Mettre à jour les valeurs du menu de sélection du joueur
        self.joueur_menu['values'] = self.joueurs_annee
        self.joueur_menu.set(self.joueurs_annee[0] if self.joueurs_annee else "")

        # Activer les boutons pour afficher les graphiques
        self.button_vis_rang['state'] = tk.NORMAL
        self.button_vis_stats['state'] = tk.NORMAL

        # Afficher les résultats
        if self.joueurs_annee:
            resultat_str = "Les joueurs qui ont joué en {} : {}".format(year, ", ".join(self.joueurs_annee))
        else:
            resultat_str = "Aucun joueur n'a joué en {}".format(year)

        self.label_resultats.config(text=resultat_str)

    def plot_vis_rang(self):
        nom_joueur = self.selected_joueur.get()
        rafa = joueur(nom_joueur)
        figure = rafa.vis_rang()

        # Affichez la figure dans une nouvelle fenêtre Tkinter
        self.plot_figure(figure)

    def plot_vis_stats(self):
        nom_joueur = self.selected_joueur.get()
        year = int(self.selected_annee.get())
        rafa = joueur(nom_joueur)
        stats_data = rafa.vis_stats(year)

        if stats_data is not None:
            figure, ax = plt.subplots(figsize=(8, 8))
            radar_chart = rafa.PlayerRadarChart(stats_data)
            radar_chart.plot_on_ax(ax, color='blue', label=f'Statistiques {year}')
            ax.legend()

            # Affichez la figure dans une nouvelle fenêtre Tkinter
            self.plot_figure(figure)

    def plot_figure(self, figure):
        # Créez une fenêtre Tkinter pour afficher la figure
        new_window = tk.Toplevel(self.root)
        new_window.title("Graphique")

        # Ajoutez la figure à la fenêtre Tkinter
        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack()


# Créez la fenêtre principale Tkinter
root = tk.Tk()

# Instanciez l'application JoueurApp
app = JoueurApp(root)

# Lancer la boucle principale Tkinter
root.mainloop()

