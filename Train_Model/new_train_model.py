from Train_Model.passenger_people import PassengerPeople
from Train_Model.people import People
from Train_Model.train_construction import TrainConstruction
from Train_Model.engine import Engine
from Train_Model.heater import Heater
from Train_Model.signals import Signals
from Train_Model.failures import Failures
from Train_Model.interior_functions import InteriorFunctions
from Train_Model.brakes import Brakes
from Train_Model.block import Block


class TrainModel:
    max_force = 48065.673
    min_force = -127380.52

    def __init__(self, numid=0, cars=1):
        self.ID = numid
        self.position = 0.0
        self.velocity = 0.0  # in m/s
        self.acceleration = 0.0  # in m/s
        self.underground = False
        self.track_circuit = False

        self.crew = People()
        self.passengers = PassengerPeople()
        self.train_const = TrainConstruction(cars)
        self.engine = Engine()
        self.heater = Heater()
        self.signals = Signals()
        self.failure = Failures()
        self.interior_functions = InteriorFunctions()
        self.brakes = Brakes()
        self.old_block = Block()
        self.new_block = Block()

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
            net_force = self.engine.force_from_engine(self.velocity, self.failure.engine_failure) - self.brakes.brake_force(self.failure.brake_failure) + self.new_block.grav_force()
        else:
            net_force = self.engine.force_from_engine(self.velocity, self.failure.engine_failure) - self.brakes.brake_force(self.failure.brake_failure) + self.old_block.grav_force()

        if net_force >= self.max_force:
            net_force = self.max_force
        elif net_force < self.min_force:
            net_force = self.min_force

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
