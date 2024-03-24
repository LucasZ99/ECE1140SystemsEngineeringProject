import sys
import threading

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUi


class Launcher_UI(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('launcher.ui', self)
        self.show()

    def show_launcher_ui(self):
        app = QApplication(sys.argv)
        ui = Launcher_UI()
        ui.show()
        app.exec()

    def start_launcher_ui(self):
        launcher_thread = threading.Thread(target=self.show_launcher_ui)
        launcher_thread.start()


