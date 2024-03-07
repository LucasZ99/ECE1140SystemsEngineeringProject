class Brakes:
    # constants
    service_force = 55991.44  # in newtons
    emergency_force = 127380.52  # in newtons

    def __init__(self):
        self.service_brake = False
        self.driver_ebrake = False
        self.passenger_ebrake = False

    def toggle_service_brake(self):
        self.service_brake = not self.service_brake

    def toggle_driver_ebrake(self):
        self.driver_ebrake = not self.driver_ebrake

    def toggle_passenger_ebrake(self):
        self.passenger_ebrake = not self.passenger_ebrake

    def emergency_brake_status(self):
        return self.passenger_ebrake or self.driver_ebrake

    def brake_force(self, fail):
        if self.driver_ebrake or self.passenger_ebrake:
            return self.emergency_force
        elif self.service_brake and (not fail):
            return self.service_brake
        else:
            return 0
