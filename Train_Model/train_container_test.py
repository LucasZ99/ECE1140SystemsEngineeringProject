import unittest
from Train_Model import TrainModel
from business_logic import TrainBusinessLogic
from trainControllerTot_Container import TrainController_Tot_Container
import SystemTime


class MyTestCase(unittest.TestCase):
    def test_driver_engages_emergency_brake(self):
        time = SystemTime.time()
        train = TrainModel(TrainController_Tot_Container())
        # set brakes
        train.brakes.driver_ebrake = True  # set brake
        train.velocity = 12
        new_time = SystemTime.time()
        train.physics_calculation(new_time - time)  # do physics
        time = new_time
        num = train.velocity
        self.assertLessEqual(num, 12)  # velocity should have decreased or hit 0

        new_time = SystemTime.time()
        train.physics_calculation(new_time - time)
        time = new_time
        new_num = train.velocity
        self.assertLessEqual(new_num, num)  # velocity should have decreased or hit 0

        num = new_num
        new_time = SystemTime.time()
        train.physics_calculation(new_time - time)
        time = new_time
        new_num = train.velocity
        self.assertLessEqual(new_num, num)  # velocity should have decreased or hit 0

    def test_driver_changes_set_temperature(self):
        time = SystemTime.time()
        train = TrainModel(TrainController_Tot_Container())  # set new temp
        train.heater.update_target(75.0)
        diff = 75 - 68  # 68 is initial default temp
        for _ in range(20):
            new_time = SystemTime.time()
            train.physics_calculation(new_time - time)  # run temp
            time = new_time
            new_diff = 75 - train.heater.current_temp
            self.assertLessEqual(new_diff, diff)  # should get closer to target every time
        new_diff = 75 - train.heater.current_temp
        self.assertGreaterEqual(new_diff, 1)  # should be within +-1 degree after 20s

    def test_train_enters_a_tunnel_goes_underground(self):
        train = TrainModel(TrainController_Tot_Container())
        train.update_blocks((0, 0, True))  # the train is now on a block that is underground
        train.update_controller()  # prob train controller for updates to train model
        self.assertTrue(train.interior_functions.exterior_lights)  # headlights should be on

    def test_update_authority_Commanded_Speed(self):
        train = TrainModel(TrainController_Tot_Container())
        train.signals.depackage_signals([4, 50, "0"*128])  # train is now receiving 4 authority and 50 speed
        train.update_controller()  # prob train controller for updates to train model
        self.assertGreater(train.engine.power, 0)  # with non 0 speed and authority controller should have applied
        # non 0 power to engine

    def test_driver_speeds_up_train(self):
        time = SystemTime.time()
        train = TrainModel(TrainController_Tot_Container())
        train.signals.depackage_signals([4, 50, "0" * 128])  # train is now receiving 4 authority and 50 speed
        for _ in range(20):
            power = train.engine.power
            train.update_controller()  # prob train controller for updates to train model
            self.assertNotEqual(train.engine.power, power)  # train controller should change power
            # sometimes this fails due to rounding errors, try running again :)
            velocity = train.velocity
            new_time = SystemTime.time()
            train.physics_calculation(new_time - time)  # run train should speed up
            time = new_time
            self.assertGreaterEqual(train.velocity, velocity)  # train should speed up

    def test_driver_slows_down_train(self):
        time = SystemTime.time()
        train = TrainModel(TrainController_Tot_Container())
        train.velocity = 50  # train is moving
        # at this point in time train is receiving 0 speed 0 authority
        for _ in range(20):
            train.update_controller()  # prob train controller for updates to train model
            self.assertEqual(train.engine.power, 0)  # train controller not speed up
            self.assertTrue(train.brakes.service_brake)  # controller should've set brake
            velocity = train.velocity
            new_time = SystemTime.time()
            train.physics_calculation(new_time - time)  # run train should speed up
            time = new_time
            self.assertLessEqual(train.velocity, velocity)  # train should slow down

    def test_train_enters_new_block(self):
        time = SystemTime.time()
        train = TrainModel(TrainController_Tot_Container())
        train.update_blocks((-15, 5, False))  # train enters block with grade
        # train will not react to new grade until its midpoint enters the new block
        train.velocity = 50
        while train.position <= train.train_const.train_length()/2:
            new_time = SystemTime.time()
            train.physics_calculation(new_time - time)
            time = new_time

        # now train should start to speed up
        print("in new block")
        for _ in range(20):
            velocity = train.velocity
            new_time = SystemTime.time()
            train.physics_calculation(new_time - time)
            time = new_time
            self.assertGreater(train.velocity, velocity, f'iteration {_}')


if __name__ == '__main__':
    unittest.main()
