import PyQt6

from CTC.CTCConstants import *
from time import localtime, strftime, strptime, struct_time, time, ctime
from PyQt6.QtCore import QSize, Qt, QDateTime, QTime, QTimer, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, \
    QGridLayout, QComboBox, QHBoxLayout, QTimeEdit, QTableWidget, QTableWidgetItem, QTabWidget, QAbstractScrollArea, \
    QHeaderView

from CTC import CTC
from CTC.Train import Train

import CTC.Route as Route
from CTC.Route import Stop
import SystemTime
from Common import Light, Switch
from Common.GreenLine import *
from Common.Constants import *
from Common.Lines import *
from SystemTime.SystemTime import time_to_str


# from models import BlockModel

class CTCMainWindowViewModel:
    def __init__(self):
        self.current_line_selected_id = 0
        self.selected_destination_id = 0


"""
Returns the block id for the block at position route_block_index in the route
where route_block_index = 0 is the yard spawn, and route_block_index len(route) - 1 is the yard delete
"""


def get_block_id(line_id: int, route_block_index: int) -> int:
    return abs(GREEN_LINE[ROUTE][route_block_index])



def calculate_times_through_route(line_id: int, departure_time: float, arrival_time: float, route: list[int]) -> list[
    Stop]:
    route_stops = Route.get_route_stops(line_id, route)
    minimum_travel_time = Route.get_route_travel_time(route_stops)

    # TODO handle next day issue
    suggested_travel_time = arrival_time - departure_time

    # force schedulable route
    if minimum_travel_time > suggested_travel_time:
        print("CTCUI: proposed time too short. ")
        arrival_time = departure_time + minimum_travel_time

    scheduled_route = Route.schedule_route(line_id, route_stops, departure_time, arrival_time)
    return scheduled_route


def convert_qtime_to_secs_since_epoch(qtime: QTime) -> float:
    # Get current day's qdatetie
    now = QDateTime()
    now.setSecsSinceEpoch(int(SystemTime.time()))

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


class CTCMainWindow(QMainWindow):
    def __init__(self, ctc: CTC):
        super(CTCMainWindow, self).__init__()

        self.stops = []

        self.ctc = ctc

        self.scheduled_trains: list[Train] = self.ctc.get_scheduled_trains()
        self.running_trains: list[Train] = self.ctc.get_running_trains()



        self.setWindowTitle("CTC Office")

        # Dispatch Train Tab
        self.dispatch_train_layout = DispatchTrainLayout(LINES, self.ctc.scheduled_trains.get_next_train_number())

        # Connect Signals from dispatch train layout

        # TODO get rid of validate destination select. When Select Destination... is selected from the list the signal is not emitted.
        self.dispatch_train_layout.dispatch_button_pressed.connect(self.schedule_train)


        # Time in center of window
        ctc_main_right_side = QVBoxLayout()
        ctc_main_right_side.setSpacing(10)
        ctc_main_layout_right_top_section = QHBoxLayout()
        self.train_system_time = QLabel(strftime("%H:%M:%S", localtime(SystemTime.time())))
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
            self.ctc_mode_select.model().item(0).setEnabled(False)

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
             "Current Block", "Authority (blocks)"])
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
        self.block_table.fill_table_for_line(0)

        block_table_line_select.currentIndexChanged.connect(self.block_table.fill_table_for_line)
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
        ctc_main_layout.addLayout(self.dispatch_train_layout)

        ctc_main_layout.addItem(ctc_main_right_side)

        main_layout_widget = QWidget()
        main_layout_widget.setLayout(ctc_main_layout)

        self.setCentralWidget(main_layout_widget)

        self.route: list[int] = []

        ########### SLOTS for CTC SIGNALS ###############
        self.ctc.update_ui_running_trains_table_signal.connect(self.refresh_ctc_schedule_data)
        self.ctc.update_ui_block_table.connect(self.block_table.update_table)

        self.time_update_timer = QTimer()
        self.time_update_timer.timeout.connect(self.update_time)

        # 100 msec
        self.time_update_timer.start(100)

    @pyqtSlot()
    def refresh_ctc_schedule_data(self):
        self.update_schedule()
        self.update_running_trains_list()

        # self.block_table.update(GREEN_LINE)

    def get_selected_line(self):
        return self.dispatch_train_layout.line_tab_widget.currentIndex()

    def train_number(self):
        return self.ctc.scheduled_trains.get_next_train_number()

    def schedule_train(self, route: list[Stop]):
        # route
        # line
        train = Train(self.train_number(), self.get_selected_line(), route)
        print(f"CTCUI: Train {self.train_number()} Scheduled.")
        print("\tt = %s", strftime("%H:%m", localtime(SystemTime.time())))
        print(f"\t{train}\n")

        self.ctc.scheduled_trains.schedule_train(train)
        self.dispatch_train_layout.update_train_number(self.train_number())
        self.update_schedule()

    def clear_schedule(self):
        self.scheduled_trains_table.setRowCount(0)

    def update_schedule(self):
        self.clear_schedule()
        for row, train in enumerate(self.ctc.scheduled_trains.get_schedule()):
            self.scheduled_trains_table.insertRow(row)
            number = QTableWidgetItem(str(train.id))
            line = QTableWidgetItem(LINES[train.line_id])

            dest_block = train.get_destination().block
            dest_name = stop_name(train.line_id, dest_block)

            dest = QTableWidgetItem(dest_name)
            first_stop_name = stop_name(train.line_id, train.get_next_stop())
            first_stop = QTableWidgetItem(first_stop_name)

            min_to_departure = (train.departure_time() - SystemTime.time()) / 60

            time_to_departure = QTableWidgetItem(str(round(min_to_departure, 0)))

            self.scheduled_trains_table.setItem(row, 0, number)
            self.scheduled_trains_table.setItem(row, 1, line)
            self.scheduled_trains_table.setItem(row, 2, dest)
            # self.scheduled_trains_table.setItem(row, 3, QTableWidgetItem)
            self.scheduled_trains_table.setItem(row, 4, first_stop)
            self.scheduled_trains_table.setItem(row, 5, time_to_departure)

    # def get_stops_to_destination(self, id):
    #     stops_to_dest = Route.find_route(self.get_selected_line(), GREEN_LINE_YARD_SPAWN, id)
    #     return stops_to_dest

    def mode_switch_handler(self, mode):
        modes = ["Automatic Mode", "Manual Mode", "Maintenance Mode"]
        self.ctc.mode = mode
        # disable automatic mode on switch from auto mode.
        if mode == MANUAL_MODE or mode == MAINTENANCE_MODE:
            self.ctc_mode_select.model().item(0).setEnabled(False)

        print("CTC: Switched to %s." % modes[mode])

    def update_running_trains_list(self):
        table = self.running_trains_table

        # Clear table
        table.setRowCount(0)

        for row, train in enumerate(self.ctc.get_running_trains()):
            table.insertRow(row)
            train_number = str(train.id)
            # TODO train_line = sorted(LINES[train.line_id].items())
            destination = stop_name(train.line_id, Route.get_block(train.get_destination().block))

            table.setItem(row, 0, QTableWidgetItem(train_number))
            table.setItem(row, 1, QTableWidgetItem(LINES[train.line_id]))
            table.setItem(row, 2, QTableWidgetItem(destination))
            table.setItem(row, 3, QTableWidgetItem(time_to_str(train.get_destination().arrival_time)))
            table.setItem(row, 4, QTableWidgetItem(stop_name(train.line_id, train.route[train.next_stop].block)))
            table.setItem(row, 6, QTableWidgetItem(str(train.current_block)))
            table.setItem(row, 7, QTableWidgetItem(str(train.blocks_to_next_stop())))

    def update_time(self):
        current_time = strftime("%H:%M:%S", localtime(SystemTime.time()))
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

class DispatchTrainLayout(QVBoxLayout):
    line_changed = pyqtSignal(int)
    dispatch_button_pressed = pyqtSignal(list)
    selected_stop_changed = pyqtSignal(int)

    def __init__(self, lines: list[str], next_train_id: int):
        super().__init__()

        # truth values of each stop in whole_route. True is stop, False is no stop.
        self.stops = []

        # current list of stops that train will make
        self.route = []

        # every stop from origin to destination including dest
        self.whole_route = None

        self.line_id = 0

        self.tab_layout = QVBoxLayout()

        self.label = QLabel("Dispatch Train")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.addWidget(self.label)
        self.addSpacing(10)

        # Tab Widget for each line
        self.line_tab_widget = QTabWidget()
        self.line_tab_list = []

        self.destination_selector_list = QComboBox()
        self.destination_selector_list.addItem("Select Destination...")
        self.destination_selector_list.setFixedSize(self.destination_selector_list.sizeHint())

        self.train_origin = GREEN_LINE_YARD_SPAWN
        self.train_destination = 0

        # arrival time
        self.arrival_time = DispatchArrivalTime()

        # departure time
        self.departure_time = DispatchDepartureTime()

        # stops to destination
        self.dispatch_train_information_grid = QGridLayout()
        self.dispatch_train_information_grid.addWidget(self.destination_selector_list, 0, 0)
        self.dispatch_train_information_grid.addWidget(self.arrival_time, 0, 1)
        self.dispatch_train_information_grid.addWidget(self.departure_time, 1, 1)

        self.next_train_id = next_train_id

        # train number
        self.dispatch_train_number_label = QLabel()
        self.dispatch_train_number_label.setText(f"Train Number: %d" % self.next_train_id)
        self.dispatch_train_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f = self.dispatch_train_number_label.font()
        f.setPointSize(20)
        self.dispatch_train_number_label.setFont(f)
        self.dispatch_train_information_grid.addWidget(self.dispatch_train_number_label, 1, 0)

        self.dispatch_train_information_grid_widget = QWidget()
        self.dispatch_train_information_grid_widget.setLayout(self.dispatch_train_information_grid)

        self.tab_layout.addWidget(self.dispatch_train_information_grid_widget)

        # stop list
        self.dispatch_train_schedule = QTableWidget()
        self.dispatch_train_schedule.setColumnCount(3)
        self.dispatch_train_schedule.setHorizontalHeaderLabels(
            ["Station Name", "Time\n(min since prev. station departure)", "Arrival Time"])
        self.dispatch_train_schedule.horizontalHeader().setStretchLastSection(False)

        self.tab_layout.addWidget(self.dispatch_train_schedule)

        # Dispatch Button
        self.dispatch_train_button = QPushButton(
            "Dispatch Train #%d" % self.next_train_id)
        self.disable_dispatch_button()

        self.tab_layout.addWidget(self.dispatch_train_button)

        for tab_id, line in enumerate(lines):
            tab_widget = QWidget()
            tab_widget.setLayout(self.tab_layout)
            self.line_tab_widget.addTab(tab_widget, line)
            self.line_tab_list.append(tab_widget)

        self.line_tab_widget.currentChanged.connect(self.load_destinations_to_selector_list)
        self.dispatch_train_button.clicked.connect(self.dispatch_button_handler)
        self.addWidget(self.line_tab_widget)

        # route stuff for displaying route
        self.whole_route: list[int] = []

        self.departure_time.timeChanged.connect(self.update_route)
        self.arrival_time.timeChanged.connect(self.arrival_time_changed)

        self.load_destinations_to_selector_list(self.line_id)
        self.destination_selector_list.currentIndexChanged.connect(self.stop_selected)

    def arrival_time_changed(self):
        print("CTCUI: Arrival Time Changed handler")
        self.set_arrival_time(self.get_arrival_time())
        if self.route.__len__() > 0:
            self.update_route()

    def clear_route(self):
        self.dispatch_train_schedule.setRowCount(0)

    # Sets the table Arrival Time and Departure Time entry for one stop
    def fill_route_table_time_line(self, row_number: int, stop: Stop):
        arrival_time = strftime("%H:%M", strptime(ctime(stop.arrival_time)))
        departure_time = strftime("%H:%M", strptime(ctime(stop.departure_time)))
        arrival_time_table_widget = QTableWidgetItem(arrival_time)
        departure_time_table_widget = QTableWidgetItem(departure_time)
        self.dispatch_train_schedule.setItem(row_number, 1, arrival_time_table_widget)
        self.dispatch_train_schedule.setItem(row_number, 2, departure_time_table_widget)

    # Sets the table Station Name entry for one stop
    def fill_route_table_stop_line(self, row_number: int, stop: Stop):
        name = stop_name(self.line_id, stop.block)
        selected_stop_table_item = QTableWidgetItem(name)
        selected_stop_table_item.setText(name)
        selected_stop_table_item.setFlags(
            PyQt6.QtCore.Qt.ItemFlag.ItemIsUserCheckable | PyQt6.QtCore.Qt.ItemFlag.ItemIsEnabled)
        selected_stop_table_item.setCheckState(PyQt6.QtCore.Qt.CheckState.Checked)
        self.dispatch_train_schedule.setItem(row_number, 0, selected_stop_table_item)

    # Populates the route table with a schedulable route.
    def fill_route_table(self, route: list[Stop]):
        self.dispatch_train_schedule.setRowCount(0)
        # print("Filling Route Table:")
        # for stop in route:
        #     print(stop)
        for row_number, stop in enumerate(route[:-1]):
            self.dispatch_train_schedule.insertRow(row_number)
            self.fill_route_table_stop_line(row_number, stop)
            self.fill_route_table_time_line(row_number, stop)

        # last stop: no departure time, not checkable.
        self.dispatch_train_schedule.insertRow(len(route) - 1)
        name = stop_name(self.line_id, route[-1].block)
        selected_stop_table_item = QTableWidgetItem(name)
        selected_stop_table_item.setText(name)
        # TODO verify that this grays out check box but keeps it checked
        selected_stop_table_item.setFlags(
            PyQt6.QtCore.Qt.ItemFlag.ItemIsEnabled)
        selected_stop_table_item.setCheckState(PyQt6.QtCore.Qt.CheckState.Checked)
        self.dispatch_train_schedule.setItem(len(route) - 1, 0, selected_stop_table_item)

        # arrival time only
        arrival_time = strftime("%H:%M", strptime(ctime(route[-1].arrival_time)))
        departure_time = "--"
        arrival_time_table_widget = QTableWidgetItem(arrival_time)
        departure_time_table_widget = QTableWidgetItem(departure_time)
        self.dispatch_train_schedule.setItem(len(route) - 1, 1, arrival_time_table_widget)
        self.dispatch_train_schedule.setItem(len(route) - 1, 2, departure_time_table_widget)

    # on press
    def dispatch_button_handler(self):
        print(f"CTCUI: Train {0} Dispatch Button Pressed")
        self.dispatch_button_pressed.emit(self.route)

    def enable_dispatch_button(self):
        self.dispatch_train_button.setEnabled(True)

    def disable_dispatch_button(self):
        self.dispatch_train_button.setEnabled(False)

    # Fills destination select list with possible destinations for a line. Trigger when line change signal occurs
    @pyqtSlot(int)
    def tab_selected(self, line_id: int):
        self.load_destinations_to_selector_list(line_id)
        self.line_id = line_id
        self.line_changed.emit(line_id)

    def load_destinations_to_selector_list(self, line_id: int):
        self.destination_selector_list.clear()
        self.destination_selector_list.addItem("Select Destination...")

        for block in GREEN_LINE[BLOCKS]:
            if block in GREEN_LINE[STATIONS]:
                block_list_name = GREEN_LINE[BLOCKS][block].name + " (STATION: %s)" % GREEN_LINE[STATIONS][block]
            else:
                block_list_name = GREEN_LINE[BLOCKS][block].name
            self.destination_selector_list.addItem(block_list_name)

    def get_departure_time(self) -> float:
        return convert_qtime_to_secs_since_epoch(self.departure_time.time())

    def get_arrival_time(self) -> float:
        return convert_qtime_to_secs_since_epoch(self.arrival_time.time())

    def set_arrival_time(self, arrival_time: float):
        print("CTCUI: Arrival Time Updated")
        self.arrival_time.set_time(arrival_time)

    # TODO test
    def stop_check_handler(self, stop):
        # stop selected
        stop_index = stop.row()
        if stop.checkState().isChecked():
            self.whole_route[stop_index] = True
        else:
            self.whole_route[stop_index] = False

        # update route and update times
        self.update_route()

    def update_route(self):
        print("CTCUI: Update Route")
        self.route.clear()
        route_to_schedule = []
        for index, stop in enumerate(self.whole_route):
            if self.whole_route[index]:
                route_to_schedule.append(stop)

        if len(route_to_schedule) > 0:
            self.route = calculate_times_through_route(self.line_id, self.get_departure_time(), self.get_arrival_time(),
                                                       route_to_schedule)
            print("CTCUI: Route travel time calculated")

            self.arrival_time.timeChanged.disconnect()
            self.set_arrival_time(Route.route_arrival_time(self.route))
            self.arrival_time.timeChanged.connect(self.arrival_time_changed)

            # update table
            self.fill_route_table(self.route)

    def update_train_number(self, number: int):
        self.dispatch_train_number_label.setText("Train Number: %d" % number)
        self.dispatch_train_button.setText("Dispatch Train #%d" % number)

    @pyqtSlot(int)
    def stop_selected(self, index):
        print("CTCUI: Stop selected:", index)
        # Selection cannot be Select Line, Yard
        # TODO can be yard once yard only shows up once in block list. When yard is selected and the train is not dispatched, the train goes through the whole route. Destination is still listed as final stop.
        if index == 1:
            # yard
            self.disable_dispatch_button()
        elif 1 < index < GREEN_LINE[BLOCKS].__len__():
            block_keys = list(GREEN_LINE[BLOCKS].keys())
            self.train_destination = block_keys[index - 1]

            print(f"CTCUI: Selected destination: block {0} ({1})".format(self.train_destination, stop_name(self.line_id, self.train_destination)))
            # Find all possible stops
            self.whole_route = Route.find_route(self.line_id, self.train_origin, self.train_destination)

            self.stops.clear()
            # set each stop to True.
            for _ in self.whole_route:
                self.stops.append(True)

            # Calculate times through route given current departure time. If the arrival time is not possible, find the minimum time through the route, and update the displayed arrival time.
            self.update_route()
            self.enable_dispatch_button()
        else:
            self.train_destination = 0
            self.clear_route()
            self.disable_dispatch_button()


    # TODO implement redispatching trains that have stopped (likely another widget)
    def train_selected(self, train: Train):
        pass

    def get_dispatch_train_tab(self, line_id: int):
        pass


class BlockTable(QTableWidget):
    def __init__(self, ctc: CTC):
        super().__init__()

        self.ctc = ctc

        self.setColumnCount(10)
        self.verticalHeader().setVisible(False)

        self.setHorizontalHeaderLabels(
            ["Block ID", "Occupied", "Block Open", "Signal Status", "Switch Destination",
             "Railroad Crossing Activated", "Length (ft)", "Speed Limit (mph)", "Suggested Speed", "Authority"])

    @pyqtSlot()
    def update_table(self):
        for row, block in enumerate(GREEN_LINE[BLOCKS]):
            block_length_ft = float(GREEN_LINE[BLOCKS][block].length) * 3.28084
            block_speed_limit_mph = GREEN_LINE[BLOCKS][block].speed_limit / 1.609

            occupied = "Yes" if self.ctc.blocks[block] is True else "No"

            self.setItem(row, 1, QTableWidgetItem(occupied))
            self.setItem(row, 6, QTableWidgetItem(str(block_length_ft)))
            self.setItem(row, 7, QTableWidgetItem(str(block_speed_limit_mph)))
            self.setItem(row, 8, QTableWidgetItem(str(self.ctc.suggested_speeds[block])))
            self.setItem(row, 9, QTableWidgetItem(str(self.ctc.authorities[block])))

    def fill_table_for_line(self, line_id: int):
        # clear rows
        self.setRowCount(0)

        # TODO fix block data
        for block in GREEN_LINE[BLOCKS]:
            row = self.rowCount()
            self.insertRow(row)
            block_id = block
            block_length_ft = float(GREEN_LINE[BLOCKS][block].length) * 3.28084
            block_speed_limit_mph = GREEN_LINE[BLOCKS][block].speed_limit / 1.609

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
    timeChanged = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.dispatch_arrival_time_layout = QVBoxLayout()
        self.dispatch_train_arrival_time_label = QLabel("Arrival Time")
        f = self.dispatch_train_arrival_time_label.font()

        self.dispatch_train_arrival_time = QTimeEdit()
        self.dispatch_train_arrival_time.setDisplayFormat("HH:mm")

        dt = QDateTime()
        dt.setSecsSinceEpoch(int(SystemTime.time()))

        self.dispatch_train_arrival_time.setTime(dt.time())

        self.dispatch_arrival_time_layout.addWidget(self.dispatch_train_arrival_time_label)
        self.dispatch_arrival_time_layout.addWidget(self.dispatch_train_arrival_time)

        self.setLayout(self.dispatch_arrival_time_layout)
        self.setFixedSize(self.minimumSizeHint())

        self.dispatch_train_arrival_time.timeChanged.connect(self.time_changed_handler)

    @pyqtSlot()
    def time_changed_handler(self):
        self.timeChanged.emit()

    def get_time_box_widget(self):
        return self.dispatch_train_arrival_time

    def set_time(self, time: float):
        dt = QDateTime()
        dt.setSecsSinceEpoch(int(time))
        self.dispatch_train_arrival_time.setTime(dt.time())

    def time(self):
        return self.dispatch_train_arrival_time.time()


class DispatchDepartureTime(QWidget):
    timeChanged = pyqtSignal()
    def __init__(self):
        super().__init__()

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
        self.depart_now_button.setCheckable(True)
        self.depart_now_button.setChecked(False)
        self.depart_now_button.clicked.connect(self.update_time)
        self.depart_now_button.click()

        self.dispatch_train_departure_time_button_hbox.addWidget(self.dispatch_train_departure_time)
        self.dispatch_train_departure_time_button_hbox.addWidget(self.depart_now_button)
        self.dispatch_train_departure_time_button_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.dispatch_train_departure_time_layout.addWidget(self.dispatch_train_departure_time_label)
        self.dispatch_train_departure_time_layout.addItem(self.dispatch_train_departure_time_button_hbox)
        self.dispatch_train_departure_time_layout.setSpacing(0)

        self.setLayout(self.dispatch_train_departure_time_layout)
        self.setFixedSize(self.minimumSizeHint())

        self.set_time(SystemTime.time())

        self.dispatch_train_departure_time.timeChanged.connect(self.time_changed_handler)

    def time_changed_handler(self):
        self.timeChanged.emit()

    def set_time(self, time: float):
        dt = QDateTime()
        dt.setSecsSinceEpoch(int(time))
        self.dispatch_train_departure_time.setTime(dt.time())

    def update_time(self):
        if self.depart_now_button.isChecked():
            time = SystemTime.time()
            self.set_time(time)

    def time(self):
        return self.dispatch_train_departure_time.time()

    def get_now_button(self):
        return self.depart_now_button


if __name__ == "__main__":
    # define CTC Object
    # pass CTC Object to CTC_MainWindow()

    ctc_ui_app = QApplication([])

    # track_layout_files = ["CTC/Green Line Track Data.csv", "CTC/Red Line Track Data.csv"]
    # track_layout_files = ["CTC/Blue Line Track Data.csv"]

    window = CTCMainWindow(CTC())
    window.show()

    ctc_ui_app.exec()
