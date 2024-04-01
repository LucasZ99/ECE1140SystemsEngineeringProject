import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from Train_Model import UITrain

ui: UITrain

if ui is None:
    ui = UITrain()

ui.isHidden()
