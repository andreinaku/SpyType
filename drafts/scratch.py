import ast

tree = ast.parse('''
def foo(a, b, /, c, *d, e, f, **g):
  return True
foo(1,2,3,4,5,6,7,e=8,f=9,x=10,y=11,z=12,k=13)
''')
print(ast.dump(tree, indent=4))
