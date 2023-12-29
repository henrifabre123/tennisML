import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from class_joueur import joueur  # Assurez-vous que votre classe joueur est dans un fichier joueur.py
from pathlib import Path
import ast

# onetime things to load
my_file = Path(__file__).parent / "Data/Data_utiles/info_joueurs.csv"
df_info_joueurs = pd.read_csv(my_file)

class JoueurApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application Joueur")
        self.setup_ui()

    def setup_ui(self):
        # Création du widget de sélection de l'année
        self.label_annee = tk.Label(self.root, text="Sélectionnez une année :")
        self.label_annee.pack(pady=10)

        self.selected_annee = tk.StringVar()
        self.selected_annee.set("2022")  # Année par défaut

        self.annee_menu = ttk.Combobox(self.root, textvariable=self.selected_annee, values=[str(year) for year in range(1993, 2023)])
        self.annee_menu.pack(pady=10)

        # Bouton pour afficher les joueurs de l'année sélectionnée
        self.button_afficher_joueurs = tk.Button(self.root, text="Afficher les joueurs", command=self.afficher_joueurs)
        self.button_afficher_joueurs.pack(pady=10)

        # Créer le widget de sélection du joueur
        self.label_joueur = tk.Label(self.root, text="Sélectionnez un joueur :")
        self.label_joueur.pack(pady=10)

        self.selected_joueur = tk.StringVar()
        self.joueur_menu = ttk.Combobox(self.root, textvariable=self.selected_joueur)
        self.joueur_menu.pack(pady=10)

        # Bouton pour afficher le graphique vis_rang
        self.button_vis_rang = tk.Button(self.root, text="Afficher vis_rang", command=self.plot_vis_rang, state=tk.DISABLED)
        self.button_vis_rang.pack(pady=10)

        # Bouton pour afficher le graphique vis_stats
        self.button_vis_stats = tk.Button(self.root, text="Afficher vis_stats", command=self.plot_vis_stats, state=tk.DISABLED)
        self.button_vis_stats.pack(pady=10)

        # Bouton Predict
        self.button_predict = tk.Button(self.root, text="Predict", command=self.prediction_classement, state=tk.DISABLED)
        self.button_predict.pack(pady=10)

        # Variables pour stocker les joueurs de l'année sélectionnée et les éléments de l'interface graphique
        self.joueurs_annee = None
        self.label_prediction = None
        self.canvas = None

    def afficher_joueurs(self):
        # Récupérer l'année sélectionnée
        year = int(self.selected_annee.get())

        # Filtrer les joueurs qui ont joué cette année
        self.joueurs_annee = [nom for nom in df_info_joueurs['name'] if joueur(nom).a_joue(year)]

        # Mettre à jour les valeurs du menu de sélection du joueur
        self.selected_joueur.set(self.joueurs_annee[0] if self.joueurs_annee else "")
        self.joueur_menu['values'] = self.joueurs_annee
        self.joueur_menu.set(self.joueurs_annee[0] if self.joueurs_annee else "")

        # Activer les boutons pour afficher les graphiques et la prédiction
        self.button_vis_rang['state'] = tk.NORMAL
        self.button_vis_stats['state'] = tk.NORMAL
        self.button_predict['state'] = tk.NORMAL

    def plot_vis_rang(self):
        nom_joueur = self.selected_joueur.get()
        rafa = joueur(nom_joueur)
        figure = rafa.vis_rang()
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
            self.plot_figure(figure)
        else:
            if self.label_prediction:
                self.label_prediction.pack_forget()
            self.label_prediction = tk.Label(self.root, text="Aucune statistique à afficher pour cette année.")
            self.label_prediction.pack(pady=10)

    def prediction_classement(self):
        nom_joueur = self.selected_joueur.get()
        year = int(self.selected_annee.get())
        rafa = joueur(nom_joueur)
        try:
            predicted_points = rafa.prediction_atp_points(year)
            if self.label_prediction:
                self.label_prediction.pack_forget()
            self.label_prediction = tk.Label(self.root, text=f"Classement prédit pour {year}: {predicted_points}")
            self.label_prediction.pack(pady=10)
        except Exception as e:
            if self.label_prediction:
                self.label_prediction.pack_forget()
            self.label_prediction = tk.Label(self.root, text=f"Erreur lors de la prédiction: {e}")
            self.label_prediction.pack(pady=10)

    def plot_figure(self, figure):
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(figure, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Créez la fenêtre principale Tkinter
root = tk.Tk()

# Instanciez l'application JoueurApp
app = JoueurApp(root)

# Lancer la boucle principale Tkinter
root.mainloop()
