from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QLCDNumber, QApplication, QMainWindow
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
            self.switch_array[0] = temp_switch


class UI(QMainWindow):
    def __init__(self, switch_array):
        super(UI, self).__init__()

        # load ui
        uic.loadUi('track_controller.ui', self)

        self.switch_array = switch_array

        #Define widgets
        self.manual_mode = self.findChild(QPushButton, 'manual_mode')
        self.browse_button = self.findChild(QPushButton, 'browse')
        self.filename = self.findChild(QLabel, 'filename')
        self.block_occupied = self.findChild(QLCDNumber, 'block_number')
        self.switch_block = self.findChild(QLCDNumber, 'switch_block_number')
        self.light_b6 = self.findChild(QLabel, 'light_block_6')
        self.light_b11 = self.findChild(QLabel, 'light_block_7')
        self.rr_crossing = self.findChild(QLabel, 'label')

        #define connections
        self.manual_mode.clicked.connect(self.manual_mode_clicked)

        # show the app
        self.show()

    def manual_mode_clicked(self):
        manual_mode_page = Manual_Dialog(self.switch_array)
        manual_mode_page.show()

def main():
    switches = [switch(5, 6, 11, 6)]
    app = QApplication(sys.argv)
    UIWindow = UI(switches)
    app.exec_()


if __name__ == '__main__':
    main()

