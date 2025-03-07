# #%%
# import os
# import sys
# sys.path.append("../")
# sys.path.append("../../")
# sys.path.append("../../script_python")
# os.environ['USE_PYGEOS'] = '0'
# import geopandas as gpd
# import osmnx as ox
# from function_utils import *
# from global_variable import *

# #%%
# ### GLOBAL VARIABLES ###
# score_columns = ["score_pollen_arbres_weight", "score_pollen_parcs_prop"]

# ### FUNCTIONS ###

# def create_uniqID(x):
#     """OSMNX invert some u and v when creating graph => create uniqId in order to make the analyse"""
#     return str(x["u"])+str(x["v"])+str(x["key"])

# def all_prop(input_path, params, output_path):
#     """create one file with all props"""
#     edges = gpd.read_file(input_path, layer="edges")
#     edges["uniqId"] = edges.apply(create_uniqID, axis=1)
#     edges = edges.set_index(["u", "v", "key"])
#     for dataname, dataprops in params.items():
#         data = gpd.read_file(dataprops["edges_path"])
#         data = data.set_index(["u", "v", "key"])
#         edges[dataname] = data[dataname]
#     edges.to_file(output_path, layer="edges", driver="GPKG")
    
# def total_score(input_path, output_path, score_columns):
#     """
#     Calculate the total pollen score based on the specified columns and save the result to a new file.
    
#     Parameters:
#     - input_path: Path to the input data file.
#     - output_path: Path where the output file will be saved.
#     - score_columns: List of columns to sum for calculating the total score.
#     """
#     edges = gpd.read_file(input_path, layer="edges")
#     print(edges.columns)
#     edges["total_score_pollen"] = edges[score_columns] +1 
#     # edges["total_score_pollen"] = edges["total_score_pollen"].sum(axis=1) 
#     print("total score :", edges["total_score_pollen"].describe())
#     edges.to_file(output_path, driver="GPKG")

# def all_score_edges(input_path, output_path, params):
#     """
#     params : {
#         columns1 : {
#             edges_path: "path",
#             fn_cont: function(),
#             alpha: 1
#             },
#         },
#         ...
#     }
#     """
#     default_edges = gpd.read_file(input_path, layer="edges")
    
#     for data_name, data_param in params.items():
#         print(f"Score {data_name}")
#         data = gpd.read_file(data_param["edges_path"])
#         default_edges[f"score_pollen_{data_name}"] = data[data_name].apply(data_param["fn_cont"])

#     default_edges.to_file(output_path, driver="GPKG", layer="edges")

# def one_score_edges(input_path, output_path, params, key):
#     """(Re)-calculate score for one data"""
#     default_edges = gpd.read_file(input_path, layer="edges")
#     data = gpd.read_file(params[key]["edges_path"])
#     default_edges[f"score_pollen_{key}"] = data[key].apply(params[key]["fn_cont"])

#     default_edges.to_file(output_path, driver="GPKG")

# def score_distance(input_path, output_path):
#     """calculate the score by distance for each edges"""
#     edges = gpd.read_file(input_path)

#     edges["score_distance_pollen"] = edges["total_score_pollen"] * edges["length"]
#     edges["score_distance_pollen"] = edges["score_distance_pollen"].replace(0, 1)
#     print("score distance : ",edges["score_distance_pollen"].describe())

#     edges.to_file(output_path, driver="GPKG")

# def score_pollen(input_path, output_path):
#     """Score from 0 to 10 """
#     edges = gpd.read_file(input_path)

#     min_score = edges["total_score_pollen"].min()
#     max_score = edges["total_score_pollen"].max()
#     slope = (0-10)/(max_score-min_score)
#     origin_ordinate = -slope*max_score
#     edges["pollen_score"] = edges["total_score_pollen"].apply(lambda x: round(slope*x+origin_ordinate, 2))

#     edges.to_file(output_path, driver="GPKG")

# params = {
#     "arbres_weight" : {
#         "edges_path": edges_buffer_arbres_pollen_prop_path,
#         "fn_cont": lambda x: x,
#         "alpha": 1
#     },
#     "parcs_prop" : {
#         "edges_path": edges_buffer_parcs_pollen_prop_path,
#         "fn_cont": lambda x: 1*x,
#         "alpha": 1
#     },
# }

# all_score_edges(edges_buffer_path, edges_buffer_scored_path, params)
# total_score(edges_buffer_scored_path, edges_buffer_total_score_path, score_columns)
# score_distance(edges_buffer_total_score_path, edges_buffer_total_score_distance_path)
# score_pollen(edges_buffer_total_score_distance_path, edges_buffer_total_score_distance_pollen_path)


######################################################################################""

# import os
# import sys
# sys.path.append("../")
# sys.path.append("../../")
# sys.path.append("../../script_python")
# os.environ['USE_PYGEOS'] = '0'
# import geopandas as gpd
# import osmnx as ox
# from function_utils import *
# from global_variable import *


# score_columns = ["score_pollen_juijan_arbres_weight", "score_pollen_juijan_parcs_prop"]

# def total_score(input_path, output_path, score_columns):
#     """Calculation of the total pollen score based on the specified columns"""
#     edges_data = gpd.read_file(input_path)
    
#     print(f"Columns in {input_path} : {edges_data.columns}")
#     edges_data["total_score_pollen"] = edges_data[score_columns].sum(axis=1) + 1
#     print(f"Calculation of total_score_pollen completed.")

#     # Save the score file
#     edges_data.to_file(output_path, driver="GPKG")
#     print(f"The score file has been saved at {output_path}.")


# def score_distance(input_path, output_path):
#     """Calculate the score by distance for each edge, favoring shorter segments"""
#     edges_data = gpd.read_file(input_path)  

#     edges_data["score_distance_pollen"] = edges_data["total_score_pollen"] * edges_data["length"]
    
#     print(f"Calculation of score_distance_pollen completed.")

#     # Save the file with distance-weighted scores
#     edges_data.to_file(output_path, driver="GPKG")
#     print(f"The score_distance_pollen file has been saved at {output_path}.")



# def score_pollen(input_path, output_path):
#     """Calculate a pollen score from 0 to 10 using log transformation"""
#     edges_data = gpd.read_file(input_path)

#     # Appliquer une transformation logarithmique pour éviter l'effet d'écrasement des petits scores
#     edges_data["total_score_pollen_log"] = np.log1p(edges_data["total_score_pollen"])
    
#     # Obtenir min et max après transformation
#     min_score = edges_data["total_score_pollen_log"].min()
#     max_score = edges_data["total_score_pollen_log"].max()

#     # Normalisation linéaire sur [0,10] après log
#     slope = (0 - 10) / (max_score - min_score)
#     origin_ordinate = -slope * max_score

#     edges_data["pollen_score"] = edges_data["total_score_pollen_log"].apply(lambda x: round(slope * x + origin_ordinate, 2))

#     print(f" Calculation of pollen_score completed.")

#     # Sauvegarde du fichier
#     edges_data.to_file(output_path, driver="GPKG")
#     print(f"The pollen_score file has been saved at {output_path}.")


# # Execution of functions
# total_score(edges_buffer_scored_path, edges_buffer_total_score_path, score_columns)
# score_distance(edges_buffer_total_score_path, edges_buffer_total_score_distance_path)
# score_pollen(edges_buffer_total_score_distance_path, edges_buffer_total_score_distance_pollen_path)



import os
import sys
import geopandas as gpd
import numpy as np
import osmnx as ox

## Supprimer le fichier avec le meme nom "edges_buffered_scored_bounding" avant l'excution ## 
# Ajouter les chemins relatifs pour l'import des modules
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")

# Désactiver PyGEOS pour compatibilité
os.environ['USE_PYGEOS'] = '0'

from function_utils import *
from global_variable import *

#  GLOBAL VARIABLES 
score_columns_pollen = ["score_pollen_arbres_weight", "score_pollen_parcs_prop"]

# 🛠️ FUNCTIONS 🛠️

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
    edges_data["total_score_pollen"] = edges_data[score_columns].sum(axis=1) + 1
    print(f"Calculation of total_score_pollen completed.")

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
        default_edges[f"score_pollen_{data_name}"] = data[data_name].apply(data_param["fn_cont"])

    default_edges.to_file(output_path, driver="GPKG")
    print(f" Fichier enregistré avec scores : {output_path}")


def score_distance(input_path, output_path):
    """Calcule le score pondéré par la distance des arêtes."""
    edges = gpd.read_file(input_path)
    edges["score_distance_pollen"] = edges["total_score_pollen"] * edges["length"]
    print(f" Calcul du score pondéré par la distance terminé.")

    edges.to_file(output_path, driver="GPKG")
    print(f" Fichier enregistré avec score de distance : {output_path}")


def score_pollen(input_path, output_path):
    """Calculate a pollen score from 0 to 10 using log transformation"""
    edges_data = gpd.read_file(input_path)

    # Appliquer une transformation logarithmique pour éviter l'effet d'écrasement des petits scores
    edges_data["total_score_pollen_log"] = np.log1p(edges_data["total_score_pollen"])

    # Obtenir min et max après transformation
    min_score = edges_data["total_score_pollen_log"].min()
    max_score = edges_data["total_score_pollen_log"].max()

    if min_score == max_score:
        print("⚠️ Aucun écart dans les scores après transformation logarithmique. Tous les scores seront mis à 0.")
        edges_data["pollen_score"] = 0
    else:
        # Normalisation linéaire sur [0,10] après transformation logarithmique
        slope = (0 - 10) / (max_score - min_score)
        origin_ordinate = -slope * max_score
        edges_data["pollen_score"] = edges_data["total_score_pollen_log"].apply(lambda x: round(slope * x + origin_ordinate, 2))

    print(f" Calculation of pollen_score completed.")

    # Sauvegarde du fichier
    edges_data.to_file(output_path, driver="GPKG")
    print(f"The pollen_score file has been saved at {output_path}.")


#  PARAMÈTRES DE TRAITEMENT 
params = {
    "arbres_weight": {
        "edges_path": edges_buffer_arbres_pollen_prop_path,
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
score_pollen(edges_buffer_total_score_distance_path, edges_buffer_total_score_distance_pollen_path)
