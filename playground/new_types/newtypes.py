from __future__ import annotations
from types import *
from typing import *
from copy import deepcopy


class Basetype:
    def __init__(self, tip):
        if isinstance(tip, UnionType):
            self.tip = deepcopy(tip)
        elif isinstance(tip, type):
            self.__args__ = (tip,)
        elif isinstance(tip, TypeVar):
            self.__args__ = (tip,)
        else:
            raise RuntimeError(f"{tip} not a supported Basetype")


if __name__ == "__main__":
    code = "list[int] | int"
    x = eval(code)
    bt = Basetype(x)
    print(bt)
