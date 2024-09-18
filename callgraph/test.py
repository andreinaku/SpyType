import ast


code = '''
class TypeName:
    def __init__(self, tname: str):
        self.tname = tname

    def __str__(self):
        return self.tname
    
    def __repr__(self):
        return self.__str__()

        
a = 3
b = TypeName('salut')
'''

tree = ast.parse(code)
print(ast.dump(tree, indent=4))
