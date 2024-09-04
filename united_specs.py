import ast

op_equiv = {
    ast.UnaryOp: {
        ast.UAdd: '__pos__',
        ast.USub: '__neg__',
        ast.Not: '__bool__',
        ast.Invert: '__invert__',
    },
    ast.BinOp: {
        ast.Add: '__add__',
        ast.Sub: '__sub__',
        ast.Mult: '__mul__',
        ast.Div: '__truediv__',
        ast.FloorDiv: '__floordiv__',
        ast.Mod: '__mod__',
        ast.Pow: '__pow__',
        ast.LShift: '__lshift__',
        ast.RShift: '__rshift__',
        ast.BitOr: '__or__',
        ast.BitXor: '__xor__',
        ast.BitAnd: '__and__',
        ast.MatMult: '__matmul__',
    },
}


unitedspecs = {
    '__class__': {
        r'((self:top /\ __type:top) -> (return:NoneType))',
        r'((self:top) -> (return:top))',
    },
    '__init__': {
        r'((self:list < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
        r'((self:dict < bytes, bytes > /\ __iterable:top) -> (return:NoneType))',
        r'((self:set < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
        r'((self:set < T?0 >) -> (return:NoneType))',
        r'((self:bytearray /\ __string:str /\ encoding:str /\ __d_errors:str) -> (return:NoneType))',
        r'((self:dict < str, T?2 > /\ __iterable:top /\ __kw_kwargs:T?2) -> (return:NoneType))',
        r'((self:bytearray /\ __ints:memoryview + Iterable < SupportsIndex > + bytearray + bytes + SupportsIndex) -> (return:NoneType))',
        r'((self:range < int > /\ __start:SupportsIndex /\ __stop:SupportsIndex /\ __d___step:SupportsIndex) -> (return:NoneType))',
        r'((self:dict < str, str > /\ __iterable:top) -> (return:NoneType))',
        r'((self:memoryview < int > /\ obj:bytearray + bytes + memoryview) -> (return:NoneType))',
        r'((self:range < int > /\ __stop:SupportsIndex) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __iterable:top) -> (return:NoneType))',
        r'((self:dict < str, T?2 > /\ __kw_kwargs:T?2) -> (return:NoneType))',
        r'((self:bytearray) -> (return:NoneType))',
        r'((self:dict < str, T?2 > /\ __map:dict < str, T?2 > /\ __kw_kwargs:T?2) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 >) -> (return:NoneType))',
        r'((self:list < T?0 >) -> (return:NoneType))',
        r'((self:top) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __map:dict < T?1, T?2 >) -> (return:NoneType))',
        r'((self:frozenset < T?3 > /\ iterable:Iterable < T?0 > /\ __d_start:int) -> (return:NoneType))',
    },
    '__new__': {
        r'((cls:top /\ __iterable:Iterable < T?3 >) -> (return:frozenset < T?3 >))',
        r'((cls:top /\ __d___iterable:Iterable < T?3 >) -> (return:tuple < T?3 >))',
        r'((cls:top /\ __d_object:top) -> (return:str))',
        r'((cls:top /\ __string:str /\ encoding:str /\ __d_errors:str) -> (return:bytes))',
        r'((cls:top) -> (return:bytes))',
        r'((cls:top /\ __va_args:top /\ __kw_kwargs:top) -> (return:dict < T?1, T?2 >))',
        r'((cls:top /\ __x:bytearray + bytes + str /\ base:SupportsIndex) -> (return:int))',
        r'((cls:top /\ __d___o:top) -> (return:bool))',
        r'((cls:top /\ object:bytearray + bytes + memoryview /\ __d_encoding:str /\ __d_errors:str) -> (return:str))',
        r'((cls:top) -> (return:top))',
        r'((cls:top /\ __name:str /\ __bases:tuple /\ __namespace:dict < str, top > /\ __kw_kwds:top) -> (return:top))',
        r'((cls:top /\ __d___x:memoryview + bytearray + bytes + SupportsIndex + top + SupportsInt + str) -> (return:int))',
        r'((cls:top) -> (return:frozenset < T?3 >))',
        r'((cls:top /\ __d___x:memoryview + SupportsFloat + bytearray + bytes + SupportsIndex + str) -> (return:float))',
        r'((cls:top /\ __o:memoryview + Iterable < SupportsIndex > + bytearray + bytes + SupportsIndex + SupportsBytes) -> (return:bytes))',
    },
    '__setattr__': {
        r'((self:top /\ __name:str /\ __value:top) -> (return:NoneType))',
    },
    '__delattr__': {
        r'((self:top /\ __name:str) -> (return:NoneType))',
    },
    '__eq__': {
        r'((self:tuple < T?3 > /\ __value:top) -> (return:bool))',
        r'((self:float /\ __value:top) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:top) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:top) -> (return:bool))',
        r'((self:bytearray /\ __value:top) -> (return:bool))',
        r'((self:range < int > /\ __value:top) -> (return:bool))',
        r'((self:dict < T?1, T?2 > /\ __value:top) -> (return:bool))',
        r'((self:top /\ __value:top) -> (return:bool))',
        r'((self:bytes /\ __value:top) -> (return:bool))',
        r'((self:memoryview < int > /\ __value:top) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:top) -> (return:bool))',
        r'((self:int /\ __value:top) -> (return:bool))',
        r'((self:str /\ __value:top) -> (return:bool))',
        r'((self:complex /\ __value:top) -> (return:bool))',
    },
    '__ne__': {
        r'((self:float /\ __value:top) -> (return:bool))',
        r'((self:bytearray /\ __value:top) -> (return:bool))',
        r'((self:top /\ __value:top) -> (return:bool))',
        r'((self:bytes /\ __value:top) -> (return:bool))',
        r'((self:int /\ __value:top) -> (return:bool))',
        r'((self:str /\ __value:top) -> (return:bool))',
        r'((self:complex /\ __value:top) -> (return:bool))',
    },
    '__str__': {
        r'((self:top) -> (return:str))',
    },
    '__repr__': {
        r'((self:top) -> (return:str))',
    },
    '__hash__': {
        r'((self:top) -> (return:int))',
        r'((self:str) -> (return:int))',
        r'((self:complex) -> (return:int))',
        r'((self:range < int >) -> (return:int))',
        r'((self:tuple < T?3 >) -> (return:int))',
        r'((self:frozenset < T?3 >) -> (return:int))',
        r'((self:memoryview < int >) -> (return:int))',
        r'((self:float) -> (return:int))',
        r'((self:int) -> (return:int))',
        r'((self:bytes) -> (return:int))',
    },
    '__format__': {
        r'((self:top /\ __format_spec:str) -> (return:str))',
    },
    '__getattribute__': {
        r'((self:top /\ __name:str) -> (return:top))',
    },
    '__sizeof__': {
        r'((self:top) -> (return:int))',
    },
    '__reduce__': {
        r'((self:top) -> (return:str + tuple < top >))',
    },
    '__dir__': {
        r'((self:top) -> (return:Iterable < str >))',
    },
    '__init_subclass__': {
        r'((cls:top) -> (return:NoneType))',
    },
    '__subclasses__': {
        r'((self:top) -> (return:top))',
    },
    '__prepare__': {
        r'((metacls:top /\ __name:str /\ __bases:tuple /\ __kw_kwds:top) -> (return:Mapping < str, top >))',
    },
    'real': {
        r'((self:float) -> (return:float))',
        r'((self:complex) -> (return:float))',
        r'((self:int) -> (return:int))',
    },
    'imag': {
        r'((self:int) -> (return:top))',
        r'((self:complex) -> (return:float))',
        r'((self:float) -> (return:float))',
    },
    'numerator': {
        r'((self:int) -> (return:int))',
    },
    'denominator': {
        r'((self:int) -> (return:top))',
    },
    'conjugate': {
        r'((self:float) -> (return:float))',
        r'((self:complex) -> (return:complex))',
        r'((self:int) -> (return:int))',
    },
    'bit_length': {
        r'((self:int) -> (return:int))',
    },
    '__add__': {
        r'((self:bytes /\ __value:bytearray + bytes + memoryview) -> (return:bytes))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:tuple < T?3 >))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bytearray))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?0 >) -> (return:tuple < T?3 + T?0 >))',
        r'((self:str /\ __value:str) -> (return:str))',
        r'((self:list < T?0 > /\ __value:list < T?4 >) -> (return:list < T?0 + T?4 >))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:list < T?0 >))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__sub__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:frozenset < T?3 > /\ __value:set < T?3 >) -> (return:frozenset < T?3 >))',
        r'((self:set < T?0 > /\ __value:set < NoneType + T?0 >) -> (return:set < T?0 >))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__mul__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
        r'((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
        r'((self:bytes /\ __value:SupportsIndex) -> (return:bytes))',
        r'((self:str /\ __value:SupportsIndex) -> (return:str))',
        r'((self:tuple < T?3 > /\ __value:SupportsIndex) -> (return:tuple < T?3 >))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__floordiv__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__truediv__': {
        r'((self:int /\ __value:int) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__mod__': {
        r'((self:bytearray /\ __value:top) -> (return:bytes))',
        r'((self:bytes /\ __value:top) -> (return:bytes))',
        r'((self:str /\ __value:str + tuple < str >) -> (return:str))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:str /\ __value:top) -> (return:str))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__divmod__': {
        r'((self:int /\ __value:int) -> (return:tuple < int >))',
        r'((self:float /\ __value:float) -> (return:tuple < float >))',
    },
    '__radd__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rsub__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rmul__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
        r'((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
        r'((self:bytes /\ __value:SupportsIndex) -> (return:bytes))',
        r'((self:str /\ __value:SupportsIndex) -> (return:str))',
        r'((self:tuple < T?3 > /\ __value:SupportsIndex) -> (return:tuple < T?3 >))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rfloordiv__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rtruediv__': {
        r'((self:int /\ __value:int) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rmod__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rdivmod__': {
        r'((self:int /\ __value:int) -> (return:tuple < int >))',
        r'((self:float /\ __value:float) -> (return:tuple < float >))',
    },
    '__pow__': {
        r'((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:int))',
        r'((self:int /\ __value:int /\ __mod:int) -> (return:int))',
        r'((self:int /\ __value:top /\ __mod:NoneType) -> (return:top))',
        r'((self:float /\ __value:float /\ __d___mod:NoneType) -> (return:top))',
        r'((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:top))',
        r'((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
        r'((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
        r'((self:int /\ __x:top) -> (return:top))',
        r'((self:complex /\ __value:complex /\ __d___mod:NoneType) -> (return:complex))',
    },
    '__rpow__': {
        r'((self:float /\ __value:float /\ __d___mod:NoneType) -> (return:top))',
        r'((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:complex))',
        r'((self:int /\ __value:int /\ __d___mod:int + NoneType) -> (return:top))',
        r'((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
        r'((self:complex /\ __value:complex /\ __d___mod:NoneType) -> (return:complex))',
    },
    '__and__': {
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:frozenset < T?3 > /\ __value:set < T?3 >) -> (return:frozenset < T?3 >))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:set < T?0 >))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__or__': {
        r'((self:frozenset < T?3 > /\ __value:set < T?4 >) -> (return:frozenset < T?3 + T?4 >))',
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:set < T?0 > /\ __value:set < T?4 >) -> (return:set < T?0 + T?4 >))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__xor__': {
        r'((self:frozenset < T?3 > /\ __value:set < T?4 >) -> (return:frozenset < T?3 + T?4 >))',
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:set < T?0 > /\ __value:set < T?4 >) -> (return:set < T?0 + T?4 >))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__lshift__': {
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rshift__': {
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rand__': {
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
    },
    '__ror__': {
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
    },
    '__rxor__': {
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
    },
    '__rlshift__': {
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rrshift__': {
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__neg__': {
        r'((self:float) -> (return:float))',
        r'((self:complex) -> (return:complex))',
        r'((self:int) -> (return:int))',
    },
    '__pos__': {
        r'((self:float) -> (return:float))',
        r'((self:complex) -> (return:complex))',
        r'((self:int) -> (return:int))',
    },
    '__invert__': {
        r'((self:int) -> (return:int))',
    },
    '__trunc__': {
        r'((self:float) -> (return:int))',
        r'((self:int) -> (return:int))',
    },
    '__ceil__': {
        r'((self:int) -> (return:int))',
    },
    '__floor__': {
        r'((self:int) -> (return:int))',
    },
    '__round__': {
        r'((self:float /\ __ndigits:SupportsIndex) -> (return:float))',
        r'((self:float /\ __d___ndigits:NoneType) -> (return:int))',
        r'((self:int /\ __d___ndigits:SupportsIndex) -> (return:int))',
    },
    '__getnewargs__': {
        r'((self:str) -> (return:tuple < str >))',
        r'((self:int) -> (return:tuple < int >))',
        r'((self:bool) -> (return:tuple < int >))',
        r'((self:float) -> (return:tuple < float >))',
        r'((self:bytes) -> (return:tuple < bytes >))',
    },
    '__lt__': {
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
    },
    '__le__': {
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
    },
    '__gt__': {
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
    },
    '__ge__': {
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
    },
    '__float__': {
        r'((self:float) -> (return:float))',
        r'((self:int) -> (return:float))',
    },
    '__int__': {
        r'((self:float) -> (return:int))',
        r'((self:int) -> (return:int))',
    },
    '__abs__': {
        r'((self:float) -> (return:float))',
        r'((self:complex) -> (return:float))',
        r'((self:int) -> (return:int))',
    },
    '__bool__': {
        r'((self:float) -> (return:bool))',
        r'((self:complex) -> (return:bool))',
        r'((self:int) -> (return:bool))',
    },
    '__index__': {
        r'((self:int) -> (return:int))',
    },
    'as_integer_ratio': {
        r'((self:float) -> (return:tuple < int >))',
    },
    'hex': {
        r'((self:float) -> (return:str))',
        r'((__number:int + SupportsIndex) -> (return:str))',
    },
    'is_integer': {
        r'((self:float) -> (return:bool))',
    },
    'fromhex': {
        r'((cls:top /\ __string:str) -> (return:float))',
        r'((cls:top /\ __string:str) -> (return:bytes))',
        r'((cls:top /\ __string:str) -> (return:bytearray))',
    },
    'capitalize': {
        r'((self:str) -> (return:str))',
        r'((self:bytes) -> (return:bytes))',
        r'((self:bytearray) -> (return:bytearray))',
    },
    'casefold': {
        r'((self:str) -> (return:str))',
    },
    'center': {
        r'((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytes) -> (return:bytearray))',
        r'((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytes) -> (return:bytes))',
        r'((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
    },
    'count': {
        r'((self:list < T?0 > /\ __value:T?0) -> (return:int))',
        r'((self:bytes /\ __sub:bytearray + bytes + memoryview + SupportsIndex /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __sub:bytearray + bytes + memoryview + SupportsIndex /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:range < int > /\ __value:int) -> (return:int))',
        r'((self:tuple < T?3 > /\ __value:top) -> (return:int))',
        r'((self:str /\ x:str /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
    },
    'encode': {
        r'((self:str /\ __d_encoding:str /\ __d_errors:str) -> (return:bytes))',
    },
    'endswith': {
        r'((self:bytearray /\ __suffix:bytearray + bytes + memoryview + tuple < bytearray + bytes + memoryview > /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:bool))',
        r'((self:bytes /\ __suffix:bytearray + bytes + memoryview + tuple < bytearray + bytes + memoryview > /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:bool))',
        r'((self:str /\ __suffix:str + tuple < str > /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:bool))',
    },
    'find': {
        r'((self:str /\ __sub:str /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytes /\ __sub:bytearray + bytes + memoryview + SupportsIndex /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __sub:bytearray + bytes + memoryview + SupportsIndex /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
    },
    'format': {
        r'((__value:top /\ __d___format_spec:str) -> (return:str))',
        r'((self:memoryview < int >) -> (return:str))',
        r'((self:str /\ __va_args:str /\ __kw_kwargs:str) -> (return:str))',
        r'((self:str /\ __va_args:top /\ __kw_kwargs:top) -> (return:str))',
    },
    'format_map': {
        r'((self:str /\ map:dict < str, int >) -> (return:str))',
    },
    'index': {
        r'((self:str /\ __sub:str /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytes /\ __sub:bytearray + bytes + memoryview + SupportsIndex /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __sub:bytearray + bytes + memoryview + SupportsIndex /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:list < T?0 > /\ __value:T?0 /\ __d___start:SupportsIndex /\ __d___stop:SupportsIndex) -> (return:int))',
        r'((self:range < int > /\ __value:int) -> (return:int))',
        r'((self:tuple < T?3 > /\ __value:top /\ __d___start:SupportsIndex /\ __d___stop:SupportsIndex) -> (return:int))',
    },
    'isalnum': {
        r'((self:str) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'isalpha': {
        r'((self:str) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'isascii': {
        r'((self:str) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'isdecimal': {
        r'((self:str) -> (return:bool))',
    },
    'isdigit': {
        r'((self:str) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'isidentifier': {
        r'((self:str) -> (return:bool))',
    },
    'islower': {
        r'((self:str) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'isnumeric': {
        r'((self:str) -> (return:bool))',
    },
    'isprintable': {
        r'((self:str) -> (return:bool))',
    },
    'isspace': {
        r'((self:str) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'istitle': {
        r'((self:str) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'isupper': {
        r'((self:str) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'join': {
        r'((self:bytearray /\ __iterable_of_bytes:Iterable < bytearray + bytes + memoryview >) -> (return:bytearray))',
        r'((self:str /\ __iterable:Iterable < str >) -> (return:str))',
        r'((self:bytes /\ __iterable_of_bytes:Iterable < bytearray + bytes + memoryview >) -> (return:bytes))',
    },
    'ljust': {
        r'((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytearray + bytes) -> (return:bytearray))',
        r'((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
        r'((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytearray + bytes) -> (return:bytes))',
    },
    'lower': {
        r'((self:str) -> (return:str))',
        r'((self:bytes) -> (return:bytes))',
        r'((self:bytearray) -> (return:bytearray))',
    },
    'lstrip': {
        r'((self:bytearray /\ __d___bytes:bytearray + bytes + memoryview + NoneType) -> (return:bytearray))',
        r'((self:str /\ __d___chars:str + NoneType) -> (return:str))',
        r'((self:bytes /\ __d___bytes:bytearray + bytes + memoryview + NoneType) -> (return:bytes))',
    },
    'partition': {
        r'((self:str /\ __sep:str) -> (return:tuple < str >))',
        r'((self:bytes /\ __sep:bytearray + bytes + memoryview) -> (return:tuple < bytes >))',
        r'((self:bytearray /\ __sep:bytearray + bytes + memoryview) -> (return:tuple < bytearray >))',
    },
    'replace': {
        r'((self:str /\ __old:str /\ __new:str /\ __d___count:SupportsIndex) -> (return:str))',
        r'((self:bytes /\ __old:bytearray + bytes + memoryview /\ __new:bytearray + bytes + memoryview /\ __d___count:SupportsIndex) -> (return:bytes))',
        r'((self:bytearray /\ __old:bytearray + bytes + memoryview /\ __new:bytearray + bytes + memoryview /\ __d___count:SupportsIndex) -> (return:bytearray))',
    },
    'rfind': {
        r'((self:str /\ __sub:str /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytes /\ __sub:bytearray + bytes + memoryview + SupportsIndex /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __sub:bytearray + bytes + memoryview + SupportsIndex /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
    },
    'rindex': {
        r'((self:str /\ __sub:str /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytes /\ __sub:bytearray + bytes + memoryview + SupportsIndex /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __sub:bytearray + bytes + memoryview + SupportsIndex /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
    },
    'rjust': {
        r'((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytearray + bytes) -> (return:bytearray))',
        r'((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
        r'((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytearray + bytes) -> (return:bytes))',
    },
    'rpartition': {
        r'((self:str /\ __sep:str) -> (return:tuple < str >))',
        r'((self:bytes /\ __sep:bytearray + bytes + memoryview) -> (return:tuple < bytes >))',
        r'((self:bytearray /\ __sep:bytearray + bytes + memoryview) -> (return:tuple < bytearray >))',
    },
    'rsplit': {
        r'((self:str /\ __d_sep:str + NoneType /\ __d_maxsplit:SupportsIndex) -> (return:list < str >))',
        r'((self:bytearray /\ __d_sep:bytearray + bytes + memoryview + NoneType /\ __d_maxsplit:SupportsIndex) -> (return:list < bytearray >))',
        r'((self:bytes /\ __d_sep:bytearray + bytes + memoryview + NoneType /\ __d_maxsplit:SupportsIndex) -> (return:list < bytes >))',
    },
    'rstrip': {
        r'((self:bytearray /\ __d___bytes:bytearray + bytes + memoryview + NoneType) -> (return:bytearray))',
        r'((self:str /\ __d___chars:str + NoneType) -> (return:str))',
        r'((self:bytes /\ __d___bytes:bytearray + bytes + memoryview + NoneType) -> (return:bytes))',
    },
    'split': {
        r'((self:str /\ __d_sep:str + NoneType /\ __d_maxsplit:SupportsIndex) -> (return:list < str >))',
        r'((self:bytearray /\ __d_sep:bytearray + bytes + memoryview + NoneType /\ __d_maxsplit:SupportsIndex) -> (return:list < bytearray >))',
        r'((self:bytes /\ __d_sep:bytearray + bytes + memoryview + NoneType /\ __d_maxsplit:SupportsIndex) -> (return:list < bytes >))',
    },
    'splitlines': {
        r'((self:bytearray /\ __d_keepends:bool) -> (return:list < bytearray >))',
        r'((self:bytes /\ __d_keepends:bool) -> (return:list < bytes >))',
        r'((self:str /\ __d_keepends:bool) -> (return:list < str >))',
    },
    'startswith': {
        r'((self:bytearray /\ __prefix:bytearray + bytes + memoryview + tuple < bytearray + bytes + memoryview > /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:bool))',
        r'((self:str /\ __prefix:str + tuple < str > /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:bool))',
        r'((self:bytes /\ __prefix:bytearray + bytes + memoryview + tuple < bytearray + bytes + memoryview > /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:bool))',
    },
    'strip': {
        r'((self:bytearray /\ __d___bytes:bytearray + bytes + memoryview + NoneType) -> (return:bytearray))',
        r'((self:str /\ __d___chars:str + NoneType) -> (return:str))',
        r'((self:bytes /\ __d___bytes:bytearray + bytes + memoryview + NoneType) -> (return:bytes))',
    },
    'swapcase': {
        r'((self:str) -> (return:str))',
        r'((self:bytes) -> (return:bytes))',
        r'((self:bytearray) -> (return:bytearray))',
    },
    'title': {
        r'((self:str) -> (return:str))',
        r'((self:bytes) -> (return:bytes))',
        r'((self:bytearray) -> (return:bytearray))',
    },
    'translate': {
        r'((self:str /\ __table:dict < int, int + str >) -> (return:str))',
        r'((self:bytes /\ __table:bytearray + bytes + memoryview + NoneType /\ __d_delete:bytes) -> (return:bytes))',
        r'((self:bytearray /\ __table:bytearray + bytes + memoryview + NoneType /\ __d_delete:bytes) -> (return:bytearray))',
    },
    'upper': {
        r'((self:str) -> (return:str))',
        r'((self:bytes) -> (return:bytes))',
        r'((self:bytearray) -> (return:bytearray))',
    },
    'zfill': {
        r'((self:bytes /\ __width:SupportsIndex) -> (return:bytes))',
        r'((self:str /\ __width:SupportsIndex) -> (return:str))',
        r'((self:bytearray /\ __width:SupportsIndex) -> (return:bytearray))',
    },
    'maketrans': {
        r'((__x:str /\ __y:str) -> (return:dict < int, int >))',
        r'((__frm:bytearray + bytes + memoryview /\ __to:bytearray + bytes + memoryview) -> (return:bytes))',
        r'((__x:str /\ __y:str /\ __z:str) -> (return:dict < int, int + NoneType >))',
        r'((__x:dict < str, T?0 > + dict < int, T?0 > + dict < int + str, T?0 >) -> (return:dict < int, T?0 >))',
    },
    '__contains__': {
        r'((self:memoryview < int > /\ __x:top) -> (return:bool))',
        r'((self:bytes /\ __key:bytearray + bytes + memoryview + SupportsIndex) -> (return:bool))',
        r'((self:bytearray /\ __key:bytearray + bytes + memoryview + SupportsIndex) -> (return:bool))',
        r'((self:range < int > /\ __key:top) -> (return:bool))',
        r'((self:str /\ __key:str) -> (return:bool))',
        r'((self:set < T?0 > /\ __o:top) -> (return:bool))',
        r'((self:list < T?0 > /\ __key:top) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __o:top) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __key:top) -> (return:bool))',
    },
    '__getitem__': {
        r'((self:bytes /\ __key:SupportsIndex) -> (return:int))',
        r'((self:tuple < T?3 > /\ __key:SupportsIndex) -> (return:T?3))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:T?2))',
        r'((self:str /\ __key:SupportsIndex) -> (return:str))',
        r'((self:memoryview < int > /\ __key:SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __key:SupportsIndex) -> (return:int))',
        r'((self:range < int > /\ __key:SupportsIndex) -> (return:int))',
        r'((self:list < T?0 > /\ __i:SupportsIndex) -> (return:T?0))',
    },
    '__len__': {
        r'((self:set < T?0 >) -> (return:int))',
        r'((self:dict < T?1, T?2 >) -> (return:int))',
        r'((self:str) -> (return:int))',
        r'((self:range < int >) -> (return:int))',
        r'((self:bytearray) -> (return:int))',
        r'((self:tuple < T?3 >) -> (return:int))',
        r'((self:frozenset < T?3 >) -> (return:int))',
        r'((self:memoryview < int >) -> (return:int))',
        r'((self:list < T?0 >) -> (return:int))',
        r'((self:bytes) -> (return:int))',
    },
    'decode': {
        r'((self:bytes /\ __d_encoding:str /\ __d_errors:str) -> (return:str))',
        r'((self:bytearray /\ __d_encoding:str /\ __d_errors:str) -> (return:str))',
    },
    '__buffer__': {
        r'((self:memoryview < int > /\ __flags:int) -> (return:memoryview))',
        r'((self:bytes /\ __flags:int) -> (return:memoryview))',
        r'((self:bytearray /\ __flags:int) -> (return:memoryview))',
    },
    'append': {
        r'((self:list < bot > /\ __object:T?0) -> (self:list < T?0 > /\ return:NoneType))',
        r'((self:list < T?0 > /\ __object:T?1) -> (self:list < T?1 + T?0 > /\ return:NoneType))',
        r'((self:bytearray /\ __item:SupportsIndex) -> (return:NoneType))',
    },
    'copy': {
        r'((self:set < T?0 >) -> (return:set < T?0 >))',
        r'((self:dict < T?1, T?2 >) -> (return:dict < T?1, T?2 >))',
        r'((self:frozenset < T?3 >) -> (return:frozenset < T?3 >))',
        r'((self:list < T?0 >) -> (return:list < T?0 >))',
        r'((self:bytearray) -> (return:bytearray))',
    },
    'extend': {
        r'((self:bytearray /\ __iterable_of_ints:Iterable < SupportsIndex >) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
    },
    'insert': {
        r'((self:list < T?0 > /\ __index:SupportsIndex /\ __object:T?0) -> (return:NoneType))',
        r'((self:bytearray /\ __index:SupportsIndex /\ __item:SupportsIndex) -> (return:NoneType))',
    },
    'pop': {
        r'((self:bytearray /\ __d___index:int) -> (return:int))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:T?2))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?2) -> (return:T?2))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?0) -> (return:T?2 + T?0))',
        r'((self:list < T?0 > /\ __d___index:SupportsIndex) -> (return:T?0))',
    },
    'remove': {
        r'((self:bytearray /\ __value:int) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __value:T?0) -> (return:NoneType))',
        r'((self:set < T?0 > /\ __element:T?0) -> (return:NoneType))',
    },
    '__setitem__': {
        r'((self:memoryview < int > /\ __key:SupportsIndex /\ __value:SupportsIndex) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __value:T?2) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __key:SupportsIndex /\ __value:T?0) -> (return:NoneType))',
        r'((self:bytearray /\ __key:SupportsIndex /\ __value:SupportsIndex) -> (return:NoneType))',
    },
    '__delitem__': {
        r'((self:list < T?0 > /\ __key:SupportsIndex) -> (return:NoneType))',
        r'((self:bytearray /\ __key:SupportsIndex) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:NoneType))',
    },
    '__iadd__': {
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bytearray))',
        r'((self:list < T?0 > /\ __value:Iterable < T?0 >) -> (return:list < T?0 >))',
    },
    '__imul__': {
        r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
        r'((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
    },
    '__alloc__': {
        r'((self:bytearray) -> (return:int))',
    },
    '__release_buffer__': {
        r'((self:memoryview < int > /\ __buffer:memoryview) -> (return:NoneType))',
        r'((self:bytearray /\ __buffer:memoryview) -> (return:NoneType))',
    },
    'itemsize': {
        r'((self:memoryview < int >) -> (return:int))',
    },
    'shape': {
        r'((self:memoryview < int >) -> (return:NoneType + tuple < int >))',
    },
    'strides': {
        r'((self:memoryview < int >) -> (return:NoneType + tuple < int >))',
    },
    'suboffsets': {
        r'((self:memoryview < int >) -> (return:NoneType + tuple < int >))',
    },
    'readonly': {
        r'((self:memoryview < int >) -> (return:bool))',
    },
    'ndim': {
        r'((self:memoryview < int >) -> (return:int))',
    },
    'obj': {
        r'((self:memoryview < int >) -> (return:bytearray + bytes + memoryview))',
    },
    'c_contiguous': {
        r'((self:memoryview < int >) -> (return:bool))',
    },
    'f_contiguous': {
        r'((self:memoryview < int >) -> (return:bool))',
    },
    'contiguous': {
        r'((self:memoryview < int >) -> (return:bool))',
    },
    'nbytes': {
        r'((self:memoryview < int >) -> (return:int))',
    },
    '__enter__': {
        r'((self:memoryview < int >) -> (return:memoryview < int >))',
    },
    '__exit__': {
        r'((self:memoryview < int > /\ __exc_type:top /\ __exc_val:NoneType /\ __exc_tb:NoneType + top) -> (return:NoneType))',
    },
    'cast': {
        r'((self:memoryview < int > /\ format:str /\ __d_shape:list < int > + tuple < int >) -> (return:memoryview))',
    },
    'tolist': {
        r'((self:memoryview < int >) -> (return:list < int >))',
    },
    'release': {
        r'((self:memoryview < int >) -> (return:NoneType))',
    },
    '__closure__': {
        r'((self:top) -> (return:tuple < _Cell > + NoneType))',
    },
    '__globals__': {
        r'((self:top) -> (return:dict < str, top >))',
    },
    '__get__': {
        r'((self:top /\ __instance:top /\ __d___owner:NoneType) -> (return:top))',
    },
    'sort': {
        r'((self:list < T?0 > /\ __ko_key:top /\ __ko___d_reverse:bool) -> (return:NoneType))',
        r'((self:list < top > /\ __ko___d_key:NoneType /\ __ko___d_reverse:bool) -> (return:NoneType))',
    },
    'fromkeys': {
        r'((cls:top /\ __iterable:Iterable < T?0 > /\ __d___value:NoneType) -> (return:dict < T?0, NoneType + top >))',
        r'((cls:top /\ __iterable:Iterable < T?0 > /\ __value:T?4) -> (return:dict < T?0, T?4 >))',
    },
    'get': {
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?0) -> (return:T?2 + T?0))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:T?2 + NoneType))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?2) -> (return:T?2))',
    },
    'add': {
        r'((self:set < T?0 > /\ __element:T?0) -> (return:NoneType))',
    },
    'difference': {
        r'((self:set < T?0 > /\ __va_s:Iterable < top >) -> (return:set < T?0 >))',
        r'((self:frozenset < T?3 > /\ __va_s:Iterable < top >) -> (return:frozenset < T?3 >))',
    },
    'difference_update': {
        r'((self:set < T?0 > /\ __va_s:Iterable < top >) -> (return:NoneType))',
    },
    'discard': {
        r'((self:set < T?0 > /\ __element:T?0) -> (return:NoneType))',
    },
    'intersection': {
        r'((self:set < T?0 > /\ __va_s:Iterable < top >) -> (return:set < T?0 >))',
        r'((self:frozenset < T?3 > /\ __va_s:Iterable < top >) -> (return:frozenset < T?3 >))',
    },
    'intersection_update': {
        r'((self:set < T?0 > /\ __va_s:Iterable < top >) -> (return:NoneType))',
    },
    'isdisjoint': {
        r'((self:set < T?0 > /\ __s:Iterable < top >) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __s:Iterable < T?3 >) -> (return:bool))',
    },
    'issubset': {
        r'((self:set < T?0 > /\ __s:Iterable < top >) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __s:Iterable < top >) -> (return:bool))',
    },
    'issuperset': {
        r'((self:set < T?0 > /\ __s:Iterable < top >) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __s:Iterable < top >) -> (return:bool))',
    },
    'symmetric_difference': {
        r'((self:frozenset < T?3 > /\ __s:Iterable < T?3 >) -> (return:frozenset < T?3 >))',
        r'((self:set < T?0 > /\ __s:Iterable < T?0 >) -> (return:set < T?0 >))',
    },
    'symmetric_difference_update': {
        r'((self:set < T?0 > /\ __s:Iterable < T?0 >) -> (return:NoneType))',
    },
    'union': {
        r'((self:set < T?0 > /\ __va_s:Iterable < T?4 >) -> (return:set < T?0 + T?4 >))',
        r'((self:frozenset < T?3 > /\ __va_s:Iterable < T?4 >) -> (return:frozenset < T?3 + T?4 >))',
    },
    'update': {
        r'((self:set < T?0 > /\ __va_s:Iterable < T?0 >) -> (return:NoneType))',
    },
    '__iand__': {
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:set < T?0 >))',
    },
    '__ior__': {
        r'((self:set < T?0 > /\ __value:set < T?0 >) -> (return:set < T?0 >))',
    },
    '__isub__': {
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:set < T?0 >))',
    },
    '__ixor__': {
        r'((self:set < T?0 > /\ __value:set < T?0 >) -> (return:set < T?0 >))',
    },
    '__iter__': {
        r'((self:frozenset < T?3 >) -> (return:frozenset < T?3 >))',
    },
    '__next__': {
        r'((self:frozenset < T?3 >) -> (return:tuple < int + T?0 >))',
    },
    'start': {
        r'((self:range < int >) -> (return:int))',
    },
    'stop': {
        r'((self:range < int >) -> (return:int))',
    },
    'step': {
        r'((self:range < int >) -> (return:int))',
    },
    '__class_getitem__': {
        r'((cls:top /\ __item:top) -> (return:top))',
    },
    'abs': {
        r'((__x:top) -> (return:T?0))',
    },
    'all': {
        r'((__iterable:Iterable < top >) -> (return:bool))',
    },
    'any': {
        r'((__iterable:Iterable < top >) -> (return:bool))',
    },
    'ascii': {
        r'((__obj:top) -> (return:str))',
    },
    'bin': {
        r'((__number:int + SupportsIndex) -> (return:str))',
    },
    'breakpoint': {
        r'((__va_args:top /\ __kw_kws:top) -> (return:NoneType))',
    },
    'callable': {
        r'((__obj:top) -> (return:top))',
    },
    'chr': {
        r'((__i:int) -> (return:str))',
    },
    'copyright': {
        r'(() -> (return:NoneType))',
    },
    'credits': {
        r'(() -> (return:NoneType))',
    },
    'delattr': {
        r'((__obj:top /\ __name:str) -> (return:NoneType))',
    },
    'dir': {
        r'((__d___o:top) -> (return:list < str >))',
    },
    'eval': {
        r'((__source:memoryview + bytearray + bytes + top + str /\ __d___globals:dict < str, top > + NoneType /\ __d___locals:NoneType + Mapping < str, top >) -> (return:top))',
    },
    'getattr': {
        r'((__o:top /\ name:str /\ __default:list < top >) -> (return:list < top > + top))',
        r'((__o:top /\ __name:str /\ __default:NoneType) -> (return:NoneType + top))',
        r'((__o:top /\ __name:str /\ __default:T?0) -> (return:T?0 + top))',
        r'((__o:top /\ __name:str /\ __default:bool) -> (return:bool + top))',
        r'((__o:top /\ __name:str) -> (return:top))',
        r'((__o:top /\ name:str /\ __default:dict < top, top >) -> (return:dict < top, top > + top))',
    },
    'globals': {
        r'(() -> (return:dict < str, top >))',
    },
    'hasattr': {
        r'((__obj:top /\ __name:str) -> (return:bool))',
    },
    'hash': {
        r'((__obj:top) -> (return:int))',
    },
    'help': {
        r'((__d_request:top) -> (return:NoneType))',
    },
    'id': {
        r'((__obj:top) -> (return:int))',
    },
    'input': {
        r'((__d___prompt:top) -> (return:str))',
    },
    'isinstance': {
        r'((__obj:top /\ __class_or_tuple:top) -> (return:bool))',
    },
    'len': {
        r'((__obj:Sized) -> (return:int))',
    },
    'license': {
        r'(() -> (return:NoneType))',
    },
    'locals': {
        r'(() -> (return:dict < str, top >))',
    },
    'max': {
        r'((__iterable:Iterable < top > /\ __ko___d_key:NoneType) -> (return:top))',
        r'((__arg1:top /\ __arg2:top /\ __va__args:top /\ __ko___d_key:NoneType) -> (return:top))',
        r'((__iterable:Iterable < top > /\ __ko___d_key:NoneType /\ __ko_default:T?0) -> (return:T?0 + top))',
        r'((__arg1:T?0 /\ __arg2:T?0 /\ __va__args:T?0 /\ __ko_key:top) -> (return:T?0))',
        r'((__iterable:Iterable < T?0 > /\ __ko_key:top) -> (return:T?0))',
        r'((__iterable:Iterable < _T1 > /\ __ko_key:top /\ __ko_default:_T2) -> (return:_T1 + _T2))',
    },
    'min': {
        r'((__iterable:Iterable < top > /\ __ko___d_key:NoneType) -> (return:top))',
        r'((__arg1:top /\ __arg2:top /\ __va__args:top /\ __ko___d_key:NoneType) -> (return:top))',
        r'((__iterable:Iterable < top > /\ __ko___d_key:NoneType /\ __ko_default:T?0) -> (return:T?0 + top))',
        r'((__arg1:T?0 /\ __arg2:T?0 /\ __va__args:T?0 /\ __ko_key:top) -> (return:T?0))',
        r'((__iterable:Iterable < T?0 > /\ __ko_key:top) -> (return:T?0))',
        r'((__iterable:Iterable < _T1 > /\ __ko_key:top /\ __ko_default:_T2) -> (return:_T1 + _T2))',
    },
    'oct': {
        r'((__number:int + SupportsIndex) -> (return:str))',
    },
    'open': {
        r'((file:str /\ mode:top /\ __d_buffering:top /\ __d_encoding:NoneType /\ __d_errors:NoneType /\ __d_newline:NoneType /\ __d_closefd:bool /\ __d_opener:NoneType + top) -> (return:top))',
        r'((file:str /\ mode:top /\ buffering:top /\ __d_encoding:NoneType /\ __d_errors:NoneType /\ __d_newline:NoneType /\ __d_closefd:bool /\ __d_opener:NoneType + top) -> (return:top))',
        r'((file:str /\ __d_mode:top /\ __d_buffering:int /\ __d_encoding:str + NoneType /\ __d_errors:str + NoneType /\ __d_newline:str + NoneType /\ __d_closefd:bool /\ __d_opener:NoneType + top) -> (return:top))',
    },
    'ord': {
        r'((__c:bytearray + bytes + str) -> (return:int))',
    },
    'print': {
        r'((__va_values:top /\ __ko___d_sep:str + NoneType /\ __ko___d_end:str + NoneType /\ __ko___d_file:top /\ __ko_flush:bool) -> (return:NoneType))',
    },
    'repr': {
        r'((__obj:top) -> (return:str))',
    },
    'setattr': {
        r'((__obj:top /\ __name:str /\ __value:top) -> (return:NoneType))',
    },
    'sorted': {
        r'((__iterable:Iterable < T?0 > /\ __ko_key:top /\ __ko___d_reverse:bool) -> (return:list < T?0 >))',
        r'((__iterable:Iterable < top > /\ __ko___d_key:NoneType /\ __ko___d_reverse:bool) -> (return:list < top >))',
    },
    'sum': {
        r'((__iterable:Iterable < int >) -> (return:top))',
    },
    'vars': {
        r'((__d___object:top) -> (return:dict < str, top >))',
    },
    '__import__': {
        r'((name:str /\ __d_globals:NoneType + Mapping < str, top > /\ __d_locals:NoneType + Mapping < str, top > /\ __d_fromlist:Sequence < str > /\ __d_level:int) -> (return:top))',
    },
    '__build_class__': {
        r'((__func:top /\ __name:str /\ __va_bases:top /\ __ko___d_metaclass:top /\ __kw_kwds:top) -> (return:top))',
    },
    'baz': {
        r'((__po_a:int /\ __po_b:float /\ __d_c:bool /\ __ko_d:str) -> (return:bool))',
    },
    'foo': {
        r'((__po_a:int /\ __po_b:int /\ c:int /\ __va_d:top /\ __ko_e:int /\ __ko_f:int /\ __kw_g:top) -> (return:bool))',
    },
    'bar': {
        r'((a:int /\ __d_b:int /\ __d_c:int /\ __va_d:top /\ __ko_e:int /\ __ko___d_f:int /\ __kw_g:top) -> (return:bool))',
    },
    'qux': {
        r'((a:int /\ b:float /\ c:str) -> (return:complex))',
    },
    'corge': {
        r'((__va_args:top /\ __kw_kwargs:top) -> (return:bool))',
    },
    'fred': {
        r'((__va_args:str /\ __kw_kwargs:str) -> (return:bool))',
    },
    'waldo': {
        r'((__va_args:Iterable < T?1 > /\ __kw_kwargs:Iterable < T?2 >) -> (return:bool))',
    },
    'simpleassign': {
        r'((x:top /\ y:T?0) -> (x:T?0 /\ return:NoneType))',
    },
    'tupleassign': {
        r'((__va_args:Iterable < top > /\ y:str + Iterable < T?0 >) -> (__va_args:Iterable < str + T?0 > /\ return:NoneType))',
    },
    'seqassign': {
        r'((x:top /\ y:str) -> (x:str /\ return:NoneType))',
        r'((x:top /\ y:Iterable < T?0 >) -> (x:T?0 /\ return:NoneType))',
    },
    'simple_subscript': {
        r'((a:dict < T?0, T?1 > /\ b:T?0) -> (return:T?1))',
        r'((a:Iterable < T?0 > /\ b:int) -> (return:T?0))',
    },
    'subscriptassign': {
        r'((x:list < T?0 > /\ y:T?1) -> (x:list < T?1 + T?0 > /\ return:NoneType))',
        r'((x:set < T?0 > /\ y:T?1) -> (x:set < T?1 + T?0 > /\ return:NoneType))',
        r'((x:frozenset < T?0 > /\ y:T?1) -> (x:frozenset < T?1 + T?0 > /\ return:NoneType))',
        r'((x:dict < T?0, T?1 > /\ y:T?2) -> (x:dict < T?0, T?2 + T?1 > /\ return:NoneType))',
        r'((x:tuple < T?0 > /\ y:T?1) -> (x:tuple < T?1 + T?0 > /\ return:NoneType))',
    },
    'assign_1_prim': {
        r'((c:str + tuple < T?1 + T?0 >) -> (return:tuple < T?1 + str + T?0 >))',
    },
    'for_parse': {
        r'((target:top /\ iter:Iterable < T?0 >) -> (target:T?0))',
        r'((target:top /\ iter:bytes) -> (target:int))',
        r'((target:top /\ iter:str) -> (target:str))',
        r'((target:top /\ iter:bytearray) -> (target:int))',
        r'((target:top /\ iter:range) -> (target:int))',
        r'((target:top /\ iter:memoryview) -> (target:int))',
    },
    'range': {
        r'((stop:int) -> (return:range))',
        r'((start:int /\ stop:int) -> (return:range))',
        r'((start:int /\ stop:int /\ step:int) -> (return:range))',
    },

}
