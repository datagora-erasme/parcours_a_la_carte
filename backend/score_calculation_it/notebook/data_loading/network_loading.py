import geopandas as gpd # type: ignore
from pathlib import Path


def load_network_from_gpkg(file_path: str) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """
    Load a GPKG gifile in a geopandas data frame
    """
    gpkg_path = Path(file_path)
    edges = gpd.read_file(gpkg_path, layer="edges")
    nodes = gpd.read_file(gpkg_path, layer="nodes")

    return edges, nodes

