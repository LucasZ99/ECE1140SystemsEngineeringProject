from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication

from Track_Model_Test_UI import TrackModelTestUI


class TrackModelTestContainer(QObject):
    update_track_model_from_wayside = pyqtSignal(list, list, list, list, list)
    update_track_model_from_train_model = pyqtSignal(object, object)
    def __init__(self):
        super().__init__()

        # test ui
        self.test_ui = TrackModelTestUI()

        # catch signals
        self.test_ui.update_track_model_from_wayside.connect(self.update_track_model_from_wayside_emit)
        self.test_ui.update_track_model_from_train_model.connect(self.update_track_model_from_train_model_emit)

    def update_track_model_from_wayside_emit(self, a, b, c, d, e):
        self.update_track_model_from_wayside.emit(a, b, c, d, e)

    def update_track_model_from_train_model_emit(self, a, b):
        self.update_track_model_from_train_model.emit(a, b)

    def show_ui(self):
        app = QApplication.instance()  # Get the QApplication instance

        # app_flag = False
        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one
            # app_flag = True

        self.test_ui.show()

        # if app_flag is True:
        app.exec()
