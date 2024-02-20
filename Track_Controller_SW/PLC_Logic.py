from PyQt6.QtCore import QObject


class ParsePlc(QObject):
    def __init__(self):
        super().__init__()
        self.filepath = None

    def set_filepath(self, filepath)
        self.filepath = filepath
        print(f"filepath: {self.filepath}")
