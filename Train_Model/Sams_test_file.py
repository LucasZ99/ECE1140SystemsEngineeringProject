class Testee:
    x = 0

    def set_x(self, y):
        self.x = y

    def get_x(self):
        return self.x


class Tester:
    y = Testee()

    def set_y(self, x):
        self.y = x

    def get_y(self):
        return self.y

    def print_y(self):
        print(self.y.get_x())

    def change_y(self, x):
        self.y.set_x(x)


tester1 = Tester()
tester2 = Tester()
testee1 = Testee()
testee2 = Testee()

tester1.set_y(testee1)
tester1.change_y(2)
tau = tester1.get_y()
tau = testee2


tester1.print_y()
