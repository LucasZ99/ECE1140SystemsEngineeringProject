import train_model_object


class TrainModelContainer:

    train_list = dict()
    track_inputs = dict()
    controller_inputs = dict()

    def track_model_inputs(self, input_list, index):
        # the list provided should have entries in this order: [commanded speed, vital authority, beacon, grade,
        # elevation, block length, underground]
        # if providing on coming passengers then provide the list: [commanded speed, vital authority, beacon, grade,
        # elevation, block length, underground, on coming passengers]
        return

    def train_controller_inputs(self, input_list, index):
        # the list provided  should have the entries in this order: [commanded speed, power, service brake,
        # emergency brake, left/right doors, announce station, cabin lights, headlights, cabin temp]
        return

    def update_values(self):
        return

    def physics_calculation(self):
        return

    def add_train(self):
        return

    def remove_train(self, index):
        return False
