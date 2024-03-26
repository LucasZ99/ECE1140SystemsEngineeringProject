import sys
import threading

from PyQt6.QtWidgets import QApplication

from Track_Controller_SW import TrackControllerContainer
from launchercontainer import LauncherContainer


def run_launcher():
    # Create a QApplication instance, which manages the GUI application's control flow and main settings
    app = QApplication(sys.argv)

    # Create an instance of LauncherContainer, which manages the GUI components and their interactions
    track_controller_container = TrackControllerContainer()
    launcher_container = LauncherContainer(track_controller_container)

    # Initialize and run the GUI within the main thread context
    launcher_container.init_launcher_ui()

    # Start the application's event loop, which processes user events and updates the GUI
    app.exec()


def main():
    launcher_thread = threading.Thread(target = run_launcher)
    launcher_thread.start()
    print("Hello")


if __name__ == "__main__":
    main()
