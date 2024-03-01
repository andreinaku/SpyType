class dict(MutableMapping[_KT, _VT], Generic[_KT, _VT]):
    # __init__ should be kept roughly in line with `collections.UserDict.__init__`, which has similar semantics
    # Also multiprocessing.managers.SyncManager.dict()
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self: dict[str, _VT], **kwargs: _VT) -> None: ...
    @overload
    def __init__(self, __map: SupportsKeysAndGetItem[_KT, _VT]) -> None: ...
    @overload
    def __init__(self: dict[str, _VT], __map: SupportsKeysAndGetItem[str, _VT], **kwargs: _VT) -> None: ...
    @overload
    def __init__(self, __iterable: Iterable[tuple[_KT, _VT]]) -> None: ...
    @overload
    def __init__(self: dict[str, _VT], __iterable: Iterable[tuple[str, _VT]], **kwargs: _VT) -> None: ...
    # Next two overloads are for dict(string.split(sep) for string in iterable)
    # Cannot be Iterable[Sequence[_T]] or otherwise dict(["foo", "bar", "baz"]) is not an error
    @overload
    def __init__(self: dict[str, str], __iterable: Iterable[list[str]]) -> None: ...
    @overload
    def __init__(self: dict[bytes, bytes], __iterable: Iterable[list[bytes]]) -> None: ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Self: ...
    def copy(self) -> dict[_KT, _VT]: ...
    def keys(self) -> dict_keys[_KT, _VT]: ...
    def values(self) -> dict_values[_KT, _VT]: ...
    def items(self) -> dict_items[_KT, _VT]: ...
    # Signature of `dict.fromkeys` should be kept identical to `fromkeys` methods of `OrderedDict`/`ChainMap`/`UserDict` in `collections`
    # TODO: the true signature of `dict.fromkeys` is not expressible in the current type system.
    # See #3800 & https://github.com/python/typing/issues/548#issuecomment-683336963.
    @classmethod
    @overload
    def fromkeys(cls, __iterable: Iterable[_T], __value: None = None) -> dict[_T, Any | None]: ...
    @classmethod
    @overload
    def fromkeys(cls, __iterable: Iterable[_T], __value: _S) -> dict[_T, _S]: ...
    # Positional-only in dict, but not in MutableMapping
    @overload  # type: ignore[override]
    def get(self, __key: _KT) -> _VT | None: ...
    @overload
    def get(self, __key: _KT, __default: _VT) -> _VT: ...
    @overload
    def get(self, __key: _KT, __default: _T) -> _VT | _T: ...
    @overload
    def pop(self, __key: _KT) -> _VT: ...
    @overload
    def pop(self, __key: _KT, __default: _VT) -> _VT: ...
    @overload
    def pop(self, __key: _KT, __default: _T) -> _VT | _T: ...
    def __len__(self) -> int: ...
    def __getitem__(self, __key: _KT) -> _VT: ...
    def __setitem__(self, __key: _KT, __value: _VT) -> None: ...
    def __delitem__(self, __key: _KT) -> None: ...
    def __iter__(self) -> Iterator[_KT]: ...
    def __eq__(self, __value: object) -> bool: ...
    if sys.version_info >= (3, 8):
        def __reversed__(self) -> Iterator[_KT]: ...
    __hash__: ClassVar[None]  # type: ignore[assignment]
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, __item: Any) -> GenericAlias: ...
        @overload
        def __or__(self, __value: dict[_KT, _VT]) -> dict[_KT, _VT]: ...
        @overload
        def __or__(self, __value: dict[_T1, _T2]) -> dict[_KT | _T1, _VT | _T2]: ...
        @overload
        def __ror__(self, __value: dict[_KT, _VT]) -> dict[_KT, _VT]: ...
        @overload
        def __ror__(self, __value: dict[_T1, _T2]) -> dict[_KT | _T1, _VT | _T2]: ...
        # dict.__ior__ should be kept roughly in line with MutableMapping.update()
        @overload  # type: ignore[misc]
        def __ior__(self, __value: SupportsKeysAndGetItem[_KT, _VT]) -> Self: ...
        @overload
        def __ior__(self, __value: Iterable[tuple[_KT, _VT]]) -> Self: ...