from Track_Model import TrackModel
import numpy as np

t = TrackModel('Blue Line.xlsx')
print(t.get_data())
t.set_block_occupancy(5, 1)
print(t.get_data())

