from typing import *
import typing
import types
from abc import ABC, abstractmethod
from copy import deepcopy
from os import PathLike
import collections.abc
import ast
import json

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
              dict,  # from types
              collections.abc.Mapping, collections.abc.MutableMapping
              ]
literal_types = [typing.Literal]

skip_types = [Ellipsis]

approximated_types = {
    typing.LiteralString: str,
    typing.Sized: collections.abc.Sized
}


class BaseType(ABC):
    @abstractmethod
    def __init__(self, ptip):
        ...

    @abstractmethod
    def __hash__(self):
        ...

    @abstractmethod
    def __str__(self):
        ...

    @abstractmethod
    def __repr__(self):
        ...


class ContainerType(BaseType):
    def __init__(self, ptip):
        self.ptip = ptip
        self.__origin__ = create_basetype(ptip.__origin__)
        self.__args__ = []
        for arg in ptip.__args__:
            if arg in skip_types:
                continue
            self.__args__.append(create_basetype(arg))
        self.__args__ = tuple(self.__args__)
    
    def __str__(self):
        retstr = f"{self.__origin__.__name__} < "
        for arg in self.__args__:
            retstr += f"{arg}, "
        retstr = retstr[:-2] + " >"
        return retstr
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash((self.__origin__, self.__args__))
    
    def __eq__(self, other) -> bool:
        if self.__origin__ != other.__origin__:
            return False
        if len(self.__args__) != len(other.__args__):
            return False
        for item in self.__args__:
            if item not in other.__args__:
                return False
        for item in other.__args__:
            if item not in self.__args__:
                return False
        return True


class ProductType(BaseType):
    def __init__(self, ptip):
        self.ptip = ptip
        self.__origin__ = create_basetype(ptip.__origin__)
        self.__args__ = []
        for arg in ptip.__args__:
            if arg in skip_types:
                continue
            self.__args__.append(create_basetype(arg))
        self.__args__ = tuple(self.__args__)

    def __str__(self):
        retstr = "("
        for arg in self.__args__:
            retstr += f"{arg} , "
        retstr += ")"
        return retstr
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(self.__args__)
    
    def __eq__(self, other) -> bool:
        if self.__origin__ != other.__origin__:
            return False
        if len(self.__args__) != len(other.__args__):
            return False
        for i in range(0, len(self.__args__)):
            if self.__args__[i] != other.__args__[i]:
                return False
        return True


class DictType(BaseType):
    def __init__(self, ptip):
        self.ptip = ptip
        self.__origin__ = create_basetype(ptip.__origin__)
        if len(ptip.__args__) != 2:
            raise TypeError(f"{ptip} is not a dictionary type")
        self.__args__ = (create_basetype(ptip.__args__[0]), create_basetype(ptip.__args__[1]))
    
    def __str__(self):
        retstr = f"{self.__origin__.__name__} < "
        for arg in self.__args__:
            retstr += f"{arg}, "
        retstr = retstr[:-2] + " >"
        return retstr
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash((self.__origin__, self.__args__))
    
    def __eq__(self, other) -> bool:
        if self.__origin__ != other.__origin__:
            return False
        if len(self.__args__) != len(other.__args__):
            return False
        for i in range(0, len(self.__args__)):
            if self.__args__[i] != other.__args__[i]:
                return False
        return True


class SumType(BaseType):
    def __init__(self, ptip):
        self.ptip = ptip
        self.__args__ = []
        for arg in ptip.__args__:
            self.__args__.append(create_basetype(arg))
        self.__args__ = tuple(self.__args__)

    def __str__(self):
        retstr = ""
        for arg in self.__args__:
            retstr += f"{arg} + "
        retstr = retstr[:-3]
        return retstr
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(self.__args__)
    
    def __contains__(self, elem: BaseType) -> bool:
        for item in self.__args__:
            if elem == item:
                return True
        return False
    
    def __eq__(self, other) -> bool:
        for elem in self:
            if elem not in other:
                return False
        for elem in other:
            if elem not in self:
                return False
        return True

    

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
    
    def __hash__(self):
        return hash(self.__name__)

    def __eq__(self, other):
        return hash(self) == hash(other)


class TypevarType(BaseType):
    def __init__(self, ptip: TypeVar):
        self.ptip = ptip

    @property
    def __name__(self):
        return self.ptip.__name__

    def __str__(self):
        return f"{self.ptip.__name__}"
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(self.__name__)
    
    def __eq__(self, other):
        return hash(self) == hash(other)



class AbstractState(dict):
    def __init__(self, initial_data=None):
        super().__init__()
        if initial_data:
            for k, v in initial_data.items():
                self.__setitem__(k, v)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f"{key} is not str")
        if not isinstance(value, BaseType):
            raise TypeError(f"{value} is not BaseType")
        super().__setitem__(key, value)

    def __str__(self):
        retstr = ''
        for k, v in self.items():
            retstr += rf'{k}:{v} /\ '
        if retstr:
            retstr = retstr[:-4]
        return retstr
    
    def __repr__(self):
        return str(self)

    def __hash__(self):
        tuppled = tuple(self.items())
        return hash(tuppled)
    
    def __eq__(self, other):
        if self.keys() != other.keys():
            return False
        for k, bt in self.items():
            if bt != other[k]:
                return False
        return True


class FunctionSpec(tuple):
    def __new__(cls, first, second):
        if not isinstance(first, AbstractState):
            raise TypeError(f"{first} is not an AbstractState")
        if not isinstance(second, AbstractState):
            raise TypeError(f"{second} is not an AbstractState")
        return super().__new__(cls, (first, second))

    def __str__(self):
        return f'({self[0]}) -> ({self[1]})'

    def __repr__(self):
        return str(self)
    
    def __eq__(self, other) -> bool:
        return self[0] == other[0] and self[1] == other[1]


# class FunctionSpecJSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, FunctionSpec):
#             return [self.serialize_abstract_state(abs_state) for abs_state in o]
#         if isinstance(o, AbstractState):
#             return self.serialize_abstract_state(o)
#         if isinstance(o, BaseType):
#             return self.serialize_basetype(o)
#         return super().default(o)

#     def serialize_abstract_state(self, abs_state):
#         if not isinstance(abs_state, AbstractState):
#             raise TypeError(f"cannot serialize {abs_state} because it is not an AbstractState")
#         return {key: self.serialize_basetype(value) for key, value in abs_state.items()}
        
    
#     def serialize_basetype(self, bt):
#         if not isinstance(bt, BaseType):
#             raise TypeError(f"cannot serialize {bt} because it is not a BaseType")
#         return str(bt)


def is_atom_type(ptip: type):
    if isinstance(ptip, type):
        return True
    return False


def is_var_type(ptip: type):
    if isinstance(ptip, typing.TypeVar):
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
    if not isinstance(ptip, (typing._BaseGenericAlias, types.GenericAlias)):
        return False
    if ptip.__origin__ in container_types:
        return True
    if len(ptip.__args__) == 1:
        return True
    return False


def is_product_type(ptip: type):
    if not isinstance(ptip, (typing._BaseGenericAlias, types.GenericAlias)):
        return False
    if is_dict_type(ptip):
        return False
    if ptip.__origin__ in product_types:
        return True
    if len(ptip.__args__) > 1:
        return True
    return False


def is_dict_type(ptip: type):
    if not isinstance(ptip, (typing._BaseGenericAlias, types.GenericAlias)):
        return False
    if ptip.__origin__ in dict_types:
        return True
    return False


def is_union_type(ptip: type):
    return isinstance(ptip, (typing._UnionGenericAlias, types.UnionType))


def create_basetype(ptip):
    if ptip in approximated_types:
        return create_basetype(approximated_types[ptip])
    elif is_atom_type(ptip):
        return AtomType(ptip)
    elif is_var_type(ptip):
        return TypevarType(ptip)
    elif is_literal_type(ptip):
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
    elif ptip is None:
        return create_basetype(type(ptip))
    else:
        raise TypeError(f"Unknown type {ptip}")


def str_tests():
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
    tip = "collections.abc.Mapping[int, float]"
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
    #
    as1 = AbstractState()
    as1['a'] = create_basetype(int)
    as1['b'] = create_basetype(float)
    print(as1)
    as2 = AbstractState()
    as2['return'] = create_basetype(list[int])
    print(as2)
    fs = FunctionSpec(as1, as2)
    print(fs)


def encode_tests():
    as1 = AbstractState()
    as1['a'] = create_basetype(int)
    as1['b'] = create_basetype(float)
    print(as1)
    as2 = AbstractState()
    as2['return'] = create_basetype(list[int])
    print(as2)
    fs = FunctionSpec(as1, as2)
    json_str = json.dumps(str(fs), indent=4)
    print(json_str)


if __name__ == "__main__":
    title = "Simple typing converter"
    print(title)
    print("=" * len(title))
    str_tests()
    encode_tests()
