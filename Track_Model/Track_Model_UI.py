import os

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QTableWidget, QGroupBox, QVBoxLayout,
    QTableWidget, QLabel, QSlider, QComboBox, QFileDialog, QTableView, QTableWidgetItem, QMainWindow,
    QFrame, QHeaderView, QAbstractScrollArea
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from Animated_Toggle import AnimatedToggle
import sys
from Track_Model import TrackModel
from dynamic_map import DynamicMap


##############################
# Main Window
##############################
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Backend
        self.file_name = self.getFileName()
        self.track_model = TrackModel(self.file_name)
        # Window Layout
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setWindowTitle("Track Model")
        self.setContentsMargins(20, 20, 20, 20)
        self.resize(1920//2, 1080//2)
        layout = QGridLayout()

        # Style
        self.setStyleSheet("""
            QMainWindow{
                background-color: #d9d9d9;
            }
            QGroupBox {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #d9d9d9, stop: 1 #FFFFFF);
                border: 2px solid black;
                border-radius: 5px;
                margin-top: 5ex; /* leave space at the top for the title */
            }  

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left; /* position at the top center */
                padding: 0 3px;
            }
            
            QTableWidget {
                font: 12px;
                gridline-color: black;
            }
            
            QHeaderView {
                font: 12px;
            }
            
            QHeaderView::section {
                font: 12px;
                border: 1px solid black;
            }

        """)
        # 3x5 grid
        #     0   1   2   3   4
        #  0 [s] [s] [m] [m] [m]
        #  1 [s] [s] [m] [m] [m]
        #  2 [s] [s] [f] [t] [u]

        # s = (0, 0, 3, 2)
        # m = (0, 2, 2, 3)
        # f = (2, 2, 1, 1)
        # t = (2, 3, 1, 1)
        # u = (2, 4, 1, 1)

        # Selected Section
        self.selected_section = 'A'
        self.selected_section_group = QGroupBox(f"Selected Section (Section {self.selected_section})")

        ss_group_layout = QVBoxLayout()

        self.table1 = QTableWidget()
        self.table1.setAlternatingRowColors(True)
        self.table1_data = self.track_model.get_block_table(self.selected_section)

        m, n = self.table1_data.shape
        self.table1.setRowCount(m-1)
        self.table1.setColumnCount(7)
        self.table1.setHorizontalHeaderLabels(self.table1_data[0, :])
        self.table1.verticalHeader().setVisible(False)

        for i in range(1, m):
            for j in range(0, n):
                self.table1.setItem(i-1, j, QTableWidgetItem(str(self.table1_data[i, j])))
        ss_group_layout.addWidget(self.table1)

        # This more or less adjusts table size to valid width, but we want cell width to decrease
        # self.table1.setVisible(False)
        # self.table1.verticalScrollBar().setValue(0)
        # self.table1.resizeColumnsToContents()
        # self.table1.setVisible(True)
        # width = self.table1.verticalHeader().width()
        # width += self.table1.horizontalHeader().length()
        # if self.table1.verticalScrollBar().isVisible():
        #     width += self.table1.verticalScrollBar().width()
        # width += self.table1.frameWidth() * 2
        # self.table1.setFixedWidth(width)

        self.table2 = QTableWidget()
        self.table2.setAlternatingRowColors(True)
        self.table2_data = self.track_model.get_station_table(self.selected_section)

        m, n = self.table2_data.shape
        self.table2.setRowCount(m)
        self.table2.setColumnCount(7)
        self.table2.setHorizontalHeaderLabels(['Station', 'Block', 'Side', 'Heaters',
                                               'Embarking', 'Disembarking', 'Ticket Sales'])
        self.table2.verticalHeader().setVisible(False)
        for i in range(0, m):
            for j in range(0, n):
                self.table2.setItem(i, j, QTableWidgetItem(str(self.table2_data[i, j])))
        ss_group_layout.addWidget(self.table2)

        self.table3 = QTableWidget()
        self.table3.setAlternatingRowColors(True)
        self.table3_data = self.track_model.get_infrastructure_table(self.selected_section)

        m, n = self.table3_data.shape
        self.table3.setRowCount(m)
        self.table3.setColumnCount(3)
        self.table3.setHorizontalHeaderLabels(['Infrastructure', 'Block', 'Value'])
        self.table3.verticalHeader().setVisible(False)
        for i in range(0, m):
            for j in range(0, n):
                self.table3.setItem(i, j, QTableWidgetItem(str(self.table3_data[i, j])))
        ss_group_layout.addWidget(self.table3)

        self.selected_section_group.setLayout(ss_group_layout)
        layout.addWidget(self.selected_section_group, 0, 0, 3, 2)

        # Failure Modes
        self.failure_modes_group = QGroupBox("Failure Modes")

        fm_group_layout = QGridLayout()

        f1_title = QLabel()
        f1_title.setText("Power Failure:")
        f2_title = QLabel()
        f2_title.setText("Track Circuit Failure:")
        f3_title = QLabel()
        f3_title.setText("Broken Rail Failure:")
        fm_group_layout.addWidget(f1_title, 0, 0)
        fm_group_layout.addWidget(f2_title, 1, 0)
        fm_group_layout.addWidget(f3_title, 2, 0)

        self.str_list_blocks = list(self.table1_data[1:, 0].astype(str))
        self.combo1 = QComboBox()
        self.combo1.addItems(self.str_list_blocks)
        self.combo1.activated.connect(self.combo1_new_item_selected)

        self.combo2 = QComboBox()
        self.combo2.addItems(self.str_list_blocks)
        self.combo2.activated.connect(self.combo2_new_item_selected)

        self.combo3 = QComboBox()
        self.combo3.addItems(self.str_list_blocks)
        self.combo3.activated.connect(self.combo3_new_item_selected)

        self.combo1.setFixedSize(50, 25)
        self.combo2.setFixedSize(50, 25)
        self.combo3.setFixedSize(50, 25)

        fm_group_layout.addWidget(self.combo1, 0, 1)
        fm_group_layout.addWidget(self.combo2, 1, 1)
        fm_group_layout.addWidget(self.combo3, 2, 1)

        self.toggle1 = AnimatedToggle()
        self.toggle1.setFixedSize(self.toggle1.sizeHint())
        self.toggle1.clicked.connect(self.toggle1_clicked)

        self.toggle2 = AnimatedToggle()
        self.toggle2.setFixedSize(self.toggle2.sizeHint())
        self.toggle2.clicked.connect(self.toggle2_clicked)

        self.toggle3 = AnimatedToggle()
        self.toggle3.setFixedSize(self.toggle3.sizeHint())
        self.toggle3.clicked.connect(self.toggle3_clicked)

        fm_group_layout.addWidget(self.toggle1, 0, 2)
        fm_group_layout.addWidget(self.toggle2, 1, 2)
        fm_group_layout.addWidget(self.toggle3, 2, 2)

        self.failure_modes_group.setLayout(fm_group_layout)
        layout.addWidget(self.failure_modes_group, 2, 2, 1, 1)

        # Temperature Controls
        self.temperature_controls_group = QGroupBox("Temperature Controls")
        tc_layout = QVBoxLayout()

        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setGeometry(50, 50, 100, 50)  # this isn't doing anything rn
        slider.setMinimum(-40)
        slider.setMaximum(120)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(5)
        slider.setValue(74)
        slider.valueChanged.connect(self.display_slider_value)
        tc_layout.addWidget(slider)

        self.slider_label = QLabel(self)
        tc_layout.addWidget(self.slider_label)
        self.slider_label.setText("Environmental Temperature:\n74 °F")

        self.temperature_controls_group.setLayout(tc_layout)
        layout.addWidget(self.temperature_controls_group, 2, 3, 1, 1)

        # Map
        self.map_group = QGroupBox("Map")
        map_layout = QVBoxLayout()

        self.dynamic_map = DynamicMap()
        self.dynamic_map.button_a.clicked.connect(self.button_a_clicked)
        self.dynamic_map.button_b.clicked.connect(self.button_b_clicked)
        self.dynamic_map.button_c.clicked.connect(self.button_c_clicked)
        map_layout.addWidget(self.dynamic_map)

        self.map_group.setLayout(map_layout)
        layout.addWidget(self.map_group, 0, 2, 2, 3)

        # Upload Button
        self.upload_layout_group = QGroupBox("Upload Track Layout")
        ul_layout = QVBoxLayout()

        upload_layout_button = QPushButton("Browse Files")
        upload_layout_button.clicked.connect(self.getFileName)
        ul_layout.addWidget(upload_layout_button)

        self.current_file_label = QLabel('Reading from\n"' + self.file_name.split('/')[-1] + '"')
        ul_layout.addWidget(self.current_file_label)

        self.upload_layout_group.setLayout(ul_layout)
        layout.addWidget(self.upload_layout_group, 2, 4, 1, 1)

        # center widget
        center_widget = QWidget()
        center_widget.setLayout(layout)
        self.setCentralWidget(center_widget)

    ##############################
    # Event Handlers
    ##############################
    def display_slider_value(self):
        self.slider_label.setText("Environmental Temperature:\n" + str(self.sender().value()) + "°F")
        # self.slider_label.adjustSize()  # Expands label size as numbers get larger
        self.track_model.set_env_temperature(self.sender().value())
        if self.sender().value() <= 32:  # could check current heater value, but no need
            self.track_model.set_heaters(1)  # we do not use bool b/c we need NaN value for non-heater blocks
        else:
            self.track_model.set_heaters(0)
        self.section_refresh()  # we could write a new function for only refreshing tables 1&3, but no need

    def getFileName(self):
        # file browser dialog
        file_filter = 'Data File (*.xlsx);; Excel File (*.xlsx, *.xls)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select Track Layout File',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Data File (*.xlsx)'
        )
        # Set file_name and change label
        self.file_name = response[0]
        if hasattr(self, 'current_file_label'):
            self.current_file_label.setText('Reading from\n"' + self.file_name.split('/')[-1] + '"')

        # Update track_model
        self.track_model = TrackModel(self.file_name)

        # TODO: Make a refresh everything (or reset everything) function and put it here
        # return our new file name
        return self.file_name

    def button_a_clicked(self):
        self.selected_section = 'A'
        self.section_refresh()

    def button_b_clicked(self):
        self.selected_section = 'B'
        self.section_refresh()

    def button_c_clicked(self):
        self.selected_section = 'C'
        self.section_refresh()

    def combo1_new_item_selected(self):
        # sets the value of the toggle based on the value from our data
        block = int(self.combo1.currentText())
        print(self.track_model.get_data()[block, 13])
        self.toggle1.setChecked(self.track_model.get_data()[block, 13])

    def toggle1_clicked(self):
        block = int(self.combo1.currentText())
        val = int(self.toggle1.isChecked())
        self.track_model.set_power_failure(block, val)
        self.data_and_tables_refresh()

    def combo2_new_item_selected(self):
        # sets the value of the toggle based on the value from our data
        block = int(self.combo2.currentText())
        self.toggle2.setChecked(self.track_model.get_data()[block, 14])

    def toggle2_clicked(self):
        block = int(self.combo2.currentText())
        val = int(self.toggle2.isChecked())
        self.track_model.set_track_circuit_failure(block, val)
        self.data_and_tables_refresh()

    def combo3_new_item_selected(self):
        # sets the value of the toggle based on the value from our data
        block = int(self.combo3.currentText())
        self.toggle3.setChecked(self.track_model.get_data()[block, 15])

    def toggle3_clicked(self):
        block = int(self.combo3.currentText())
        val = int(self.toggle3.isChecked())
        self.track_model.set_broken_rail_failure(block, val)
        self.data_and_tables_refresh()

    def data_and_tables_refresh(self):
        # data
        self.table1_data = self.track_model.get_block_table(self.selected_section)
        self.table2_data = self.track_model.get_station_table(self.selected_section)
        self.table3_data = self.track_model.get_infrastructure_table(self.selected_section)
        # table1
        m, n = self.table1_data.shape
        self.table1.setRowCount(m - 1)
        self.table1.verticalHeader().setVisible(False)
        for i in range(1, m):
            for j in range(0, n):
                self.table1.setItem(i - 1, j, QTableWidgetItem(str(self.table1_data[i, j])))
        # table2
        m, n = self.table2_data.shape
        self.table2.setRowCount(m)
        for i in range(0, m):
            for j in range(0, n):
                self.table2.setItem(i, j, QTableWidgetItem(str(self.table2_data[i, j])))
        # table3
        m, n = self.table3_data.shape
        self.table3.setRowCount(m)
        self.table3.setColumnCount(3)
        for i in range(0, m):
            for j in range(0, n):
                self.table3.setItem(i, j, QTableWidgetItem(str(self.table3_data[i, j])))

    def section_refresh(self):
        # data
        self.table1_data = self.track_model.get_block_table(self.selected_section)
        self.table2_data = self.track_model.get_station_table(self.selected_section)
        self.table3_data = self.track_model.get_infrastructure_table(self.selected_section)
        # table1
        m, n = self.table1_data.shape
        self.table1.setRowCount(m - 1)
        self.table1.verticalHeader().setVisible(False)
        for i in range(1, m):
            for j in range(0, n):
                self.table1.setItem(i - 1, j, QTableWidgetItem(str(self.table1_data[i, j])))
        # table2
        m, n = self.table2_data.shape
        self.table2.setRowCount(m)
        for i in range(0, m):
            for j in range(0, n):
                self.table2.setItem(i, j, QTableWidgetItem(str(self.table2_data[i, j])))
        # table3
        m, n = self.table3_data.shape
        self.table3.setRowCount(m)
        self.table3.setColumnCount(3)
        for i in range(0, m):
            for j in range(0, n):
                self.table3.setItem(i, j, QTableWidgetItem(str(self.table3_data[i, j])))

        # failure drop-downs
        self.str_list_blocks = list(self.table1_data[1:, 0].astype(str))
        self.combo1.clear()
        self.combo2.clear()
        self.combo3.clear()
        self.combo1.addItems(self.str_list_blocks)
        self.combo2.addItems(self.str_list_blocks)
        self.combo3.addItems(self.str_list_blocks)


##############################
# Run app
##############################

# app = QApplication(sys.argv)
# window = Window()
# window.show()
# sys.exit(app.exec())
