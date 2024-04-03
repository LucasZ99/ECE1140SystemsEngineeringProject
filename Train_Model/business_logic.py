from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot


class TrainBusinessLogic(QObject):

    # declare signals
    train_list = dict()
    values_updated = pyqtSignal(int)
    block_updated = pyqtSignal(int)
    passengers_updated = pyqtSignal(int)
    temp_updated = pyqtSignal(int)
    train_added = pyqtSignal(int)
    train_removed = pyqtSignal(int)

    def update_values(self):
        self.values_updated.emit(1)

