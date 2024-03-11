import ast
import astpretty

expr = '(a * 3) + b'
astpretty.pprint(ast.parse(expr))
