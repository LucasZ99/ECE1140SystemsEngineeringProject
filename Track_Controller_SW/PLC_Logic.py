import os
import subprocess
import pickle


class PlcProgram(object):
    def __init__(self, section: str):
        super().__init__()
        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        if section == "A":
            self.filepath = os.path.join(current_dir, 'PLCProgramSectionA.py')
        elif section == "C":
            self.filepath = os.path.join(current_dir, 'PLCProgramSectionC.py')

    def set_filepath(self, filepath: str):
        self.filepath = filepath
        print(f"filepath: {self.filepath}")

    def execute_plc(self, occupancy_list: list[bool]):

        with open('occupancy_file.pkl', 'wb') as f:
            pickle.dump(occupancy_list, f)
            f.close()

        try:
            subprocess.check_output(['python', self.filepath],
                                         stderr=subprocess.STDOUT)
        except Exception as e:
            print(e)
            raise e

        with open('plc_result.pkl', 'rb') as f:
            result = pickle.load(f)

        print("result list: ", result)
        return result


if __name__ == "__main__":
    program = PlcProgram("A")
    output = program.execute_plc([False] * 32)
