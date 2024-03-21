class Failures:
    def __init__(self):
        self.engine_failure = False
        self.signal_pickup_failure = False
        self.brake_failure = False

    def toggle_engine(self):
        self.engine_failure = not self.engine_failure

    def toggle_signal_pickup(self):
        self.signal_pickup_failure = not self.signal_pickup_failure

    def toggle_brakes(self):
        self.brake_failure = not self.brake_failure

    def get_safety(self):
        return self.engine_failure or self.signal_pickup_failure or self.brake_failure
