import os
import sys
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../script_python")
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import osmnx as ox
from function_utils import *
from global_variable import *

def total_score(input_path, output_path, score_columns):
    """Calculation of the total noise score based on the specified columns"""
    edges_data = gpd.read_file(input_path)
    
    print(f"Columns in {input_path} : {edges_data.columns}")
    edges_data["total_score_bruit"] = edges_data[score_columns].sum(axis=1) 
    print(f"Calculation of total_score_bruit completed.")

    # Save the score file
    edges_data.to_file(output_path, driver="GPKG")
    print(f"The score file has been saved at {output_path}.")


def score_distance(input_path, output_path):
    """Calculate the score by distance for each edge, favoring shorter segments"""
    edges_data = gpd.read_file(input_path)  

    edges_data["score_distance_bruit"] = edges_data["DN"] * edges_data["length"]
    
    print(f"Calculation of score_distance_bruit completed.")

    # Save the file with distance-weighted scores
    edges_data.to_file(output_path, driver="GPKG")
    print(f"The score_distance_bruit file has been saved at {output_path}.")


def score_bruit(input_path, output_path):
    """Calculate a noise score from 0 to 10, based on the score_distance_bruit"""
    edges_data = gpd.read_file(input_path)
    
    # Get the minimum and maximum values of score_distance_bruit for normalization
    min_score = edges_data["score_distance_bruit"].min()  
    max_score = edges_data["score_distance_bruit"].max()  
    slope = (0 - 10) / (max_score - min_score)  # Calculate the slope for scaling
    origin_ordinate = -slope * max_score  # Y-intercept for normalization
    
    # Apply normalization to score_distance_bruit to get a bruit_score between 0 and 10
    edges_data["bruit_score"] = edges_data["score_distance_bruit"].apply(lambda x: round(slope * x + origin_ordinate, 2))
    
    print(f"Calculation of bruit_score completed.")

    # Save the noise score file
    edges_data.to_file(output_path, driver="GPKG")
    print(f"The bruit_score file has been saved at {output_path}.")

# Execution of functions
total_score(edges_buffer_bruit_wavg_path, edges_buffer_total_score_path, ["DN"])
score_distance(edges_buffer_total_score_path, edges_buffer_total_score_distance_path)
score_bruit(edges_buffer_total_score_distance_path, edges_buffer_total_score_distance_bruit_path)
