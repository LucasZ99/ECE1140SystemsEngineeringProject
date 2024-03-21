class PlcProgram(object):
    def __init__(self):
        super().__init__()
        self.filepath = None

    def set_filepath(self, filepath: str):
        self.filepath = filepath
        print(f"filepath: {self.filepath}")

    def execute_plc(self, occupancy_list: list[bool] = None):
        zero_speed_flag_list = [False] * len(occupancy_list)
        # safe_speed, switch_permitted, close_block_permitted = (
        #     subprocess.run(['python', self.filepath, occupancy_list, switches_list, block_to_close]).returncode)
        # return safe_speed, switch_permitted, close_block_permitted
        return zero_speed_flag_list
