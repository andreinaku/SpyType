from __future__ import annotations
from typing_extensions import *
import ast
import astor
import types


class AddClassTypes(ast.NodeVisitor):
    def __init__(self, tree):
        self.new_types = set()
        self.tree = tree

    @staticmethod
    def generate_template(classname: str, basenames: list[str]) -> str:
        basestr = ''
        for basename in basenames:
            basestr += basename + ", "
        if len(basestr) > 1:
            basestr = basestr[:-2]
        basestr = f"({basestr})"
        retstr = f"class {classname}{basestr}: ..."
        return retstr 

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        basenames = []
        for basenode in node.bases:
            basenames.append(astor.to_source(basenode).strip())
        # temp_code = self.generate_template(node.name, basenames)
        # exec(temp_code, globals())
        self.new_types.add(types.new_class(node.name))
        print(f"added {node.name}")

    def get_new_types(self):
        self.visit(self.tree)
        return self.new_types


if __name__ == "__main__":
    tree = ast.parse(open("playground\\python\\testclass.py").read())
    new_types = AddClassTypes(tree).get_new_types()
    print(new_types)
    # print(foo)
    # print(bar)
    # print(int)
    # print(issubclass(bar, foo))
    # print(issubclass(foo, bar))
    # print(eval('foo'))
    # print(MutableSequence)
