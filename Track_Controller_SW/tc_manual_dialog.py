from PyQt5.QtWidgets import QDialog, QPushButton
from PyQt5 import uic
import sys
from switching import switch


class Manual_Dialog(QDialog):
    def __init__(self, switches):
        super(Manual_Dialog, self).__init__()
        uic.loadUi('Manual Mode.ui', self)
        self.setWindowTitle('Manual Mode')

        self.switch_array = switches

        # Define widgets
        self.toggle_switch_1 = self.findChild(QPushButton, 'pushButton')

        # Connect signals
        self.toggle_switch_1.clicked.connect(self.toggle_switch_1)

        self.show()

    def toggle_switch_1(self):
        temp_switch = self.switch_array[0]

        if temp_switch is switch:
            temp_switch.toggle()


if __name__ == '__main__':
    switches = [switch(5, 6, 11, 6)]
    UI = Manual_Dialog(switches)
    UI.show()