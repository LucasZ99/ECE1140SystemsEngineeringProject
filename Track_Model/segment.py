from Track_Model import TrackModel
import numpy as np

# will divide our track layout into segments based on switch positions
# and then connect to make map, maybe linked list implementation

t = TrackModel('Blue Line.xlsx')
data = t.get_data()
infrastructure = data[:, 9]
print(infrastructure)
temp_segment = np.array([])
segments = np.array([])
for i in range(0, len(infrastructure)):
    if 'Switch' in infrastructure[i]:
        pass


