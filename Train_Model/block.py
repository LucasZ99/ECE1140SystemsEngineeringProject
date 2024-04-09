import math

class Block:
    # constant
    acc_due_to_gravity = 9.81  # in m/s^2

    def __init__(self, grd=0.0, elev=0.0, undr=False):
        self.grade = grd
        self.elevation = elev
        self.underground = undr

    def grav_force(self, mass=float()):
        prop_grade = self.grade / 100
        force_from_gravity = (-1 * mass * self.acc_due_to_gravity *
                              prop_grade / math.sqrt(1 + prop_grade * prop_grade))
        return force_from_gravity

    def update_all_values(self, input_list):
        self.grade = input_list[0]
        self.elevation = input_list[1]
        self.underground = input_list[2]
