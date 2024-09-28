from typing_extensions import *
import ast


class AddClassTypes(ast.NodeVisitor):

    @staticmethod
    def generate_template(classname: str, parentnames: list[str]) -> str:
        if len(parentnames) > 0:
            raise RuntimeError("Inheritance not yet supported")
        retstr = f"class {classname}: ..."
        return retstr 

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        temp_code = self.generate_template(node.name, [])
        exec(temp_code, globals())


if __name__ == "__main__":
    tree = ast.parse(open("playground\\python\\testclass.py").read())
    v = AddClassTypes()
    v.visit(tree)
    print(foo)
