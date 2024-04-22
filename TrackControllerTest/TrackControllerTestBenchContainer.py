from PyQt6.QtCore import QObject, pyqtSlot

from TopLevelSignals import TopLevelSignals as top_level_signals
from TrackControllerTest.TrackControllerTestSignals import TrackControllerTestSignals as signals
from TrackControllerTest import TestBackend


class TrackControllerTestBenchContainer(QObject):

    def __init__(self):
        super().__init__()
        self.test_backend = TestBackend()
        # self.ui = TestUi()
        self.top_level_signals = top_level_signals
        self.signals = signals

        self.signals.ctc_inputs_from_testbench_signal.connect(self.update_wayside_from_ctc)
        self.signals.track_inputs_from_testbench_signal.connect(self.update_wayside_from_track_model)

        # self.top_level_signals.update_testbench_from_wayside.connect(self.test_continuous_update)

    # @pyqtSlot()
    # def test_continuous_update(self):
    #     print("TB: continuous update")
    #     self.top_level_signals.update_wayside_from_testbench.emit()

    @pyqtSlot(list)
    def update_wayside_from_ctc(self, track_signal: list):
        self.top_level_signals.test_update_wayside_from_ctc.emit(track_signal, [], [])

    @pyqtSlot(dict)
    def update_wayside_from_track_model(self, occupancy_dict: dict):
        self.top_level_signals.test_update_wayside_from_track_model.emit(occupancy_dict)

    # def show_ui(self):
    #     app = QApplication.instance()  # Get the QApplication instance
    #
    #     # app_flag = False
    #     if app is None:
    #         app = QApplication([])  # If QApplication instance doesn't exist, create a new one
    #
    #     self.ui.show()
    #
    #     # if app_flag is True:
    #     app.exec()


def main():
    track_controller_testbench_container = TrackControllerTestBenchContainer()
    track_controller_testbench_container.show_ui()


if __name__ == "__main__":
    main()

