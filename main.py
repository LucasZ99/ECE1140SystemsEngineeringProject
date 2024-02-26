#
# Pseudocode for array-based communication implementation
#

# Import dependencies
import time
from PyQt6 import QApplication
import sys
# Import our defined module classes
from ctc import CTC
from track_controller import TrackController
from track_model import TrackModel
from train_model import TrainModel
from train_controller import TrainController
# Import Launcher class
from launcher import LauncherWindow


def main():
    # Initialize instances of our classes (This would in actuality be more complicated)
    ctc = CTC()
    track_controller = TrackController()
    track_model = TrackModel()
    train_model = TrainModel()
    train_controller = TrainController()

    # Run Launcher UI
    app = QApplication(sys.argv)
    window = LauncherWindow()
    window.show()

    [starting_time, time_multiplier, track_layout] = LauncherWindow.getInputs()
    time_counter = starting_time

    # Main simulation loop
    while True:
        # Communication Between CTC and Track Controller
        pass
        # Communication Between Track Controller and Track Model
        [switch_activation, signal_positions, rxr_positions,
         authority, commanded_speed] = track_controller.get_track_model_outputs()

        track_model.set_track_controller_inputs(
            switch_activation, signal_positions, rxr_positions,
            authority, commanded_speed
        )
        # Communication Between Track Model and Train Model
        [commanded_speed, authority, beacon_msg, grade,
         elevation, block_length, underground_status] = track_model.get_train_model_outputs()

        train_model.set_track_model_inputs(
            commanded_speed, authority, beacon_msg, grade,
            elevation, block_length, underground_status
        )
        # Communication between Train Model and Train Controller
        pass

        # 1 ms per iteration
        time.sleep(0.001*time_multiplier)
        time_counter += .001
        # Update modules based on time
        ctc.update(time_counter)
        track_controller.update(time_counter)
        track_model.update(time_counter)
        train_model.update(time_counter)
        train_controller.update(time_counter)


if __name__ == "__main__":
    main()


