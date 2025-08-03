# initialization:
# Load processed data
graph_3d = load_processed_graph('nyc_graph_3d.pkl')
buildings = load_buildings('nyc_buildings.geojson')

# Create components
planner = RoadAStar(graph_3d)
obstacle_checker = ObstacleChecker(buildings)
visualizer = MapVisualizer(graph_3d, buildings)

# Set start and goal coordinates
start = (-74.00597, 40.71427)  # World Trade Center
goal = (-73.97803, 40.75889)   # Times Square

# path planning:
path_nodes = planner.plan_path(start, goal, altitude=50)
path_3d = [(
    graph_3d.nodes[n]['x'], 
    graph_3d.nodes[n]['y'], 
    graph_3d.nodes[n]['z'] + 50  # Flight altitude
) for n in path_nodes]

# simulation loop:
controller = UAVController(path_3d, obstacle_checker)

for _ in range(1000):  # Simulate 1000 steps
    position = controller.update(0.1)  # 0.1s timestep
    visualizer.update_uav(position)
    
    if controller.current_idx >= len(path_3d) - 1:
        print("Destination reached!")
        break

visualizer.visualize()

