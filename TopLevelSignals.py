from PyQt6.QtCore import pyqtSignal, QObject


class TopLevelSignals(QObject):

    # Track Controller test signals
    test_update_wayside_from_ctc = pyqtSignal(list, bool, list, list)
    test_update_wayside_from_track_model = pyqtSignal(dict)

    # Track Controller Signals
    update_track_model_from_wayside = pyqtSignal(list, list, list, list, list)
    update_ctc_from_wayside = pyqtSignal(dict, list, list, list)

    # CTC Signals:
    update_wayside_from_ctc = pyqtSignal(list, bool, list, list)

    # Track Model Signals
    update_wayside_from_track_model = pyqtSignal(dict)

    # for testing purposes
    update_testbench_from_wayside = pyqtSignal()
    update_wayside_from_testbench = pyqtSignal()


    def __init__(self, parent=None):
        super(TopLevelSignals, self).__init__(parent)

