class foo:
    def __init__(self, x):
        self.x = x

    def bar(self):
        self.y = 42
        return self.x + self.y

    def baz(self):
        return self.bar()


