import sys
from PyQt6.QtGui import QPixmap, QPainter
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

        background = QLabel(self)
        pixmap = QPixmap(map_file)
        pixmap = pixmap.scaled(400, 600, Qt.AspectRatioMode.KeepAspectRatio)
        background.setPixmap(pixmap)

        self.train_pixmap = QPixmap(yellow_box_file)
        self.train_pixmap = self.train_pixmap.scaled(10, 10, Qt.AspectRatioMode.KeepAspectRatio)

        self.green_light_pixmap = QPixmap(green_light_file)
        # self.green_light_pixmap = self.green_light_pixmap.scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio)

        self.red_light_pixmap = QPixmap(red_light_file)
        # self.red_light_pixmap = self.red_light_pixmap.scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio)

        self.rxr_unactivated_pixmap = QPixmap(rxr_unactivated_file)
        self.rxr_unactivated_pixmap = self.rxr_unactivated_pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)

        self.rxr_activated_pixmap = QPixmap(rxr_activated_file)
        self.rxr_activated_pixmap = self.rxr_activated_pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)

        self.warning_pixmap = QPixmap(warning_file)
        self.warning_pixmap = self.warning_pixmap.scaled(15, 15, Qt.AspectRatioMode.KeepAspectRatio)

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
            54: (280, 218), 55: (290, 218), 56: (300, 218), 57: (300, 218),
            # Skipping '58' to '62'
            # k
            63: (354, 250), 64: (354, 288), 65: (354, 326), 66: (354, 364), 67: (354, 380), 68: (354, 400),
            # l
            69: (354, 425), 70: (354, 450), 71: (345, 480), 72: (330, 500), 73: (300, 515),
            # m
            74: (263, 515), 75: (226, 515), 76: (190, 515),
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

    # def test_pix_dict(self):
    #     for key in self.pixel_dict:
    #         self.train.move(list(self.pixel_dict[key])[0], list(self.pixel_dict[key])[1])

    def show_ui(self):
        self.show()
        # self.test_pix_dict()

    # def move_box(self, x, y):
    #     self.train.move(x, y)

    def get_pix_dict(self):
        return self.pixel_dict

    # def populate_map(self, train_dict):
    #     for key in train_dict:
    #         print(key)
    #         print(train_dict[key])
    #         block = train_dict[key]
    #         self.train = QLabel(self)
    #         self.train.setPixmap(self.train_pixmap)
    #         self.train.move(list(self.pixel_dict[block])[0], list(self.pixel_dict[block])[1])

    def add_train(self):
        print('map: add train called')
        train = QLabel(self)
        train.setPixmap(self.train_pixmap)
        train.move(354, 250)
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

    def add_failure(self, block):
        [x, y] = self.pixel_dict[block]
        failure = QLabel(self)
        failure.setPixmap(self.warning_pixmap)

        failure.move(x, y)
        failure.show()
        self.failure_dict[block] = failure

    def remove_failure(self, block):
        failure = self.failure_dict.pop(block, None)
        if failure:
            failure.deleteLater()
        else:
            print(f"No failure with ID {block} found")

# app = QApplication(sys.argv)/
# w = Map()
# w.add_train()
# w.add_train()
# w.move_train(1, 100)
# w.move_train(2, 86)
# w.add_failure(2, 100)
# w.show()
# sys.exit(app.exec())
