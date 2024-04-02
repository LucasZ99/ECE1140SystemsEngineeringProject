from CTC.CTCSchedule import CTCSchedule
from CTC.Train import Train
from SystemTime import SystemTime
from Track_Controller_SW.switching import Switch
from PyQt6.QtCore import QObject



class CTC(QObject):
    def __init__(self, system_time: SystemTime):
        super().__init__()
        self.system_time = system_time

        self.scheduled_trains = CTCSchedule(system_time)
        self.dispatched_trains = CTCSchedule(system_time)

        self.running_trains: list[Train] = []

    def set_block_to_maintenance_mode(self, line_id: int, block_id: int):
        pass

    def set_switch_position(self, line_id: int, block_id: int, switch: Switch):
        pass

    def set_block_authority(self, train: Train):
        pass

    def set_block_suggested_speeds(self, train: Train):
        pass

    def update_swtich_position(self, line_id: int, block_id: int, switch: Switch):
        pass

    def update_signal_status(self, line_id: int, block_id: int, signal_green: bool):
        pass

    def update_block_occupancy(self, line_id: int, block_id: int, occupied: bool):
        pass

    def update_railroad_crossing_status(self, line_id: int, block_id: int, crossing_activated: bool):
        pass

    def update_ticket_sales(self, line_id: int, sales: int):
        pass

    def timer_handler(self):
        pass
