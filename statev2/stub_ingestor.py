import ast
from statev2.existential_types import TypeRegistry, ExistentialType, FunctionType


def to_et_name(name: str) -> str:
    return name.capitalize() + "ET"


class StubIngestor(ast.NodeVisitor):
    def __init__(self, registry: TypeRegistry):
        self.registry = registry
        self.current_class: ExistentialType | None = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        pass

    def visit_ClassDef(self, node: ast.ClassDef):
        et_name = to_et_name(node.name)
        et = self.registry.get_or_create(et_name)

    def visit_Import(self, node: ast.Import):
        pass