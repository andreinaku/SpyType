"""
Script to parse test_stubs.pyi and print the obtained TypeRegistry.
"""
import ast
from pathlib import Path

from existential_types import TypeRegistry
from stub_ingestor import StubIngestor


def main():
    # Read the test_stubs.pyi file
    stub_path = "test_stubs.pyi"
    with open(stub_path, "r") as f:
        source = f.read()
    
    # Parse the source code into an AST
    tree = ast.parse(source)
    
    # Create a TypeRegistry and StubIngestor
    registry = TypeRegistry()
    ingestor = StubIngestor(registry)
    
    # Visit all nodes in the AST
    for node in ast.walk(tree):
        ingestor.visit(node)
    
    # Print the registry
    print("=" * 60)
    print("TypeRegistry after parsing test_stubs.pyi")
    print("=" * 60)
    registry.print_registry()


if __name__ == "__main__":
    main()
