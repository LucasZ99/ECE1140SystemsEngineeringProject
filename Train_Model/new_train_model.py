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
from trainControllerTot_Container import TrainController_Tot_Container


class TrainModel:
    max_force = 48065.673
    min_force = -127380.52

    def __init__(self, controller_container: TrainController_Tot_Container, numid: int = 0, cars: int = 1, ):
        self.ID = numid
        self.position = 0.0
        self.velocity = 0.0  # in m/s
        self.acceleration = 0.0  # in m/s
        self.underground = False
        self.track_circuit = False

        self.crew = People(2)
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
        self.controller = controller_container.new_train_controller()

    # noinspection PyPep8Naming

    def set_velocity(self, vel):
        if vel <= 0:
            self.velocity = 0
        else:
            self.velocity = vel

    def get_total_mass(self):
        return self.train_const.train_mass() + self.crew.mass_of_people() + self.passengers.mass_of_people()

    def update_blocks(self, input_list):
        self.track_circuit = not self.track_circuit
        self.position = 0
        self.old_block = self.new_block
        self.new_block.update_all_values(input_list)

    def physics_calculation(self, time):
        self.heater.physics_calculation(time)
        if self.position > self.train_const.train_length() / 2:
            net_force = (self.engine.force_from_engine(self.velocity, self.failure.engine_failure)
                         - self.brakes.brake_force(self.failure.brake_failure)
                         + self.new_block.grav_force(self.train_const.train_mass()))
            print("> condition, grav force is ", self.new_block.grav_force(self.train_const.train_mass()))
        else:
            net_force = (self.engine.force_from_engine(self.velocity, self.failure.engine_failure)
                         - self.brakes.brake_force(self.failure.brake_failure)
                         + self.old_block.grav_force(self.train_const.train_mass()))
            print("<= condition, grav force is ", self.old_block.grav_force(self.train_const.train_mass()))

        if net_force >= self.max_force:
            net_force = self.max_force
        elif net_force < self.min_force:
            net_force = self.min_force

        # acceleration calculation
        new_acc = net_force / self.train_const.train_mass()

        # velocity calculation
        new_vel = self.velocity + time / 2 * (self.acceleration + new_acc)
        if new_vel < 0:
            new_vel = 0

        # position calculation
        delta_x = time / 2 * (self.velocity + new_vel)
        self.position += delta_x
        self.set_velocity(new_vel)
        self.acceleration = new_acc

        return delta_x

    def update_controller(self):
        auth_speed_list = [self.signals.authority, self.signals.commanded_speed]
        block_list = [self.track_circuit, self.new_block.underground, self.signals.beacon]
        phys_list = [self.velocity, self.brakes.passenger_ebrake]

        output_list: list
        output_list = self.controller.update_train_controller_from_train_model(auth_speed_list, block_list, phys_list)

        # output_list = [Commanded Speed: float, power: float, service_brake: bool, e_brake: bool, door_side: int,
        # announcement: string, interior_lights: bool, exterior_lights: bool, cabin_temperature: float]

        self.engine.set_power(output_list[1])
        self.brakes.service_brake = output_list[2]
        self.brakes.driver_ebrake = output_list[3]
        self.brakes.passenger_ebrake = output_list[3]
        self.interior_functions.left_doors = (int(output_list[4] % 2) == 1)
        self.interior_functions.right_doors = (int(output_list[4] / 2) == 1)
        self.interior_functions.announcement = output_list[5]
        self.interior_functions.interior_lights = output_list[6]
        self.interior_functions.exterior_lights = output_list[7]
        if output_list[8] != self.heater.target_temp:
            self.heater.update_target(output_list[8])
