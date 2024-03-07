class InteriorFunctions:
    def __init__(self):
        self.interior_lights = True
        self.exterior_lights = False
        self.left_doors = False
        self.right_doors = False
        self.announcement = ""

    def toggle_interior_lights(self):
        self.interior_lights = not self.interior_lights

    def toggle_exterior_lights(self):
        self.exterior_lights = not self.exterior_lights

    def toggle_left_doors(self):
        self.left_doors = not self.left_doors

    def toggle_right_doors(self):
        self.right_doors = not self.right_doors

    def clear_announcement(self):
        self.announcement = ""
