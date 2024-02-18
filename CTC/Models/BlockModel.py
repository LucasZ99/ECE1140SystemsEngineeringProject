class BlockModel():
    def __init__(self, line:str, id:str, station_name:str | None, railroad_crossing:bool, switch_dest:list[str] | None, length_m:float, speed_limit_kph:float):
        self.line = line
        self.id = id
        self.station_name = station_name
        self.railroad_crossing = railroad_crossing
        self.length_m = length_m
        self.speed_limit_kph = speed_limit_kph
        self.switch_dest = switch_dest
