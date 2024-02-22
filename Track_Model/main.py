from PyQt6.QtWidgets import (
    QApplication
)
import sys
from Track_Model import TrackModel
from Track_Model_UI import Window


# t = TrackModel('Blue Line.xlsx')
# print(t.get_data())
app = QApplication([])
window = Window()
window.show()
app.exec()
