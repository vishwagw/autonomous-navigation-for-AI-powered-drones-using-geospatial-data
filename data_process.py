# data processing pipline :
import osmnx as ox
import pyproj
import numpy as np
from scipy.interpolate import interp1d

# Fetch OSM data
G = ox.graph_from_place('Manhattan, NYC', network_type='drive', simplify=True)
buildings = ox.geometries_from_place('Manhattan, NYC', tags={'building': True})

# Convert to 3D with elevation
dem = load_dem('nyc_dem.tif')  # Digital Elevation Model

def add_elevation(graph, dem):
    transformer = pyproj.Transformer.from_crs(4326, dem.crs, always_xy=True)
    for node, data in graph.nodes(data=True):
        lon, lat = data['x'], data['y']
        x, y = transformer.transform(lon, lat)
        data['z'] = dem.sample((x, y))[0] + 5  # 5m above ground
    return graph

G_3d = add_elevation(G, dem)

