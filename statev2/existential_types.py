from __future__ import annotations
from dataclasses import dataclass, field
from inspect import signature


NONE_TYPE_NAME = "NoneTypeET"


@dataclass
class ExistentialType:
    name: str
    bound: 'ExistentialType' | None = None
    generics: list['ExistentialType'] = field(default_factory=list)
    signature: dict[str, 'ExistentialType'] = field(default_factory=dict)

    is_bottom: bool = False
    is_top: bool = False
    
    def is_subtype_of(self, other: 'ExistentialType') -> bool:
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


class TypeRegistry:
    def __init__(self):
        self._types: dict[str, ExistentialType] = {}
        self.get_or_create("NoneTypeET")
        self.get_or_create("AnyTypeET")
        self.get_or_create("ObjectET", is_top=True)
        
    def get_or_create(self, name: str, **kwargs) -> ExistentialType:
        if name not in self._types:
            self._types[name] = ExistentialType(name, **kwargs)
        return self._types[name]
    
    def get_all_types(self) -> list[ExistentialType]:
        return list(self._types.values())
