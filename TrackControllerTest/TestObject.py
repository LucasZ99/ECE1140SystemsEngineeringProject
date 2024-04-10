from PyQt6.QtCore import QObject


class TestObject(QObject):
    def __init__(self):
        super().__init__()