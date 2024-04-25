import sys
from PyQt6.QtGui import QPixmap, QPainter, QImage
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QVBoxLayout, QLayout, QGraphicsScene, \
    QGraphicsView, QHBoxLayout, QGraphicsItem
from PyQt6.QtCore import Qt
import time
import os


# class Train(QWidget):
#     def __init__(self, current_block, train_id):
#         super(Train, self).__init__()
#         self.current_block = QLabel(current_block)
#         self.train_id = QLabel(train_id)
#
#         self.box = QLabel()
#         pixmap = QPixmap('./yellow_box.png')
#         pixmap = pixmap.scaled(10, 10, Qt.AspectRatioMode.KeepAspectRatio)
#         self.box.setPixmap(pixmap)
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.box)
#         layout.addWidget(self.current_block)
#         layout.addWidget(self.train_id)
#         self.setLayout(layout)
#
#     def move(self, x, y):
#         self.box.move(x, y)
#         self.current_block.move(x, y)
#         self.train_id.move(x, y)

class Map(QWidget):
    def __init__(self):
        super(Map, self).__init__()

        self.setWindowTitle('map')
        self.setFixedSize(400, 600)

        dirname = os.path.dirname(__file__)
        map_file = os.path.join(dirname, 'map_3.png')
        yellow_box_file = os.path.join(dirname, 'yellow_box.png')
        green_light_file = os.path.join(dirname, 'greenlight.png')
        red_light_file = os.path.join(dirname, 'redlight.png')
        rxr_unactivated_file = os.path.join(dirname, 'rxr_unactivated.png')
        rxr_activated_file = os.path.join(dirname, 'rxr_activated.png')
        warning_file = os.path.join(dirname, 'warning.png')
        station_file = os.path.join(dirname, 'station.png')
        highlight_file = os.path.join(dirname, 'highlight.png')

        background = QLabel(self)
        pixmap = QPixmap(map_file)
        pixmap = pixmap.scaled(400, 600, Qt.AspectRatioMode.KeepAspectRatio)
        background.setPixmap(pixmap)

        # StyleSheet for transparent background
        self.setStyleSheet("""
        QWidget
{
    color: #b1b1b1;
    background-color: rgba(0, 0, 0, 0);
    selection-background-color:rgba(0, 0, 0, 0);
    selection-color: black;
    background-clip: border;
    border-image: none;
    border: 0px transparent black;
    outline: 0;
}
        """)

        self.train_pixmap = QPixmap(yellow_box_file)
        self.train_pixmap = self.train_pixmap.scaled(10, 10, Qt.AspectRatioMode.KeepAspectRatio)

        self.green_light_pixmap = QPixmap(green_light_file)

        self.red_light_pixmap = QPixmap(red_light_file)

        self.rxr_unactivated_pixmap = QPixmap(rxr_unactivated_file)
        self.rxr_unactivated_pixmap = self.rxr_unactivated_pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)

        self.rxr_activated_pixmap = QPixmap(rxr_activated_file)
        self.rxr_activated_pixmap = self.rxr_activated_pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)

        self.warning_pixmap = QPixmap(warning_file)
        self.warning_pixmap = self.warning_pixmap.scaled(15, 15, Qt.AspectRatioMode.KeepAspectRatio)

        self.station_pixmap = QPixmap(station_file)
        self.station_pixmap = self.station_pixmap.scaled(12, 12, Qt.AspectRatioMode.KeepAspectRatio)

        self.highlight_pixmap = QPixmap(highlight_file)


        # TODO:
        # self.view_box = QLabel()
        # self.view_box.move(100, 100)

        self.train_dict = {}
        self.train_id_counter = 0

        self.failure_dict = {}  # block, failure type

        self.rxr_19 = QLabel(self)
        self.rxr_19.setPixmap(self.rxr_unactivated_pixmap)
        self.rxr_19.move(30, 5)

        self.rxr_108 = QLabel(self)
        self.rxr_108.setPixmap(self.rxr_unactivated_pixmap)
        self.rxr_108.move(300, 425)

        self.signal_1 = QLabel(self)
        self.signal_1.setPixmap(self.red_light_pixmap)
        self.signal_1.move(138, 12)
        self.signal_12 = QLabel(self)
        self.signal_12.setPixmap(self.green_light_pixmap)
        self.signal_12.move(154, 20)

        self.signal_29 = QLabel(self)
        self.signal_29.setPixmap(self.green_light_pixmap)
        self.signal_29.move(55, 145)
        self.signal_150 = QLabel(self)
        self.signal_150.setPixmap(self.red_light_pixmap)
        self.signal_150.move(20, 130)

        self.signal_76 = QLabel(self)
        self.signal_76.setPixmap(self.green_light_pixmap)
        self.signal_76.move(170, 525)
        self.signal_101 = QLabel(self)
        self.signal_101.setPixmap(self.red_light_pixmap)
        self.signal_101.move(170, 490)

        self.signal_100 = QLabel(self)
        self.signal_100.setPixmap(self.red_light_pixmap)
        self.signal_100.move(80, 490)
        self.signal_86 = QLabel(self)
        self.signal_86.setPixmap(self.green_light_pixmap)
        self.signal_86.move(50, 528)

        self.pixel_dict = {
            # a
            1: (170, 16), 2: (182, 32), 3: (193, 45),
            # b
            4: (208, 52), 5: (223, 59), 6: (238, 66),
            # c
            7: (253, 58), 8: (268, 49), 9: (283, 40), 10: (250, 14), 11: (210, 6), 12: (162, 4),
            # d
            13: (140, 4), 14: (120, 4), 15: (100, 4), 16: (80, 4),
            # e
            17: (68, 7), 18: (56, 10), 19: (52, 20), 20: (48, 30),
            # f
            21: (48, 44), 22: (48, 58), 23: (48, 71), 24: (48, 85), 25: (48, 99), 26: (48, 113), 27: (48, 126),
            28: (48, 140),
            # g
            29: (48, 154), 30: (48, 168), 31: (48, 181), 32: (48, 195),
            # h
            33: (54, 205), 34: (62, 212), 35: (90, 218),
            # i
            36: (100, 218), 37: (110, 218), 38: (120, 218), 39: (130, 218), 40: (140, 218), 41: (150, 218),
            42: (160, 218), 43: (170, 218), 44: (180, 218), 45: (190, 218), 46: (200, 218), 47: (210, 218),
            48: (220, 218), 49: (230, 218), 50: (240, 218), 51: (250, 218), 52: (260, 218), 53: (270, 218),
            54: (280, 218), 55: (290, 218), 56: (300, 218), 57: (310, 218),

            # should never reach 58-62
            58: (320, 218), 59: (320, 218), 60: (320, 218), 61: (320, 218),

            # k
            62: (354, 225), 63: (354, 250), 64: (354, 288), 65: (354, 326), 66: (354, 364), 67: (354, 380), 68: (354, 400),
            # l
            69: (354, 425), 70: (354, 450), 71: (345, 480), 72: (330, 500), 73: (300, 515),
            # m
            74: (263, 515), 75: (226, 515), 76: (205, 515),
            # n
            77: (190, 515), 78: (175, 515), 79: (161, 515), 80: (146, 515), 81: (132, 515), 82: (117, 515),
            83: (102, 515), 84: (88, 515), 85: (73, 515),
            # o
            86: (55, 516), 87: (43, 515), 88: (25, 512),
            # p
            89: (9, 500), 90: (1, 480), 91: (4, 460), 92: (11, 443), 93: (25, 434), 94: (45, 443), 95: (54, 457),
            96: (60, 470), 97: (63, 480),
            # q
            98: (65, 490), 99: (68, 500), 100: (70, 510),
            # r
            101: (200, 495),
            # s
            102: (210, 484), 103: (230, 484), 104: (250, 484),
            # t
            105: (270, 484), 106: (288, 478), 107: (305, 469), 108: (318, 452), 109: (326, 435),
            # u
            110: (326, 419), 111: (326, 404), 112: (326, 388), 113: (326, 373), 114: (326, 357), 115: (326, 341),
            116: (326, 332),
            # v
            117: (326, 310), 118: (324, 290), 119: (318, 275), 120: (308, 263), 121: (290, 254),
            # w
            122: (275, 250), 123: (265, 247), 124: (255, 247), 125: (246, 247), 126: (236, 247), 127: (226, 247),
            128: (216, 247), 129: (207, 247), 130: (197, 247), 131: (187, 247), 132: (177, 247), 133: (168, 247),
            134: (158, 247), 135: (148, 247), 136: (138, 247), 137: (128, 247), 138: (119, 247), 139: (109, 247),
            140: (99, 247), 141: (89, 247), 142: (80, 247), 143: (70, 247),
            # x
            144: (60, 247), 145: (40, 244), 146: (28, 235),
            # y
            147: (20, 210), 148: (20, 190), 149: (20, 170),
            # z
            150: (33, 151)
        }

        # STATIONS
        # 2,
        self.station2 = QLabel(self)
        self.station2.setPixmap(self.station_pixmap)
        self.station2.move(self.pixel_dict[2][0], self.pixel_dict[2][1])
        # 9,
        self.station9 = QLabel(self)
        self.station9.setPixmap(self.station_pixmap)
        self.station9.move(self.pixel_dict[9][0], self.pixel_dict[9][1])
        # 16,
        self.station16 = QLabel(self)
        self.station16.setPixmap(self.station_pixmap)
        self.station16.move(self.pixel_dict[16][0], self.pixel_dict[16][1])
        # 22,
        self.station22 = QLabel(self)
        self.station22.setPixmap(self.station_pixmap)
        self.station22.move(self.pixel_dict[22][0], self.pixel_dict[22][1])
        # 31,
        self.station31 = QLabel(self)
        self.station31.setPixmap(self.station_pixmap)
        self.station31.move(self.pixel_dict[31][0], self.pixel_dict[31][1])
        # 39,
        self.station39 = QLabel(self)
        self.station39.setPixmap(self.station_pixmap)
        self.station39.move(self.pixel_dict[39][0], self.pixel_dict[39][1])
        # 48,
        self.station48 = QLabel(self)
        self.station48.setPixmap(self.station_pixmap)
        self.station48.move(self.pixel_dict[48][0], self.pixel_dict[48][1])
        # 57,
        self.station57 = QLabel(self)
        self.station57.setPixmap(self.station_pixmap)
        self.station57.move(self.pixel_dict[57][0], self.pixel_dict[57][1])
        # 65,
        self.station65 = QLabel(self)
        self.station65.setPixmap(self.station_pixmap)
        self.station65.move(self.pixel_dict[65][0], self.pixel_dict[65][1])
        # 73,
        self.station73 = QLabel(self)
        self.station73.setPixmap(self.station_pixmap)
        self.station73.move(self.pixel_dict[73][0], self.pixel_dict[73][1])
        # 77,
        self.station77 = QLabel(self)
        self.station77.setPixmap(self.station_pixmap)
        self.station77.move(self.pixel_dict[77][0], self.pixel_dict[77][1])
        # 88,
        self.station88 = QLabel(self)
        self.station88.setPixmap(self.station_pixmap)
        self.station88.move(self.pixel_dict[88][0], self.pixel_dict[88][1])
        # 96,
        self.station96 = QLabel(self)
        self.station96.setPixmap(self.station_pixmap)
        self.station96.move(self.pixel_dict[96][0], self.pixel_dict[96][1])
        # 105,
        self.station105 = QLabel(self)
        self.station105.setPixmap(self.station_pixmap)
        self.station105.move(self.pixel_dict[105][0], self.pixel_dict[105][1])
        # 114,
        self.station114 = QLabel(self)
        self.station114.setPixmap(self.station_pixmap)
        self.station114.move(self.pixel_dict[114][0], self.pixel_dict[114][1])
        # 123,
        self.station123 = QLabel(self)
        self.station123.setPixmap(self.station_pixmap)
        self.station123.move(self.pixel_dict[123][0], self.pixel_dict[123][1])
        # 132,
        self.station132 = QLabel(self)
        self.station132.setPixmap(self.station_pixmap)
        self.station132.move(self.pixel_dict[132][0], self.pixel_dict[132][1])
        # 141
        self.station141 = QLabel(self)
        self.station141.setPixmap(self.station_pixmap)
        self.station141.move(self.pixel_dict[141][0], self.pixel_dict[141][1])

        # VIEWFINDER
        self.view_finder = QLabel(self)
        self.view_finder.setPixmap(self.highlight_pixmap)
        self.view_finder.move(self.pixel_dict[1][0]-5, self.pixel_dict[1][1]-5)

    def show_ui(self):
        self.show()
        # self.test_pix_dict()

    # def move_box(self, x, y):
    #     self.train.move(x, y)

    def get_pix_dict(self):
        return self.pixel_dict

    def move_view_finder(self, block):
        self.view_finder.move(self.pixel_dict[block][0]-5, self.pixel_dict[block][1]-5)

    def add_train(self):
        print('map: add train called')
        train = QLabel(self)
        train.setPixmap(self.train_pixmap)
        train.move(354, 225)
        train.show()
        self.train_id_counter += 1
        self.train_dict[self.train_id_counter] = train

    def move_train(self, train_id, block):
        print(f'map: move train called, train_id = {train_id}, block = {block}')
        if block != 58:
            [x, y] = self.pixel_dict[block]
            train = self.train_dict.get(train_id)
            if train:
                train.move(x, y)
            else:
                print(f"No train with ID {train_id} found")
        else:
            self.remove_train(train_id)

    def remove_train(self, train_id):
        train = self.train_dict.pop(train_id, None)
        if train:
            train.deleteLater()
        else:
            print(f"No train with ID {train_id} found")

    def set_rxr(self, rxr_index, value):
        print(f'map: set_rxr called w/ {rxr_index}, {value}')
        if rxr_index == 19:
            if value:
                self.rxr_19.setPixmap(self.rxr_activated_pixmap)
            else:
                self.rxr_19.setPixmap(self.rxr_unactivated_pixmap)
        elif rxr_index == 108:
            if value:
                self.rxr_108.setPixmap(self.rxr_activated_pixmap)
            else:
                self.rxr_108.setPixmap(self.rxr_unactivated_pixmap)
        else:
            print('map: invalid toggle_rxr index called')

    def set_signal(self, signal_index, value):  # 1, 12, 29, 150, 77, 101, 100, 86
        print(f'map: set_signal called w/ {signal_index}, {value}')
        if signal_index == 1:
            if value:
                self.signal_1.setPixmap(self.green_light_pixmap)
            else:
                self.signal_1.setPixmap(self.red_light_pixmap)
        elif signal_index == 12:
            if value:
                self.signal_12.setPixmap(self.green_light_pixmap)
            else:
                self.signal_12.setPixmap(self.red_light_pixmap)
        elif signal_index == 29:
            if value:
                self.signal_29.setPixmap(self.green_light_pixmap)
            else:
                self.signal_29.setPixmap(self.red_light_pixmap)
        elif signal_index == 150:
            if value:
                self.signal_150.setPixmap(self.green_light_pixmap)
            else:
                self.signal_150.setPixmap(self.red_light_pixmap)
        elif signal_index == 76:
            if value:
                self.signal_76.setPixmap(self.green_light_pixmap)
            else:
                self.signal_76.setPixmap(self.red_light_pixmap)
        elif signal_index == 101:
            if value:
                self.signal_101.setPixmap(self.green_light_pixmap)
            else:
                self.signal_101.setPixmap(self.red_light_pixmap)
        elif signal_index == 100:
            if value:
                self.signal_100.setPixmap(self.green_light_pixmap)
            else:
                self.signal_100.setPixmap(self.red_light_pixmap)
        elif signal_index == 86:
            if value:
                self.signal_86.setPixmap(self.green_light_pixmap)
            else:
                self.signal_86.setPixmap(self.red_light_pixmap)
        else:
            print(f'map: invalid toggle_signal index called: {signal_index}')

    def update_closure(self, block, val):
        if val:
            [x, y] = self.pixel_dict[block]
            failure = QLabel(self)
            failure.setPixmap(self.warning_pixmap)

            failure.move(x, y)
            failure.show()
            self.failure_dict[block] = failure
        else:
            failure = self.failure_dict.pop(block, None)
            if failure:
                failure.deleteLater()
            else:
                print(f"No failure with ID {block} found")

# app = QApplication(sys.argv)
# w = Map()
# w.show()
# sys.exit(app.exec())
