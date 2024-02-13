from Track_Model import TrackModel
import numpy as np

t = TrackModel('Blue Line.xlsx')
print(t.get_data())
data = t.get_data()
el = data[0, 6]
print(el)
print(np.isnan(el))

print(t.get_line_name())
print(t.get_num_blocks())
