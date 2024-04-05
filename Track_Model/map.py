import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QVBoxLayout, QLayout
from PyQt6.QtCore import Qt
import time

class Train:
    def __init__(self, current_block, train_id):
        super(self).__init__()
        self.current_block = current_block
        self.train_id = train_id

        self.train = QLabel(self)
        pixmap = QPixmap('yellow_box.png')
        pixmap = pixmap.scaled(10, 10, Qt.AspectRatioMode.KeepAspectRatio)
        self.train.setPixmap(pixmap)
        self.train.move(0, 0)


class Map(QWidget):
    def __init__(self):
        super(Map, self).__init__()
        self.setWindowTitle('map')
        self.setFixedSize(400, 600)

        background = QLabel(self)
        pixmap = QPixmap('map_3.png')
        pixmap = pixmap.scaled(400, 600, Qt.AspectRatioMode.KeepAspectRatio)
        background.setPixmap(pixmap)

        self.centerWidget = background

        self.train = QLabel(self)
        pixmap = QPixmap('yellow_box.png')
        pixmap = pixmap.scaled(10, 10, Qt.AspectRatioMode.KeepAspectRatio)
        self.train.setPixmap(pixmap)
        self.train.move(0, 0)

        # self.train = QLabel(self)
        # pixmap = QPixmap('yellow_box.png')
        # pixmap = pixmap.scaled(10, 10, Qt.AspectRatioMode.KeepAspectRatio)
        # self.train.setPixmap(pixmap)
        # self.train.move(45, 443)
        #
        # self.train = QLabel(self)
        # pixmap = QPixmap('yellow_box.png')
        # pixmap = pixmap.scaled(10, 10, Qt.AspectRatioMode.KeepAspectRatio)
        # self.train.setPixmap(pixmap)
        # self.train.move(60, 470)

        self.pixel_dict = {
            # a
            '1': (170, 16), '2': (182, 32), '3': (193, 45),
            # b
            '4': (208, 52), '5': (223, 59), '6': (238, 66),
            # c
            '7': (253, 58), '8': (268, 49), '9': (283, 40), '10': (250, 14), '11': (210, 6), '12': (162, 4),
            # d
            '13': (140, 4), '14': (120, 4), '15': (100, 4), '16': (80, 4),
            # e
            '17': (68, 7), '18': (56, 10), '19': (52, 20), '20': (48, 30),
            # f
            '21': (48, 44), '22': (48, 58), '23': (48, 71), '24': (48, 85), '25': (48, 99), '26': (48, 113), '27': (48, 126), '28': (48, 140),
            # g
            '29': (48, 154), '30': (48, 168), '31': (48, 181), '32': (48, 195),
            # h
            '33': (54, 205), '34': (62, 212), '35': (90, 218),
            # i
            '36': (100, 218), '37': (110, 218), '38': (120, 218), '39': (130, 218), '40': (140, 218), '41': (150, 218), '42': (160, 218), '43': (170, 218), '44': (180, 218), '45': (190, 218), '46': (200, 218), '47': (210, 218), '48': (220, 218), '49': (230, 218), '50': (240, 218), '51': (250, 218), '52': (260, 218), '53': (270, 218), '54': (280, 218), '55': (290, 218), '56': (300, 218), '57': (300, 218),
            # Skipping '58' to '62'
            # k
            '63': (354, 250), '64': (354, 288), '65': (354, 326), '66': (354, 364), '67': (354, 380), '68': (354, 400),
            # l
            '69': (354, 425), '70': (354, 450), '71': (345, 480), '72': (330, 500), '73': (300, 515),
            # m
            '74': (263, 515), '75': (226, 515), '76': (190, 515),
            # n
            '77': (190, 515), '78': (175, 515), '79': (161, 515), '80': (146, 515), '81': (132, 515), '82': (117, 515), '83': (102, 515), '84': (88, 515), '85': (73, 515),
            # o
            '86': (55, 516), '87': (43, 515), '88': (25, 512),
            # p
            '89': (9, 500), '90': (1, 480), '91': (4, 460), '92': (11, 443), '93': (25, 434), '94': (45, 443), '95': (54, 457), '96': (60, 470), '97': (53, 453),
            # q
            '98': (0, 0), '99': (0, 0), '100': (0, 0),
            # r
            '101': (200, 495),
            # s
            '102': (210, 484), '103': (230, 484), '104': (250, 484),
            # t
            '105': (270, 484), '106': (288, 478), '107': (305, 469), '108': (318, 452), '109': (326, 435),
            # u
            '110': (326, 419), '111': (326, 404), '112': (326, 388), '113': (326, 373), '114': (326, 357), '115': (326, 341), '116': (326, 332),
            # v
            '117': (326, 310), '118': (324, 290), '119': (318, 275), '120': (308, 263), '121': (290, 254),
            # w
            '122': (275, 250), '123': (265, 247), '124': (255, 247), '125': (246, 247), '126': (236, 247), '127': (226, 247), '128': (216, 247), '129': (207, 247), '130': (197, 247), '131': (187, 247), '132': (177, 247), '133': (168, 247), '134': (158, 247), '135': (148, 247), '136': (138, 247), '137': (128, 247), '138': (119, 247), '139': (109, 247), '140': (99, 247), '141': (89, 247), '142': (80, 247), '143': (70, 247),
            # x
            '144': (60, 247), '145': (40, 244), '146': (28, 235),
            # y
            '147': (20, 210), '148': (20, 190), '149': (20, 170),
            # z
            '150': (33, 151)
        }

    def test_pix_dict(self):
        for key in self.pixel_dict:
            self.train.move(list(self.pixel_dict[key])[0], list(self.pixel_dict[key])[1])

    def show_ui(self):
        self.show()
        # self.test_pix_dict()

    def move_box(self, x, y):
        self.train.move(x, y)

    def get_pix_dict(self):
        return self.pixel_dict

# 33 95-100
# app = QApplication(sys.argv)
# w = Map()
# w.show()
# sys.exit(app.exec())
