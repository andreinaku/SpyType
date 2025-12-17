from __future__ import annotations
from dataclasses import dataclass, field


NONE_TYPE_NAME = "NoneTypeET"
OBJECT_TYPE_NAME = "ObjectET"
BOTTOM_TYPE_NAME = "BottomET"
ANY_TYPE_NAME = "AnyTypeET"
SELF_TYPE_MARKER = "SelfET"

@dataclass
class ExistentialType:
    name: str
    bound: 'ExistentialType' | None = None
    generics: list['ExistentialType'] = field(default_factory=list)
    signature: dict[str, 'ExistentialType'] = field(default_factory=dict)
    sum_of: list['ExistentialType'] = field(default_factory=list)

    is_bottom: bool = False
    is_top: bool = False

    def is_subtype_of(self, other: 'ExistentialType', assumptions: set[tuple[str, str]] | None = None) -> bool:
        # This is not <: but rather <=
        
        # TODO: Support sum types
        if len(self.sum_of) > 0 or len(other.sum_of) > 0:
            raise NotImplementedError("Sum types are not supported yet")

        # TODO: Maybe add axioms for subtyping?
        # TODO: Add support for "constant" types in __init__ methods of basetype-classes.

        if assumptions is None:
            assumptions = set()
        
        pair = (self.name, other.name)
        if pair in assumptions:
            return True

        # If the names are the same, then they are equal
        if self.name == other.name:
            return True
        if other.is_top:  # Everything is a subtype of top (Object)
            return True
        if self.is_bottom:  # Bottom is a subtype of everything
            return True
        
        # Every type is equal to Self
        if self.name == SELF_TYPE_MARKER:
            return True  # Self is a subtype of everything
        if other.name == SELF_TYPE_MARKER:
            return True  # Everything is a subtype of Self

        # Add the pair to assumptions to avoid infinite recursion
        assumptions.add(pair)

        if not other.signature:
            return False  # No structural basis for subtyping, and names already differ

        # Structural subtyping: subtype must have all methods of supertype
        for func_name, func_type in other.signature.items():
            if func_name not in self.signature: 
                return False
            if not self.signature[func_name].is_subtype_of(func_type, assumptions):
                return False
        return True


# NoneTypeET is the existential type for the type of None
NoneTypeET = ExistentialType(NONE_TYPE_NAME)
SelfMarkerET = ExistentialType(SELF_TYPE_MARKER)

@dataclass
class FunctionType(ExistentialType):
    domain: list[ExistentialType] = field(default_factory=list)
    codomain: ExistentialType | None = None

    def __repr__(self) -> str:
        param_types = " x ".join(repr(t) for t in self.domain) if self.domain else ""
        codomain_repr = repr(self.codomain) if self.codomain is not None else repr(NoneTypeET)
        if param_types:
            return f"({param_types}) -> {codomain_repr}"
        else:
            return f"() -> {codomain_repr}"

    def is_subtype_of(self, other: 'FunctionType', assumptions: set[tuple[str, str]] | None = None) -> bool:
        if not isinstance(other, FunctionType):
            return False
        if assumptions is None:
            assumptions = set()
        
        # Check domain (contravariant)
        if len(self.domain) != len(other.domain):
            return False
        for i in range(len(self.domain)):
            if not other.domain[i].is_subtype_of(self.domain[i], assumptions):
                return False
        # Check codomain (covariant)
        if self.codomain is None and other.codomain is None:
            return True
        if self.codomain is None or other.codomain is None:
            return False
        return self.codomain.is_subtype_of(other.codomain, assumptions)


@dataclass
class TypeVarType(ExistentialType):
    # Already inherits all fields from ExistentialType
    # - name: holds the TypeVar name directly (e.g., "_T", "_KT", "_VT")
    # - bound: holds the bound type if specified (e.g., SizedET)
    pass


class TypeRegistry:
    def __init__(self):
        self._types: dict[str, ExistentialType] = {}
        # Special types
        self._types[NONE_TYPE_NAME] = NoneTypeET  # NoneTypeET is the unit type in our type system
        self.get_or_create(OBJECT_TYPE_NAME, is_top=True)  # ObjectET is the top type
        self.get_or_create(BOTTOM_TYPE_NAME, is_bottom=True)  # The bottom type
        self.get_or_create(ANY_TYPE_NAME)  # Any type placeholder for unknown types
        self.get_or_create(SELF_TYPE_MARKER)  # Self type marker
        
    def get_or_create(self, name: str, **kwargs) -> ExistentialType:
        if name not in self._types:
            self._types[name] = ExistentialType(name, **kwargs)
        return self._types[name]
    
    def get_all_types(self) -> list[ExistentialType]:
        return list(self._types.values())
    
    def print_registry(self) -> None:
        for name, et in self._types.items():
            if et.signature:
                print(f"{name}: {{")
                for method_name, method_type in et.signature.items():
                    if isinstance(method_type, FunctionType):
                        domain_str = " x ".join(t.name for t in method_type.domain) if method_type.domain else ""
                        codomain_str = method_type.codomain.name if method_type.codomain else "NoneTypeET"
                        print(f'    "{method_name}": {domain_str} -> {codomain_str}')
                    else:
                        print(f'    "{method_name}": {method_type.name}')
                print("}")
            else:
                print(f"{name}: {{}}")
