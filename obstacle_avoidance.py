# obstacle avoidance algorithm approach:

class ObstacleChecker:
    def __init__(self, buildings, safety_margin=15):
        self.building_boxes = []
        for _, b in buildings.iterrows():
            minx, miny, maxx, maxy = b.geometry.bounds
            minz = 0
            maxz = b.get('height', 30)  # Default 30m height
            self.building_boxes.append((
                (minx - safety_margin, miny - safety_margin, minz),
                (maxx + safety_margin, maxy + safety_margin, maxz + safety_margin)
            ))
    
    def is_safe(self, position):
        x, y, z = position
        for (minx, miny, minz), (maxx, maxy, maxz) in self.building_boxes:
            if minx <= x <= maxx and miny <= y <= maxy and minz <= z <= maxz:
                return False
        return True
    
    