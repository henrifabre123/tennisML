import pandas as pd
import tensorflow
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.metrics import accuracy_score
import joblib




#On commence par formater les données
# Chargement des données
base_path = './Data/Data_utiles/Data_ML/'

# Liste pour stocker chaque DataFrame
dataframes = []

# Boucle pour lire chaque fichier CSV de 1995 à 2018
for year in range(1995, 2022):
    file_path = f'{base_path}infos_joueurs_{year}.csv'
    df = pd.read_csv(file_path)
    dataframes.append(df)

# Concaténer tous les DataFrames en un seul
data = pd.concat(dataframes, ignore_index=True)

#On supprime hand (car la proportion de gauchers est trop faible), name, et rang
columns = [
    "height", "matchs", "win",
    "pourc_return_win_pnt", "pourc_break_games", "pourc_break_point_made",
    "pourc_break_point_saved", "pourc_serv_games_win", "pourc_serv_in",
    "mean_ranking_oppo", "pourc_serv_win_pnt", "Under Pressure Rating",
    " % Break Point Saved", " % Break Points Converted Pressure",
    " % Deciding Sets Won", " % Tie Breaks Won","atp_points"
]


df = pd.DataFrame(data, columns=columns)

#On supprime les joueurs qui ont 0 atp_points

df=df[df['atp_points']!=0]



#certains joueurs du dataset ont des infos manquantes pour les stats des services.
#On va donc créer 2 datasets : un avec les valeurs des services pour ceux qui peuvent
# un en supprimant les stats des services mais en gardant tous les joueurs

# Dataset avec tous les joueurs
df_all_players = df.copy()

df_all_players = df_all_players.drop(['Under Pressure Rating',
       ' % Break Point Saved', ' % Break Points Converted Pressure',
       ' % Deciding Sets Won', ' % Tie Breaks Won'], axis=1)

y_all_players = df_all_players['atp_points']
df_all_players = df_all_players.drop('atp_points', axis=1)

# Dataset seulement avec les joueurs qui ont des stats pour les services
df.dropna(inplace=True)

y = df['atp_points']
df = df.drop('atp_points', axis=1)


# Séparation des données en ensembles d'entraînement et de test

X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=30)

X_all_players_train, X_all_players_test, y_all_players_train, y_all_players_test = train_test_split(df_all_players, y_all_players, test_size=0.2, random_state=30)

print(X_train.columns)
# Pour le cas où on a supprimé une partie des joueurs, on va faire une régression Ridge car c'est un modèle qui
#s'adapte bien quand il y a assez peu de données et beaucoup de caractéristiques (ce qui est notre cas)

"""*********************************************** Reégression Ridge *********************************************** """

from sklearn.model_selection import GridSearchCV

# Définir la grille des hyperparamètres à tester
param_grid = {'alpha': [0.1, 1.0, 10.0]}

# Initialiser le modèle Ridge
ridge_model = Ridge()

# Recherche par grille des hyperparamètres
grid_search = GridSearchCV(ridge_model, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# Meilleurs hyperparamètres
best_alpha = grid_search.best_params_['alpha']
print(f"Meilleur paramètre alpha : {best_alpha}")

# Utiliser le meilleur modèle
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# Évaluation du modèle
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Squared Error (MSE) après réglage des hyperparamètres : {mse}")
print(f"Root Mean Squared Error (RMSE) après réglage des hyperparamètres : {rmse}")


#On sauvegarde le modèle
joblib.dump(best_model, './Modeles_ML/ridge_model.pkl')

"""On fait de même avec le dataset avec tous les joueurs """

# Initialiser le modèle Ridge
ridge_model = Ridge()

# Recherche par grille des hyperparamètres
grid_search = GridSearchCV(ridge_model, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_all_players_train, y_all_players_train)

# Meilleurs hyperparamètres
best_alpha = grid_search.best_params_['alpha']
print(f"Meilleur paramètre alpha : {best_alpha}")

# Utiliser le meilleur modèle
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_all_players_test)

# Évaluation du modèle
mse = mean_squared_error(y_all_players_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Squared Error (MSE) après réglage des hyperparamètres : {mse}")
print(f"Root Mean Squared Error (RMSE) après réglage des hyperparamètres : {rmse}")


#On sauvegarde le modèle
joblib.dump(best_model, './Modeles_ML/all_players_ridge_model.pkl')

"""*********************************************** SVM *********************************************** """

# Initialisation et entraînement du modèle SVM pour la régression
svm_model = SVR(kernel='linear', C=1.0)  # 'linear' est utilisé ici pour une SVM linéaire, ajustez le noyau selon vos besoins
svm_model.fit(X_train, y_train)

# Prédictions sur l'ensemble de test
y_pred = svm_model.predict(X_test)

# Évaluation du modèle
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Squared Error (MSE) avec SVM : {mse}")
print(f"Root Mean Squared Error (RMSE) avec SVM : {rmse}")

# Sauvegarder le modèle SVM
joblib.dump(svm_model, './Modeles_ML/svm_model.pkl')

""" on fait de même avec le dataset qui contient tous les joueurs """

svm_model = SVR(kernel='linear', C=1.0)  # 'linear' est utilisé ici pour une SVM linéaire, ajustez le noyau selon vos besoins
svm_model.fit(X_all_players_train, y_all_players_train)

# Prédictions sur l'ensemble de test
y_pred = svm_model.predict(X_all_players_test)

# Évaluation du modèle
mse = mean_squared_error(y_all_players_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Squared Error (MSE) avec SVM : {mse}")
print(f"Root Mean Squared Error (RMSE) avec SVM : {rmse}")

# Sauvegarder le modèle SVM
joblib.dump(svm_model, './Modeles_ML/all_players_svm_model.pkl')


"""*********************************************** Réseau de Neurones  *********************************************** """

#Normalisation des données


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(X_train.columns)
print(X_train.shape)

# Construction du modèle de réseau de neurones
model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1))  # Couche de sortie sans activation pour la régression

# Compilation du modèle
model.compile(optimizer='adam', loss='mean_squared_error')

# Entraînement du modèle
model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, validation_split=0.2)

# Évaluation du modèle sur l'ensemble de test
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Squared Error (MSE) avec le réseau de neurones : {mse}")
print(f"Root Mean Squared Error (RMSE) avec le réseau de neurones : {rmse}")

# Sauvegarder le modèle de réseau de neurones
model.save('./Modeles_ML/neural_network_model.keras')


""" On fait de même avec le datasets qui contient tous les joueurs """

#scaler = StandardScaler()
#X_train_scaled = scaler.fit_transform(X_all_players_train)
#X_test_scaled = scaler.transform(X_all_players_test)

# Construction du modèle de réseau de neurones
model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(X_all_players_train.shape[1],)))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1))  # Couche de sortie sans activation pour la régression


# Compilation du modèle
model.compile(optimizer='adam', loss='mean_squared_error')

# Entraînement du modèle
model.fit(X_all_players_train, y_all_players_train, epochs=100, batch_size=32, validation_split=0.2)

# Évaluation du modèle sur l'ensemble de test
y_pred = model.predict(X_all_players_test)
mse = mean_squared_error(y_all_players_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Squared Error (MSE) avec le réseau de neurones : {mse}")
print(f"Root Mean Squared Error (RMSE) avec le réseau de neurones : {rmse}")

# Sauvegarder le modèle de réseau de neurones
model.save('./Modeles_ML/all_players_neural_network_model.keras')

#
