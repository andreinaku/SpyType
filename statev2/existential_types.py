from __future__ import annotations
from dataclasses import dataclass, field


NONE_TYPE_NAME = "NoneTypeET"
OBJECT_TYPE_NAME = "ObjectET"
BOTTOM_TYPE_NAME = "BottomET"

@dataclass
class ExistentialType:
    name: str
    bound: 'ExistentialType' | None = None
    generics: list['ExistentialType'] = field(default_factory=list)
    signature: dict[str, 'ExistentialType'] = field(default_factory=dict)
    sum_of: list['ExistentialType'] = field(default_factory=list)

    is_bottom: bool = False
    is_top: bool = False

    def is_subtype_of(self, other: 'ExistentialType') -> bool:
        if self.name == other.name:
            return True
        if self.name == OBJECT_TYPE_NAME and other.name != OBJECT_TYPE_NAME:
            return True
        if self.name == BOTTOM_TYPE_NAME and other.name != BOTTOM_TYPE_NAME:
            return True
        return False


# NoneTypeET is the existential type for the type of None
NoneTypeET = ExistentialType(NONE_TYPE_NAME)


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

    def is_subtype_of(self, other: 'FunctionType') -> bool:
        if not isinstance(other, FunctionType):
            return False
        if self.codomain is None and other.codomain is not None:
            return False
        if self.codomain is not None and other.codomain is None:
            return False
        if self.codomain is not None and other.codomain is not None:
            return self.codomain.is_subtype_of(other.codomain)
        if len(self.domain) != len(other.domain):
            return False
        for i in range(len(self.domain)):
            if not other.domain[i].is_subtype_of(self.domain[i]):
                return False
        return True


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
