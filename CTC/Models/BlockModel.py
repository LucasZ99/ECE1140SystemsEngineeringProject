from Track_Controller_SW import Switch

class BlockModel:
    def __init__(self, line:str, id:str, station_name:str, railroad_crossing:bool, switch:Switch | None, length_m:float, speed_limit_kph:float):
        self.line = line
        self.id = id
        self.station_name = station_name
        self.railroad_crossing = railroad_crossing
        self.length_m = length_m
        self.speed_limit_kph = speed_limit_kph
        self.switch = switch
        self.occupied = False

    def __str__(self):
        s = ""
        s += self.line + ", " + self.id + ", " + (self.station_name if len(self.station_name) > 0 else "None") + ", " + str(self.railroad_crossing) + ", " + (str(self.switch_dest) if len(self.switch_dest) > 0 else "None") + ", " + str(self.speed_limit_kph) + ", " + str(self.length_m)
        return s