import new_train_model

train = new_train_model.TrainModel()

train.heater.update_target(75)

for i in range(100):
    train.physics_calculation(1)
    print(f'target = {train.heater.target_temp}, initial = {train.heater.initial_temp}, current = {train.heater.current_temp}, constant = {train.heater.time_constant}')

train.heater.update_target(68)

for i in range(100):
    train.physics_calculation(1)
    print(f'target = {train.heater.target_temp}, initial = {train.heater.initial_temp}, current = {train.heater.current_temp}, constant = {train.heater.time_constant}')