from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit, QPushButton
from PyQt5 import uic
import sys


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # load the ui file
        uic.loadUi("testui.ui", self)

        # define widgets
        self.label = self.findChild(QLabel, "label")
        self.textedit = self.findChild(QTextEdit, "textEdit")
        self.button = self.findChild(QPushButton, "pushButton")
        self.clear_button = self.findChild(QPushButton, "pushButton_2")

        # define behavior
        self.button.clicked.connect(self.clicker)
        self.clear_button.clicked.connect(self.clearer)

        # show the app
        self.show()

    def clicker(self):
        self.label.setText(f'Hello There {self.textedit.toPlainText()}')
        self.textedit.setPlainText("")

    def clearer(self):
        self.textedit.setPlainText("")
        self.label.setText(f'Enter your name')


# initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec()
