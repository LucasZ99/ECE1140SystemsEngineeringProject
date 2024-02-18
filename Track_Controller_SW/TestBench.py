from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QWidget, QTextEdit, QPushButton, QLabel, QComboBox, QCheckBox, QGroupBox
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QCoreApplication
import numpy as np
from BusinessObject import BusinessLogic

# Global Variables
suggestSpeed = 50
numSwitches = 1
switches = [True] * numSwitches

class TbMainWindow(QMainWindow):
    occupancy_changed_signal = pyqtSignal(list)

    def __init__(self, authority_num, business_logic):
        super(TbMainWindow, self).__init__()

        self.authority = authority_num
        self.business_logic = business_logic
        self.blocks = np.copy(business_logic.occupancy_arr)

        self.setObjectName("MainWindow")
        self.resize(369, 365)
        self.setMinimumSize(369, 365)
        self.setMaximumSize(369, 365)
        self.centralwidget = QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")

        self.textEdit = QTextEdit(parent=self.centralwidget)
        self.textEdit.setGeometry(140, 210, 104, 31)
        self.textEdit.setObjectName("textEdit")

        self.pushButton = QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(200, 260, 75, 24)
        self.pushButton.setObjectName("pushButton")

        self.label_4 = QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(28, 40, 95, 16)
        self.label_4.setObjectName("label_4")

        self.comboBox_3 = QComboBox(parent=self.centralwidget)
        self.comboBox_3.setGeometry(140, 40, 71, 22)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItems(["Block 1", "Block 2", "Block 3", "Block 4", "Block 5", "Block 6", "Block 7",
                                  "Block 8", "Block 9", "Block 10", "Block 11", "Block 12", "Block 13",
                                  "Block 14", "Block 15"])

        self.groupBox = QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(9, 89, 351, 233)
        self.groupBox.setObjectName("groupBox")

        self.label = QLabel(parent=self.groupBox)
        self.label.setGeometry(40, 80, 81, 20)
        self.label.setObjectName("label")

        self.comboBox = QComboBox(parent=self.groupBox)
        self.comboBox.setGeometry(130, 80, 81, 22)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(["SW1", "SW2"])

        self.label_2 = QLabel(parent=self.groupBox)
        self.label_2.setGeometry(70, 30, 51, 20)
        self.label_2.setObjectName("label_2")

        self.textEdit_3 = QTextEdit(parent=self.groupBox)
        self.textEdit_3.setGeometry(130, 30, 104, 31)
        self.textEdit_3.setObjectName("textEdit_3")

        self.label_3 = QLabel(parent=self.groupBox)
        self.label_3.setGeometry(240, 30, 51, 20)
        self.label_3.setObjectName("label_3")

        self.checkBox_4 = QCheckBox(parent=self.groupBox)
        self.checkBox_4.setGeometry(230, 80, 51, 20)
        self.checkBox_4.setObjectName("checkBox_4")

        self.checkBox_6 = QCheckBox(parent=self.groupBox)
        self.checkBox_6.setGeometry(290, 80, 51, 20)
        self.checkBox_6.setObjectName("checkBox_6")

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

        self.pushButton_2 = QPushButton(parent=self.groupBox)
        self.pushButton_2.setGeometry(70, 170, 75, 24)
        self.pushButton_2.setObjectName("pushButton_2")

        self.groupBox_2 = QGroupBox(parent=self.centralwidget)
        self.groupBox_2.setGeometry(8, 10, 351, 71)
        self.groupBox_2.setObjectName("groupBox_2")

        self.checkBox_3 = QCheckBox(parent=self.centralwidget)
        self.checkBox_3.setGeometry(240, 40, 74, 20)
        self.checkBox_3.setObjectName("checkBox_3")

        self.label_5 = QLabel(parent=self.centralwidget)
        self.label_5.setGeometry(40, 210, 91, 20)
        self.label_5.setObjectName("label_5")

        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.textEdit.raise_()
        self.pushButton.raise_()
        self.label_4.raise_()
        self.comboBox_3.raise_()
        self.checkBox_3.raise_()
        self.label_5.raise_()

        self.setCentralWidget(self.centralwidget)

        self.retranslate_ui(self)

        # defaults
        self.checkBox_4.setChecked(True)
        self.textEdit_3.setText("5")
        self.textEdit.setText("50")

        # Events:
        self.checkBox_4.clicked.connect(self.sw_sel_left_handler)
        self.checkBox_6.clicked.connect(self.sw_sel_right_handler)
        self.pushButton.clicked.connect(self.apply_handler)
        self.checkBox_3.clicked.connect(self.bl_occupancy_handler)
        self.comboBox.currentIndexChanged.connect(self.sw_status_handler)
        self.comboBox_3.currentIndexChanged.connect(self.bl_status_handler)
        self.textEdit_3.textChanged.connect(self.auth_text_handler)
        self.textEdit.textChanged.connect(self.sug_speed_text_handler)
        self.pushButton_2.clicked.connect(self.defaults_press_handler)
        self.show()

    def retranslate_ui(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Track Controller Test Bench"))
        self.pushButton.setText(_translate("MainWindow", "Apply"))
        self.label_4.setText(_translate("MainWindow", "Block Occupancy:"))
        self.comboBox_3.addItems(["Block 1", "Block 2", "Block 3", "Block 4", "Block 5", "Block 6", "Block 7",
                                  "Block 8", "Block 9", "Block 10", "Block 11", "Block 12", "Block 13",
                                  "Block 14", "Block 15"])
        self.groupBox.setTitle(_translate("MainWindow", "Inputs from CTC:"))
        self.label.setText(_translate("MainWindow", "Switch Selction:"))
        self.comboBox.addItems(["SW1", "SW2"])
        self.label_2.setText(_translate("MainWindow", "Authority:"))
        self.label_3.setText(_translate("MainWindow", "blocks"))
        self.checkBox_4.setText(_translate("MainWindow", "Left"))
        self.checkBox_6.setText(_translate("MainWindow", "Right"))
        self.pushButton_2.setText(_translate("MainWindow", "Defaults"))
        self.label_6.setText(_translate("MainWindow", "m/s"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Inputs from Track Model:"))
        self.checkBox_3.setText(_translate("MainWindow", "Occupied"))
        self.label_5.setText(_translate("MainWindow", "Suggested Speed:"))

    # Handlers:
    # mutual exclusion for check boxes
    def sw_status_handler(self):
        if switches[self.comboBox.currentIndex()] == 'L':
            self.checkBox_4.setChecked(True)
            self.checkBox_6.setChecked(False)
        else:
            self.checkBox_4.setChecked(False)
            self.checkBox_6.setChecked(True)

    def sw_sel_left_handler(self):  # 'Left' checkbox is activated
        if self.checkBox_4.isChecked():
            self.checkBox_6.setChecked(False)
            switchIndex = self.comboBox.currentIndex()
            switches[switchIndex] = True
        else:
            self.checkBox_6.setChecked(True)

    def sw_sel_right_handler(self):  # 'Right' checkbox is activated
        if self.checkBox_6.isChecked():
            self.checkBox_4.setChecked(False)
            switchIndex = self.comboBox.currentIndex()
            switches[switchIndex] = False
        else:
            self.checkBox_4.setChecked(True)

    def bl_status_handler(self):  # New block is selected from the dropdown menu
        if self.blocks[self.comboBox_3.currentIndex()] == 'O':
            self.checkBox_3.setChecked(True)
        else:
            self.checkBox_3.setChecked(False)

    def defaults_press_handler(self):  # Defaults button is pressed
        global suggestSpeed
        global numSwitches
        global switches

        # assigning vals from defaults to variables
        self.authority = 5
        suggestSpeed = 50
        for i in range(0, numSwitches):
            switches[i] = True

        # updating UI
        if (self.checkBox_3.isChecked()) and (~self.business_logic.occupancy_arr[self.comboBox_3.currentIndex()]):
            self.checkBox_3.setChecked(False)
        self.comboBox_3.setCurrentIndex(0)

        self.textEdit_3.setText(str(self.authority))  # authority update

        self.checkBox_4.setChecked(True)  # switch state update
        self.checkBox_6.setChecked(False)
        self.comboBox.setCurrentIndex(0)

        self.textEdit.setText(str(suggestSpeed))  # suggested speed update

    def bl_occupancy_handler(self):  # The block occupancy status of a block is altered

        if self.checkBox_3.isChecked():
            #re assign occupancy to false
            self.blocks = [False] * len(self.blocks)
            self.blocks[self.comboBox_3.currentIndex()] = True
        else:
            self.blocks[self.comboBox_3.currentIndex()] = False

    def auth_text_handler(self):  # When the text field is changed for authority
        text = self.textEdit_3.toPlainText()  # checking to see if it is a valid integer
        text2 = self.textEdit.toPlainText()
        if text.isdigit():
            value = int(text)
            if value <= 0:
                self.label_7.setText("must be a positive integer")
                self.label_7.setStyleSheet("color: red")
                self.pushButton.setEnabled(False)
            else:
                self.label_7.setText("")
                self.authority = value
                if text2.isnumeric() or text2.replace(".", "").isnumeric():
                    self.pushButton.setEnabled(True)

        else:
            self.label_7.setText("must be a positive integer")
            self.label_7.setStyleSheet("color: red")
            self.pushButton.setEnabled(False)

    def sug_speed_text_handler(self):
        text = self.textEdit.toPlainText()  # checking to see if it is a valid integer
        text2 = self.textEdit_3.toPlainText()
        if text.isnumeric() or text.replace(".", "").isnumeric():  # text must be an int or float
            value = float(text)
            if value <= 0:
                self.label_8.setText("must be a positive value")
                self.label_8.setStyleSheet("color: red")
                self.pushButton.setEnabled(False)
            else:
                self.label_8.setText("")
                global suggestSpeed  # pass suggestSpeed out the global variable
                suggestSpeed = value
                if text2.isdigit():
                    self.pushButton.setEnabled(True)

        else:
            self.label_8.setText("must be a positive value")
            self.label_8.setStyleSheet("color: red")
            self.pushButton.setEnabled(False)

    def update_occupancy(self, blocks):
        QtCore.QMetaObject.invokeMethod(self, "occupancy_changed_signal",
                                        QtCore.Q_ARG(list, blocks))

    def apply_handler(self):  # When the apply button is pressed [this will be used to send vals out into main module]
        print("-----------------")
        print("BLOCK STATUS:")
        print("Blocks:", self.blocks)
        print("-----------------")
        print("SWITCH STATUS:")
        print("Switches:", switches)
        print("-----------------")
        print("AUTHORITY:")
        print("Authority:", self.authority, " blocks")
        print("-----------------")
        print("SUGGESTED SPEED:")
        print("Suggested Speed:", suggestSpeed, " m/s")
        print("-----------------")

        # Send occupancy change signal back to main UI, which calls business logic to change the data
        self.update_occupancy(self.blocks)
