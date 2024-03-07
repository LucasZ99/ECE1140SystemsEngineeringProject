from Track_Model import TrackModel
import numpy as np

t = TrackModel('Blue Line.xlsx')
data = t.get_data()
infrastructure = data[:, 9]
print(infrastructure)
temp_segment = np.array([])
segments = np.array([])
for i in range(0, len(infrastructure)):
    if 'Switch' in infrastructure[i]:


