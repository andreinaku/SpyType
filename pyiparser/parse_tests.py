import logging
import ast
from pyiparser import pyiparse
from pyiparser.pyiparse import ClassDefParser
from Translator import Translator


logging.basicConfig(level=logging.INFO, filename='info.log', filemode='w', format='%(message)s')


test_dict = {
    # list
    ('list<T?0>', r'def __init__(self) -> None: ...'): r'self:T?1 /\ return:T?r ^ (T?1:list<T?0> /\ T?r:NoneType)',
    # def __init__(self, __iterable: Iterable[_T]) -> None: ... => self:T?1 /\ __iterable:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:Iterable<T?0> /\ T?r:NoneType)
    ('list<T?0>', r'def __init__(self, __iterable: Iterable[_T]) -> None: ...'):
        r'self:T?1 /\ __iterable:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:Iterable<T?0> /\ T?r:NoneType)',
    # def copy(self) -> list[_T]: ...
    ('list<T?0>', r'def copy(self) -> list[_T]: ...'):
        r'self:T?1 /\ return:T?r ^ (T?1:list<T?0> /\ T?r:list<T?0>)',
    # def append(self, __object: _T) -> None: ...
    ('list<T?0>', r'def append(self, __object: _T) -> None: ...'):
        r'self:T?1 /\ __object:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:T?0 /\ T?r:NoneType)',
    # def extend(self, __iterable: Iterable[_T]) -> None: ...
    ('list<T?0>', r'def extend(self, __iterable: Iterable[_T]) -> None: ...'):
        r'self:T?1 /\ __iterable:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:Iterable<T?0> /\ T?r:NoneType)',
    # def pop(self, __index: SupportsIndex = -1) -> _T: ...
    ('list<T?0>', r'def pop(self, __index: SupportsIndex = -1) -> _T: ...'):
        r'self:T?1 /\ __index:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?r:T?0)',
    # def index(self, __value: _T, __start: SupportsIndex = 0, __stop: SupportsIndex = sys.maxsize) -> int: ...
    ('list<T?0>',
     r'def index(self, __value: _T, __start: SupportsIndex = 0, __stop: SupportsIndex = sys.maxsize) -> int: ...'):
        r'self:T?1 /\ __value:T?2 /\ __start:T?3 /\ __stop:T?4 /\ return:T?r ^ '
        r'(T?1:list<T?0> /\ T?2:T?0 /\ T?3:SupportsIndex /\ T?4:SupportsIndex /\ T?r:int)',
    # def count(self, __value: _T) -> int: ...
    ('list<T?0>', r'def count(self, __value: _T) -> int: ...'):
        r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:T?0 /\ T?r:int)',
    # def insert(self, __index: SupportsIndex, __object: _T) -> None: ...
    ('list<T?0>', r'def insert(self, __index: SupportsIndex, __object: _T) -> None: ...'):
        r'self:T?1 /\ __index:T?2 /\ __object:T?3 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?3:T?0 /\ T?r:NoneType)',
    # def remove(self, __value: _T) -> None: ...
    ('list<T?0>', r'def remove(self, __value: _T) -> None: ...'):
        r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:T?0 /\ T?r:NoneType)',
    # def sort(self: list[SupportsRichComparisonT], *, key: None = None, reverse: bool = False) -> None: ...
    ('list<T?0>', r'def sort(self: list[SupportsRichComparisonT], *, key: None = None, reverse: bool = False) -> None: ...'):
        r'self:T?1 /\ __ko_key:T?2 /\ __ko_reverse:T?3 /\ return:T?r ^ '
        r'(T?1:list<SupportsRichComparisonT> /\ T?2:NoneType /\ T?3:bool /\ T?r:NoneType)',
    # @overload
    # def sort(self, *, key: Callable[[_T], SupportsRichComparison], reverse: bool = False) -> None: ...
    # def __len__(self) -> int: ...
    ('list<T?0>', r'def __len__(self) -> int: ...'):
        r'self:T?1 /\ return:T?r ^ (T?1:list<T?0> /\ T?r:int)',
    # def __iter__(self) -> Iterator[_T]: ...
    ('list<T?0>', r'def __iter__(self) -> Iterator[_T]: ...'):
        r'self:T?1 /\ return:T?r ^ (T?1:list<T?0> /\ T?r:Iterator<T?0>)',
    # __hash__: ClassVar[None]  # type: ignore[assignment]
    # @overload
    # def __getitem__(self, __i: SupportsIndex) -> _T: ...
    # def __getitem__(self, __i: SupportsIndex) -> _T: ...
    ('list<T?0>', r'def __getitem__(self, __i: SupportsIndex) -> _T: ...'):
        r'self:T?1 /\ __i:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?r:T?0)',
    # @overload
    # def __getitem__(self, __s: slice) -> list[_T]: ...
    # @overload
    # def __setitem__(self, __key: SupportsIndex, __value: _T) -> None: ...
    ('list<T?0>', r'def __setitem__(self, __key: SupportsIndex, __value: _T) -> None: ...'):
        r'self:T?1 /\ __key:T?2 /\ __value:T?3 /\ return:T?r ^ '
        r'(T?1:list<T?0> /\ T?2:SupportsIndex /\ T?3:T?0 /\ T?r:NoneType)',
    # @overload
    # def __setitem__(self, __key: slice, __value: Iterable[_T]) -> None: ...
    # def __delitem__(self, __key: SupportsIndex | slice) -> None: ...
    ('list<T?0>', r'def __delitem__(self, __key: SupportsIndex | slice) -> None: ...'):
        r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?r:NoneType)',
    # # Overloading looks unnecessary, but is needed to work around complex mypy problems
    # @overload
    # def __add__(self, __value: list[_T]) -> list[_T]: ...
    ('list<T?0>', r'def __add__(self, __value: list[_T]) -> list[_T]: ...'):
        r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:list<T?0> /\ T?r:list<T?0>)',
    # @overload
    # def __add__(self, __value: list[_S]) -> list[_S | _T]: ...
    ('list<T?0>', r'def __add__(self, __value: list[_S]) -> list[_S | _T]: ...'):
        r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:list<T?s> /\ T?r:list<T?0+T?s>)',
    # def __iadd__(self, __value: Iterable[_T]) -> Self: ...  # type: ignore[misc]
    ('list<T?0>', r'def __iadd__(self, __value: Iterable[_T]) -> Self: ...'):
        r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:Iterable<T?0> /\ T?r:list<T?0>)',
    # def __mul__(self, __value: SupportsIndex) -> list[_T]: ...
    ('list<T?0>', r'def __mul__(self, __value: SupportsIndex) -> list[_T]: ...'):
        r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?r:list<T?0>)',
    # def __rmul__(self, __value: SupportsIndex) -> list[_T]: ...
    # def __imul__(self, __value: SupportsIndex) -> Self: ...
    ('list<T?0>', r'def __imul__(self, __value: SupportsIndex) -> Self: ...'):
        r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?r:list<T?0>)',
    # def __contains__(self, __key: object) -> bool: ...
    ('list<T?0>', r'def __contains__(self, __key: object) -> bool: ...'):
        r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:TopType /\ T?r:bool)',
    # def __reversed__(self) -> Iterator[_T]: ...
    ('list<T?0>', r'def __reversed__(self) -> Iterator[_T]: ...'):
        r'self:T?1 /\ return:T?r ^ (T?1:list<T?0> /\ T?r:Iterator<T?0>)',
    # def __gt__(self, __value: list[_T]) -> bool: ...
    ('list<T?0>', r'def __gt__(self, __value: list[_T]) -> bool: ...'):
        r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:list<T?0> /\ T?r:bool)',
    # def __ge__(self, __value: list[_T]) -> bool: ...
    # def __lt__(self, __value: list[_T]) -> bool: ...
    # def __le__(self, __value: list[_T]) -> bool: ...
    # def __eq__(self, __value: object) -> bool: ...
    ('list<T?0>', r'def __eq__(self, __value: object) -> bool: ...'):
        r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:TopType /\ T?r:bool)',
    #
    # int
    #
    # @overload
    # def __new__(cls, __x: str | ReadableBuffer | SupportsInt | SupportsIndex | SupportsTrunc = ...) -> Self: ...
    ('int', r'def __new__(cls, __x: str | ReadableBuffer | SupportsInt | SupportsIndex | SupportsTrunc = ...) -> Self: ...'):
        r'cls:T?1 /\ __x:T?2 /\ return:T?r ^ '
        r'(T?1:int /\ T?2:str+bytes+bytearray+memoryview+SupportsInt+SupportsIndex+SupportsTrunc /\ T?r:int)',
    # @overload
    # def __new__(cls, __x: str | bytes | bytearray, base: SupportsIndex) -> Self: ...
    ('int', r'def __new__(cls, __x: str | bytes | bytearray, base: SupportsIndex) -> Self: ...'):
        r'cls:T?1 /\ __x:T?2 /\ base:T?3 /\ return:T?r ^ '
        r'(T?1:int /\ T?2:str+bytes+bytearray /\ T?3:SupportsIndex /\ T?r:int)',
    # if sys.version_info >= (3, 8):
    #     def as_integer_ratio(self) -> tuple[int, Literal[1]]: ...
    #
    # @property
    # def real(self) -> int: ...
    # @property
    # def imag(self) -> Literal[0]: ...
    # @property
    # def numerator(self) -> int: ...
    # @property
    # def denominator(self) -> Literal[1]: ...
    # def conjugate(self) -> int: ...
    # def bit_length(self) -> int: ...
    # if sys.version_info >= (3, 10):
    #     def bit_count(self) -> int: ...
    #
    # if sys.version_info >= (3, 11):
    #     def to_bytes(
    #         self, length: SupportsIndex = 1, byteorder: Literal["little", "big"] = "big", *, signed: bool = False
    #     ) -> bytes: ...
    #     @classmethod
    #     def from_bytes(
    #         cls,
    #         bytes: Iterable[SupportsIndex] | SupportsBytes | ReadableBuffer,
    #         byteorder: Literal["little", "big"] = "big",
    #         *,
    #         signed: bool = False,
    #     ) -> Self: ...
    # else:
    #     def to_bytes(self, length: SupportsIndex, byteorder: Literal["little", "big"], *, signed: bool = False) -> bytes: ...
    #     @classmethod
    #     def from_bytes(
    #         cls,
    #         bytes: Iterable[SupportsIndex] | SupportsBytes | ReadableBuffer,
    #         byteorder: Literal["little", "big"],
    #         *,
    #         signed: bool = False,
    #     ) -> Self: ...
    #
    # if sys.version_info >= (3, 12):
    #     def is_integer(self) -> Literal[True]: ...
    #
    # def __add__(self, __value: int) -> int: ...
    # def __sub__(self, __value: int) -> int: ...
    # def __mul__(self, __value: int) -> int: ...
    # def __floordiv__(self, __value: int) -> int: ...
    # def __truediv__(self, __value: int) -> float: ...
    # def __mod__(self, __value: int) -> int: ...
    # def __divmod__(self, __value: int) -> tuple[int, int]: ...
    # def __radd__(self, __value: int) -> int: ...
    # def __rsub__(self, __value: int) -> int: ...
    # def __rmul__(self, __value: int) -> int: ...
    # def __rfloordiv__(self, __value: int) -> int: ...
    # def __rtruediv__(self, __value: int) -> float: ...
    # def __rmod__(self, __value: int) -> int: ...
    # def __rdivmod__(self, __value: int) -> tuple[int, int]: ...
    # @overload
    # def __pow__(self, __x: Literal[0]) -> Literal[1]: ...
    # @overload
    # def __pow__(self, __value: Literal[0], __mod: None) -> Literal[1]: ...
    # @overload
    # def __pow__(self, __value: _PositiveInteger, __mod: None = None) -> int: ...
    # @overload
    # def __pow__(self, __value: _NegativeInteger, __mod: None = None) -> float: ...
    # # positive x -> int; negative x -> float
    # # return type must be Any as `int | float` causes too many false-positive errors
    # @overload
    # def __pow__(self, __value: int, __mod: None = None) -> Any: ...
    # @overload
    # def __pow__(self, __value: int, __mod: int) -> int: ...
    # def __rpow__(self, __value: int, __mod: int | None = None) -> Any: ...
    # def __and__(self, __value: int) -> int: ...
    # def __or__(self, __value: int) -> int: ...
    # def __xor__(self, __value: int) -> int: ...
    # def __lshift__(self, __value: int) -> int: ...
    # def __rshift__(self, __value: int) -> int: ...
    # def __rand__(self, __value: int) -> int: ...
    # def __ror__(self, __value: int) -> int: ...
    # def __rxor__(self, __value: int) -> int: ...
    # def __rlshift__(self, __value: int) -> int: ...
    # def __rrshift__(self, __value: int) -> int: ...
    # def __neg__(self) -> int: ...
    # def __pos__(self) -> int: ...
    # def __invert__(self) -> int: ...
    # def __trunc__(self) -> int: ...
    # def __ceil__(self) -> int: ...
    # def __floor__(self) -> int: ...
    # def __round__(self, __ndigits: SupportsIndex = ...) -> int: ...
    # def __getnewargs__(self) -> tuple[int]: ...
    # def __eq__(self, __value: object) -> bool: ...
    # def __ne__(self, __value: object) -> bool: ...
    # def __lt__(self, __value: int) -> bool: ...
    # def __le__(self, __value: int) -> bool: ...
    # def __gt__(self, __value: int) -> bool: ...
    # def __ge__(self, __value: int) -> bool: ...
    # def __float__(self) -> float: ...
    # def __int__(self) -> int: ...
    # def __abs__(self) -> int: ...
    # def __hash__(self) -> int: ...
    # def __bool__(self) -> bool: ...
    # def __index__(self) -> int: ...
}


def translate_test():
    for _in, _expected in test_dict.items():
        selftype = _in[0]
        shed_spec = _in[1]
        funcdef_node = ast.parse(shed_spec).body[0]  # parse returns an ast.Module node
        spec_tuple = ClassDefParser.parse_FunctionDef(funcdef_node, selftype)
        abs_state = spec_tuple[1] + ' ^ ' + spec_tuple[2]
        aux = Translator.translate_as(abs_state)  # check that no exceptions raised while translating
        aux2 = Translator.translate_as(_expected)
        if abs_state != _expected:
            logging.info(f'Hash compare needed for:\n\t{_expected}\n\t{abs_state}\n')
            if hash(aux) != hash(aux2):
                raise RuntimeError(f'Incorrect translation. Expected {_expected} and got {abs_state}')


def aux_test():
    func_str = r'def __new__(cls, __x: str | ReadableBuffer | SupportsInt | SupportsIndex | SupportsTrunc = ...) -> Self: ...'
    func_node = ast.parse(func_str).body[0]
    spec_tuple = ClassDefParser.parse_FunctionDef(func_node, 'list<T?0>')
    abs_state = spec_tuple[1] + ' ^ ' + spec_tuple[2]
    aux = Translator.translate_as(abs_state)
    pass


if __name__ == "__main__":
    # aux_test()
    translate_test()
