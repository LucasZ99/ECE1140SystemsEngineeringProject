class Switch(object):
    def __init__(self, block: int, pos_a: int, pos_b: int, current_pos: int):
        super(Switch, self).__init__()

        self.block = block
        self.pos_a = pos_a
        self.pos_b = pos_b
        self.current_pos = current_pos

        '''a switch consists of the block it sits on, the two it connects,
        and its current position '''
        if current_pos == pos_a or current_pos == pos_b:
            self.switch = [block, pos_a, pos_b, current_pos]

        else:
            raise ValueError('current_post must be either pos_a or pos_b')

    def toggle(self):
        if self.current_pos == self.pos_a:
            self.current_pos = self.pos_b
        else:
            self.current_pos = self.pos_a

    def to_tuple(self):
        if self.current_pos == self.pos_a:
            return self.block, False
        else:
            return self.block, True

    def __str__(self):
        return str(f'Switch at block {self.block} -> {self.current_pos}')
