import numpy as np 


def cohen_d(x, y):
    """Calcule l'effet de taille d de Cohen basé sur la moyenne et l'écart-type des différences."""
    differences = x - y  
    return np.mean(differences) / np.std(differences, ddof=1)  # Moyenne des différences / écart-type des différences


def print_statistics(df, cols):
    """
    Affiche les statistiques descriptives des colonnes spécifiées.
    """
    print("\nStatistiques Descriptives:")
    print(df[cols].describe())