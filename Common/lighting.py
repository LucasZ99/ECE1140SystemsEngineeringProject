class Light:
    def __init__(self, block: int, val: bool):
        self.block = block
        self.val = val

    def to_tuple(self):
        return (self.block, self.val)

    def toggle(self):
        self.val = not self.val

    def __str__(self):
        return f'light at {self.block} is {self.val}'
