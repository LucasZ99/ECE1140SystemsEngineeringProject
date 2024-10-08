import sys
import threading
from PyQt6.QtWidgets import QApplication

from Track_Model_Test_Launcher_Container import TrackModelTestContainer, TrackModelTestLauncherContainer

# Notes:
# You have to send authority to block b4 train bc train_dict in track model needs to be initialized


def run_launcher():
    # Create a QApplication instance, which manages the GUI application's control flow and main settings
    app = QApplication(sys.argv)

    # Create an instance of LauncherContainer, which manages the GUI components and their interactions
    launcher_container = TrackModelTestLauncherContainer()

    # Initialize and run the GUI within the main thread context
    launcher_container.init_launcher_ui()

    # Start the application's event loop, which processes user events and updates the GUI
    app.exec()


def main():
    try:
        launcher_thread = threading.Thread(target=run_launcher)
        launcher_thread.start()
        print("Launcher is starting...")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
