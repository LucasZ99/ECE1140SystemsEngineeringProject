class TrainModelContainer:
    track_inputs = [0, 0, 0, 0.0, 0.0, 0.0, False]
    controller_inputs = [0.0, False, False, 0, "", True, False, 68]

    def track_model_inputs(self, input_list):
        # the list provided should have entries in this order: [commanded speed, vital authority, beacon, grade,
        # elevation, block length, underground]
        # if providing on coming passengers then provide the list: [commanded speed, vital authority, beacon, grade,
        # elevation, block length, underground, on coming passengers]
        self.track_inputs = input_list

    def train_controller_inputs(self, input_list):
        # the list provided  should have the entries in this order: [power, service brake, emergency brake,
        # left/right doors, announce station, cabin lights, headlights, cabin temp]
        self.controller_inputs = input_list

    def get_update_values(self):
        temp_list = self.track_inputs
        temp_list.extend(self.controller_inputs)
        return temp_list
