import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from class_joueur import joueur  # Assurez-vous que votre classe joueur est dans un fichier joueur.py
from pathlib import Path
import ast
from class_joueur import PlayerRadarChart

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
        self.selected_annee.set("2021")  # Année par défaut

        self.annee_menu = ttk.Combobox(self.root, textvariable=self.selected_annee, values=[str(year) for year in range(1993, 2021)])
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

        # Bouton pour comparer avec un autre joueur
        if not hasattr(self, 'button_compare'):
            self.button_compare = tk.Button(self.root, text="Comparer avec un autre joueur", command=self.setup_comparison_ui)
            self.button_compare.pack(pady=10)

        # Variable pour stocker le joueur sélectionné pour la comparaison

        self.selected_joueur_compare = None
        self.selected_annee_compare = None
        self.joueur_menu_compare = None
        self.annee_menu_compare = None
        

    
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
            predicted_rank = rafa.prediction_rang(year)
            
            # Assurez-vous que les prédictions sont des nombres ou des textes que vous pouvez afficher
            predicted_points_str = f"Points ATP prédits pour {year}: {predicted_points}"
            predicted_rank_str = f"Rang prédit pour {year}: {predicted_rank}"
            
            if self.label_prediction:
                self.label_prediction.pack_forget()
            
            self.label_prediction = tk.Label(self.root, text=f"{predicted_points_str}\n{predicted_rank_str}")
            self.label_prediction.pack(pady=10)
        except Exception as e:
            # Gérer le cas où la prédiction échoue
            if self.label_prediction:
                self.label_prediction.pack_forget()
            
            self.label_prediction = tk.Label(self.root, text=f"Erreur lors de la prédiction: {e}")
            self.label_prediction.pack(pady=10)

    
    def setup_comparison_ui(self):
        # Si les widgets de comparaison existent déjà, on les met à jour au lieu de les recréer
        if not hasattr(self, 'label_annee_compare'):
            # Création du widget de sélection de l'année pour la comparaison
            self.label_annee_compare = tk.Label(self.root, text="Sélectionnez une année pour la comparaison :")
            self.label_annee_compare.pack(pady=10)
            self.selected_annee_compare = tk.StringVar()
            self.selected_annee_compare.set("2021")  # Année par défaut pour la comparaison

            self.annee_menu_compare = ttk.Combobox(self.root, textvariable=self.selected_annee_compare, values=[str(year) for year in range(1993, 2021)])
            self.annee_menu_compare.pack(pady=10)
        
            self.annee_menu_compare.bind('<<ComboboxSelected>>', self.update_joueur_menu_compare)

            # Création du widget de sélection du joueur pour la comparaison
            self.label_joueur_compare = tk.Label(self.root, text="Sélectionnez un joueur pour la comparaison :")
            self.label_joueur_compare.pack(pady=10)

            self.selected_joueur_compare = tk.StringVar()
            self.joueur_menu_compare = ttk.Combobox(self.root, textvariable=self.selected_joueur_compare)
            self.joueur_menu_compare.pack(pady=10)

            # Bouton pour effectuer la comparaison
            self.button_execute_compare = tk.Button(self.root, text="Comparer", command=self.execute_comparison, state=tk.DISABLED)
            self.button_execute_compare.pack(pady=10)
        else:
            # Les widgets existent déjà, on les affiche simplement
            self.label_annee_compare.pack(pady=10)
            self.annee_menu_compare.pack(pady=10)
            self.label_joueur_compare.pack(pady=10)
            self.joueur_menu_compare.pack(pady=10)
            self.button_execute_compare.pack(pady=10)

    def update_joueur_menu_compare(self, event=None):
        # Mettre à jour le menu déroulant des joueurs en fonction de l'année sélectionnée pour la comparaison
        year_compare = int(self.selected_annee_compare.get())
        joueurs_annee_compare = [nom for nom in df_info_joueurs['name'] if joueur(nom).a_joue(year_compare)]
        self.selected_joueur_compare.set(joueurs_annee_compare[0] if joueurs_annee_compare else "")
        self.joueur_menu_compare['values'] = joueurs_annee_compare
        self.button_execute_compare['state'] = tk.NORMAL if joueurs_annee_compare else tk.DISABLED


    def execute_comparison(self):
        # Obtenez les noms et années des joueurs sélectionnés pour la comparaison
        player1_name = self.selected_joueur.get()
        player2_name = self.selected_joueur_compare.get()
        year1 = int(self.selected_annee.get())
        year2 = int(self.selected_annee_compare.get())

        # Générer et afficher le graphique de comparaison
        self.generate_comparison_radar_chart(player1_name, player2_name, year1, year2)

    def generate_comparison_radar_chart(self, player1_name, player2_name, year1, year2):
        def prepare_player_data(player_name, year):
            player_info = df_info_joueurs[df_info_joueurs['name'] == player_name]
            if player_info.empty or str(year) not in player_info or pd.isna(player_info[str(year)].values[0]):
                print(f"No data available for {player_name} in {year}.")
                return None

            year_data_str = player_info[str(year)].values[0]
            if year_data_str:  # Assurez-vous que la chaîne n'est pas vide
                year_data_dict = ast.literal_eval(year_data_str)
                if year_data_dict:  # Assurez-vous que le dictionnaire n'est pas None
                    year_data_dict = self.convert_percentages_to_decimals(year_data_dict)
                    filtered_data = {key: year_data_dict[key] for key in keys_to_plot if key in year_data_dict}
                    return filtered_data
            return None

        keys_to_plot = [
            'pourc_return_win_pnt', 'pourc_break_games', 'pourc_break_point_made',
            'pourc_break_point_saved', 'pourc_serv_games_win', 'pourc_serv_in']


        player1_data_year1 = prepare_player_data(player1_name, year1)
        player2_data_year2 = prepare_player_data(player2_name, year2)

        if any(data is None for data in [player1_data_year1, player2_data_year2]):
            return  None

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        radar_chart1_y1 = PlayerRadarChart(player1_data_year1)
        radar_chart2_y2 = PlayerRadarChart(player2_data_year2)

        radar_chart1_y1.plot_on_ax(ax, 'red', f'{player1_name} {year1}')
        radar_chart2_y2.plot_on_ax(ax, 'orange', f'{player2_name} {year2}')

        ax.legend(loc='upper right')
        ax.set_xticks(radar_chart1_y1.angles[:-1])
        ax.set_xticklabels(radar_chart1_y1.categories, color='grey', size=8)  # Ajoutez des étiquettes de catégorie
        plt.title(f'Comparison: {player1_name} vs {player2_name} ({year1} vs {year2})', size=15)
        
        self.plot_figure(fig)  # Utilisez la méthode existante pour afficher la figure dans votre application Tkinter


                
    def convert_percentages_to_decimals(self, data_dict):
        for key, value in data_dict.items():
            if isinstance(value, str) and '%' in value:
                data_dict[key] = float(value.strip('%')) / 100
        return data_dict


    def plot_figure(self, figure):
        # Créer une nouvelle fenêtre pop-up
        new_window = tk.Toplevel(self.root)
        new_window.title("Graphique")

        # Ajouter le graphique à la fenêtre pop-up
        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    


# Créez la fenêtre principale Tkinter
root = tk.Tk()

# Instanciez l'application JoueurApp
app = JoueurApp(root)

# Lancer la boucle principale Tkinter
root.mainloop()
