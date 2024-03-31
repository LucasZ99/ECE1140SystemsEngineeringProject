from Track_Controller_SW import Switch


class Light:
    def __init__(self, block: int, val: bool):
        self.block = block
        self.val = val

    def toggle(self):
        self.val = not self.val
