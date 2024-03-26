from PyQt6.QtWidgets import QApplication

from Track_Controller_SW import BusinessLogic, TbMainWindow


class TestbenchContainer:
    def __init__(self, business_logic : BusinessLogic):
        self.business_logic = business_logic

    def show_ui(self):
        app = QApplication.instance()  # Get the QApplication instance

        # app_flag = False
        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one
            # app_flag = True

        print("before tb ui call")
        self.testbench_ui = TbMainWindow(self.business_logic)

        print("before tb ui show")
        self.testbench_ui.show()

        # if app_flag is True:
        app.exec()
