# flight simulator is a simple flight simulator that simulates the flight of an aircraft
class UAVController:
    def __init__(self, path_3d, obstacle_checker):
        self.path = path_3d
        self.current_idx = 0
        self.obstacle_checker = obstacle_checker
        self.position = self.path[0]
        self.velocity = 10  # m/s
        self.max_climb_rate = 5  # m/s
    
    def update(self, dt):
        if self.current_idx >= len(self.path) - 1:
            return self.position  # Reached destination
        
        target = self.path[self.current_idx + 1]
        direction = np.array(target) - np.array(self.position)
        distance = np.linalg.norm(direction)
        
        # Adjust altitude gradually
        max_alt_change = self.max_climb_rate * dt
        if abs(direction[2]) > max_alt_change:
            direction[2] = np.sign(direction[2]) * max_alt_change
        
        # Move toward target
        step = direction * min(1, self.velocity * dt / distance)
        new_position = tuple(np.array(self.position) + step)
        
        # Obstacle avoidance
        if not self.obstacle_checker.is_safe(new_position):
            # Emergency climb procedure
            new_position = (new_position[0], new_position[1], 
                           new_position[2] + self.max_climb_rate * dt)
        
        self.position = new_position
        
        # Advance to next waypoint if close
        if distance < 5:  # 5m threshold
            self.current_idx += 1
            
        return self.position