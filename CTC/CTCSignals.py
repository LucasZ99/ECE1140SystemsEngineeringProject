from PyQt6.QtCore import QObject, pyqtSignal


class CTCSignalsCls(QObject):
    update_wayside_from_ctc_signal = pyqtSignal(list, list, list)

    ui_scheduled_trains_signal = pyqtSignal(list)
    ui_next_train_number_signal = pyqtSignal(int)
    ui_running_trains_signal = pyqtSignal(list)
    ui_mode_signal = pyqtSignal(int)
    ui_blocks_signal = pyqtSignal(dict)
    # ui_track_signals_signal = pyqtSignal(list)
    ui_authorities_signal = pyqtSignal(dict)
    ui_suggested_speeds_signal = pyqtSignal(dict)
    ui_switch_positions_signal = pyqtSignal(list)
    ui_lights_signal = pyqtSignal(list)
    ui_railroad_crossings_signal = pyqtSignal(list)
    ui_ticket_sales = pyqtSignal(int)
    ui_throughput = pyqtSignal(int)

    # CTC UI to Backend Signals
    ctc_get_scheduled_trains_signal = pyqtSignal()
    ctc_get_next_train_number_signal = pyqtSignal()
    ctc_get_running_trains_signal = pyqtSignal()
    ctc_schedule_train_signal = pyqtSignal(object)
    ctc_get_mode_signal = pyqtSignal()
    ctc_set_mode_signal = pyqtSignal(int)
    ctc_update_queues_signal = pyqtSignal()
    ctc_get_blocks_signal = pyqtSignal()
    # ctc_get_track_signals_signal = pyqtSignal()
    ctc_get_authority_signal = pyqtSignal()
    ctc_get_suggested_speeds_signal = pyqtSignal()
    ctc_get_switch_positions_signal = pyqtSignal()
    ctc_get_lights_signal = pyqtSignal()
    ctc_get_railroad_crossings_signal = pyqtSignal()

    new_minute_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        print("CTCSignals.py init")


CTCSignals = CTCSignalsCls()
