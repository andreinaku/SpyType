class A:
    def __init__(self):
        self.val = 0

    def update(self, x):
        self.val = x

x = A()
z1 = x.val
y = x
y.update('a')
z2 = x.val
