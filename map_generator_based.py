import osmnx as ox
import rasterio
import pyvista as pv
from shapely.geometry import Polygon

# Fetch OSM data
gdf = ox.geometries.geometries_from_place("Manhattan, NYC", tags={"building": True})
gdf = gdf[gdf.geom_type == 'Polygon']  # Filter polygons

# Estimate heights (simplified)
gdf['height'] = gdf['height'].fillna(gdf['building:levels'] * 3).fillna(10)  # Default 10m

# Load DEM
with rasterio.open("dem.tif") as dem:
    elevation = dem.read(1)
    transform = dem.transform

# Generate terrain mesh
grid = pv.UniformGrid(dimensions=dem.shape, spacing=(abs(transform.a), abs(transform.e), 1))
grid.points[:, 2] = elevation.ravel(order='F')  # Flatten elevation

# Create 3D buildings
meshes = []
for geom, height in zip(gdf.geometry, gdf.height):
    # Convert to 3D
    z = ...  # Sample DEM at centroid for ground elevation
    poly = pv.Polygon(geom.exterior.coords[:-1])  # Remove duplicate endpoint
    building = poly.extrude((0, 0, height), capping=True)
    meshes.append(building)

# Combine and export
terrain = grid.warp_by_scalar()  # Optional: smooth terrain
scene = terrain + meshes
scene.save("nyc_3d.glb")