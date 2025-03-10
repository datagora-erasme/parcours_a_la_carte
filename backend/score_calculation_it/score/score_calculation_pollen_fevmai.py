import os
import sys
import geopandas as gpd
import numpy as np

# Ajouter les chemins relatifs pour l'import des modules
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")

# Désactiver PyGEOS pour compatibilité
os.environ['USE_PYGEOS'] = '0'

from function_utils import *
from global_variable import *

#  GLOBAL VARIABLES 
score_columns_pollen = ["score_pollen_fevmai_arbres_weight", "score_pollen_fevmai_parcs_prop"]

#  FUNCTIONS 

def create_uniqID(x):
    """OSMNX inverse certains 'u' et 'v' lors de la création du graphe => créer un identifiant unique."""
    return str(x["u"]) + str(x["v"]) + str(x["key"])


def all_prop(input_path, params, output_path):
    """Crée un fichier contenant toutes les propriétés fusionnées."""
    edges = gpd.read_file(input_path)
    edges["uniqId"] = edges.apply(create_uniqID, axis=1)
    edges = edges.set_index(["u", "v", "key"])

    for dataname, dataprops in params.items():
        data = gpd.read_file(dataprops["edges_path"])
        data = data.set_index(["u", "v", "key"])
        edges[dataname] = data[dataname]

    edges.to_file(output_path, driver="GPKG")
    print(f" Fichier fusionné enregistré : {output_path}")


def total_score(input_path, output_path, score_columns):
    """Calculation of the total pollen score based on the specified columns"""
    edges_data = gpd.read_file(input_path)

    print(f"Columns in {input_path} : {edges_data.columns}")
    edges_data["total_score_pollen_fevmai"] = edges_data[score_columns].sum(axis=1) + 1
    print(f"Calculation of total_score_pollen_fevmai completed.")

    # Save the score file
    edges_data.to_file(output_path, driver="GPKG")
    print(f"The score file has been saved at {output_path}.")


def all_score_edges(input_path, output_path, params):
    """Applique des scores aux arêtes du graphe en fonction des paramètres définis."""
    default_edges = gpd.read_file(input_path)
    print(f" Colonnes avant traitement : {default_edges.columns}")

    for data_name, data_param in params.items():
        print(f" Ajout du score {data_name}...")
        data = gpd.read_file(data_param["edges_path"])
        default_edges[f"score_pollen_fevmai_{data_name}"] = data[data_name].apply(data_param["fn_cont"])

    default_edges.to_file(output_path, driver="GPKG")
    print(f" Fichier enregistré avec scores : {output_path}")


def score_distance(input_path, output_path):
    """Calcule le score pondéré par la distance des arêtes."""
    edges = gpd.read_file(input_path)
    edges["score_distance_pollen_fevmai"] = edges["total_score_pollen_fevmai"] * edges["length"]
    print(f" Calcul du score pondéré par la distance terminé.")

    edges.to_file(output_path, driver="GPKG")
    print(f" Fichier enregistré avec score de distance : {output_path}")


def score_pollen(input_path, output_path):
    """Calculate a pollen score from 0 to 10 using log transformation"""
    edges_data = gpd.read_file(input_path)

    # Appliquer une transformation logarithmique pour éviter l'effet d'écrasement des petits scores
    edges_data["total_score_pollen_fevmai_log"] = np.log1p(edges_data["total_score_pollen_fevmai"])

    # Obtenir min et max après transformation
    min_score = edges_data["total_score_pollen_fevmai_log"].min()
    max_score = edges_data["total_score_pollen_fevmai_log"].max()

    if min_score == max_score:
        print("⚠️ Aucun écart dans les scores après transformation logarithmique. Tous les scores seront mis à 0.")
        edges_data["pollen_fevmai_score"] = 0
    else:
        # Normalisation linéaire sur [0,10] après transformation logarithmique
        slope = (0 - 10) / (max_score - min_score)
        origin_ordinate = -slope * max_score
        edges_data["pollen_fevmai_score"] = edges_data["total_score_pollen_fevmai_log"].apply(lambda x: round(slope * x + origin_ordinate, 2))

    print(f" Calculation of pollen_fevmai_score completed.")

    # Sauvegarde du fichier
    edges_data.to_file(output_path, driver="GPKG")
    print(f"The pollen_fevmai_score file has been saved at {output_path}.")


#  PARAMÈTRES DE TRAITEMENT 
params = {
    "arbres_weight": {
        "edges_path": edges_buffer_arbres_pollen_prop_path_fevmai,
        "fn_cont": lambda x: x,
        "alpha": 1
    },
    "parcs_prop": {
        "edges_path": edges_buffer_parcs_pollen_prop_path,
        "fn_cont": lambda x: 1 * x,
        "alpha": 1
    },
}

#  EXÉCUTION DU PIPELINE 
all_score_edges(edges_buffer_path, edges_buffer_scored_path, params)
total_score(edges_buffer_scored_path, edges_buffer_total_score_path, score_columns_pollen)
score_distance(edges_buffer_total_score_path, edges_buffer_total_score_distance_path)
score_pollen(edges_buffer_total_score_distance_path, edges_buffer_total_score_distance_pollen_fevmai_path)
