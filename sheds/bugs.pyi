class type:
    @overload
    def __new__(
        cls: type[_typeshed.Self], __name: str, __bases: tuple[type, ...], __namespace: dict[str, Any], **kwds: Any
    ) -> _typeshed.Self: ...
