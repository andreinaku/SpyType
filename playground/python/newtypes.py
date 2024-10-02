from typing_extensions import *
import ast
import astor


class AddClassTypes(ast.NodeVisitor):

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
            basenames.append(astor.to_source(basenode))
        temp_code = self.generate_template(node.name, basenames)
        exec(temp_code, globals())


if __name__ == "__main__":
    tree = ast.parse(open("playground\\python\\testclass.py").read())
    v = AddClassTypes()
    v.visit(tree)
    print(foo)
    print(bar)
    print(int)
    print(issubclass(bar, foo))
    print(issubclass(foo, bar))
