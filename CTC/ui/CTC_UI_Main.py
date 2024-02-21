from datetime import date, datetime, timedelta
from time import localtime, strftime, strptime, struct_time, time
from PyQt6.QtCore import QSize, Qt, QTime, QTimer
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QGridLayout, QComboBox, QHBoxLayout, QTimeEdit, QTableWidget, QTableWidgetItem, QTabWidget
from click import DateTime

from CTC.CTCSchedule import Train, CTCSchedule
from CTC.CTC import CTC
from CTC.CTCTime import get_current_time, get_current_time_hh_mm, get_current_time_hh_mm_str

from CTC.TrackDataCSVParser import LineTrackDataCSVParser

# from models import BlockModel

class CTC_MainWindow(QMainWindow):
    def __init__(self, ctc:CTC):
        super(CTC_MainWindow, self).__init__()

        self.ctc = ctc

        self.scheduled_trains = []

        self.setWindowTitle("CTC Office")

        dispatch_train_layout = QVBoxLayout()

        # Dispatch Train Label
        dispatch_label = QLabel("Dispatch Train")
        dispatch_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        dispatch_train_layout.addWidget(dispatch_label)

        
        self.dispatch_train_tab_widget = QTabWidget()
        self.disptach_train_tab_list = []


        self.arrival_time_list:list[QTimeEdit] = []
        self.departure_time_list:list[QTimeEdit] = []
        self.depart_now_button_list:list[QPushButton] = []
        self.dispatch_train_schedule_list:list[QTableWidget] = []
        self.dispatch_button_list:list[QPushButton] = []
        self.train_id_label_list:list[QLabel] = []

        self.destination_selector_list:list[QComboBox] = []
        for _ in self.ctc.get_lines():
            self.disptach_train_tab_list.append(QWidget())

        for (id, tab) in enumerate(self.disptach_train_tab_list):
            self.dispatch_train_tab_widget.addTab(self.disptach_train_tab_list[id], self.ctc.get_lines()[id] + " Line")

            tab.layout = QVBoxLayout()

            destination_list_combo_box = QComboBox()
            destination_list_combo_box.addItem("Select Destination...")
            for block in self.ctc.get_blocks_and_stations(id):
                block_list_name = ""
                if block[1] != "":
                    block_list_name = block[0] + "(STATION: %s)" % block[1]
                else:
                    block_list_name = block[0]
                destination_list_combo_box.addItem(block_list_name)

            destination_list_combo_box.setFixedSize(destination_list_combo_box.sizeHint())

            self.destination_selector_list.append(destination_list_combo_box)
            destination_list_combo_box.currentIndexChanged.connect(self.validate_destination_select)

            # Arrival Time

            dispatch_train_arrival_time_widget = DispatchArrivalTime()
            self.arrival_time_list.append(dispatch_train_arrival_time_widget.get_time_box_widget())
            
            # Departure Time

            dispatch_train_departure_time_widget = DispatchDepartureTime()
            # dispatch_train_departure_time_widget.get_time_box_widget().textChanged.connect(self.departure_time_updated)
            self.departure_time_list.append(dispatch_train_departure_time_widget.get_time_box_widget())
            self.departure_time_list[id].timeChanged.connect(self.departure_time_updated)


            dispatch_train_dispatch_information_grid = QGridLayout()
            dispatch_train_dispatch_information_grid.addWidget(destination_list_combo_box, 0, 0)
            dispatch_train_dispatch_information_grid.addWidget(dispatch_train_arrival_time_widget, 0, 1)
            dispatch_train_dispatch_information_grid.addWidget(dispatch_train_departure_time_widget, 1, 1)

            dispatch_train_information_grid_widget = QWidget()
            dispatch_train_information_grid_widget.setLayout(dispatch_train_dispatch_information_grid)

            # Train Number
            dispatch_train_train_number = QLabel()
            dispatch_train_train_number.setText(f"Train Number: %d" % self.ctc.schedule.get_next_train_number())
            dispatch_train_train_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
            f = dispatch_train_train_number.font()
            f.setPointSize(20)
            dispatch_train_train_number.setFont(f)
            dispatch_train_dispatch_information_grid.addWidget(dispatch_train_train_number, 1, 0)
            self.train_id_label_list.append(dispatch_train_train_number)

            dispatch_train_dispatch_information_grid_widget = QWidget()
            dispatch_train_dispatch_information_grid_widget.setLayout(dispatch_train_dispatch_information_grid)

            tab.layout.addWidget(dispatch_train_dispatch_information_grid_widget)


            # # List of stops
            dispatch_train_schedule = QTableWidget()
            dispatch_train_schedule.setColumnCount(4)
            dispatch_train_schedule.setHorizontalHeaderLabels(["", "Station Name", "Time\n(min since prev. station departure)", "Arrival Time"])
            self.dispatch_train_schedule_list.append(dispatch_train_schedule)
            # dispatch_train_schedule.setFixedWidth(dispatch_train_schedule.sizeHint().width())
            # dispatch_train_schedule_header = dispatch_train_schedule.horizontalHeader()
            
            tab.layout.addWidget(dispatch_train_schedule)  

            # Dispatch Button
            dispatch_train_button = QPushButton("Dispatch Train #%d" % self.ctc.schedule.get_next_train_number())
            dispatch_train_button.setEnabled(False)
            tab.layout.addWidget(dispatch_train_button)
            self.dispatch_button_list.append(dispatch_train_button)
            dispatch_train_button.clicked.connect(self.schedule_train)

            # add layout to widget
            tab.setLayout(tab.layout)

        dispatch_train_layout.addWidget(self.dispatch_train_tab_widget)

        

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
        
        self.scheduled_trains_table = QTableWidget()
        self.scheduled_trains_table.setColumnCount(6)
        self.scheduled_trains_table.setHorizontalHeaderLabels(["Train Number", "Line", "Destination", "Arrival Time", "First Stop", "Time to Departure (min)"])
        scheduled_trains_layout.addWidget(self.scheduled_trains_table)

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


        self.route = []

    def current_line_id(self):
        return self.dispatch_train_tab_widget.currentIndex()

    def departure_time_updated(self):
        print(self.departure_time_list[self.current_line_id()].time().toPyTime())

        if(len(self.route) > 1):
            self.calculate_route_arrival_times()

    def validate_destination_select(self, selected_id:int):
        print("validate dest", self.departure_time())
        if selected_id == 0:
            self.dispatch_button_list[self.current_line_id()].setEnabled(False)
            self.clear_schedule()
        else:
            self.dispatch_button_list[self.current_line_id()].setEnabled(True)
            self.list_stops_to_destination(selected_id)
            self.calculate_route_arrival_times()

    def departure_time(self)->QTime:
        departure_time = self.departure_time_list[self.dispatch_train_tab_widget.currentIndex()].time()
        return departure_time

    def clear_stops_list(self):
        dispatch_train_schedule = self.dispatch_train_schedule_list[self.dispatch_train_tab_widget.currentIndex()]
        dispatch_train_schedule.setRowCount(0)

    def reset_dispatch_panel(self):
        self.clear_stops_list()
        self.destination_selector_list[self.current_line_id()].setCurrentIndex(0)
        self.update_train_number()

    def train_number(self):
        return self.ctc.schedule.get_next_train_number()
    
    def update_train_number(self):
        for button, label in zip(self.dispatch_button_list, self.train_id_label_list):
            label.setText("Train Number: %d" % self.train_number())
            button.setText("Dispatch Train #%d" % self.train_number())


    def schedule_train(self):
        # route
        # line
        train = Train(self.ctc.schedule.get_next_train_number(), self.current_line_id(),
                      self.route[-1],
                      self.departure_time(),
                      self.route
                    )
        
        self.ctc.schedule.schedule_train(train)
        self.reset_dispatch_panel()
        self.update_schedule()


    def clear_schedule(self):
        self.scheduled_trains_table.setRowCount(0)

    def update_schedule(self):
        self.clear_schedule()
        for row, train in enumerate(self.ctc.schedule.get_schedule()):
            self.scheduled_trains_table.insertRow(row)
            print(train.number)
            number = QTableWidgetItem(str(train.number))
            line = QTableWidgetItem(self.ctc.get_lines()[train.line])

            block, station = self.ctc.get_block_and_station(train.line, train.destination)
            dest_name = ""
            if block != "":
                dest_name = block + "(STATION: %s)" % station
            else:
                dest_name = block

            dest = QTableWidgetItem(dest_name)
            # arr_time = QTableWidgetItem(train.)
            departure_time = QTableWidgetItem(train.departure_time.toString("HH:mm"))
            first_stop = QTableWidgetItem(train.route[0])
            time_to_departure = QTableWidgetItem(str(QTime.currentTime().msecsTo(train.departure_time) / 1000 * 60))

            self.scheduled_trains_table.setItem(row, 0, number)
            self.scheduled_trains_table.setItem(row, 1, line)
            self.scheduled_trains_table.setItem(row, 2, dest)
            #self.scheduled_trains_table.setItem(row, 3, QTableWidgetItem)
            self.scheduled_trains_table.setItem(row, 4, first_stop)
            self.scheduled_trains_table.setItem(row, 5, time_to_departure)
            




    def calculate_route_arrival_times(self):
        print("calculate times", self.departure_time())
        dispatch_train_schedule = self.dispatch_train_schedule_list[self.current_line_id()]

        travel_time_s = 0
        arrival_time = QTime(self.departure_time_list[self.current_line_id()].time())

        for stop_i in range(len(self.route)-1):
            block_a = self.route[stop_i]
            block_b = self.route[stop_i+1]
            # travel time to stop
            time_between_blocks_sec = self.ctc.get_travel_time_between_blocks_s(self.current_line_id(), block_a, block_b)
            dispatch_train_schedule.setItem(stop_i, 2, QTableWidgetItem(str(timedelta(seconds=time_between_blocks_sec))))

            travel_time_s = travel_time_s + time_between_blocks_sec

            arrival_time = self.departure_time().addSecs(int(travel_time_s))
            dispatch_train_schedule.setItem(stop_i, 3, QTableWidgetItem(arrival_time.toString("HH:mm")))

            # dwell time for stop
            travel_time_s += travel_time_s + 60
        
        self.arrival_time_list[self.current_line_id()].setTime(arrival_time)

    def list_stops_to_destination(self, selected_id)->None:
        line_id = self.dispatch_train_tab_widget.currentIndex()
        dispatch_train_schedule = self.dispatch_train_schedule_list[self.dispatch_train_tab_widget.currentIndex()]

        self.route = ["A1"]

        dispatch_train_schedule.setRowCount(0)
        if selected_id != 0:
            for station, block in zip(self.ctc.get_stations(line_id)[:(selected_id)], self.ctc.get_blocks(line_id)[:(selected_id)]):
                if station != "":
                    self.route.append(block)
                    row_number = dispatch_train_schedule.rowCount()
                    dispatch_train_schedule.insertRow(row_number)

                    station_name = QTableWidgetItem(station)
                    dispatch_train_schedule.setItem(row_number, 1, station_name)

            if self.ctc.get_stations(line_id)[selected_id - 1] == "":
                self.route.append(self.ctc.get_blocks(line_id)[selected_id - 1])
                row_number = dispatch_train_schedule.rowCount()
                dispatch_train_schedule.insertRow(row_number)
                station_name = QTableWidgetItem(self.ctc.get_blocks(line_id)[selected_id - 1])
                dispatch_train_schedule.setItem(row_number, 1, station_name)

            # self.calculate_route_arrival_times()

            # calculate times between each stop
            # for i in range(len(self.route) - 1):
            #     # get pair of blocks
            #     block_a = self.route[i]
            #     block_b = self.route[i+1]

            #     time_between_blocks_sec = self.ctc.get_travel_time_between_blocks_minutes(line_id, block_a, block_b)
                
            #     dispatch_train_schedule.setItem(i, 2, QTableWidgetItem(str(timedelta(seconds=time_between_blocks_sec))))

               
            #     time_through_route_sec += time_between_blocks_sec
            #     time_through_route_sec+=60




    def select_line_to_dispatch(self, line_button)->None:
        line = self.dispatch_train_tab_widget.currentIndex()

        print("Line: %d" % line)
        print("Current Line: %d" % self.current_line)

        if(line != self.current_line):
            self.current_line = line


    # def submit_scheduled_train(self):
    #     scheduled_train:Train(
    #         number=ctc_schedule.get_next_number(),
    #         destination=str(self.dispatch_train_destination_selector.currentText()),

    #     )

    def get_stops_to_destination(self, id):
        stops_to_dest = self.ctc.get_stations(self.current_line)[:id]
        return stops_to_dest

    # Timer Functions
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

class DispatchArrivalTime(QWidget):
    def __init__(self):
        super().__init__()

        self.dispatch_arrival_time_layout = QVBoxLayout()
        self.dispatch_train_arrival_time_label = QLabel("Arrival Time")
        f = self.dispatch_train_arrival_time_label.font()

        self.dispatch_train_arrival_time = QTimeEdit()
        self.dispatch_train_arrival_time.setDisplayFormat("HH:mm")
        self.dispatch_train_arrival_time.setDisabled(True)
        # self.dispatch_train_arrival_time.setInputMask("00:00")
        hhmm = get_current_time_hh_mm_str()
        # dispatch_train_arrival_time.textEdited.

        self.dispatch_arrival_time_layout.addWidget(self.dispatch_train_arrival_time_label)
        self.dispatch_arrival_time_layout.addWidget(self.dispatch_train_arrival_time)

        self.setLayout(self.dispatch_arrival_time_layout)
        self.setFixedSize(self.minimumSizeHint())

    def get_time_box_widget(self):
        return self.dispatch_train_arrival_time

class DispatchDepartureTime(QWidget):
    def __init__(self):
        super().__init__()
        self.dispatch_train_departure_time_layout = QVBoxLayout()
        self.dispatch_train_departure_time_button_hbox = QHBoxLayout()

        self.dispatch_train_departure_time_label = QLabel("Departure Time")

        self.dispatch_train_departure_time = QTimeEdit()
        self.dispatch_train_departure_time.setDisplayFormat("HH:mm")
        # self.dispatch_train_departure_time.setFixedSize(self.dispatch_train_departure_time.sizeHint())
        # self.dispatch_train_departure_time.timeChanged.connect(self.update_time)

        # Now Button
        self.depart_now_button = QPushButton()
        self.depart_now_button.setText("Now")
        self.depart_now_button.setFixedSize(self.depart_now_button.sizeHint())
        self.depart_now_button.clicked.connect(self.set_time_to_now)
        self.depart_now_button.click()

        self.dispatch_train_departure_time_button_hbox.addWidget(self.dispatch_train_departure_time)
        self.dispatch_train_departure_time_button_hbox.addWidget(self.depart_now_button)
        self.dispatch_train_departure_time_button_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)


        self.dispatch_train_departure_time_layout.addWidget(self.dispatch_train_departure_time_label)
        self.dispatch_train_departure_time_layout.addItem(self.dispatch_train_departure_time_button_hbox)
        self.dispatch_train_departure_time_layout.setSpacing(0)

        self.setLayout(self.dispatch_train_departure_time_layout)
        self.setFixedSize(self.minimumSizeHint())

    def set_time_to_now(self):
        self.departure_time = QTime.currentTime()
        self.dispatch_train_departure_time.setTime(self.departure_time)
        print(self.departure_time)

    def get_time_box_widget(self):
        return self.dispatch_train_departure_time
    
    def get_now_button(self):
        return self.depart_now_button


if __name__=="__main__":
    # define CTC Object
    # pass CTC Object to CTC_MainWindow()

    ctc_ui_app = QApplication([])

    track_layout_files = ["CTC/Green Line Track Data.csv", "CTC/Red Line Track Data.csv"]
    # track_layout_files = ["CTC/Blue Line Track Data.csv"]

    window = CTC_MainWindow(CTC(CTCSchedule(), [LineTrackDataCSVParser(track_layout).get_block_list() for track_layout in track_layout_files]))
    window.show()

    ctc_ui_app.exec()