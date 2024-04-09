class TrackSignal:
    def __init__(self, block_id: int, authority: int, speed: float):
        self.block_id = block_id
        self.authority = authority
        self.speed = speed

    def zero_speed(self):
        self.speed = 0

    def to_tuple(self):
        return (self.block_id, self.authority, self.speed)

    def __str__(self):
        return f"Track Signal at Block ID: {self.block_id}, Authority: {self.authority}, Speed: {self.speed}"
