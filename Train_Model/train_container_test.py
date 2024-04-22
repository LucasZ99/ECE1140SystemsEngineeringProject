import unittest
from Train_Model import TrainModelContainer, TrainModel
from trainControllerTot_Container import TrainController_Tot_Container


class MyTestCase(unittest.TestCase):
    def test_driver_brake(self):
        container = TrainModelContainer(TrainController_Tot_Container())
        container.add_train()
        # set brakes
        container.train_controller_inputs([0, 0, False, True, 0, "", True, False], 1)
        container.business_logic.train_dict[1].velocity = 12
        container.physics_calculation()
        num = container.business_logic.train_dict[1].velocity
        self.assertLessEqual(num, 12)
        container.physics_calculation()
        new_num = container.business_logic.train_dict[1].velocity
        self.assertLessEqual(new_num, num)
        num = new_num
        container.physics_calculation()
        new_num = container.business_logic.train_dict[1].velocity
        self.assertLessEqual(new_num, num)

    def test_change_test(self):
        container = TrainModelContainer(TrainController_Tot_Container())
        container.add_train()
        # set new temp
        container.controller_update_temp(75, 1)
        diff = 75 - 68  # 68 is initial default temp
        for i in range(20):
            container.physics_calculation()
            new_diff = 75 - container.business_logic.train_dict[1].heater.current_temp
            self.assertLess(new_diff, diff)  # should get closer to target every time
        new_diff = 75 - container.business_logic.train_dict[1].heater.current_temp
        self.assertGreaterEqual(new_diff, 1)  # should be within +-1 degree after 20s


if __name__ == '__main__':
    unittest.main()
