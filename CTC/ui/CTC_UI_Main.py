from time import localtime, struct_time
from PyQt6.QtCore import QSize, Qt, QTime, QTimer
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QGridLayout, QComboBox, QHBoxLayout, QButtonGroup, QTableWidget

# from models import BlockModel

class CTC_MainWindow(QMainWindow):
    def __init__(self):
        super(CTC_MainWindow, self).__init__()

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

        self.line_select_buttons = QButtonGroup()
        self.line_select_buttons.setExclusive(True)

        # TODO add exclusivity button handler for dispatch line select OR change this to PyQt tabs
        for line in train_lines:
            line_select_button = QPushButton()
            dispatch_line_select_buttons_layout.addWidget(line_select_button)
            line_select_button.setText(line)
            line_select_button.setCheckable(True)
            self.line_select_buttons.addButton(line_select_button)


        dispatch_train_layout.addItem(dispatch_line_select_buttons_layout)

        # Destination Select, Arrival/Departure Time Set, Train Number
        dispatch_train_dispatch_information_grid = QGridLayout()

        # Destination Select
        dispatch_train_destination_selector = QComboBox()
        dispatch_train_destination_selector.addItems(["Select Destination...", "Dormont", "South Hills"])
        dispatch_train_dispatch_information_grid.addWidget(dispatch_train_destination_selector, 0,0)

        dispatch_train_train_number = QLabel()
        dispatch_train_train_number.setText(f"Train Number: %d" % 1)
        dispatch_train_train_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f = dispatch_train_train_number.font()
        f.setPointSize(20)
        dispatch_train_train_number.setFont(f)
        dispatch_train_dispatch_information_grid.addWidget(dispatch_train_train_number, 1, 0)

        # Arrival Time
        dispatch_arrival_time_layout = QVBoxLayout()

        dispatch_train_arrival_time_label = QLabel("Arrival Time")
        f = dispatch_train_arrival_time_label.font()


        dispatch_train_arrival_time = QLineEdit()
        dispatch_train_arrival_time.setInputMask("00:00")
        dispatch_train_arrival_time.setText("15:10")
        dispatch_train_arrival_time.setFixedSize(dispatch_train_arrival_time.sizeHint())
        # dispatch_train_arrival_time.textEdited.

        dispatch_arrival_time_layout.addWidget(dispatch_train_arrival_time_label)
        dispatch_arrival_time_layout.addWidget(dispatch_train_arrival_time)

        dispatch_train_arrival_time_widget = QWidget()
        dispatch_train_arrival_time_widget.setLayout(dispatch_arrival_time_layout)


        dispatch_train_departure_time_layout = QVBoxLayout()
        dispatch_train_departure_time_button_hbox = QHBoxLayout()

        dispatch_train_departure_time_label = QLabel("Departure Time")

        self.dispatch_train_departure_time = QLineEdit()
        self.dispatch_train_departure_time.setInputMask("00:00")
        self.dispatch_train_departure_time.setText("12:47")
        self.dispatch_train_departure_time.setFixedSize(self.dispatch_train_departure_time.sizeHint())

        # Now Button
        depart_now_button = QPushButton()
        depart_now_button.setText("Now")
        depart_now_button.setFixedSize(depart_now_button.sizeHint())
        depart_now_button.clicked.connect(self.set_time_to_now)

        dispatch_train_departure_time_button_hbox.addWidget(self.dispatch_train_departure_time)
        dispatch_train_departure_time_button_hbox.addWidget(depart_now_button)
        dispatch_train_departure_time_button_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)


        dispatch_train_departure_time_layout.addWidget(dispatch_train_departure_time_label)
        dispatch_train_departure_time_layout.addItem(dispatch_train_departure_time_button_hbox)
        dispatch_train_departure_time_layout.setSpacing(0)

        dispatch_train_departure_time_widget = QWidget()
        dispatch_train_departure_time_widget.setLayout(dispatch_train_departure_time_layout)

        dispatch_train_dispatch_information_grid.addWidget(dispatch_train_arrival_time_widget, 0, 1)
        dispatch_train_dispatch_information_grid.addWidget(dispatch_train_departure_time_widget, 1, 1)
        # dispatch_train_dispatch_information_grid.addWidget(depart_now_button, 1, 2)

        dispatch_train_information_grid_widget = QWidget()
        dispatch_train_information_grid_widget.setLayout(dispatch_train_dispatch_information_grid)

        dispatch_train_layout.addWidget(dispatch_train_information_grid_widget)


        # List of stops
        dispatch_train_schedule = QTableWidget()
        dispatch_train_schedule.setColumnCount(4)
        dispatch_train_schedule.setHorizontalHeaderLabels(["", "Station Name", "Time\n(min since prev. station departure)", "Arrival Time"])
        # dispatch_train_schedule_header = dispatch_train_schedule.horizontalHeader()
        

        dispatch_train_layout.addWidget(dispatch_train_schedule)

        # dispatch train button
        dispatch_train_button = QPushButton("Dispatch Train #%d" % 1)
        dispatch_train_layout.addWidget(dispatch_train_button)
        # dispatch_train_widget = QWidget()
        # dispatch_train_widget.setLayout(dispatch_train_layout)
        # dispatch_train_widget.setFixedSize(dispatch_train_widget.baseSize())
        

        # Time
        # Time in center of window
        ctc_main_right_side = QVBoxLayout()
        ctc_main_right_side.setSpacing(10)
        ctc_main_layout_right_top_section = QHBoxLayout()
        self.train_system_time = QLabel(self.format_time_hhmm(localtime()))
        train_system_time_font = self.train_system_time.font()
        train_system_time_font.setPointSize(30)
        self.train_system_time.setFont(train_system_time_font)

        # Update time every 1 second
        time_timer = QTimer(self)
        time_timer.timeout.connect(self.timer_handler_1sec)
        time_timer.start(1000)

        ctc_mode_select = QComboBox()
        ctc_mode_select.addItems(["Automatic Mode", "Manual Mode", "Maintenance Mode"])
        ctc_main_layout_right_top_section.addWidget(self.train_system_time)
        ctc_main_layout_right_top_section.addWidget(ctc_mode_select)


        ctc_main_right_side.addItem(ctc_main_layout_right_top_section)

        # Currently Running Trains
        currently_running_trains_layout = QVBoxLayout()


        currently_running_trains_label = QLabel("Currently Running Trains")
        currently_running_trains_layout.addWidget(currently_running_trains_label)

        ctc_main_layout_currently_running_trains = QTableWidget()
        ctc_main_layout_currently_running_trains.setColumnCount(8)
        ctc_main_layout_currently_running_trains.setHorizontalHeaderLabels(["Train Number", "Line", "Destination", "Arrival Time", "Next Stop", "Time to Next Stop (min)", "Current Block", "Authority (ft)"])
        currently_running_trains_layout.addWidget(ctc_main_layout_currently_running_trains)
        ctc_main_right_side.addLayout(currently_running_trains_layout)

        # Scheduled Trains
        scheduled_trains_layout = QVBoxLayout()
        scheduled_trains_header_layout = QHBoxLayout()
        scheduled_trains_label = QLabel("Scheduled Trains")
        #scheduled_trains_header_layout.setSpacing(10)
        import_schedule_button = QPushButton("Import Schedule")
        import_schedule_button.setFixedSize(import_schedule_button.sizeHint())
        

        scheduled_trains_header_layout.addWidget(scheduled_trains_label)
        scheduled_trains_header_layout.addWidget(import_schedule_button)
        scheduled_trains_layout.addLayout(scheduled_trains_header_layout)
        
        ctc_main_layout_scheduled_trains = QTableWidget()
        ctc_main_layout_scheduled_trains.setColumnCount(6)
        ctc_main_layout_scheduled_trains.setHorizontalHeaderLabels(["Train Number", "Line", "Destination", "Arrival Time", "First Stop", "Time to Departure (min)"])
        scheduled_trains_layout.addWidget(ctc_main_layout_scheduled_trains)

        ctc_main_right_side.addLayout(scheduled_trains_layout)


        ctc_main_right_side_bottom = QHBoxLayout()
        ctc_main_right_side_bottom.setSpacing(10)


        # Block table
        # Search bar: https://www.pythonguis.com/faq/how-to-create-a-filter-search-bar-for-a-qtablewidget/
        block_table_layout = QVBoxLayout()
        block_table_label = QLabel("Block Table")
        block_table_search_bar = QLineEdit()
        block_table_search_bar.setPlaceholderText("Search for Block")
        block_table_search_bar.setFixedSize(block_table_search_bar.sizeHint())

        block_table_header_layout = QHBoxLayout()
        block_table_header_layout.addWidget(block_table_label)
        block_table_header_layout.addWidget(block_table_search_bar)
        
        block_table_layout.addItem(block_table_header_layout)

        ctc_main_layout_block_table = QTableWidget()
        ctc_main_layout_block_table.setColumnCount(7)
        ctc_main_layout_block_table.setHorizontalHeaderLabels(["Block ID", "Train in Block\n(train number)","Block Open","Signal Status","Switch Destination","Railroad Crossing Activated","Speed Limit"])
        
        block_table_layout.addWidget(ctc_main_layout_block_table)

        ctc_main_right_side_bottom.addItem(block_table_layout)

        ctc_throughput_layout = QVBoxLayout()
        ctc_throughput_label = QLabel("System Throughput")
        ctc_throughput_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        ctc_throughput_layout.addWidget(ctc_throughput_label)

        ctc_main_layout_throughput = QTableWidget()
        ctc_main_layout_throughput.setRowCount(2)
        ctc_main_layout_throughput.setVerticalHeaderLabels(["Red Line", "Green Line"])

        ctc_main_layout_throughput.setColumnCount(2)
        ctc_main_layout_throughput.setHorizontalHeaderLabels(["Trains Per Hour", "# Ticket Sales Per Hour"])
        
        ctc_throughput_layout.addWidget(ctc_main_layout_throughput)
        ctc_main_right_side_bottom.addItem(ctc_throughput_layout)
    
        ctc_main_right_side.addItem(ctc_main_right_side_bottom)

        ctc_main_layout = QHBoxLayout()
        ctc_main_layout.addItem(dispatch_train_layout)

        ctc_main_layout.addItem(ctc_main_right_side)

        main_layout_widget = QWidget()
        main_layout_widget.setLayout(ctc_main_layout)

        self.setCentralWidget(main_layout_widget)

    def set_time_to_now(self):
        current_time = localtime()
        self.dispatch_train_departure_time.setText(self.format_time_hhmm(current_time))

    def timer_handler_1sec(self):
        self.update_time()

    def update_time(self):
        current_time = localtime()

        self.train_system_time.setText(self.format_time_hhmm(current_time))

    def format_time_hhmm(self, time:struct_time)->str:
        h = str(time.tm_hour)
        m = str(time.tm_min)

        if(len(h) == 1):
            hh = "0" + h
        else:
            hh = h
        
        if(len(m) == 1):
            mm = "0" + m
        else:
            mm = m

        return hh + ":" + mm

    # def validate_input_time(self, t):

if __name__=="__main__":
    # define CTC Object
    # pass CTC Object to CTC_MainWindow()

    ctc_ui_app = QApplication([])

    window = CTC_MainWindow()
    window.show()

    ctc_ui_app.exec()