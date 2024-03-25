import sys
import threading

from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication
from Track_Controller_SW import TrackControllerContainer
from launcherui import LauncherUi


class LauncherContainer(QObject):
    def __init__(self, track_controller_container: TrackControllerContainer):
        super().__init__()
        self.track_controller_container = track_controller_container

    def init_launcher_ui(self):
        app = QApplication.instance()

        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one

        # Create and show the launcher UI
        launcher_ui = LauncherUi()

        # Create signal connections
        launcher_ui.open_track_controller_ui_signal.connect(self.open_track_controller_ui)

        # Show launcher
        launcher_ui.show()

        # run event loop
        app.exec()

    def create_launcher_ui(self):
        launcher = LauncherUi()

        # Connect signal to slot within the same thread
        launcher.open_track_controller_ui_signal.connect(self.open_track_controller_ui)

        launcher.show()

    # @pyqtSlot(str)
    def open_track_controller_ui(self, section: str):
        print("Signal received, section:", section)
        self.track_controller_container.show_ui(section)
