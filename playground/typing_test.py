from __future__ import annotations
from typing import *
import typing
import types
from abc import ABC, abstractmethod
from copy import deepcopy
from os import PathLike
import collections.abc
import ast
import json
from dataclasses import dataclass
from enum import Enum
import pickle

'''
type: int, float, str, ....
_GenericAlias:
* List, Set, .... -> SequenceType
* Tuple, Dict -> ProductType
'''

class Relation(Enum):
    LEQ = '<='
    EQ = '=='
    GEQ = '>='
    LT = '<'
    GT = '>'
    NEQ = '!='


container_types = [typing.List, typing.Set, typing.FrozenSet,  # from typing
                   list, set, frozenset,  # from types
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

with open('playground/type_pairs.pkl', 'rb') as f:
    type_pairs = pickle.load(f)
new_pairs = set()
for ttuple in type_pairs:
    t1, t2 = ttuple
    if t1 in approximated_types:
        if t2 in approximated_types:
            new_pairs.add((approximated_types[t1], approximated_types[t2]))
        else:
            new_pairs.add((approximated_types[t1], t2))
    if t2 in approximated_types:
        if t1 in approximated_types:
            new_pairs.add((approximated_types[t1], approximated_types[t2]))
        else:
            new_pairs.add((t1, approximated_types[t2]))
type_pairs |= new_pairs


class Constraint(tuple):
    def __new__(cls, rel: Relation, left: BaseType, right: BaseType) -> Constraint:
        if not isinstance(rel, Relation):
            raise TypeError(f"First element must be a Relation, got {type(rel).__name__}")
        if not isinstance(left, BaseType):
            raise TypeError(f"Second element must be a BaseType, got {type(left).__name__}")
        if not isinstance(right, BaseType):
            raise TypeError(f"Third element must be a BaseType, got {type(right).__name__}")
        return super().__new__(cls, (rel, left, right))

    @property
    def relation(self):
        return self[0]
    
    @property
    def left(self):
        return self[1]
    
    @property
    def right(self):
        return self[2]
    
    def __str__(self):
        return f"{self.left} {self.relation.value} {self.right}"

    def __repr__(self):
        return str(self)


class ConstraintSet(set):
    def __init__(self, iterable=None):
        super().__init__()
        if iterable is not None:
            for item in iterable:
                self.add(item)

    def add(self, item):
        if not isinstance(item, Constraint):
            raise TypeError(f"ConstraintSet can only contain Constraint objects, got {type(item).__name__}")
        super().add(item)

    def update(self, *others):
        for other in others:
            for item in other:
                self.add(item)


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

    @abstractmethod
    def to_type(self):
        ...

    @classmethod
    def lub(cls, bt1: BaseType, bt2: BaseType) -> SumType:
        return SumType.from_basetypes([bt1, bt2])
    
    def __le__(self, other: BaseType) -> bool:
        if isinstance(self, AtomType) and isinstance(other, AtomType):
            if self == other:
                return True
            type_tuple = (self.to_type(), other.to_type())
            if type_tuple in type_pairs:
                return True
            return False
        elif isinstance(self, AtomType) and isinstance(other, SumType):
            for t in other.get_args():
                if self <= t:
                    return True
            return False
        elif isinstance(self, ContainerType) and isinstance(other, ContainerType):
            if not self.get_orig() <= other.get_orig():
                return False
            if not self.get_contained() <= other.get_contained():
                return False
            return True
        elif isinstance(self, ProductType) and isinstance(other, ProductType):
            if not self.get_orig() <= other.get_orig():
                return False
            args1 = self.get_args()
            args2 = other.get_args()
            arg_nr = len(args1)
            if arg_nr != len(args2):
                return False
            for i in range(0, arg_nr):
                if not args1[i] <= args2[i]:
                    return False
            return True

        # TODO: add logic for other types
        return False


class ContainerType(BaseType):
    def validate(self):
        if not isinstance(self.__origin__, BaseType):
            raise TypeError(f"{self}'s origin, {self.__origin__}, is not a BaseType")
        if len(self.__args__) > 1:
            raise TypeError(f"{self.__args__} has more than 1 argument")
        for _arg in self.__args__:
            if not isinstance(_arg, BaseType):
                raise TypeError(f"{self}'s argument, {_arg}, is not a BaseType")

    def __init__(self):
        self.__pythontype__ = None
        self.__origin__ = None
        self.__args__ = []

    def get_orig(self):
        return self.__origin__
    
    def get_contained(self):
        return self.__args__[0]

    @classmethod
    def from_type(cls, ptip: type) -> ContainerType:
        new_instance = cls.from_type_pieces(ptip.__origin__, ptip.__args__)
        new_instance.__pythontype__ = ptip
        new_instance.validate()
        return new_instance
    
    @classmethod
    def from_type_pieces(cls, _orig: type, _args: list[type]) -> ContainerType:
        new_instance = cls()
        new_instance.__origin__ = create_basetype(_orig)
        for arg in _args:
            if arg in skip_types:
                continue
            new_instance.__args__.append(create_basetype(arg))
        new_instance.__args__ = tuple(new_instance.__args__)
        new_instance.__pythontype__ = types.GenericAlias(new_instance.__origin__.to_type(), 
                                                         [_arg.to_type() for _arg in new_instance.__args__])
        new_instance.validate()
        return new_instance
    
    def to_type(self):
        return self.__pythontype__

    def __str__(self):
        return str(self.__pythontype__)
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash((self.__origin__, self.__args__))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ContainerType):
            return False
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
    def validate(self):
        if not isinstance(self.__origin__, BaseType):
            raise TypeError(f"{self}'s origin, {self.__origin__}, is not a BaseType")
        for _arg in self.__args__:
            if not isinstance(_arg, BaseType):
                raise TypeError(f"{self}'s argument, {_arg}, is not a BaseType")

    def __init__(self):
        self.__pythontype__ = None
        self.__origin__ = None
        self.__args__ = []

    def get_orig(self):
        return self.__origin__

    def get_args(self):
        return self.__args__

    @classmethod
    def from_type_pieces(cls, _orig: type, _args: list[type]) -> ContainerType:
        new_instance = cls()
        new_instance.__origin__ = create_basetype(_orig)
        for arg in _args:
            if arg in skip_types:
                continue
            new_instance.__args__.append(create_basetype(arg))
        new_instance.__args__ = tuple(new_instance.__args__)
        new_instance.__pythontype__ = types.GenericAlias(new_instance.__origin__.to_type(), 
                                                         [_arg.to_type() for _arg in new_instance.__args__])
        new_instance.validate()
        return new_instance

    @classmethod
    def from_type(cls, ptip: type) -> ProductType:
        new_instance = cls.from_type_pieces(ptip.__origin__, ptip.__args__)
        new_instance.__pythontype__ = ptip
        new_instance.validate()
        return new_instance

    def to_type(self):
        return self.__pythontype__

    def __str__(self):
        return str(self.__pythontype__)
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(self.__args__)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ProductType):
            return False
        if self.__origin__ != other.__origin__:
            return False
        if len(self.__args__) != len(other.__args__):
            return False
        for i in range(0, len(self.__args__)):
            if self.__args__[i] != other.__args__[i]:
                return False
        return True


class DictType(BaseType):
    def validate(self):
        if not isinstance(self.__origin__, BaseType):
            raise TypeError(f"{self}'s origin, {self.__origin__}, is not a BaseType")
        for _arg in self.__args__:
            if not isinstance(_arg, BaseType):
                raise TypeError(f"{self}'s argument, {_arg}, is not a BaseType")

    def __init__(self):
        self.__pythontype__ = None
        self.__origin__ = None
        self.__args__ = []
    
    @classmethod
    def from_type_pieces(cls, _orig: type, _args: tuple[type]) -> DictType:
        new_instance = cls()
        new_instance.__origin__ = create_basetype(_orig)
        if len(_args) != 2:
            raise TypeError(f"{_orig}, {_args} not a dictionary type")
        new_instance.__args__ = (create_basetype(_args[0]), create_basetype(_args[1]))
        new_instance.__pythontype__ = types.GenericAlias(_orig, [_args[0], _args[1]])
        new_instance.validate()
        return new_instance

    @classmethod
    def from_type(cls, ptip: types.GenericAlias) -> DictType:
        new_instance = cls.from_type_pieces(ptip.__origin__, ptip.__args__)
        new_instance.__pythontype__ = ptip
        new_instance.validate()
        return new_instance
    
    def to_type(self):
        if self.__pythontype__ is not None:
            return self.__pythontype__
        new_type = types.GenericAlias(dict, [self.__args__[0].to_type(), self.__args__[1].to_type()])
        return new_type

    def __str__(self):
        return str(self.__pythontype__)
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash((self.__origin__, self.__args__))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, DictType):
            return False
        if self.__origin__ != other.__origin__:
            return False
        if len(self.__args__) != len(other.__args__):
            return False
        for i in range(0, len(self.__args__)):
            if self.__args__[i] != other.__args__[i]:
                return False
        return True


class SumType(BaseType):
    def validate(self):
        for _arg in self.__args__:
            if not isinstance(_arg, BaseType):
                raise TypeError(f"{self}'s argument, {_arg}, is not a BaseType")

    def __init__(self):
        self.__pythontype__ = None
        self.__args__ = None

    @classmethod
    def from_type(cls, ptip: type):
        new_instance = cls.from_type_seq(ptip.__args__)
        new_instance.__pythontype__ = ptip
        new_instance.validate()
        return new_instance
    
    @classmethod
    def from_type_seq(cls, type_seq: Sequence[type]):
        new_instance = cls()
        new_instance.__args__ = []
        for _arg in type_seq:
            new_instance.__args__.append(create_basetype(_arg))
        new_instance.__args__ = frozenset(new_instance.__args__)
        new_instance.__pythontype__ = type_seq[0]
        for i in range(1, len(type_seq)):
            new_instance.__pythontype__ |= type_seq[i]
        new_instance.validate()
        return new_instance
    
    @classmethod
    def from_basetypes(cls, btype_seq: Sequence[BaseType]):
        new_instance = cls()
        new_instance.__args__ = []
        for btype in btype_seq:
            if isinstance(btype, SumType):
                # new_instance.__args__ = [_arg for _arg in btype.__args__ if _arg not in new_instance.__args__]
                for _arg in btype.__args__:
                    if _arg not in new_instance.__args__: 
                        new_instance.__args__.append(_arg)
                continue
            new_instance.__args__.append(btype)
        new_instance.__args__ = frozenset(new_instance.__args__)
        new_instance.__pythontype__ = btype_seq[0].to_type()
        for i in range(1, len(btype_seq)):
            new_instance.__pythontype__ |= btype_seq[i].to_type()
        new_instance.validate()
        return new_instance

        
    def to_type(self):
        return self.__pythontype__

    def __str__(self):
        retstr = ""
        for _arg in self.__args__:
            retstr += f"{_arg} | "
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
        if not isinstance(other, SumType):
            if isinstance(other, AtomType) and len(self.__args__) == 1:
                return self.__args__[0] == other
            return False
        for elem in self.__args__:
            if elem not in other.__args__:
                return False
        for elem in other.__args__:
            if elem not in self.__args__:
                return False
        return True
    
    def get_args(self):
        return self.__args__


class AtomType(BaseType):
    def __init__(self, ptip):
        self.__pythontype__ = ptip

    @property
    def __name__(self):
        return self.__pythontype__.__name__

    def __str__(self):
        return f"{self.__pythontype__.__name__}"
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(self.__name__)

    def __eq__(self, other):
        if not isinstance(other, AtomType):
            if isinstance(other, SumType) and len(other.__args__) == 1:
                return self == other.__args__[0]
            return False
        return hash(self) == hash(other)
    
    def to_type(self):
        return self.__pythontype__
            

class TypevarType(BaseType):
    def __init__(self):
        self.__pythontype__ = None
        self.__name__ = ''
    
    @classmethod
    def from_str(cls, _str: str) -> TypevarType:
        new_instance = cls()
        new_instance.__name__ = _str
        new_instance.__pythontype__ = typing.TypeVar(new_instance.__name__)
        return new_instance

    @classmethod
    def from_type(cls, ptip: TypeVar):
        new_instance = cls.from_str(ptip.__name__)
        new_instance.__pythontype__ = ptip
        return new_instance

    def __str__(self):
        return f"{self.__name__}"
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(self.__name__)
    
    def __eq__(self, other):
        return hash(self) == hash(other)

    def to_type(self):
        return self.__pythontype__


class AbstractState(dict):
    # TODO: implement <=
    def validate(self):
        for k, v in self.items():
            if not isinstance(k, str) and not isinstance(v, BaseType):
                raise TypeError(f"{self} is not a valid AbstractState")
                
    def __init__(self, initial_data=None):
        super().__init__()
        if initial_data:
            for k, v in initial_data.items():
                self.__setitem__(k, v)
        self.validate()

    @classmethod
    def from_dict(cls, _d: dict[str, type]) -> AbstractState:
        new_dict = {k: create_basetype(v) for k, v in _d.items()}
        new_as = cls(new_dict)
        return new_as

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f"{key} is not str")
        if not isinstance(value, BaseType):
            raise TypeError(f"{value} is not BaseType")
        super().__setitem__(key, value)

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
    
    def __le__(self, other: AbstractState) -> bool:
        if self.keys() != other.keys():
            return False
        for k, bt in self.items():
            if not bt <= other[k]:
                return False
        return True


class FunctionSpec(tuple):
    def __new__(cls, first, second):
        if not isinstance(first, AbstractState):
            raise TypeError(f"{first} is not an AbstractState")
        if not isinstance(second, AbstractState):
            raise TypeError(f"{second} is not an AbstractState")
        return super().__new__(cls, (first, second))

    @classmethod
    def from_dict_tuple(cls, dtuple: tuple[dict[str, BaseType]]) -> FunctionSpec:
        if len(dtuple) != 2:
            raise TypeError(f"{dtuple} has more than 2 elements")
        if not isinstance(dtuple[0], dict) or not isinstance(dtuple[1], dict):
            raise TypeError(f"one of the {dtuple} elements is not a dict")
        return FunctionSpec(AbstractState.from_dict(dtuple[0]), AbstractState.from_dict(dtuple[1]))

    def __eq__(self, other) -> bool:
        return self[0] == other[0] and self[1] == other[1]


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
    if len(ptip.__args__) == 1 and ptip.__origin__ not in product_types:
        return True
    return False


def is_product_type(ptip: type):
    if not isinstance(ptip, (typing._BaseGenericAlias, types.GenericAlias)):
        return False
    if is_dict_type(ptip):
        return False
    if is_union_type(ptip):
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
        return TypevarType.from_type(ptip)
    elif is_literal_type(ptip):
        new_ptip = get_literal_args(ptip)
        return create_basetype(new_ptip)
    elif is_container_type(ptip):
        return ContainerType.from_type(ptip)
    elif is_product_type(ptip):
        return ProductType.from_type(ptip)
    elif is_dict_type(ptip):
        return DictType.from_type(ptip)
    elif is_union_type(ptip):
        return SumType.from_type(ptip)
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
    print(_tip.to_type())
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
    print(_tip.to_type())
    tip = "tuple[int | float]"    
    _tip = create_basetype(eval(tip))
    print(_tip)
    print(_tip.to_type())
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


def constructor_tests():
    as_in = AbstractState.from_dict({'a': int, 'b': float})
    as_out = AbstractState.from_dict({'return': float})
    fspec = FunctionSpec(as_in, as_out)
    print(as_in)
    print(as_out)
    print(fspec)
    fspec = FunctionSpec.from_dict_tuple(
        ({'a': list[int], 'b': int | float}, {'return': str | list[int]})
    )
    print(fspec)
    T1 = TypeVar('T1')
    ss = create_basetype(int | T1)
    print(ss)

    bt1 = create_basetype(int)
    bt2 = create_basetype(int | float)
    bt3 = BaseType.lub(bt1, bt2)
    print(bt3)

    bt1 = create_basetype(int)
    bt2 = create_basetype(str | float)
    bt3 = BaseType.lub(bt1, bt2)
    print(bt3)


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


def constraint_tests():
    T1 = TypeVar('T1')
    bt1 = create_basetype(int)
    bt2 = create_basetype(T1)
    ct = Constraint(Relation.LEQ, bt1, bt2)
    print(ct)


def lesser_tests():
    bt1 = create_basetype(list)
    bt2 = create_basetype(typing.Sized)
    aux = bt1 <= bt2
    print(aux)
    bt1 = create_basetype(int)
    bt2 = create_basetype(int | float | str)
    aux = bt1 <= bt2
    print(aux)
    bt1 = create_basetype(list[int])
    bt2 = create_basetype(list[int | float | str])
    aux = bt1 <= bt2
    print(aux)
    bt1 = create_basetype(tuple[int, float])
    bt2 = create_basetype(tuple[int | float, float | str])
    aux = bt1 <= bt2
    print(aux)


if __name__ == "__main__":
    title = "Simple typing converter"
    print(title)
    print("=" * len(title))
    # str_tests()
    # encode_tests()
    # constructor_tests()
    # constraint_tests()
    lesser_tests()
