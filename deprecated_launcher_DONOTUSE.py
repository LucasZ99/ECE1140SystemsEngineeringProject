import sys
import threading

from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QApplication

from CTC import CTCContainer
from launchercontainer import LauncherContainer


class TrainSystem(QThread):
    def __init__(self, ctc_container: CTCContainer) -> None:
        super().__init__()
        self.ctc_container = ctc_container

    def run(self):
        while True:
            pass
            # self.ctc_container.update_wayside_from_ctc()


def run_launcher():
    # Create a QApplication instance, which manages the GUI application's control flow and main settings
    app = QApplication(sys.argv)

    # Create an instance of LauncherContainer, which manages the GUI components and their interactions
    launcher_container = LauncherContainer()
    train_system = TrainSystem(launcher_container.ctc_container)

    # Initialize and run the GUI within the main thread context
    launcher_container.init_launcher_ui()

    # Runs the main event thread
    train_system.start()

    # Start the application's event loop, which processes user events and updates the GUI
    app.exec()

#
# def main():
#     try:
#         launcher_thread = threading.Thread(target=run_launcher)
#         launcher_thread.start()
#         print("Hello")
#     except Exception as e:
#         print(e)


if __name__ == "__main__":
    # main()
    run_launcher()
