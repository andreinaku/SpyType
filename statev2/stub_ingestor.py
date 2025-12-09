import ast
from existential_types import TypeRegistry, ExistentialType, FunctionType, NoneTypeET
from typing import Any


def to_et_name(name: str) -> str:
    return name.capitalize() + "ET"


class StubIngestor(ast.NodeVisitor):
    def __init__(self, registry: TypeRegistry):
        self.registry = registry
        self.current_class: ExistentialType | None = None

    def parse_annotation(self, node: ast.expr | None) -> ExistentialType:
        if isinstance(node, ast.Name):
            # Simple type name like int, str, float, MyClass, etc.
            # Covers all non-generic types, theoretically
            return self.registry.get_or_create(to_et_name(node.id))
        
        if isinstance(node, ast.Constant):
            # None used as an annotation has type ast.Constant with value=None
            if node.value is None:
                # NoneTypeET is already in the registry, so we don't need to create it again
                # We raise an error because we don't support other constant annotations
                return NoneTypeET
            raise NotImplementedError(f"Unsupported constant annotation: {node.value}")
                
        
        # Placeholder for other types (ast.Subscript, ast.BinOp, etc.)
        raise NotImplementedError(f"Unsupported annotation type: {type(node).__name__}")

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Parse parameter annotations
        param_types: list[ExistentialType] = []
        for arg in node.args.args:
            if arg.annotation is not None:
                param_type = self.parse_annotation(arg.annotation)
                param_types.append(param_type)
        
        # Parse return type annotation
        return_type: ExistentialType | None = None
        if node.returns is not None:
            return_type = self.parse_annotation(node.returns)

    def visit_ClassDef(self, node: ast.ClassDef):
        et_name = to_et_name(node.name)
        current_et = self.registry.get_or_create(et_name)
        pass

    def visit_Assign(self, node: ast.Assign):
        pass

    def visit_Import(self, node: ast.Import):
        pass


if __name__ == "__main__":
    code = "def f(x: int, y: list[int], z: None, q) -> float: ..."
    tree = ast.parse(code)
    func = tree.body[0]
    
    print(ast.dump(func, indent=2))
