from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QGridLayout, QApplication
)
import sys

class DynamicMapSection(QPushButton):
    def __init__(self, text):
        super().__init__()
        self.setStyleSheet("""
        QPushButton {
            background-color: lightblue;
            border: 1px solid black;
            font: 12px;
            border-width: 2px;
            border-radius: 10px;
            border-color: black;
        }
        QPushButton:hover {
            background-color: blue;
            border-style: inset;
        }
        QPushButton:Text {
        background-color: white
        }
        """)
        self.setText(text)
        self.setFont(QFont("Arial white"))
        self.setFixedSize(200, 15)


class DynamicMap(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()

        self.button_a = DynamicMapSection("A")
        self.button_b = DynamicMapSection("B")
        self.button_c = DynamicMapSection("C")
        layout.addWidget(self.button_a, 1, 0)
        layout.addWidget(self.button_b, 0, 1)
        layout.addWidget(self.button_c, 2, 1)
        # TODO: Set spacing somehow and eventually automate
        self.setLayout(layout)


##############################
# Run app
##############################

# app = QApplication(sys.argv)
# window = DynamicMap()
# window.show()
# sys.exit(app.exec())
