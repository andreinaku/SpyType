'''
Script to get translatable basetypes for varargs and kwargs within a stub file.
Requires pyiparser_2.
'''

from ast import FunctionDef
from typing import Any
from pyiparser_2 import *


class GetStarTypes(ast.NodeVisitor):
    def __init__(self):
        self.argtypes = set()
        self.kwargtypes = set()
        self.unsupported = set()

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        if node.args.vararg is not None:
            try:
                aux = ClassdefToBasetypes().parse_node_type(node.args.vararg.annotation)
                self.argtypes.add(aux)
            except Exception:
                self.unsupported.add(astor.to_source(node.args.vararg.annotation).strip())
        if node.args.kwarg is not None:
            try:
                aux = ClassdefToBasetypes().parse_node_type(node.args.kwarg.annotation)
                self.kwargtypes.add(aux)
            except Exception:
                self.unsupported.add(astor.to_source(node.args.kwarg.annotation).strip())


tree = ast.parse(open('sheds/builtins.pyi', 'r').read())
aux = GetStarTypes()
aux.visit(tree)
print(f'Types for varargs: {aux.argtypes}')
print(f'Types for kwargs: {aux.kwargtypes}')
print(f'Unsupported annotations: {aux.unsupported}')
