import ast
from pyiparser import pyiparse
from pyiparser.pyiparse import ClassDefParser
from Translator import Translator


test_dict = {
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
        r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ __key:SupportsIndex /\ T?r:NoneType)',
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
}


def translate_test():
    for _in, _expected in test_dict.items():
        selftype = _in[0]
        shed_spec = _in[1]
        funcdef_node = ast.parse(shed_spec).body[0]  # parse returns an ast.Module node
        spec_tuple = ClassDefParser.parse_FunctionDef(funcdef_node, selftype)
        abs_state = spec_tuple[1] + ' ^ ' + spec_tuple[2]
        aux = Translator.translate_as(abs_state)  # check that no exceptions raised while translating
        if abs_state != _expected:
            raise RuntimeError(f'Incorrect translation. Expected {_expected} and got {abs_state}')


def aux_test():
    func_str = r'def __delitem__(self, __key: SupportsIndex | slice) -> None: ...'
    func_node = ast.parse(func_str).body[0]
    spec_tuple = ClassDefParser.parse_FunctionDef(func_node, 'list<T?0>')
    abs_state = spec_tuple[1] + ' ^ ' + spec_tuple[2]
    pass


if __name__ == "__main__":
    # aux_test()
    translate_test()
