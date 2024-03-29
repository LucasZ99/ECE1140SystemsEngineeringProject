from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot


class BusinessLogic(QObject):

    # declare signals
    train_list = dict()
    values_updated = pyqtSignal()
    block_updated = pyqtSignal(int)
    passengers_updated = pyqtSignal(int)
    temp_updated = pyqtSignal(int)
    train_added = pyqtSignal(int)
    train_removed = pyqtSignal(int)

