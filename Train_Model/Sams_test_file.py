from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(611, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.clickme_button = QtWidgets.QPushButton(self.centralwidget)
        self.clickme_button.setGeometry(QtCore.QRect(170, 300, 271, 141))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.clickme_button.setFont(font)
        self.clickme_button.setObjectName("clickme_button")
        self.clickme_button.clicked.connect(self.press_it())
        self.Hello_Word_label = QtWidgets.QLabel(self.centralwidget)
        self.Hello_Word_label.setGeometry(QtCore.QRect(30, 70, 551, 121))
        font = QtGui.QFont()
        font.setPointSize(72)
        self.Hello_Word_label.setFont(font)
        self.Hello_Word_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Hello_Word_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Hello_Word_label.setObjectName("Hello_Word_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 611, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def press_it(self):
        self.Hello_World_label.setText("Boom!")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.clickme_button.setText(_translate("MainWindow", "click me"))
        self.Hello_Word_label.setText(_translate("MainWindow", "Hello World!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())