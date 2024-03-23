class TestClass:
    x = int()

    def __init__(self):
        self.x = 0


x = TestClass()
y = TestClass()
z = TestClass()

x.x = 1
y = x
print(y.x)

y = z
z.x = 2
print(y.x)