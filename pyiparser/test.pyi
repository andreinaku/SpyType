class list(MutableSequence[_T], Generic[_T]):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, __iterable: Iterable[_T]) -> None: ...
    def copy(self) -> list[_T]: ...
    def append(self, __object: _T) -> None: ...
    def extend(self, __iterable: Iterable[_T]) -> None: ...
    def pop(self, __index: SupportsIndex = -1) -> _T: ...
    # Signature of `list.index` should be kept in line with `collections.UserList.index()`
    # and multiprocessing.managers.ListProxy.index()
    def index(self, __value: _T, __start: SupportsIndex = 0, __stop: SupportsIndex = sys.maxsize) -> int: ...
    def count(self, __value: _T) -> int: ...
    def insert(self, __index: SupportsIndex, __object: _T) -> None: ...
    def remove(self, __value: _T) -> None: ...
    # Signature of `list.sort` should be kept inline with `collections.UserList.sort()`
    # and multiprocessing.managers.ListProxy.sort()
    #
    # Use list[SupportsRichComparisonT] for the first overload rather than [SupportsRichComparison]
    # to work around invariance
    @overload
    def sort(self: list[SupportsRichComparisonT], *, key: None = None, reverse: bool = False) -> None: ...
    @overload
    def sort(self, *, key: Callable[[_T], SupportsRichComparison], reverse: bool = False) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_T]: ...
    __hash__: ClassVar[None]  # type: ignore[assignment]
    @overload
    def __getitem__(self, __i: SupportsIndex) -> _T: ...
    def __getitem__(self, __i: SupportsIndex) -> _T: ...
    @overload
    def __getitem__(self, __s: slice) -> list[_T]: ...
    @overload
    def __setitem__(self, __key: SupportsIndex, __value: _T) -> None: ...
    @overload
    def __setitem__(self, __key: slice, __value: Iterable[_T]) -> None: ...
    def __delitem__(self, __key: SupportsIndex | slice) -> None: ...
    # Overloading looks unnecessary, but is needed to work around complex mypy problems
    @overload
    def __add__(self, __value: list[_T]) -> list[_T]: ...
    @overload
    def __add__(self, __value: list[_S]) -> list[_S | _T]: ...
    def __iadd__(self, __value: Iterable[_T]) -> Self: ...  # type: ignore[misc]
    def __mul__(self, __value: SupportsIndex) -> list[_T]: ...
    def __rmul__(self, __value: SupportsIndex) -> list[_T]: ...
    def __imul__(self, __value: SupportsIndex) -> Self: ...
    def __contains__(self, __key: object) -> bool: ...
    def __reversed__(self) -> Iterator[_T]: ...
    def __gt__(self, __value: list[_T]) -> bool: ...
    def __ge__(self, __value: list[_T]) -> bool: ...
    def __lt__(self, __value: list[_T]) -> bool: ...
    def __le__(self, __value: list[_T]) -> bool: ...
    def __eq__(self, __value: object) -> bool: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, __item: Any) -> GenericAlias: ...

class int:
    @overload
    def __new__(cls, __x: str | ReadableBuffer | SupportsInt | SupportsIndex | SupportsTrunc = ...) -> Self: ...
    @overload
    def __new__(cls, __x: str | bytes | bytearray, base: SupportsIndex) -> Self: ...
    if sys.version_info >= (3, 8):
        def as_integer_ratio(self) -> tuple[int, Literal[1]]: ...

    @property
    def real(self) -> int: ...
    @property
    def imag(self) -> Literal[0]: ...
    @property
    def numerator(self) -> int: ...
    @property
    def denominator(self) -> Literal[1]: ...
    def conjugate(self) -> int: ...
    def bit_length(self) -> int: ...
    if sys.version_info >= (3, 10):
        def bit_count(self) -> int: ...

    if sys.version_info >= (3, 11):
        def to_bytes(
            self, length: SupportsIndex = 1, byteorder: Literal["little", "big"] = "big", *, signed: bool = False
        ) -> bytes: ...
        @classmethod
        def from_bytes(
            cls,
            bytes: Iterable[SupportsIndex] | SupportsBytes | ReadableBuffer,
            byteorder: Literal["little", "big"] = "big",
            *,
            signed: bool = False,
        ) -> Self: ...
    else:
        def to_bytes(self, length: SupportsIndex, byteorder: Literal["little", "big"], *, signed: bool = False) -> bytes: ...
        @classmethod
        def from_bytes(
            cls,
            bytes: Iterable[SupportsIndex] | SupportsBytes | ReadableBuffer,
            byteorder: Literal["little", "big"],
            *,
            signed: bool = False,
        ) -> Self: ...

    if sys.version_info >= (3, 12):
        def is_integer(self) -> Literal[True]: ...

    def __add__(self, __value: int) -> int: ...
    def __sub__(self, __value: int) -> int: ...
    def __mul__(self, __value: int) -> int: ...
    def __floordiv__(self, __value: int) -> int: ...
    def __truediv__(self, __value: int) -> float: ...
    def __mod__(self, __value: int) -> int: ...
    def __divmod__(self, __value: int) -> tuple[int, int]: ...
    def __radd__(self, __value: int) -> int: ...
    def __rsub__(self, __value: int) -> int: ...
    def __rmul__(self, __value: int) -> int: ...
    def __rfloordiv__(self, __value: int) -> int: ...
    def __rtruediv__(self, __value: int) -> float: ...
    def __rmod__(self, __value: int) -> int: ...
    def __rdivmod__(self, __value: int) -> tuple[int, int]: ...
    @overload
    def __pow__(self, __x: Literal[0]) -> Literal[1]: ...
    @overload
    def __pow__(self, __value: Literal[0], __mod: None) -> Literal[1]: ...
    @overload
    def __pow__(self, __value: _PositiveInteger, __mod: None = None) -> int: ...
    @overload
    def __pow__(self, __value: _NegativeInteger, __mod: None = None) -> float: ...
    # positive x -> int; negative x -> float
    # return type must be Any as `int | float` causes too many false-positive errors
    @overload
    def __pow__(self, __value: int, __mod: None = None) -> Any: ...
    @overload
    def __pow__(self, __value: int, __mod: int) -> int: ...
    def __rpow__(self, __value: int, __mod: int | None = None) -> Any: ...
    def __and__(self, __value: int) -> int: ...
    def __or__(self, __value: int) -> int: ...
    def __xor__(self, __value: int) -> int: ...
    def __lshift__(self, __value: int) -> int: ...
    def __rshift__(self, __value: int) -> int: ...
    def __rand__(self, __value: int) -> int: ...
    def __ror__(self, __value: int) -> int: ...
    def __rxor__(self, __value: int) -> int: ...
    def __rlshift__(self, __value: int) -> int: ...
    def __rrshift__(self, __value: int) -> int: ...
    def __neg__(self) -> int: ...
    def __pos__(self) -> int: ...
    def __invert__(self) -> int: ...
    def __trunc__(self) -> int: ...
    def __ceil__(self) -> int: ...
    def __floor__(self) -> int: ...
    def __round__(self, __ndigits: SupportsIndex = ...) -> int: ...
    def __getnewargs__(self) -> tuple[int]: ...
    def __eq__(self, __value: object) -> bool: ...
    def __ne__(self, __value: object) -> bool: ...
    def __lt__(self, __value: int) -> bool: ...
    def __le__(self, __value: int) -> bool: ...
    def __gt__(self, __value: int) -> bool: ...
    def __ge__(self, __value: int) -> bool: ...
    def __float__(self) -> float: ...
    def __int__(self) -> int: ...
    def __abs__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def __index__(self) -> int: ...

class test:
    def func(self, a: int, b: int) -> int: ...
    def func(self, a: float, b: float) -> float: ...
    # def fifi(self: list[SupportsRichComparisonT], *, key: None = None, reverse: bool = False) -> None: ...
    def fifi(self: list[SupportsRichComparisonT], *, key: None = None, reverse: bool = False) -> None: ...