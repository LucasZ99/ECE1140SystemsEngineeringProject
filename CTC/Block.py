from Track_Controller_SW import Switch


class Block:
    def __init__(self, line: str, id: str, station_name: str, railroad_crossing: bool, switch: Switch | None,
                 length_m: float, speed_limit_kph: float):
        self.line = line
        self.id = id
        self.occupied = False

    def __str__(self):
        s = ""
        s += self.line + ", " + self.id + ", " + (
            self.station_name if len(self.station_name) > 0 else "None") + ", " + str(
            self.railroad_crossing) + ", " + str(self.speed_limit_kph) + ", " + str(self.length_m)
        return s
