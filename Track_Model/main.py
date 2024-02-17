from Track_Model import TrackModel

t = TrackModel('Blue Line.xlsx')
print(t.get_data())
print()
print(t.get_section('A'))
print()
print(t.get_section('B', 'C'))
