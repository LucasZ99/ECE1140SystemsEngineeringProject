import sys
import threading

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUi


class Launcher_UI(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('launcher.ui', self)
        self.show()

def show_launcher_ui():
    app = QApplication(sys.argv)
    ui = Launcher_UI()
    ui.show()
    app.exec()

def start_launcher_ui():
    launcher_thread = threading.Thread(target=show_launcher_ui)
    launcher_thread.start()

start_launcher_ui()
print('Launcher started')
