import os
os.environ['USE_PYGEOS'] = '0'
import pickle
import gzip
from datetime import datetime
from global_variable import merged_network_pickle_path, merged_network_multidigraph_pickle_path, merged_network_cache

def are_pickle_files_in_cache():
    return ((merged_network_pickle_path in merged_network_cache) and (merged_network_cache[merged_network_pickle_path] is not None)) and ((merged_network_multidigraph_pickle_path in merged_network_cache) or (merged_network_cache[merged_network_multidigraph_pickle_path] is not None))        


def cache_merged_network_graphs_from_pickles():

    print(datetime.now(), f"Load pickle file start")

    with gzip.open(f"{merged_network_pickle_path}.gz", 'rb') as file:
        pickle_file = pickle.load(file)
        merged_network_cache[merged_network_pickle_path] = pickle_file
    
    with gzip.open(f"{merged_network_multidigraph_pickle_path}.gz", 'rb') as file:
        multidi_pickle_file = pickle.load(file)
        merged_network_cache[merged_network_multidigraph_pickle_path] = multidi_pickle_file
        
    print(datetime.now(), f"Load pickle file end")
