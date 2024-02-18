import random
import math


class TrainModel:
    # constants
    max_power = 120000  # in watts
    min_power = 0  # in watts
    service_force = 55991.44  # in newtons
    emergency_force = 127380.52  # in newtons
    max_passengers_per_car = 222
    train_mass_per_car = 37103.86  # in kg
    mass_per_person = 81.65  # in kg
    length_per_car = 32.2  # per car in meters
    height = 3.42  # in meters
    width = 2.65  # in meters
    acc_due_to_gravity = 9.81  # in m/s^2

    def __init__(self, numid=0, cars=1):
        # physics values
        self.power = 0.0  # in watts
        self.velocity = 0.0  # in m/s
        self.acceleration = 0.0  # in m/s
        self.grade = 0.0  # in %
        self.elevation = 0.0  # in meters
        self.service_status = False
        self.passenger_emergency_status = False
        self.driver_emergency_status = False

        # train descriptors
        self.ID = numid
        self.car_number = cars
        self.passenger_count = 0
        self.crew_count = 2
        self.train_length = self.car_number * self.length_per_car  # in meters
        self.max_passengers = self.car_number * self.max_passengers_per_car
        self.total_mass = self.car_number * self.train_mass_per_car + self.crew_count * self.mass_per_person  # in kg

        # train services
        self.exterior_light = False
        self.interior_light = True
        self.left_door = False
        self.right_door = False
        self.announcement = ""
        self.interior_temp = 68  # room temp in fahrenheit

        # signals received
        self.commanded_velocity = 0.0
        self.authority = 0.0
        self.beacon = ""

        # failures
        self.engine_failure = False
        self.pickup_failure = False
        self.brake_failure = False

    def get_train_mass_per_car(self):
        return self.train_mass_per_car

    def set_power(self, pwr):
        if pwr >= self.max_power:
            self.power = self.max_power
        elif pwr <= self.min_power:
            self.power = self.min_power
        else:
            self.power = pwr

    def get_power(self):
        return self.power

    # noinspection PyPep8Naming
    def set_ID(self, numid):
        self.ID = numid

    # noinspection PyPep8Naming
    def get_ID(self):
        return self.ID

    def set_velocity(self, vel):
        self.velocity = vel

    def get_velocity(self):
        return self.velocity

    def set_acceleration(self, acc):
        self.acceleration = acc

    def get_acceleration(self):
        return self.acceleration

    def set_grade(self, grd):
        self.grade = grd

    def get_grade(self):
        return self.grade

    def set_elevation(self, elev):
        self.elevation = elev

    def get_elevation(self):
        return self.elevation

    def enable_service_brake(self):
        self.service_status = True

    def disable_service_brake(self):
        self.service_status = False

    def get_service_brake(self):
        return self.service_status

    def enable_passenger_emergency_brake(self):
        self.passenger_emergency_status = True

    def disable_passenger_emergency_brake(self):
        self.passenger_emergency_status = False

    def get_passenger_emergency_brake(self):
        return self.passenger_emergency_status

    def enable_driver_emergency_brake(self):
        self.driver_emergency_status = True

    def disable_driver_emergency_brake(self):
        self.driver_emergency_status = False

    def get_driver_emergency_brake(self):
        return self.driver_emergency_status

    def set_car_count(self, cars):
        if cars < 1:
            return False
        else:
            self.car_number = cars
            self.train_length = self.car_number * self.length_per_car
            self.max_passengers = self.car_number * self.max_passengers_per_car
            self.total_mass = (self.car_number * self.train_mass_per_car +
                               (self.crew_count + self.passenger_count) * self.mass_per_person)
            return True

    def get_car_count(self):
        return self.crew_count

    def set_passenger_count(self, pas):
        if pas <= 0:
            self.passenger_count = 0
        elif pas >= self.max_passengers:
            self.passenger_count = self.max_passengers
        else:
            self.passenger_count = pas

        self.total_mass = (self.car_number * self.train_mass_per_car +
                           (self.crew_count + self.passenger_count) * self.mass_per_person)

    def get_passenger_count(self):
        return self.passenger_count

    def set_crew_count(self, crew):
        if crew < 1:
            return False
        else:
            self.crew_count = crew
            self.total_mass = (self.car_number * self.train_mass_per_car +
                               (self.crew_count + self.passenger_count) * self.mass_per_person)
            return True

    def get_crew_count(self):
        return self.crew_count

    def set_total_mass(self, tot):
        if tot <= 0:
            return False
        else:
            self.total_mass = tot

    def get_total_mass(self):
        return self.total_mass

    def exterior_lights_on(self):
        self.exterior_light = True

    def exterior_lights_off(self):
        self.exterior_light = False

    def get_exterior_light(self):
        return self.exterior_light

    def interior_lights_on(self):
        self.interior_light = True

    def interior_lights_off(self):
        self.interior_light = False

    def get_interior_light(self):
        return self.interior_light

    def left_door_open(self):
        self.left_door = True

    def left_door_close(self):
        self.left_door = False

    def get_left_door(self):
        return self.left_door

    def right_door_open(self):
        self.right_door = True

    def right_door_close(self):
        self.right_door = False

    def get_right_door(self):
        return self.right_door

    def set_announcement(self, announce):
        self.announcement = announce

    def get_announcement(self):
        return self.announcement

    def set_interior_temp(self, temp):
        self.interior_temp = temp

    def get_interior_temp(self):
        return self.interior_temp

    def set_commanded_velocity(self, c_speed):
        self.commanded_velocity = c_speed

    def get_commanded_velocity(self):
        return self.commanded_velocity

    def set_authority(self, auth):
        self.authority = auth

    def get_authority(self):
        return self.authority

    def fail_engine(self):
        self.engine_failure = True

    def fix_engine(self):
        self.engine_failure = False

    def get_engine_failure(self):
        return self.engine_failure

    def fail_signal_pickup(self):
        self.pickup_failure = True

    def fix_signal_pickup(self):
        self.pickup_failure = False

    def get_signal_pickup_failure(self):
        return self.pickup_failure

    def fail_brake(self):
        self.brake_failure = True

    def fix_brake(self):
        self.brake_failure = False

    def get_brake_failure(self):
        return self.brake_failure

    def station_passenger_update(self, ingoing):
        outgoing = random.randint(0, self.passenger_count)
        self.set_passenger_count(self.passenger_count - outgoing + ingoing)

    def physics_calculation(self, time):
        # power is already delimited by the nature of set_power
        # if velocity = 0 when starting to move, kick-start
        if self.velocity == 0 & (self.power != 0):
            self.velocity = .1

        # force calculation
        force_from_power = self.power / self.velocity
        prop_grade = self.grade / 100
        force_from_gravity = (-1 * self.total_mass * self.acc_due_to_gravity *
                              prop_grade / math.sqrt(1 + prop_grade * prop_grade))
        # multiply by negative because the grade points in the wrong direction
        net_force = force_from_gravity + force_from_power

        if self.passenger_emergency_status | self.driver_emergency_status:
            net_force -= self.emergency_force
        elif (not self.brake_failure) & self.service_status:
            net_force -= self.service_force

        # acceleration calculation
        new_acc = net_force / self.total_mass

        # velocity calculation
        self.velocity = self.velocity + time/2 * (self.acceleration + new_acc)
        self.acceleration = new_acc
