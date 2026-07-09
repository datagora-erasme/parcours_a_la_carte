"""
Distribution des distances des trajets (plus court chemin réel)
Sorties : output/distribution_distances.png, output/distances.csv
"""
import gzip
import pickle
import sys
from pathlib import Path
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) # -> analytics/
from common import load_requetes, GRAPH_DIR, OUTPUT_DIR

def charge_graphe():
    """Charge le graphe routier (merged_networ)"""
    with gzip.open(GRAPH_DIR/"merged_network.pickle.gz", "rb") as f:
        return pickle.load(f)

def calcule_distances(df, graph):
    """Longueur du plus court chemin (km) pour chaque requête"""
    origines = ox.nearest_nodes(graph, X=df["start_lon"].to_numpy(), Y=df["start_lat"].to_numpy())
    destinations = ox.nearest_nodes(graph, X=df["end_lon"].to_numpy(), Y=df["end_lat"].to_numpy())

    distances = []
    for o, d, ville_o, ville_d in zip(origines, destinations, df["start_city"], df["end_city"]):
        try:
            metres = nx.shortest_path_length(graph, o, d, weight="length")
            distances.append(metres / 1000)  # en km
        except nx.NetworkXNoPath:
            print(f"Aucun chemin : {ville_o} à {ville_d}")
            distances.append(None)
    return distances

def trace_histogramme(distances_km):
    """Histogramme des distances"""
    plt.figure(figsize=(10, 5))
    plt.hist(distances_km.dropna(), bins=40, color="#2c7bb6", edgecolor="white")
    plt.xlabel("Distance du plus court chemin (km)")
    plt.ylabel("Nombre de trajets")
    plt.title("Distribution des distances de trajets")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR/"distribution_distances.png", dpi=150)

def main():
    df = load_requetes()
    graph = charge_graphe()
    df["distance_km"] = calcule_distances(df, graph)

    trace_histogramme(df["distance_km"])
    df[["distance_km"]].to_csv(OUTPUT_DIR/"distances.csv", index=False)

    d = df["distance_km"]
    print(f"Distance moyenne : {d.mean():.2f} km")
    print(f"Distance médiane : {d.median():.2f} km")
    print(f"Distance max     : {d.max():.2f} km")
    print(f"Distance min     : {d.min():.2f} km")


if __name__ == "__main__":
    main()