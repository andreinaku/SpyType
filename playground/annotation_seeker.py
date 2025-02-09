import ast
import astor
from typing import *
from _typeshed import *
import json


class AnnotationSeeker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST):
        self.tree = tree
        self.problems = []
        self.goodies = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for arg in node.args.args:
            if not hasattr(arg, "annotation") or arg.annotation is None:
                continue
            try:
                argstr = astor.to_source(arg.annotation).strip()
                eval(argstr)
                self.goodies.append(argstr)
            except:
                # print(f"not evalled {argstr}")
                self.problems.append(argstr)

    def collect(self) -> list[str]:
        self.visit(self.tree)
        self.goodies = list(set(self.goodies))
        self.problems = list(set(self.problems))
        return self.goodies, self.problems


def seek_from_stubs(fname: str) -> list[str]:
    with open(fname, 'r') as f:
        tree = ast.parse(f.read())
    aux = AnnotationSeeker(tree).collect()
    return aux


if __name__ == "__main__":
    fname = "/Users/andrei/work/doctorat/SpyType/sheds/builtins.pyi"
    goodlist, badlist = seek_from_stubs(fname)
    print(f"good = {len(goodlist)} items\nbad = {len(badlist)} items")
    with open("badseeks.json", "w") as f:
        json.dump(badlist, f, indent=4)
