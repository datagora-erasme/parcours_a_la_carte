"""
Détours induits par chaque critère par rapport au plus court chemin.
Sorties : output/detours_{criteres}.html (un par critère)
    -> le calcul étant lourd, faire tourner le code uniquement sur les critères d'intérêt et pas sur tout
"""
import gzip
import pickle
import sys
from collections import defaultdict
from pathlib import Path
import folium
import geopandas as gpd
import networkx as nx
import osmnx as ox
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) # -> analytics/
from common import load_requetes, GRAPH_DIR, OUTPUT_DIR

centre_lyon = [45.75, 4.85]

# Critère et sa fonction de poids
# Fonction trouvé de backend/global_variable.py
POIDS_CRITERE = {
    "pollen": "score_distance_pollen",
    "frais": "score_distance_13",
    "bruit": "score_distance_bruit",
    "tourisme": "score_distance_tourisme",
}

def charge_graphes():
    """Charge le graphe et le multidigraph"""
    with gzip.open(GRAPH_DIR/"merged_network.pickle.gz", "rb") as f:
        graph = pickle.load(f)
    with gzip.open(GRAPH_DIR/"merged_network_multidigraph.pickle.gz", "rb") as f:
        multidigraph = pickle.load(f)
    return graph, multidigraph

def compte_segments(df, graph, multidigraph, poids):
    """Compte l'usage de chaque segment pour l'itinéraire  'poids' et pour 'length'"""
    origines = ox.nearest_nodes(graph, X=df["start_lon"].to_numpy(), Y=df["start_lat"].to_numpy())
    destinations = ox.nearest_nodes(graph, X=df["end_lon"].to_numpy(), Y=df["end_lat"].to_numpy())

    count_critere = defaultdict(int)
    count_lenghth = defaultdict(int)
    geometries = {}

    for o, d in zip(origines, destinations):
        for poids_col, compteur in [(poids, count_critere), ("length", count_lenghth)]:
            try:
                chemin = nx.shortest_path(graph, o, d, weight=poids_col)
            except nx.NetworkXNoPath:
                continue
            aretes = ox.utils_graph.get_route_edge_attributes(multidigraph, chemin)
            gdf = gpd.GeoDataFrame(aretes, crs=graph.graph["crs"], geometry="geometry").to_crs(epsg=4326)
            for _, arete in gdf.iterrows():
                cle = arete.geometry.wkt
                compteur[cle] += 1
                geometries[cle] = arete.geometry
    return count_critere, count_lenghth, geometries

def carte_detours(count_critere, count_length, geometries, critere):
    """Carte des segments évités (rouge) / détournés (vert) par le critère"""
    m = folium.Map(location=centre_lyon, zoom_start=13, tiles="CartoDB positron")
    max_length = max(count_length.values(), default=1)
    max_critere = max(count_critere.values(), default=1)
        
    for cle in set(count_critere) | set(count_length):
        diff = count_length.get(cle, 0) - count_critere.get(cle, 0)
        if diff == 0:
            continue
        coords = [(lat, lon) for lon, lat in geometries[cle].coords]
        if diff > 0:
            color, ref = "#d73027", max_length
            tooltip = f"Évité {critere} : {diff} trajets de moins"
        else:
            color, ref = "#1a9850", max_critere
            tooltip = f"Détour {critere} : {abs(diff)} trajets de plus"
        folium.PolyLine(coords, weight=1 + 4*(abs(diff)/ref), color=color, opacity=0.3 + 0.6*(abs(diff) / ref), tooltip=tooltip).add_to(m)

    legend = f"""
    <div style="position:fixed; bottom:30px; left:30px; z-index:1000;
        background:white; padding:12px 16px; border-radius:8px;
        box-shadow:0 2px 8px rgba(0,0,0,0.2); font-family:sans-serif; font-size:12px;">
    <span style="color:#d73027">—</span> Segment évité par {critere}<br>
    <span style="color:#1a9850">—</span> Détour {critere}
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend))
    return m

def genere_detours(df, graph, multidigraph, critere):
    """Calcule et sauvegarde la carte des détours pour un critère"""
    df_c = df[df["criteria"].str.contains(critere)]
    count_c, count_l, geoms = compte_segments(df_c, graph, multidigraph, POIDS_CRITERE[critere])
    sortie = OUTPUT_DIR/f"detours_{critere}.html"
    carte_detours(count_c, count_l, geoms, critere).save(str(sortie))

def main(criteres=None):
    criteres = criteres or list(POIDS_CRITERE)
    df = load_requetes()
    graph, multidigraph = charge_graphes()
    for critere in criteres:
        genere_detours(df, graph, multidigraph, critere)

if __name__ == "__main__":
    demandes = [c for c in sys.argv[1:] if c in POIDS_CRITERE]
    main(demandes or None)