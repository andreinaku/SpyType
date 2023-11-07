import ast
import astor


# tree = ast.parse('''
# def foo(a, b, /, c, *d, e, f, **g):
#   return True
# foo(1,2,3,4,5,6,7,e=8,f=9,x=10,y=11,z=12,k=13)
# ''')
tree = ast.parse("a.f().g().h()")
print(ast.dump(tree, indent=4))

callnode = tree.body[0].value


def f(node):
    retstr = ''
    if isinstance(node, ast.Call):
        retstr += f(node.func)
    elif isinstance(node, ast.Name):
        retstr += node.id
    elif isinstance(node, ast.Attribute):
        retstr += f(node.value) + '.' + node.attr
    else:
        raise RuntimeError(f'Unexpected type of node: {type(node)}')
    return retstr


aux = f(callnode)
print(aux)
