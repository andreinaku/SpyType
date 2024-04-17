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
        r'((self:dict< T?1, T?2 > /\ __map:dict< T?1, T?2 >) -> (return:NoneType))',
        r'((self:top) -> (return:NoneType))',
        r'((self:dict< str, T?2 > /\ __kw_kwargs:T?2) -> (return:NoneType))',
        r'((self:dict< T?1, T?2 >) -> (return:NoneType))',
        r'((self:list< T?0 > /\ __iterable:Iterable< T?0 >) -> (return:NoneType))',
        r'((self:list< T?0 >) -> (return:NoneType))',
        r'((self:bytearray /\ __string:str /\ encoding:str /\ errors:str) -> (return:NoneType))',
        r'((self:dict< str, T?2 > /\ __map:dict< str, T?2 > /\ __kw_kwargs:T?2) -> (return:NoneType))',
        r'((self:set< T?0 >) -> (return:NoneType))',
        r'((self:set< T?0 > /\ __iterable:Iterable< T?0 >) -> (return:NoneType))',
        r'((self:range< int > /\ __start:bool + int /\ __stop:bool + int /\ __step:bool + int) -> (return:NoneType))',
        r'((self:memoryview< int > /\ obj:bytearray + bytes + memoryview) -> (return:NoneType))',
        r'((self:bytearray) -> (return:NoneType))',
        r'((self:frozenset< T?3 > /\ iterable:Iterable< T?0 > /\ start:int) -> (return:NoneType))',
        r'((self:bytearray /\ __ints:bool + memoryview + bytes + bytearray + int + Iterable< bool + int >) -> (return:NoneType))',
        r'((self:range< int > /\ __stop:bool + int) -> (return:NoneType))',
    },
    '__setattr__': {
        r'((self:top /\ __name:str /\ __value:top) -> (return:NoneType))',
    },
    '__delattr__': {
        r'((self:top /\ __name:str) -> (return:NoneType))',
    },
    '__eq__': {
        r'((self:range< int > /\ __value:top) -> (return:bool))',
        r'((self:bytearray /\ __value:top) -> (return:bool))',
        r'((self:float /\ __value:top) -> (return:bool))',
        r'((self:complex /\ __value:top) -> (return:bool))',
        r'((self:tuple< T?3 > /\ __value:top) -> (return:bool))',
        r'((self:int /\ __value:top) -> (return:bool))',
        r'((self:frozenset< T?3 > /\ __value:top) -> (return:bool))',
        r'((self:bytes /\ __value:top) -> (return:bool))',
        r'((self:list< T?0 > /\ __value:top) -> (return:bool))',
        r'((self:set< T?0 > /\ __value:top) -> (return:bool))',
        r'((self:top /\ __value:top) -> (return:bool))',
        r'((self:memoryview< int > /\ __value:top) -> (return:bool))',
        r'((self:str /\ __value:top) -> (return:bool))',
        r'((self:dict< T?1, T?2 > /\ __value:top) -> (return:bool))',
    },
    '__ne__': {
        r'((self:bytearray /\ __value:top) -> (return:bool))',
        r'((self:float /\ __value:top) -> (return:bool))',
        r'((self:complex /\ __value:top) -> (return:bool))',
        r'((self:int /\ __value:top) -> (return:bool))',
        r'((self:bytes /\ __value:top) -> (return:bool))',
        r'((self:top /\ __value:top) -> (return:bool))',
        r'((self:str /\ __value:top) -> (return:bool))',
    },
    '__str__': {
        r'((self:top) -> (return:str))',
    },
    '__repr__': {
        r'((self:top) -> (return:str))',
    },
    '__hash__': {
        r'((self:complex) -> (return:int))',
        r'((self:top) -> (return:int))',
        r'((self:str) -> (return:int))',
        r'((self:range< int >) -> (return:int))',
        r'((self:frozenset< T?3 >) -> (return:int))',
        r'((self:bytes) -> (return:int))',
        r'((self:int) -> (return:int))',
        r'((self:tuple< T?3 >) -> (return:int))',
        r'((self:memoryview< int >) -> (return:int))',
        r'((self:float) -> (return:int))',
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
        r'((self:top) -> (return:tuple< top > + str))',
    },
    '__dir__': {
        r'((self:top) -> (return:Iterable< str >))',
    },
    'real': {
        r'((self:complex) -> (return:float))',
        r'((self:float) -> (return:float))',
        r'((self:int) -> (return:int))',
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
        r'((self:list< T?0 > /\ __value:list< T?4 >) -> (return:list< T?0 + T?4 >))',
        r'((self:str /\ __value:str) -> (return:str))',
        r'((self:list< T?0 > /\ __value:list< T?0 >) -> (return:list< T?0 >))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:tuple< T?3 > /\ __value:tuple< T?0 >) -> (return:tuple< T?0 + T?3 >))',
        r'((self:bytes /\ __value:bytearray + bytes + memoryview) -> (return:bytes))',
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bytearray))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:tuple< T?3 > /\ __value:tuple< T?3 >) -> (return:tuple< T?3 >))',
    },
    '__sub__': {
        r'((self:set< T?0 > /\ __value:set< T?0 + NoneType >) -> (return:set< T?0 >))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:frozenset< T?3 > /\ __value:set< T?3 >) -> (return:frozenset< T?3 >))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__mul__': {
        r'((self:str /\ __value:bool + int) -> (return:str))',
        r'((self:tuple< T?3 > /\ __value:bool + int) -> (return:tuple< T?3 >))',
        r'((self:bytes /\ __value:bool + int) -> (return:bytes))',
        r'((self:list< T?0 > /\ __value:bool + int) -> (return:list< T?0 >))',
        r'((self:bytearray /\ __value:bool + int) -> (return:bytearray))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__floordiv__': {
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__truediv__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:float))',
    },
    '__mod__': {
        r'((self:bytes /\ __value:top) -> (return:bytes))',
        r'((self:str /\ __value:tuple< str > + str) -> (return:str))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:bytearray /\ __value:top) -> (return:bytes))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:str /\ __value:top) -> (return:str))',
    },
    '__divmod__': {
        r'((self:int /\ __value:int) -> (return:tuple< int >))',
        r'((self:float /\ __value:float) -> (return:tuple< float >))',
    },
    '__radd__': {
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rsub__': {
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rmul__': {
        r'((self:str /\ __value:bool + int) -> (return:str))',
        r'((self:tuple< T?3 > /\ __value:bool + int) -> (return:tuple< T?3 >))',
        r'((self:bytes /\ __value:bool + int) -> (return:bytes))',
        r'((self:list< T?0 > /\ __value:bool + int) -> (return:list< T?0 >))',
        r'((self:bytearray /\ __value:bool + int) -> (return:bytearray))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rfloordiv__': {
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rtruediv__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:float))',
    },
    '__rmod__': {
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rdivmod__': {
        r'((self:int /\ __value:int) -> (return:tuple< int >))',
        r'((self:float /\ __value:float) -> (return:tuple< float >))',
    },
    '__pow__': {
        r'((self:float /\ __value:int /\ __mod:NoneType) -> (return:float))',
        r'((self:int /\ __value:int /\ __mod:NoneType) -> (return:float))',
        r'((self:int /\ __value:int /\ __mod:int) -> (return:int))',
        r'((self:int /\ __value:int /\ __mod:NoneType) -> (return:top))',
        r'((self:complex /\ __value:complex /\ __mod:NoneType) -> (return:complex))',
        r'((self:int /\ __value:int /\ __mod:NoneType) -> (return:int))',
        r'((self:float /\ __value:float /\ __mod:NoneType) -> (return:top))',
    },
    '__rpow__': {
        r'((self:float /\ __value:int /\ __mod:NoneType) -> (return:float))',
        r'((self:complex /\ __value:complex /\ __mod:NoneType) -> (return:complex))',
        r'((self:int /\ __value:int /\ __mod:NoneType + int) -> (return:top))',
        r'((self:float /\ __value:int /\ __mod:NoneType) -> (return:complex))',
        r'((self:float /\ __value:float /\ __mod:NoneType) -> (return:top))',
    },
    '__and__': {
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:set< T?0 > /\ __value:set< top >) -> (return:set< T?0 >))',
        r'((self:frozenset< T?3 > /\ __value:set< T?3 >) -> (return:frozenset< T?3 >))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__or__': {
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:frozenset< T?3 > /\ __value:set< T?4 >) -> (return:frozenset< T?4 + T?3 >))',
        r'((self:set< T?0 > /\ __value:set< T?4 >) -> (return:set< T?0 + T?4 >))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__xor__': {
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:frozenset< T?3 > /\ __value:set< T?4 >) -> (return:frozenset< T?4 + T?3 >))',
        r'((self:set< T?0 > /\ __value:set< T?4 >) -> (return:set< T?0 + T?4 >))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__lshift__': {
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rshift__': {
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rand__': {
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__ror__': {
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rxor__': {
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:int /\ __value:int) -> (return:int))',
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
        r'((self:int /\ __ndigits:bool + int) -> (return:int))',
        r'((self:float /\ __ndigits:bool + int) -> (return:float))',
        r'((self:float /\ __ndigits:NoneType) -> (return:int))',
    },
    '__getnewargs__': {
        r'((self:bytes) -> (return:tuple< bytes >))',
        r'((self:int) -> (return:tuple< int >))',
        r'((self:bool) -> (return:tuple< int >))',
        r'((self:float) -> (return:tuple< float >))',
        r'((self:str) -> (return:tuple< str >))',
    },
    '__lt__': {
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:set< T?0 > /\ __value:set< top >) -> (return:bool))',
        r'((self:tuple< T?3 > /\ __value:tuple< T?3 >) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:list< T?0 > /\ __value:list< T?0 >) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:frozenset< T?3 > /\ __value:set< top >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
    },
    '__le__': {
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:set< T?0 > /\ __value:set< top >) -> (return:bool))',
        r'((self:tuple< T?3 > /\ __value:tuple< T?3 >) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:list< T?0 > /\ __value:list< T?0 >) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:frozenset< T?3 > /\ __value:set< top >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
    },
    '__gt__': {
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:set< T?0 > /\ __value:set< top >) -> (return:bool))',
        r'((self:tuple< T?3 > /\ __value:tuple< T?3 >) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:list< T?0 > /\ __value:list< T?0 >) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:frozenset< T?3 > /\ __value:set< top >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bool))',
    },
    '__ge__': {
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:set< T?0 > /\ __value:set< top >) -> (return:bool))',
        r'((self:tuple< T?3 > /\ __value:tuple< T?3 >) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:list< T?0 > /\ __value:list< T?0 >) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:frozenset< T?3 > /\ __value:set< top >) -> (return:bool))',
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
        r'((self:complex) -> (return:float))',
        r'((self:float) -> (return:float))',
        r'((self:int) -> (return:int))',
    },
    '__bool__': {
        r'((self:complex) -> (return:bool))',
        r'((self:float) -> (return:bool))',
        r'((self:int) -> (return:bool))',
    },
    '__index__': {
        r'((self:int) -> (return:int))',
    },
    'as_integer_ratio': {
        r'((self:float) -> (return:tuple< int >))',
    },
    'hex': {
        r'((self:float) -> (return:str))',
        r'((__number:bool + int) -> (return:str))',
    },
    'is_integer': {
        r'((self:float) -> (return:bool))',
    },
    'imag': {
        r'((self:complex) -> (return:float))',
        r'((self:float) -> (return:float))',
    },
    'capitalize': {
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:str) -> (return:str))',
        r'((self:bytes) -> (return:bytes))',
    },
    'casefold': {
        r'((self:str) -> (return:str))',
    },
    'center': {
        r'((self:str /\ __width:bool + int /\ __fillchar:str) -> (return:str))',
        r'((self:bytearray /\ __width:bool + int /\ __fillchar:bytes) -> (return:bytearray))',
        r'((self:bytes /\ __width:bool + int /\ __fillchar:bytes) -> (return:bytes))',
    },
    'count': {
        r'((self:str /\ x:str /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
        r'((self:bytes /\ __sub:bool + memoryview + bytes + bytearray + int /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
        r'((self:list< T?0 > /\ __value:T?0) -> (return:int))',
        r'((self:range< int > /\ __value:int) -> (return:int))',
        r'((self:tuple< T?3 > /\ __value:top) -> (return:int))',
        r'((self:bytearray /\ __sub:bool + memoryview + bytes + bytearray + int /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
    },
    'encode': {
        r'((self:str /\ encoding:str /\ errors:str) -> (return:bytes))',
    },
    'endswith': {
        r'((self:bytes /\ __suffix:bytearray + bytes + memoryview + tuple< bytearray + bytes + memoryview > /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:bool))',
        r'((self:bytearray /\ __suffix:bytearray + bytes + memoryview + tuple< bytearray + bytes + memoryview > /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:bool))',
        r'((self:str /\ __suffix:tuple< str > + str /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:bool))',
    },
    'find': {
        r'((self:str /\ __sub:str /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
        r'((self:bytes /\ __sub:bool + memoryview + bytes + bytearray + int /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
        r'((self:bytearray /\ __sub:bool + memoryview + bytes + bytearray + int /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
    },
    'format': {
        r'((self:str /\ __va_args:str /\ __kw_kwargs:str) -> (return:str))',
        r'((self:str /\ __va_args:top /\ __kw_kwargs:top) -> (return:str))',
        r'((__value:top /\ __format_spec:str) -> (return:str))',
        r'((self:memoryview< int >) -> (return:str))',
    },
    'format_map': {
        r'((self:str /\ map:dict< str, int >) -> (return:str))',
    },
    'index': {
        r'((self:bytes /\ __sub:bool + memoryview + bytes + bytearray + int /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
        r'((self:range< int > /\ __value:int) -> (return:int))',
        r'((self:str /\ __sub:str /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
        r'((self:list< T?0 > /\ __value:T?0 /\ __start:bool + int /\ __stop:bool + int) -> (return:int))',
        r'((self:bytearray /\ __sub:bool + memoryview + bytes + bytearray + int /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
        r'((self:tuple< T?3 > /\ __value:top /\ __start:bool + int /\ __stop:bool + int) -> (return:int))',
    },
    'isalnum': {
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
    },
    'isalpha': {
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
    },
    'isascii': {
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
    },
    'isdecimal': {
        r'((self:str) -> (return:bool))',
    },
    'isdigit': {
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
    },
    'isidentifier': {
        r'((self:str) -> (return:bool))',
    },
    'islower': {
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
    },
    'isnumeric': {
        r'((self:str) -> (return:bool))',
    },
    'isprintable': {
        r'((self:str) -> (return:bool))',
    },
    'isspace': {
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
    },
    'istitle': {
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
    },
    'isupper': {
        r'((self:str) -> (return:bool))',
        r'((self:bytes) -> (return:bool))',
        r'((self:bytearray) -> (return:bool))',
    },
    'join': {
        r'((self:bytearray /\ __iterable_of_bytes:Iterable< bytearray + bytes + memoryview >) -> (return:bytearray))',
        r'((self:bytes /\ __iterable_of_bytes:Iterable< bytearray + bytes + memoryview >) -> (return:bytes))',
        r'((self:str /\ __iterable:Iterable< str >) -> (return:str))',
    },
    'ljust': {
        r'((self:str /\ __width:bool + int /\ __fillchar:str) -> (return:str))',
        r'((self:bytearray /\ __width:bool + int /\ __fillchar:bytearray + bytes) -> (return:bytearray))',
        r'((self:bytes /\ __width:bool + int /\ __fillchar:bytearray + bytes) -> (return:bytes))',
    },
    'lower': {
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:str) -> (return:str))',
        r'((self:bytes) -> (return:bytes))',
    },
    'lstrip': {
        r'((self:str /\ __chars:str + NoneType) -> (return:str))',
        r'((self:bytes /\ __bytes:bytearray + bytes + NoneType + memoryview) -> (return:bytes))',
        r'((self:bytearray /\ __bytes:bytearray + bytes + NoneType + memoryview) -> (return:bytearray))',
    },
    'partition': {
        r'((self:bytearray /\ __sep:bytearray + bytes + memoryview) -> (return:tuple< bytearray >))',
        r'((self:bytes /\ __sep:bytearray + bytes + memoryview) -> (return:tuple< bytes >))',
        r'((self:str /\ __sep:str) -> (return:tuple< str >))',
    },
    'replace': {
        r'((self:bytearray /\ __old:bytearray + bytes + memoryview /\ __new:bytearray + bytes + memoryview /\ __count:bool + int) -> (return:bytearray))',
        r'((self:str /\ __old:str /\ __new:str /\ __count:bool + int) -> (return:str))',
        r'((self:bytes /\ __old:bytearray + bytes + memoryview /\ __new:bytearray + bytes + memoryview /\ __count:bool + int) -> (return:bytes))',
    },
    'rfind': {
        r'((self:str /\ __sub:str /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
        r'((self:bytes /\ __sub:bool + memoryview + bytes + bytearray + int /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
        r'((self:bytearray /\ __sub:bool + memoryview + bytes + bytearray + int /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
    },
    'rindex': {
        r'((self:str /\ __sub:str /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
        r'((self:bytes /\ __sub:bool + memoryview + bytes + bytearray + int /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
        r'((self:bytearray /\ __sub:bool + memoryview + bytes + bytearray + int /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:int))',
    },
    'rjust': {
        r'((self:str /\ __width:bool + int /\ __fillchar:str) -> (return:str))',
        r'((self:bytearray /\ __width:bool + int /\ __fillchar:bytearray + bytes) -> (return:bytearray))',
        r'((self:bytes /\ __width:bool + int /\ __fillchar:bytearray + bytes) -> (return:bytes))',
    },
    'rpartition': {
        r'((self:bytearray /\ __sep:bytearray + bytes + memoryview) -> (return:tuple< bytearray >))',
        r'((self:bytes /\ __sep:bytearray + bytes + memoryview) -> (return:tuple< bytes >))',
        r'((self:str /\ __sep:str) -> (return:tuple< str >))',
    },
    'rsplit': {
        r'((self:str /\ sep:str + NoneType /\ maxsplit:bool + int) -> (return:list< str >))',
        r'((self:bytes /\ sep:bytearray + bytes + NoneType + memoryview /\ maxsplit:bool + int) -> (return:list< bytes >))',
        r'((self:bytearray /\ sep:bytearray + bytes + NoneType + memoryview /\ maxsplit:bool + int) -> (return:list< bytearray >))',
    },
    'rstrip': {
        r'((self:str /\ __chars:str + NoneType) -> (return:str))',
        r'((self:bytes /\ __bytes:bytearray + bytes + NoneType + memoryview) -> (return:bytes))',
        r'((self:bytearray /\ __bytes:bytearray + bytes + NoneType + memoryview) -> (return:bytearray))',
    },
    'split': {
        r'((self:str /\ sep:str + NoneType /\ maxsplit:bool + int) -> (return:list< str >))',
        r'((self:bytes /\ sep:bytearray + bytes + NoneType + memoryview /\ maxsplit:bool + int) -> (return:list< bytes >))',
        r'((self:bytearray /\ sep:bytearray + bytes + NoneType + memoryview /\ maxsplit:bool + int) -> (return:list< bytearray >))',
    },
    'splitlines': {
        r'((self:bytes /\ keepends:bool) -> (return:list< bytes >))',
        r'((self:bytearray /\ keepends:bool) -> (return:list< bytearray >))',
        r'((self:str /\ keepends:bool) -> (return:list< str >))',
    },
    'startswith': {
        r'((self:bytearray /\ __prefix:bytearray + bytes + memoryview + tuple< bytearray + bytes + memoryview > /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:bool))',
        r'((self:bytes /\ __prefix:bytearray + bytes + memoryview + tuple< bytearray + bytes + memoryview > /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:bool))',
        r'((self:str /\ __prefix:tuple< str > + str /\ __start:bool + NoneType + int /\ __end:bool + NoneType + int) -> (return:bool))',
    },
    'strip': {
        r'((self:str /\ __chars:str + NoneType) -> (return:str))',
        r'((self:bytes /\ __bytes:bytearray + bytes + NoneType + memoryview) -> (return:bytes))',
        r'((self:bytearray /\ __bytes:bytearray + bytes + NoneType + memoryview) -> (return:bytearray))',
    },
    'swapcase': {
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:str) -> (return:str))',
        r'((self:bytes) -> (return:bytes))',
    },
    'title': {
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:str) -> (return:str))',
        r'((self:bytes) -> (return:bytes))',
    },
    'translate': {
        r'((self:bytearray /\ __table:bytearray + bytes + NoneType + memoryview /\ delete:bytes) -> (return:bytearray))',
        r'((self:bytes /\ __table:bytearray + bytes + NoneType + memoryview /\ delete:bytes) -> (return:bytes))',
        r'((self:str /\ __table:dict< int, str + int >) -> (return:str))',
    },
    'upper': {
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:str) -> (return:str))',
        r'((self:bytes) -> (return:bytes))',
    },
    'zfill': {
        r'((self:str /\ __width:bool + int) -> (return:str))',
        r'((self:bytes /\ __width:bool + int) -> (return:bytes))',
        r'((self:bytearray /\ __width:bool + int) -> (return:bytearray))',
    },
    'maketrans': {
        r'((__x:str /\ __y:str) -> (return:dict< int, int >))',
        r'((__frm:bytearray + bytes + memoryview /\ __to:bytearray + bytes + memoryview) -> (return:bytes))',
        r'((__x:str /\ __y:str /\ __z:str) -> (return:dict< int, NoneType + int >))',
        r'((__x:dict< int, T?0 > + dict< str + int, T?0 > + dict< str, T?0 >) -> (return:dict< int, T?0 >))',
    },
    '__contains__': {
        r'((self:range< int > /\ __key:top) -> (return:bool))',
        r'((self:tuple< T?3 > /\ __key:top) -> (return:bool))',
        r'((self:set< T?0 > /\ __o:top) -> (return:bool))',
        r'((self:frozenset< T?3 > /\ __o:top) -> (return:bool))',
        r'((self:list< T?0 > /\ __key:top) -> (return:bool))',
        r'((self:bytearray /\ __key:bool + memoryview + bytes + bytearray + int) -> (return:bool))',
        r'((self:memoryview< int > /\ __x:top) -> (return:bool))',
        r'((self:bytes /\ __key:bool + memoryview + bytes + bytearray + int) -> (return:bool))',
        r'((self:str /\ __key:str) -> (return:bool))',
    },
    '__getitem__': {
        r'((self:memoryview< int > /\ __key:bool + int) -> (return:int))',
        r'((self:dict< T?1, T?2 > /\ __key:T?1) -> (return:T?2))',
        r'((self:range< int > /\ __key:bool + int) -> (return:int))',
        r'((self:tuple< T?3 > /\ __key:bool + int) -> (return:T?3))',
        r'((self:bytes /\ __key:bool + int) -> (return:int))',
        r'((self:str /\ __key:bool + int) -> (return:str))',
        r'((self:bytearray /\ __key:bool + int) -> (return:int))',
        r'((self:list< T?0 > /\ __i:bool + int) -> (return:T?0))',
    },
    '__len__': {
        r'((self:dict< T?1, T?2 >) -> (return:int))',
        r'((self:bytearray) -> (return:int))',
        r'((self:set< T?0 >) -> (return:int))',
        r'((self:str) -> (return:int))',
        r'((self:range< int >) -> (return:int))',
        r'((self:frozenset< T?3 >) -> (return:int))',
        r'((self:bytes) -> (return:int))',
        r'((self:tuple< T?3 >) -> (return:int))',
        r'((self:memoryview< int >) -> (return:int))',
        r'((self:list< T?0 >) -> (return:int))',
    },
    'decode': {
        r'((self:bytearray /\ encoding:str /\ errors:str) -> (return:str))',
        r'((self:bytes /\ encoding:str /\ errors:str) -> (return:str))',
    },
    '__buffer__': {
        r'((self:bytearray /\ __flags:int) -> (return:memoryview))',
        r'((self:memoryview< int > /\ __flags:int) -> (return:memoryview))',
        r'((self:bytes /\ __flags:int) -> (return:memoryview))',
    },
    'append': {
        r'((self:bytearray /\ __item:bool + int) -> (return:NoneType))',
        r'((self:list< T?0 > /\ __object:T?0) -> (return:NoneType))',
    },
    'copy': {
        r'((self:frozenset< T?3 >) -> (return:frozenset< T?3 >))',
        r'((self:dict< T?1, T?2 >) -> (return:dict< T?1, T?2 >))',
        r'((self:set< T?0 >) -> (return:set< T?0 >))',
        r'((self:list< T?0 >) -> (return:list< T?0 >))',
        r'((self:bytearray) -> (return:bytearray))',
    },
    'extend': {
        r'((self:list< T?0 > /\ __iterable:Iterable< T?0 >) -> (return:NoneType))',
        r'((self:bytearray /\ __iterable_of_ints:Iterable< bool + int >) -> (return:NoneType))',
    },
    'insert': {
        r'((self:list< T?0 > /\ __index:bool + int /\ __object:T?0) -> (return:NoneType))',
        r'((self:bytearray /\ __index:bool + int /\ __item:bool + int) -> (return:NoneType))',
    },
    'pop': {
        r'((self:dict< T?1, T?2 > /\ __key:T?1 /\ __default:T?2) -> (return:T?2))',
        r'((self:bytearray /\ __index:int) -> (return:int))',
        r'((self:dict< T?1, T?2 > /\ __key:T?1) -> (return:T?2))',
        r'((self:list< T?0 > /\ __index:bool + int) -> (return:T?0))',
        r'((self:dict< T?1, T?2 > /\ __key:T?1 /\ __default:T?0) -> (return:T?0 + T?2))',
    },
    'remove': {
        r'((self:bytearray /\ __value:int) -> (return:NoneType))',
        r'((self:set< T?0 > /\ __element:T?0) -> (return:NoneType))',
        r'((self:list< T?0 > /\ __value:T?0) -> (return:NoneType))',
    },
    '__setitem__': {
        r'((self:dict< T?1, T?2 > /\ __key:T?1 /\ __value:T?2) -> (return:NoneType))',
        r'((self:list< T?0 > /\ __key:bool + int /\ __value:T?0) -> (return:NoneType))',
        r'((self:memoryview< int > /\ __key:bool + int /\ __value:bool + int) -> (return:NoneType))',
        r'((self:bytearray /\ __key:bool + int /\ __value:bool + int) -> (return:NoneType))',
    },
    '__delitem__': {
        r'((self:list< T?0 > /\ __key:bool + int) -> (return:NoneType))',
        r'((self:dict< T?1, T?2 > /\ __key:T?1) -> (return:NoneType))',
        r'((self:bytearray /\ __key:bool + int) -> (return:NoneType))',
    },
    '__iadd__': {
        r'((self:bytearray /\ __value:bytearray + bytes + memoryview) -> (return:bytearray))',
        r'((self:list< T?0 > /\ __value:Iterable< T?0 >) -> (return:list< T?0 >))',
    },
    '__imul__': {
        r'((self:bytearray /\ __value:bool + int) -> (return:bytearray))',
        r'((self:list< T?0 > /\ __value:bool + int) -> (return:list< T?0 >))',
    },
    '__alloc__': {
        r'((self:bytearray) -> (return:int))',
    },
    '__release_buffer__': {
        r'((self:bytearray /\ __buffer:memoryview) -> (return:NoneType))',
        r'((self:memoryview< int > /\ __buffer:memoryview) -> (return:NoneType))',
    },
    'itemsize': {
        r'((self:memoryview< int >) -> (return:int))',
    },
    'shape': {
        r'((self:memoryview< int >) -> (return:tuple< int > + NoneType))',
    },
    'strides': {
        r'((self:memoryview< int >) -> (return:tuple< int > + NoneType))',
    },
    'suboffsets': {
        r'((self:memoryview< int >) -> (return:tuple< int > + NoneType))',
    },
    'readonly': {
        r'((self:memoryview< int >) -> (return:bool))',
    },
    'ndim': {
        r'((self:memoryview< int >) -> (return:int))',
    },
    'obj': {
        r'((self:memoryview< int >) -> (return:bytearray + bytes + memoryview))',
    },
    'c_contiguous': {
        r'((self:memoryview< int >) -> (return:bool))',
    },
    'f_contiguous': {
        r'((self:memoryview< int >) -> (return:bool))',
    },
    'contiguous': {
        r'((self:memoryview< int >) -> (return:bool))',
    },
    'nbytes': {
        r'((self:memoryview< int >) -> (return:int))',
    },
    '__enter__': {
        r'((self:memoryview< int >) -> (return:memoryview< int >))',
    },
    'cast': {
        r'((self:memoryview< int > /\ format:str /\ shape:tuple< int > + list< int >) -> (return:memoryview))',
    },
    'tolist': {
        r'((self:memoryview< int >) -> (return:list< int >))',
    },
    'release': {
        r'((self:memoryview< int >) -> (return:NoneType))',
    },
    '__closure__': {
        r'((self:tuple< T?3 >) -> (return:tuple< _Cell > + NoneType))',
    },
    '__globals__': {
        r'((self:tuple< T?3 >) -> (return:dict< str, top >))',
    },
    '__get__': {
        r'((self:tuple< T?3 > /\ __instance:top /\ __owner:NoneType) -> (return:top))',
    },
    'get': {
        r'((self:dict< T?1, T?2 > /\ __key:T?1 /\ __default:T?0) -> (return:T?0 + T?2))',
        r'((self:dict< T?1, T?2 > /\ __key:T?1 /\ __default:T?2) -> (return:T?2))',
        r'((self:dict< T?1, T?2 > /\ __key:T?1) -> (return:NoneType + T?2))',
    },
    'add': {
        r'((self:set< T?0 > /\ __element:T?0) -> (return:NoneType))',
    },
    'difference': {
        r'((self:frozenset< T?3 > /\ __va_s:Iterable< top >) -> (return:frozenset< T?3 >))',
        r'((self:set< T?0 > /\ __va_s:Iterable< top >) -> (return:set< T?0 >))',
    },
    'difference_update': {
        r'((self:set< T?0 > /\ __va_s:Iterable< top >) -> (return:NoneType))',
    },
    'discard': {
        r'((self:set< T?0 > /\ __element:T?0) -> (return:NoneType))',
    },
    'intersection': {
        r'((self:frozenset< T?3 > /\ __va_s:Iterable< top >) -> (return:frozenset< T?3 >))',
        r'((self:set< T?0 > /\ __va_s:Iterable< top >) -> (return:set< T?0 >))',
    },
    'intersection_update': {
        r'((self:set< T?0 > /\ __va_s:Iterable< top >) -> (return:NoneType))',
    },
    'isdisjoint': {
        r'((self:frozenset< T?3 > /\ __s:Iterable< T?3 >) -> (return:bool))',
        r'((self:set< T?0 > /\ __s:Iterable< top >) -> (return:bool))',
    },
    'issubset': {
        r'((self:frozenset< T?3 > /\ __s:Iterable< top >) -> (return:bool))',
        r'((self:set< T?0 > /\ __s:Iterable< top >) -> (return:bool))',
    },
    'issuperset': {
        r'((self:frozenset< T?3 > /\ __s:Iterable< top >) -> (return:bool))',
        r'((self:set< T?0 > /\ __s:Iterable< top >) -> (return:bool))',
    },
    'symmetric_difference': {
        r'((self:set< T?0 > /\ __s:Iterable< T?0 >) -> (return:set< T?0 >))',
        r'((self:frozenset< T?3 > /\ __s:Iterable< T?3 >) -> (return:frozenset< T?3 >))',
    },
    'symmetric_difference_update': {
        r'((self:set< T?0 > /\ __s:Iterable< T?0 >) -> (return:NoneType))',
    },
    'union': {
        r'((self:set< T?0 > /\ __va_s:Iterable< T?4 >) -> (return:set< T?0 + T?4 >))',
        r'((self:frozenset< T?3 > /\ __va_s:Iterable< T?4 >) -> (return:frozenset< T?4 + T?3 >))',
    },
    'update': {
        r'((self:set< T?0 > /\ __va_s:Iterable< T?0 >) -> (return:NoneType))',
    },
    '__iand__': {
        r'((self:set< T?0 > /\ __value:set< top >) -> (return:set< T?0 >))',
    },
    '__ior__': {
        r'((self:set< T?0 > /\ __value:set< T?0 >) -> (return:set< T?0 >))',
    },
    '__isub__': {
        r'((self:set< T?0 > /\ __value:set< top >) -> (return:set< T?0 >))',
    },
    '__ixor__': {
        r'((self:set< T?0 > /\ __value:set< T?0 >) -> (return:set< T?0 >))',
    },
    '__iter__': {
        r'((self:frozenset< T?3 >) -> (return:frozenset< T?3 >))',
    },
    '__next__': {
        r'((self:frozenset< T?3 >) -> (return:tuple< T?0 + int >))',
    },
    'start': {
        r'((self:range< int >) -> (return:int))',
    },
    'stop': {
        r'((self:range< int >) -> (return:int))',
    },
    'step': {
        r'((self:range< int >) -> (return:int))',
    },
    'all': {
        r'((__iterable:Iterable< top >) -> (return:bool))',
    },
    'any': {
        r'((__iterable:Iterable< top >) -> (return:bool))',
    },
    'ascii': {
        r'((__obj:top) -> (return:str))',
    },
    'bin': {
        r'((__number:bool + int) -> (return:str))',
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
        r'((__o:top) -> (return:list< str >))',
    },
    'getattr': {
        r'((__o:top /\ __name:str) -> (return:top))',
        r'((__o:top /\ __name:str /\ __default:NoneType) -> (return:top + NoneType))',
        r'((__o:top /\ name:str /\ __default:list< top >) -> (return:list< top > + top))',
        r'((__o:top /\ name:str /\ __default:dict< top, top >) -> (return:dict< top, top > + top))',
        r'((__o:top /\ __name:str /\ __default:T?0) -> (return:T?0 + top))',
        r'((__o:top /\ __name:str /\ __default:bool) -> (return:bool + top))',
    },
    'globals': {
        r'(() -> (return:dict< str, top >))',
    },
    'hasattr': {
        r'((__obj:top /\ __name:str) -> (return:bool))',
    },
    'hash': {
        r'((__obj:top) -> (return:int))',
    },
    'help': {
        r'((request:top) -> (return:NoneType))',
    },
    'id': {
        r'((__obj:top) -> (return:int))',
    },
    'input': {
        r'((__prompt:top) -> (return:str))',
    },
    'len': {
        r'((__obj:str + memoryview + tuple< top > + frozenset< top > + bytes + dict< top, top > + bytearray + range + set< top > + list< top >) -> (return:int))',
    },
    'license': {
        r'(() -> (return:NoneType))',
    },
    'locals': {
        r'(() -> (return:dict< str, top >))',
    },
    'oct': {
        r'((__number:bool + int) -> (return:str))',
    },
    'ord': {
        r'((__c:bytearray + str + bytes) -> (return:int))',
    },
    'repr': {
        r'((__obj:top) -> (return:str))',
    },
    'setattr': {
        r'((__obj:top /\ __name:str /\ __value:top) -> (return:NoneType))',
    },
    'vars': {
        r'((__object:top) -> (return:dict< str, top >))',
    },

}
