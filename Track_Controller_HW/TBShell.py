from PyQt6.QtWidgets import QApplication

from Track_Controller_HW import SlotsSigs
from Track_Controller_HW.TestBench import Tb_Ui


class TB_Shell:
    def __init__(self, slots_sigs: SlotsSigs):
        self.slots_sigs = slots_sigs

    def show_ui(self):
        app = QApplication.instance()  # Get the QApplication instance

        # app_flag = False
        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one
            # app_flag = True

        print("before tb ui call")
        self.testbench_ui = Tb_Ui(self.slots_sigs)

        print("before tb ui show")
        self.testbench_ui.show()

        # if app_flag is True:
        app.exec()


