from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QGridLayout, QComboBox, QHBoxLayout, QButtonGroup, QTableWidget, QFrame


class CTC_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CTC Office")


        dispatch_train_layout = QVBoxLayout()

        # Dispatch Train Label
        dispatch_label = QLabel("Dispatch Train")
        dispatch_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        dispatch_train_layout.addWidget(dispatch_label)

        # Line Select
        train_lines = ["Red Line", "Green Line"]

        dispatch_line_select_buttons_layout = QHBoxLayout()
        dispatch_line_select_buttons_layout.setContentsMargins(0,0,0,0)

        line_select_buttons = QButtonGroup()
        line_select_buttons.setExclusive(True)

        # TODO add exclusivity button handler for dispatch line select
        for line in train_lines:
            line_select_button = QPushButton()
            dispatch_line_select_buttons_layout.addWidget(line_select_button)
            line_select_button.setText(line)
            line_select_button.setCheckable(True)
            line_select_buttons.addButton(line_select_button)


        dispatch_train_layout.addItem(dispatch_line_select_buttons_layout)

        # Destination Select, Arrival/Departure Time Set, Train Number
        dispatch_train_dispatch_information_grid = QGridLayout()

        # Destination Select
        dispatch_train_destination_selector = QComboBox()
        dispatch_train_destination_selector.addItems(["Select Destination...", "Dormont", "South Hills"])
        dispatch_train_dispatch_information_grid.addWidget(dispatch_train_destination_selector, 0,0)

        dispatch_train_train_number = QLabel()
        dispatch_train_train_number.setText(f"Train Number: %d" % 1)
        dispatch_train_dispatch_information_grid.addWidget(dispatch_train_train_number, 1, 0)

        # Arrival Time
        dispatch_train_arrival_time = QLineEdit()
        dispatch_train_arrival_time.setInputMask("00:00")
        dispatch_train_arrival_time.setText("15:10")
        # dispatch_train_arrival_time.textEdited.

        dispatch_train_departure_time = QLineEdit()
        dispatch_train_departure_time.setInputMask("00:00")
        dispatch_train_departure_time.setText("12:47")

        depart_now_button = QPushButton()
        depart_now_button.setText("Now")

        dispatch_train_dispatch_information_grid.addWidget(dispatch_train_arrival_time, 0, 1)
        dispatch_train_dispatch_information_grid.addWidget(dispatch_train_departure_time, 1, 1)
        dispatch_train_dispatch_information_grid.addWidget(depart_now_button, 1, 2)

        dispatch_train_information_grid_widget = QWidget()
        dispatch_train_information_grid_widget.setLayout(dispatch_train_dispatch_information_grid)

        dispatch_train_layout.addWidget(dispatch_train_information_grid_widget)


        # List of stops
        dispatch_train_schedule = QTableWidget()
        dispatch_train_schedule.setColumnCount(4)
        dispatch_train_schedule.setHorizontalHeaderLabels(["", "Station Name", "Time\n(min since prev. station departure)", "Arrival Time"])

        dispatch_train_layout.addWidget(dispatch_train_schedule)

        # dispatch train button
        dispatch_train_button = QPushButton("Dispatch Train #%d" % 1)
        dispatch_train_layout.addWidget(dispatch_train_button)

        dispatch_train_widget = QWidget()
        dispatch_train_widget.setLayout(dispatch_train_layout)
        # dispatch_train_widget.

        self.setCentralWidget(dispatch_train_widget)

    # def validate_input_time(self, t):



       


ctc_ui_app = QApplication([])

window = CTC_MainWindow()
window.show()

ctc_ui_app.exec()