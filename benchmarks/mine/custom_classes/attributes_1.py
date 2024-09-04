from typing import ClassVar


class foo:
    x: int
    __hash__: ClassVar[None]
    
    def __init__(self) -> None:
        self.y = 3.5
