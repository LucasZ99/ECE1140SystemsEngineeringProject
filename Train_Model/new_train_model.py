import random
import math
import people
import passenger_people
import train_construction
import engine
import heater
import signals
import failures
import interior_functions
import brakes
import block


class TrainModel:
    def __init__(self, numid=0, cars=1):
        self.ID = numid
        self.position = 0.0
        self.velocity = 0.0  # in m/s
        self.acceleration = 0.0  # in m/s

        self.crew = people.People()
        self.passengers = passenger_people.PassengerPeople()
        self.train_const = train_construction.TrainConstruction(cars)
        self.engine = engine.Engine()
        self.heater = heater.Heater()
        self.signals = signals.Signals()
        self.failure = failures.Failures()
        self.interior_functions = interior_functions.InteriorFunctions()
        self.brakes = brakes.Brakes()
        self.old_block = block.Block()
        self.new_block = block.Block()

    # noinspection PyPep8Naming

    def set_velocity(self, vel):
        if vel <= 0:
            self.velocity = 0
        else:
            self.velocity = vel

    def get_total_mass(self):
        return self.train_const.train_mass() + self.crew.mass_of_people() + self.passengers.mass_of_people()

    def update_blocks(self, input_list):
        self.old_block = self.new_block
        self.new_block.update_all_values(input_list)

    def physics_calculation(self, time):
        if self.position > self.train_const.train_length()/2:
            net_force = self.engine.force_from_engine(self.velocity, self.failure.engine_failure) + self.brakes.brake_force(self.failure.brake_failure) + self.new_block.grav_force()
        else:
            net_force = self.engine.force_from_engine(self.velocity,self.failure.engine_failure) + self.brakes.brake_force(self.failure.brake_failure) + self.new_block.grav_force()

        # acceleration calculation
        new_acc = net_force / self.train_const.train_mass()

        # velocity calculation
        new_vel = self.velocity + time/2 * (self.acceleration + new_acc)
        if new_vel < 0:
            new_vel = 0

        # position calculation
        self.position = self.position + time/2 * (self.velocity + new_vel)
        self.set_velocity(new_vel)
        self.acceleration = new_acc

        self.heater.physics_calculation(time)
