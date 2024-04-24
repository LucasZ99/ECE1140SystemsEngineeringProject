from PyQt6.QtCore import pyqtSignal, QObject


class TrackModelSignalsCls(QObject):

    # Track Model/Container -> UI
    refresh_ui_signal = pyqtSignal()
    map_add_train_signal = pyqtSignal()
    map_move_train_signal = pyqtSignal(int, int)
    map_update_signal_signal = pyqtSignal(int, bool)
    map_update_rxr_signal = pyqtSignal(int, bool)
    map_update_closure_signal = pyqtSignal(int, bool)

    # Track Model data <- UI
    get_data_signal = pyqtSignal()
    get_block_info_signal = pyqtSignal(int)
    get_train_dict_signal = pyqtSignal()
    get_full_path_signal = pyqtSignal()

    # Track Model data -> UI
    send_data_signal = pyqtSignal(object)
    send_block_info_signal = pyqtSignal(object)
    send_train_dict_signal = pyqtSignal(dict)
    send_full_path_signal = pyqtSignal(object)

    # UI -> Track Model
    set_power_failure_signal = pyqtSignal(int, bool)
    set_track_circuit_failure_signal = pyqtSignal(int, bool)
    set_broken_rail_failure_signal = pyqtSignal(int, bool)

    set_env_temperature_signal = pyqtSignal(int)
    set_heaters_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(TrackModelSignalsCls, self).__init__(parent)


TrackModelSignals = TrackModelSignalsCls()
