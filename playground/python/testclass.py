class foo:
    def __init__(self, x):
        self.x = x


class bar(foo):
    pass


class int:
    pass


class baz(int, bar):
    pass
