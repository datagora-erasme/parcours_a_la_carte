from datetime import datetime
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import networkx as nx
import osmnx as ox
import json
from global_variable import merged_network_cache, merged_network_pickle_path, merged_network_multidigraph_pickle_path, graph_columns, current_month

def nearest_nodes(start, end):
    """
    Finds the nearest nodes in the graph to the given start and end coordinates.
    
    Args:
        start (tuple): The (latitude, longitude) coordinates of the starting point.
        end (tuple): The (latitude, longitude) coordinates of the ending point.
    
    Returns:
        tuple: The nearest node IDs for the start and end points.

    Notes:
        - We use this function before shortest_path for performance reasons: Since this calculation is expensive, we do it only once.
    """
    pickle_graph = merged_network_cache[merged_network_pickle_path] 

    print(datetime.now(), f"Preparing nodes start")

    origin_node = ox.nearest_nodes(pickle_graph, X=start[0], Y=start[1])
    destination_node = ox.nearest_nodes(pickle_graph, X=end[0], Y=end[1])

    print(datetime.now(), f"Preparing nodes end")

    return origin_node, destination_node


def is_fevmai_period():
    return current_month in [2, 3, 4, 5]

def shortest_path(criterion, origin_node, destination_node):
    """
    Finds the best (based on criterion) path between the given start and destination nodes.
    
    Args:
        criterion (str): The criterion to use for the path calculation.
        origin_node (int): The ID of the starting node.
        destination_node (int): The ID of the ending node.
    
    Returns:
        GeoJSON object representing the best (based on criterion) path.

    Notes:
        The term "if" is for "indicator of freshness" (i.e criterion).
    """
    cached_pickle_graph = merged_network_cache[merged_network_pickle_path]
    cached_pickle_multidigraph = merged_network_cache[merged_network_multidigraph_pickle_path]
    weight = graph_columns[criterion]["score_weigth"]

    #TODO change the weight according to the hour (8h, 13h, 18h)
    shortest_path = nx.shortest_path(cached_pickle_graph, source=origin_node, target=destination_node, weight=weight)

    route_edges = ox.utils_graph.get_route_edge_attributes(cached_pickle_multidigraph, shortest_path)

    gdf_route_edges = gpd.GeoDataFrame(route_edges, crs=cached_pickle_graph.graph['crs'], geometry='geometry')

    #epsg = 4326 is the epsg need by Leaflet in order to display the results on the map
    gdf_route_edges = gdf_route_edges.to_crs(epsg=4326)

    geojson = json.loads(gdf_route_edges.to_json())

    return geojson


def path_mean_score_criterion(criterion, geojson):
    """
    Calculates the mean score for a given criterion and GeoJSON object.
    
    Args:
        criterion (str): The criterion to calculate the mean score for.
        geojson (dict): The GeoJSON object representing the path.
    
    Returns:
        dict: A dictionary containing the mean score for the given criterion.
    """

    scores = [feature["properties"][graph_columns[criterion]["score_value"]] for feature in geojson["features"]]   
    meanScore = sum(scores) / len(scores)

    return {criterion: meanScore}


def path_mean_score_length(geojson, criteria):
    """
    Calculates the mean score for a list of criteria on a given GeoJSON object.
    
    Args:
        geojson (dict): The GeoJSON object representing the path.
        criteria (list): A list of criteria to calculate the mean score for.
    
    Returns:
        list: A list of dictionaries, where each dictionary contains the mean score for a single criterion.
    """
    score_value_length = []

    for criterion in criteria:
        score_value_length.append(path_mean_score_criterion(criterion, geojson))

    return score_value_length