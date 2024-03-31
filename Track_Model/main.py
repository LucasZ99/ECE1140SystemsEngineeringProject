from PyQt6.QtWidgets import (
    QApplication
)
import sys
from Track_Model import TrackModel
from Track_Model_UI import Window
import pandas as pd
import numpy as np
import random


t = TrackModel('Green Line.xlsx')

app = QApplication([])
window = Window()
window.show()
app.exec()
