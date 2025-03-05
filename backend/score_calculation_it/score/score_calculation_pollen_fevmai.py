#%%
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

#%%
### GLOBAL VARIABLES ###

score_columns_pollen = ["score_pollen_fevmai_arbres_weight", "score_pollen_fevmai_parcs_prop"]

### FUNCTIONS ###

def create_uniqID(x):
    """OSMNX invert some u and v when creating graph => create uniqId in order to make the analyse"""
    return str(x["u"])+str(x["v"])+str(x["key"])

def all_prop(input_path, params, output_path):
    """create one file with all props"""
    edges = gpd.read_file(input_path, layer="edges")
    edges["uniqId"] = edges.apply(create_uniqID, axis=1)
    edges = edges.set_index(["u", "v", "key"])
    for dataname, dataprops in params.items():
        data = gpd.read_file(dataprops["edges_path"])
        data = data.set_index(["u", "v", "key"])
        edges[dataname] = data[dataname]
    edges.to_file(output_path, layer="edges", driver="GPKG")
    
def total_score(input_path, output_path, score_columns):
    """
    Calculate the total pollen score based on the specified columns and save the result to a new file.
    
    Parameters:
    - input_path: Path to the input data file.
    - output_path: Path where the output file will be saved.
    - score_columns: List of columns to sum for calculating the total score.
    """
    edges = gpd.read_file(input_path, layer="edges")
    print(edges.columns)
    edges["total_score_pollen_fevmai"] = edges[score_columns].sum(axis=1)
    edges["total_score_pollen_fevmai"] = edges["total_score_pollen_fevmai"] + 1
    print("total score :", edges["total_score_pollen_fevmai"].describe())
    edges.to_file(output_path, driver="GPKG")

def all_score_edges(input_path, output_path, params):
    """
    params : {
        columns1 : {
            edges_path: "path",
            fn_cont: function(),
            alpha: 1
            },
        },
        ...
    }
    """
    default_edges = gpd.read_file(input_path, layer="edges")
    print(default_edges.columns)
    
    for data_name, data_param in params.items():
        print(f"Score {data_name}")
        data = gpd.read_file(data_param["edges_path"])
        default_edges[f"score_pollen_fevmai_{data_name}"] = data[data_name].apply(data_param["fn_cont"])

    default_edges.to_file(output_path, driver="GPKG", layer="edges")


def score_distance(input_path, output_path):
    """calculate the score by distance for each edges"""
    edges = gpd.read_file(input_path)

    edges["score_distance_pollen_fevmai"] = edges["total_score_pollen_fevmai"] * edges["length"]
    edges["score_distance_pollen_fevmai"] = edges["score_distance_pollen_fevmai"].replace(0, 1)
    print("score distance : ",edges["score_distance_pollen_fevmai"].describe())

    edges.to_file(output_path, driver="GPKG")

def score_pollen(input_path, output_path):
    """Score from 0 to 10 """
    edges = gpd.read_file(input_path)

    min_score = edges["score_distance_pollen_fevmai"].min()
    max_score = edges["score_distance_pollen_fevmai"].max()
    slope = (0-10)/(max_score-min_score)
    origin_ordinate = -slope*max_score
    edges["pollen_fevmai_score"] = edges["score_distance_pollen_fevmai"].apply(lambda x: round(slope*x+origin_ordinate, 2))

    edges.to_file(output_path, driver="GPKG")

params = {
    "arbres_weight" : {
        "edges_path": edges_buffer_arbres_pollen_prop_path_fevmai,
        "fn_cont": lambda x: x,
        "alpha": 1
    },
    "parcs_prop" : {
        "edges_path": edges_buffer_parcs_pollen_prop_path,
        "fn_cont": lambda x: 1*x,
        "alpha": 1
    },
}



all_score_edges(edges_buffer_path, edges_buffer_scored_path, params)

total_score(edges_buffer_scored_path, edges_buffer_total_score_path, score_columns_pollen)

score_distance(edges_buffer_total_score_path, edges_buffer_total_score_distance_path)
score_pollen(edges_buffer_total_score_distance_path, edges_buffer_total_score_distance_pollen_fevmai_path)
