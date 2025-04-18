import os
import sys 
sys.path.append("../")
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
from models.data import *
from load_graph import *
from models.itinerary import *
from global_variable import *

app = Flask(__name__)

frontend_url = os.environ.get('FRONTEND_URL')
CORS(app, origins=[frontend_url])

def preload_merged_network_graphs_in_cache():
    """    
    Preloads the merged network graph into the local cache, if not already present.
    """    
    if not are_pickle_files_in_cache():
        print(datetime.now(), f"Caching merged network graphs")
        cache_merged_network_graphs_from_pickles()


@app.route('/data/', methods=['GET'])
def get_layers():
    """
    Route for retrieving layer data used in the "Consulter la carte fraîcheur" functionality.

    This function handles requests for specific layer data based on the provided layer ID. 
    It can return either a single layer or all layers if the 'id' parameter is set to "all". 
    If no 'id' is provided, it returns all available layers.

    Parameters:
    -----------
    None

    Returns:
    --------
    - If successful, returns a JSON response with the layer data.
    - If no data is found, returns an empty response with a 404 status.
    - In case of an error, returns an empty response with a 500 status.

    Notes:
    -----
    - This function interacts with external functions: `findMany`, `findOne`.
    - The `request.args.get('id')` is used to get the 'id' parameter from the request.
    """    """Route for layers used in the "Consulter la carte fraîcheur" functionality"""
    layer_id = request.args.get('id')
    print("request", request)
    if layer_id:
        if layer_id == "all":
            print("tourisme all")
            try:
                all_id = findMany()
                data = [findOne(id["id"]) for id in all_id]
                if not data:
                    return '', 404
                return jsonify(data)
            except Exception as e:
                print(e)
                return '', 500
        else:
            print("tourisme")
            try:
                print("one layer")
                data = findOne(layer_id)
                if not data:
                    return '', 404
                return jsonify(data)
            except Exception as e:
                print(e)
                return '', 500
    else:

        try:
            results = findMany()
            return jsonify(results)
        except Exception as e:
            print(e)
            return '', 500
    
@app.route('/itinerary/', methods=['GET'])
def get_itinerary():
    """
    Route for itinerary calculation based on various criteria (e.g., "frais", "pollen", "bruit", "tourisme").
    
    This function computes itineraries between a start and end point for multiple criteria provided in the request. 
    It loads the graph based on the specified criteria and calculates two types of itineraries:
    1. The shortest path ("LENGTH").
    2. The best path based on the specific criteria (e.g., least pollen, least noise, most scenic, etc. - "IF").

    Parameters:
    -----------
    - criteria[] (list of str): A list of criteria that determine how the itinerary should be calculated.
    - start[lat] (float): Latitude of the starting point.
    - start[lon] (float): Longitude of the starting point.
    - end[lat] (float): Latitude of the destination point.
    - end[lon] (float): Longitude of the destination point.

    Returns:
    --------
    - A JSON response with a list of itinerary results for each criteria. Each result contains:
        - id: The ID for the type of itinerary (LENGTH or IF).
        - idcriteria: The ID for the criteria used (e.g., frais, pollen).
        - name: A descriptive name for the itinerary.
        - geojson: The GeoJSON path for the calculated itinerary.
        - color: A color code for displaying the itinerary on a map.

    Notes:
    -----
    - The `load_graphs` function loads the network graph based on the specified criteria.
    - The `shortest_path` function calculates the itineraries based on the loaded graph.
    - If no valid criteria are found or if an error occurs, the request will return a 500 status.
    """
    criteria_list = request.args.getlist("criteria[]")

    start_lat = request.args.get("start[lat]")
    start_lon = request.args.get("start[lon]")
    end_lat = request.args.get("end[lat]")
    end_lon = request.args.get("end[lon]")

    start = (float(start_lon), float(start_lat))
    end = (float(end_lon), float(end_lat))
    
    if (("pollen" in criteria_list) and is_fevmai_period()):
        criteria_list.remove("pollen")
        criteria_list.append("pollen_fevmai")

    print(datetime.now(), start_lat, start_lon, end_lat, end_lon, criteria_list)

    origin_node, destination_node = nearest_nodes(start, end)

    results = []
    try:
        preload_merged_network_graphs_in_cache()
        for criterion in criteria_list:
            print(datetime.now(), f"Calculating itinerary for {criterion}")

            geojson = shortest_path(criterion, origin_node, destination_node)
            path_score = path_mean_score_criterion(criterion, geojson)
            results.append({
                "id": "IF",
                "idcriteria": criterion,
                "name": graph_columns[criterion]["label"],
                "geojson": geojson, 
                "score": path_score
            })
            
        criterion = "length"
        print(datetime.now(), f"Calculating itinerary for {criterion}")
        geojson = shortest_path(criterion, origin_node, destination_node)
        path_score = path_mean_score_length(geojson, criteria_list)
        results.append({
            "id": "LENGTH",
            "idcriteria": "length",
            "name": graph_columns[criterion]["label"],
            "geojson": geojson,
            "score": path_score
        })

        return jsonify(results)
    except Exception as e:
        print('error:', e)
        return '', 500
    
@app.errorhandler(500)
def internal_server_error(e):
    """Handle internal server error (500) and shows custom HTML page"""
    print('error 500:', e)
    return render_template('./public/error500.html'), 500

@app.route('/force_error')
def force_error():
    """Route to force a 500 error for testing"""
    raise Exception("This is a forced error to test the 500 error handler.")

# Pre-load graph on application startup
preload_merged_network_graphs_in_cache()

# Launch application
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=3002)