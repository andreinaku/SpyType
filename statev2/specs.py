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
        ast.Mult: '__mul__ ',
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
    '__new__': {
        r'((cls:frozenset<T?co>) -> (return:frozenset<T?co>))',
        r'((cls:int /\ __x:SupportsTrunc+str+SupportsInt+bytearray+bytes+memoryview+SupportsIndex) -> (return:int))',
        r'((cls:str<str> /\ object:bytearray+bytes+memoryview /\ encoding:str /\ errors:str) -> (return:str<str>))',
        r'((cls:frozenset<T?co> /\ __iterable:Iterable<T?co>) -> (return:frozenset<T?co>))',
        r'((cls:bytes<int> /\ __o:SupportsBytes+bytearray+bytes+Iterable<SupportsIndex>+memoryview+SupportsIndex) -> (return:bytes<int>))',
        r'((cls:dict<T?K, T?V> /\ __va_args:top /\ __kw_kwargs:top) -> (return:dict<T?K, T?V>))',
        r'((cls:float /\ __x:str+SupportsFloat+bytearray+bytes+memoryview+SupportsIndex) -> (return:float))',
        r'((cls:bytes<int> /\ __string:str /\ encoding:str /\ errors:str) -> (return:bytes<int>))',
        r'((cls:str<str> /\ object:top) -> (return:str<str>))',
        r'((cls:tuple<T?co> /\ __iterable:Iterable<T?co>) -> (return:tuple<T?co>))',
        r'((cls:bytes<int>) -> (return:bytes<int>))',
        r'((cls:int /\ __x:bytearray+str+bytes /\ base:SupportsIndex) -> (return:int))',
        r'((cls:bool /\ __o:top) -> (return:bool))',
    },
    'real': {
        r'((self:float) -> (return:float))',
        r'((self:int) -> (return:int))',
        r'((self:complex) -> (return:float))',
    },
    'imag': {
        r'((self:float) -> (return:float))',
        r'((self:int) -> (return:int))',
        r'((self:complex) -> (return:float))',
    },
    'numerator': {
        r'((self:int) -> (return:int))',
    },
    'denominator': {
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
        r'((self:list<T?0> /\ __value:list<T?s>) -> (return:list<T?0+T?s>))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:str /\ __value:str) -> (return:str))',
        r'((self:str<str> /\ __value:str) -> (return:str))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:bytearray<int> /\ __value:bytearray+bytes+memoryview) -> (return:bytearray))',
        r'((self:bytes<int> /\ __value:bytearray+bytes+memoryview) -> (return:bytes))',
        r'((self:tuple<T?co> /\ __value:tuple<T?co>) -> (return:tuple<T?co>))',
        r'((self:list<T?0> /\ __value:list<T?0>) -> (return:list<T?0>))',
        r'((self:tuple<T?co> /\ __value:tuple<T?0>) -> (return:tuple<T?co+T?0>))',
    },
    '__sub__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:set<T?0> /\ __value:set<T?0+NoneType>) -> (return:set<T?0>))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:frozenset<T?co> /\ __value:set<T?co>) -> (return:frozenset<T?co>))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__mul__': {
        r'((self:str /\ __value:SupportsIndex) -> (return:str))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:bytes<int> /\ __value:SupportsIndex) -> (return:bytes))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:str<str> /\ __value:SupportsIndex) -> (return:str))',
        r'((self:list<T?0> /\ __value:SupportsIndex) -> (return:list<T?0>))',
        r'((self:tuple<T?co> /\ __value:SupportsIndex) -> (return:tuple<T?co>))',
        r'((self:bytearray<int> /\ __value:SupportsIndex) -> (return:bytearray))',
    },
    '__floordiv__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__truediv__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:float))',
    },
    '__mod__': {
        r'((self:str<str> /\ __value:top) -> (return:str))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bytearray<int> /\ __value:top) -> (return:bytes))',
        r'((self:bytes<int> /\ __value:top) -> (return:bytes))',
        r'((self:str /\ __value:str+tuple<str>) -> (return:str))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__divmod__': {
        r'((self:int /\ __value:int) -> (return:tuple<int>))',
        r'((self:float /\ __value:float) -> (return:tuple<float>))',
    },
    '__radd__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rsub__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rmul__': {
        r'((self:str /\ __value:SupportsIndex) -> (return:str))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:bytes<int> /\ __value:SupportsIndex) -> (return:bytes))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:str<str> /\ __value:SupportsIndex) -> (return:str))',
        r'((self:list<T?0> /\ __value:SupportsIndex) -> (return:list<T?0>))',
        r'((self:tuple<T?co> /\ __value:SupportsIndex) -> (return:tuple<T?co>))',
        r'((self:bytearray<int> /\ __value:SupportsIndex) -> (return:bytearray))',
    },
    '__rfloordiv__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rtruediv__': {
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:float))',
    },
    '__rmod__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
    },
    '__rdivmod__': {
        r'((self:int /\ __value:int) -> (return:tuple<int>))',
        r'((self:float /\ __value:float) -> (return:tuple<float>))',
    },
    '__pow__': {
        r'((self:int /\ __x:int) -> (return:int))',
        r'((self:int /\ __value:int /\ __mod:int) -> (return:int))',
        r'((self:int /\ __value:int /\ __mod:NoneType) -> (return:float))',
        r'((self:float /\ __value:int /\ __mod:NoneType) -> (return:float))',
        r'((self:int /\ __value:int /\ __mod:NoneType) -> (return:int))',
        r'((self:complex /\ __value:complex /\ __mod:NoneType) -> (return:complex))',
    },
    '__and__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:frozenset<T?co> /\ __value:set<T?co>) -> (return:frozenset<T?co>))',
        r'((self:set<T?0> /\ __value:set<top>) -> (return:set<T?0>))',
        r'((self:bool /\ __value:int) -> (return:int))',
    },
    '__or__': {
        r'((self:frozenset<T?co> /\ __value:set<T?s>) -> (return:frozenset<T?co+T?s>))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:set<T?0> /\ __value:set<T?s>) -> (return:set<T?0+T?s>))',
        r'((self:bool /\ __value:int) -> (return:int))',
    },
    '__xor__': {
        r'((self:frozenset<T?co> /\ __value:set<T?s>) -> (return:frozenset<T?co+T?s>))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:set<T?0> /\ __value:set<T?s>) -> (return:set<T?0+T?s>))',
        r'((self:bool /\ __value:int) -> (return:int))',
    },
    '__lshift__': {
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rshift__': {
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rand__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:bool /\ __value:int) -> (return:int))',
    },
    '__ror__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:bool /\ __value:int) -> (return:int))',
    },
    '__rxor__': {
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
        r'((self:bool /\ __value:int) -> (return:int))',
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
        r'((self:int) -> (return:int))',
        r'((self:float) -> (return:int))',
    },
    '__ceil__': {
        r'((self:int) -> (return:int))',
    },
    '__floor__': {
        r'((self:int) -> (return:int))',
    },
    '__round__': {
        r'((self:float /\ __ndigits:NoneType) -> (return:int))',
        r'((self:float /\ __ndigits:SupportsIndex) -> (return:float))',
        r'((self:int /\ __ndigits:SupportsIndex) -> (return:int))',
    },
    '__getnewargs__': {
        r'((self:float) -> (return:tuple<float>))',
        r'((self:int) -> (return:tuple<int>))',
        r'((self:bool) -> (return:tuple<int>))',
        r'((self:bytes<int>) -> (return:tuple<bytes>))',
        r'((self:str<str>) -> (return:tuple<str>))',
    },
    '__eq__': {
        r'((self:dict<T?K, T?V> /\ __value:top) -> (return:bool))',
        r'((self:tuple<T?co> /\ __value:top) -> (return:bool))',
        r'((self:frozenset<T?co> /\ __value:top) -> (return:bool))',
        r'((self:complex /\ __value:top) -> (return:bool))',
        r'((self:set<T?0> /\ __value:top) -> (return:bool))',
        r'((self:int /\ __value:top) -> (return:bool))',
        r'((self:range<int> /\ __value:top) -> (return:bool))',
        r'((self:list<T?0> /\ __value:top) -> (return:bool))',
        r'((self:slice /\ __value:top) -> (return:bool))',
        r'((self:bytes<int> /\ __value:top) -> (return:bool))',
        r'((self:str<str> /\ __value:top) -> (return:bool))',
        r'((self:float /\ __value:top) -> (return:bool))',
        r'((self:bytearray<int> /\ __value:top) -> (return:bool))',
    },
    '__ne__': {
        r'((self:bytes<int> /\ __value:top) -> (return:bool))',
        r'((self:str<str> /\ __value:top) -> (return:bool))',
        r'((self:float /\ __value:top) -> (return:bool))',
        r'((self:complex /\ __value:top) -> (return:bool))',
        r'((self:bytearray<int> /\ __value:top) -> (return:bool))',
        r'((self:int /\ __value:top) -> (return:bool))',
    },
    '__lt__': {
        r'((self:list<T?0> /\ __value:list<T?0>) -> (return:bool))',
        r'((self:set<T?0> /\ __value:set<top>) -> (return:bool))',
        r'((self:tuple<T?co> /\ __value:tuple<T?co>) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:bytes<int> /\ __value:bytes) -> (return:bool))',
        r'((self:bytearray<int> /\ __value:bytearray+bytes+memoryview) -> (return:bool))',
        r'((self:str<str> /\ __value:str) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:frozenset<T?co> /\ __value:set<top>) -> (return:bool))',
    },
    '__le__': {
        r'((self:list<T?0> /\ __value:list<T?0>) -> (return:bool))',
        r'((self:set<T?0> /\ __value:set<top>) -> (return:bool))',
        r'((self:tuple<T?co> /\ __value:tuple<T?co>) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:bytes<int> /\ __value:bytes) -> (return:bool))',
        r'((self:bytearray<int> /\ __value:bytearray+bytes+memoryview) -> (return:bool))',
        r'((self:str<str> /\ __value:str) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:frozenset<T?co> /\ __value:set<top>) -> (return:bool))',
    },
    '__gt__': {
        r'((self:list<T?0> /\ __value:list<T?0>) -> (return:bool))',
        r'((self:set<T?0> /\ __value:set<top>) -> (return:bool))',
        r'((self:tuple<T?co> /\ __value:tuple<T?co>) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:bytes<int> /\ __value:bytes) -> (return:bool))',
        r'((self:bytearray<int> /\ __value:bytearray+bytes+memoryview) -> (return:bool))',
        r'((self:str<str> /\ __value:str) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:frozenset<T?co> /\ __value:set<top>) -> (return:bool))',
    },
    '__ge__': {
        r'((self:list<T?0> /\ __value:list<T?0>) -> (return:bool))',
        r'((self:set<T?0> /\ __value:set<top>) -> (return:bool))',
        r'((self:tuple<T?co> /\ __value:tuple<T?co>) -> (return:bool))',
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:bytes<int> /\ __value:bytes) -> (return:bool))',
        r'((self:bytearray<int> /\ __value:bytearray+bytes+memoryview) -> (return:bool))',
        r'((self:str<str> /\ __value:str) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
        r'((self:frozenset<T?co> /\ __value:set<top>) -> (return:bool))',
    },
    '__float__': {
        r'((self:float) -> (return:float))',
        r'((self:int) -> (return:float))',
    },
    '__int__': {
        r'((self:int) -> (return:int))',
        r'((self:float) -> (return:int))',
    },
    '__abs__': {
        r'((self:float) -> (return:float))',
        r'((self:int) -> (return:int))',
        r'((self:complex) -> (return:float))',
    },
    '__hash__': {
        r'((self:tuple<T?co>) -> (return:int))',
        r'((self:range<int>) -> (return:int))',
        r'((self:str<str>) -> (return:int))',
        r'((self:complex) -> (return:int))',
        r'((self:frozenset<T?co>) -> (return:int))',
        r'((self:int) -> (return:int))',
        r'((self:bytes<int>) -> (return:int))',
        r'((self:float) -> (return:int))',
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
        r'((self:float) -> (return:tuple<int>))',
    },
    'hex': {
        r'((__number:int+SupportsIndex) -> (return:str))',
        r'((self:float) -> (return:str))',
    },
    'is_integer': {
        r'((self:float) -> (return:bool))',
    },
    'fromhex': {
        r'((cls:bytes<int> /\ __string:str) -> (return:bytes<int>))',
        r'((cls:bytearray<int> /\ __string:str) -> (return:bytearray<int>))',
        r'((cls:float /\ __string:str) -> (return:float))',
    },
    '__rpow__': {
        r'((self:float /\ __value:int /\ __mod:NoneType) -> (return:complex))',
        r'((self:float /\ __value:int /\ __mod:NoneType) -> (return:float))',
        r'((self:complex /\ __value:complex /\ __mod:NoneType) -> (return:complex))',
    },
    'capitalize': {
        r'((self:bytearray<int>) -> (return:bytearray))',
        r'((self:str<str>) -> (return:str))',
        r'((self:bytes<int>) -> (return:bytes))',
        r'((self:str) -> (return:str))',
    },
    'casefold': {
        r'((self:str<str>) -> (return:str))',
        r'((self:str) -> (return:str))',
    },
    'center': {
        r'((self:bytearray<int> /\ __width:SupportsIndex /\ __fillchar:bytes) -> (return:bytearray))',
        r'((self:str<str> /\ __width:SupportsIndex /\ __fillchar:str) -> (return:str))',
        r'((self:str /\ __width:SupportsIndex /\ __fillchar:str) -> (return:str))',
        r'((self:bytes<int> /\ __width:SupportsIndex /\ __fillchar:bytes) -> (return:bytes))',
    },
    'count': {
        r'((self:bytes<int> /\ __sub:bytearray+bytes+memoryview+SupportsIndex /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
        r'((self:bytearray<int> /\ __sub:bytearray+bytes+memoryview+SupportsIndex /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
        r'((self:str<str> /\ x:str /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
        r'((self:list<T?0> /\ __value:T?0) -> (return:int))',
        r'((self:tuple<T?co> /\ __value:top) -> (return:int))',
        r'((self:range<int> /\ __value:int) -> (return:int))',
    },
    'encode': {
        r'((self:str<str> /\ encoding:str /\ errors:str) -> (return:bytes))',
    },
    'endswith': {
        r'((self:bytearray<int> /\ __suffix:bytearray+bytes+memoryview+tuple<bytearray+bytes+memoryview> /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:bool))',
        r'((self:str<str> /\ __suffix:str+tuple<str> /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:bool))',
        r'((self:bytes<int> /\ __suffix:bytearray+bytes+memoryview+tuple<bytearray+bytes+memoryview> /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:bool))',
    },
    'find': {
        r'((self:bytes<int> /\ __sub:bytearray+bytes+memoryview+SupportsIndex /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
        r'((self:bytearray<int> /\ __sub:bytearray+bytes+memoryview+SupportsIndex /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
        r'((self:str<str> /\ __sub:str /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
    },
    'format': {
        r'((self:str<str> /\ __va_args:top /\ __kw_kwargs:top) -> (return:str))',
        r'((self:str /\ __va_args:str /\ __kw_kwargs:str) -> (return:str))',
        r'((__value:top /\ __format_spec:str) -> (return:str))',
    },
    'format_map': {
        r'((self:str<str> /\ map:dict<str, int>) -> (return:str))',
    },
    'index': {
        r'((self:bytes<int> /\ __sub:bytearray+bytes+memoryview+SupportsIndex /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
        r'((self:bytearray<int> /\ __sub:bytearray+bytes+memoryview+SupportsIndex /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
        r'((self:tuple<T?co> /\ __value:top /\ __start:SupportsIndex /\ __stop:SupportsIndex) -> (return:int))',
        r'((self:list<T?0> /\ __value:T?0 /\ __start:SupportsIndex /\ __stop:SupportsIndex) -> (return:int))',
        r'((self:str<str> /\ __sub:str /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
        r'((self:range<int> /\ __value:int) -> (return:int))',
    },
    'isalnum': {
        r'((self:bytearray<int>) -> (return:bool))',
        r'((self:bytes<int>) -> (return:bool))',
        r'((self:str<str>) -> (return:bool))',
    },
    'isalpha': {
        r'((self:bytearray<int>) -> (return:bool))',
        r'((self:bytes<int>) -> (return:bool))',
        r'((self:str<str>) -> (return:bool))',
    },
    'isascii': {
        r'((self:bytearray<int>) -> (return:bool))',
        r'((self:bytes<int>) -> (return:bool))',
        r'((self:str<str>) -> (return:bool))',
    },
    'isdecimal': {
        r'((self:str<str>) -> (return:bool))',
    },
    'isdigit': {
        r'((self:bytearray<int>) -> (return:bool))',
        r'((self:bytes<int>) -> (return:bool))',
        r'((self:str<str>) -> (return:bool))',
    },
    'isidentifier': {
        r'((self:str<str>) -> (return:bool))',
    },
    'islower': {
        r'((self:bytearray<int>) -> (return:bool))',
        r'((self:bytes<int>) -> (return:bool))',
        r'((self:str<str>) -> (return:bool))',
    },
    'isnumeric': {
        r'((self:str<str>) -> (return:bool))',
    },
    'isprintable': {
        r'((self:str<str>) -> (return:bool))',
    },
    'isspace': {
        r'((self:bytearray<int>) -> (return:bool))',
        r'((self:bytes<int>) -> (return:bool))',
        r'((self:str<str>) -> (return:bool))',
    },
    'istitle': {
        r'((self:bytearray<int>) -> (return:bool))',
        r'((self:bytes<int>) -> (return:bool))',
        r'((self:str<str>) -> (return:bool))',
    },
    'isupper': {
        r'((self:bytearray<int>) -> (return:bool))',
        r'((self:bytes<int>) -> (return:bool))',
        r'((self:str<str>) -> (return:bool))',
    },
    'join': {
        r'((self:bytearray<int> /\ __iterable_of_bytes:Iterable<bytearray+bytes+memoryview>) -> (return:bytearray))',
        r'((self:str /\ __iterable:Iterable<str>) -> (return:str))',
        r'((self:bytes<int> /\ __iterable_of_bytes:Iterable<bytearray+bytes+memoryview>) -> (return:bytes))',
        r'((self:str<str> /\ __iterable:Iterable<str>) -> (return:str))',
    },
    'ljust': {
        r'((self:bytearray<int> /\ __width:SupportsIndex /\ __fillchar:bytearray+bytes) -> (return:bytearray))',
        r'((self:str<str> /\ __width:SupportsIndex /\ __fillchar:str) -> (return:str))',
        r'((self:str /\ __width:SupportsIndex /\ __fillchar:str) -> (return:str))',
        r'((self:bytes<int> /\ __width:SupportsIndex /\ __fillchar:bytearray+bytes) -> (return:bytes))',
    },
    'lower': {
        r'((self:bytearray<int>) -> (return:bytearray))',
        r'((self:str<str>) -> (return:str))',
        r'((self:bytes<int>) -> (return:bytes))',
        r'((self:str) -> (return:str))',
    },
    'lstrip': {
        r'((self:str /\ __chars:NoneType+str) -> (return:str))',
        r'((self:bytearray<int> /\ __bytes:NoneType+bytes+memoryview+bytearray) -> (return:bytearray))',
        r'((self:bytes<int> /\ __bytes:NoneType+bytes+memoryview+bytearray) -> (return:bytes))',
        r'((self:str<str> /\ __chars:NoneType+str) -> (return:str))',
    },
    'partition': {
        r'((self:bytes<int> /\ __sep:bytearray+bytes+memoryview) -> (return:tuple<bytes>))',
        r'((self:str<str> /\ __sep:str) -> (return:tuple<str>))',
        r'((self:bytearray<int> /\ __sep:bytearray+bytes+memoryview) -> (return:tuple<bytearray>))',
        r'((self:str /\ __sep:str) -> (return:tuple<str>))',
    },
    'replace': {
        r'((self:bytes<int> /\ __old:bytearray+bytes+memoryview /\ __new:bytearray+bytes+memoryview /\ __count:SupportsIndex) -> (return:bytes))',
        r'((self:str /\ __old:str /\ __new:str /\ __count:SupportsIndex) -> (return:str))',
        r'((self:bytearray<int> /\ __old:bytearray+bytes+memoryview /\ __new:bytearray+bytes+memoryview /\ __count:SupportsIndex) -> (return:bytearray))',
        r'((self:str<str> /\ __old:str /\ __new:str /\ __count:SupportsIndex) -> (return:str))',
    },
    'rfind': {
        r'((self:bytes<int> /\ __sub:bytearray+bytes+memoryview+SupportsIndex /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
        r'((self:bytearray<int> /\ __sub:bytearray+bytes+memoryview+SupportsIndex /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
        r'((self:str<str> /\ __sub:str /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
    },
    'rindex': {
        r'((self:bytes<int> /\ __sub:bytearray+bytes+memoryview+SupportsIndex /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
        r'((self:bytearray<int> /\ __sub:bytearray+bytes+memoryview+SupportsIndex /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
        r'((self:str<str> /\ __sub:str /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:int))',
    },
    'rjust': {
        r'((self:bytearray<int> /\ __width:SupportsIndex /\ __fillchar:bytearray+bytes) -> (return:bytearray))',
        r'((self:str<str> /\ __width:SupportsIndex /\ __fillchar:str) -> (return:str))',
        r'((self:str /\ __width:SupportsIndex /\ __fillchar:str) -> (return:str))',
        r'((self:bytes<int> /\ __width:SupportsIndex /\ __fillchar:bytearray+bytes) -> (return:bytes))',
    },
    'rpartition': {
        r'((self:bytes<int> /\ __sep:bytearray+bytes+memoryview) -> (return:tuple<bytes>))',
        r'((self:str<str> /\ __sep:str) -> (return:tuple<str>))',
        r'((self:bytearray<int> /\ __sep:bytearray+bytes+memoryview) -> (return:tuple<bytearray>))',
        r'((self:str /\ __sep:str) -> (return:tuple<str>))',
    },
    'rsplit': {
        r'((self:str /\ sep:NoneType+str /\ maxsplit:SupportsIndex) -> (return:list<str>))',
        r'((self:str<str> /\ sep:NoneType+str /\ maxsplit:SupportsIndex) -> (return:list<str>))',
        r'((self:bytearray<int> /\ sep:NoneType+bytes+memoryview+bytearray /\ maxsplit:SupportsIndex) -> (return:list<bytearray>))',
        r'((self:bytes<int> /\ sep:NoneType+bytes+memoryview+bytearray /\ maxsplit:SupportsIndex) -> (return:list<bytes>))',
    },
    'rstrip': {
        r'((self:str /\ __chars:NoneType+str) -> (return:str))',
        r'((self:bytearray<int> /\ __bytes:NoneType+bytes+memoryview+bytearray) -> (return:bytearray))',
        r'((self:bytes<int> /\ __bytes:NoneType+bytes+memoryview+bytearray) -> (return:bytes))',
        r'((self:str<str> /\ __chars:NoneType+str) -> (return:str))',
    },
    'split': {
        r'((self:str /\ sep:NoneType+str /\ maxsplit:SupportsIndex) -> (return:list<str>))',
        r'((self:str<str> /\ sep:NoneType+str /\ maxsplit:SupportsIndex) -> (return:list<str>))',
        r'((self:bytearray<int> /\ sep:NoneType+bytes+memoryview+bytearray /\ maxsplit:SupportsIndex) -> (return:list<bytearray>))',
        r'((self:bytes<int> /\ sep:NoneType+bytes+memoryview+bytearray /\ maxsplit:SupportsIndex) -> (return:list<bytes>))',
    },
    'splitlines': {
        r'((self:str /\ keepends:bool) -> (return:list<str>))',
        r'((self:str<str> /\ keepends:bool) -> (return:list<str>))',
        r'((self:bytearray<int> /\ keepends:bool) -> (return:list<bytearray>))',
        r'((self:bytes<int> /\ keepends:bool) -> (return:list<bytes>))',
    },
    'startswith': {
        r'((self:bytearray<int> /\ __prefix:bytearray+bytes+memoryview+tuple<bytearray+bytes+memoryview> /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:bool))',
        r'((self:str<str> /\ __prefix:str+tuple<str> /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:bool))',
        r'((self:bytes<int> /\ __prefix:bytearray+bytes+memoryview+tuple<bytearray+bytes+memoryview> /\ __start:NoneType+SupportsIndex /\ __end:NoneType+SupportsIndex) -> (return:bool))',
    },
    'strip': {
        r'((self:str /\ __chars:NoneType+str) -> (return:str))',
        r'((self:bytearray<int> /\ __bytes:NoneType+bytes+memoryview+bytearray) -> (return:bytearray))',
        r'((self:bytes<int> /\ __bytes:NoneType+bytes+memoryview+bytearray) -> (return:bytes))',
        r'((self:str<str> /\ __chars:NoneType+str) -> (return:str))',
    },
    'swapcase': {
        r'((self:bytearray<int>) -> (return:bytearray))',
        r'((self:str<str>) -> (return:str))',
        r'((self:bytes<int>) -> (return:bytes))',
        r'((self:str) -> (return:str))',
    },
    'title': {
        r'((self:bytearray<int>) -> (return:bytearray))',
        r'((self:str<str>) -> (return:str))',
        r'((self:bytes<int>) -> (return:bytes))',
        r'((self:str) -> (return:str))',
    },
    'translate': {
        r'((self:str<str> /\ __table:dict<int, str+int>) -> (return:str))',
        r'((self:bytearray<int> /\ __table:NoneType+bytes+memoryview+bytearray /\ delete:bytes) -> (return:bytearray))',
        r'((self:bytes<int> /\ __table:NoneType+bytes+memoryview+bytearray /\ delete:bytes) -> (return:bytes))',
    },
    'upper': {
        r'((self:bytearray<int>) -> (return:bytearray))',
        r'((self:str<str>) -> (return:str))',
        r'((self:bytes<int>) -> (return:bytes))',
        r'((self:str) -> (return:str))',
    },
    'zfill': {
        r'((self:str<str> /\ __width:SupportsIndex) -> (return:str))',
        r'((self:str /\ __width:SupportsIndex) -> (return:str))',
        r'((self:bytearray<int> /\ __width:SupportsIndex) -> (return:bytearray))',
        r'((self:bytes<int> /\ __width:SupportsIndex) -> (return:bytes))',
    },
    'maketrans': {
        r'((__frm:bytearray+bytes+memoryview /\ __to:bytearray+bytes+memoryview) -> (return:bytes))',
        r'((__x:str /\ __y:str /\ __z:str) -> (return:dict<int, NoneType+int>))',
        r'((__x:dict<str+int, T?0>+dict<str, T?0>+dict<int, T?0>) -> (return:dict<int, T?0>))',
        r'((__x:str /\ __y:str) -> (return:dict<int, int>))',
    },
    '__contains__': {
        r'((self:bytes<int> /\ __key:bytearray+bytes+memoryview+SupportsIndex) -> (return:bool))',
        r'((self:range<int> /\ __key:top) -> (return:bool))',
        r'((self:set<T?0> /\ __o:top) -> (return:bool))',
        r'((self:list<T?0> /\ __key:top) -> (return:bool))',
        r'((self:frozenset<T?co> /\ __o:top) -> (return:bool))',
        r'((self:str<str> /\ __key:str) -> (return:bool))',
        r'((self:bytearray<int> /\ __key:bytearray+bytes+memoryview+SupportsIndex) -> (return:bool))',
        r'((self:tuple<T?co> /\ __key:top) -> (return:bool))',
    },
    '__iter__': {
        r'((self:set<T?0>) -> (return:Iterator<T?0>))',
        r'((self:bytearray<int>) -> (return:Iterator<int>))',
        r'((self:bytes<int>) -> (return:Iterator<int>))',
        r'((self:dict<T?K, T?V>) -> (return:Iterator<T?K>))',
        r'((self:frozenset<T?co>) -> (return:Iterator<T?co>))',
        r'((self:range<int>) -> (return:Iterator<int>))',
        r'((self:reversed<T?0>) -> (return:reversed<T?0>))',
        r'((self:str) -> (return:Iterator<str>))',
        r'((self:list<T?0>) -> (return:Iterator<T?0>))',
        r'((self:filter<T?0>) -> (return:filter<T?0>))',
        r'((self:map<T?s>) -> (return:map<T?s>))',
        r'((self:tuple<T?co>) -> (return:Iterator<T?co>))',
        r'((self:str<str>) -> (return:Iterator<str>))',
        r'((self:zip<T?co>) -> (return:zip<T?co>))',
    },
    '__len__': {
        r'((self:tuple<T?co>) -> (return:int))',
        r'((self:str<str>) -> (return:int))',
        r'((self:set<T?0>) -> (return:int))',
        r'((self:frozenset<T?co>) -> (return:int))',
        r'((self:bytearray<int>) -> (return:int))',
        r'((self:bytes<int>) -> (return:int))',
        r'((self:dict<T?K, T?V>) -> (return:int))',
        r'((self:range<int>) -> (return:int))',
        r'((self:list<T?0>) -> (return:int))',
    },
    'decode': {
        r'((self:bytearray<int> /\ encoding:str /\ errors:str) -> (return:str))',
        r'((self:bytes<int> /\ encoding:str /\ errors:str) -> (return:str))',
    },
    '__getitem__': {
        r'((self:dict<T?K, T?V> /\ __key:T?K) -> (return:T?V))',
        r'((self:bytes<int> /\ __key:SupportsIndex) -> (return:int))',
        r'((self:list<T?0> /\ __i:SupportsIndex) -> (return:T?0))',
        r'((self:bytearray<int> /\ __key:SupportsIndex) -> (return:int))',
        r'((self:range<int> /\ __key:SupportsIndex) -> (return:int))',
        r'((self:tuple<T?co> /\ __key:SupportsIndex) -> (return:T?co))',
    },
    '__buffer__': {
        r'((self:bytearray<int> /\ __flags:int) -> (return:memoryview))',
        r'((self:bytes<int> /\ __flags:int) -> (return:memoryview))',
    },
    '__init__': {
        r'((self:dict<T?K, T?V> /\ __iterable:Iterable<tuple<T?K+T?V>>) -> (return:NoneType))',
        r'((self:reversed<T?0> /\ __sequence:Reversible<T?0>) -> (return:NoneType))',
        r'((self:dict<str, str> /\ __iterable:Iterable<list<str>>) -> (return:NoneType))',
        r'((self:dict<str, T?V> /\ __kw_kwargs:T?V) -> (return:NoneType))',
        r'((self:set<T?0>) -> (return:NoneType))',
        r'((self:range<int> /\ __start:SupportsIndex /\ __stop:SupportsIndex /\ __step:SupportsIndex) -> (return:NoneType))',
        r'((self:dict<bytes, bytes> /\ __iterable:Iterable<list<bytes>>) -> (return:NoneType))',
        r'((self:slice /\ __stop:top) -> (return:NoneType))',
        r'((self:bytearray<int>) -> (return:NoneType))',
        r'((self:list<T?0> /\ __iterable:Iterable<T?0>) -> (return:NoneType))',
        r'((self:dict<str, T?V> /\ __iterable:Iterable<tuple<T?V+str>> /\ __kw_kwargs:T?V) -> (return:NoneType))',
        r'((self:set<T?0> /\ __iterable:Iterable<T?0>) -> (return:NoneType))',
        r'((self:range<int> /\ __stop:SupportsIndex) -> (return:NoneType))',
        r'((self:dict<str, T?V> /\ __map:dict<str, T?V> /\ __kw_kwargs:T?V) -> (return:NoneType))',
        r'((self:dict<T?K, T?V> /\ __map:dict<T?K, T?V>) -> (return:NoneType))',
        r'((self:list<T?0>) -> (return:NoneType))',
        r'((self:UnicodeTranslateError /\ __object:str /\ __start:int /\ __end:int /\ __reason:str) -> (return:NoneType))',
        r'((self:UnicodeDecodeError /\ __encoding:str /\ __object:bytearray+bytes+memoryview /\ __start:int /\ __end:int /\ __reason:str) -> (return:NoneType))',
        r'((self:bytearray<int> /\ __string:str /\ encoding:str /\ errors:str) -> (return:NoneType))',
        r'((self:slice /\ __start:top /\ __stop:top /\ __step:top) -> (return:NoneType))',
        r'((self:dict<T?K, T?V>) -> (return:NoneType))',
        r'((self:reversed<T?0> /\ __sequence:SupportsLenAndGetItem<T?0>) -> (return:NoneType))',
        r'((self:BaseException /\ __va_args:top) -> (return:NoneType))',
        r'((self:UnicodeEncodeError /\ __encoding:str /\ __object:str /\ __start:int /\ __end:int /\ __reason:str) -> (return:NoneType))',
        r'((self:ImportError /\ __va_args:top /\ __ko_name:NoneType+str /\ __ko_path:NoneType+str) -> (return:NoneType))',
        r'((self:filter<T?0> /\ __function:NoneType /\ __iterable:Iterable<T?0+NoneType>) -> (return:NoneType))',
        r'((self:bytearray<int> /\ __ints:bytearray+bytes+Iterable<SupportsIndex>+memoryview+SupportsIndex) -> (return:NoneType))',
    },
    'append': {
        r'((self:list<T?0> /\ __object:T?0) -> (return:NoneType))',
        r'((self:bytearray<int> /\ __item:SupportsIndex) -> (return:NoneType))',
    },
    'copy': {
        r'((self:bytearray<int>) -> (return:bytearray))',
        r'((self:frozenset<T?co>) -> (return:frozenset<T?co>))',
        r'((self:set<T?0>) -> (return:set<T?0>))',
        r'((self:dict<T?K, T?V>) -> (return:dict<T?K, T?V>))',
        r'((self:list<T?0>) -> (return:list<T?0>))',
    },
    'extend': {
        r'((self:list<T?0> /\ __iterable:Iterable<T?0>) -> (return:NoneType))',
        r'((self:bytearray<int> /\ __iterable_of_ints:Iterable<SupportsIndex>) -> (return:NoneType))',
    },
    'insert': {
        r'((self:bytearray<int> /\ __index:SupportsIndex /\ __item:SupportsIndex) -> (return:NoneType))',
        r'((self:list<T?0> /\ __index:SupportsIndex /\ __object:T?0) -> (return:NoneType))',
    },
    'pop': {
        r'((self:dict<T?K, T?V> /\ __key:T?K) -> (return:T?V))',
        r'((self:list<T?0> /\ __index:SupportsIndex) -> (return:T?0))',
        r'((self:dict<T?K, T?V> /\ __key:T?K /\ __default:T?V) -> (return:T?V))',
        r'((self:bytearray<int> /\ __index:int) -> (return:int))',
        r'((self:dict<T?K, T?V> /\ __key:T?K /\ __default:T?0) -> (return:T?0+T?V))',
    },
    'remove': {
        r'((self:set<T?0> /\ __element:T?0) -> (return:NoneType))',
        r'((self:list<T?0> /\ __value:T?0) -> (return:NoneType))',
        r'((self:bytearray<int> /\ __value:int) -> (return:NoneType))',
    },
    '__setitem__': {
        r'((self:bytearray<int> /\ __key:SupportsIndex /\ __value:SupportsIndex) -> (return:NoneType))',
        r'((self:dict<T?K, T?V> /\ __key:T?K /\ __value:T?V) -> (return:NoneType))',
        r'((self:list<T?0> /\ __key:SupportsIndex /\ __value:T?0) -> (return:NoneType))',
    },
    '__iadd__': {
        r'((self:bytearray<int> /\ __value:bytearray+bytes+memoryview) -> (return:bytearray<int>))',
        r'((self:list<T?0> /\ __value:Iterable<T?0>) -> (return:list<T?0>))',
    },
    '__imul__': {
        r'((self:list<T?0> /\ __value:SupportsIndex) -> (return:list<T?0>))',
        r'((self:bytearray<int> /\ __value:SupportsIndex) -> (return:bytearray<int>))',
    },
    '__alloc__': {
        r'((self:bytearray<int>) -> (return:int))',
    },
    '__release_buffer__': {
        r'((self:bytearray<int> /\ __buffer:memoryview) -> (return:NoneType))',
    },
    'indices': {
        r'((self:slice /\ __len:SupportsIndex) -> (return:tuple<int>))',
    },
    'sort': {
        r'((self:list<SupportsRichComparisonT> /\ __ko_key:NoneType /\ __ko_reverse:bool) -> (return:NoneType))',
    },
    '__reversed__': {
        r'((self:range<int>) -> (return:Iterator<int>))',
        r'((self:list<T?0>) -> (return:Iterator<T?0>))',
    },
    'keys': {
        r'((self:dict<T?K, T?V>) -> (return:list<T?K>))',
    },
    'values': {
        r'((self:dict<T?K, T?V>) -> (return:list<T?V>))',
    },
    'items': {
        r'((self:dict<T?K, T?V>) -> (return:list<tuple<T?K+T?V>>))',
    },
    'fromkeys': {
        r'((cls:dict<T?K, T?V> /\ __iterable:Iterable<T?0> /\ __value:NoneType) -> (return:dict<T?0, NoneType+top>))',
        r'((cls:dict<T?K, T?V> /\ __iterable:Iterable<T?0> /\ __value:T?s) -> (return:dict<T?0, T?s>))',
    },
    'get': {
        r'((self:dict<T?K, T?V> /\ __key:T?K /\ __default:T?0) -> (return:T?0+T?V))',
        r'((self:dict<T?K, T?V> /\ __key:T?K /\ __default:T?V) -> (return:T?V))',
        r'((self:dict<T?K, T?V> /\ __key:T?K) -> (return:NoneType+T?V))',
    },
    '__delitem__': {
        r'((self:dict<T?K, T?V> /\ __key:T?K) -> (return:NoneType))',
    },
    'add': {
        r'((self:set<T?0> /\ __element:T?0) -> (return:NoneType))',
    },
    'difference': {
        r'((self:frozenset<T?co> /\ __va_s:Iterable<top>) -> (return:frozenset<T?co>))',
        r'((self:set<T?0> /\ __va_s:Iterable<top>) -> (return:set<T?0>))',
    },
    'difference_update': {
        r'((self:set<T?0> /\ __va_s:Iterable<top>) -> (return:NoneType))',
    },
    'discard': {
        r'((self:set<T?0> /\ __element:T?0) -> (return:NoneType))',
    },
    'intersection': {
        r'((self:frozenset<T?co> /\ __va_s:Iterable<top>) -> (return:frozenset<T?co>))',
        r'((self:set<T?0> /\ __va_s:Iterable<top>) -> (return:set<T?0>))',
    },
    'intersection_update': {
        r'((self:set<T?0> /\ __va_s:Iterable<top>) -> (return:NoneType))',
    },
    'isdisjoint': {
        r'((self:frozenset<T?co> /\ __s:Iterable<T?co>) -> (return:bool))',
        r'((self:set<T?0> /\ __s:Iterable<top>) -> (return:bool))',
    },
    'issubset': {
        r'((self:frozenset<T?co> /\ __s:Iterable<top>) -> (return:bool))',
        r'((self:set<T?0> /\ __s:Iterable<top>) -> (return:bool))',
    },
    'issuperset': {
        r'((self:frozenset<T?co> /\ __s:Iterable<top>) -> (return:bool))',
        r'((self:set<T?0> /\ __s:Iterable<top>) -> (return:bool))',
    },
    'symmetric_difference': {
        r'((self:frozenset<T?co> /\ __s:Iterable<T?co>) -> (return:frozenset<T?co>))',
        r'((self:set<T?0> /\ __s:Iterable<T?0>) -> (return:set<T?0>))',
    },
    'symmetric_difference_update': {
        r'((self:set<T?0> /\ __s:Iterable<T?0>) -> (return:NoneType))',
    },
    'union': {
        r'((self:set<T?0> /\ __va_s:Iterable<T?s>) -> (return:set<T?0+T?s>))',
        r'((self:frozenset<T?co> /\ __va_s:Iterable<T?s>) -> (return:frozenset<T?co+T?s>))',
    },
    'update': {
        r'((self:set<T?0> /\ __va_s:Iterable<T?0>) -> (return:NoneType))',
    },
    '__iand__': {
        r'((self:set<T?0> /\ __value:set<top>) -> (return:set<T?0>))',
    },
    '__ior__': {
        r'((self:set<T?0> /\ __value:set<T?0>) -> (return:set<T?0>))',
    },
    '__isub__': {
        r'((self:set<T?0> /\ __value:set<top>) -> (return:set<T?0>))',
    },
    '__ixor__': {
        r'((self:set<T?0> /\ __value:set<T?0>) -> (return:set<T?0>))',
    },
    'start': {
        r'((self:range<int>) -> (return:int))',
    },
    'stop': {
        r'((self:range<int>) -> (return:int))',
    },
    'step': {
        r'((self:range<int>) -> (return:int))',
    },
    '__set__': {
        r'((self:property /\ __instance:top /\ __value:top) -> (return:NoneType))',
    },
    '__delete__': {
        r'((self:property /\ __instance:top) -> (return:NoneType))',
    },
    '__next__': {
        r'((self:reversed<T?0>) -> (return:T?0))',
        r'((self:filter<T?0>) -> (return:T?0))',
        r'((self:zip<T?co>) -> (return:T?co))',
        r'((self:map<T?s>) -> (return:T?s))',
    },
    '__length_hint__': {
        r'((self:reversed<T?0>) -> (return:int))',
    },
    '__setstate__': {
        r'((self:BaseException /\ __state:NoneType+dict<str, top>) -> (return:NoneType))',
    },
    'abs': {
        r'((__x:SupportsAbs<T?0>) -> (return:T?0))',
    },
    'all': {
        r'((__iterable:Iterable<top>) -> (return:bool))',
    },
    'any': {
        r'((__iterable:Iterable<top>) -> (return:bool))',
    },
    'ascii': {
        r'((__obj:top) -> (return:str))',
    },
    'bin': {
        r'((__number:int+SupportsIndex) -> (return:str))',
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
        r'((__o:top) -> (return:list<str>))',
    },
    'divmod': {
        r'((__x:SupportsDivMod<T?co+T?contra> /\ __y:T?contra) -> (return:T?co))',
        r'((__x:T?contra /\ __y:SupportsRDivMod<T?co+T?contra>) -> (return:T?co))',
    },
    'getattr': {
        r'((__o:top /\ name:str /\ __default:dict<top, top>) -> (return:dict<top, top>+top))',
        r'((__o:top /\ __name:str /\ __default:bool) -> (return:bool+top))',
        r'((__o:top /\ __name:str /\ __default:T?0) -> (return:T?0+top))',
        r'((__o:top /\ __name:str /\ __default:NoneType) -> (return:NoneType+top))',
        r'((__o:top /\ name:str /\ __default:list<top>) -> (return:top+list<top>))',
    },
    'globals': {
        r'(() -> (return:dict<str, top>))',
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
    'iter': {
        r'((__iterable:Iterable<SupportsNext>) -> (return:SupportsNext))',
        r'((__iterable:GetItemIterable<T?0>) -> (return:Iterator<T?0>))',
    },
    'len': {
        r'((__obj:SupportsLen) -> (return:int))',
    },
    'license': {
        r'(() -> (return:NoneType))',
    },
    'locals': {
        r'(() -> (return:dict<str, top>))',
    },
    'max': {
        r'((__iterable:Iterable<SupportsRichComparisonT> /\ __ko_key:NoneType /\ __ko_default:T?0) -> (return:T?0+SupportsRichComparisonT))',
        r'((__arg1:SupportsRichComparisonT /\ __arg2:SupportsRichComparisonT /\ __va__args:SupportsRichComparisonT /\ __ko_key:NoneType) -> (return:SupportsRichComparisonT))',
        r'((__iterable:Iterable<SupportsRichComparisonT> /\ __ko_key:NoneType) -> (return:SupportsRichComparisonT))',
    },
    'min': {
        r'((__iterable:Iterable<SupportsRichComparisonT> /\ __ko_key:NoneType /\ __ko_default:T?0) -> (return:T?0+SupportsRichComparisonT))',
        r'((__arg1:SupportsRichComparisonT /\ __arg2:SupportsRichComparisonT /\ __va__args:SupportsRichComparisonT /\ __ko_key:NoneType) -> (return:SupportsRichComparisonT))',
        r'((__iterable:Iterable<SupportsRichComparisonT> /\ __ko_key:NoneType) -> (return:SupportsRichComparisonT))',
    },
    'next': {
        r'((__i:SupportsNext<T?0>) -> (return:T?0))',
        r'((__i:SupportsNext<T?0> /\ __default:T?V) -> (return:T?0+T?V))',
    },
    'oct': {
        r'((__number:int+SupportsIndex) -> (return:str))',
    },
    'ord': {
        r'((__c:bytearray+str+bytes) -> (return:int))',
    },
    'print': {
        r'((__va_values:top /\ __ko_sep:NoneType+str /\ __ko_end:NoneType+str /\ __ko_file:NoneType+SupportsWrite<str> /\ __ko_flush:bool) -> (return:NoneType))',
    },
    'repr': {
        r'((__obj:top) -> (return:str))',
    },
    'round': {
        r'((number:SupportsRound<T?0> /\ ndigits:SupportsIndex) -> (return:T?0))',
        r'((number:SupportsRound<T?0> /\ ndigits:NoneType) -> (return:T?0))',
    },
    'setattr': {
        r'((__obj:top /\ __name:str /\ __value:top) -> (return:NoneType))',
    },
    'sorted': {
        r'((__iterable:Iterable<SupportsRichComparisonT> /\ __ko_key:NoneType /\ __ko_reverse:bool) -> (return:list<SupportsRichComparisonT>))',
    },
    'sum': {
        r'((__iterable:Iterable<int>) -> (return:int))',
    },
    'vars': {
        r'((__object:top) -> (return:dict<str, top>))',
    },

}
