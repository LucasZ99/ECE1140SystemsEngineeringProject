import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel


class Map(QMainWindow):

    def __init__(self):
        super(Map, self).__init__()
        self.setWindowTitle('map')

        label = QLabel(self)
        pixmap = QPixmap('map_picture.PNG')
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.setFixedSize(800, 600)


app = QApplication(sys.argv)
w = Map()
w.show()
sys.exit(app.exec())
