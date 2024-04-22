import PyQt6
from PyQt6 import QtWidgets

from CTC.CTCConstants import *
from time import localtime, strftime, strptime, struct_time, time, ctime
from PyQt6.QtCore import QSize, Qt, QDateTime, QTime, QTimer, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, \
    QGridLayout, QComboBox, QHBoxLayout, QTimeEdit, QTableWidget, QTableWidgetItem, QTabWidget, QAbstractScrollArea, \
    QHeaderView

from CTC.CTCSignals import CTCSignals
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


def get_block_id(line_id: int, route_block_index: int) -> int:
    """
    Returns the block id for the block at position route_block_index in the route
    where route_block_index = 0 is the yard spawn, and route_block_index len(route) - 1 is the yard delete
    """
    return abs(get_line_route()[route_block_index])


def calculate_times_through_route(line_id: int, departure_time: float, arrival_time: float, route: list[int]) \
        -> list[Stop]:
    route_stops = Route.get_route_stops(line_id, route)
    minimum_travel_time = Route.get_route_travel_time(route_stops)

    print("============= Testing Arrival Time ============")
    print(f"\tDeparture time: {time_to_str(departure_time)}")
    print(f"\tArrival time: {time_to_str(arrival_time)}")
    print(f"\tMinimum travel time: {minimum_travel_time}")
    print(f"\tProposed travel time: {arrival_time - departure_time}")

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


# TODO move running trains to its own class
# TODO move scheduled trains to its own class


class CTCMainWindow(QMainWindow):
    def __init__(self):
        super(CTCMainWindow, self).__init__()

        self.next_train_number = 0
        self.mode: int = 0
        self.stops = []

        self.setWindowTitle("CTC Office")

        # Dispatch Train Tab
        self.dispatch_train_layout = DispatchTrainLayout(LINES)

        # Connect Signals from dispatch train layout

        # TODO get rid of validate destination select. When Select Destination... is selected from the list the signal is not emitted.
        self.dispatch_train_layout.dispatch_button_pressed.connect(self.schedule_train)

        # Time in center of window
        self.ctc_main_right_side = QVBoxLayout()
        self.ctc_main_right_side.setSpacing(10)
        self.ctc_main_layout_right_top_section = QHBoxLayout()
        self.train_system_time = QLabel(strftime("%H:%M:%S", localtime(SystemTime.time())))
        train_system_time_font = self.train_system_time.font()
        train_system_time_font.setPointSize(30)
        self.train_system_time.setFont(train_system_time_font)

        self.ctc_mode_select = QComboBox()
        self.ctc_mode_select.addItems(["Automatic Mode", "Manual Mode", "Maintenance Mode"])
        self.ctc_main_layout_right_top_section.addWidget(self.train_system_time)
        self.ctc_main_layout_right_top_section.addWidget(self.ctc_mode_select)
        self.ctc_mode_select.currentIndexChanged.connect(self.mode_switch_handler)
        self.ctc_mode_select.setFixedSize(self.ctc_mode_select.sizeHint())

        self.ctc_mode_select.setCurrentIndex(self.mode)

        if self.mode == MANUAL_MODE or self.mode == MAINTENANCE_MODE:
            self.ctc_mode_select.model().item(0).setEnabled(False)

        self.ctc_main_right_side.addItem(self.ctc_main_layout_right_top_section)

        # Currently Running Trains
        self.running_trains = RunningTrainsTableLayout()
        self.ctc_main_right_side.addItem(self.running_trains)

        # Scheduled Trains
        self.scheduled_trains = ScheduledTrainsTableLayout()
        self.ctc_main_right_side.addItem(self.scheduled_trains)

        # currently_running_trains_layout = QVBoxLayout()
        #
        # currently_running_trains_label = QLabel("Currently Running Trains")
        # currently_running_trains_layout.addWidget(currently_running_trains_label)
        #
        # self.running_trains_table = QTableWidget()
        # self.running_trains_table.verticalHeader().setHidden(True)
        # # self.running_trains_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        # # self.running_trains_table.resizeColumnsToContents()
        #
        # self.running_trains_table.setColumnCount(8)
        # self.running_trains_table.setHorizontalHeaderLabels(
        #     ["Train Number", "Line", "Destination", "Arrival Time", "Next Stop", "Time to Next Stop (min)",
        #      "Current Block", "Authority (blocks)"])
        # currently_running_trains_layout.addWidget(self.running_trains_table)
        # ctc_main_right_side.addLayout(currently_running_trains_layout)
        # Scheduled Trains
        # scheduled_trains_layout = QVBoxLayout()
        # scheduled_trains_header_layout = QHBoxLayout()
        # scheduled_trains_label = QLabel("Scheduled Trains")
        # import_schedule_button = QPushButton("Import Schedule")
        # import_schedule_button.setFixedSize(import_schedule_button.sizeHint())
        #
        # scheduled_trains_header_layout.addWidget(scheduled_trains_label)
        # scheduled_trains_header_layout.addWidget(import_schedule_button)
        # scheduled_trains_layout.addLayout(scheduled_trains_header_layout)
        #
        # self.scheduled_trains_table = QTableWidget()
        # self.scheduled_trains_table.setColumnCount(6)
        # self.scheduled_trains_table.setHorizontalHeaderLabels(
        #     ["Train Number", "Line", "Destination", "Arrival Time", "First Stop", "Time to Departure (min)"])
        # scheduled_trains_layout.addWidget(self.scheduled_trains_table)
        # # self.scheduled_trains_table.verticalHeader().setHidden(True)
        # # self.scheduled_trains_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        # # self.scheduled_trains_table.resizeColumnsToContents()

        # ctc_main_right_side.addLayout(scheduled_trains_layout)

        self.ctc_main_right_side_bottom = QHBoxLayout()
        self.ctc_main_right_side_bottom.setSpacing(10)

        # Block table
        # Search bar: https://www.pythonguis.com/faq/how-to-create-a-filter-search-bar-for-a-qtablewidget/
        # block_table_layout = QVBoxLayout()
        # block_table_label = QLabel("Block Table")
        # block_table_search_bar = QLineEdit()
        # block_table_search_bar.setPlaceholderText("Search for Block")
        # block_table_search_bar.setFixedSize(block_table_search_bar.sizeHint())
        #
        # block_table_line_select = QComboBox()
        # block_table_line_select.addItems([line_name for line_name in LINES])
        #
        # block_table_header_layout = QHBoxLayout()
        # block_table_header_layout.addWidget(block_table_label)
        # block_table_header_layout.addWidget(block_table_line_select)
        # block_table_header_layout.addWidget(block_table_search_bar)
        #
        # block_table_layout.addItem(block_table_header_layout)
        #
        # self.block_table = BlockTable()
        # self.block_table.fill_table_for_line(0)
        #
        # block_table_line_select.currentIndexChanged.connect(self.block_table.fill_table_for_line)
        # block_table_search_bar.textChanged.connect(self.block_table.search)
        #
        # block_table_layout.addWidget(self.block_table)

        # Block Table
        self.block_table = BlockTableLayout()
        self.ctc_main_right_side_bottom.addItem(self.block_table)

        self.ctc_throughput_layout = QVBoxLayout()
        self.ctc_throughput_label = QLabel("System Throughput")
        self.ctc_throughput_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.ctc_throughput_layout.addWidget(self.ctc_throughput_label)

        self.ctc_main_layout_throughput = QGridLayout()
        self.ctc_main_layout_throughput.addWidget(QLabel("Trains Per Hour"), 0, 1)
        self.ctc_main_layout_throughput.addWidget(QLabel("# Ticket Sales Per Hour"), 0, 2)

        for id, line in enumerate(LINES):
            self.ctc_main_layout_throughput.addWidget(QLabel(line), id + 1, 0)

        self.ctc_throughput_layout.addItem(self.ctc_main_layout_throughput)
        self.ctc_main_right_side_bottom.addItem(self.ctc_throughput_layout)

        self.ctc_main_right_side.addItem(self.ctc_main_right_side_bottom)

        self.ctc_main_layout = QHBoxLayout()
        self.ctc_main_layout.addLayout(self.dispatch_train_layout)

        self.ctc_main_layout.addItem(self.ctc_main_right_side)

        main_layout_widget = QWidget()
        main_layout_widget.setLayout(self.ctc_main_layout)

        self.setCentralWidget(main_layout_widget)

        self.route: list[int] = []

        # Connect signals from CTC
        self.connect_backend_signals()

        # Initialize data from CTC
        self.initialize_ui_data_from_backend()

        self.time_update_timer = QTimer()
        self.time_update_timer.timeout.connect(self.update_ctc)

        # 100 msec
        self.time_update_timer.start(100)

    # @pyqtSlot()
    # def refresh_ctc_schedule_data(self):
    #     self.update_running_trains_list()

        # self.block_table.update(GREEN_LINE)

    def get_selected_line(self):
        return self.dispatch_train_layout.line_tab_widget.currentIndex()

    def schedule_train(self, route: list[Stop]):
        # route
        # line
        train = Train(self.next_train_number, self.get_selected_line(), route)
        print(f"CTCUI: Train {self.next_train_number} Scheduled.")
        print("\tt = %s", strftime("%H:%m", localtime(SystemTime.time())))
        print(f"\t{train}\n")

        CTCSignals.ctc_schedule_train_signal.emit(train)
        self.dispatch_train_layout.update_train_number(self.next_train_number)

    # def clear_schedule(self):
    #     self.scheduled_trains_table.setRowCount(0)
    #
    # def update_schedule(self):
    #     self.clear_schedule()
    #     for row, train in enumerate(self.ctc.scheduled_trains.get_schedule()):
    #         self.scheduled_trains_table.insertRow(row)
    #         number = QTableWidgetItem(str(train.id))
    #         line = QTableWidgetItem(LINES[train.line_id])
    #
    #         dest_block = train.get_destination().block
    #         dest_name = stop_name(train.line_id, dest_block)
    #
    #         dest = QTableWidgetItem(dest_name)
    #         first_stop_name = stop_name(train.line_id, train.get_next_stop())
    #         first_stop = QTableWidgetItem(first_stop_name)
    #
    #         min_to_departure = (train.departure_time() - SystemTime.time()) / 60
    #
    #         time_to_departure = QTableWidgetItem(str(round(min_to_departure, 0)))
    #
    #         self.scheduled_trains_table.setItem(row, 0, number)
    #         self.scheduled_trains_table.setItem(row, 1, line)
    #         self.scheduled_trains_table.setItem(row, 2, dest)
    #         # self.scheduled_trains_table.setItem(row, 3, QTableWidgetItem)
    #         self.scheduled_trains_table.setItem(row, 4, first_stop)
    #         self.scheduled_trains_table.setItem(row, 5, time_to_departure)

    # def get_stops_to_destination(self, id):
    #     stops_to_dest = Route.find_route(self.get_selected_line(), GREEN_LINE_YARD_SPAWN, id)
    #     return stops_to_dest

    def mode_switch_handler(self, mode):
        modes = ["Automatic Mode", "Manual Mode", "Maintenance Mode"]
        self.mode = mode
        # disable automatic mode on switch from auto mode.
        if mode == MANUAL_MODE or mode == MAINTENANCE_MODE:
            self.ctc_mode_select.model().item(0).setEnabled(False)

        print("CTC: Switched to %s." % modes[mode])

    def connect_backend_signals(self):
        # Return signals for data requested from backend
        CTCSignals.ui_scheduled_trains_signal.connect(self.get_scheduled_trains_signal_handler)
        CTCSignals.ui_next_train_number_signal.connect(self.get_next_train_number_signal_handler)
        CTCSignals.ui_running_trains_signal.connect(self.get_running_trains_signal_handler)
        CTCSignals.ui_mode_signal.connect(self.get_mode_signal_handler)
        CTCSignals.ui_blocks_signal.connect(self.get_blocks_signal_handler)
        # self.ctc_signals.ui_track_signals_signal.connect(self.get_track_signals_signal_handler)
        CTCSignals.ui_authorities_signal.connect(self.get_authorities_signal_handler)
        CTCSignals.ui_suggested_speeds_signal.connect(self.get_suggested_speeds_signal_handler)
        CTCSignals.ui_switch_positions_signal.connect(self.get_switch_positions_signal_handler)
        CTCSignals.ui_lights_signal.connect(self.get_lights_signal_handler)

    def initialize_ui_data_from_backend(self):
        # Fill running trains list
        CTCSignals.ctc_get_running_trains_signal.emit()

        # Fill Scheduled trains list
        CTCSignals.ctc_get_scheduled_trains_signal.emit()

        # Set mode
        CTCSignals.ctc_get_mode_signal.emit()

        # Set next train number
        CTCSignals.ctc_get_next_train_number_signal.emit()

        # fill block table (occupancies, speed, authority)
        CTCSignals.ctc_get_authority_signal.emit()
        CTCSignals.ctc_get_blocks_signal.emit()
        CTCSignals.ctc_get_suggested_speeds_signal.emit()

    # def update_running_trains_list(self):
    #     table = self.running_trains_table
    #
    #     # Clear table
    #     table.setRowCount(0)
    #
    #     for row, train in enumerate(self.ctc.get_running_trains()):
    #         table.insertRow(row)
    #         train_number = str(train.id)
    #         # TODO train_line = sorted(LINES[train.line_id].items())
    #         destination = stop_name(train.line_id, Route.get_block(train.get_destination().block))
    #
    #         table.setItem(row, 0, QTableWidgetItem(train_number))
    #         table.setItem(row, 1, QTableWidgetItem(LINES[train.line_id]))
    #         table.setItem(row, 2, QTableWidgetItem(destination))
    #         table.setItem(row, 3, QTableWidgetItem(time_to_str(train.get_destination().arrival_time)))
    #         table.setItem(row, 4, QTableWidgetItem(stop_name(train.line_id, train.route[train.next_stop].block)))
    #         table.setItem(row, 6, QTableWidgetItem(str(train.current_block)))
    #         table.setItem(row, 7, QTableWidgetItem(str(train.blocks_to_next_stop() - 1)))

    def update_ctc(self):
        self.update_time()
        CTCSignals.ctc_update_queues_signal.emit()

    def update_time(self):
        current_time = strftime("%H:%M:%S", localtime(SystemTime.time()))
        # [label.setTime(get_current_time_qtime()) for label in self.departure_time_list]
        self.train_system_time.setText(current_time)

    @pyqtSlot(list)
    def get_scheduled_trains_signal_handler(self, scheduled_trains: list[Train]):
        self.scheduled_trains.update_scheduled_trains(scheduled_trains)

    @pyqtSlot(int)
    def get_next_train_number_signal_handler(self, next_train_number: int):
        self.next_train_number = next_train_number
        self.dispatch_train_layout.update_train_number(next_train_number)

    @pyqtSlot(dict)
    def get_suggested_speeds_signal_handler(self, suggested_speeds: dict[int, float]):
        self.block_table.update_suggested_speeds(suggested_speeds)

    @pyqtSlot(list)
    def get_running_trains_signal_handler(self, running_trains: list[Train]):
        self.running_trains.update_running_trains(running_trains)

    @pyqtSlot(list)
    def get_lights_signal_handler(self, lights: list[Light]):
        self.block_table.update_lights(lights)

    @pyqtSlot(int)
    def get_mode_signal_handler(self, mode: int):
        self.mode_switch_handler(mode)

    @pyqtSlot(dict)
    def get_blocks_signal_handler(self, block_occupancies: dict[int, bool]):
        self.block_table.update_block_occupancies(block_occupancies)

    @pyqtSlot(dict)
    def get_authorities_signal_handler(self, authorities: dict[int, int]):
        print("CTCUI: Authorities received from backend")
        self.block_table.update_authorities(authorities)

    @pyqtSlot(list)
    def get_switch_positions_signal_handler(self, switch_positions: list[Switch]):
        self.block_table.update_switch_positions(switch_positions)

    def update_running_trains_list(self):
        CTCSignals.ctc_get_running_trains_signal.emit()

    def update_scheduled_trains_list(self):
        CTCSignals.ctc_get_scheduled_trains_signal.emit()


class RunningTrainsTableLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget()
        self.label = QLabel("Currently Running Trains")
        self.addWidget(self.label)
        self.table.verticalHeader().setHidden(True)

        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Train Number", "Line", "Destination", "Arrival Time", "Next Stop", "Time to Next Stop (min)",
             "Current Block", "Authority (blocks)"])
        self.addWidget(self.table)

    def clear_table(self):
        self.table.setRowCount(0)

    def update_running_trains(self, running_trains: list[Train]):
        print(f"CTCUI: updating running trains. {len(running_trains)}")
        self.clear_table()

        for row, train in enumerate(running_trains):
            self.table.insertRow(row)
            train_number = str(train.id)
            # TODO train_line = sorted(LINES[train.line_id].items())
            destination = stop_name(train.line_id, Route.get_block(train.get_destination().block))

            self.table.setItem(row, 0, QTableWidgetItem(train_number))
            self.table.setItem(row, 1, QTableWidgetItem(LINES[train.line_id]))
            self.table.setItem(row, 2, QTableWidgetItem(destination))
            self.table.setItem(row, 3, QTableWidgetItem(
                time_to_str(train.get_destination().arrival_time)))
            self.table.setItem(row, 4, QTableWidgetItem(stop_name(train.line_id,
                                                                  train.route[train.next_stop].block)))
            self.table.setItem(row, 6, QTableWidgetItem(str(train.current_block)))
            self.table.setItem(row, 7, QTableWidgetItem(str(train.blocks_to_next_stop() - 1)))


class ScheduledTrainsTableLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.header_layout = QHBoxLayout()
        self.label = QLabel("Scheduled Trains")
        self.import_schedule_button = QPushButton("Import Schedule")
        self.import_schedule_button.setFixedSize(self.import_schedule_button.sizeHint())

        self.header_layout.addWidget(self.label)
        self.header_layout.addWidget(self.import_schedule_button)
        self.addLayout(self.header_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Train Number", "Line", "Destination", "Arrival Time", "First Stop", "Time to Departure (min)"])
        self.addWidget(self.table)
        # self.scheduled_trains_table.verticalHeader().setHidden(True)
        # self.scheduled_trains_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        # self.scheduled_trains_table.resizeColumnsToContents()

    def enable_import_button(self):
        self.import_schedule_button.setEnabled(True)

    def disable_import_button(self):
        self.import_schedule_button.setEnabled(False)

    def clear_table(self):
        self.table.setRowCount(0)

    def update_scheduled_trains(self, scheduled_trains: list[Train]):
        self.clear_table()
        for row, train in enumerate(scheduled_trains):
            self.table.insertRow(row)
            number = QTableWidgetItem(str(train.id))
            line = QTableWidgetItem(LINES[train.line_id])

            dest_block = train.get_destination().block
            dest_name = stop_name(train.line_id, dest_block)

            dest = QTableWidgetItem(dest_name)
            first_stop_name = stop_name(train.line_id, train.get_next_stop())
            first_stop = QTableWidgetItem(first_stop_name)

            min_to_departure = (train.departure_time() - SystemTime.time()) / 60

            time_to_departure = QTableWidgetItem(str(round(min_to_departure, 0)))

            self.table.setItem(row, 0, number)
            self.table.setItem(row, 1, line)
            self.table.setItem(row, 2, dest)
            # self.scheduled_trains_table.setItem(row, 3, QTableWidgetItem)
            self.table.setItem(row, 4, first_stop)
            self.table.setItem(row, 5, time_to_departure)


class BlockTableLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Block Table")
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for Block")
        self.search_bar.setFixedSize(self.search_bar.sizeHint())

        self.line_select = QComboBox()
        self.line_select.addItems([line_name for line_name in LINES])

        self.header_layout = QHBoxLayout()
        self.header_layout.addWidget(self.label)
        self.header_layout.addWidget(self.line_select)
        self.header_layout.addWidget(self.search_bar)

        self.addItem(self.header_layout)

        self.block_table = BlockTable()
        self.block_table.init_table_for_line(0)

        self.line_select.currentIndexChanged.connect(self.block_table.init_table_for_line)
        self.search_bar.textChanged.connect(self.block_table.search)

        self.addWidget(self.block_table)

    def update_block_occupancies(self, block_occupancies: dict[int, bool]):
        self.block_table.update_block_occupancies(block_occupancies)

    def update_authorities(self, authorities: dict[int, int]):
        self.block_table.update_authorities(authorities)

    def update_switch_positions(self, switch_positions: list[Switch]):
        self.block_table.update_switches(switch_positions)

    def update_suggested_speeds(self, suggested_speeds: dict[int, float]):
        self.block_table.update_suggested_speeds(suggested_speeds)

    def update_lights(self, lights: list[Light]):
        self.block_table.update_lights(lights)

    def update_railroad_crossings(self, railroad_crossings: list[RRCrossing]):
        self.block_table.update_railroad_crossings(railroad_crossings)


class DispatchTrainLayout(QVBoxLayout):
    line_changed = pyqtSignal(int)
    dispatch_button_pressed = pyqtSignal(list)
    selected_stop_changed = pyqtSignal(int)

    def __init__(self, lines: list[str]):
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

        self.next_train_id = 0

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
        # self.arrival_time.timeChanged.connect(self.arrival_time_changed)

        self.load_destinations_to_selector_list(self.line_id)
        self.destination_selector_list.currentIndexChanged.connect(self.stop_selected)

    def set_next_train_id(self, id: int):
        self.next_train_id = id

    def arrival_time_changed(self):
        print("CTCUI: Arrival Time Changed handler")
        self.set_arrival_time(self.get_arrival_time())
        if self.route.__len__() > 0:
            self.update_route()
        pass

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
        print(f"CTCUI: Train {self.next_train_id} Dispatch Button Pressed")
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

        for block in get_line_blocks_in_route_order():
            block_list_name = stop_name(self.line_id, block)
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

            # self.arrival_time.timeChanged.disconnect()
            # if self.get_arrival_time() < Route.route_arrival_time(self.route):
            self.set_arrival_time(Route.route_arrival_time(self.route))
            # self.arrival_time.timeChanged.connect(self.arrival_time_changed)

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
            block_keys = list(get_line_blocks_in_route_order().keys())
            self.train_destination = block_keys[index - 1]

            print(f"CTCUI: Selected destination: block {0} ({1})".format(self.train_destination, stop_name(self.line_id,
                                                                                                           self.train_destination)))
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
    block_id_column_index = 0
    block_occupancy_column_index = 1
    block_open_column_index = 2
    signal_status_column_index = 3
    switch_destination_column_index = 4
    railroad_crossing_column_index = 5
    length_column_index = 6
    speed_limit_column_index = 7
    suggested_speed_column_index = 8
    authority_column_index = 9

    def __init__(self):
        super().__init__()

        self.setColumnCount(10)
        self.verticalHeader().setVisible(False)

        self.setHorizontalHeaderLabels(
            ["Block ID", "Occupied", "Block Open", "Signal Status", "Switch Destination",
             "Railroad Crossing Activated", "Length (ft)", "Speed Limit (mph)", "Suggested Speed", "Authority"])

        self.row_block_mapping = list(get_line_blocks().keys())

    def init_table_for_line(self, line_id: int):
        # clear rows
        self.setRowCount(0)

        # TODO fix block data
        for row, block in enumerate(self.row_block_mapping):
            self.insertRow(row)
            block_id = block
            block_length_ft = float(get_line_blocks()[block].length) * 3.28084
            block_speed_limit_mph = get_line_blocks()[block].speed_limit / 1.609

            # occupied = "Yes" if self.ctc.blocks[block] is True else "No"

            block_id_widget = QTableWidgetItem(str(block_id))
            block_length_widget = QTableWidgetItem(str(block_length_ft))
            speed_widget = QTableWidgetItem(str(block_speed_limit_mph))

            self.setItem(row, 0, block_id_widget)
            self.setItem(row, 6, block_length_widget)
            self.setItem(row, 7, speed_widget)

            # initialize switch
            if block in [switch.block for switch in get_line_switches()]:
                switch = get_line_switches()[[switch.block for switch in get_line_switches()].index(block)]
                switch_dest_combo_box = QComboBox()
                switch_dest_combo_box.addItem(str(switch.pos_a))
                switch_dest_combo_box.addItem(str(switch.pos_b))
                switch_dest_combo_box.setCurrentIndex([switch.pos_a, switch.pos_b].index(switch.current_pos))

                # TODO connect to maintenance mode handler
                # TODO connect to switch changed list to set index
                # switch_table_widget = QTableWidgetItem(switch_dest_combo_box)
                self.setCellWidget(row, self.switch_destination_column_index, switch_dest_combo_box)

        # Call CTCSignals to populate rest of table
        CTCSignals.ctc_get_blocks_signal.emit()
        CTCSignals.ctc_get_authority_signal.emit()
        CTCSignals.ctc_get_switch_positions_signal.emit()
        CTCSignals.ctc_get_suggested_speeds_signal.emit()
        CTCSignals.ctc_get_lights_signal.emit()
        CTCSignals.ctc_get_switch_positions_signal.emit()
        CTCSignals.ctc_get_railroad_crossings_signal.emit()

    def search(self, search_term: str):
        self.setCurrentItem(None)

        if not search_term:
            return

        search_results = self.findItems(search_term, Qt.MatchFlag.MatchContains)
        if search_results:
            for search_result in search_results:
                search_result.setSelected(True)

    def update_block_occupancies(self, block_occupancies):
        for block in block_occupancies:
            occupied = "Yes" if block_occupancies[block] is True else "No"
            self.setItem(self.row_block_mapping.index(block), self.block_occupancy_column_index,
                         QTableWidgetItem(occupied))

    def update_authorities(self, authorities: dict[int, int]):
        for block in authorities:
            self.setItem(self.row_block_mapping.index(block), self.authority_column_index,
                         QTableWidgetItem(str(authorities[block])))

    def update_suggested_speeds(self, suggested_speeds: dict[int, float]):
        for block in suggested_speeds:
            self.setItem(self.row_block_mapping.index(block), self.suggested_speed_column_index,
                         QTableWidgetItem(str(suggested_speeds[block])))

    def update_lights(self, lights: list[Light]):
        for light in lights:
            light_status = "Green" if light.val is True else "Red"
            self.setItem(self.row_block_mapping.index(light.block), self.signal_status_column_index,
                         QTableWidgetItem(light_status))

    def update_switches(self, switches: list[Switch]):
        for switch in switches:
            switch_dest = switch.current_pos
            switch_combo_box = self.cellWidget(self.row_block_mapping.index(switch.block),
                                               self.switch_destination_column_index)
            switch_combo_box.setCurrentIndex([switch.pos_a, switch.pos_b].index(switch_dest))

    def update_railroad_crossings(self, railroad_crossings: list[RRCrossing]):
        for crossing in railroad_crossings:
            crossing_state = "Activated" if crossing.val is True else "Not Activated"

            self.setItem(self.row_block_mapping.index(crossing.block), self.railroad_crossing_column_index,
                         QTableWidgetItem(crossing_state))


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

    def time(self) -> QTime:
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

    window = CTCMainWindow()
    window.show()

    ctc_ui_app.exec()
