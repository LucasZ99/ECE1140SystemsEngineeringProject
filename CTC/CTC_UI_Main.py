import PyQt6

from CTC.CTCConstants import *
from time import localtime, strftime, strptime, struct_time, time, ctime
from PyQt6.QtCore import QSize, Qt, QDateTime, QTime, QTimer, pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, \
    QGridLayout, QComboBox, QHBoxLayout, QTimeEdit, QTableWidget, QTableWidgetItem, QTabWidget, QAbstractScrollArea, \
    QHeaderView

from CTC import CTC
from CTC.Train import Train

import CTC.Route as Route
from SystemTime import SystemTime
from CTC.Track import *
from SystemTime.SystemTime import time_to_str


# from models import BlockModel

class CTCMainWindowViewModel:
    def __init__(self):
        self.current_line_selected_id = 0
        self.selected_destination_id = 0


class CTCMainWindow(QMainWindow):
    def __init__(self, ctc: CTC, system_time: SystemTime):
        super(CTCMainWindow, self).__init__()

        self.stops = []
        self.system_time = system_time

        self.ctc = ctc

        self.scheduled_trains: list[Train] = self.ctc.get_scheduled_trains()
        self.running_trains: list[Train] = self.ctc.get_running_trains()

        ########### SLOTS for CTC SIGNALS ###############
        self.system_time.update_time_signal.connect(self.update_time)
        self.ctc.update_ui_signal.connect(self.refresh_ctc_data)

        self.setWindowTitle("CTC Office")

        dispatch_train_layout = QVBoxLayout()

        # Dispatch Train Label
        dispatch_label = QLabel("Dispatch Train")
        dispatch_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        dispatch_train_layout.addWidget(dispatch_label)
        dispatch_train_layout.addSpacing(10)

        self.dispatch_train_tab_widget = QTabWidget()
        self.dispatch_train_tab_list = []

        self.arrival_time_list: list[QTimeEdit] = []
        self.departure_time_list: list[QTimeEdit] = []
        self.depart_now_button_list: list[QPushButton] = []
        self.dispatch_train_schedule_list: list[QTableWidget] = []
        self.dispatch_button_list: list[QPushButton] = []
        self.train_id_label_list: list[QLabel] = []

        self.destination_selector_list: list[QComboBox] = []
        for _ in LINES:
            self.dispatch_train_tab_list.append(QWidget())

        for (id, tab) in enumerate(self.dispatch_train_tab_list):
            self.dispatch_train_tab_widget.addTab(self.dispatch_train_tab_list[id], LINES[id])
            tab.layout = QVBoxLayout()

            destination_list_combo_box = QComboBox()
            destination_list_combo_box.addItem("Select Destination...")
            for block in BLOCK_NAMES[id]:
                block_list_name = ""
                if BLOCK_NAMES[id][block] in STATIONS[id]:
                    block_list_name = block + " (STATION: %s)" % STATIONS[id][BLOCK_NAMES[id][block]]
                else:
                    block_list_name = block
                destination_list_combo_box.addItem(block_list_name)

            destination_list_combo_box.setFixedSize(destination_list_combo_box.sizeHint())

            self.destination_selector_list.append(destination_list_combo_box)
            destination_list_combo_box.currentIndexChanged.connect(self.validate_destination_select)

            # Arrival Time

            dispatch_train_arrival_time_widget = DispatchArrivalTime(self.system_time)
            dispatch_train_arrival_time_widget.get_time_box_widget().timeChanged.connect(self.calculate_route_arrival_times)

            self.arrival_time_list.append(dispatch_train_arrival_time_widget.get_time_box_widget())

            # Departure Time

            dispatch_train_departure_time_widget = DispatchDepartureTime(self.system_time)
            dispatch_train_departure_time_widget.get_time_box_widget().timeChanged.connect(
                self.calculate_route_arrival_times)
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
            dispatch_train_train_number.setText(f"Train Number: %d" % self.ctc.scheduled_trains.get_next_train_number())
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
            dispatch_train_schedule.setColumnCount(3)
            dispatch_train_schedule.setHorizontalHeaderLabels(
                ["Station Name", "Time\n(min since prev. station departure)", "Arrival Time"])
            dispatch_train_schedule.horizontalHeader().setStretchLastSection(False)
            # dispatch_train_schedule.setSizeAdjustPolicy(
            #     QAbstractScrollArea.AdjustToContentsOnFirstShow
            # )
            self.dispatch_train_schedule_list.append(dispatch_train_schedule)
            # dispatch_train_schedule.setFixedWidth(dispatch_train_schedule.sizeHint().width())
            # dispatch_train_schedule_header = dispatch_train_schedule.horizontalHeader()

            tab.layout.addWidget(dispatch_train_schedule)

            # Dispatch Button
            dispatch_train_button = QPushButton(
                "Dispatch Train #%d" % self.ctc.scheduled_trains.get_next_train_number())
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
        self.train_system_time = QLabel(strftime("%H:%M:%S", localtime(system_time.time())))
        train_system_time_font = self.train_system_time.font()
        train_system_time_font.setPointSize(30)
        self.train_system_time.setFont(train_system_time_font)

        self.ctc_mode_select = QComboBox()
        self.ctc_mode_select.addItems(["Automatic Mode", "Manual Mode", "Maintenance Mode"])
        ctc_main_layout_right_top_section.addWidget(self.train_system_time)
        ctc_main_layout_right_top_section.addWidget(self.ctc_mode_select)
        self.ctc_mode_select.currentIndexChanged.connect(self.mode_switch_handler)
        self.ctc_mode_select.setFixedSize(self.ctc_mode_select.sizeHint())

        self.ctc_mode_select.setCurrentIndex(self.ctc.mode)

        if self.ctc.mode == MANUAL_MODE or self.ctc.mode == MAINTENANCE_MODE:
            self.ctc_mode_select.item(0).setEnabled(False)

        ctc_main_right_side.addItem(ctc_main_layout_right_top_section)

        # Currently Running Trains
        currently_running_trains_layout = QVBoxLayout()

        currently_running_trains_label = QLabel("Currently Running Trains")
        currently_running_trains_layout.addWidget(currently_running_trains_label)

        self.running_trains_table = QTableWidget()
        self.running_trains_table.verticalHeader().setHidden(True)

        self.running_trains_table.setColumnCount(8)
        self.running_trains_table.setHorizontalHeaderLabels(
            ["Train Number", "Line", "Destination", "Arrival Time", "Next Stop", "Time to Next Stop (min)",
             "Current Block", "Authority (ft)"])
        currently_running_trains_layout.addWidget(self.running_trains_table)
        ctc_main_right_side.addLayout(currently_running_trains_layout)

        # Scheduled Trains
        scheduled_trains_layout = QVBoxLayout()
        scheduled_trains_header_layout = QHBoxLayout()
        scheduled_trains_label = QLabel("Scheduled Trains")
        import_schedule_button = QPushButton("Import Schedule")
        import_schedule_button.setFixedSize(import_schedule_button.sizeHint())

        scheduled_trains_header_layout.addWidget(scheduled_trains_label)
        scheduled_trains_header_layout.addWidget(import_schedule_button)
        scheduled_trains_layout.addLayout(scheduled_trains_header_layout)

        self.scheduled_trains_table = QTableWidget()
        self.scheduled_trains_table.setColumnCount(6)
        self.scheduled_trains_table.setHorizontalHeaderLabels(
            ["Train Number", "Line", "Destination", "Arrival Time", "First Stop", "Time to Departure (min)"])
        scheduled_trains_layout.addWidget(self.scheduled_trains_table)
        self.scheduled_trains_table.verticalHeader().setHidden(True)

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

        block_table_line_select = QComboBox()
        block_table_line_select.addItems([line_name for line_name in LINES])

        block_table_header_layout = QHBoxLayout()
        block_table_header_layout.addWidget(block_table_label)
        block_table_header_layout.addWidget(block_table_line_select)
        block_table_header_layout.addWidget(block_table_search_bar)

        block_table_layout.addItem(block_table_header_layout)

        self.block_table = BlockTable(self.ctc)
        self.block_table.get_table_for_line(0)

        block_table_line_select.currentIndexChanged.connect(self.block_table.get_table_for_line)
        block_table_search_bar.textChanged.connect(self.block_table.search)

        block_table_layout.addWidget(self.block_table)

        ctc_main_right_side_bottom.addItem(block_table_layout)

        ctc_throughput_layout = QVBoxLayout()
        ctc_throughput_label = QLabel("System Throughput")
        ctc_throughput_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        ctc_throughput_layout.addWidget(ctc_throughput_label)

        ctc_main_layout_throughput = QGridLayout()
        ctc_main_layout_throughput.addWidget(QLabel("Trains Per Hour"), 0, 1)
        ctc_main_layout_throughput.addWidget(QLabel("# Ticket Sales Per Hour"), 0, 2)

        for id, line in enumerate(LINES):
            ctc_main_layout_throughput.addWidget(QLabel(line), id + 1, 0)

        ctc_throughput_layout.addItem(ctc_main_layout_throughput)
        ctc_main_right_side_bottom.addItem(ctc_throughput_layout)

        ctc_main_right_side.addItem(ctc_main_right_side_bottom)

        ctc_main_layout = QHBoxLayout()
        ctc_main_layout.addItem(dispatch_train_layout)

        ctc_main_layout.addItem(ctc_main_right_side)

        main_layout_widget = QWidget()
        main_layout_widget.setLayout(ctc_main_layout)

        self.setCentralWidget(main_layout_widget)

        self.route: list[int] = []

    @pyqtSlot()
    def refresh_ctc_data(self):
        self.update_schedule()
        self.update_running_trains_list()

        # self.block_table.update(GREEN_LINE)

    def current_line_id(self):
        return self.dispatch_train_tab_widget.currentIndex()

    def departure_time_updated(self):
        print(self.departure_time_list[self.current_line_id()].time().toPyTime())

        if len(self.route) > 1:
            self.calculate_route_arrival_times()

    def validate_destination_select(self, selected_id: int):
        destination_select_id = self.destination_selector_list[self.current_line_id()].currentIndex()

        print("validate dest", selected_id, self.departure_time(), "   ", destination_select_id)
        if selected_id < 1:
            self.dispatch_button_list[self.current_line_id()].setEnabled(False)
            self.clear_schedule()
        else:
            self.dispatch_button_list[self.current_line_id()].setEnabled(True)
            self.list_stops_to_destination(destination_select_id)
            self.calculate_route_arrival_times()

    # Convert QDateTime to seconds since epoch
    def departure_time(self) -> float:
        departure_time = self.departure_time_list[self.dispatch_train_tab_widget.currentIndex()].time()
        return self.convert_qtime_to_secs_since_epoch(departure_time)

    def convert_qtime_to_secs_since_epoch(self, qtime: QTime) -> float:

        # Get current day's qdatetie
        now = QDateTime()
        now.setSecsSinceEpoch(int(self.system_time.time()))

        # next day
        if qtime.hour() < now.time().hour():
            # subtract one day
            time_0 = QDateTime(now).addDays(1)
        elif qtime.hour() == now.time().hour() and qtime.minute() < now.time().minute():
            time_0 = QDateTime(now).addDays(1)
        else:
            time_0 = QDateTime(now)

        time_0.time().setHMS(qtime.hour(), qtime.minute(), 0, 0)
        return time_0.toSecsSinceEpoch()

    def clear_stops_list(self):
        dispatch_train_schedule = self.dispatch_train_schedule_list[self.dispatch_train_tab_widget.currentIndex()]
        dispatch_train_schedule.setRowCount(0)

    def reset_dispatch_panel(self):
        self.clear_stops_list()
        self.destination_selector_list[self.current_line_id()].setCurrentIndex(0)
        self.update_train_number()

    def train_number(self):
        return self.ctc.scheduled_trains.get_next_train_number()

    def update_train_number(self):
        for button, label in zip(self.dispatch_button_list, self.train_id_label_list):
            label.setText("Train Number: %d" % self.train_number())
            button.setText("Dispatch Train #%d" % self.train_number())

    def schedule_train(self):
        # route
        # line
        train = Train(self.system_time, self.train_number(), self.current_line_id(), self.scheduled_stops)
        print("Train Scheduled.")
        print("t = %s", strftime("%H:%m", localtime(self.system_time.time())))
        print(train)

        self.ctc.scheduled_trains.schedule_train(train)
        self.reset_dispatch_panel()
        self.update_schedule()

    def clear_schedule(self):
        self.scheduled_trains_table.setRowCount(0)

    def stop_name(self, line_id: int, block_id: int) -> str:
        block_id = abs(block_id)
        if block_id in STATIONS[line_id] != "":
            stop_name = str(block_id) + " (STATION: %s)" % STATIONS[line_id][block_id]
        else:
            stop_name = str(block_id)
        return stop_name

    def update_schedule(self):
        self.clear_schedule()
        for row, train in enumerate(self.ctc.scheduled_trains.get_schedule()):
            self.scheduled_trains_table.insertRow(row)
            print(train.id)
            number = QTableWidgetItem(str(train.id))
            line = QTableWidgetItem(LINES[train.line_id])

            dest_block = train.get_destination().block
            dest_name = self.stop_name(train.line_id, dest_block)

            dest = QTableWidgetItem(dest_name)
            # arr_time = QTableWidgetItem(train.)
            # eparture_time = QTableWidgetItem(train.departure_time.toString("HH:mm"))
            first_stop_name = self.stop_name(train.line_id, train.get_next_stop())
            first_stop = QTableWidgetItem(first_stop_name)

            min_to_departure = (train.departure_time() - self.system_time.time()) / 60

            time_to_departure = QTableWidgetItem(str(round(min_to_departure, 0)))

            self.scheduled_trains_table.setItem(row, 0, number)
            self.scheduled_trains_table.setItem(row, 1, line)
            self.scheduled_trains_table.setItem(row, 2, dest)
            # self.scheduled_trains_table.setItem(row, 3, QTableWidgetItem)
            self.scheduled_trains_table.setItem(row, 4, first_stop)
            self.scheduled_trains_table.setItem(row, 5, time_to_departure)

    def calculate_route_arrival_times(self):
        print("calculate times", self.departure_time())
        dispatch_train_schedule = self.dispatch_train_schedule_list[self.current_line_id()]

        print(self.route)

        # TODO set minumum based on departure time
        route_arrival_time = self.arrival_time_list[self.current_line_id()].time()

        # this is relative to midnight on the day of dispatch.
        route_departure_time = self.departure_time_list[self.current_line_id()].time()

        arrival_time = self.convert_qtime_to_secs_since_epoch(route_arrival_time)
        departure_time = self.convert_qtime_to_secs_since_epoch(route_departure_time)

        if len(self.route) > 0:
            self.stops = Route.get_times_through_route(self.current_line_id(), self.route)
            for stop in self.stops:
                print(stop.block, stop.arrival_time, stop.departure_time)

            # breakpoint()

            # arrival time is too short
            if not Route.is_route_schedulable(self.current_line_id(), self.stops, departure_time,
                                              departure_time + Route.get_route_travel_time(self.stops)):
                arrival_time = departure_time + Route.get_route_travel_time(self.stops)

            self.scheduled_stops = Route.schedule_route(self.current_line_id(), self.stops, departure_time,
                                                        departure_time + Route.get_route_travel_time(self.stops))

            for i, stop in enumerate(self.scheduled_stops):
                # table
                arrival_time = strftime("%H:%M", strptime(ctime(stop.arrival_time)))
                departure_time = strftime("%H:%M", strptime(ctime(stop.departure_time)))
                dispatch_train_schedule.setItem(i, 1, QTableWidgetItem(arrival_time))

                dispatch_train_schedule.setItem(i, 2, QTableWidgetItem(departure_time))

        # self.arrival_time_list[self.current_line_id()].setTime(arrival_time)

    def list_stops_to_destination(self, selected_id) -> None:
        line_id = self.dispatch_train_tab_widget.currentIndex()
        dispatch_train_schedule = self.dispatch_train_schedule_list[self.dispatch_train_tab_widget.currentIndex()]
        dispatch_train_schedule.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        dispatch_train_schedule.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        # handles the double tracked sections
        if selected_id >= 1:
            self.route = Route.find_route(line_id, GREEN_LINE_YARD_SPAWN, BLOCKS[GREEN_LINE][selected_id - 1])

        dispatch_train_schedule.setRowCount(0)
        if selected_id != 0:
            for stop in self.route[:-1]:



                stop_name = self.stop_name(line_id, stop)
                row_number = dispatch_train_schedule.rowCount()
                dispatch_train_schedule.insertRow(row_number)

                selected_stop_table_item = QTableWidgetItem(stop_name)
                selected_stop_table_item.setText(stop_name)
                selected_stop_table_item.setFlags(PyQt6.QtCore.Qt.ItemFlag.ItemIsUserCheckable | PyQt6.QtCore.Qt.ItemFlag.ItemIsEnabled)
                selected_stop_table_item.setCheckState(PyQt6.QtCore.Qt.CheckState.Checked)

                station_name = QTableWidgetItem(stop_name)
                dispatch_train_schedule.setItem(row_number, 0, selected_stop_table_item)

        row_number = dispatch_train_schedule.rowCount()
        dispatch_train_schedule.insertRow(row_number)
        print(self.route)
        last_stop = self.route[-1]
        print("---------LAST STOP--------")

        last_stop_name = self.stop_name(line_id, last_stop)
        print(last_stop_name)
        last_stop_widget_item = QTableWidgetItem(last_stop_name)
        dispatch_train_schedule.setItem(row_number, 0, last_stop_widget_item)

    def select_line_to_dispatch(self, line_button) -> None:
        line = self.dispatch_train_tab_widget.currentIndex()

        print("Line: %d" % line)
        print("Current Line: %d" % self.current_line)

        if (line != self.current_line):
            self.current_line = line

    def get_stops_to_destination(self, id):
        stops_to_dest = Route.find_route(self.current_line, GREEN_LINE_YARD_SPAWN, id)
        return stops_to_dest

    def mode_switch_handler(self, mode):
        modes = ["Automatic Mode", "Manual Mode", "Maintenance Mode"]
        self.ctc.mode = mode
        # disable automatic mode on switch from auto mode.
        if mode == MANUAL_MODE or mode == MAINTENANCE_MODE:
            self.ctc_mode_select.model().item(0).setEnabled(False)

        print("CTC Switched to %s." % modes[mode])

    def update_running_trains_list(self):
        table = self.running_trains_table

        # Clear table
        table.setRowCount(0)

        for row, train in enumerate(self.ctc.running_trains):
            table.insertRow(row)
            train_number = str(train.id)
            # TODO train_line = sorted(LINES[train.line_id].items())
            destination = self.stop_name(train.line_id, Route.get_block(train.line_id, train.get_destination().block))

            table.setItem(row, 0, QTableWidgetItem(train_number))
            table.setItem(row, 1, QTableWidgetItem(train_line[0]))
            table.setItem(row, 2, QTableWidgetItem(destination))
            table.setItem(row, 3, QTableWidgetItem(time_to_str(train.get_destination().arrival_time)))
            table.setItem(row, 4, QTableWidgetItem(self.stop_name(train.line_id, train.route[train.next_stop].block)))
            table.setItem(row, 6, QTableWidgetItem(str(train.current_block)))
            table.setItem(row, 7, QTableWidgetItem(str(train.blocks_to_next_stop())))

    @pyqtSlot()
    def update_time(self):
        current_time = strftime("%H:%M:%S", localtime(self.system_time.time()))
        # [label.setTime(get_current_time_qtime()) for label in self.departure_time_list]
        self.train_system_time.setText(current_time)

    def format_time_hhmm(self, time: struct_time) -> str:
        h = str(time.tm_hour)
        m = str(time.tm_min)

        if (len(h) == 1):
            hh = "0" + h
        else:
            hh = h

        if (len(m) == 1):
            mm = "0" + m
        else:
            mm = m

        return hh + ":" + mm


class BlockTable(QTableWidget):
    def __init__(self, ctc: CTC):
        super().__init__()

        self.ctc = ctc

        self.setColumnCount(10)
        self.verticalHeader().setVisible(False)

        self.setHorizontalHeaderLabels(
            ["Block ID", "Occupied", "Block Open", "Signal Status", "Switch Destination",
             "Railroad Crossing Activated", "Length (ft)", "Speed Limit (mph)", "Suggested Speed", "Authority"])

    def update(self, line_id: int):
        self.setRowCount(0)

        # TODO fix block data
        for row, block in enumerate(TRACK[line_id]):
            self.insertRow(block)
            block_id = block
            block_length_ft = float(LENGTHS_SPEED_LIMITS[line_id][block][LENGTH]) * 3.28084
            block_speed_limit_mph = LENGTHS_SPEED_LIMITS[line_id][block][SPEED_LIMIT] / 1.609

            occupied = "Yes" if self.ctc.blocks[block] is True else "No"

            self.setItem(row, 0, QTableWidgetItem(block_id))
            self.setItem(row, 1, QTableWidgetItem(occupied))
            self.setItem(row, 6, QTableWidgetItem(str(block_length_ft)))
            self.setItem(row, 7, QTableWidgetItem(str(block_speed_limit_mph)))
            self.setItem(row, 8, QTableWidgetItem(str(self.ctc.suggested_speeds[block])))
            self.setItem(row, 9, QTableWidgetItem(str(self.ctc.authorities[block])))

    def get_table_for_line(self, line_id: int):
        # clear rows
        self.setRowCount(0)

        # TODO fix block data
        for block in TRACK[line_id]:
            row = self.rowCount()
            self.insertRow(row)
            block_id = block
            block_length_ft = float(LENGTHS_SPEED_LIMITS[line_id][block][LENGTH]) * 3.28084
            block_speed_limit_mph = LENGTHS_SPEED_LIMITS[line_id][block][SPEED_LIMIT] / 1.609

            occupied = "Yes" if self.ctc.blocks[block] is True else "No"

            block_id_widget = QTableWidgetItem(str(block_id))
            occupied_widget = QTableWidgetItem(occupied)
            block_length_widget = QTableWidgetItem(str(block_length_ft))
            speed_widget = QTableWidgetItem(str(block_speed_limit_mph))
            suggested_speed_widget = QTableWidgetItem(str(self.ctc.suggested_speeds[block]))
            authority_widget = QTableWidgetItem(str(self.ctc.authorities[block]))

            self.setItem(row, 0, block_id_widget)
            self.setItem(row, 1, occupied_widget)
            self.setItem(row, 6, block_length_widget)
            self.setItem(row, 7, speed_widget)
            self.setItem(row, 8, suggested_speed_widget)
            self.setItem(row, 9, authority_widget)

            # set switch combobox if there is a switch
            # if block.switch_dest.__len__() > 0:
            #     switch_combo_box = QComboBox()
            #     switch_combo_box.addItems(block.switch_dest)
            #     self.setCellWidget(id, 4, switch_combo_box)

    def search(self, search_term: str):
        self.setCurrentItem(None)

        if not search_term:
            return

        search_results = self.findItems(search_term, Qt.MatchFlag.MatchContains)
        if search_results:
            for search_result in search_results:
                search_result.setSelected(True)


class DispatchArrivalTime(QWidget):
    def __init__(self, system_time: SystemTime):
        super().__init__()

        self.system_time = system_time

        self.dispatch_arrival_time_layout = QVBoxLayout()
        self.dispatch_train_arrival_time_label = QLabel("Arrival Time")
        f = self.dispatch_train_arrival_time_label.font()

        self.dispatch_train_arrival_time = QTimeEdit()
        self.dispatch_train_arrival_time.setDisplayFormat("HH:mm")

        dt = QDateTime()
        dt.setSecsSinceEpoch(int(self.system_time.time()))

        self.dispatch_train_arrival_time.setTime(dt.time())

        self.dispatch_arrival_time_layout.addWidget(self.dispatch_train_arrival_time_label)
        self.dispatch_arrival_time_layout.addWidget(self.dispatch_train_arrival_time)

        self.setLayout(self.dispatch_arrival_time_layout)
        self.setFixedSize(self.minimumSizeHint())

    def get_time_box_widget(self):
        return self.dispatch_train_arrival_time


class DispatchDepartureTime(QWidget):
    def __init__(self, system_time: SystemTime):
        super().__init__()
        self.system_time = system_time

        self.dispatch_train_departure_time_layout = QVBoxLayout()
        self.dispatch_train_departure_time_button_hbox = QHBoxLayout()

        self.dispatch_train_departure_time_label = QLabel("Departure Time")

        self.dispatch_train_departure_time = QTimeEdit()

        # dt = QDateTime()
        # dt.setSecsSinceEpoch(int(system_time.time()))
        # self.dispatch_train_departure_time.setMinimumDateTime(dt)

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
        self.departure_time = self.system_time.time()
        dt = QDateTime()
        dt.setSecsSinceEpoch(int(self.departure_time))

        self.dispatch_train_departure_time.setTime(dt.time())
        print(self.departure_time)

    def get_time_box_widget(self):
        return self.dispatch_train_departure_time

    def get_now_button(self):
        return self.depart_now_button


if __name__ == "__main__":
    # define CTC Object
    # pass CTC Object to CTC_MainWindow()

    ctc_ui_app = QApplication([])

    # track_layout_files = ["CTC/Green Line Track Data.csv", "CTC/Red Line Track Data.csv"]
    # track_layout_files = ["CTC/Blue Line Track Data.csv"]

    system_time = SystemTime()

    window = CTCMainWindow(CTC(system_time), system_time)
    window.show()

    ctc_ui_app.exec()
