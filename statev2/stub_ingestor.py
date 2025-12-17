import ast
from existential_types import TypeRegistry, ExistentialType, FunctionType, NoneTypeET, SelfMarkerET
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
        # The class visitor should:
        # - create an ExistentialType for the class, if it doesn't already exist.
        # - parse the base classes and add them to the class's bound field.
        # - iterate over the class body and parse the method signatures.
        et_name = to_et_name(node.name)
        current_et = self.registry.get_or_create(et_name)
        
        # Iterate over the class body to extract method and attribute signatures
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                # Create a FunctionType for the method
                method_name = item.name
                
                # Check for @staticmethod or @classmethod decorators
                decorator_names = [
                    d.id for d in item.decorator_list 
                    if isinstance(d, ast.Name)
                ]
                is_staticmethod = "staticmethod" in decorator_names
                # is_classmethod = "classmethod" in decorator_names
                
                # Parse parameter annotations
                param_types: list[ExistentialType] = []
                if is_staticmethod:
                    # @staticmethod: no self/cls, use all args
                    args = item.args.args
                else:
                    # # Regular method or @classmethod: first param is self/cls (type is the class)
                    param_types.append(SelfMarkerET)                    
                    args = item.args.args[1:]  # Skip 'self' or 'cls'
                
                for arg in args:
                    if arg.annotation is not None:
                        param_type = self.parse_annotation(arg.annotation)
                        param_types.append(param_type)
                
                # Parse return type annotation
                return_type: ExistentialType | None = None
                if item.returns is not None:
                    return_type = self.parse_annotation(item.returns)
                
                # Create FunctionType and add to signature
                func_type = FunctionType(
                    name=method_name,
                    domain=param_types,
                    codomain=return_type
                )
                current_et.signature[method_name] = func_type
                
            elif isinstance(item, ast.AnnAssign):
                # Create a FunctionType for the attribute (Unit -> AttributeType)
                if isinstance(item.target, ast.Name):
                    attr_name = item.target.id
                    attr_type = self.parse_annotation(item.annotation)
                    
                    # Attribute as a getter: () -> AttributeType
                    func_type = FunctionType(
                        name=attr_name,
                        domain=[NoneTypeET],  # Unit type (type of None)
                        codomain=attr_type
                    )
                    current_et.signature[attr_name] = func_type

    def visit_Assign(self, node: ast.Assign):
        pass

    def visit_Import(self, node: ast.Import):
        pass


if __name__ == "__main__":
    code = "def f(x: int, y: list[int], z: None, q) -> float: ..."
    tree = ast.parse(code)
    func = tree.body[0]
    
    print(ast.dump(func, indent=2))
