class Block:
    def __init__(self, block_name: str, block_length: float, block_speed_limit: float):
        self.name = block_name
        self.length = block_length
        self.speed_limit = block_speed_limit

    def id(self):
        return self.name[1:]
