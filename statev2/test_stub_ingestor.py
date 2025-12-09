import unittest
import ast
from stub_ingestor import StubIngestor, to_et_name
from existential_types import TypeRegistry, ExistentialType


class StubIngestorTestCases(unittest.TestCase):
    def test_to_et_name(self):
        """Test that the to_et_name function converts simple type names to ET names."""
        self.assertEqual(to_et_name("int"), "IntET")
        self.assertEqual(to_et_name("str"), "StrET")
        self.assertEqual(to_et_name("MyClass"), "MyclassET")

    def test_visit_function_def_simple_annotations(self):
        """Test that simple type annotations are parsed and added to registry."""
        code = "def f(x: int, y: str) -> float: ..."
        tree = ast.parse(code)
        
        registry = TypeRegistry()
        ingestor = StubIngestor(registry)
        ingestor.visit(tree)
        
        # Check that types were added to registry
        all_types = {t.name for t in registry.get_all_types()}
        self.assertIn("IntET", all_types)
        self.assertIn("StrET", all_types)
        self.assertIn("FloatET", all_types)

    def test_visit_function_def_none_return(self):
        """Test that None return type annotation is parsed correctly."""
        code = "def f(x: int) -> None: ..."
        tree = ast.parse(code)
        
        registry = TypeRegistry()
        ingestor = StubIngestor(registry)
        ingestor.visit(tree)
        
        all_types = {t.name for t in registry.get_all_types()}
        self.assertIn("IntET", all_types)
        self.assertIn("NoneTypeET", all_types)
        

    def test_visit_function_def_no_return_annotation(self):
        """Test function without return annotation."""
        code = "def f(x: int): ..."
        tree = ast.parse(code)
        
        registry = TypeRegistry()
        ingestor = StubIngestor(registry)
        ingestor.visit(tree)
        
        all_types = {t.name for t in registry.get_all_types()}
        self.assertIn("IntET", all_types)

    def test_visit_function_def_no_param_annotations(self):
        """Test function with unannotated parameters."""
        code = "def f(x, y) -> int: ..."
        tree = ast.parse(code)
        
        registry = TypeRegistry()
        ingestor = StubIngestor(registry)
        ingestor.visit(tree)
        
        all_types = {t.name for t in registry.get_all_types()}
        self.assertIn("IntET", all_types)

    def test_visit_function_def_custom_types(self):
        """Test that custom class type annotations are added to registry."""
        code = "def process(data: MyClass) -> Result: ..."
        tree = ast.parse(code)
        
        registry = TypeRegistry()
        ingestor = StubIngestor(registry)
        ingestor.visit(tree)
        
        all_types = {t.name for t in registry.get_all_types()}
        self.assertIn("MyclassET", all_types)
        self.assertIn("ResultET", all_types)

    def test_visit_multiple_functions(self):
        """Test parsing multiple function definitions."""
        code = """
def f1(x: int) -> str: ...
def f2(y: float) -> bool: ...
"""
        tree = ast.parse(code)
        
        registry = TypeRegistry()
        ingestor = StubIngestor(registry)
        ingestor.visit(tree)
        
        all_types = {t.name for t in registry.get_all_types()}
        self.assertIn("IntET", all_types)
        self.assertIn("StrET", all_types)
        self.assertIn("FloatET", all_types)
        self.assertIn("BoolET", all_types)

    def test_registry_types_are_existential_types(self):
        """Test that types in registry are ExistentialType instances."""
        code = "def f(x: int) -> str: ..."
        tree = ast.parse(code)
        
        registry = TypeRegistry()
        ingestor = StubIngestor(registry)
        ingestor.visit(tree)
        
        for t in registry.get_all_types():
            self.assertIsInstance(t, ExistentialType)

    def test_registry_deduplicates_types(self):
        """Test that same types are not duplicated in registry."""
        code = "def f(x: int, y: int) -> int: ..."
        tree = ast.parse(code)
        
        registry = TypeRegistry()
        ingestor = StubIngestor(registry)
        ingestor.visit(tree)
        
        # Count occurrences of IntET
        int_types = [t for t in registry.get_all_types() if t.name == "IntET"]
        self.assertEqual(len(int_types), 1)


if __name__ == "__main__":
    unittest.main()
