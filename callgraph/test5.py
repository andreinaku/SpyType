class bar:
    @staticmethod
    def lulu():
        return 42


class foo:
    def __init__(self, x):
        self.x = x

    def sum(self):
        return self.dif()

    def dif(self):
        return self.lali()

    def lali(self):
        return len('abc')

    def qux(self):
        return bar.lulu()
