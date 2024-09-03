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
        r'((self:dict < T?1, T?2 >) -> (return:NoneType))',
        r'((self:dict < str, T?2 > /\ __map:dict < str, T?2 > /\ __kw_kwargs:T?2) -> (return:NoneType))',
        r'((self:range < int > /\ __start:SupportsIndex /\ __stop:SupportsIndex /\ __d___step:SupportsIndex) -> (return:NoneType))',
        r'((self:bytearray /\ __ints:bytearray + bytes + memoryview + SupportsIndex + Iterable < SupportsIndex >) -> (return:NoneType))',
        r'((self:bytearray /\ __string:str /\ encoding:str /\ __d_errors:str) -> (return:NoneType))',
        r'((self:list < T?0 >) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __map:dict < T?1, T?2 >) -> (return:NoneType))',
        r'((self:set < T?0 >) -> (return:NoneType))',
        r'((self:memoryview < int > /\ obj:bytearray + bytes + memoryview) -> (return:NoneType))',
        r'((self:set < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
        r'((self:dict < str, T?2 > /\ __kw_kwargs:T?2) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
        r'((self:bytearray) -> (return:NoneType))',
        r'((self:top) -> (return:NoneType))',
        r'((self:frozenset < T?3 > /\ iterable:Iterable < T?0 > /\ __d_start:int) -> (return:NoneType))',
        r'((self:range < int > /\ __stop:SupportsIndex) -> (return:NoneType))',
    },
    '__setattr__': {
        r'((self:top /\ __name:str /\ __value:top) -> (return:NoneType))',
    },
    '__delattr__': {
        r'((self:top /\ __name:str) -> (return:NoneType))',
    },
    '__eq__': {
        r'((self:float /\ __value:top) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:top) -> (return:bool))',
        r'((self:memoryview < int > /\ __value:top) -> (return:bool))',
        r'((self:bytearray /\ __value:top) -> (return:bool))',
        r'((self:complex /\ __value:top) -> (return:bool))',
        r'((self:bytes /\ __value:top) -> (return:bool))',
        r'((self:dict < T?1, T?2 > /\ __value:top) -> (return:bool))',
        r'((self:str /\ __value:top) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:top) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:top) -> (return:bool))',
        r'((self:int /\ __value:top) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:top) -> (return:bool))',
        r'((self:range < int > /\ __value:top) -> (return:bool))',
        r'((self:top /\ __value:top) -> (return:bool))',
    },
    '__ne__': {
        r'((self:float /\ __value:top) -> (return:bool))',
        r'((self:bytearray /\ __value:top) -> (return:bool))',
        r'((self:complex /\ __value:top) -> (return:bool))',
        r'((self:bytes /\ __value:top) -> (return:bool))',
        r'((self:str /\ __value:top) -> (return:bool))',
        r'((self:int /\ __value:top) -> (return:bool))',
        r'((self:top /\ __value:top) -> (return:bool))',
    },
    '__str__': {
        r'((self:top) -> (return:str))',
    },
    '__repr__': {
        r'((self:top) -> (return:str))',
    },
    '__hash__': {
        r'((self:str) -> (return:int))',
        r'((self:frozenset < T?3 >) -> (return:int))',
        r'((self:int) -> (return:int))',
        r'((self:bytes) -> (return:int))',
        r'((self:complex) -> (return:int))',
        r'((self:float) -> (return:int))',
        r'((self:range < int >) -> (return:int))',
        r'((self:top) -> (return:int))',
        r'((self:memoryview < int >) -> (return:int))',
        r'((self:tuple < T?3 >) -> (return:int))',
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
        r'((self:int) -> (return:int))',
        r'((self:float) -> (return:float))',
        r'((self:complex) -> (return:float))',
    },
    'numerator': {
        r'((self:int) -> (return:int))',
    },
    'conjugate': {
        r'((self:complex) -> (return:complex))',
        r'((self:float) -> (return:float))',
        r'((self:int) -> (return:int))',
    },
    'bit_length': {
        r'((self:int) -> (return:int))',
    },
    '__add__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?0 >) -> (return:tuple < T?0 + T?3 >))',
        r'((self:str /\ __value:str) -> (return:str))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:list < T?0 >))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:tuple < T?3 >))',
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bytearray))',
        r'((self:list < T?0 > /\ __value:list < T?4 >) -> (return:list < T?0 + T?4 >))',
        r'((self:bytes /\ __value:bytearray + bytes + memoryview) -> (return:bytes))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__sub__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:set < T?0 > /\ __value:set < T?0 + NoneType >) -> (return:set < T?0 >))',
        r'((self:frozenset < T?3 > /\ __value:set < T?3 >) -> (return:frozenset < T?3 >))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__mul__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:tuple < T?3 > /\ __value:SupportsIndex) -> (return:tuple < T?3 >))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
        r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
        r'((self:bytes /\ __value:SupportsIndex) -> (return:bytes))',
        r'((self:str /\ __value:SupportsIndex) -> (return:str))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__floordiv__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__truediv__': {
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
    },
    '__mod__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:str /\ __value:top) -> (return:str))',
        r'((self:str /\ __value:str + tuple < str >) -> (return:str))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:bytearray /\ __value:top) -> (return:bytes))',
        r'((self:bytes /\ __value:top) -> (return:bytes))',
    },
    '__divmod__': {
        r'((self:float /\ __value:float) -> (return:tuple < float >))',
        r'((self:int /\ __value:int) -> (return:tuple < int >))',
    },
    '__radd__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
    },
    '__rsub__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
    },
    '__rmul__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:tuple < T?3 > /\ __value:SupportsIndex) -> (return:tuple < T?3 >))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
        r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
        r'((self:bytes /\ __value:SupportsIndex) -> (return:bytes))',
        r'((self:str /\ __value:SupportsIndex) -> (return:str))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rfloordiv__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rtruediv__': {
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
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
        r'((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:int))',
        r'((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:top))',
        r'((self:complex /\ __value:complex /\ __d___mod:NoneType) -> (return:complex))',
        r'((self:int /\ __value:int /\ __mod:int) -> (return:int))',
        r'((self:float /\ __value:float /\ __d___mod:NoneType) -> (return:top))',
        r'((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
        r'((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
    },
    '__rpow__': {
        r'((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:complex))',
        r'((self:complex /\ __value:complex /\ __d___mod:NoneType) -> (return:complex))',
        r'((self:float /\ __value:float /\ __d___mod:NoneType) -> (return:top))',
        r'((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
        r'((self:int /\ __value:int /\ __d___mod:NoneType + int) -> (return:top))',
    },
    '__and__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:set < T?0 >))',
        r'((self:frozenset < T?3 > /\ __value:set < T?3 >) -> (return:frozenset < T?3 >))',
        r'((self:bool /\ __value:int) -> (return:int))',
    },
    '__or__': {
        r'((self:set < T?0 > /\ __value:set < T?4 >) -> (return:set < T?0 + T?4 >))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < T?4 >) -> (return:frozenset < T?4 + T?3 >))',
        r'((self:bool /\ __value:int) -> (return:int))',
    },
    '__xor__': {
        r'((self:set < T?0 > /\ __value:set < T?4 >) -> (return:set < T?0 + T?4 >))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < T?4 >) -> (return:frozenset < T?4 + T?3 >))',
        r'((self:bool /\ __value:int) -> (return:int))',
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
        r'((self:complex) -> (return:complex))',
        r'((self:float) -> (return:float))',
        r'((self:int) -> (return:int))',
    },
    '__pos__': {
        r'((self:complex) -> (return:complex))',
        r'((self:float) -> (return:float))',
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
        r'((self:int /\ __d___ndigits:SupportsIndex) -> (return:int))',
        r'((self:float /\ __d___ndigits:NoneType) -> (return:int))',
        r'((self:float /\ __ndigits:SupportsIndex) -> (return:float))',
    },
    '__getnewargs__': {
        r'((self:bool) -> (return:tuple < int >))',
        r'((self:float) -> (return:tuple < float >))',
        r'((self:bytes) -> (return:tuple < bytes >))',
        r'((self:str) -> (return:tuple < str >))',
        r'((self:int) -> (return:tuple < int >))',
    },
    '__lt__': {
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
    },
    '__le__': {
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
    },
    '__gt__': {
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
    },
    '__ge__': {
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
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
        r'((self:int) -> (return:int))',
        r'((self:float) -> (return:float))',
        r'((self:complex) -> (return:float))',
    },
    '__bool__': {
        r'((self:float) -> (return:bool))',
        r'((self:int) -> (return:bool))',
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
        r'((self:float) -> (return:float))',
        r'((self:complex) -> (return:float))',
    },
    'capitalize': {
        r'((self:bytes) -> (return:bytes))',
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:str) -> (return:str))',
    },
    'casefold': {
        r'((self:str) -> (return:str))',
    },
    'center': {
        r'((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytes) -> (return:bytearray))',
        r'((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
        r'((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytes) -> (return:bytes))',
    },
    'count': {
        r'((self:range < int > /\ __value:int) -> (return:int))',
        r'((self:tuple < T?3 > /\ __value:top) -> (return:int))',
        r'((self:bytes /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:bytearray /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:list < T?0 > /\ __value:T?0) -> (return:int))',
        r'((self:str /\ x:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
    },
    'encode': {
        r'((self:str /\ __d_encoding:str /\ __d_errors:str) -> (return:bytes))',
    },
    'endswith': {
        r'((self:str /\ __suffix:str + tuple < str > /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
        r'((self:bytearray /\ __suffix:bytearray + tuple < bytearray + bytes + memoryview > + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
        r'((self:bytes /\ __suffix:bytearray + tuple < bytearray + bytes + memoryview > + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
    },
    'find': {
        r'((self:str /\ __sub:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:bytearray /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:bytes /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
    },
    'format': {
        r'((self:memoryview < int >) -> (return:str))',
        r'((self:str /\ __va_args:str /\ __kw_kwargs:str) -> (return:str))',
        r'((self:str /\ __va_args:top /\ __kw_kwargs:top) -> (return:str))',
        r'((__value:top /\ __d___format_spec:str) -> (return:str))',
    },
    'format_map': {
        r'((self:str /\ map:dict < str, int >) -> (return:str))',
    },
    'index': {
        r'((self:range < int > /\ __value:int) -> (return:int))',
        r'((self:bytes /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:list < T?0 > /\ __value:T?0 /\ __d___start:SupportsIndex /\ __d___stop:SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:tuple < T?3 > /\ __value:top /\ __d___start:SupportsIndex /\ __d___stop:SupportsIndex) -> (return:int))',
        r'((self:str /\ __sub:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
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
        r'((self:bytes /\ __iterable_of_bytes:Iterable < bytearray + bytes + memoryview >) -> (return:bytes))',
        r'((self:str /\ __iterable:Iterable < str >) -> (return:str))',
        r'((self:bytearray /\ __iterable_of_bytes:Iterable < bytearray + bytes + memoryview >) -> (return:bytearray))',
    },
    'ljust': {
        r'((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytearray + bytes) -> (return:bytearray))',
        r'((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
        r'((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytearray + bytes) -> (return:bytes))',
    },
    'lower': {
        r'((self:bytes) -> (return:bytes))',
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:str) -> (return:str))',
    },
    'lstrip': {
        r'((self:bytearray /\ __d___bytes:bytearray + NoneType + bytes + memoryview) -> (return:bytearray))',
        r'((self:bytes /\ __d___bytes:bytearray + NoneType + bytes + memoryview) -> (return:bytes))',
        r'((self:str /\ __d___chars:str + NoneType) -> (return:str))',
    },
    'partition': {
        r'((self:str /\ __sep:str) -> (return:tuple < str >))',
        r'((self:bytearray /\ __sep:bytearray + bytes + memoryview) -> (return:tuple < bytearray >))',
        r'((self:bytes /\ __sep:bytearray + bytes + memoryview) -> (return:tuple < bytes >))',
    },
    'replace': {
        r'((self:bytes /\ __old:bytearray + bytes + memoryview /\ __new:bytearray + bytes + memoryview /\ __d___count:SupportsIndex) -> (return:bytes))',
        r'((self:bytearray /\ __old:bytearray + bytes + memoryview /\ __new:bytearray + bytes + memoryview /\ __d___count:SupportsIndex) -> (return:bytearray))',
        r'((self:str /\ __old:str /\ __new:str /\ __d___count:SupportsIndex) -> (return:str))',
    },
    'rfind': {
        r'((self:str /\ __sub:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:bytearray /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:bytes /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
    },
    'rindex': {
        r'((self:str /\ __sub:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:bytearray /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
        r'((self:bytes /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
    },
    'rjust': {
        r'((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytearray + bytes) -> (return:bytearray))',
        r'((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
        r'((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytearray + bytes) -> (return:bytes))',
    },
    'rpartition': {
        r'((self:str /\ __sep:str) -> (return:tuple < str >))',
        r'((self:bytearray /\ __sep:bytearray + bytes + memoryview) -> (return:tuple < bytearray >))',
        r'((self:bytes /\ __sep:bytearray + bytes + memoryview) -> (return:tuple < bytes >))',
    },
    'rsplit': {
        r'((self:str /\ __d_sep:str + NoneType /\ __d_maxsplit:SupportsIndex) -> (return:list < str >))',
        r'((self:bytes /\ __d_sep:bytearray + NoneType + bytes + memoryview /\ __d_maxsplit:SupportsIndex) -> (return:list < bytes >))',
        r'((self:bytearray /\ __d_sep:bytearray + NoneType + bytes + memoryview /\ __d_maxsplit:SupportsIndex) -> (return:list < bytearray >))',
    },
    'rstrip': {
        r'((self:bytearray /\ __d___bytes:bytearray + NoneType + bytes + memoryview) -> (return:bytearray))',
        r'((self:bytes /\ __d___bytes:bytearray + NoneType + bytes + memoryview) -> (return:bytes))',
        r'((self:str /\ __d___chars:str + NoneType) -> (return:str))',
    },
    'split': {
        r'((self:str /\ __d_sep:str + NoneType /\ __d_maxsplit:SupportsIndex) -> (return:list < str >))',
        r'((self:bytes /\ __d_sep:bytearray + NoneType + bytes + memoryview /\ __d_maxsplit:SupportsIndex) -> (return:list < bytes >))',
        r'((self:bytearray /\ __d_sep:bytearray + NoneType + bytes + memoryview /\ __d_maxsplit:SupportsIndex) -> (return:list < bytearray >))',
    },
    'splitlines': {
        r'((self:str /\ __d_keepends:bool) -> (return:list < str >))',
        r'((self:bytes /\ __d_keepends:bool) -> (return:list < bytes >))',
        r'((self:bytearray /\ __d_keepends:bool) -> (return:list < bytearray >))',
    },
    'startswith': {
        r'((self:bytes /\ __prefix:bytearray + tuple < bytearray + bytes + memoryview > + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
        r'((self:str /\ __prefix:str + tuple < str > /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
        r'((self:bytearray /\ __prefix:bytearray + tuple < bytearray + bytes + memoryview > + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
    },
    'strip': {
        r'((self:bytearray /\ __d___bytes:bytearray + NoneType + bytes + memoryview) -> (return:bytearray))',
        r'((self:bytes /\ __d___bytes:bytearray + NoneType + bytes + memoryview) -> (return:bytes))',
        r'((self:str /\ __d___chars:str + NoneType) -> (return:str))',
    },
    'swapcase': {
        r'((self:bytes) -> (return:bytes))',
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:str) -> (return:str))',
    },
    'title': {
        r'((self:bytes) -> (return:bytes))',
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:str) -> (return:str))',
    },
    'translate': {
        r'((self:str /\ __table:dict < int, str + int >) -> (return:str))',
        r'((self:bytearray /\ __table:bytearray + NoneType + bytes + memoryview /\ __d_delete:bytes) -> (return:bytearray))',
        r'((self:bytes /\ __table:bytearray + NoneType + bytes + memoryview /\ __d_delete:bytes) -> (return:bytes))',
    },
    'upper': {
        r'((self:bytes) -> (return:bytes))',
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:str) -> (return:str))',
    },
    'zfill': {
        r'((self:bytearray /\ __width:SupportsIndex) -> (return:bytearray))',
        r'((self:str /\ __width:SupportsIndex) -> (return:str))',
        r'((self:bytes /\ __width:SupportsIndex) -> (return:bytes))',
    },
    'maketrans': {
        r'((__frm:bytearray + bytes + memoryview /\ __to:bytearray + bytes + memoryview) -> (return:bytes))',
        r'((__x:str /\ __y:str /\ __z:str) -> (return:dict < int, NoneType + int >))',
        r'((__x:dict < str, T?0 > + dict < str + int, T?0 > + dict < int, T?0 >) -> (return:dict < int, T?0 >))',
        r'((__x:str /\ __y:str) -> (return:dict < int, int >))',
    },
    '__contains__': {
        r'((self:tuple < T?3 > /\ __key:top) -> (return:bool))',
        r'((self:range < int > /\ __key:top) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __o:top) -> (return:bool))',
        r'((self:set < T?0 > /\ __o:top) -> (return:bool))',
        r'((self:str /\ __key:str) -> (return:bool))',
        r'((self:bytes /\ __key:bytearray + SupportsIndex + bytes + memoryview) -> (return:bool))',
        r'((self:memoryview < int > /\ __x:top) -> (return:bool))',
        r'((self:bytearray /\ __key:bytearray + SupportsIndex + bytes + memoryview) -> (return:bool))',
        r'((self:list < T?0 > /\ __key:top) -> (return:bool))',
    },
    '__getitem__': {
        r'((self:tuple < T?3 > /\ __key:SupportsIndex) -> (return:T?3))',
        r'((self:bytes /\ __key:SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __key:SupportsIndex) -> (return:int))',
        r'((self:list < T?0 > /\ __i:SupportsIndex) -> (return:T?0))',
        r'((self:range < int > /\ __key:SupportsIndex) -> (return:int))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:T?2))',
        r'((self:memoryview < int > /\ __key:SupportsIndex) -> (return:int))',
        r'((self:str /\ __key:SupportsIndex) -> (return:str))',
    },
    '__len__': {
        r'((self:str) -> (return:int))',
        r'((self:frozenset < T?3 >) -> (return:int))',
        r'((self:bytearray) -> (return:int))',
        r'((self:bytes) -> (return:int))',
        r'((self:list < T?0 >) -> (return:int))',
        r'((self:range < int >) -> (return:int))',
        r'((self:set < T?0 >) -> (return:int))',
        r'((self:memoryview < int >) -> (return:int))',
        r'((self:tuple < T?3 >) -> (return:int))',
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
        r'((self:bytearray /\ __item:SupportsIndex) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __object:T?1) -> (self:list < T?1 + T?0 > /\ return:NoneType))',
        r'((self:list < bot > /\ __object:T?0) -> (self:list < T?0 > /\ return:NoneType))',
    },
    'copy': {
        r'((self:list < T?0 >) -> (return:list < T?0 >))',
        r'((self:dict < T?1, T?2 >) -> (return:dict < T?1, T?2 >))',
        r'((self:frozenset < T?3 >) -> (return:frozenset < T?3 >))',
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:set < T?0 >) -> (return:set < T?0 >))',
    },
    'extend': {
        r'((self:list < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
        r'((self:bytearray /\ __iterable_of_ints:Iterable < SupportsIndex >) -> (return:NoneType))',
    },
    'insert': {
        r'((self:list < T?0 > /\ __index:SupportsIndex /\ __object:T?0) -> (return:NoneType))',
        r'((self:bytearray /\ __index:SupportsIndex /\ __item:SupportsIndex) -> (return:NoneType))',
    },
    'pop': {
        r'((self:bytearray /\ __d___index:int) -> (return:int))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?2) -> (return:T?2))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:T?2))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?0) -> (return:T?0 + T?2))',
        r'((self:list < T?0 > /\ __d___index:SupportsIndex) -> (return:T?0))',
    },
    'remove': {
        r'((self:list < T?0 > /\ __value:T?0) -> (return:NoneType))',
        r'((self:set < T?0 > /\ __element:T?0) -> (return:NoneType))',
        r'((self:bytearray /\ __value:int) -> (return:NoneType))',
    },
    '__setitem__': {
        r'((self:list < T?0 > /\ __key:SupportsIndex /\ __value:T?0) -> (return:NoneType))',
        r'((self:memoryview < int > /\ __key:SupportsIndex /\ __value:SupportsIndex) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __value:T?2) -> (return:NoneType))',
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
    'cast': {
        r'((self:memoryview < int > /\ format:str /\ __d_shape:tuple < int > + list < int >) -> (return:memoryview))',
    },
    'tolist': {
        r'((self:memoryview < int >) -> (return:list < int >))',
    },
    'release': {
        r'((self:memoryview < int >) -> (return:NoneType))',
    },
    '__closure__': {
        r'((self:tuple < T?3 >) -> (return:tuple < _Cell > + NoneType))',
    },
    '__globals__': {
        r'((self:tuple < T?3 >) -> (return:dict < str, top >))',
    },
    '__get__': {
        r'((self:tuple < T?3 > /\ __instance:top /\ __d___owner:NoneType) -> (return:top))',
    },
    'get': {
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?2) -> (return:T?2))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?0) -> (return:T?0 + T?2))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:NoneType + T?2))',
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
        r'((self:frozenset < T?3 > /\ __s:Iterable < top >) -> (return:bool))',
        r'((self:set < T?0 > /\ __s:Iterable < top >) -> (return:bool))',
    },
    'issuperset': {
        r'((self:frozenset < T?3 > /\ __s:Iterable < top >) -> (return:bool))',
        r'((self:set < T?0 > /\ __s:Iterable < top >) -> (return:bool))',
    },
    'symmetric_difference': {
        r'((self:set < T?0 > /\ __s:Iterable < T?0 >) -> (return:set < T?0 >))',
        r'((self:frozenset < T?3 > /\ __s:Iterable < T?3 >) -> (return:frozenset < T?3 >))',
    },
    'symmetric_difference_update': {
        r'((self:set < T?0 > /\ __s:Iterable < T?0 >) -> (return:NoneType))',
    },
    'union': {
        r'((self:set < T?0 > /\ __va_s:Iterable < T?4 >) -> (return:set < T?0 + T?4 >))',
        r'((self:frozenset < T?3 > /\ __va_s:Iterable < T?4 >) -> (return:frozenset < T?4 + T?3 >))',
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
        r'((__o:top /\ __name:str /\ __default:bool) -> (return:top + bool))',
        r'((__o:top /\ __name:str) -> (return:top))',
        r'((__o:top /\ __name:str /\ __default:T?0) -> (return:T?0 + top))',
        r'((__o:top /\ name:str /\ __default:dict < top, top >) -> (return:top + dict < top, top >))',
        r'((__o:top /\ name:str /\ __default:list < top >) -> (return:top + list < top >))',
        r'((__o:top /\ __name:str /\ __default:NoneType) -> (return:top + NoneType))',
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
        r'((__c:str + bytearray + bytes) -> (return:int))',
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
        r'((x:set < T?0 > /\ y:T?1) -> (x:set < T?1 + T?0 > /\ return:NoneType))',
        r'((x:list < T?0 > /\ y:T?1) -> (x:list < T?1 + T?0 > /\ return:NoneType))',
        r'((x:dict < T?0, T?1 > /\ y:T?2) -> (x:dict < T?0, T?1 + T?2 > /\ return:NoneType))',
        r'((x:tuple < T?0 > /\ y:T?1) -> (x:tuple < T?1 + T?0 > /\ return:NoneType))',
        r'((x:frozenset < T?0 > /\ y:T?1) -> (x:frozenset < T?1 + T?0 > /\ return:NoneType))',
    },
    'assign_1_prim': {
        r'((c:str + tuple < T?1 + T?0 >) -> (return:tuple < T?1 + T?0 + str >))',
    },
    'for_parse': {
        r'((target:top /\ iter:Iterable < T?0 >) -> (target:T?0))',
        r'((target:top /\ iter:bytes) -> (target:int))',
        r'((target:top /\ iter:memoryview) -> (target:int))',
        r'((target:top /\ iter:range) -> (target:int))',
        r'((target:top /\ iter:str) -> (target:str))',
        r'((target:top /\ iter:bytearray) -> (target:int))',
    },
    'range': {
        r'((stop:int) -> (return:range))',
        r'((start:int /\ stop:int) -> (return:range))',
        r'((start:int /\ stop:int /\ step:int) -> (return:range))',
    },

}
class_specs = {
    'object': {
        'attributes': {},
        'methods': {
            '__init__': {
                '((self:top) -> (return:NoneType))',
            },
            '__setattr__': {
                '((self:top /\ __name:str /\ __value:top) -> (return:NoneType))',
            },
            '__delattr__': {
                '((self:top /\ __name:str) -> (return:NoneType))',
            },
            '__eq__': {
                '((self:top /\ __value:top) -> (return:bool))',
            },
            '__ne__': {
                '((self:top /\ __value:top) -> (return:bool))',
            },
            '__str__': {
                '((self:top) -> (return:str))',
            },
            '__repr__': {
                '((self:top) -> (return:str))',
            },
            '__hash__': {
                '((self:top) -> (return:int))',
            },
            '__format__': {
                '((self:top /\ __format_spec:str) -> (return:str))',
            },
            '__getattribute__': {
                '((self:top /\ __name:str) -> (return:top))',
            },
            '__sizeof__': {
                '((self:top) -> (return:int))',
            },
            '__reduce__': {
                '((self:top) -> (return:str + tuple < top >))',
            },
            '__dir__': {
                '((self:top) -> (return:Iterable < str >))',
            },
        }
    },
    'int': {
        'attributes': {},
        'methods': {
            'real': {
                '((self:int) -> (return:int))',
            },
            'numerator': {
                '((self:int) -> (return:int))',
            },
            'conjugate': {
                '((self:int) -> (return:int))',
            },
            'bit_length': {
                '((self:int) -> (return:int))',
            },
            '__add__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__sub__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__mul__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__floordiv__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__truediv__': {
                '((self:int /\ __value:int) -> (return:float))',
            },
            '__mod__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__divmod__': {
                '((self:int /\ __value:int) -> (return:tuple < int >))',
            },
            '__radd__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__rsub__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__rmul__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__rfloordiv__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__rtruediv__': {
                '((self:int /\ __value:int) -> (return:float))',
            },
            '__rmod__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__rdivmod__': {
                '((self:int /\ __value:int) -> (return:tuple < int >))',
            },
            '__pow__': {
                '((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:int))',
                '((self:int /\ __value:int /\ __mod:int) -> (return:int))',
                '((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:top))',
                '((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
            },
            '__rpow__': {
                '((self:int /\ __value:int /\ __d___mod:NoneType + int) -> (return:top))',
            },
            '__and__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__or__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__xor__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__lshift__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__rshift__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__rand__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__ror__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__rxor__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__rlshift__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__rrshift__': {
                '((self:int /\ __value:int) -> (return:int))',
            },
            '__neg__': {
                '((self:int) -> (return:int))',
            },
            '__pos__': {
                '((self:int) -> (return:int))',
            },
            '__invert__': {
                '((self:int) -> (return:int))',
            },
            '__trunc__': {
                '((self:int) -> (return:int))',
            },
            '__ceil__': {
                '((self:int) -> (return:int))',
            },
            '__floor__': {
                '((self:int) -> (return:int))',
            },
            '__round__': {
                '((self:int /\ __d___ndigits:SupportsIndex) -> (return:int))',
            },
            '__getnewargs__': {
                '((self:int) -> (return:tuple < int >))',
            },
            '__eq__': {
                '((self:int /\ __value:top) -> (return:bool))',
            },
            '__ne__': {
                '((self:int /\ __value:top) -> (return:bool))',
            },
            '__lt__': {
                '((self:int /\ __value:int) -> (return:bool))',
            },
            '__le__': {
                '((self:int /\ __value:int) -> (return:bool))',
            },
            '__gt__': {
                '((self:int /\ __value:int) -> (return:bool))',
            },
            '__ge__': {
                '((self:int /\ __value:int) -> (return:bool))',
            },
            '__float__': {
                '((self:int) -> (return:float))',
            },
            '__int__': {
                '((self:int) -> (return:int))',
            },
            '__abs__': {
                '((self:int) -> (return:int))',
            },
            '__hash__': {
                '((self:int) -> (return:int))',
            },
            '__bool__': {
                '((self:int) -> (return:bool))',
            },
            '__index__': {
                '((self:int) -> (return:int))',
            },
        }
    },
    'float': {
        'attributes': {},
        'methods': {
            'as_integer_ratio': {
                '((self:float) -> (return:tuple < int >))',
            },
            'hex': {
                '((self:float) -> (return:str))',
            },
            'is_integer': {
                '((self:float) -> (return:bool))',
            },
            'real': {
                '((self:float) -> (return:float))',
            },
            'imag': {
                '((self:float) -> (return:float))',
            },
            'conjugate': {
                '((self:float) -> (return:float))',
            },
            '__add__': {
                '((self:float /\ __value:float) -> (return:float))',
            },
            '__sub__': {
                '((self:float /\ __value:float) -> (return:float))',
            },
            '__mul__': {
                '((self:float /\ __value:float) -> (return:float))',
            },
            '__floordiv__': {
                '((self:float /\ __value:float) -> (return:float))',
            },
            '__truediv__': {
                '((self:float /\ __value:float) -> (return:float))',
            },
            '__mod__': {
                '((self:float /\ __value:float) -> (return:float))',
            },
            '__divmod__': {
                '((self:float /\ __value:float) -> (return:tuple < float >))',
            },
            '__pow__': {
                '((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
                '((self:float /\ __value:float /\ __d___mod:NoneType) -> (return:top))',
            },
            '__radd__': {
                '((self:float /\ __value:float) -> (return:float))',
            },
            '__rsub__': {
                '((self:float /\ __value:float) -> (return:float))',
            },
            '__rmul__': {
                '((self:float /\ __value:float) -> (return:float))',
            },
            '__rfloordiv__': {
                '((self:float /\ __value:float) -> (return:float))',
            },
            '__rtruediv__': {
                '((self:float /\ __value:float) -> (return:float))',
            },
            '__rmod__': {
                '((self:float /\ __value:float) -> (return:float))',
            },
            '__rdivmod__': {
                '((self:float /\ __value:float) -> (return:tuple < float >))',
            },
            '__rpow__': {
                '((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
                '((self:float /\ __value:float /\ __d___mod:NoneType) -> (return:top))',
                '((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:complex))',
            },
            '__getnewargs__': {
                '((self:float) -> (return:tuple < float >))',
            },
            '__trunc__': {
                '((self:float) -> (return:int))',
            },
            '__round__': {
                '((self:float /\ __d___ndigits:NoneType) -> (return:int))',
                '((self:float /\ __ndigits:SupportsIndex) -> (return:float))',
            },
            '__eq__': {
                '((self:float /\ __value:top) -> (return:bool))',
            },
            '__ne__': {
                '((self:float /\ __value:top) -> (return:bool))',
            },
            '__lt__': {
                '((self:float /\ __value:float) -> (return:bool))',
            },
            '__le__': {
                '((self:float /\ __value:float) -> (return:bool))',
            },
            '__gt__': {
                '((self:float /\ __value:float) -> (return:bool))',
            },
            '__ge__': {
                '((self:float /\ __value:float) -> (return:bool))',
            },
            '__neg__': {
                '((self:float) -> (return:float))',
            },
            '__pos__': {
                '((self:float) -> (return:float))',
            },
            '__int__': {
                '((self:float) -> (return:int))',
            },
            '__float__': {
                '((self:float) -> (return:float))',
            },
            '__abs__': {
                '((self:float) -> (return:float))',
            },
            '__hash__': {
                '((self:float) -> (return:int))',
            },
            '__bool__': {
                '((self:float) -> (return:bool))',
            },
        }
    },
    'complex': {
        'attributes': {},
        'methods': {
            'real': {
                '((self:complex) -> (return:float))',
            },
            'imag': {
                '((self:complex) -> (return:float))',
            },
            'conjugate': {
                '((self:complex) -> (return:complex))',
            },
            '__add__': {
                '((self:complex /\ __value:complex) -> (return:complex))',
            },
            '__sub__': {
                '((self:complex /\ __value:complex) -> (return:complex))',
            },
            '__mul__': {
                '((self:complex /\ __value:complex) -> (return:complex))',
            },
            '__pow__': {
                '((self:complex /\ __value:complex /\ __d___mod:NoneType) -> (return:complex))',
            },
            '__truediv__': {
                '((self:complex /\ __value:complex) -> (return:complex))',
            },
            '__radd__': {
                '((self:complex /\ __value:complex) -> (return:complex))',
            },
            '__rsub__': {
                '((self:complex /\ __value:complex) -> (return:complex))',
            },
            '__rmul__': {
                '((self:complex /\ __value:complex) -> (return:complex))',
            },
            '__rpow__': {
                '((self:complex /\ __value:complex /\ __d___mod:NoneType) -> (return:complex))',
            },
            '__rtruediv__': {
                '((self:complex /\ __value:complex) -> (return:complex))',
            },
            '__eq__': {
                '((self:complex /\ __value:top) -> (return:bool))',
            },
            '__ne__': {
                '((self:complex /\ __value:top) -> (return:bool))',
            },
            '__neg__': {
                '((self:complex) -> (return:complex))',
            },
            '__pos__': {
                '((self:complex) -> (return:complex))',
            },
            '__abs__': {
                '((self:complex) -> (return:float))',
            },
            '__hash__': {
                '((self:complex) -> (return:int))',
            },
            '__bool__': {
                '((self:complex) -> (return:bool))',
            },
        }
    },
    'str': {
        'attributes': {},
        'methods': {
            'capitalize': {
                '((self:str) -> (return:str))',
            },
            'casefold': {
                '((self:str) -> (return:str))',
            },
            'center': {
                '((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
            },
            'count': {
                '((self:str /\ x:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'encode': {
                '((self:str /\ __d_encoding:str /\ __d_errors:str) -> (return:bytes))',
            },
            'endswith': {
                '((self:str /\ __suffix:str + tuple < str > /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
            },
            'find': {
                '((self:str /\ __sub:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'format': {
                '((self:str /\ __va_args:str /\ __kw_kwargs:str) -> (return:str))',
                '((self:str /\ __va_args:top /\ __kw_kwargs:top) -> (return:str))',
            },
            'format_map': {
                '((self:str /\ map:dict < str, int >) -> (return:str))',
            },
            'index': {
                '((self:str /\ __sub:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'isalnum': {
                '((self:str) -> (return:bool))',
            },
            'isalpha': {
                '((self:str) -> (return:bool))',
            },
            'isascii': {
                '((self:str) -> (return:bool))',
            },
            'isdecimal': {
                '((self:str) -> (return:bool))',
            },
            'isdigit': {
                '((self:str) -> (return:bool))',
            },
            'isidentifier': {
                '((self:str) -> (return:bool))',
            },
            'islower': {
                '((self:str) -> (return:bool))',
            },
            'isnumeric': {
                '((self:str) -> (return:bool))',
            },
            'isprintable': {
                '((self:str) -> (return:bool))',
            },
            'isspace': {
                '((self:str) -> (return:bool))',
            },
            'istitle': {
                '((self:str) -> (return:bool))',
            },
            'isupper': {
                '((self:str) -> (return:bool))',
            },
            'join': {
                '((self:str /\ __iterable:Iterable < str >) -> (return:str))',
            },
            'ljust': {
                '((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
            },
            'lower': {
                '((self:str) -> (return:str))',
            },
            'lstrip': {
                '((self:str /\ __d___chars:str + NoneType) -> (return:str))',
            },
            'partition': {
                '((self:str /\ __sep:str) -> (return:tuple < str >))',
            },
            'replace': {
                '((self:str /\ __old:str /\ __new:str /\ __d___count:SupportsIndex) -> (return:str))',
            },
            'rfind': {
                '((self:str /\ __sub:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'rindex': {
                '((self:str /\ __sub:str /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'rjust': {
                '((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
            },
            'rpartition': {
                '((self:str /\ __sep:str) -> (return:tuple < str >))',
            },
            'rsplit': {
                '((self:str /\ __d_sep:str + NoneType /\ __d_maxsplit:SupportsIndex) -> (return:list < str >))',
            },
            'rstrip': {
                '((self:str /\ __d___chars:str + NoneType) -> (return:str))',
            },
            'split': {
                '((self:str /\ __d_sep:str + NoneType /\ __d_maxsplit:SupportsIndex) -> (return:list < str >))',
            },
            'splitlines': {
                '((self:str /\ __d_keepends:bool) -> (return:list < str >))',
            },
            'startswith': {
                '((self:str /\ __prefix:str + tuple < str > /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
            },
            'strip': {
                '((self:str /\ __d___chars:str + NoneType) -> (return:str))',
            },
            'swapcase': {
                '((self:str) -> (return:str))',
            },
            'title': {
                '((self:str) -> (return:str))',
            },
            'translate': {
                '((self:str /\ __table:dict < int, str + int >) -> (return:str))',
            },
            'upper': {
                '((self:str) -> (return:str))',
            },
            'zfill': {
                '((self:str /\ __width:SupportsIndex) -> (return:str))',
            },
            'maketrans': {
                '((__x:str /\ __y:str /\ __z:str) -> (return:dict < int, NoneType + int >))',
                '((__x:dict < str, T?0 > + dict < str + int, T?0 > + dict < int, T?0 >) -> (return:dict < int, T?0 >))',
                '((__x:str /\ __y:str) -> (return:dict < int, int >))',
            },
            '__add__': {
                '((self:str /\ __value:str) -> (return:str))',
            },
            '__contains__': {
                '((self:str /\ __key:str) -> (return:bool))',
            },
            '__eq__': {
                '((self:str /\ __value:top) -> (return:bool))',
            },
            '__ge__': {
                '((self:str /\ __value:str) -> (return:bool))',
            },
            '__getitem__': {
                '((self:str /\ __key:SupportsIndex) -> (return:str))',
            },
            '__gt__': {
                '((self:str /\ __value:str) -> (return:bool))',
            },
            '__hash__': {
                '((self:str) -> (return:int))',
            },
            '__le__': {
                '((self:str /\ __value:str) -> (return:bool))',
            },
            '__len__': {
                '((self:str) -> (return:int))',
            },
            '__lt__': {
                '((self:str /\ __value:str) -> (return:bool))',
            },
            '__mod__': {
                '((self:str /\ __value:str + tuple < str >) -> (return:str))',
                '((self:str /\ __value:top) -> (return:str))',
            },
            '__mul__': {
                '((self:str /\ __value:SupportsIndex) -> (return:str))',
            },
            '__ne__': {
                '((self:str /\ __value:top) -> (return:bool))',
            },
            '__rmul__': {
                '((self:str /\ __value:SupportsIndex) -> (return:str))',
            },
            '__getnewargs__': {
                '((self:str) -> (return:tuple < str >))',
            },
        }
    },
    'bytes': {
        'attributes': {},
        'methods': {
            'capitalize': {
                '((self:bytes) -> (return:bytes))',
            },
            'center': {
                '((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytes) -> (return:bytes))',
            },
            'count': {
                '((self:bytes /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'decode': {
                '((self:bytes /\ __d_encoding:str /\ __d_errors:str) -> (return:str))',
            },
            'endswith': {
                '((self:bytes /\ __suffix:bytearray + tuple < bytearray + bytes + memoryview > + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
            },
            'find': {
                '((self:bytes /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'index': {
                '((self:bytes /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'isalnum': {
                '((self:bytes) -> (return:bool))',
            },
            'isalpha': {
                '((self:bytes) -> (return:bool))',
            },
            'isascii': {
                '((self:bytes) -> (return:bool))',
            },
            'isdigit': {
                '((self:bytes) -> (return:bool))',
            },
            'islower': {
                '((self:bytes) -> (return:bool))',
            },
            'isspace': {
                '((self:bytes) -> (return:bool))',
            },
            'istitle': {
                '((self:bytes) -> (return:bool))',
            },
            'isupper': {
                '((self:bytes) -> (return:bool))',
            },
            'join': {
                '((self:bytes /\ __iterable_of_bytes:Iterable < bytearray + bytes + memoryview >) -> (return:bytes))',
            },
            'ljust': {
                '((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytearray + bytes) -> (return:bytes))',
            },
            'lower': {
                '((self:bytes) -> (return:bytes))',
            },
            'lstrip': {
                '((self:bytes /\ __d___bytes:bytearray + NoneType + bytes + memoryview) -> (return:bytes))',
            },
            'partition': {
                '((self:bytes /\ __sep:bytearray + bytes + memoryview) -> (return:tuple < bytes >))',
            },
            'replace': {
                '((self:bytes /\ __old:bytearray + bytes + memoryview /\ __new:bytearray + bytes + memoryview /\ __d___count:SupportsIndex) -> (return:bytes))',
            },
            'rfind': {
                '((self:bytes /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'rindex': {
                '((self:bytes /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'rjust': {
                '((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytearray + bytes) -> (return:bytes))',
            },
            'rpartition': {
                '((self:bytes /\ __sep:bytearray + bytes + memoryview) -> (return:tuple < bytes >))',
            },
            'rsplit': {
                '((self:bytes /\ __d_sep:bytearray + NoneType + bytes + memoryview /\ __d_maxsplit:SupportsIndex) -> (return:list < bytes >))',
            },
            'rstrip': {
                '((self:bytes /\ __d___bytes:bytearray + NoneType + bytes + memoryview) -> (return:bytes))',
            },
            'split': {
                '((self:bytes /\ __d_sep:bytearray + NoneType + bytes + memoryview /\ __d_maxsplit:SupportsIndex) -> (return:list < bytes >))',
            },
            'splitlines': {
                '((self:bytes /\ __d_keepends:bool) -> (return:list < bytes >))',
            },
            'startswith': {
                '((self:bytes /\ __prefix:bytearray + tuple < bytearray + bytes + memoryview > + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
            },
            'strip': {
                '((self:bytes /\ __d___bytes:bytearray + NoneType + bytes + memoryview) -> (return:bytes))',
            },
            'swapcase': {
                '((self:bytes) -> (return:bytes))',
            },
            'title': {
                '((self:bytes) -> (return:bytes))',
            },
            'translate': {
                '((self:bytes /\ __table:bytearray + NoneType + bytes + memoryview /\ __d_delete:bytes) -> (return:bytes))',
            },
            'upper': {
                '((self:bytes) -> (return:bytes))',
            },
            'zfill': {
                '((self:bytes /\ __width:SupportsIndex) -> (return:bytes))',
            },
            'maketrans': {
                '((__frm:bytearray + bytes + memoryview /\ __to:bytearray + bytes + memoryview) -> (return:bytes))',
            },
            '__len__': {
                '((self:bytes) -> (return:int))',
            },
            '__hash__': {
                '((self:bytes) -> (return:int))',
            },
            '__getitem__': {
                '((self:bytes /\ __key:SupportsIndex) -> (return:int))',
            },
            '__add__': {
                '((self:bytes /\ __value:bytearray + bytes + memoryview) -> (return:bytes))',
            },
            '__mul__': {
                '((self:bytes /\ __value:SupportsIndex) -> (return:bytes))',
            },
            '__rmul__': {
                '((self:bytes /\ __value:SupportsIndex) -> (return:bytes))',
            },
            '__mod__': {
                '((self:bytes /\ __value:top) -> (return:bytes))',
            },
            '__contains__': {
                '((self:bytes /\ __key:bytearray + SupportsIndex + bytes + memoryview) -> (return:bool))',
            },
            '__eq__': {
                '((self:bytes /\ __value:top) -> (return:bool))',
            },
            '__ne__': {
                '((self:bytes /\ __value:top) -> (return:bool))',
            },
            '__lt__': {
                '((self:bytes /\ __value:bytes) -> (return:bool))',
            },
            '__le__': {
                '((self:bytes /\ __value:bytes) -> (return:bool))',
            },
            '__gt__': {
                '((self:bytes /\ __value:bytes) -> (return:bool))',
            },
            '__ge__': {
                '((self:bytes /\ __value:bytes) -> (return:bool))',
            },
            '__getnewargs__': {
                '((self:bytes) -> (return:tuple < bytes >))',
            },
            '__buffer__': {
                '((self:bytes /\ __flags:int) -> (return:memoryview))',
            },
        }
    },
    'bytearray': {
        'attributes': {},
        'methods': {
            '__init__': {
                '((self:bytearray) -> (return:NoneType))',
                '((self:bytearray /\ __string:str /\ encoding:str /\ __d_errors:str) -> (return:NoneType))',
                '((self:bytearray /\ __ints:bytearray + bytes + memoryview + SupportsIndex + Iterable < SupportsIndex >) -> (return:NoneType))',
            },
            'append': {
                '((self:bytearray /\ __item:SupportsIndex) -> (return:NoneType))',
            },
            'capitalize': {
                '((self:bytearray) -> (return:bytearray))',
            },
            'center': {
                '((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytes) -> (return:bytearray))',
            },
            'count': {
                '((self:bytearray /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'copy': {
                '((self:bytearray) -> (return:bytearray))',
            },
            'decode': {
                '((self:bytearray /\ __d_encoding:str /\ __d_errors:str) -> (return:str))',
            },
            'endswith': {
                '((self:bytearray /\ __suffix:bytearray + tuple < bytearray + bytes + memoryview > + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
            },
            'extend': {
                '((self:bytearray /\ __iterable_of_ints:Iterable < SupportsIndex >) -> (return:NoneType))',
            },
            'find': {
                '((self:bytearray /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'index': {
                '((self:bytearray /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'insert': {
                '((self:bytearray /\ __index:SupportsIndex /\ __item:SupportsIndex) -> (return:NoneType))',
            },
            'isalnum': {
                '((self:bytearray) -> (return:bool))',
            },
            'isalpha': {
                '((self:bytearray) -> (return:bool))',
            },
            'isascii': {
                '((self:bytearray) -> (return:bool))',
            },
            'isdigit': {
                '((self:bytearray) -> (return:bool))',
            },
            'islower': {
                '((self:bytearray) -> (return:bool))',
            },
            'isspace': {
                '((self:bytearray) -> (return:bool))',
            },
            'istitle': {
                '((self:bytearray) -> (return:bool))',
            },
            'isupper': {
                '((self:bytearray) -> (return:bool))',
            },
            'join': {
                '((self:bytearray /\ __iterable_of_bytes:Iterable < bytearray + bytes + memoryview >) -> (return:bytearray))',
            },
            'ljust': {
                '((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytearray + bytes) -> (return:bytearray))',
            },
            'lower': {
                '((self:bytearray) -> (return:bytearray))',
            },
            'lstrip': {
                '((self:bytearray /\ __d___bytes:bytearray + NoneType + bytes + memoryview) -> (return:bytearray))',
            },
            'partition': {
                '((self:bytearray /\ __sep:bytearray + bytes + memoryview) -> (return:tuple < bytearray >))',
            },
            'pop': {
                '((self:bytearray /\ __d___index:int) -> (return:int))',
            },
            'remove': {
                '((self:bytearray /\ __value:int) -> (return:NoneType))',
            },
            'replace': {
                '((self:bytearray /\ __old:bytearray + bytes + memoryview /\ __new:bytearray + bytes + memoryview /\ __d___count:SupportsIndex) -> (return:bytearray))',
            },
            'rfind': {
                '((self:bytearray /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'rindex': {
                '((self:bytearray /\ __sub:bytearray + SupportsIndex + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:int))',
            },
            'rjust': {
                '((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytearray + bytes) -> (return:bytearray))',
            },
            'rpartition': {
                '((self:bytearray /\ __sep:bytearray + bytes + memoryview) -> (return:tuple < bytearray >))',
            },
            'rsplit': {
                '((self:bytearray /\ __d_sep:bytearray + NoneType + bytes + memoryview /\ __d_maxsplit:SupportsIndex) -> (return:list < bytearray >))',
            },
            'rstrip': {
                '((self:bytearray /\ __d___bytes:bytearray + NoneType + bytes + memoryview) -> (return:bytearray))',
            },
            'split': {
                '((self:bytearray /\ __d_sep:bytearray + NoneType + bytes + memoryview /\ __d_maxsplit:SupportsIndex) -> (return:list < bytearray >))',
            },
            'splitlines': {
                '((self:bytearray /\ __d_keepends:bool) -> (return:list < bytearray >))',
            },
            'startswith': {
                '((self:bytearray /\ __prefix:bytearray + tuple < bytearray + bytes + memoryview > + bytes + memoryview /\ __d___start:SupportsIndex + NoneType /\ __d___end:SupportsIndex + NoneType) -> (return:bool))',
            },
            'strip': {
                '((self:bytearray /\ __d___bytes:bytearray + NoneType + bytes + memoryview) -> (return:bytearray))',
            },
            'swapcase': {
                '((self:bytearray) -> (return:bytearray))',
            },
            'title': {
                '((self:bytearray) -> (return:bytearray))',
            },
            'translate': {
                '((self:bytearray /\ __table:bytearray + NoneType + bytes + memoryview /\ __d_delete:bytes) -> (return:bytearray))',
            },
            'upper': {
                '((self:bytearray) -> (return:bytearray))',
            },
            'zfill': {
                '((self:bytearray /\ __width:SupportsIndex) -> (return:bytearray))',
            },
            'maketrans': {
                '((__frm:bytearray + bytes + memoryview /\ __to:bytearray + bytes + memoryview) -> (return:bytes))',
            },
            '__len__': {
                '((self:bytearray) -> (return:int))',
            },
            '__getitem__': {
                '((self:bytearray /\ __key:SupportsIndex) -> (return:int))',
            },
            '__setitem__': {
                '((self:bytearray /\ __key:SupportsIndex /\ __value:SupportsIndex) -> (return:NoneType))',
            },
            '__delitem__': {
                '((self:bytearray /\ __key:SupportsIndex) -> (return:NoneType))',
            },
            '__add__': {
                '((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bytearray))',
            },
            '__iadd__': {
                '((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bytearray))',
            },
            '__mul__': {
                '((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
            },
            '__rmul__': {
                '((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
            },
            '__imul__': {
                '((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
            },
            '__mod__': {
                '((self:bytearray /\ __value:top) -> (return:bytes))',
            },
            '__contains__': {
                '((self:bytearray /\ __key:bytearray + SupportsIndex + bytes + memoryview) -> (return:bool))',
            },
            '__eq__': {
                '((self:bytearray /\ __value:top) -> (return:bool))',
            },
            '__ne__': {
                '((self:bytearray /\ __value:top) -> (return:bool))',
            },
            '__lt__': {
                '((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
            },
            '__le__': {
                '((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
            },
            '__gt__': {
                '((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
            },
            '__ge__': {
                '((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
            },
            '__alloc__': {
                '((self:bytearray) -> (return:int))',
            },
            '__buffer__': {
                '((self:bytearray /\ __flags:int) -> (return:memoryview))',
            },
            '__release_buffer__': {
                '((self:bytearray /\ __buffer:memoryview) -> (return:NoneType))',
            },
        }
    },
    'memoryview': {
        'attributes': {},
        'methods': {
            'format': {
                '((self:memoryview < int >) -> (return:str))',
            },
            'itemsize': {
                '((self:memoryview < int >) -> (return:int))',
            },
            'shape': {
                '((self:memoryview < int >) -> (return:tuple < int > + NoneType))',
            },
            'strides': {
                '((self:memoryview < int >) -> (return:tuple < int > + NoneType))',
            },
            'suboffsets': {
                '((self:memoryview < int >) -> (return:tuple < int > + NoneType))',
            },
            'readonly': {
                '((self:memoryview < int >) -> (return:bool))',
            },
            'ndim': {
                '((self:memoryview < int >) -> (return:int))',
            },
            'obj': {
                '((self:memoryview < int >) -> (return:bytearray + bytes + memoryview))',
            },
            'c_contiguous': {
                '((self:memoryview < int >) -> (return:bool))',
            },
            'f_contiguous': {
                '((self:memoryview < int >) -> (return:bool))',
            },
            'contiguous': {
                '((self:memoryview < int >) -> (return:bool))',
            },
            'nbytes': {
                '((self:memoryview < int >) -> (return:int))',
            },
            '__init__': {
                '((self:memoryview < int > /\ obj:bytearray + bytes + memoryview) -> (return:NoneType))',
            },
            '__enter__': {
                '((self:memoryview < int >) -> (return:memoryview < int >))',
            },
            'cast': {
                '((self:memoryview < int > /\ format:str /\ __d_shape:tuple < int > + list < int >) -> (return:memoryview))',
            },
            '__getitem__': {
                '((self:memoryview < int > /\ __key:SupportsIndex) -> (return:int))',
            },
            '__contains__': {
                '((self:memoryview < int > /\ __x:top) -> (return:bool))',
            },
            '__len__': {
                '((self:memoryview < int >) -> (return:int))',
            },
            '__eq__': {
                '((self:memoryview < int > /\ __value:top) -> (return:bool))',
            },
            '__hash__': {
                '((self:memoryview < int >) -> (return:int))',
            },
            '__setitem__': {
                '((self:memoryview < int > /\ __key:SupportsIndex /\ __value:SupportsIndex) -> (return:NoneType))',
            },
            'tolist': {
                '((self:memoryview < int >) -> (return:list < int >))',
            },
            'release': {
                '((self:memoryview < int >) -> (return:NoneType))',
            },
            '__buffer__': {
                '((self:memoryview < int > /\ __flags:int) -> (return:memoryview))',
            },
            '__release_buffer__': {
                '((self:memoryview < int > /\ __buffer:memoryview) -> (return:NoneType))',
            },
        }
    },
    'bool': {
        'attributes': {},
        'methods': {
            '__and__': {
                '((self:bool /\ __value:int) -> (return:int))',
                '((self:bool /\ __value:bool) -> (return:bool))',
            },
            '__or__': {
                '((self:bool /\ __value:int) -> (return:int))',
                '((self:bool /\ __value:bool) -> (return:bool))',
            },
            '__xor__': {
                '((self:bool /\ __value:int) -> (return:int))',
                '((self:bool /\ __value:bool) -> (return:bool))',
            },
            '__rand__': {
                '((self:bool /\ __value:int) -> (return:int))',
                '((self:bool /\ __value:bool) -> (return:bool))',
            },
            '__ror__': {
                '((self:bool /\ __value:int) -> (return:int))',
                '((self:bool /\ __value:bool) -> (return:bool))',
            },
            '__rxor__': {
                '((self:bool /\ __value:int) -> (return:int))',
                '((self:bool /\ __value:bool) -> (return:bool))',
            },
            '__getnewargs__': {
                '((self:bool) -> (return:tuple < int >))',
            },
        }
    },
    'tuple': {
        'attributes': {},
        'methods': {
            '__len__': {
                '((self:tuple < T?3 >) -> (return:int))',
            },
            '__contains__': {
                '((self:tuple < T?3 > /\ __key:top) -> (return:bool))',
            },
            '__getitem__': {
                '((self:tuple < T?3 > /\ __key:SupportsIndex) -> (return:T?3))',
            },
            '__lt__': {
                '((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
            },
            '__le__': {
                '((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
            },
            '__gt__': {
                '((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
            },
            '__ge__': {
                '((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:bool))',
            },
            '__eq__': {
                '((self:tuple < T?3 > /\ __value:top) -> (return:bool))',
            },
            '__hash__': {
                '((self:tuple < T?3 >) -> (return:int))',
            },
            '__add__': {
                '((self:tuple < T?3 > /\ __value:tuple < T?3 >) -> (return:tuple < T?3 >))',
                '((self:tuple < T?3 > /\ __value:tuple < T?0 >) -> (return:tuple < T?0 + T?3 >))',
            },
            '__mul__': {
                '((self:tuple < T?3 > /\ __value:SupportsIndex) -> (return:tuple < T?3 >))',
            },
            '__rmul__': {
                '((self:tuple < T?3 > /\ __value:SupportsIndex) -> (return:tuple < T?3 >))',
            },
            'count': {
                '((self:tuple < T?3 > /\ __value:top) -> (return:int))',
            },
            'index': {
                '((self:tuple < T?3 > /\ __value:top /\ __d___start:SupportsIndex /\ __d___stop:SupportsIndex) -> (return:int))',
            },
        }
    },
    'function': {
        'attributes': {},
        'methods': {
            '__closure__': {
                '((self:tuple < T?3 >) -> (return:tuple < _Cell > + NoneType))',
            },
            '__globals__': {
                '((self:tuple < T?3 >) -> (return:dict < str, top >))',
            },
            '__get__': {
                '((self:tuple < T?3 > /\ __instance:top /\ __d___owner:NoneType) -> (return:top))',
            },
        }
    },
    'list': {
        'attributes': {},
        'methods': {
            '__init__': {
                '((self:list < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
                '((self:list < T?0 >) -> (return:NoneType))',
            },
            'copy': {
                '((self:list < T?0 >) -> (return:list < T?0 >))',
            },
            'append': {
                '((self:list < T?0 > /\ __object:T?0) -> (return:NoneType))',
            },
            'extend': {
                '((self:list < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
            },
            'pop': {
                '((self:list < T?0 > /\ __d___index:SupportsIndex) -> (return:T?0))',
            },
            'index': {
                '((self:list < T?0 > /\ __value:T?0 /\ __d___start:SupportsIndex /\ __d___stop:SupportsIndex) -> (return:int))',
            },
            'count': {
                '((self:list < T?0 > /\ __value:T?0) -> (return:int))',
            },
            'insert': {
                '((self:list < T?0 > /\ __index:SupportsIndex /\ __object:T?0) -> (return:NoneType))',
            },
            'remove': {
                '((self:list < T?0 > /\ __value:T?0) -> (return:NoneType))',
            },
            '__len__': {
                '((self:list < T?0 >) -> (return:int))',
            },
            '__getitem__': {
                '((self:list < T?0 > /\ __i:SupportsIndex) -> (return:T?0))',
            },
            '__setitem__': {
                '((self:list < T?0 > /\ __key:SupportsIndex /\ __value:T?0) -> (return:NoneType))',
            },
            '__delitem__': {
                '((self:list < T?0 > /\ __key:SupportsIndex) -> (return:NoneType))',
            },
            '__add__': {
                '((self:list < T?0 > /\ __value:list < T?4 >) -> (return:list < T?0 + T?4 >))',
                '((self:list < T?0 > /\ __value:list < T?0 >) -> (return:list < T?0 >))',
            },
            '__iadd__': {
                '((self:list < T?0 > /\ __value:Iterable < T?0 >) -> (return:list < T?0 >))',
            },
            '__mul__': {
                '((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
            },
            '__rmul__': {
                '((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
            },
            '__imul__': {
                '((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
            },
            '__contains__': {
                '((self:list < T?0 > /\ __key:top) -> (return:bool))',
            },
            '__gt__': {
                '((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
            },
            '__ge__': {
                '((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
            },
            '__lt__': {
                '((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
            },
            '__le__': {
                '((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
            },
            '__eq__': {
                '((self:list < T?0 > /\ __value:top) -> (return:bool))',
            },
        }
    },
    'dict': {
        'attributes': {},
        'methods': {
            '__init__': {
                '((self:dict < str, T?2 > /\ __map:dict < str, T?2 > /\ __kw_kwargs:T?2) -> (return:NoneType))',
                '((self:dict < T?1, T?2 > /\ __map:dict < T?1, T?2 >) -> (return:NoneType))',
                '((self:dict < T?1, T?2 >) -> (return:NoneType))',
                '((self:dict < str, T?2 > /\ __kw_kwargs:T?2) -> (return:NoneType))',
            },
            'copy': {
                '((self:dict < T?1, T?2 >) -> (return:dict < T?1, T?2 >))',
            },
            'get': {
                '((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?2) -> (return:T?2))',
                '((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?0) -> (return:T?0 + T?2))',
                '((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:NoneType + T?2))',
            },
            'pop': {
                '((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:T?2))',
                '((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?0) -> (return:T?0 + T?2))',
                '((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?2) -> (return:T?2))',
            },
            '__len__': {
                '((self:dict < T?1, T?2 >) -> (return:int))',
            },
            '__getitem__': {
                '((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:T?2))',
            },
            '__setitem__': {
                '((self:dict < T?1, T?2 > /\ __key:T?1 /\ __value:T?2) -> (return:NoneType))',
            },
            '__delitem__': {
                '((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:NoneType))',
            },
            '__eq__': {
                '((self:dict < T?1, T?2 > /\ __value:top) -> (return:bool))',
            },
        }
    },
    'set': {
        'attributes': {},
        'methods': {
            '__init__': {
                '((self:set < T?0 >) -> (return:NoneType))',
                '((self:set < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
            },
            'add': {
                '((self:set < T?0 > /\ __element:T?0) -> (return:NoneType))',
            },
            'copy': {
                '((self:set < T?0 >) -> (return:set < T?0 >))',
            },
            'difference': {
                '((self:set < T?0 > /\ __va_s:Iterable < top >) -> (return:set < T?0 >))',
            },
            'difference_update': {
                '((self:set < T?0 > /\ __va_s:Iterable < top >) -> (return:NoneType))',
            },
            'discard': {
                '((self:set < T?0 > /\ __element:T?0) -> (return:NoneType))',
            },
            'intersection': {
                '((self:set < T?0 > /\ __va_s:Iterable < top >) -> (return:set < T?0 >))',
            },
            'intersection_update': {
                '((self:set < T?0 > /\ __va_s:Iterable < top >) -> (return:NoneType))',
            },
            'isdisjoint': {
                '((self:set < T?0 > /\ __s:Iterable < top >) -> (return:bool))',
            },
            'issubset': {
                '((self:set < T?0 > /\ __s:Iterable < top >) -> (return:bool))',
            },
            'issuperset': {
                '((self:set < T?0 > /\ __s:Iterable < top >) -> (return:bool))',
            },
            'remove': {
                '((self:set < T?0 > /\ __element:T?0) -> (return:NoneType))',
            },
            'symmetric_difference': {
                '((self:set < T?0 > /\ __s:Iterable < T?0 >) -> (return:set < T?0 >))',
            },
            'symmetric_difference_update': {
                '((self:set < T?0 > /\ __s:Iterable < T?0 >) -> (return:NoneType))',
            },
            'union': {
                '((self:set < T?0 > /\ __va_s:Iterable < T?4 >) -> (return:set < T?0 + T?4 >))',
            },
            'update': {
                '((self:set < T?0 > /\ __va_s:Iterable < T?0 >) -> (return:NoneType))',
            },
            '__len__': {
                '((self:set < T?0 >) -> (return:int))',
            },
            '__contains__': {
                '((self:set < T?0 > /\ __o:top) -> (return:bool))',
            },
            '__and__': {
                '((self:set < T?0 > /\ __value:set < top >) -> (return:set < T?0 >))',
            },
            '__iand__': {
                '((self:set < T?0 > /\ __value:set < top >) -> (return:set < T?0 >))',
            },
            '__or__': {
                '((self:set < T?0 > /\ __value:set < T?4 >) -> (return:set < T?0 + T?4 >))',
            },
            '__ior__': {
                '((self:set < T?0 > /\ __value:set < T?0 >) -> (return:set < T?0 >))',
            },
            '__sub__': {
                '((self:set < T?0 > /\ __value:set < T?0 + NoneType >) -> (return:set < T?0 >))',
            },
            '__isub__': {
                '((self:set < T?0 > /\ __value:set < top >) -> (return:set < T?0 >))',
            },
            '__xor__': {
                '((self:set < T?0 > /\ __value:set < T?4 >) -> (return:set < T?0 + T?4 >))',
            },
            '__ixor__': {
                '((self:set < T?0 > /\ __value:set < T?0 >) -> (return:set < T?0 >))',
            },
            '__le__': {
                '((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
            },
            '__lt__': {
                '((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
            },
            '__ge__': {
                '((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
            },
            '__gt__': {
                '((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
            },
            '__eq__': {
                '((self:set < T?0 > /\ __value:top) -> (return:bool))',
            },
        }
    },
    'frozenset': {
        'attributes': {},
        'methods': {
            'copy': {
                '((self:frozenset < T?3 >) -> (return:frozenset < T?3 >))',
            },
            'difference': {
                '((self:frozenset < T?3 > /\ __va_s:Iterable < top >) -> (return:frozenset < T?3 >))',
            },
            'intersection': {
                '((self:frozenset < T?3 > /\ __va_s:Iterable < top >) -> (return:frozenset < T?3 >))',
            },
            'isdisjoint': {
                '((self:frozenset < T?3 > /\ __s:Iterable < T?3 >) -> (return:bool))',
            },
            'issubset': {
                '((self:frozenset < T?3 > /\ __s:Iterable < top >) -> (return:bool))',
            },
            'issuperset': {
                '((self:frozenset < T?3 > /\ __s:Iterable < top >) -> (return:bool))',
            },
            'symmetric_difference': {
                '((self:frozenset < T?3 > /\ __s:Iterable < T?3 >) -> (return:frozenset < T?3 >))',
            },
            'union': {
                '((self:frozenset < T?3 > /\ __va_s:Iterable < T?4 >) -> (return:frozenset < T?4 + T?3 >))',
            },
            '__len__': {
                '((self:frozenset < T?3 >) -> (return:int))',
            },
            '__contains__': {
                '((self:frozenset < T?3 > /\ __o:top) -> (return:bool))',
            },
            '__and__': {
                '((self:frozenset < T?3 > /\ __value:set < T?3 >) -> (return:frozenset < T?3 >))',
            },
            '__or__': {
                '((self:frozenset < T?3 > /\ __value:set < T?4 >) -> (return:frozenset < T?4 + T?3 >))',
            },
            '__sub__': {
                '((self:frozenset < T?3 > /\ __value:set < T?3 >) -> (return:frozenset < T?3 >))',
            },
            '__xor__': {
                '((self:frozenset < T?3 > /\ __value:set < T?4 >) -> (return:frozenset < T?4 + T?3 >))',
            },
            '__le__': {
                '((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
            },
            '__lt__': {
                '((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
            },
            '__ge__': {
                '((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
            },
            '__gt__': {
                '((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
            },
            '__eq__': {
                '((self:frozenset < T?3 > /\ __value:top) -> (return:bool))',
            },
            '__hash__': {
                '((self:frozenset < T?3 >) -> (return:int))',
            },
        }
    },
    'enumerate': {
        'attributes': {},
        'methods': {
            '__init__': {
                '((self:frozenset < T?3 > /\ iterable:Iterable < T?0 > /\ __d_start:int) -> (return:NoneType))',
            },
            '__iter__': {
                '((self:frozenset < T?3 >) -> (return:frozenset < T?3 >))',
            },
            '__next__': {
                '((self:frozenset < T?3 >) -> (return:tuple < T?0 + int >))',
            },
        }
    },
    'range': {
        'attributes': {},
        'methods': {
            'start': {
                '((self:range < int >) -> (return:int))',
            },
            'stop': {
                '((self:range < int >) -> (return:int))',
            },
            'step': {
                '((self:range < int >) -> (return:int))',
            },
            '__init__': {
                '((self:range < int > /\ __start:SupportsIndex /\ __stop:SupportsIndex /\ __d___step:SupportsIndex) -> (return:NoneType))',
                '((self:range < int > /\ __stop:SupportsIndex) -> (return:NoneType))',
            },
            'count': {
                '((self:range < int > /\ __value:int) -> (return:int))',
            },
            'index': {
                '((self:range < int > /\ __value:int) -> (return:int))',
            },
            '__len__': {
                '((self:range < int >) -> (return:int))',
            },
            '__eq__': {
                '((self:range < int > /\ __value:top) -> (return:bool))',
            },
            '__hash__': {
                '((self:range < int >) -> (return:int))',
            },
            '__contains__': {
                '((self:range < int > /\ __key:top) -> (return:bool))',
            },
            '__getitem__': {
                '((self:range < int > /\ __key:SupportsIndex) -> (return:int))',
            },
        }
    },

}
