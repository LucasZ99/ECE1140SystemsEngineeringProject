class Block:
    def __init__(self, block_name: str, block_length: float, block_speed_limit: float):
        self.name = block_name
        self.length = block_length
        self.speed_limit = block_speed_limit

    def id(self):
        return int(self.name[1:])

    def get_block_travel_time(self) -> float:
        """
        returns the travel time through a block in seconds
        """
        speed_limit_mps = self.speed_limit / 3.6

        travel_time = self.length / speed_limit_mps

        return travel_time
