from PyQt6.QtCore import pyqtSignal, pyqtSlot


class TrainControllerSWSignals:

    # signals to UI
    update_mode_from_controller = pyqtSignal()
    update_extLights_from_controller = pyqtSignal()
    update_intLights_from_controller = pyqtSignal()
    update_cabinTemp_from_controller = pyqtSignal()
    update_doorOpen_from_controller = pyqtSignal()
    update_station_from_controller = pyqtSignal()
    update_doorSide_from_controller = pyqtSignal()
    update_kp_from_controller = pyqtSignal()
    update_ki_from_controller = pyqtSignal()
    update_speedLim_from_controller = pyqtSignal()
    update_actSpeed_from_controller = pyqtSignal()
    update_setSpeed_from_controller = pyqtSignal()
    update_power_from_controller = pyqtSignal()
    update_serviceBrake_from_controller = pyqtSignal()
    update_eBrake_from_controller = pyqtSignal()

    # signals to controller
    update_autoMode_from_ui = pyqtSignal()
    update_manualMode_from_ui = pyqtSignal()
    update_extLights_from_ui = pyqtSignal()
    update_intLights_from_ui = pyqtSignal()
    update_cabinTemp_from_ui = pyqtSignal()
    update_doorOpen_from_ui = pyqtSignal()
    update_kp_from_ui = pyqtSignal()
    update_ki_from_ui = pyqtSignal()
    update_setSpeed_from_ui = pyqtSignal()
    update_serviceBrake_from_ui = pyqtSignal()
    update_eBrake_from_ui = pyqtSignal()

    update_actSpeed_from_ui = pyqtSignal()
    update_cmdSpeed_from_ui = pyqtSignal()
    update_authority_from_ui = pyqtSignal()
    update_passEBrake_from_ui = pyqtSignal()
    update_polarity_from_ui = pyqtSignal()
    update_signalFail_from_ui = pyqtSignal()
    update_engineFail_from_ui = pyqtSignal()
    update_brakeFail_from_ui = pyqtSignal()
    update_doorSide_from_ui = pyqtSignal()
    update_beacon_from_ui = pyqtSignal()

    update_tb_from_ui = pyqtSignal()

    # signals to container?

    def __init__(self):

        # connect signals from UI to Controller

        # connect signals from Controller to UI

        # connect signals to container ?

        pass
