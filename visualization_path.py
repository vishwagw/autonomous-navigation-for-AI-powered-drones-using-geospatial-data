# visualizing the path of the UAV:
import pyvista as pv

class MapVisualizer:
    def __init__(self, graph_3d, buildings):
        self.plotter = pv.Plotter()
        self.buildings = self._create_building_meshes(buildings)
        self.roads = self._create_road_meshes(graph_3d)
        self.uav = pv.Sphere(radius=2)
        
    def _create_building_meshes(self, buildings):
        meshes = []
        for _, b in buildings.iterrows():
            height = b.get('height', 30)
            mesh = pv.Polygon(b.geometry.exterior.coords[:-1]).extrude([0, 0, height])
            meshes.append(mesh)
        return pv.MultiBlock(meshes)
    
    def _create_road_meshes(self, graph):
        lines = []
        for u, v, data in graph.edges(data=True):
            u_pos = (graph.nodes[u]['x'], graph.nodes[u]['y'], graph.nodes[u]['z'])
            v_pos = (graph.nodes[v]['x'], graph.nodes[v]['y'], graph.nodes[v]['z'])
            lines.append(pv.Line(u_pos, v_pos))
        return pv.MultiBlock(lines)
    
    def update_uav(self, position):
        self.uav.translate(position, inplace=True)
        
    def visualize(self):
        self.plotter.add_mesh(self.buildings, color='tan')
        self.plotter.add_mesh(self.roads, color='black', line_width=2)
        self.plotter.add_mesh(self.uav, color='red')
        self.plotter.show()