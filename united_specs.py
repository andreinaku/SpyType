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
        r'((self:top /\ __type:type < top >) -> (return:NoneType))',
        r'((self:top) -> (return:type < top >))',
    },
    '__init__': {
        r'((self:map < T?4 > /\ __func:Callable /\ __iter1:Iterable < _T1 > /\ __iter2:Iterable < _T2 > /\ __iter3:Iterable < _T3 > /\ __iter4:Iterable < _T4 > /\ __iter5:Iterable < _T5 >) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __kw_kwargs:T?2) -> (return:NoneType))',
        r'((self:reversed < T?0 > /\ __sequence:Reversible < T?0 >) -> (return:NoneType))',
        r'((self:top) -> (return:NoneType))',
        r'((self:set < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __iterable:Iterable < tuple < T?2 + str > > /\ __kw_kwargs:T?2) -> (return:NoneType))',
        r'((self:map < T?4 > /\ __func:Callable /\ __iter1:Iterable < _T1 > /\ __iter2:Iterable < _T2 >) -> (return:NoneType))',
        r'((self:reversed < T?0 > /\ __sequence:memoryview < T?0 > + dict < T?0 > + list < T?0 > + bytearray + tuple < T?0 > + str + range + bytes) -> (return:NoneType))',
        r'((self:classmethod < T?6 + T?0 + T?5 > /\ __f:Callable) -> (return:NoneType))',
        r'((self:filter < T?0 > /\ __function:NoneType /\ __iterable:Iterable < NoneType + T?0 >) -> (return:NoneType))',
        r'((self:range /\ __start:SupportsIndex /\ __stop:SupportsIndex /\ __d___step:SupportsIndex) -> (return:NoneType))',
        r'((self:BaseException /\ __va_args:top) -> (return:NoneType))',
        r'((self:map < T?4 > /\ __func:Callable /\ __iter1:Iterable < _T1 > /\ __iter2:Iterable < _T2 > /\ __iter3:Iterable < _T3 > /\ __iter4:Iterable < _T4 >) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __iterable:Iterable < list < str > >) -> (return:NoneType))',
        r'((self:staticmethod < T?6 + T?5 > /\ __f:Callable) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
        r'((self:slice /\ __start:top /\ __stop:top /\ __d___step:top) -> (return:NoneType))',
        r'((self:property /\ __d_fget:NoneType + Callable /\ __d_fset:NoneType + Callable /\ __d_fdel:NoneType + Callable /\ __d_doc:NoneType + str) -> (return:NoneType))',
        r'((self:UnicodeTranslateError /\ __object:str /\ __start:int /\ __end:int /\ __reason:str) -> (return:NoneType))',
        r'((self:type /\ __o:top) -> (return:NoneType))',
        r'((self:map < T?4 > /\ __func:Callable /\ __iter1:Iterable < _T1 >) -> (return:NoneType))',
        r'((self:range /\ __stop:SupportsIndex) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 >) -> (return:NoneType))',
        r'((self:super /\ __t:top /\ __obj:top) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __iterable:Iterable < tuple < T?1 + T?2 > >) -> (return:NoneType))',
        r'((self:bytearray /\ __string:str /\ encoding:str /\ __d_errors:str) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __map:dict < T?1, T?2 >) -> (return:NoneType))',
        r'((self:bytearray /\ __ints:memoryview + bytearray + SupportsIndex + Iterable < SupportsIndex > + bytes) -> (return:NoneType))',
        r'((self:bytearray) -> (return:NoneType))',
        r'((self:slice /\ __stop:top) -> (return:NoneType))',
        r'((self:map < T?4 > /\ __func:Callable /\ __iter1:Iterable < top > /\ __iter2:Iterable < top > /\ __iter3:Iterable < top > /\ __iter4:Iterable < top > /\ __iter5:Iterable < top > /\ __iter6:Iterable < top > /\ __va_iterables:Iterable < top >) -> (return:NoneType))',
        r'((self:filter < T?0 > /\ __function:Callable /\ __iterable:Iterable < T?0 >) -> (return:NoneType))',
        r'((self:memoryview < int > /\ obj:bytes + bytearray + memoryview) -> (return:NoneType))',
        r'((self:set < T?0 >) -> (return:NoneType))',
        r'((self:super /\ __t:top) -> (return:NoneType))',
        r'((self:UnicodeDecodeError /\ __encoding:str /\ __object:bytes + bytearray + memoryview /\ __start:int /\ __end:int /\ __reason:str) -> (return:NoneType))',
        r'((self:filter < T?0 > /\ __function:Callable /\ __iterable:Iterable < T?4 >) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __map:dict < str, T?2 > /\ __kw_kwargs:T?2) -> (return:NoneType))',
        r'((self:type /\ __name:str /\ __bases:tuple < type + ellipsis > /\ __dict:dict < str, top > /\ __kw_kwds:top) -> (return:NoneType))',
        r'((self:map < T?4 > /\ __func:Callable /\ __iter1:Iterable < _T1 > /\ __iter2:Iterable < _T2 > /\ __iter3:Iterable < _T3 >) -> (return:NoneType))',
        r'((self:UnicodeEncodeError /\ __encoding:str /\ __object:str /\ __start:int /\ __end:int /\ __reason:str) -> (return:NoneType))',
        r'((self:enumerate < tuple < int + T?0 > > /\ iterable:Iterable < T?0 > /\ __d_start:int) -> (return:NoneType))',
        r'((self:list < T?0 >) -> (return:NoneType))',
        r'((self:ImportError /\ __va_args:top /\ __ko___d_name:NoneType + str /\ __ko___d_path:NoneType + str) -> (return:NoneType))',
        r'((self:super) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __iterable:Iterable < list < bytes > >) -> (return:NoneType))',
    },
    '__new__': {
        r'((cls:str /\ __d_object:top) -> (return:str))',
        r'((cls:frozenset < T?3 > /\ __iterable:Iterable < T?3 >) -> (return:frozenset < T?3 >))',
        r'((cls:int /\ __x:bytearray + bytes + str /\ base:SupportsIndex) -> (return:int))',
        r'((cls:bytes /\ __o:memoryview + bytearray + SupportsIndex + SupportsBytes + Iterable < SupportsIndex > + bytes) -> (return:bytes))',
        r'((cls:float /\ __d___x:memoryview + SupportsFloat + bytearray + SupportsIndex + str + bytes) -> (return:float))',
        r'((cls:frozenset < T?3 >) -> (return:frozenset < T?3 >))',
        r'((cls:type /\ __name:str /\ __bases:tuple < type + ellipsis > /\ __namespace:dict < str, top > /\ __kw_kwds:top) -> (return:type))',
        r'((cls:top) -> (return:top))',
        r'((cls:bytes /\ __string:str /\ encoding:str /\ __d_errors:str) -> (return:bytes))',
        r'((cls:bytes) -> (return:bytes))',
        r'((cls:tuple < T?3 > /\ __d___iterable:Iterable < T?3 >) -> (return:tuple < T?3 >))',
        r'((cls:int /\ __d___x:memoryview + SupportsInt + bytearray + int + SupportsIndex + str + float + bytes) -> (return:int))',
        r'((cls:type /\ __o:top) -> (return:type))',
        r'((cls:str /\ object:bytes + bytearray + memoryview /\ __d_encoding:str /\ __d_errors:str) -> (return:str))',
        r'((cls:bool /\ __d___o:top) -> (return:bool))',
        r'((cls:dict < T?1, T?2 > /\ __va_args:top /\ __kw_kwargs:top) -> (return:dict < T?1, T?2 >))',
    },
    '__setattr__': {
        r'((self:top /\ __name:str /\ __value:top) -> (return:NoneType))',
    },
    '__delattr__': {
        r'((self:top /\ __name:str) -> (return:NoneType))',
    },
    '__eq__': {
        r'((self:bytearray /\ __value:top) -> (return:bool))',
        r'((self:range /\ __value:top) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:top) -> (return:bool))',
        r'((self:float /\ __value:top) -> (return:bool))',
        r'((self:str /\ __value:top) -> (return:bool))',
        r'((self:complex /\ __value:top) -> (return:bool))',
        r'((self:int /\ __value:top) -> (return:bool))',
        r'((self:slice /\ __value:top) -> (return:bool))',
        r'((self:dict < T?1, T?2 > /\ __value:top) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:top) -> (return:bool))',
        r'((self:top /\ __value:top) -> (return:bool))',
        r'((self:memoryview < int > /\ __value:top) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:top) -> (return:bool))',
        r'((self:bytes /\ __value:top) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:top) -> (return:bool))',
    },
    '__ne__': {
        r'((self:bytearray /\ __value:top) -> (return:bool))',
        r'((self:float /\ __value:top) -> (return:bool))',
        r'((self:str /\ __value:top) -> (return:bool))',
        r'((self:int /\ __value:top) -> (return:bool))',
        r'((self:top /\ __value:top) -> (return:bool))',
        r'((self:bytes /\ __value:top) -> (return:bool))',
        r'((self:complex /\ __value:top) -> (return:bool))',
    },
    '__str__': {
        r'((self:top) -> (return:str))',
    },
    '__repr__': {
        r'((self:top) -> (return:str))',
    },
    '__hash__': {
        r'((self:float) -> (return:int))',
        r'((self:top) -> (return:int))',
        r'((self:int) -> (return:int))',
        r'((self:memoryview < int >) -> (return:int))',
        r'((self:str) -> (return:int))',
        r'((self:frozenset < T?3 >) -> (return:int))',
        r'((self:tuple < T?3 >) -> (return:int))',
        r'((self:bytes) -> (return:int))',
        r'((self:range) -> (return:int))',
        r'((self:complex) -> (return:int))',
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
        r'((self:top) -> (return:tuple < top + ellipsis > + str))',
    },
    '__dir__': {
        r'((self:top) -> (return:Iterable < str >))',
    },
    '__init_subclass__': {
        r'((cls:top) -> (return:NoneType))',
    },
    '__subclasshook__': {
        r'((cls:top /\ __subclass:type) -> (return:bool))',
    },
    '__func__': {
        r'((self:staticmethod < T?6 + T?5 >) -> (return:Callable))',
        r'((self:classmethod < T?6 + T?0 + T?5 >) -> (return:Callable))',
    },
    '__isabstractmethod__': {
        r'((self:classmethod < T?6 + T?0 + T?5 >) -> (return:bool))',
        r'((self:staticmethod < T?6 + T?5 >) -> (return:bool))',
    },
    '__get__': {
        r'((self:tuple < T?3 > /\ __instance:top /\ __d___owner:type + NoneType) -> (return:top))',
        r'((self:classmethod < T?6 + T?0 + T?5 > /\ __instance:NoneType /\ __owner:type < T?0 >) -> (return:Callable))',
        r'((self:staticmethod < T?6 + T?5 > /\ __instance:T?0 /\ __d___owner:NoneType + type < T?0 >) -> (return:Callable))',
        r'((self:property /\ __instance:top /\ __d___owner:type + NoneType) -> (return:top))',
        r'((self:staticmethod < T?6 + T?5 > /\ __instance:NoneType /\ __owner:type) -> (return:Callable))',
        r'((self:classmethod < T?6 + T?0 + T?5 > /\ __instance:T?0 /\ __d___owner:NoneType + type < T?0 >) -> (return:Callable))',
    },
    '__base__': {
        r'((self:type) -> (return:type))',
    },
    '__basicsize__': {
        r'((self:type) -> (return:int))',
    },
    '__dict__': {
        r'((self:type) -> (return:mappingproxy < top + str >))',
    },
    '__dictoffset__': {
        r'((self:type) -> (return:int))',
    },
    '__flags__': {
        r'((self:type) -> (return:int))',
    },
    '__itemsize__': {
        r'((self:type) -> (return:int))',
    },
    '__mro__': {
        r'((self:type) -> (return:tuple < type + ellipsis >))',
    },
    '__text_signature__': {
        r'((self:type) -> (return:NoneType + str))',
    },
    '__weakrefoffset__': {
        r'((self:type) -> (return:int))',
    },
    '__call__': {
        r'((self:type /\ __va_args:top /\ __kw_kwds:top) -> (return:top))',
    },
    '__subclasses__': {
        r'((self:type) -> (return:list < type >))',
    },
    'mro': {
        r'((self:type) -> (return:list < type >))',
    },
    '__instancecheck__': {
        r'((self:type /\ __instance:top) -> (return:bool))',
    },
    '__subclasscheck__': {
        r'((self:type /\ __subclass:type) -> (return:bool))',
    },
    'real': {
        r'((self:float) -> (return:float))',
        r'((self:complex) -> (return:float))',
        r'((self:int) -> (return:int))',
    },
    'imag': {
        r'((self:float) -> (return:float))',
        r'((self:complex) -> (return:float))',
        r'((self:int) -> (return:int))',
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
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:list < T?0 >))',
        r'((self:tuple < T?3 > /\ __value:tuple < ellipsis + T?0 >) -> (return:tuple < T?3 + ellipsis + T?0 >))',
        r'((self:bytes /\ __value:bytes + bytearray + memoryview) -> (return:bytes))',
        r'((self:list < T?0 > /\ __value:list < T?4 >) -> (return:list < T?4 + T?0 >))',
        r'((self:bytearray /\ __value:bytes + bytearray + memoryview) -> (return:bytearray))',
        r'((self:str /\ __value:str) -> (return:str))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 + ellipsis >) -> (return:tuple < T?3 + ellipsis >))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
    },
    '__sub__': {
        r'((self:set < T?0 > /\ __value:set < NoneType + T?0 >) -> (return:set < T?0 >))',
        r'((self:frozenset < T?3 > /\ __value:set < T?3 >) -> (return:frozenset < T?3 >))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
    },
    '__mul__': {
        r'((self:bytes /\ __value:SupportsIndex) -> (return:bytes))',
        r'((self:str /\ __value:SupportsIndex) -> (return:str))',
        r'((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
        r'((self:tuple < T?3 > /\ __value:SupportsIndex) -> (return:tuple < T?3 + ellipsis >))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
    },
    '__floordiv__': {
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__truediv__': {
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:int /\ __value:int) -> (return:float))',
    },
    '__mod__': {
        r'((self:bytes /\ __value:top) -> (return:bytes))',
        r'((self:str /\ __value:tuple < ellipsis + str > + str) -> (return:str))',
        r'((self:bytearray /\ __value:top) -> (return:bytes))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:str /\ __value:top) -> (return:str))',
    },
    '__divmod__': {
        r'((self:int /\ __value:int) -> (return:tuple < int >))',
        r'((self:float /\ __value:float) -> (return:tuple < float >))',
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
        r'((self:bytes /\ __value:SupportsIndex) -> (return:bytes))',
        r'((self:str /\ __value:SupportsIndex) -> (return:str))',
        r'((self:list < T?0 > /\ __value:SupportsIndex) -> (return:list < T?0 >))',
        r'((self:tuple < T?3 > /\ __value:SupportsIndex) -> (return:tuple < T?3 + ellipsis >))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
    },
    '__rfloordiv__': {
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rtruediv__': {
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:complex /\ __value:complex) -> (return:complex))',
        r'((self:int /\ __value:int) -> (return:float))',
    },
    '__rmod__': {
        r'((self:float /\ __value:float) -> (return:float))',
        r'((self:int /\ __value:int) -> (return:int))',
    },
    '__rdivmod__': {
        r'((self:int /\ __value:int) -> (return:tuple < int >))',
        r'((self:float /\ __value:float) -> (return:tuple < float >))',
    },
    '__pow__': {
        r'((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:top))',
        r'((self:complex /\ __value:complex /\ __d___mod:NoneType) -> (return:complex))',
        r'((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
        r'((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:int))',
        r'((self:float /\ __value:float /\ __d___mod:NoneType) -> (return:top))',
        r'((self:int /\ __x:int) -> (return:int))',
        r'((self:int /\ __value:int /\ __mod:int) -> (return:int))',
        r'((self:int /\ __value:int /\ __mod:NoneType) -> (return:int))',
        r'((self:int /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
    },
    '__rpow__': {
        r'((self:complex /\ __value:complex /\ __d___mod:NoneType) -> (return:complex))',
        r'((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:complex))',
        r'((self:float /\ __value:int /\ __d___mod:NoneType) -> (return:float))',
        r'((self:float /\ __value:float /\ __d___mod:NoneType) -> (return:top))',
        r'((self:int /\ __value:int /\ __d___mod:NoneType + int) -> (return:top))',
    },
    '__and__': {
        r'((self:frozenset < T?3 > /\ __value:set < T?3 >) -> (return:frozenset < T?3 >))',
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:set < T?0 >))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
    },
    '__or__': {
        r'((self:set < T?0 > /\ __value:set < T?4 >) -> (return:set < T?4 + T?0 >))',
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:frozenset < T?3 > /\ __value:set < T?4 >) -> (return:frozenset < T?3 + T?4 >))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
    },
    '__xor__': {
        r'((self:set < T?0 > /\ __value:set < T?4 >) -> (return:set < T?4 + T?0 >))',
        r'((self:bool /\ __value:int) -> (return:int))',
        r'((self:int /\ __value:int) -> (return:int))',
        r'((self:frozenset < T?3 > /\ __value:set < T?4 >) -> (return:frozenset < T?3 + T?4 >))',
        r'((self:bool /\ __value:bool) -> (return:bool))',
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
        r'((self:float /\ __ndigits:SupportsIndex) -> (return:float))',
        r'((self:int /\ __d___ndigits:SupportsIndex) -> (return:int))',
        r'((self:float /\ __d___ndigits:NoneType) -> (return:int))',
    },
    '__getnewargs__': {
        r'((self:float) -> (return:tuple < float >))',
        r'((self:bytes) -> (return:tuple < bytes >))',
        r'((self:bool) -> (return:tuple < int >))',
        r'((self:int) -> (return:tuple < int >))',
        r'((self:str) -> (return:tuple < str >))',
    },
    '__lt__': {
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 + ellipsis >) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytes + bytearray + memoryview) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
    },
    '__le__': {
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 + ellipsis >) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytes + bytearray + memoryview) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
    },
    '__gt__': {
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 + ellipsis >) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytes + bytearray + memoryview) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
    },
    '__ge__': {
        r'((self:int /\ __value:int) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __value:set < top >) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __value:tuple < T?3 + ellipsis >) -> (return:bool))',
        r'((self:list < T?0 > /\ __value:list < T?0 >) -> (return:bool))',
        r'((self:set < T?0 > /\ __value:set < top >) -> (return:bool))',
        r'((self:bytearray /\ __value:bytes + bytearray + memoryview) -> (return:bool))',
        r'((self:str /\ __value:str) -> (return:bool))',
        r'((self:bytes /\ __value:bytes) -> (return:bool))',
        r'((self:float /\ __value:float) -> (return:bool))',
    },
    '__float__': {
        r'((self:int) -> (return:float))',
        r'((self:float) -> (return:float))',
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
        r'((cls:bytes /\ __string:str) -> (return:bytes))',
        r'((cls:float /\ __string:str) -> (return:float))',
        r'((cls:bytearray /\ __string:str) -> (return:bytearray))',
    },
    'capitalize': {
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:bytes) -> (return:bytes))',
        r'((self:str) -> (return:str))',
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
        r'((self:range /\ __value:int) -> (return:int))',
        r'((self:list < T?0 > /\ __value:T?0) -> (return:int))',
        r'((self:bytearray /\ __sub:bytes + SupportsIndex + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:str /\ x:str /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:tuple < T?3 > /\ __value:top) -> (return:int))',
        r'((self:bytes /\ __sub:bytes + SupportsIndex + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
    },
    'encode': {
        r'((self:str /\ __d_encoding:str /\ __d_errors:str) -> (return:bytes))',
    },
    'endswith': {
        r'((self:bytes /\ __suffix:tuple < ellipsis + bytes + bytearray + memoryview > + bytes + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:bool))',
        r'((self:str /\ __suffix:tuple < ellipsis + str > + str /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:bool))',
        r'((self:bytearray /\ __suffix:tuple < ellipsis + bytes + bytearray + memoryview > + bytes + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:bool))',
    },
    'find': {
        r'((self:str /\ __sub:str /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __sub:bytes + SupportsIndex + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytes /\ __sub:bytes + SupportsIndex + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
    },
    'format': {
        r'((self:str /\ __va_args:str /\ __kw_kwargs:str) -> (return:str))',
        r'((self:memoryview < int >) -> (return:str))',
        r'((__value:top /\ __d___format_spec:str) -> (return:str))',
        r'((self:str /\ __va_args:top /\ __kw_kwargs:top) -> (return:str))',
    },
    'format_map': {
        r'((self:str /\ map:dict < str, int >) -> (return:str))',
    },
    'index': {
        r'((self:list < T?0 > /\ __value:T?0 /\ __d___start:SupportsIndex /\ __d___stop:SupportsIndex) -> (return:int))',
        r'((self:range /\ __value:int) -> (return:int))',
        r'((self:str /\ __sub:str /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:tuple < T?3 > /\ __value:top /\ __d___start:SupportsIndex /\ __d___stop:SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __sub:bytes + SupportsIndex + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytes /\ __sub:bytes + SupportsIndex + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
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
        r'((self:bytes /\ __iterable_of_bytes:Iterable < bytes + bytearray + memoryview >) -> (return:bytes))',
        r'((self:bytearray /\ __iterable_of_bytes:Iterable < bytes + bytearray + memoryview >) -> (return:bytearray))',
        r'((self:str /\ __iterable:Iterable < str >) -> (return:str))',
    },
    'ljust': {
        r'((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytes + bytearray) -> (return:bytearray))',
        r'((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytes + bytearray) -> (return:bytes))',
        r'((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
    },
    'lower': {
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:bytes) -> (return:bytes))',
        r'((self:str) -> (return:str))',
    },
    'lstrip': {
        r'((self:bytes /\ __d___bytes:NoneType + bytes + bytearray + memoryview) -> (return:bytes))',
        r'((self:str /\ __d___chars:NoneType + str) -> (return:str))',
        r'((self:bytearray /\ __d___bytes:NoneType + bytes + bytearray + memoryview) -> (return:bytearray))',
    },
    'partition': {
        r'((self:bytes /\ __sep:bytes + bytearray + memoryview) -> (return:tuple < bytes >))',
        r'((self:bytearray /\ __sep:bytes + bytearray + memoryview) -> (return:tuple < bytearray >))',
        r'((self:str /\ __sep:str) -> (return:tuple < str >))',
    },
    'replace': {
        r'((self:bytearray /\ __old:bytes + bytearray + memoryview /\ __new:bytes + bytearray + memoryview /\ __d___count:SupportsIndex) -> (return:bytearray))',
        r'((self:bytes /\ __old:bytes + bytearray + memoryview /\ __new:bytes + bytearray + memoryview /\ __d___count:SupportsIndex) -> (return:bytes))',
        r'((self:str /\ __old:str /\ __new:str /\ __d___count:SupportsIndex) -> (return:str))',
    },
    'rfind': {
        r'((self:str /\ __sub:str /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __sub:bytes + SupportsIndex + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytes /\ __sub:bytes + SupportsIndex + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
    },
    'rindex': {
        r'((self:str /\ __sub:str /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __sub:bytes + SupportsIndex + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
        r'((self:bytes /\ __sub:bytes + SupportsIndex + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:int))',
    },
    'rjust': {
        r'((self:bytearray /\ __width:SupportsIndex /\ __d___fillchar:bytes + bytearray) -> (return:bytearray))',
        r'((self:bytes /\ __width:SupportsIndex /\ __d___fillchar:bytes + bytearray) -> (return:bytes))',
        r'((self:str /\ __width:SupportsIndex /\ __d___fillchar:str) -> (return:str))',
    },
    'rpartition': {
        r'((self:bytes /\ __sep:bytes + bytearray + memoryview) -> (return:tuple < bytes >))',
        r'((self:bytearray /\ __sep:bytes + bytearray + memoryview) -> (return:tuple < bytearray >))',
        r'((self:str /\ __sep:str) -> (return:tuple < str >))',
    },
    'rsplit': {
        r'((self:str /\ __d_sep:NoneType + str /\ __d_maxsplit:SupportsIndex) -> (return:list < str >))',
        r'((self:bytes /\ __d_sep:NoneType + bytes + bytearray + memoryview /\ __d_maxsplit:SupportsIndex) -> (return:list < bytes >))',
        r'((self:bytearray /\ __d_sep:NoneType + bytes + bytearray + memoryview /\ __d_maxsplit:SupportsIndex) -> (return:list < bytearray >))',
    },
    'rstrip': {
        r'((self:bytes /\ __d___bytes:NoneType + bytes + bytearray + memoryview) -> (return:bytes))',
        r'((self:str /\ __d___chars:NoneType + str) -> (return:str))',
        r'((self:bytearray /\ __d___bytes:NoneType + bytes + bytearray + memoryview) -> (return:bytearray))',
    },
    'split': {
        r'((self:str /\ __d_sep:NoneType + str /\ __d_maxsplit:SupportsIndex) -> (return:list < str >))',
        r'((self:bytes /\ __d_sep:NoneType + bytes + bytearray + memoryview /\ __d_maxsplit:SupportsIndex) -> (return:list < bytes >))',
        r'((self:bytearray /\ __d_sep:NoneType + bytes + bytearray + memoryview /\ __d_maxsplit:SupportsIndex) -> (return:list < bytearray >))',
    },
    'splitlines': {
        r'((self:str /\ __d_keepends:bool) -> (return:list < str >))',
        r'((self:bytearray /\ __d_keepends:bool) -> (return:list < bytearray >))',
        r'((self:bytes /\ __d_keepends:bool) -> (return:list < bytes >))',
    },
    'startswith': {
        r'((self:bytearray /\ __prefix:tuple < ellipsis + bytes + bytearray + memoryview > + bytes + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:bool))',
        r'((self:bytes /\ __prefix:tuple < ellipsis + bytes + bytearray + memoryview > + bytes + bytearray + memoryview /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:bool))',
        r'((self:str /\ __prefix:tuple < ellipsis + str > + str /\ __d___start:NoneType + SupportsIndex /\ __d___end:NoneType + SupportsIndex) -> (return:bool))',
    },
    'strip': {
        r'((self:bytes /\ __d___bytes:NoneType + bytes + bytearray + memoryview) -> (return:bytes))',
        r'((self:str /\ __d___chars:NoneType + str) -> (return:str))',
        r'((self:bytearray /\ __d___bytes:NoneType + bytes + bytearray + memoryview) -> (return:bytearray))',
    },
    'swapcase': {
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:bytes) -> (return:bytes))',
        r'((self:str) -> (return:str))',
    },
    'title': {
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:bytes) -> (return:bytes))',
        r'((self:str) -> (return:str))',
    },
    'translate': {
        r'((self:bytearray /\ __table:NoneType + bytes + bytearray + memoryview /\ __d_delete:bytes) -> (return:bytearray))',
        r'((self:bytes /\ __table:NoneType + bytes + bytearray + memoryview /\ __d_delete:bytes) -> (return:bytes))',
        r'((self:str /\ __table:dict < int, int + str >) -> (return:str))',
    },
    'upper': {
        r'((self:bytearray) -> (return:bytearray))',
        r'((self:bytes) -> (return:bytes))',
        r'((self:str) -> (return:str))',
    },
    'zfill': {
        r'((self:bytes /\ __width:SupportsIndex) -> (return:bytes))',
        r'((self:bytearray /\ __width:SupportsIndex) -> (return:bytearray))',
        r'((self:str /\ __width:SupportsIndex) -> (return:str))',
    },
    'maketrans': {
        r'((__frm:bytes + bytearray + memoryview /\ __to:bytes + bytearray + memoryview) -> (return:bytes))',
        r'((__x:str /\ __y:str /\ __z:str) -> (return:dict < int, NoneType + int >))',
        r'((__x:dict < int, T?0 > + dict < int + str, T?0 > + dict < str, T?0 >) -> (return:dict < int, T?0 >))',
        r'((__x:str /\ __y:str) -> (return:dict < int, int >))',
    },
    '__contains__': {
        r'((self:str /\ __key:str) -> (return:bool))',
        r'((self:frozenset < T?3 > /\ __o:top) -> (return:bool))',
        r'((self:range /\ __key:top) -> (return:bool))',
        r'((self:bytearray /\ __key:bytes + SupportsIndex + bytearray + memoryview) -> (return:bool))',
        r'((self:tuple < T?3 > /\ __key:top) -> (return:bool))',
        r'((self:list < T?0 > /\ __key:top) -> (return:bool))',
        r'((self:bytes /\ __key:bytes + SupportsIndex + bytearray + memoryview) -> (return:bool))',
        r'((self:memoryview < int > /\ __x:top) -> (return:bool))',
        r'((self:set < T?0 > /\ __o:top) -> (return:bool))',
    },
    '__getitem__': {
        r'((self:bytearray /\ __key:slice) -> (return:bytearray))',
        r'((self:range /\ __key:slice) -> (return:range))',
        r'((self:list < T?0 > /\ __i:SupportsIndex) -> (return:T?0))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:T?2))',
        r'((self:memoryview < int > /\ __key:slice) -> (return:memoryview))',
        r'((self:tuple < T?3 > /\ __key:slice) -> (return:tuple < T?3 + ellipsis >))',
        r'((self:tuple < T?3 > /\ __key:SupportsIndex) -> (return:T?3))',
        r'((self:bytes /\ __key:slice) -> (return:bytes))',
        r'((self:bytes /\ __key:SupportsIndex) -> (return:int))',
        r'((self:str /\ __key:slice + SupportsIndex) -> (return:str))',
        r'((self:memoryview < int > /\ __key:SupportsIndex) -> (return:int))',
        r'((self:bytearray /\ __key:SupportsIndex) -> (return:int))',
        r'((self:list < T?0 > /\ __s:slice) -> (return:list < T?0 >))',
        r'((self:range /\ __key:SupportsIndex) -> (return:int))',
    },
    '__iter__': {
        r'((self:enumerate < tuple < int + T?0 > >) -> (return:enumerate < tuple < int + T?0 > >))',
        r'((self:filter < T?0 >) -> (return:filter < T?0 >))',
        r'((self:dict < T?1, T?2 >) -> (return:Iterator < T?1 >))',
        r'((self:range) -> (return:Iterator < int >))',
        r'((self:reversed < T?0 >) -> (return:reversed < T?0 >))',
        r'((self:map < T?4 >) -> (return:map < T?4 >))',
        r'((self:frozenset < T?3 >) -> (return:Iterator < T?3 >))',
        r'((self:set < T?0 >) -> (return:Iterator < T?0 >))',
        r'((self:memoryview < int >) -> (return:Iterator < int >))',
        r'((self:tuple < T?3 >) -> (return:Iterator < T?3 >))',
        r'((self:list < T?0 >) -> (return:Iterator < T?0 >))',
        r'((self:str) -> (return:Iterator < str >))',
        r'((self:bytearray) -> (return:Iterator < int >))',
        r'((self:zip < T?3 >) -> (return:zip < T?3 >))',
        r'((self:bytes) -> (return:Iterator < int >))',
    },
    '__len__': {
        r'((self:memoryview < int >) -> (return:int))',
        r'((self:str) -> (return:int))',
        r'((self:bytearray) -> (return:int))',
        r'((self:frozenset < T?3 >) -> (return:int))',
        r'((self:list < T?0 >) -> (return:int))',
        r'((self:set < T?0 >) -> (return:int))',
        r'((self:tuple < T?3 >) -> (return:int))',
        r'((self:bytes) -> (return:int))',
        r'((self:range) -> (return:int))',
        r'((self:dict < T?1, T?2 >) -> (return:int))',
    },
    'decode': {
        r'((self:bytes /\ __d_encoding:str /\ __d_errors:str) -> (return:str))',
        r'((self:bytearray /\ __d_encoding:str /\ __d_errors:str) -> (return:str))',
    },
    '__buffer__': {
        r'((self:bytes /\ __flags:int) -> (return:memoryview))',
        r'((self:bytearray /\ __flags:int) -> (return:memoryview))',
        r'((self:memoryview < int > /\ __flags:int) -> (return:memoryview))',
    },
    'append': {
        r'((self:list < T?0 > /\ __object:T?1) -> (self:list < T?1 + T?0 > /\ return:NoneType))',
        r'((self:list < bot > /\ __object:T?0) -> (self:list < T?0 > /\ return:NoneType))',
        r'((self:bytearray /\ __item:SupportsIndex) -> (return:NoneType))',
    },
    'copy': {
        r'((self:list < T?0 >) -> (return:list < T?0 >))',
        r'((self:dict < T?1, T?2 >) -> (return:dict < T?1, T?2 >))',
        r'((self:frozenset < T?3 >) -> (return:frozenset < T?3 >))',
        r'((self:set < T?0 >) -> (return:set < T?0 >))',
        r'((self:bytearray) -> (return:bytearray))',
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
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:T?2))',
        r'((self:list < T?0 > /\ __d___index:SupportsIndex) -> (return:T?0))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?0) -> (return:T?0 + T?2))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?2) -> (return:T?2))',
    },
    'remove': {
        r'((self:bytearray /\ __value:int) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __value:T?0) -> (return:NoneType))',
        r'((self:set < T?0 > /\ __element:T?0) -> (return:NoneType))',
    },
    '__setitem__': {
        r'((self:list < T?0 > /\ __key:slice /\ __value:Iterable < T?0 >) -> (return:NoneType))',
        r'((self:bytearray /\ __key:slice /\ __value:bytes + Iterable < SupportsIndex >) -> (return:NoneType))',
        r'((self:memoryview < int > /\ __key:SupportsIndex /\ __value:SupportsIndex) -> (return:NoneType))',
        r'((self:memoryview < int > /\ __key:slice /\ __value:bytes + bytearray + memoryview) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __key:SupportsIndex /\ __value:T?0) -> (return:NoneType))',
        r'((self:bytearray /\ __key:SupportsIndex /\ __value:SupportsIndex) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __value:T?2) -> (return:NoneType))',
    },
    '__delitem__': {
        r'((self:bytearray /\ __key:slice + SupportsIndex) -> (return:NoneType))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __key:slice + SupportsIndex) -> (return:NoneType))',
    },
    '__iadd__': {
        r'((self:list < T?0 > /\ __value:Iterable < T?0 >) -> (return:list < T?0 >))',
        r'((self:bytearray /\ __value:bytes + bytearray + memoryview) -> (return:bytearray))',
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
        r'((self:memoryview < int >) -> (return:NoneType + tuple < ellipsis + int >))',
    },
    'strides': {
        r'((self:memoryview < int >) -> (return:NoneType + tuple < ellipsis + int >))',
    },
    'suboffsets': {
        r'((self:memoryview < int >) -> (return:NoneType + tuple < ellipsis + int >))',
    },
    'readonly': {
        r'((self:memoryview < int >) -> (return:bool))',
    },
    'ndim': {
        r'((self:memoryview < int >) -> (return:int))',
    },
    'obj': {
        r'((self:memoryview < int >) -> (return:bytes + bytearray + memoryview))',
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
        r'((self:memoryview < int > /\ __exc_type:NoneType + type < BaseException > /\ __exc_val:BaseException + NoneType /\ __exc_tb:NoneType + traceback) -> (return:NoneType))',
    },
    'cast': {
        r'((self:memoryview < int > /\ format:str /\ __d_shape:list < int > + tuple < ellipsis + int >) -> (return:memoryview))',
    },
    'tolist': {
        r'((self:memoryview < int >) -> (return:list < int >))',
    },
    'release': {
        r'((self:memoryview < int >) -> (return:NoneType))',
    },
    'start': {
        r'((self:range) -> (return:int))',
        r'((self:slice) -> (return:top))',
    },
    'step': {
        r'((self:range) -> (return:int))',
        r'((self:slice) -> (return:top))',
    },
    'stop': {
        r'((self:range) -> (return:int))',
        r'((self:slice) -> (return:top))',
    },
    'indices': {
        r'((self:slice /\ __len:SupportsIndex) -> (return:tuple < int >))',
    },
    '__closure__': {
        r'((self:tuple < T?3 >) -> (return:NoneType + tuple < _Cell + ellipsis >))',
    },
    '__globals__': {
        r'((self:tuple < T?3 >) -> (return:dict < str, top >))',
    },
    'sort': {
        r'((self:list < T?0 > /\ __ko___d_key:NoneType /\ __ko___d_reverse:bool) -> (return:NoneType))',
        r'((self:list < T?0 > /\ __ko_key:Callable /\ __ko___d_reverse:bool) -> (return:NoneType))',
    },
    '__reversed__': {
        r'((self:list < T?0 >) -> (return:Iterator < T?0 >))',
        r'((self:range) -> (return:Iterator < int >))',
    },
    'fromkeys': {
        r'((cls:dict < T?1, T?2 > /\ __iterable:Iterable < T?0 > /\ __value:T?4) -> (return:dict < T?0, T?4 >))',
        r'((cls:dict < T?1, T?2 > /\ __iterable:Iterable < T?0 > /\ __d___value:NoneType) -> (return:dict < T?0, top + NoneType >))',
    },
    'get': {
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?2) -> (return:T?2))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1) -> (return:NoneType + T?2))',
        r'((self:dict < T?1, T?2 > /\ __key:T?1 /\ __default:T?0) -> (return:T?0 + T?2))',
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
        r'((self:frozenset < T?3 > /\ __s:Iterable < top >) -> (return:bool))',
        r'((self:set < T?0 > /\ __s:Iterable < top >) -> (return:bool))',
    },
    'issuperset': {
        r'((self:frozenset < T?3 > /\ __s:Iterable < top >) -> (return:bool))',
        r'((self:set < T?0 > /\ __s:Iterable < top >) -> (return:bool))',
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
    '__next__': {
        r'((self:map < T?4 >) -> (return:T?4))',
        r'((self:reversed < T?0 >) -> (return:T?0))',
        r'((self:zip < T?3 >) -> (return:T?3))',
        r'((self:filter < T?0 >) -> (return:T?0))',
        r'((self:enumerate < tuple < int + T?0 > >) -> (return:tuple < int + T?0 >))',
    },
    'getter': {
        r'((self:property /\ __fget:Callable) -> (return:property))',
    },
    'setter': {
        r'((self:property /\ __fset:Callable) -> (return:property))',
    },
    'deleter': {
        r'((self:property /\ __fdel:Callable) -> (return:property))',
    },
    '__set__': {
        r'((self:property /\ __instance:top /\ __value:top) -> (return:NoneType))',
    },
    '__delete__': {
        r'((self:property /\ __instance:top) -> (return:NoneType))',
    },
    '__length_hint__': {
        r'((self:reversed < T?0 >) -> (return:int))',
    },
    '__setstate__': {
        r'((self:BaseException /\ __state:dict < str, top > + NoneType) -> (return:NoneType))',
    },
    'with_traceback': {
        r'((self:BaseException /\ __tb:NoneType + traceback) -> (return:BaseException))',
    },
    'abs': {
        r'((__x:int < T?0 > + float < T?0 > + complex < T?0 >) -> (return:T?0))',
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
        r'((__obj:top) -> (return:TypeGuard < Callable >))',
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
        r'((__source:code + memoryview + bytearray + str + bytes /\ __d___globals:dict < str, top > + NoneType /\ __d___locals:NoneType + Mapping < str, top >) -> (return:top))',
    },
    'exit': {
        r'((__d_code:NoneType + int + str) -> (return:bot))',
    },
    'getattr': {
        r'((__o:top /\ name:str /\ __default:list < top >) -> (return:top + list < top >))',
        r'((__o:top /\ __name:str) -> (return:top))',
        r'((__o:top /\ __name:str /\ __default:T?0) -> (return:top + T?0))',
        r'((__o:top /\ __name:str /\ __default:bool) -> (return:top + bool))',
        r'((__o:top /\ __name:str /\ __default:NoneType) -> (return:top + NoneType))',
        r'((__o:top /\ name:str /\ __default:dict < top, top >) -> (return:top + dict < top, top >))',
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
    'iter': {
        r'((__function:Callable /\ __sentinel:NoneType) -> (return:Iterator < T?0 >))',
        r'((__function:Callable /\ __sentinel:top) -> (return:Iterator < T?0 >))',
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
        r'((__iterable:Iterable < T?0 > /\ __ko_key:Callable) -> (return:T?0))',
        r'((__arg1:T?0 /\ __arg2:T?0 /\ __va__args:T?0 /\ __ko_key:Callable) -> (return:T?0))',
        r'((__iterable:Iterable < _T1 > /\ __ko_key:Callable /\ __ko_default:_T2) -> (return:_T1 + _T2))',
    },
    'min': {
        r'((__iterable:Iterable < T?0 > /\ __ko_key:Callable) -> (return:T?0))',
        r'((__arg1:T?0 /\ __arg2:T?0 /\ __va__args:T?0 /\ __ko_key:Callable) -> (return:T?0))',
        r'((__iterable:Iterable < _T1 > /\ __ko_key:Callable /\ __ko_default:_T2) -> (return:_T1 + _T2))',
    },
    'oct': {
        r'((__number:int + SupportsIndex) -> (return:str))',
    },
    'ord': {
        r'((__c:bytearray + bytes + str) -> (return:int))',
    },
    'print': {
        r'((__va_values:top /\ __ko___d_sep:NoneType + str /\ __ko___d_end:NoneType + str /\ __ko___d_file:NoneType + top < str > /\ __ko_flush:bool) -> (return:NoneType))',
    },
    'quit': {
        r'((__d_code:NoneType + int + str) -> (return:bot))',
    },
    'repr': {
        r'((__obj:top) -> (return:str))',
    },
    'setattr': {
        r'((__obj:top /\ __name:str /\ __value:top) -> (return:NoneType))',
    },
    'sorted': {
        r'((__iterable:Iterable < T?0 > /\ __ko_key:Callable /\ __ko___d_reverse:bool) -> (return:list < T?0 >))',
    },
    'sum': {
        r'((__iterable:Iterable < int >) -> (return:int))',
    },
    'vars': {
        r'((__object:type) -> (return:mappingproxy < top + str >))',
        r'((__d___object:top) -> (return:dict < str, top >))',
    },
    '__import__': {
        r'((name:str /\ __d_globals:NoneType + Mapping < str, top > /\ __d_locals:NoneType + Mapping < str, top > /\ __d_fromlist:Sequence < str > /\ __d_level:int) -> (return:module))',
    },
    '__build_class__': {
        r'((__func:Callable /\ __name:str /\ __va_bases:top /\ __ko___d_metaclass:top /\ __kw_kwds:top) -> (return:top))',
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
        r'((__va_args:Iterable < top > /\ y:Iterable < T?0 > + str) -> (__va_args:Iterable < T?0 + str > /\ return:NoneType))',
    },
    'seqassign': {
        r'((x:top /\ y:Iterable < T?0 >) -> (x:T?0 /\ return:NoneType))',
        r'((x:top /\ y:str) -> (x:str /\ return:NoneType))',
    },
    'simple_subscript': {
        r'((a:dict < T?0, T?1 > /\ b:T?0) -> (return:T?1))',
        r'((a:Iterable < T?0 > /\ b:int) -> (return:T?0))',
    },
    'subscriptassign': {
        r'((x:set < T?0 > /\ y:T?1) -> (x:set < T?1 + T?0 > /\ return:NoneType))',
        r'((x:frozenset < T?0 > /\ y:T?1) -> (x:frozenset < T?1 + T?0 > /\ return:NoneType))',
        r'((x:dict < T?0, T?1 > /\ y:T?2) -> (x:dict < T?0, T?1 + T?2 > /\ return:NoneType))',
        r'((x:tuple < T?0 > /\ y:T?1) -> (x:tuple < T?1 + T?0 > /\ return:NoneType))',
        r'((x:list < T?0 > /\ y:T?1) -> (x:list < T?1 + T?0 > /\ return:NoneType))',
    },
    'assign_1_prim': {
        r'((c:tuple < T?1 + T?0 > + str) -> (return:tuple < T?1 + T?0 + str >))',
    },
    'for_parse': {
        r'((target:top /\ iter:memoryview) -> (target:int))',
        r'((target:top /\ iter:Iterable < T?0 >) -> (target:T?0))',
        r'((target:top /\ iter:bytes) -> (target:int))',
        r'((target:top /\ iter:bytearray) -> (target:int))',
        r'((target:top /\ iter:range) -> (target:int))',
        r'((target:top /\ iter:str) -> (target:str))',
    },
    'range': {
        r'((stop:int) -> (return:range))',
        r'((start:int /\ stop:int) -> (return:range))',
        r'((start:int /\ stop:int /\ step:int) -> (return:range))',
    },

}
