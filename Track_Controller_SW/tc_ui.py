import functools

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QFileDialog, QDialog, QPushButton, QLabel, QLCDNumber, QApplication, QMainWindow, QWidget, \
    QVBoxLayout
from PyQt5 import uic
import sys
from switching import switch
from PLC_Logic import parse_plc


def better_button_ret(size=None, text1=None, text2=None, checkable=True, style1=None, style2=None):
    if text1 and not text2: text2 = text1
    button = QPushButton()
    button.setCheckable(checkable)
    button.setFixedHeight(24)
    # button.clicked.connect( functools.partial(button_click1, but=button) )
    if checkable:
        # button.setStyleSheet(
        #     "background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px")
        if text1:
            button.setText(text1)
        else:
            button.setText("Off")
        button.clicked.connect(
            functools.partial(gen_but_tog, but=button, text1=text1, text2=text2, style_on=style1, style_off=style2))
    else:
        # button.setStyleSheet("background-color: rgb(222, 62, 38); border: 2px solid rgb(222, 0, 0); border-radius: 4px")
        if text1: button.setText(text2)
    if size: button.setFixedWidth(size)
    return button


def gen_but_tog(but, text1=None, text2=None, style_on=None, style_off=None):
    if but.isChecked():
        # but.setStyleSheet(
        #     f"{style_on if style_on else 'background-color: rgb(143, 186, 255); border: 2px solid rgb( 42,  97, 184); border-radius: 6px'}")
        if text1:
            but.setText(text2)
        else:
            but.setText("On")
    else:
        # but.setStyleSheet(
        #     f"{style_off if style_off else 'background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px'}")
        if text1:
            but.setText(text1)
        else:
            but.setText("Off")


class ManualMode(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Manual Mode')
        self.setFixedSize(400, 400)

        self.toggle_button = better_button_ret(200, text1="Facing Block 6", text2= "Facing Block 11")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.toggle_button)


    def toggle(self):
        if self.toggle_button.text() == 'Facing block 6':
            self.toggle_button.setText('Facing block 11')
            # update switch array
        else:
            self.toggle_button.setText('Facing block 6')
            # update switch array


class UI(QMainWindow):
    def __init__(self, switch_array, plc_logic):
        super(UI, self).__init__()
        # load ui
        uic.loadUi('track_controller.ui', self)

        # Fix the size
        self.setFixedWidth(757)
        self.setFixedHeight(649)

        # Assign attributes
        self.switch_array = switch_array
        self.plc_logic = plc_logic

        # Define widgets
        self.manual_mode = self.findChild(QPushButton, 'manual_mode')
        self.browse_button = self.findChild(QPushButton, 'browse')
        self.filename = self.findChild(QLabel, 'filename')
        self.block_occupied = self.findChild(QLCDNumber, 'block_number')
        self.switch_block = self.findChild(QLCDNumber, 'switch_block_number')
        self.light_b6 = self.findChild(QLabel, 'light_block_6')
        self.light_b11 = self.findChild(QLabel, 'light_block_7')
        self.rr_crossing = self.findChild(QLabel, 'label')

        # define connections
        # self.manual_mode.clicked.connect(self.manual_mode_clicked)
        self.browse_button.clicked.connect(self.browse_files)
        self.manual_mode.clicked.connect(self.window2)

        # show the app
        self.show()

    def window2(self):
        self.w = ManualMode()
        self.w.show()

    # def manual_mode_clicked(self):

    def browse_files(self):
        fname = QFileDialog.getOpenFileName(self, 'Open PLC File', 'C:/Users/lucas')
        self.filename.setText(fname[0])
        self.filename.adjustSize()

        # send filename to parsing program
        self.plc_logic.set_filepath(fname[0])
        # print(self.plc_logic.filepath)

    # def update_occupancy(self):


def main(switches_arr, plc_logic):
    app = QApplication(sys.argv)
    UIWindow = UI(switches_arr, plc_logic)
    UIWindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
