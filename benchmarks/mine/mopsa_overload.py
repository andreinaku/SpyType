class newstr:
    def __init__(self, a):
        self.a = a

    def __rshift__(self, x):
        return self.a * x
        

def f(a, b):
    return a >> b


x = newstr('a')
y = f(x, 3)
print(y)
