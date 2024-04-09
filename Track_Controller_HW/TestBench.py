# Form implementation generated from reading ui file 'TestBench.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import threading
import sys
import copy
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal, QCoreApplication, pyqtSlot
from PyQt6.QtWidgets import QMainWindow
import os

from Track_Controller_HW import SlotsSigs


# Global Variables


#current_dir = os.path.dirname(__file__)  # setting up dir to work in any location in a directory
#tb_subdir = 'TBData'
#tb_subfolder = os.path.join(current_dir, tb_subdir)
#path = os.path.join(tb_subdir, 'TBData.txt')
#print(tb_subfolder)



class Tb_Ui(QMainWindow):

    occupancy_changed_signal = pyqtSignal(dict)
    switch_changed_signal = pyqtSignal(list)
    authority_updated_signal = pyqtSignal(bool)
    sug_speed_updated_signal = pyqtSignal(list)
    
    def __init__(self, slots_sigs: SlotsSigs):
        super(Tb_Ui, self).__init__()

        self.authority = slots_sigs.authority
        self.suggestedSpeed = slots_sigs.suggested_speed
        self.switches = slots_sigs.switches
        self.blocks = slots_sigs.blocks

        self.slots_sigs = slots_sigs
        self.slots_sigs.occupancy_signal.connect(self.occupancy_changed_signal)
        self.slots_sigs.switches_signal.connect(self.switch_changed_signal)
        self.slots_sigs.suggested_speed_signal.connect(self.sug_speed_updated_signal)
        
        
        #print("Setting up UI...")
        self.setObjectName("MainWindow")
        self.resize(369, 365)
        self.setMinimumSize(QtCore.QSize(369, 365))
        self.setMaximumSize(QtCore.QSize(369, 365))
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")

        self.suggSpeedText = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.suggSpeedText.setGeometry(QtCore.QRect(140, 210, 104, 31))
        self.suggSpeedText.setObjectName("SuggestedSpeed")

        self.apply = QtWidgets.QPushButton(parent=self.centralwidget)
        self.apply.setGeometry(QtCore.QRect(200, 260, 75, 24))
        self.apply.setObjectName("apply")

        self.blOccLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.blOccLabel.setGeometry(QtCore.QRect(28, 40, 95, 16))
        self.blOccLabel.setObjectName("blockOccLabel")

        self.blOccDropdown = QtWidgets.QComboBox(parent=self.centralwidget)
        self.blOccDropdown.setGeometry(QtCore.QRect(140, 40, 71, 22))
        self.blOccDropdown.setObjectName("blOccDropdown")
        for i, block_val in enumerate(self.blocks):
            self.blOccDropdown.addItem(f"Block {i}")


        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(9, 89, 351, 233))
        self.groupBox.setObjectName("groupBox")

        self.swSelLabel = QtWidgets.QLabel(parent=self.groupBox)
        self.swSelLabel.setGeometry(QtCore.QRect(40, 80, 81, 20))
        self.swSelLabel.setObjectName("switchSelLabel")

        self.swSelDropdown = QtWidgets.QComboBox(parent=self.groupBox)
        self.swSelDropdown.setGeometry(QtCore.QRect(130, 80, 81, 22))
        self.swSelDropdown.setObjectName("swSelDropdown")
        self.swSelDropdown.addItem("")

        self.authLabel = QtWidgets.QLabel(parent=self.groupBox)
        self.authLabel.setGeometry(QtCore.QRect(70, 30, 51, 20))
        self.authLabel.setObjectName("authLabel")

        self.authText = QtWidgets.QTextEdit(parent=self.groupBox)
        self.authText.setGeometry(QtCore.QRect(130, 30, 104, 31))
        self.authText.setObjectName("authText")

        self.blocksLabel = QtWidgets.QLabel(parent=self.groupBox)
        self.blocksLabel.setGeometry(QtCore.QRect(240, 30, 51, 20))
        self.blocksLabel.setObjectName("blocksLabel")

        self.swLeftCheck = QtWidgets.QCheckBox(parent=self.groupBox)
        self.swLeftCheck.setGeometry(QtCore.QRect(230, 80, 51, 20))
        self.swLeftCheck.setObjectName("swLeftCheck")

        self.swRightCheck = QtWidgets.QCheckBox(parent=self.groupBox)
        self.swRightCheck.setGeometry(QtCore.QRect(290, 80, 51, 20))
        self.swRightCheck.setObjectName("swRightCheck")

        self.msLabel = QtWidgets.QLabel(parent=self.groupBox)
        self.msLabel.setGeometry(QtCore.QRect(240, 120, 51, 20))
        self.msLabel.setObjectName("msLabel")

        self.authWarnLabel = QtWidgets.QLabel(parent=self.groupBox)
        self.authWarnLabel.setGeometry(QtCore.QRect(120, 10, 131, 20))
        self.authWarnLabel.setText("")
        self.authWarnLabel.setObjectName("authWarnLabel")

        self.speedWarnLabel = QtWidgets.QLabel(parent=self.groupBox)
        self.speedWarnLabel.setGeometry(QtCore.QRect(130, 100, 121, 20))
        self.speedWarnLabel.setText("")
        self.speedWarnLabel.setObjectName("speedWarnLabel")

        self.defaults = QtWidgets.QPushButton(parent=self.groupBox)
        self.defaults.setGeometry(QtCore.QRect(70, 170, 75, 24))
        self.defaults.setObjectName("defaults")

        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(8, 10, 351, 71))
        self.groupBox_2.setObjectName("groupBox_2")

        self.occCheck = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.occCheck.setGeometry(QtCore.QRect(240, 40, 74, 20))
        self.occCheck.setObjectName("occCheck")

        self.suggSpeedLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.suggSpeedLabel.setGeometry(QtCore.QRect(40, 210, 91, 20))
        self.suggSpeedLabel.setObjectName("suggSpeedLabel")

        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.suggSpeedText.raise_()
        self.apply.raise_()
        self.blOccLabel.raise_()
        self.blOccDropdown.raise_()
        self.occCheck.raise_()
        self.suggSpeedLabel.raise_()

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 369, 22))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslate_ui(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        # defaults
        self.swLeftCheck.setChecked(True)
        self.authText.setText("5")
        self.suggSpeedText.setText("50")


        # Events:
        #print("Connecting events...")
        self.swLeftCheck.clicked.connect(self.sw_sel_left_handler)

        self.swRightCheck.clicked.connect(self.sw_sel_right_handler)

        self.apply.clicked.connect(self.apply_handler)

        self.occCheck.clicked.connect(self.bl_occupancy_handler)

        self.swSelDropdown.currentIndexChanged.connect(self.sw_status_handler)

        self.blOccDropdown.currentIndexChanged.connect(self.bl_status_handler)

        self.authText.textChanged.connect(self.auth_text_handler)

        self.suggSpeedText.textChanged.connect(self.sug_speed_text_handler)

        self.defaults.clicked.connect(self.defaults_press_handler)
        #print("Event connections completed.")

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Track Controller Test Bench"))
        self.apply.setText(_translate("self", "Apply"))
        self.blOccLabel.setText(_translate("self", "Block Occupancy:"))
        self.groupBox.setTitle(_translate("self", "Inputs from CTC:"))
        self.swSelLabel.setText(_translate("self", "Switch Selction:"))
        self.swSelDropdown.setItemText(0, _translate("self", "SW1"))
        self.authLabel.setText(_translate("self", "Authority:"))
        self.blocksLabel.setText(_translate("self", "blocks"))
        self.swLeftCheck.setText(_translate("self", "Left"))
        self.swRightCheck.setText(_translate("self", "Right"))
        self.defaults.setText(_translate("self", "Defaults"))
        self.msLabel.setText(_translate("self", "m/s"))
        self.groupBox_2.setTitle(_translate("self", "Inputs from Track Model:"))
        self.occCheck.setText(_translate("self", "Occupied"))
        self.suggSpeedLabel.setText(_translate("self", "Suggested Speed:"))

    # Handlers:
    # mutual exclusion for check boxes
    #print("Connecting events...2")
    def sw_status_handler(self):
        if self.switches[self.swSelDropdown.currentIndex()] == False:
            self.swLeftCheck.setChecked(True)
            self.swRightCheck.setChecked(False)
        else:
            self.swLeftCheck.setChecked(False)
            self.swRightCheck.setChecked(True)

    def sw_sel_left_handler(self):  # 'Left' checkbox is activated
        if self.swLeftCheck.isChecked():
            self.swRightCheck.setChecked(False)
            switch_index = self.swSelDropdown.currentIndex()
            self.switches[switch_index] = False
        else:
            self.swRightCheck.setChecked(True)

    def sw_sel_right_handler(self):  # 'Right' checkbox is activated
        if self.swRightCheck.isChecked():
            self.swLeftCheck.setChecked(False)
            switch_index = self.swSelDropdown.currentIndex()
            self.switches[switch_index] = True
        else:
            self.swLeftCheck.setChecked(True)

    def bl_status_handler(self):  # New block is selected from the dropdown menu
        if self.blocks[self.blOccDropdown.currentIndex()] == True:
            self.occCheck.setChecked(True)
        else:
            self.occCheck.setChecked(False)

    def defaults_press_handler(self):  # Defaults button is pressed

        # assigning vals from defaults to variables
        self.authority = 5
        self.suggestedSpeed = 50
        for i in enumerate(self.switches):
            self.switches[i] = False
        for j in enumerate(self.blocks):
            self.blocks[j] = False

        # updating UI
        if (self.occCheck.isChecked()) and (self.blocks[self.blOccDropdown.currentIndex()] == False):
            self.occCheck.setChecked(False)
        self.blOccDropdown.setCurrentIndex(0)

        self.authText.setText(str(self.authority))  # authority update

        self.swLeftCheck.setChecked(True)  # switch state update
        self.swRightCheck.setChecked(False)
        self.swSelDropdown.setCurrentIndex(0)

        self.suggSpeedText.setText(str(self.suggestedSpeed))  # suggested speed update

    def bl_occupancy_handler(self):  # The block occupancy status of a block is altered
        if self.occCheck.isChecked():
            self.blocks[self.blOccDropdown.currentIndex()] = True
        else:
            self.blocks[self.blOccDropdown.currentIndex()] = False

    def auth_text_handler(self):  # When the text field is changed for authority
        text = self.authText.toPlainText()  # checking to see if it is a valid integer
        text2 = self.suggSpeedText.toPlainText()
        if text.isdigit():
            value = int(text)
            if value <= 0:
                self.authWarnLabel.setText("must be positive integer")
                self.authWarnLabel.setStyleSheet("color : red")
                self.apply.setEnabled(False)
            else:
                self.authWarnLabel.setText("")
                self.authority = value
                if text2.isnumeric() or text2.replace(".", "").isnumeric():
                    self.apply.setEnabled(True)

        else:
            self.authWarnLabel.setText("must be positive integer")
            self.authWarnLabel.setStyleSheet("color : red")
            self.apply.setEnabled(False)

    def sug_speed_text_handler(self):
        text = self.suggSpeedText.toPlainText()  # checking to see if it is a valid integer
        text2 = self.authText.toPlainText()
        if text.isnumeric() or text.replace(".", "").isnumeric():  # text must be an int or float
            value = float(text)
            if value <= 0:
                self.speedWarnLabel.setText("must be positive value")
                self.speedWarnLabel.setStyleSheet("color : red")
                self.apply.setEnabled(False)
            else:
                self.speedWarnLabel.setText("")
                self.suggestedSpeed[0] = value
                if text2.isdigit():
                    self.apply.setEnabled(True)

        else:
            self.speedWarnLabel.setText("must be positive value")
            self.speedWarnLabel.setStyleSheet("color : red")
            self.apply.setEnabled(False)

    def apply_handler(self):  # When the apply button is pressed [this will be used to send vals out into main module]
        self.slots_sigs.new_speed(self.suggestedSpeed)
        self.slots_sigs.new_occupancy(self.blocks)
        self.slots_sigs.new_switches(self.switches)

    #print("Event connections completed.2")


