import ast


class ClassMethodNames(ast.NodeVisitor):
    def __init__(self, class_ast: ast.AST):
        self.class_ast = class_ast
        self.method_names = set()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.method_names.add(node.name)
    
    def get_names(self) -> set[str]:
        self.visit(self.class_ast)
        return self.method_names
    

class ClassAttributeNames(ast.NodeVisitor):
    def __init__(self, class_ast: ast.AST):
        self.class_ast = class_ast
        self.attr_names = set()
        self.func_names = ClassMethodNames(self.class_ast).get_names()

    def visit_Attribute(self, node: ast.Attribute):
        if isinstance(node.value, ast.Name) and node.value.id == 'self':
            if node.attr not in self.func_names:
                self.attr_names.add(node.attr)
    
    def get_names(self) -> set[str]:
        self.visit(self.class_ast)
        return self.attr_names
    

if __name__ == "__main__":
    code = '''
class Direction:
    def __init__(self, dx, dy, letter):
        self.dx, self.dy, self.letter = dx, dy, letter

    def f(self):
        return "a"

    def g(self):
        return self.f()        
'''
    tree = ast.parse(code)
    print(ClassAttributeNames(tree).get_names())
