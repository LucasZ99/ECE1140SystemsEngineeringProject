from PyQt6.QtWidgets import (
    QApplication
)
import sys
from Track_Model import TrackModel
from Track_Model.oldUI import Window
import pandas as pd
import numpy as np
import random


t = TrackModel('Green Line.xlsx')

t.train_spawned()
t.train_presence_changed(1)
t.train_presence_changed(1)
t.train_presence_changed(1)
t.train_presence_changed(1)
app = QApplication([])
window = Window()
window.show()
app.exec()
