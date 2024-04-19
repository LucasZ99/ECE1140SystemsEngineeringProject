from PyQt6.QtCore import pyqtSignal, QObject


class TrackControllerSignals(QObject):
    # UI get from Business logic
    get_switches_list_A_switch_ui_signal = pyqtSignal()
    get_switches_list_C_switch_ui_signal = pyqtSignal()

    get_switches_list_A_signal = pyqtSignal()
    get_switches_list_C_signal = pyqtSignal()

    get_occupancy_A_signal = pyqtSignal()
    get_occupancy_C_signal = pyqtSignal()

    get_lights_A_signal = pyqtSignal()
    get_lights_C_signal = pyqtSignal()

    get_filename_A_signal = pyqtSignal()
    get_filename_C_signal = pyqtSignal()

    # UI send to business logic:
    maintenance_switch_changed_A_signal = pyqtSignal(int)
    maintenance_switch_changed_C_signal = pyqtSignal(int)

    set_plc_filepath_A_signal = pyqtSignal(str)
    set_plc_filepath_C_signal = pyqtSignal(str)

    # Business logic send to UI signals
    send_switches_list_A_switch_ui_signal = pyqtSignal(list)
    send_switches_list_C_switch_ui_signal = pyqtSignal(list)

    send_switches_list_A_signal = pyqtSignal(list)
    send_switches_list_C_signal = pyqtSignal(list)

    send_occupancy_A_signal = pyqtSignal(dict)
    send_occupancy_C_signal = pyqtSignal(dict)

    init_lights_A_signal = pyqtSignal(list)
    init_lights_C_signal = pyqtSignal(list)

    send_filename_A_signal = pyqtSignal(str)
    send_filename_C_signal = pyqtSignal(str)

    send_rr_crossing_A_signal = pyqtSignal(bool)

    send_light_A_signal = pyqtSignal(int)
    send_light_C_signal = pyqtSignal(int)

    send_lights_signal = pyqtSignal(list)

    send_switch_changed_A_signal = pyqtSignal(int)
    send_switch_changed_C_signal = pyqtSignal(int)

    track_controller_A_switch_changed_signal = pyqtSignal(int)
    track_controller_C_switch_changed_signal = pyqtSignal(int)

    track_controller_A_lights_changed_signal = pyqtSignal(list)
    track_controller_C_lights_changed_signal = pyqtSignal(list)

    track_controller_A_rr_crossing_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(TrackControllerSignals, self).__init__(parent)


