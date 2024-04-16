from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication

from TrackControllerTest import TestBusinessLogic, TestUi


class TrackControllerTestBenchContainer(QObject):

    test_update_wayside_from_ctc = pyqtSignal(list, bool, list, list)
    test_update_wayside_from_track_model = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.test_business_logic = TestBusinessLogic()

        self.test_business_logic.ctc_inputs_from_testbench_signal.connect(self.update_wayside_from_ctc)
        self.test_business_logic.track_inputs_from_testbench_signal.connect(self.update_wayside_from_track_model)

    @pyqtSlot(list)
    def update_wayside_from_ctc(self, track_signal: list):
        self.test_update_wayside_from_ctc.emit(track_signal, False, [], [])

    @pyqtSlot(dict)
    def update_wayside_from_track_model(self, occupancy_dict: dict):
        self.test_update_wayside_from_track_model.emit(occupancy_dict)

    def show_ui(self):
        app = QApplication.instance()  # Get the QApplication instance

        # app_flag = False
        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one

        self.ui = TestUi(self.test_business_logic)
        self.ui.show()

        # if app_flag is True:
        app.exec()


def main():
    track_controller_testbench_container = TrackControllerTestBenchContainer()
    track_controller_testbench_container.show_ui()


if __name__ == "__main__":
    main()

