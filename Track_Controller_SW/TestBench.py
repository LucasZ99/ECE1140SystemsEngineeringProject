import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, QCoreApplication
from PyQt6.QtWidgets import QMainWindow, QWidget, QTextEdit, QPushButton, QLabel, QComboBox, QCheckBox, QGroupBox


class TbMainWindow(QMainWindow):
    occupancy_changed_signal = pyqtSignal(list)
    switch_changed_signal = pyqtSignal(int)
    authority_updated = pyqtSignal(bool)
    sug_speed_updated = pyqtSignal(float)

    def __init__(self, business_logic):
        super(TbMainWindow, self).__init__()

        self.authority = business_logic.authority
        self.business_logic = business_logic
        self.blocks = np.copy(business_logic.occupancy_arr)
        self.switches = business_logic.switches_arr
        self.sug_speed = business_logic.suggested_speed

        self.setObjectName("MainWindow")
        self.resize(369, 365)
        self.setMinimumSize(369, 365)
        self.setMaximumSize(369, 365)
        self.centralwidget = QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")

        self.sug_speed = QTextEdit(parent=self.centralwidget)
        self.sug_speed.setGeometry(140, 210, 104, 31)
        self.sug_speed.setObjectName("textEdit")

        self.label_4 = QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(28, 40, 95, 16)
        self.label_4.setObjectName("label_4")

        self.comboBox_3 = QComboBox(parent=self.centralwidget)
        self.comboBox_3.setGeometry(140, 40, 71, 22)
        self.comboBox_3.setObjectName("comboBox_3")
        for i in range(len(self.blocks)):
            self.comboBox_3.addItem(f"Block {i}")

        self.groupBox = QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(9, 89, 351, 233)
        self.groupBox.setObjectName("groupBox")

        self.label = QLabel(parent=self.groupBox)
        self.label.setGeometry(40, 80, 81, 20)
        self.label.setObjectName("label")

        self.comboBox = QComboBox(parent=self.groupBox)
        self.comboBox.setGeometry(130, 80, 81, 22)
        self.comboBox.setObjectName("comboBox")
        for i in range(len(self.switches)):
            self.comboBox.addItem(f"SW{i + 1}")

        self.label_2 = QLabel(parent=self.groupBox)
        self.label_2.setGeometry(70, 30, 51, 20)
        self.label_2.setObjectName("label_2")

        self.authority_check = QCheckBox(parent=self.groupBox)
        self.authority_check.setGeometry(160, 15, 50, 50)
        self.authority_check.setObjectName("authority_check")

        self.switch_button = QPushButton(parent=self.groupBox)
        self.switch_button.setGeometry(230, 80, 60, 30)
        self.switch_button.setObjectName("switch_button")

        self.label_6 = QLabel(parent=self.groupBox)
        self.label_6.setGeometry(240, 120, 51, 20)
        self.label_6.setObjectName("label_6")

        self.label_7 = QLabel(parent=self.groupBox)
        self.label_7.setGeometry(120, 10, 131, 20)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")

        self.label_8 = QLabel(parent=self.groupBox)
        self.label_8.setGeometry(130, 100, 121, 20)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")

        self.groupBox_2 = QGroupBox(parent=self.centralwidget)
        self.groupBox_2.setGeometry(8, 10, 351, 71)
        self.groupBox_2.setObjectName("groupBox_2")

        self.show_button = QPushButton(parent=self.groupBox_2)
        self.show_button.setGeometry(240, 40, 75, 24)
        self.show_button.setObjectName("pushButton")

        self.checkBox_3 = QCheckBox(parent=self.centralwidget)
        self.checkBox_3.setGeometry(250, 30, 74, 20)
        self.checkBox_3.setObjectName("checkBox_3")

        self.label_5 = QLabel(parent=self.centralwidget)
        self.label_5.setGeometry(40, 210, 91, 20)
        self.label_5.setObjectName("label_5")

        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.sug_speed.raise_()
        self.show_button.raise_()
        self.label_4.raise_()
        self.comboBox_3.raise_()
        self.checkBox_3.raise_()
        self.label_5.raise_()

        self.setCentralWidget(self.centralwidget)

        self.retranslate_ui(self)

        # defaults
        # self.authority_check.setText("5")
        # self.textEdit.setText("50")

        # Events:
        self.switch_button.clicked.connect(self.sw_toggle_handler)
        self.show_button.clicked.connect(self.print_blocks)
        self.checkBox_3.clicked.connect(self.bl_occupancy_handler)
        self.comboBox_3.currentIndexChanged.connect(self.bl_status_handler)
        self.authority_check.stateChanged.connect(self.auth_handler)
        # TODO - Figure out how to implement read delay
        self.sug_speed.textChanged.connect(self.sug_speed_text_handler)
        self.show()

    def retranslate_ui(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Track Controller Test Bench"))
        self.show_button.setText(_translate("MainWindow", "Show Blocks"))
        self.show_button.adjustSize()
        self.label_4.setText(_translate("MainWindow", "Block Occupancy:"))
        self.groupBox.setTitle(_translate("MainWindow", "Inputs from CTC:"))
        self.label.setText(_translate("MainWindow", "Switch Selection:"))
        self.label.adjustSize()
        self.label_2.setText(_translate("MainWindow", "Authority:"))
        self.switch_button.setText(_translate("MainWindow", "Toggle"))
        self.label_6.setText(_translate("MainWindow", "m/s"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Inputs from Track Model:"))
        self.checkBox_3.setText(_translate("MainWindow", "Occupied"))
        self.label_5.setText(_translate("MainWindow", "Suggested Speed:"))

    # Handlers:
    def sw_toggle_handler(self):
        QtCore.QMetaObject.invokeMethod(self, "switch_changed_signal",
                                        QtCore.Q_ARG(int, self.comboBox_3.currentIndex()))

    def bl_status_handler(self):  # New block is selected from the dropdown menu
        if self.blocks[self.comboBox_3.currentIndex()] == 'O':
            self.checkBox_3.setChecked(True)
        else:
            self.checkBox_3.setChecked(False)

    def bl_occupancy_handler(self):  # The block occupancy status of a block is altered

        if self.checkBox_3.isChecked():
            # re-assign occupancy to false
            self.blocks = [False] * len(self.blocks)
            self.blocks[self.comboBox_3.currentIndex()] = True
        else:
            self.blocks[self.comboBox_3.currentIndex()] = False

        self.update_occupancy(self.blocks)

    def auth_handler(self):  # When the checkbox is changed for authority
        if self.authority_check.isChecked():
            QtCore.QMetaObject.invokeMethod(self, "authority_updated",
                                            QtCore.Q_ARG(bool, True))
        else:
            QtCore.QMetaObject.invokeMethod(self, "authority_updated",
                                            QtCore.Q_ARG(bool, False))

    def sug_speed_text_handler(self):
        text = self.sug_speed.toPlainText()  # checking to see if it is a valid integer
        if text.isnumeric() or text.replace(".", "").isnumeric():  # text must be an int or float
            value = float(text)
            if value <= 0:
                self.label_8.setText("must be a positive value")
                self.label_8.setStyleSheet("color: red")
                self.show_button.setEnabled(False)
            else:
                self.label_8.clear()
                self.update_sug_speed(value)
        else:
            self.label_8.setText("must be a positive number")
            self.label_8.setStyleSheet("color: red")
            self.show_button.setEnabled(False)

    def update_sug_speed(self, value):
        QtCore.QMetaObject.invokeMethod(self, "sug_speed_updated",
                                        QtCore.Q_ARG(float, value))

    def update_occupancy(self, blocks):
        QtCore.QMetaObject.invokeMethod(self, "occupancy_changed_signal",
                                        QtCore.Q_ARG(list, blocks))

    def print_blocks(self):  # When the apply button is pressed [this will be used to send vals out into main module]
        print("-----------------")
        print("BLOCK STATUS:")
        print(f"Blocks: {self.blocks}")
        print("-----------------")
