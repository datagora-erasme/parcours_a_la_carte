import os
from pathlib import Path
import sys
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import osmnx as ox
from global_variable import *
import pickle
import gzip
import networkx as nx

def prepare_edges():
    # Charger les fichiers GPKG
    frais = gpd.read_file(edges_buffer_total_score_distance_freshness_path)
    tourisme = gpd.read_file(edges_buffer_total_score_distance_tourisme_path)
    bruit = gpd.read_file(edges_buffer_total_score_distance_bruit_path)
    pollen = gpd.read_file(edges_buffer_total_score_distance_pollen_path)
    pollen_fevmai = gpd.read_file(edges_buffer_total_score_distance_pollen_fevmai_path)

    # Afficher les colonnes avant fusion
    print("Colonnes de frais:", frais.columns)
    print("Colonnes de tourisme:", tourisme.columns)
    print("Colonnes de bruit:", bruit.columns)
    print("Colonnes de pollen:", pollen.columns)
    print("Colonnes de pollen_fevmai:", pollen_fevmai.columns)

    # Liste des fichiers supplémentaires et colonnes à ajouter
    fichiers = [
        (tourisme, [graph_columns["tourisme"]["score_weigth"], graph_columns["tourisme"]["score_value"]]),
        (bruit, [graph_columns["bruit"]["score_weigth"], graph_columns["bruit"]["score_value"]]),
        (pollen, [graph_columns["pollen"]["score_weigth"], graph_columns["pollen"]["score_value"]]),
        (pollen_fevmai, [graph_columns["pollen_fevmai"]["score_weigth"], graph_columns["pollen_fevmai"]["score_value"]]),
    ]

    df_final = frais.copy()
    for df, cols in fichiers:
        # Vérifier que les fichiers secondaires ont bien les colonnes "u", "v", "key"
        df_subset = df[["u", "v", "key", "geometry"] + cols]
        df_final = df_final.merge(df_subset, on=["u", "v", "key", "geometry"], how="left")

    # Liste des colonnes à conserver après fusion
    column = ["u", "v", "key", "osmid", "length", "from", "to", "geometry",
              graph_columns["frais"]["score_weigth"], graph_columns["frais"]["score_value"],
              graph_columns["tourisme"]["score_weigth"], graph_columns["tourisme"]["score_value"],
              graph_columns["bruit"]["score_weigth"], graph_columns["bruit"]["score_value"],
              graph_columns["pollen"]["score_weigth"], graph_columns["pollen"]["score_value"],
              graph_columns["pollen_fevmai"]["score_weigth"], graph_columns["pollen_fevmai"]["score_value"]
    ]
    # Sélectionner uniquement les colonnes nécessaires
    df_final = df_final[column]

    # Vérification des colonnes après filtrage
    print("Colonnes finales après filtrage:", df_final.columns)

    # Nombre de lignes après filtrage
    print(f"Nombre de lignes : {len(df_final)}")

    # Sauvegarde en GPKG
    df_final.to_file(edges_buffer_merged_network_path, driver="GPKG")
    print(f"Fichier sauvegardé avec succès : {edges_buffer_merged_network_path}")


def create_graph():
    global graph_columns
    """Create a graph with applied noise scores and save only edges and nodes layers"""

    # Charger les nœuds et arêtes du graphe initial
    graph_e = gpd.read_file(metrop_network_bouding_path, layer="edges")
    graph_n = gpd.read_file(metrop_network_bouding_path, layer="nodes")

    # Charger les scores (edges_buffered_data)
    edges_buffered_data = gpd.read_file(edges_buffer_merged_network_path)

    # Mettre les index sur les bonnes colonnes
    graph_e = graph_e.set_index(["u", "v", "key"])
    edges_buffered_data = edges_buffered_data.set_index(["u", "v", "key"])
    graph_n = graph_n.set_index(["osmid"])

    # Appliquer les scores aux arêtes
    for col in [
            graph_columns["frais"]["score_weigth"], graph_columns["frais"]["score_value"],
            graph_columns["tourisme"]["score_weigth"], graph_columns["tourisme"]["score_value"],
            graph_columns["bruit"]["score_weigth"], graph_columns["bruit"]["score_value"],
            graph_columns["pollen"]["score_weigth"], graph_columns["pollen"]["score_value"],
            graph_columns["pollen_fevmai"]["score_weigth"], graph_columns["pollen_fevmai"]["score_value"]
        ]:
        
        if col in edges_buffered_data.columns:  # Vérifier si la colonne existe avant d'appliquer
            graph_e[col] = edges_buffered_data[col]

    # Générer le graphe
    G = ox.graph_from_gdfs(graph_n, graph_e)

    # Supprimer l'ancien fichier s'il existe
    if Path(merged_network_graph_path).exists():
        os.remove(merged_network_graph_path)

    # Extraire les nouveaux nœuds et arêtes
    graph_n, graph_e = ox.graph_to_gdfs(G)

    # Sauvegarder uniquement les couches `edges` et `nodes`
    graph_n.to_file(merged_network_graph_path, layer="nodes", driver="GPKG")
    graph_e.to_file(merged_network_graph_path, layer="edges", driver="GPKG")

    print(f"Le fichier {merged_network_graph_path} contient uniquement les couches 'edges' et 'nodes'.")
    

def create_pickles():
    """
    Load a graph into pickle files.
    Both simple graph and multidigraph are needed for the function shortest_path of the project.

    Parameters:
    - graph_path: str, path to the graph file.
    - graph_pickle_path: str, path to save the simple graph pickle file.
    - graph_multidigraph_pickle_path: str, path to save the multidigraph pickle file.
    - score_type: str, type of score ('pollen' or 'bruit') to be used for specific columns.
    """
    print(datetime.now(), f"Pickle file creation start")

    gdf_edges = gpd.read_file(merged_network_graph_path, layer='edges')
    gdf_nodes = gpd.read_file(merged_network_graph_path, layer="nodes")

    gdf_nodes["y"] = gdf_nodes["lat"]
    gdf_nodes["x"] = gdf_nodes["lon"]
    gdf_nodes["geometry"] = gpd.points_from_xy(gdf_nodes["x"], gdf_nodes["y"])  # Fix warning

    new_edges = gdf_edges[
        ["u", "v", "key", "osmid", "length", "from", "to", "geometry",
         graph_columns["frais"]["score_weigth"], graph_columns["frais"]["score_value"],
         graph_columns["tourisme"]["score_weigth"], graph_columns["tourisme"]["score_value"],
         graph_columns["bruit"]["score_weigth"], graph_columns["bruit"]["score_value"],
         graph_columns["pollen"]["score_weigth"], graph_columns["pollen"]["score_value"],
         graph_columns["pollen_fevmai"]["score_weigth"], graph_columns["pollen_fevmai"]["score_value"]
        ]
    ]
    new_edges = new_edges.set_geometry("geometry")
    new_edges.to_crs(gdf_edges.crs)
    
    new_edges = new_edges.set_index(["u", "v", "key"])
    gdf_nodes = gdf_nodes.set_index(['osmid'])

    G = ox.graph_from_gdfs(gdf_nodes, new_edges)

    G2 = nx.Graph(G)
    G_digraph = nx.MultiDiGraph(G2)

    with gzip.open(f"{merged_network_pickle_path}.gz", mode="wb") as file:
        pickle.dump(G2, file, protocol=5)

    with gzip.open(f"{merged_network_multidigraph_pickle_path}.gz", mode="wb") as file:
        pickle.dump(G_digraph, file, protocol=5)
    
    print(datetime.now(), f"Pickle file creation end")

prepare_edges()
create_graph()
create_pickles()