import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import joblib





# Chargement et préparation des données
base_path = './Data/Data_utiles/Data_ML/'
dataframes = []

for year in range(1995, 2022):
    file_path = f'{base_path}infos_joueurs_{year}.csv'
    df = pd.read_csv(file_path)
    dataframes.append(df)

data = pd.concat(dataframes, ignore_index=True)

columns = [
    "height", "matchs", "win",
    "pourc_return_win_pnt", "pourc_break_games", "pourc_break_point_made",
    "pourc_break_point_saved", "pourc_serv_games_win", "pourc_serv_in",
    "mean_ranking_oppo", "pourc_serv_win_pnt", "Under Pressure Rating",
    " % Break Point Saved", " % Break Points Converted Pressure",
    " % Deciding Sets Won", " % Tie Breaks Won", "rang"
]

df = pd.DataFrame(data, columns=columns)
df = df[df['rang'] != 0]  # Remplacer 'atp_points' par 'rang'

# Préparation des jeux de données
df_all_players = df.copy()
df_all_players = df_all_players.drop(['Under Pressure Rating',
                                      ' % Break Point Saved', ' % Break Points Converted Pressure',
                                      ' % Deciding Sets Won', ' % Tie Breaks Won'], axis=1)

y = df_all_players['rang']
df = df_all_players.drop('rang', axis=1)
df.dropna(inplace=True)


X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=30)


"""*********************************************** Régression Ridge **********************************************"""
param_grid = {'alpha': [0.1, 1.0, 10.0]}
ridge_model = Ridge()
grid_search = GridSearchCV(ridge_model, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

y_pred=best_model.predict(X_test)
# Évaluation du modèle
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Squared Error (MSE) après réglage des hyperparamètres : {mse}")
print(f"Root Mean Squared Error (RMSE) après réglage des hyperparamètres : {rmse}")

joblib.dump(best_model, './Modeles_ML/rang_ridge_model.pkl')


"""*********************************************** SVM **********************************************"""

svm_model = SVR(kernel='linear', C=1.0)
svm_model.fit(X_train, y_train)

y_pred=svm_model.predict(X_test)
# Évaluation du modèle
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Squared Error (MSE) avec SVM : {mse}")
print(f"Root Mean Squared Error (RMSE) avec SVM : {rmse}")

# Sauvegarder le modèle SVM
joblib.dump(svm_model, './Modeles_ML/rang_svm_model.pkl')



"""*********************************************** Réseau de neurones **********************************************"""


model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Squared Error (MSE) avec le réseau de neurones : {mse}")
print(f"Root Mean Squared Error (RMSE) avec le réseau de neurones : {rmse}")

print(y_pred)
model.save('./Modeles_ML/rang_neural_network_model.keras')

# Note: Répétez les étapes ci-dessus pour le jeu de données `X_all_players_train` si nécessaire
