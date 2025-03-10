import pandas as pd 
from pathlib import Path
import networkx as nx
import numpy as np
from concurrent.futures import ThreadPoolExecutor
def load_itineraires_from_csv(file_path: str) -> pd.DataFrame:
    """
    Load itinéraires in pandas DataFrame
    """
    # Charger le fichier CSV contenant les itinéraires optimisés en distance
    file_path = Path(file_path)
    itineraire = pd.read_csv(file_path)

    return itineraire


def check_required_columns(df: pd.DataFrame, required_columns: set) -> None:
    """
    Vérifier que les colonnes nécessaires existent dans le DataFrame.
    """
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Les colonnes suivantes sont manquantes dans le fichier edges : {missing_columns}")


def build_graph(edges: pd.DataFrame, weight_column: str, length_column: str, directed: bool = True) -> nx.Graph:
    G = nx.DiGraph() if directed else nx.Graph()

    for _, row in edges.iterrows():
        G.add_edge(row['u'], row['v'], **{
            weight_column: row.get(weight_column, 0),  # ✅ Utiliser `.get()` pour éviter une erreur
            "length": row.get(length_column, 0)
        })
    return G


def check_valid_routes(df: pd.DataFrame, graph: nx.Graph, start_col: str, end_col: str) -> pd.DataFrame:
    """
    Filtrer les itinéraires pour ne garder que ceux dont les nœuds de départ et d'arrivée existent dans le graphe.
    """
    nodes_in_graph = set(graph.nodes)
    return df[df[start_col].isin(nodes_in_graph) & df[end_col].isin(nodes_in_graph)]

def compute_all_itineraries(graph: nx.Graph, df: pd.DataFrame, start_col: str, end_col: str, weight_attr: str) -> list:
    """
    Calcule les itinéraires minimisant un critère donné (bruit ou distance) pour toutes les paires start-end du DataFrame.
    """
    def compute_shortest_path(start, end):
        """Calcule le chemin optimal entre deux nœuds selon `weight_attr`."""
        try:
            path = nx.shortest_path(graph, source=start, target=end, weight=weight_attr)
            total_score = sum(graph[path[i]][path[i+1]][weight_attr] for i in range(len(path)-1))
            total_distance = sum(graph[path[i]][path[i+1]]["length"] for i in range(len(path)-1))
            return total_score, total_distance
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return np.nan, np.nan  # Aucun chemin trouvé

    # Récupérer toutes les paires (start, end) du DataFrame
    start_end_pairs = list(zip(df[start_col], df[end_col]))

    # Exécuter en parallèle pour accélérer le calcul
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda pair: compute_shortest_path(pair[0], pair[1]), start_end_pairs))

    return results  # Retourne la liste des résultats au lieu de modifier df

def add_results_to_dataframe(df: pd.DataFrame, results: list, score_col: str, distance_col: str) -> pd.DataFrame:
    """
    Ajoute les résultats des itinéraires au DataFrame.
    """
    df[score_col], df[distance_col] = zip(*results)
    return df

def remove_invalid_routes(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Supprime les itinéraires où aucun chemin n'a été trouvé (valeurs NaN dans les colonnes spécifiées).
    """
    return df.dropna(subset=columns)

def reorder_columns(df: pd.DataFrame, column_order: list) -> pd.DataFrame:
    """
    Réorganise les colonnes du DataFrame selon un ordre donné.
    """
    return df[column_order]

def save_and_display_results(df: pd.DataFrame, filename: str) -> None:
    """
    Sauvegarde le DataFrame dans un fichier CSV et affiche un message de confirmation.
    """
    df.to_csv(filename, index=False)
    print(f"\n Calcul terminé : {len(df)} itinéraires enregistrés dans '{filename}' !")
    print("Colonnes 'distance_court', 'bruit_court', 'distance_bruit', et 'bruit_score' ajoutées et réorganisées avec succès.")
