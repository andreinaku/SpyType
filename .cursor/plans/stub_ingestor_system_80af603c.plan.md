---
name: Stub Ingestor System
overview: Design a stub file parser that converts Python type annotations into ExistentialType structures, with support for sum types (unions), generic types, Callable/FunctionType, Literal types, and TypeVars.
todos:
  - id: update-existential-types
    content: Add `sum_of` field to ExistentialType; add TypeVarType subclass; update is_subtype_of for sum semantics
    status: pending
  - id: parse-annotation
    content: Implement parse_annotation() to handle ast.Name, ast.Subscript, ast.BinOp, ast.Constant, ast.Attribute, ast.Tuple
    status: pending
  - id: handle-callable
    content: Handle Callable[...] → FunctionType conversion in parse_annotation
    status: pending
  - id: handle-literal
    content: Handle Literal[...] → infer type from literal value
    status: pending
  - id: handle-typevar
    content: Implement visit_Assign to detect TypeVar declarations and create TypeVarType instances
    status: pending
  - id: visit-classdef
    content: Implement visit_ClassDef to parse classes, base classes, and method signatures
    status: pending
  - id: visit-functiondef
    content: Implement visit_FunctionDef to create FunctionType from parameter and return annotations
    status: pending
---

# Stub Ingestor System Plan

## Required Changes to `existential_types.py`

### 1. Add Sum Type Support

Add a `sum_of` field to `ExistentialType`:

```python
@dataclass
class ExistentialType:
    name: str
    bound: 'ExistentialType' | None = None
    generics: list['ExistentialType'] = field(default_factory=list)
    signature: dict[str, 'ExistentialType'] = field(default_factory=dict)
    sum_of: list['ExistentialType'] = field(default_factory=list)  # NEW
    is_bottom: bool = False
    is_top: bool = False
```

**Semantics:**

- Empty `sum_of` = atomic type (the type itself)
- Non-empty `sum_of` = union of listed types (e.g., `[IntET, StrET]` for `int | str`)

### 2. Update Subtyping for Sum Types

Update `is_subtype_of` to handle sum semantics:

- Atomic `A <: B` if A equals B or A is in B's sum components
- Sum `A1 + A2 <: B` if both A1 and A2 are subtypes of B

### 3. Add TypeVarType Subclass

Create a `TypeVarType` subclass (following the `FunctionType` pattern):

```python
@dataclass
class TypeVarType(ExistentialType):
    # Inherits all fields from ExistentialType
    # - name: holds the TypeVar name directly (e.g., "_T", "_KT", "_VT")
    # - bound: holds the bound type if specified (e.g., SizedET)
    pass  # No additional fields needed
```

**Example usage:**

```python
# _T = TypeVar("_T")
TypeVarType(name="_T")

# _T = TypeVar("_T", bound=Sized)
TypeVarType(name="_T", bound=SizedET)
```

This follows the same pattern as `FunctionType` and allows easy identification via `isinstance(t, TypeVarType)`.

---

## `stub_ingestor.py` Architecture

### Core Components

#### 1. Type Annotation Parser (`parse_annotation`)

A recursive function handling all AST node types for annotations:

| AST Node | Example | Result |

|----------|---------|--------|

| `ast.Name` | `int` | `IntET` |

| `ast.Subscript` | `list[int] `| `ListET` with `generics=[IntET]` |

| `ast.BinOp(BitOr)` | `int \| str` | `ExistentialType(sum_of=[IntET, StrET])` |

| `ast.Constant(None)` | `None` | `NoneTypeET` |

| `ast.Attribute` | `typing.List` | `ListET` |

| `ast.Tuple` | `(str, int)` in `dict[str, int]` | List of ETs |

#### 2. Special Type Handlers

**Callable types** → `FunctionType`:

```python
# Callable[[int, str], bool]
# Subscript.value = "Callable"
# Subscript.slice = Tuple([List[int, str], bool])
FunctionType(name="CallableET", domain=[IntET, StrET], codomain=BoolET)
```

**Literal types** → Infer from value:

```python
# Literal[0] → IntET (type of 0)
# Literal["a"] → StrET (type of "a")
# Literal[True] → BoolET
```

**Optional[X]** → Sum type:

```python
# Optional[int] = int | None
ExistentialType(sum_of=[IntET, NoneTypeET])
```

#### 3. TypeVar Handler

Detect `TypeVar` assignments and create `TypeVarType` instances:

```python
# _T = TypeVar("_T")
TypeVarType(name="_T")

# _T = TypeVar("_T", bound=SomeType)
TypeVarType(name="_T", bound=SomeTypeET)
```

**Note:** TypeVars keep their original name (e.g., `_T`, `_KT`, `_VT`) without the `ET` suffix, since they are placeholders rather than concrete types. Use `isinstance(t, TypeVarType)` to identify them.

#### 4. Class Visitor (`visit_ClassDef`)

- Create `ExistentialType` for the class
- Parse base classes (store in `bound` for single inheritance or track separately)
- Iterate over class body to extract method signatures into `signature` dict

#### 5. Function Visitor (`visit_FunctionDef`)

- Parse parameter annotations → `domain`
- Parse return annotation → `codomain`
- Create `FunctionType` and add to class signature if inside a class

---

## Implementation Flow

```
StubIngestor.ingest(file_path)
    │
    ├── ast.parse(source)
    │
    ├── visit_Assign()  ─────► Handle TypeVar declarations
    │
    ├── visit_ClassDef() ────► Create ExistentialType for class
    │       │
    │       └── visit_FunctionDef() ──► Create FunctionType for methods
    │               │
    │               └── parse_annotation() ──► Recursively parse types
    │
    └── Return populated TypeRegistry
```

---

## Key Methods to Implement

### `parse_annotation(node: ast.expr | None) -> ExistentialType`

```python
def parse_annotation(self, node: ast.expr | None) -> ExistentialType:
    if node is None:
        return self.registry.get_or_create("AnyTypeET")
    
    match node:
        case ast.Name(id=name):
            return self.registry.get_or_create(to_et_name(name))
        
        case ast.Subscript(value=ast.Name(id="list"), slice=inner):
            inner_et = self.parse_annotation(inner)
            return ExistentialType(name="ListET", generics=[inner_et])
        
        case ast.Subscript(value=ast.Name(id="Callable"), slice=...):
            # Handle Callable[[args], return]
            ...
        
        case ast.Subscript(value=ast.Name(id="Literal"), slice=...):
            # Extract literal value type
            ...
        
        case ast.BinOp(op=ast.BitOr(), left=l, right=r):
            left_et = self.parse_annotation(l)
            right_et = self.parse_annotation(r)
            return self._make_sum_type([left_et, right_et])
        
        case ast.Constant(value=None):
            return self.registry.get_or_create("NoneTypeET")
        ...
```

### `_make_sum_type(components: list[ExistentialType]) -> ExistentialType`

Flatten nested sums and create a normalized sum type.

### `visit_ClassDef(node: ast.ClassDef)`

```python
should def visit_ClassDef(self, node: ast.ClassDef):
    et = self.registry.get_or_create(to_et_name(node.name))
    
    # Parse base classes
    for base in node.bases:
        base_et = self.parse_annotation(base)
        # Store inheritance info (e.g., in bound or separate field)
    
    # Parse methods
    self.current_class = et
    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            self.visit_FunctionDef(item)
    self.current_class = None
```

---

## Edge Cases to Handle

1. **Nested generics**: `list[dict[str, int]]` → `ListET[DictET[StrET, IntET]]`
2. **Self references**: `def copy(self) -> Self` → Handle `Self` type
3. **Overloaded methods**: Multiple `@overload` decorated functions (consider taking first or merging)
4. **Forward references**: String annotations like `"SomeClass"`
5. **`*args` and `**kwargs`**: Could be ignored or represented specially