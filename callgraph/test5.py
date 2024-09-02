def f():
    return 'what?'


class bar:
    @staticmethod
    def f():
        return 42


class foo:
    def __init__(self, x):
        self.x = x

    def f(self):
        return self.g()

    def g(self):
        return self.h()

    def h(self):
        return len('abc')

    def qux(self):
        return bar.f()


class grx(foo):
    def f2(self):
        pass

f()
