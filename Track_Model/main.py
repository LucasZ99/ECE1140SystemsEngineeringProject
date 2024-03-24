from PyQt6.QtWidgets import (
    QApplication
)
import sys
from Track_Model import TrackModel
from Track_Model_UI import Window
import pandas as pd
import numpy as np
import random


# t = TrackModel('Blue Line.xlsx')
# print(t.get_data()[:, -1])
# app = QApplication([])
# window = Window()
# window.show()
# app.exec()

d = pd.read_excel('Green Line.xlsx', header=None)  # We will also load our header row, and block IDs will map to index
data = d.to_numpy()

false_col = np.full((data.shape[0], 1), False, dtype=bool)
temp = np.full((data.shape[0], 1), 74, dtype=int)
new_data = np.hstack((data[:, 0:7], np.copy(false_col)))
new_data = np.hstack((new_data[:, 0:8], temp))
new_data = np.hstack((new_data, data[:, 7:]))
nan_array = np.full((data.shape[0], 1), np.nan, dtype=object)
new_data = np.hstack((new_data, nan_array))
new_data = np.hstack((new_data, np.copy(false_col)))
new_data = np.hstack((new_data, np.copy(false_col)))
new_data = np.hstack((new_data, np.copy(false_col)))
new_data = np.hstack((new_data, np.copy(nan_array)))
new_data = np.hstack((new_data, np.copy(nan_array)))
for i in range(0, new_data.shape[0]):
    if 'station' in str(new_data[i, 9]).lower():
        new_data[i, 12] = False
        new_data[i, 16] = 0
        new_data[i, 17] = 0
        if i != 0:
            new_data[i-1, 12] = False
        if i != new_data.shape[0]-2:
            new_data[i+1, 12] = False

new_data[0, 7] = 'Block Occupancy'
new_data[0, 8] = 'Temperature'
new_data[0, 12] = 'Heaters'
new_data[0, 13] = 'Power Failure'
new_data[0, 14] = 'Track Circuit Failure'
new_data[0, 15] = 'Broken Rail Failure'
new_data[0, 16] = 'Ticket Sales'
new_data[0, 17] = 'Embarking'

data = new_data
print(data)
# Convert the NumPy array to a pandas DataFrame
df = pd.DataFrame(data)

# Define the filename for the Excel file
excel_filename = "testing_output.xlsx"

# Export the DataFrame to an Excel file
df.to_excel(excel_filename, index=False, header=False)  # index=False, header=False to exclude row and column labels

print("Array data has been exported to:", excel_filename)
