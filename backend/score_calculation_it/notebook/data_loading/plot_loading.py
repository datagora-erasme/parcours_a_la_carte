import pandas as pd 
import matplotlib as plt
import numpy as np



def plot_histogram(df, col_x, col_y, binwidth=150, xlabel="Distance (m)", ylabel="Densité", title="Comparaison des distributions (Histogramme)"):
    """
    Génère un histogramme comparant deux colonnes spécifiques d'un DataFrame,
    en commençant à la plus petite valeur trouvée dans les colonnes sélectionnées.

    Paramètres :
    - df : DataFrame contenant les données.
    - col_x : Nom de la première colonne à comparer.
    - col_y : Nom de la deuxième colonne à comparer.
    - binwidth : Largeur des bins pour l'histogramme (par défaut 150).
    - xlabel : Label pour l'axe des X.
    - ylabel : Label pour l'axe des Y.
    - title : Titre du graphique.
    """
    min_val = min(df[col_x].min(), df[col_y].min())  
    max_val = max(df[col_x].max(), df[col_y].max())  
    
    # Définir des bins communs avec un binwidth fixe
    bins = np.arange(min_val, max_val + binwidth, binwidth)

    plt.figure(figsize=(12, 6))
    plt.hist(df[col_x], bins=bins, alpha=1, label=col_x, color="blue", density=True, histtype="step", linewidth=2)
    plt.hist(df[col_y], bins=bins, alpha=1, label=col_y, color="red", density=True, histtype="step", linewidth=2)

    plt.xlim(min_val, max_val) 
    plt.xlabel(xlabel)  # Utilisation du paramètre xlabel
    plt.ylabel(ylabel)  # Utilisation du paramètre ylabel
    plt.title(title)  # Utilisation du paramètre title
    plt.legend()
    plt.show()


def plot_scatter(df, col_x, col_y, label_x="Colonne X", label_y="Colonne Y", title="Comparaison des distances (Scatter Plot)"):
    """
    Génère un scatter plot comparant deux colonnes spécifiques d'un DataFrame.
    """
     # Trouver le min et le max des deux colonnes pour ajuster l'affichage
    min_val = min(df[col_x].min(), df[col_y].min())
    max_val = max(df[col_x].max(), df[col_y].max())

    plt.figure(figsize=(12, 6))
    plt.scatter(df[col_x], df[col_y], alpha=0.5, label="Itinéraires", color="purple", edgecolors="black")
    
    # Tracer la ligne de référence x = y
    plt.plot([min_val, max_val], [min_val, max_val], color="red", linestyle="dashed", label="x = y")

    # Ajuster les limites des axes
    plt.xlim(min_val, max_val)
    plt.ylim(min_val, max_val)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(title)
    plt.legend()
    plt.grid(False)  # Supprimer la grille pour un affichage plus propre
    plt.show()


def plot_qq(data, col_court="distance_court", col_score="distance_bruit"):
    """
    Génère un Q-Q plot basé sur les percentiles pour comparer les distributions de deux itinéraires.
    Ajoute des lignes reliant les points pour une meilleure lisibilité.

    Paramètres :
    - data : DataFrame contenant les colonnes de distances à comparer.
    - col_court : Nom de la colonne représentant l'itinéraire court.
    - col_score : Nom de la colonne représentant l'itinéraire minimisant le bruit.
    """
    # Liste des percentiles demandés
    percentiles = [25, 50, 75, 85, 92, 98.5]

    # Calcul des quantiles empiriques
    quantiles_court = np.percentile(data[col_court], percentiles)
    quantiles_score = np.percentile(data[col_score], percentiles)

    # Création du Q-Q plot
    plt.figure(figsize=(8, 6))
    
    # Tracer les points
    plt.scatter(percentiles, quantiles_court, color="blue", label=col_court, marker='o')
    plt.scatter(percentiles, quantiles_score, color="red", label=col_score, marker='s')

    # Relier les points avec des lignes
    plt.plot(percentiles, quantiles_court, linestyle="-", color="blue", alpha=0.7)
    plt.plot(percentiles, quantiles_score, linestyle="-", color="red", alpha=0.7)

    # Mise en forme du graphique
    plt.xticks(percentiles, [f"{p}%" for p in percentiles])  # Étiquettes en pourcentage
    plt.xlabel("Percentiles des itinéraires")
    plt.ylabel("Distance observée")
    plt.title(f"Q-Q Plot basé sur les percentiles : {col_court} vs {col_score}")
    plt.legend()
    plt.show()



    
