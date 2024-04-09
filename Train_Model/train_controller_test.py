import unittest
from Train_Model import TrainModelContainer, TrainModel
from trainControllerTot_Container import TrainController_Tot_Container
from SystemTime import SystemTimeContainer


class MyTestCase(unittest.TestCase):
    def test_driver_brake(self):
        container = TrainModelContainer(TrainController_Tot_Container(SystemTimeContainer(), True), SystemTimeContainer())
        container.add_train()
        container.train_controller_inputs([0, 0, False, True, 0, "", True, False], 1)
        container.business_logic.train_dict[1].velocity == 12
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


if __name__ == '__main__':
    unittest.main()
