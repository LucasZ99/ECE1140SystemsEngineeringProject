import subprocess
import json

class PlcProgram(object):
    def __init__(self):
        super().__init__()
        self.filepath = None
        # self.filepath_test_A = "PLCProgramSectionA.py"

    def set_filepath(self, filepath: str):
        self.filepath = filepath
        print(f"filepath: {self.filepath}")

    def execute_plc(self, occupancy_list: list[bool]):

        arg_json = json.dumps(occupancy_list)
        try:
            result = subprocess.check_output(['python', self.filepath, arg_json], stderr=subprocess.STDOUT)
            result_decoded = result.decode('utf-8')
            result_list = json.loads(result_decoded)
            print("result list: ", result_list)
            return result_list
        except subprocess.CalledProcessError as e:
            # Handle any errors
            print("Error:", e.output.decode('utf-8'))


# if __name__ == "__main__":
#     program = PlcProgram()
#     output = program.execute_plc([True, False, False], section="A")
#     print(output)
