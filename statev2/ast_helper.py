import ast
import astpretty

expr = '3'
astpretty.pprint(ast.parse(expr))
