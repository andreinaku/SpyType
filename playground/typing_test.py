from typing import *
import typing
import types
from abc import ABC
from copy import deepcopy


'''
type: int, float, str, ....
_GenericAlias:
* List, Set, .... -> SequenceType
* Tuple, Dict -> ProductType
'''

container_types = [typing.List, typing.Set, typing.FrozenSet,  # from typing
                   list, set, frozenset  # from types
                   ]
product_types = [typing.Tuple,  # from typing
                 tuple  # from types
                 ]
dict_types = [typing.Dict,  # from typing
              dict  # from types
              ]
literal_types = [typing.Literal]


class BaseType(ABC):
    def __init__(self, ptip):
        ...


class ContainerType(BaseType):
    def __init__(self, ptip):
        self.ptip = ptip
        self.__origin__ = create_basetype(ptip.__origin__)
        self.__args__ = []
        for arg in ptip.__args__:
            self.__args__.append(create_basetype(arg))
    
    def __str__(self):
        retstr = f"{self.__origin__.__name__} < "
        for arg in self.__args__:
            retstr += f"{arg}, "
        retstr = retstr[:-2] + " >"
        return retstr
    
    def __repr__(self):
        return str(self)


class ProductType(BaseType):
    def __init__(self, ptip):
        self.ptip = ptip
        self.__args__ = []
        for arg in ptip.__args__:
            self.__args__.append(create_basetype(arg))

    def __str__(self):
        retstr = "("
        for arg in self.__args__:
            retstr += f"{arg} , "
        retstr += ")"
        return retstr
    
    def __repr__(self):
        return str(self)


class DictType(BaseType):
    def __init__(self, ptip):
        self.ptip = ptip
        self.__origin__ = create_basetype(ptip.__origin__)
        self.__args__ = []
        for arg in ptip.__args__:
            self.__args__.append(create_basetype(arg))
    
    def __str__(self):
        retstr = f"{self.__origin__.__name__} < "
        for arg in self.__args__:
            retstr += f"{arg}, "
        retstr = retstr[:-2] + " >"
        return retstr
    
    def __repr__(self):
        return str(self)


class SumType(BaseType):
    def __init__(self, ptip):
        self.ptip = ptip
        self.__args__ = []
        for arg in ptip.__args__:
            self.__args__.append(create_basetype(arg))

    def __str__(self):
        retstr = ""
        for arg in self.__args__:
            retstr += f"{arg} + "
        retstr = retstr[:-3]
        return retstr
    
    def __repr__(self):
        return str(self)
    

class AtomType(BaseType):
    def __init__(self, ptip):
        self.ptip = ptip

    @property
    def __name__(self):
        return self.ptip.__name__

    def __str__(self):
        return f"{self.ptip.__name__}"
    
    def __repr__(self):
        return str(self)


def is_atom_type(ptip: type):
    if isinstance(ptip, type):
        return True
    return False


def is_literal_type(ptip: type):
    if isinstance(ptip, typing._LiteralGenericAlias):
        return True


def get_literal_args(ptip: typing._LiteralGenericAlias) -> type:
    typelist = []
    if len(ptip.__args__) == 1:
        return type(ptip.__args__[0])
    newtype = type(ptip.__args__[0])
    for i in range(1, len(ptip.__args__)):
        newtype = newtype | type(ptip.__args__[i])
    return newtype


def is_container_type(ptip: type):
    if not isinstance(ptip, (typing._GenericAlias, types.GenericAlias)):
        return False
    if ptip.__origin__ in container_types:
        return True
    if len(ptip.__args__) == 1:
        return True
    return False


def is_product_type(ptip: type):
    if not isinstance(ptip, (typing._GenericAlias, types.GenericAlias)):
        return False
    if ptip.__origin__ in product_types:
        return True
    if len(ptip.__args__) > 1:
        return True
    return False


def is_dict_type(ptip: type):
    if not isinstance(ptip, (typing._GenericAlias, types.GenericAlias)):
        return False
    if ptip.__origin__ in dict_types:
        return True
    return False


def is_union_type(ptip: type):
    return isinstance(ptip, (typing._UnionGenericAlias, types.UnionType))


def create_basetype(ptip):
    if is_atom_type(ptip):
        return AtomType(ptip)
    if is_literal_type(ptip):
        new_ptip = get_literal_args(ptip)
        return create_basetype(new_ptip)
    elif is_container_type(ptip):
        return ContainerType(ptip)
    elif is_product_type(ptip):
        return ProductType(ptip)
    elif is_dict_type(ptip):
        return DictType(ptip)
    elif is_union_type(ptip):
        return SumType(ptip)
    else:
        raise TypeError(f"Unknown type {ptip}")


if __name__ == "__main__":
    title = "Simple typing converter"
    print(title)
    print("=" * len(title))
    tip = "int"
    _tip = create_basetype(eval(tip))
    print(_tip)
    tip = "List[int]"
    _tip = create_basetype(eval(tip))
    print(_tip)
    tip = "List[int | float]"
    _tip = create_basetype(eval(tip))
    print(_tip)
    tip = "list[int | float]"
    _tip = create_basetype(eval(tip))
    print(_tip)
    tip = "tuple[int, float]"    
    _tip = create_basetype(eval(tip))
    print(_tip)
    tip = "tuple[int | float]"    
    _tip = create_basetype(eval(tip))
    print(_tip)
    tip = "dict[int, float]"    
    _tip = create_basetype(eval(tip))
    print(_tip)
    tip = "Iterable[int]"
    _tip = create_basetype(eval(tip))
    print(_tip)
    tip = "types.MappingProxyType[int, float]"
    _tip = create_basetype(eval(tip))
    print(_tip)
    tip = 'Literal["w"]'
    _tip = create_basetype(eval(tip))
    print(_tip)
    tip = 'Literal["w", 3]'
    _tip = create_basetype(eval(tip))
    print(_tip)
    tip = 'Literal[3, "w"]'
    _tip = create_basetype(eval(tip))
    print(_tip)
