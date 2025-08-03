# path planning module for the UAV:
# 3D A algorithm:

import networkx as nx
from scipy.spatial import KDTree

class RoadAStar:
    def __init__(self, graph_3d):
        self.graph = graph_3d
        self.kdtree = KDTree([(data['x'], data['y'], data['z']) 
                             for _, data in graph_3d.nodes(data=True)])
    
    def heuristic(self, a, b):
        return np.linalg.norm(np.array(a) - np.array(b))
    
    def plan_path(self, start, goal, altitude=50):
        # Convert to 3D points
        start_3d = (*start, altitude)
        goal_3d = (*goal, altitude)
        
        # Find nearest road nodes
        _, start_idx = self.kdtree.query(start_3d)
        _, goal_idx = self.kdtree.query(goal_3d)
        
        # Convert to NetworkX nodes
        nodes = list(self.graph.nodes)
        start_node = nodes[start_idx]
        goal_node = nodes[goal_idx]
        
        # 3D A* pathfinding
        return nx.astar_path(
            self.graph, 
            start_node, 
            goal_node, 
            heuristic=lambda u, v: self.heuristic(
                (self.graph.nodes[u]['x'], self.graph.nodes[u]['y'], self.graph.nodes[u]['z']),
                (self.graph.nodes[v]['x'], self.graph.nodes[v]['y'], self.graph.nodes[v]['z'])
            ),
            weight='length'
        )