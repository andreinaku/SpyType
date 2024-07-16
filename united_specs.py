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
    '__init__': {
        r'((self:range < int > /\ __start:SupportsIndex /\ __stop:SupportsIndex /\ __d___step:SupportsIndex) -> (return:NoneType))',
        r'((self:bytearray /\ __ints:SupportsIndex + memoryview + bytearray + Iterable < SupportsIndex > + bytes) -> (return:NoneType))',
        r'((self:bytearray /\ __string:str /\ encoding:str /\ __d_errors:str) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
        r'((self:list < T?0 >) -> (return:NoneType))',
        r'((self:set < T?0 >) -> (return:NoneType))',
        r'((self:range < int > /\ __stop:SupportsIndex) -> (return:NoneType))',
        r'((self:dict < str, T?2 > /\ __kw_kwargs:T?2) -> (return:NoneType))',
        r'((self:bytearray) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __map:dict < T?1, T?2 >) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 >) -> (return:NoneType))',
        r'((self:memoryview < int > /\ obj:bytes + memoryview + bytearray) -> (return:NoneType))',
        r'((self:frozenset < T?3 > /\ iterable:Iterable < T?0 > /\ __d_start:int) -> (return:NoneType))',
        r'((self:dict < str, T?2 > /\ __map:dict < str, T?2 > /\ __kw_kwargs:T?2) -> (return:NoneType))',
        r'((self:set < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
        r'((self:top) -> (return:NoneType))',
    },
    '__setattr__': {
        r'((self:top /\ __name:str /\ __value:top) -> (return:NoneType))',
    },
    '__delattr__': {
        r'((self:top /\ __name:str) -> (return:NoneType))',
    },
    '__eq__': {
        r'((self:float /\ __value:top) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:top) -> (return:bool))',
        r'((self:memoryview < int > /\ __value:top) -> (return:bool))',
        r'((self:int /\ __value:top) -> (return:bool))',
        r'((self:dict < T?1, T?2 > /\ __value:top) -> (return:bool))',
        r'((self:complex /\ __value:top) -> (return:bool))',
        r'((self:bytearray /\ __value:top) -> (return:bool))',
        r'((self:range < int > /\ __value:top) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:top) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:top) -> (return:bool))',
        r'((self:bytes /\ __value:top) -> (return:bool))',
        r'((self:str /\ __value:top) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:top) -> (return:bool))',
        r'((self:top /\ __value:top) -> (return:bool))',
    },
    '__ne__': {
        r'((self:float /\ __value:top) -> (return:bool))',
        r'((self:int /\ __value:top) -> (return:bool))',
        r'((self:bytearray /\ __value:top) -> (return:bool))',
        r'((self:complex /\ __value:top) -> (return:bool))',
        r'((self:bytes /\ __value:top) -> (return:bool))',
        r'((self:str /\ __value:top) -> (return:bool))',
        r'((self:top /\ __value:top) -> (return:bool))',
    },
    '__str__': {
        r'((self:top) -> (return:str))',
    },
    '__repr__': {
        r'((self:top) -> (return:str))',
    },
    '__hash__': {
        r'((self:bytes) -> (return:int))',
        r'((self:frozenset < T?3 >) -> (return:int))',
        r'((self:str) -> (return:int))',
        r'((self:tuple < T?3 >) -> (return:int))',
        r'((self:range < int >) -> (return:int))',
        r'((self:memoryview < int >) -> (return:int))',
        r'((self:int) -> (return:int))',
        r'((self:float) -> (return:int))',
        r'((self:complex) -> (return:int))',
        r'((self:top) -> (return:int))',
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
    'real': {
        r'((self:complex) -> (return:float))',
        r'((self:int) -> (return:int))',
        r'((self:float) -> (return:float))',
    },
    'numerator': {
        r'((self:int) -> (return:int))',
    },
    'conjugate': {
        r'((self:complex) -> (return:complex))',
        r'((self:int) -> (return:int))',
        r'((self:float) -> (return:float))',
    },
    'bit_length': {
        r'((self:int) -> (return:int))',
    },
    '__add__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:tuple < T?3 >))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:list < T?0 >))',
        r'((self:list < T?0 > /\ __value:list < T?4 >) -> (return:list < T?4 + T?0 >))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?0 >) -> (return:tuple < T?3 + T?0 >))',
        r'((self:str /\ __value:str) -> (return:str))',
        r'((self:bytearray /\ __value:bytes + memoryview + bytearray) -> (return:bytearray))',
        r'((self:bytes /\ __value:bytes + memoryview + bytearray) -> (return:bytes))',
    },
    '__sub__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:set < T?0 > /\ __value:set < NoneType + T?0 >) -> (return:set < T?0 >))',
        r'((self:frozenset < T?3 > /\ __value:set < T?3 >) -> (return:frozenset < T?3 >))',
    },
    '__mul__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:bytes /\ __value:SupportsIndex) -> (return:bytes))',
        r'((self:str /\ __value:SupportsIndex) -> (return:str))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
        r'((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
        r'((self:tuple < T?3 > /\ __value:SupportsIndex) -> (return:tuple < T?3 >))',
    },
    '__floordiv__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__truediv__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:int /\ __value:int) -> (return:float))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__mod__': {
        r'((self:bytearray /\ __value:top) -> (return:bytes))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:str /\ __value:top) -> (return:str))',
        r'((self:bytes /\ __value:top) -> (return:bytes))',
        r'((self:str /\ __value:str + tuple < str >) -> (return:str))',
    },
    '__divmod__': {
        r'((self:float /\ __value:float) -> (return:tuple < float >))',
        r'((self:int /\ __value:int) -> (return:tuple < int >))',
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
        r'((self:bytes /\ __value:SupportsIndex) -> (return:bytes))',
        r'((self:str /\ __value:SupportsIndex) -> (return:str))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
        r'((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
        r'((self:tuple < T?3 > /\ __value:SupportsIndex) -> (return:tuple < T?3 >))',
    },
    '__rfloordiv__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rtruediv__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:int /\ __value:int) -> (return:float))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rmod__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rdivmod__': {
        r'((self:float /\ __value:float) -> (return:tuple < float >))',
        r'((self:int /\ __value:int) -> (return:tuple < int >))',
    },
    '__pow__': {
        r'((self:complex /\ __value:complex /\ __d___mod:NoneType) -> (return:complex))',
        r'((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:top))',
        r'((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:int))',
        r'((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
        r'((self:int /\ __value:int /\ __mod:int) -> (return:int))',
        r'((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
        r'((self:float /\ __value:float /\ __d___mod:NoneType) -> (return:top))',
    },
    '__rpow__': {
        r'((self:complex /\ __value:complex /\ __d___mod:NoneType) -> (return:complex))',
        r'((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:complex))',
        r'((self:int /\ __value:int /\ __d___mod:NoneType + int) -> (return:top))',
        r'((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
        r'((self:float /\ __value:float /\ __d___mod:NoneType) -> (return:top))',
    },
    '__and__': {
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:set < T?0 >))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < T?3 >) -> (return:frozenset < T?3 >))',
    },
    '__or__': {
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < T?4 >) -> (return:set < T?4 + T?0 >))',
        r'((self:frozenset < T?3 > /\ __value:set < T?4 >) -> (return:frozenset < T?3 + T?4 >))',
    },
    '__xor__': {
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < T?4 >) -> (return:set < T?4 + T?0 >))',
        r'((self:frozenset < T?3 > /\ __value:set < T?4 >) -> (return:frozenset < T?3 + T?4 >))',
    },
    '__lshift__': {
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rshift__': {
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rand__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
    },
    '__ror__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
    },
    '__rxor__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
    },
    '__rlshift__': {
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rrshift__': {
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__neg__': {
        r'((self:complex) -> (return:complex))',
        r'((self:int) -> (return:int))',
        r'((self:float) -> (return:float))',
    },
    '__pos__': {
        r'((self:complex) -> (return:complex))',
        r'((self:int) -> (return:int))',
        r'((self:float) -> (return:float))',
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
        r'((self:int /\ __d___ndigits:SupportsIndex) -> (return:int))',
        r'((self:float /\ __d___ndigits:NoneType) -> (return:int))',
    },
    '__getnewargs__': {
        r'((self:bytes) -> (return:tuple < bytes >))',
        r'((self:str) -> (return:tuple < str >))',
        r'((self:int) -> (return:tuple < int >))',
        r'((self:bool) -> (return:tuple < int >))',
        r'((self:float) -> (return:tuple < float >))',
    },
    '__lt__': {
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytes + memoryview + bytearray) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
    },
    '__le__': {
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytes + memoryview + bytearray) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
    },
    '__gt__': {
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytes + memoryview + bytearray) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
    },
    '__ge__': {
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytes + memoryview + bytearray) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
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
        r'((self:complex) -> (return:float))',
        r'((self:int) -> (return:int))',
        r'((self:float) -> (return:float))',
    },
    '__bool__': {
        r'((self:int) -> (return:bool))',
        r'((self:float) -> (return:bool))',
        r'((self:complex) -> (return:bool))',
    },
    '__index__': {
        r'((self:int) -> (return:int))',
    },
    'as_integer_ratio': {
        r'((self:float) -> (return:tuple < int >))',
    },
    'hex': {
        r'((__number:SupportsIndex + int) -> (return:str))',
        r'((self:float) -> (return:str))',
    },
    'is_integer': {
        r'((self:float) -> (return:bool))',
    },
    'imag': {
        r'((self:complex) -> (return:float))',
        r'((self:float) -> (return:float))',
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
        r'((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
        r'((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytes) -> (return:bytes))',
        r'((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytes) -> (return:bytearray))',
    },
    'count': {
        r'((self:list < T?0 > /\ __value:T?0) -> (return:int))',
        r'((self:str /\ x:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:bytes /\ __sub:SupportsIndex + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:range < int > /\ __value:int) -> (return:int))',
        r'((self:tuple < T?3 > /\ __value:top) -> (return:int))',
        r'((self:bytearray /\ __sub:SupportsIndex + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
    },
    'encode': {
        r'((self:str /\ __d_encoding:str /\ __d_errors:str) -> (return:bytes))',
    },
    'endswith': {
        r'((self:str /\ __suffix:str + tuple < str > /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
        r'((self:bytearray /\ __suffix:tuple < bytes + memoryview + bytearray > + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
        r'((self:bytes /\ __suffix:tuple < bytes + memoryview + bytearray > + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
    },
    'find': {
        r'((self:bytearray /\ __sub:SupportsIndex + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:bytes /\ __sub:SupportsIndex + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:str /\ __sub:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
    },
    'format': {
        r'((self:memoryview < int >) -> (return:str))',
        r'((self:str /\ __va_args:str /\ __kw_kwargs:str) -> (return:str))',
        r'((__value:top /\ __d___format_spec:str) -> (return:str))',
        r'((self:str /\ __va_args:top /\ __kw_kwargs:top) -> (return:str))',
    },
    'format_map': {
        r'((self:str /\ map:dict < str, int >) -> (return:str))',
    },
    'index': {
        r'((self:bytes /\ __sub:SupportsIndex + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:range < int > /\ __value:int) -> (return:int))',
        r'((self:str /\ __sub:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:bytearray /\ __sub:SupportsIndex + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:tuple < T?3 > /\ __value:top /\ __d___start:SupportsIndex /\ __d___stop:SupportsIndex) -> (return:int))',
        r'((self:list < T?0 > /\ __value:T?0 /\ __d___start:SupportsIndex /\ __d___stop:SupportsIndex) -> (return:int))',
    },
    'isalnum': {
        r'((self:bytearray) -> (return:bool))',
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'isalpha': {
        r'((self:bytearray) -> (return:bool))',
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'isascii': {
        r'((self:bytearray) -> (return:bool))',
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'isdecimal': {
        r'((self:str) -> (return:bool))',
    },
    'isdigit': {
        r'((self:bytearray) -> (return:bool))',
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'isidentifier': {
        r'((self:str) -> (return:bool))',
    },
    'islower': {
        r'((self:bytearray) -> (return:bool))',
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'isnumeric': {
        r'((self:str) -> (return:bool))',
    },
    'isprintable': {
        r'((self:str) -> (return:bool))',
    },
    'isspace': {
        r'((self:bytearray) -> (return:bool))',
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'istitle': {
        r'((self:bytearray) -> (return:bool))',
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'isupper': {
        r'((self:bytearray) -> (return:bool))',
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
    },
    'join': {
        r'((self:bytes /\ __iterable_of_bytes:Iterable < bytes + memoryview + bytearray >) -> (return:bytes))',
        r'((self:bytearray /\ __iterable_of_bytes:Iterable < bytes + memoryview + bytearray >) -> (return:bytearray))',
        r'((self:str /\ __iterable:Iterable < str >) -> (return:str))',
    },
    'ljust': {
        r'((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
        r'((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytes + bytearray) -> (return:bytearray))',
        r'((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytes + bytearray) -> (return:bytes))',
    },
    'lower': {
        r'((self:str) -> (return:str))',
        r'((self:bytes) -> (return:bytes))',
        r'((self:bytearray) -> (return:bytearray))',
    },
    'lstrip': {
        r'((self:bytes /\ __d___bytes:NoneType + bytes + memoryview + bytearray) -> (return:bytes))',
        r'((self:bytearray /\ __d___bytes:NoneType + bytes + memoryview + bytearray) -> (return:bytearray))',
        r'((self:str /\ __d___chars:str + NoneType) -> (return:str))',
    },
    'partition': {
        r'((self:str /\ __sep:str) -> (return:tuple < str >))',
        r'((self:bytes /\ __sep:bytes + memoryview + bytearray) -> (return:tuple < bytes >))',
        r'((self:bytearray /\ __sep:bytes + memoryview + bytearray) -> (return:tuple < bytearray >))',
    },
    'replace': {
        r'((self:bytes /\ __old:bytes + memoryview + bytearray /\ __new:bytes + memoryview + bytearray /\ __d___count:SupportsIndex) -> (return:bytes))',
        r'((self:str /\ __old:str /\ __new:str /\ __d___count:SupportsIndex) -> (return:str))',
        r'((self:bytearray /\ __old:bytes + memoryview + bytearray /\ __new:bytes + memoryview + bytearray /\ __d___count:SupportsIndex) -> (return:bytearray))',
    },
    'rfind': {
        r'((self:bytearray /\ __sub:SupportsIndex + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:bytes /\ __sub:SupportsIndex + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:str /\ __sub:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
    },
    'rindex': {
        r'((self:bytearray /\ __sub:SupportsIndex + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:bytes /\ __sub:SupportsIndex + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:str /\ __sub:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
    },
    'rjust': {
        r'((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
        r'((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytes + bytearray) -> (return:bytearray))',
        r'((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytes + bytearray) -> (return:bytes))',
    },
    'rpartition': {
        r'((self:str /\ __sep:str) -> (return:tuple < str >))',
        r'((self:bytes /\ __sep:bytes + memoryview + bytearray) -> (return:tuple < bytes >))',
        r'((self:bytearray /\ __sep:bytes + memoryview + bytearray) -> (return:tuple < bytearray >))',
    },
    'rsplit': {
        r'((self:str /\ __d_sep:str + NoneType /\ __d_maxsplit:SupportsIndex) -> (return:list < str >))',
        r'((self:bytes /\ __d_sep:NoneType + bytes + memoryview + bytearray /\ __d_maxsplit:SupportsIndex) -> (return:list < bytes >))',
        r'((self:bytearray /\ __d_sep:NoneType + bytes + memoryview + bytearray /\ __d_maxsplit:SupportsIndex) -> (return:list < bytearray >))',
    },
    'rstrip': {
        r'((self:bytes /\ __d___bytes:NoneType + bytes + memoryview + bytearray) -> (return:bytes))',
        r'((self:bytearray /\ __d___bytes:NoneType + bytes + memoryview + bytearray) -> (return:bytearray))',
        r'((self:str /\ __d___chars:str + NoneType) -> (return:str))',
    },
    'split': {
        r'((self:str /\ __d_sep:str + NoneType /\ __d_maxsplit:SupportsIndex) -> (return:list < str >))',
        r'((self:bytes /\ __d_sep:NoneType + bytes + memoryview + bytearray /\ __d_maxsplit:SupportsIndex) -> (return:list < bytes >))',
        r'((self:bytearray /\ __d_sep:NoneType + bytes + memoryview + bytearray /\ __d_maxsplit:SupportsIndex) -> (return:list < bytearray >))',
    },
    'splitlines': {
        r'((self:bytes /\ __d_keepends:bool) -> (return:list < bytes >))',
        r'((self:bytearray /\ __d_keepends:bool) -> (return:list < bytearray >))',
        r'((self:str /\ __d_keepends:bool) -> (return:list < str >))',
    },
    'startswith': {
        r'((self:bytes /\ __prefix:tuple < bytes + memoryview + bytearray > + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
        r'((self:bytearray /\ __prefix:tuple < bytes + memoryview + bytearray > + bytes + memoryview + bytearray /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
        r'((self:str /\ __prefix:str + tuple < str > /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
    },
    'strip': {
        r'((self:bytes /\ __d___bytes:NoneType + bytes + memoryview + bytearray) -> (return:bytes))',
        r'((self:bytearray /\ __d___bytes:NoneType + bytes + memoryview + bytearray) -> (return:bytearray))',
        r'((self:str /\ __d___chars:str + NoneType) -> (return:str))',
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
        r'((self:bytes /\ __table:NoneType + bytes + memoryview + bytearray /\ __d_delete:bytes) -> (return:bytes))',
        r'((self:str /\ __table:dict < int, str + int >) -> (return:str))',
        r'((self:bytearray /\ __table:NoneType + bytes + memoryview + bytearray /\ __d_delete:bytes) -> (return:bytearray))',
    },
    'upper': {
        r'((self:str) -> (return:str))',
        r'((self:bytes) -> (return:bytes))',
        r'((self:bytearray) -> (return:bytearray))',
    },
    'zfill': {
        r'((self:str /\ __width:SupportsIndex) -> (return:str))',
        r'((self:bytes /\ __width:SupportsIndex) -> (return:bytes))',
        r'((self:bytearray /\ __width:SupportsIndex) -> (return:bytearray))',
    },
    'maketrans': {
        r'((__x:str /\ __y:str /\ __z:str) -> (return:dict < int, NoneType + int >))',
        r'((__x:str /\ __y:str) -> (return:dict < int, int >))',
        r'((__x:dict < str + int, T?0 > + dict < str, T?0 > + dict < int, T?0 >) -> (return:dict < int, T?0 >))',
        r'((__frm:bytes + memoryview + bytearray /\ __to:bytes + memoryview + bytearray) -> (return:bytes))',
    },
    '__contains__': {
        r'((self:frozenset < T?3 > /\ __o:top) -> (return:bool))',
        r'((self:set < T?0 > /\ __o:top) -> (return:bool))',
        r'((self:str /\ __key:str) -> (return:bool))',
        r'((self:bytes /\ __key:SupportsIndex + bytes + memoryview + bytearray) -> (return:bool))',
        r'((self:bytearray /\ __key:SupportsIndex + bytes + memoryview + bytearray) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __key:top) -> (return:bool))',
        r'((self:range < int > /\ __key:top) -> (return:bool))',
        r'((self:memoryview < int > /\ __x:top) -> (return:bool))',
        r'((self:list < T?0 > /\ __key:top) -> (return:bool))',
    },
    '__getitem__': {
        r'((self:bytearray /\ __key:SupportsIndex) -> (return:int))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:T?2))',
        r'((self:list < T?0 > /\ __i:SupportsIndex) -> (return:T?0))',
        r'((self:memoryview < int > /\ __key:SupportsIndex) -> (return:int))',
        r'((self:bytes /\ __key:SupportsIndex) -> (return:int))',
        r'((self:range < int > /\ __key:SupportsIndex) -> (return:int))',
        r'((self:tuple < T?3 > /\ __key:SupportsIndex) -> (return:T?3))',
        r'((self:str /\ __key:SupportsIndex) -> (return:str))',
    },
    '__len__': {
        r'((self:bytes) -> (return:int))',
        r'((self:frozenset < T?3 >) -> (return:int))',
        r'((self:str) -> (return:int))',
        r'((self:set < T?0 >) -> (return:int))',
        r'((self:list < T?0 >) -> (return:int))',
        r'((self:tuple < T?3 >) -> (return:int))',
        r'((self:range < int >) -> (return:int))',
        r'((self:bytearray) -> (return:int))',
        r'((self:memoryview < int >) -> (return:int))',
        r'((self:dict < T?1, T?2 >) -> (return:int))',
    },
    'decode': {
        r'((self:bytes /\ __d_encoding:str /\ __d_errors:str) -> (return:str))',
        r'((self:bytearray /\ __d_encoding:str /\ __d_errors:str) -> (return:str))',
    },
    '__buffer__': {
        r'((self:bytearray /\ __flags:int) -> (return:memoryview))',
        r'((self:bytes /\ __flags:int) -> (return:memoryview))',
        r'((self:memoryview < int > /\ __flags:int) -> (return:memoryview))',
    },
    'append': {
        r'((self:list < T?0 > /\ __object:T?1) -> (self:list < T?1 + T?0 > /\ return:NoneType))',
        r'((self:bytearray /\ __item:SupportsIndex) -> (return:NoneType))',
        r'((self:list < bot > /\ __object:T?0) -> (self:list < T?0 > /\ return:NoneType))',
    },
    'copy': {
        r'((self:dict < T?1, T?2 >) -> (return:dict < T?1, T?2 >))',
        r'((self:set < T?0 >) -> (return:set < T?0 >))',
        r'((self:list < T?0 >) -> (return:list < T?0 >))',
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:frozenset < T?3 >) -> (return:frozenset < T?3 >))',
    },
    'extend': {
        r'((self:bytearray /\ __iterable_of_ints:Iterable < SupportsIndex >) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
    },
    'insert': {
        r'((self:bytearray /\ __index:SupportsIndex /\ __item:SupportsIndex) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __index:SupportsIndex /\ __object:T?0) -> (return:NoneType))',
    },
    'pop': {
        r'((self:bytearray /\ __d___index:int) -> (return:int))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?2) -> (return:T?2))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:T?2))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?0) -> (return:T?2 + T?0))',
        r'((self:list < T?0 > /\ __d___index:SupportsIndex) -> (return:T?0))',
    },
    'remove': {
        r'((self:set < T?0 > /\ __element:T?0) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __value:T?0) -> (return:NoneType))',
        r'((self:bytearray /\ __value:int) -> (return:NoneType))',
    },
    '__setitem__': {
        r'((self:memoryview < int > /\ __key:SupportsIndex /\ __value:SupportsIndex) -> (return:NoneType))',
        r'((self:bytearray /\ __key:SupportsIndex /\ __value:SupportsIndex) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __key:SupportsIndex /\ __value:T?0) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __value:T?2) -> (return:NoneType))',
    },
    '__delitem__': {
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __key:SupportsIndex) -> (return:NoneType))',
        r'((self:bytearray /\ __key:SupportsIndex) -> (return:NoneType))',
    },
    '__iadd__': {
        r'((self:bytearray /\ __value:bytes + memoryview + bytearray) -> (return:bytearray))',
        r'((self:list < T?0 > /\ __value:Iterable < T?0 >) -> (return:list < T?0 >))',
    },
    '__imul__': {
        r'((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
        r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
    },
    '__alloc__': {
        r'((self:bytearray) -> (return:int))',
    },
    '__release_buffer__': {
        r'((self:bytearray /\ __buffer:memoryview) -> (return:NoneType))',
        r'((self:memoryview < int > /\ __buffer:memoryview) -> (return:NoneType))',
    },
    'itemsize': {
        r'((self:memoryview < int >) -> (return:int))',
    },
    'shape': {
        r'((self:memoryview < int >) -> (return:tuple < int > + NoneType))',
    },
    'strides': {
        r'((self:memoryview < int >) -> (return:tuple < int > + NoneType))',
    },
    'suboffsets': {
        r'((self:memoryview < int >) -> (return:tuple < int > + NoneType))',
    },
    'readonly': {
        r'((self:memoryview < int >) -> (return:bool))',
    },
    'ndim': {
        r'((self:memoryview < int >) -> (return:int))',
    },
    'obj': {
        r'((self:memoryview < int >) -> (return:bytes + memoryview + bytearray))',
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
        r'((self:tuple < T?3 >) -> (return:NoneType + tuple < _Cell >))',
    },
    '__globals__': {
        r'((self:tuple < T?3 >) -> (return:dict < str, top >))',
    },
    '__get__': {
        r'((self:tuple < T?3 > /\ __instance:top /\ __d___owner:NoneType) -> (return:top))',
    },
    'get': {
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:T?2 + NoneType))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?0) -> (return:T?2 + T?0))',
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
        r'((self:frozenset < T?3 > /\ __s:Iterable < T?3 >) -> (return:bool))',
        r'((self:set < T?0 > /\ __s:Iterable < top >) -> (return:bool))',
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
        r'((self:frozenset < T?3 > /\ __va_s:Iterable < T?4 >) -> (return:frozenset < T?3 + T?4 >))',
        r'((self:set < T?0 > /\ __va_s:Iterable < T?4 >) -> (return:set < T?4 + T?0 >))',
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
        r'((self:frozenset < T?3 >) -> (return:tuple < T?0 + int >))',
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
        r'((__number:SupportsIndex + int) -> (return:str))',
    },
    'breakpoint': {
        r'((__va_args:top /\ __kw_kws:top) -> (return:NoneType))',
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
    'getattr': {
        r'((__o:top /\ __name:str /\ __default:bool) -> (return:bool + top))',
        r'((__o:top /\ __name:str /\ __default:T?0) -> (return:T?0 + top))',
        r'((__o:top /\ name:str /\ __default:list < top >) -> (return:list < top > + top))',
        r'((__o:top /\ name:str /\ __default:dict < top, top >) -> (return:dict < top, top > + top))',
        r'((__o:top /\ __name:str) -> (return:top))',
        r'((__o:top /\ __name:str /\ __default:NoneType) -> (return:NoneType + top))',
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
    'len': {
        r'((__obj:Sized) -> (return:int))',
    },
    'license': {
        r'(() -> (return:NoneType))',
    },
    'locals': {
        r'(() -> (return:dict < str, top >))',
    },
    'oct': {
        r'((__number:SupportsIndex + int) -> (return:str))',
    },
    'ord': {
        r'((__c:str + bytes + bytearray) -> (return:int))',
    },
    'repr': {
        r'((__obj:top) -> (return:str))',
    },
    'setattr': {
        r'((__obj:top /\ __name:str /\ __value:top) -> (return:NoneType))',
    },
    'vars': {
        r'((__d___object:top) -> (return:dict < str, top >))',
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
        r'((a:Iterable < T?0 > /\ b:int) -> (return:T?0))',
        r'((a:dict < T?0, T?1 > /\ b:T?0) -> (return:T?1))',
    },
    'subscriptassign': {
        r'((x:dict < T?0, T?1 > /\ y:T?2) -> (x:dict < T?0, T?2 + T?1 > /\ return:NoneType))',
        r'((x:set < T?0 > /\ y:T?1) -> (x:set < T?1 + T?0 > /\ return:NoneType))',
        r'((x:frozenset < T?0 > /\ y:T?1) -> (x:frozenset < T?1 + T?0 > /\ return:NoneType))',
        r'((x:list < T?0 > /\ y:T?1) -> (x:list < T?1 + T?0 > /\ return:NoneType))',
        r'((x:tuple < T?0 > /\ y:T?1) -> (x:tuple < T?1 + T?0 > /\ return:NoneType))',
    },
    'assign_1_prim': {
        r'((c:str + tuple < T?1 + T?0 >) -> (return:tuple < str + T?1 + T?0 >))',
    },
    'for_parse': {
        r'((target:top /\ iter:str) -> (target:str))',
        r'((target:top /\ iter:range) -> (target:int))',
        r'((target:top /\ iter:bytes) -> (target:int))',
        r'((target:top /\ iter:memoryview) -> (target:int))',
        r'((target:top /\ iter:bytearray) -> (target:int))',
        r'((target:top /\ iter:Iterable < T?0 >) -> (target:T?0))',
    },
    'range': {
        r'((start:int /\ stop:int) -> (return:range))',
        r'((start:int /\ stop:int /\ step:int) -> (return:range))',
        r'((stop:int) -> (return:range))',
    },

}
