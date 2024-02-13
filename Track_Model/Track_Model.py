import pandas as pd


class TrackModel:
    def __init__(self, file_name):
        d = pd.read_excel(file_name)
        self.data = d.to_numpy()
        self.line_name = self.data[0, 0]
        self.num_blocks = len(self.data)

    def get_data(self):
        return self.data

    def get_line_name(self):
        return self.line_name

    def get_num_blocks(self):
        return self.num_blocks

