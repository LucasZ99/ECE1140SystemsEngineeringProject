from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLCDNumber
from PyQt5 import uic
import sys

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # load ui
        uic.loadUi('track_controller.ui', self)

        # show the app
        self.show()