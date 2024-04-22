from PyQt6.QtCore import QObject, pyqtSignal


class TrainModelSignalsCls(QObject):

    # business to container signals
    business_update = pyqtSignal(object, object)

    # container to business signals
    send_back_track_returns = pyqtSignal()
    physics_calculation = pyqtSignal()
    train_update_controller = pyqtSignal()
    track_update_passenger = pyqtSignal(int, int)
    track_update_block = pyqtSignal(tuple, int)
    track_model_inputs = pyqtSignal(tuple, int)
    business_add_train = pyqtSignal()
    business_remove_train = pyqtSignal(int)
    clear_return_dicts = pyqtSignal()
    controller_update_temp = pyqtSignal(float, int)
    train_controller_inputs = pyqtSignal(tuple, int)

    # business to ui signals
    ui_remove_train = pyqtSignal(object, int)
    ui_add_train = pyqtSignal(object, int)
    index_update = pyqtSignal(object, int)
    total_update = pyqtSignal(object)
    pass_dict_to_ui = pyqtSignal(object)

    # ui to business signals
    ui_update = pyqtSignal(object)
    ui_initialization = pyqtSignal()

    # testbench to container signals
    tb_track_model_inputs = pyqtSignal(tuple, int)
    tb_train_controller_inputs = pyqtSignal(tuple, int)
    tb_track_update_block = pyqtSignal(tuple, int)
    tb_track_update_passenger = pyqtSignal(int, int)
    tb_controller_update_temp = pyqtSignal(float, int)
    tb_physics_calculation = pyqtSignal()
    tb_add_train = pyqtSignal()
    tb_remove_train = pyqtSignal(int)

    def __init__(self):
        super().__init__()


train_model_signals = TrainModelSignalsCls()
