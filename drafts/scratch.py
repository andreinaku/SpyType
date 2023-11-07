import ast
import astor
from pyiparser import specs_shed as ss
from copy import deepcopy


# tree = ast.parse('''
# def foo(a, b, /, c, *d, e, f, **g):
#   return True
# foo(1,2,3,4,5,6,7,e=8,f=9,x=10,y=11,z=12,k=13)
# ''')
tree = ast.parse("a.f().g().h()")
print(ast.dump(tree, indent=4))

callnode = tree.body[0].value


def search_func_spec(funcname):
    print(funcname)
    for classname, funcdict in ss.funcspecs.items():
        for funcname, speclist in funcdict.items():
            print(f'found the spec in class {classname}: {speclist}')
            return funcdict[funcname]


def transform_node(node):
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            return deepcopy(node)
        elif isinstance(node.func, ast.Attribute):
            newnode = ast.Call()
            newnode.keywords = deepcopy(node.keywords)
            newnode.args = deepcopy(node.args)
            newnode.func = ast.Name(id=node.func.attr, ctx=ast.Load())
            newnode.args.insert(0, transform_node(node.func.value))
            return newnode
        else:
            raise RuntimeError('aaa')
    elif isinstance(node, ast.Name):
        return deepcopy(node)
    elif isinstance(node, ast.Attribute):
        newnode = ast.Attribute()
        newnode.attr = deepcopy(node.attr)
        newnode.ctx = deepcopy(node.ctx)
        newnode.value = transform_node(node.value)
        return newnode


class CallVisit(ast.NodeVisitor):
    def visit_Call(self, node):
        for arg in node.args:
            self.visit(arg)
        print(f'call {astor.to_source(node).strip()}')

# aux = f(callnode)
# print(aux)
# search_func_spec('pow')
# tree = ast.parse('a.f(x)')
# tree = ast.parse('a(y).f(x)')
tree = ast.parse('a.g(y).b.f(x)')
# tree = ast.parse('foo.a(x).bar.b(y).c(z).f(k)')
callnode = tree.body[0].value
aux = transform_node(callnode)
f = CallVisit()
f.visit(aux)
pass