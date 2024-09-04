class foo:
    def __init__(self, x):
        self.x = x

    def bar(self, a):
        self.x += a

    def bar(self, a, b):
        self.x += a + b
    

qux = foo(10)
qux.bar(10)
print(qux.x)
qux.bar(10, 11)
print(qux.x)
