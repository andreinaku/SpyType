import ast

fooclass = '''
class foo:
    x: int
    __hash__: ClassVar[None]
    
    def __init__(self, y: int) -> None:
        self.y = 3.5
'''

objectclass = '''
class object:
    __doc__: str | None
    __dict__: dict[str, Any]
    __module__: str
    __annotations__: dict[str, Any]
    @property
    def __class__(self) -> type[Self]: ...
    # Ignore errors about type mismatch between property getter and setter
    @__class__.setter
    def __class__(self, __type: type[object]) -> None: ...  # noqa: F811
    def __init__(self) -> None: ...
    def __new__(cls) -> Self: ...
    # N.B. `object.__setattr__` and `object.__delattr__` are heavily special-cased by type checkers.
    # Overriding them in subclasses has different semantics, even if the override has an identical signature.
    def __setattr__(self, __name: str, __value: Any) -> None: ...
    def __delattr__(self, __name: str) -> None: ...
    def __eq__(self, __value: object) -> bool: ...
    def __ne__(self, __value: object) -> bool: ...
    def __str__(self) -> str: ...  # noqa: Y029
    def __repr__(self) -> str: ...  # noqa: Y029
    def __hash__(self) -> int: ...
    def __format__(self, __format_spec: str) -> str: ...
    def __getattribute__(self, __name: str) -> Any: ...
    def __sizeof__(self) -> int: ...
    # return type of pickle methods is rather hard to express in the current type system
    # see #6661 and https://docs.python.org/3/library/pickle.html#object.__reduce__
    def __reduce__(self) -> str | tuple[Any, ...]: ...
    if sys.version_info >= (3, 8):
        def __reduce_ex__(self, __protocol: SupportsIndex) -> str | tuple[Any, ...]: ...
    else:
        def __reduce_ex__(self, __protocol: int) -> str | tuple[Any, ...]: ...
    if sys.version_info >= (3, 11):
        def __getstate__(self) -> object: ...

    def __dir__(self) -> Iterable[str]: ...
    def __init_subclass__(cls) -> None: ...
    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool: ...
'''

inherit_1 = '''
class A:
    def __init__(self, x):
        self.x = x


class B(A):
    pass
'''

tree = ast.parse(fooclass)
print(ast.dump(tree, indent=4))
