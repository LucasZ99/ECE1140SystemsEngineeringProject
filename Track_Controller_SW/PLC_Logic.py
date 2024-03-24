import subprocess
import json

class PlcProgram(object):
    def __init__(self):
        super().__init__()
        self.filepath = None
        self.filepath_test_A = "PLCProgramSectionA.py"

    def set_filepath(self, filepath: str):
        self.filepath = filepath
        print(f"filepath: {self.filepath}")

    def execute_plc(self, occupancy_list: list[bool], section : str):
        zero_speed_flag_list = [False] * len(occupancy_list)

        if section == "A":

            zone_DEF_flag = False
            for block in range(12, 28):
                if occupancy_list[block] is True:
                    zone_DEF_flag = True
                    break

            zone_AB_flag = False
            for block in range(0, 4):
                if occupancy_list[block] is True:
                    zone_AB_flag = True
                    break

            args_list = [occupancy_list,
                         zero_speed_flag_list,
                         zone_DEF_flag,
                         zone_AB_flag,
                         ]
            args_json = json.dumps(args_list)
            try:
                result = subprocess.check_output(['python', self.filepath_test_A, args_json], stderr=subprocess.STDOUT)
                result_decoded = result.decode('utf-8')
                result_list = json.loads(result_decoded)
                return result_list
            except subprocess.CalledProcessError as e:
                # Handle any errors
                print("Error:", e.output.decode('utf-8'))


if __name__ == "__main__":
    program = PlcProgram()
    output = program.execute_plc([True, False, False], section="A")
    print(output)
