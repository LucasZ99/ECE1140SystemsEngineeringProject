import SystemTime
from Train_Model import TrainModel
from trainControllerTot_Container import TrainController_Tot_Container

time = SystemTime.time()
train = TrainModel(TrainController_Tot_Container())
new_time = SystemTime.time()
train.physics_calculation(new_time-time)