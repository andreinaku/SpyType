class reversed(Iterator[_T], Generic[_T]):
    @overload
    def __init__(self, __sequence: SupportsLenAndGetItem[_T]) -> None: ...
