unitedspecs = {
	'__new__': {
			r'((cls:frozenset<T?co>) -> (return:frozenset<T?co>))',
			r'((cls:int /\ __x:SupportsIndex+SupportsTrunc+memoryview+str+bytearray+SupportsInt+bytes) -> (return:int))',
			r'((cls:int /\ __x:bytearray+str+bytes /\ base:SupportsIndex) -> (return:int))',
			r'((cls:str /\ object:bytearray+bytes+memoryview /\ encoding:str /\ errors:str) -> (return:str))',
			r'((cls:frozenset<T?co> /\ __iterable:Iterable<T?co>) -> (return:frozenset<T?co>))',
			r'((cls:bytes) -> (return:bytes))',
			r'((cls:str /\ object:top) -> (return:str))',
			r'((cls:tuple<T?co> /\ __iterable:Iterable<T?co>) -> (return:tuple<T?co>))',
			r'((cls:bytes /\ __string:str /\ encoding:str /\ errors:str) -> (return:bytes))',
			r'((cls:bool /\ __o:top) -> (return:bool))',
			r'((cls:dict<T?K, T?V> /\ __va_args:top /\ __kw_kwargs:top) -> (return:dict<T?K, T?V>))',
			r'((cls:float /\ __x:SupportsIndex+SupportsFloat+memoryview+str+bytearray+bytes) -> (return:float))',
			r'((cls:bytes /\ __o:SupportsIndex+Iterable<SupportsIndex>+memoryview+SupportsBytes+bytearray+bytes) -> (return:bytes))',
	},
	'real': {
			r'((self:int) -> (return:int))',
			r'((self:complex) -> (return:float))',
			r'((self:float) -> (return:float))',
	},
	'imag': {
			r'((self:int) -> (return:int))',
			r'((self:complex) -> (return:float))',
			r'((self:float) -> (return:float))',
	},
	'numerator': {
			r'((self:int) -> (return:int))',
	},
	'denominator': {
			r'((self:int) -> (return:int))',
	},
	'conjugate': {
			r'((self:int) -> (return:int))',
			r'((self:complex) -> (return:complex))',
			r'((self:float) -> (return:float))',
	},
	'bit_length': {
			r'((self:int) -> (return:int))',
	},
	'__add__': {
			r'((self:float /\ __value:float) -> (return:float))',
			r'((self:tuple<T?co> /\ __value:tuple<T?0>) -> (return:tuple<T?0+T?co>))',
			r'((self:tuple<T?co> /\ __value:tuple<T?co>) -> (return:tuple<T?co>))',
			r'((self:bytes /\ __value:bytearray+bytes+memoryview) -> (return:bytes))',
			r'((self:int /\ __value:int) -> (return:int))',
			r'((self:str /\ __value:str) -> (return:str))',
			r'((self:complex /\ __value:complex) -> (return:complex))',
			r'((self:list<T?0> /\ __value:list<T?0>) -> (return:list<T?0>))',
			r'((self:list<T?0> /\ __value:list<T?s>) -> (return:list<T?0+T?s>))',
			r'((self:bytearray /\ __value:bytearray+bytes+memoryview) -> (return:bytearray))',
	},
	'__sub__': {
			r'((self:float /\ __value:float) -> (return:float))',
			r'((self:complex /\ __value:complex) -> (return:complex))',
			r'((self:set<T?0> /\ __value:set<T?0+NoneType>) -> (return:set<T?0>))',
			r'((self:frozenset<T?co> /\ __value:set<T?co>) -> (return:frozenset<T?co>))',
			r'((self:int /\ __value:int) -> (return:int))',
	},
	'__mul__': {
			r'((self:float /\ __value:float) -> (return:float))',
			r'((self:complex /\ __value:complex) -> (return:complex))',
			r'((self:list<T?0> /\ __value:SupportsIndex) -> (return:list<T?0>))',
			r'((self:bytes /\ __value:SupportsIndex) -> (return:bytes))',
			r'((self:tuple<T?co> /\ __value:SupportsIndex) -> (return:tuple<T?co>))',
			r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
			r'((self:int /\ __value:int) -> (return:int))',
			r'((self:str /\ __value:SupportsIndex) -> (return:str))',
	},
	'__floordiv__': {
			r'((self:float /\ __value:float) -> (return:float))',
			r'((self:int /\ __value:int) -> (return:int))',
	},
	'__truediv__': {
			r'((self:int /\ __value:int) -> (return:float))',
			r'((self:complex /\ __value:complex) -> (return:complex))',
			r'((self:float /\ __value:float) -> (return:float))',
	},
	'__mod__': {
			r'((self:float /\ __value:float) -> (return:float))',
			r'((self:str /\ __value:top) -> (return:str))',
			r'((self:str /\ __value:str+tuple<str>) -> (return:str))',
			r'((self:int /\ __value:int) -> (return:int))',
			r'((self:bytearray /\ __value:top) -> (return:bytes))',
			r'((self:bytes /\ __value:top) -> (return:bytes))',
	},
	'__divmod__': {
			r'((self:float /\ __value:float) -> (return:tuple<float>))',
			r'((self:int /\ __value:int) -> (return:tuple<int>))',
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
			r'((self:float /\ __value:float) -> (return:float))',
			r'((self:complex /\ __value:complex) -> (return:complex))',
			r'((self:list<T?0> /\ __value:SupportsIndex) -> (return:list<T?0>))',
			r'((self:bytes /\ __value:SupportsIndex) -> (return:bytes))',
			r'((self:tuple<T?co> /\ __value:SupportsIndex) -> (return:tuple<T?co>))',
			r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
			r'((self:int /\ __value:int) -> (return:int))',
			r'((self:str /\ __value:SupportsIndex) -> (return:str))',
	},
	'__rfloordiv__': {
			r'((self:float /\ __value:float) -> (return:float))',
			r'((self:int /\ __value:int) -> (return:int))',
	},
	'__rtruediv__': {
			r'((self:int /\ __value:int) -> (return:float))',
			r'((self:complex /\ __value:complex) -> (return:complex))',
			r'((self:float /\ __value:float) -> (return:float))',
	},
	'__rmod__': {
			r'((self:float /\ __value:float) -> (return:float))',
			r'((self:int /\ __value:int) -> (return:int))',
	},
	'__rdivmod__': {
			r'((self:float /\ __value:float) -> (return:tuple<float>))',
			r'((self:int /\ __value:int) -> (return:tuple<int>))',
	},
	'__pow__': {
			r'((self:complex /\ __value:complex /\ __mod:NoneType) -> (return:complex))',
			r'((self:int /\ __value:int /\ __mod:int) -> (return:int))',
			r'((self:int /\ __x:int) -> (return:int))',
			r'((self:int /\ __value:int /\ __mod:NoneType) -> (return:float))',
			r'((self:float /\ __value:int /\ __mod:NoneType) -> (return:float))',
			r'((self:int /\ __value:int /\ __mod:NoneType) -> (return:int))',
	},
	'__and__': {
			r'((self:bool /\ __value:int) -> (return:int))',
			r'((self:frozenset<T?co> /\ __value:set<T?co>) -> (return:frozenset<T?co>))',
			r'((self:int /\ __value:int) -> (return:int))',
			r'((self:bool /\ __value:bool) -> (return:bool))',
			r'((self:set<T?0> /\ __value:set<top>) -> (return:set<T?0>))',
	},
	'__or__': {
			r'((self:bool /\ __value:int) -> (return:int))',
			r'((self:frozenset<T?co> /\ __value:set<T?s>) -> (return:frozenset<T?s+T?co>))',
			r'((self:set<T?0> /\ __value:set<T?s>) -> (return:set<T?0+T?s>))',
			r'((self:int /\ __value:int) -> (return:int))',
			r'((self:bool /\ __value:bool) -> (return:bool))',
	},
	'__xor__': {
			r'((self:bool /\ __value:int) -> (return:int))',
			r'((self:frozenset<T?co> /\ __value:set<T?s>) -> (return:frozenset<T?s+T?co>))',
			r'((self:set<T?0> /\ __value:set<T?s>) -> (return:set<T?0+T?s>))',
			r'((self:int /\ __value:int) -> (return:int))',
			r'((self:bool /\ __value:bool) -> (return:bool))',
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
			r'((self:int) -> (return:int))',
			r'((self:complex) -> (return:complex))',
			r'((self:float) -> (return:float))',
	},
	'__pos__': {
			r'((self:int) -> (return:int))',
			r'((self:complex) -> (return:complex))',
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
			r'((self:float /\ __ndigits:NoneType) -> (return:int))',
			r'((self:float /\ __ndigits:SupportsIndex) -> (return:float))',
			r'((self:int /\ __ndigits:SupportsIndex) -> (return:int))',
	},
	'__getnewargs__': {
			r'((self:bool) -> (return:tuple<int>))',
			r'((self:bytes) -> (return:tuple<bytes>))',
			r'((self:float) -> (return:tuple<float>))',
			r'((self:int) -> (return:tuple<int>))',
			r'((self:str) -> (return:tuple<str>))',
	},
	'__eq__': {
			r'((self:range<int> /\ __value:top) -> (return:bool))',
			r'((self:slice /\ __value:top) -> (return:bool))',
			r'((self:dict<T?K, T?V> /\ __value:top) -> (return:bool))',
			r'((self:frozenset<T?co> /\ __value:top) -> (return:bool))',
			r'((self:complex /\ __value:top) -> (return:bool))',
			r'((self:int /\ __value:top) -> (return:bool))',
			r'((self:bytes /\ __value:top) -> (return:bool))',
			r'((self:tuple<T?co> /\ __value:top) -> (return:bool))',
			r'((self:float /\ __value:top) -> (return:bool))',
			r'((self:str /\ __value:top) -> (return:bool))',
			r'((self:list<T?0> /\ __value:top) -> (return:bool))',
			r'((self:set<T?0> /\ __value:top) -> (return:bool))',
			r'((self:bytearray /\ __value:top) -> (return:bool))',
	},
	'__ne__': {
			r'((self:bytes /\ __value:top) -> (return:bool))',
			r'((self:str /\ __value:top) -> (return:bool))',
			r'((self:bytearray /\ __value:top) -> (return:bool))',
			r'((self:int /\ __value:top) -> (return:bool))',
			r'((self:complex /\ __value:top) -> (return:bool))',
			r'((self:float /\ __value:top) -> (return:bool))',
	},
	'__lt__': {
			r'((self:tuple<T?co> /\ __value:tuple<T?co>) -> (return:bool))',
			r'((self:int /\ __value:int) -> (return:bool))',
			r'((self:bytearray /\ __value:bytearray+bytes+memoryview) -> (return:bool))',
			r'((self:bytes /\ __value:bytes) -> (return:bool))',
			r'((self:str /\ __value:str) -> (return:bool))',
			r'((self:set<T?0> /\ __value:set<top>) -> (return:bool))',
			r'((self:float /\ __value:float) -> (return:bool))',
			r'((self:list<T?0> /\ __value:list<T?0>) -> (return:bool))',
			r'((self:frozenset<T?co> /\ __value:set<top>) -> (return:bool))',
	},
	'__le__': {
			r'((self:tuple<T?co> /\ __value:tuple<T?co>) -> (return:bool))',
			r'((self:int /\ __value:int) -> (return:bool))',
			r'((self:bytearray /\ __value:bytearray+bytes+memoryview) -> (return:bool))',
			r'((self:bytes /\ __value:bytes) -> (return:bool))',
			r'((self:str /\ __value:str) -> (return:bool))',
			r'((self:set<T?0> /\ __value:set<top>) -> (return:bool))',
			r'((self:float /\ __value:float) -> (return:bool))',
			r'((self:list<T?0> /\ __value:list<T?0>) -> (return:bool))',
			r'((self:frozenset<T?co> /\ __value:set<top>) -> (return:bool))',
	},
	'__gt__': {
			r'((self:tuple<T?co> /\ __value:tuple<T?co>) -> (return:bool))',
			r'((self:int /\ __value:int) -> (return:bool))',
			r'((self:bytearray /\ __value:bytearray+bytes+memoryview) -> (return:bool))',
			r'((self:bytes /\ __value:bytes) -> (return:bool))',
			r'((self:str /\ __value:str) -> (return:bool))',
			r'((self:set<T?0> /\ __value:set<top>) -> (return:bool))',
			r'((self:float /\ __value:float) -> (return:bool))',
			r'((self:list<T?0> /\ __value:list<T?0>) -> (return:bool))',
			r'((self:frozenset<T?co> /\ __value:set<top>) -> (return:bool))',
	},
	'__ge__': {
			r'((self:tuple<T?co> /\ __value:tuple<T?co>) -> (return:bool))',
			r'((self:int /\ __value:int) -> (return:bool))',
			r'((self:bytearray /\ __value:bytearray+bytes+memoryview) -> (return:bool))',
			r'((self:bytes /\ __value:bytes) -> (return:bool))',
			r'((self:str /\ __value:str) -> (return:bool))',
			r'((self:set<T?0> /\ __value:set<top>) -> (return:bool))',
			r'((self:float /\ __value:float) -> (return:bool))',
			r'((self:list<T?0> /\ __value:list<T?0>) -> (return:bool))',
			r'((self:frozenset<T?co> /\ __value:set<top>) -> (return:bool))',
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
			r'((self:complex) -> (return:float))',
			r'((self:float) -> (return:float))',
	},
	'__hash__': {
			r'((self:str) -> (return:int))',
			r'((self:tuple<T?co>) -> (return:int))',
			r'((self:int) -> (return:int))',
			r'((self:bytes) -> (return:int))',
			r'((self:frozenset<T?co>) -> (return:int))',
			r'((self:float) -> (return:int))',
			r'((self:complex) -> (return:int))',
			r'((self:range<int>) -> (return:int))',
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
			r'((self:float) -> (return:tuple<int>))',
	},
	'hex': {
			r'((__number:SupportsIndex+int) -> (return:str))',
			r'((self:float) -> (return:str))',
	},
	'is_integer': {
			r'((self:float) -> (return:bool))',
	},
	'fromhex': {
			r'((cls:bytes /\ __string:str) -> (return:bytes))',
			r'((cls:float /\ __string:str) -> (return:float))',
			r'((cls:bytearray /\ __string:str) -> (return:bytearray))',
	},
	'__rpow__': {
			r'((self:complex /\ __value:complex /\ __mod:NoneType) -> (return:complex))',
			r'((self:float /\ __value:int /\ __mod:NoneType) -> (return:complex))',
			r'((self:float /\ __value:int /\ __mod:NoneType) -> (return:float))',
	},
	'capitalize': {
			r'((self:bytes) -> (return:bytes))',
			r'((self:str) -> (return:str))',
			r'((self:bytearray) -> (return:bytearray))',
	},
	'casefold': {
			r'((self:str) -> (return:str))',
	},
	'center': {
			r'((self:str /\ __width:SupportsIndex /\ __fillchar:str) -> (return:str))',
			r'((self:bytearray /\ __width:SupportsIndex /\ __fillchar:bytes) -> (return:bytearray))',
			r'((self:bytes /\ __width:SupportsIndex /\ __fillchar:bytes) -> (return:bytes))',
	},
	'count': {
			r'((self:list<T?0> /\ __value:T?0) -> (return:int))',
			r'((self:bytes /\ __sub:bytearray+SupportsIndex+bytes+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
			r'((self:str /\ x:str /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
			r'((self:range<int> /\ __value:int) -> (return:int))',
			r'((self:tuple<T?co> /\ __value:top) -> (return:int))',
			r'((self:bytearray /\ __sub:bytearray+SupportsIndex+bytes+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
	},
	'encode': {
			r'((self:str /\ encoding:str /\ errors:str) -> (return:bytes))',
	},
	'endswith': {
			r'((self:str /\ __suffix:str+tuple<str> /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:bool))',
			r'((self:bytes /\ __suffix:bytearray+bytes+tuple<bytearray+bytes+memoryview>+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:bool))',
			r'((self:bytearray /\ __suffix:bytearray+bytes+tuple<bytearray+bytes+memoryview>+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:bool))',
	},
	'find': {
			r'((self:bytes /\ __sub:bytearray+SupportsIndex+bytes+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
			r'((self:str /\ __sub:str /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
			r'((self:bytearray /\ __sub:bytearray+SupportsIndex+bytes+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
	},
	'format': {
			r'((self:str /\ __va_args:str /\ __kw_kwargs:str) -> (return:str))',
			r'((__value:top /\ __format_spec:str) -> (return:str))',
			r'((self:str /\ __va_args:top /\ __kw_kwargs:top) -> (return:str))',
	},
	'format_map': {
			r'((self:str /\ map:dict<str, int>) -> (return:str))',
	},
	'index': {
			r'((self:bytes /\ __sub:bytearray+SupportsIndex+bytes+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
			r'((self:str /\ __sub:str /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
			r'((self:tuple<T?co> /\ __value:top /\ __start:SupportsIndex /\ __stop:SupportsIndex) -> (return:int))',
			r'((self:range<int> /\ __value:int) -> (return:int))',
			r'((self:list<T?0> /\ __value:T?0 /\ __start:SupportsIndex /\ __stop:SupportsIndex) -> (return:int))',
			r'((self:bytearray /\ __sub:bytearray+SupportsIndex+bytes+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
	},
	'isalnum': {
			r'((self:bytearray) -> (return:bool))',
			r'((self:bytes) -> (return:bool))',
			r'((self:str) -> (return:bool))',
	},
	'isalpha': {
			r'((self:bytearray) -> (return:bool))',
			r'((self:bytes) -> (return:bool))',
			r'((self:str) -> (return:bool))',
	},
	'isascii': {
			r'((self:bytearray) -> (return:bool))',
			r'((self:bytes) -> (return:bool))',
			r'((self:str) -> (return:bool))',
	},
	'isdecimal': {
			r'((self:str) -> (return:bool))',
	},
	'isdigit': {
			r'((self:bytearray) -> (return:bool))',
			r'((self:bytes) -> (return:bool))',
			r'((self:str) -> (return:bool))',
	},
	'isidentifier': {
			r'((self:str) -> (return:bool))',
	},
	'islower': {
			r'((self:bytearray) -> (return:bool))',
			r'((self:bytes) -> (return:bool))',
			r'((self:str) -> (return:bool))',
	},
	'isnumeric': {
			r'((self:str) -> (return:bool))',
	},
	'isprintable': {
			r'((self:str) -> (return:bool))',
	},
	'isspace': {
			r'((self:bytearray) -> (return:bool))',
			r'((self:bytes) -> (return:bool))',
			r'((self:str) -> (return:bool))',
	},
	'istitle': {
			r'((self:bytearray) -> (return:bool))',
			r'((self:bytes) -> (return:bool))',
			r'((self:str) -> (return:bool))',
	},
	'isupper': {
			r'((self:bytearray) -> (return:bool))',
			r'((self:bytes) -> (return:bool))',
			r'((self:str) -> (return:bool))',
	},
	'join': {
			r'((self:bytes /\ __iterable_of_bytes:Iterable<bytearray+bytes+memoryview>) -> (return:bytes))',
			r'((self:str /\ __iterable:Iterable<str>) -> (return:str))',
			r'((self:bytearray /\ __iterable_of_bytes:Iterable<bytearray+bytes+memoryview>) -> (return:bytearray))',
	},
	'ljust': {
			r'((self:str /\ __width:SupportsIndex /\ __fillchar:str) -> (return:str))',
			r'((self:bytearray /\ __width:SupportsIndex /\ __fillchar:bytearray+bytes) -> (return:bytearray))',
			r'((self:bytes /\ __width:SupportsIndex /\ __fillchar:bytearray+bytes) -> (return:bytes))',
	},
	'lower': {
			r'((self:bytes) -> (return:bytes))',
			r'((self:str) -> (return:str))',
			r'((self:bytearray) -> (return:bytearray))',
	},
	'lstrip': {
			r'((self:bytes /\ __bytes:bytearray+NoneType+bytes+memoryview) -> (return:bytes))',
			r'((self:bytearray /\ __bytes:bytearray+NoneType+bytes+memoryview) -> (return:bytearray))',
			r'((self:str /\ __chars:str+NoneType) -> (return:str))',
	},
	'partition': {
			r'((self:bytes /\ __sep:bytearray+bytes+memoryview) -> (return:tuple<bytes>))',
			r'((self:str /\ __sep:str) -> (return:tuple<str>))',
			r'((self:bytearray /\ __sep:bytearray+bytes+memoryview) -> (return:tuple<bytearray>))',
	},
	'replace': {
			r'((self:bytearray /\ __old:bytearray+bytes+memoryview /\ __new:bytearray+bytes+memoryview /\ __count:SupportsIndex) -> (return:bytearray))',
			r'((self:str /\ __old:str /\ __new:str /\ __count:SupportsIndex) -> (return:str))',
			r'((self:bytes /\ __old:bytearray+bytes+memoryview /\ __new:bytearray+bytes+memoryview /\ __count:SupportsIndex) -> (return:bytes))',
	},
	'rfind': {
			r'((self:bytes /\ __sub:bytearray+SupportsIndex+bytes+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
			r'((self:str /\ __sub:str /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
			r'((self:bytearray /\ __sub:bytearray+SupportsIndex+bytes+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
	},
	'rindex': {
			r'((self:bytes /\ __sub:bytearray+SupportsIndex+bytes+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
			r'((self:str /\ __sub:str /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
			r'((self:bytearray /\ __sub:bytearray+SupportsIndex+bytes+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:int))',
	},
	'rjust': {
			r'((self:str /\ __width:SupportsIndex /\ __fillchar:str) -> (return:str))',
			r'((self:bytearray /\ __width:SupportsIndex /\ __fillchar:bytearray+bytes) -> (return:bytearray))',
			r'((self:bytes /\ __width:SupportsIndex /\ __fillchar:bytearray+bytes) -> (return:bytes))',
	},
	'rpartition': {
			r'((self:bytes /\ __sep:bytearray+bytes+memoryview) -> (return:tuple<bytes>))',
			r'((self:str /\ __sep:str) -> (return:tuple<str>))',
			r'((self:bytearray /\ __sep:bytearray+bytes+memoryview) -> (return:tuple<bytearray>))',
	},
	'rsplit': {
			r'((self:bytearray /\ sep:bytearray+NoneType+bytes+memoryview /\ maxsplit:SupportsIndex) -> (return:list<bytearray>))',
			r'((self:str /\ sep:str+NoneType /\ maxsplit:SupportsIndex) -> (return:list<str>))',
			r'((self:bytes /\ sep:bytearray+NoneType+bytes+memoryview /\ maxsplit:SupportsIndex) -> (return:list<bytes>))',
	},
	'rstrip': {
			r'((self:bytes /\ __bytes:bytearray+NoneType+bytes+memoryview) -> (return:bytes))',
			r'((self:bytearray /\ __bytes:bytearray+NoneType+bytes+memoryview) -> (return:bytearray))',
			r'((self:str /\ __chars:str+NoneType) -> (return:str))',
	},
	'split': {
			r'((self:bytearray /\ sep:bytearray+NoneType+bytes+memoryview /\ maxsplit:SupportsIndex) -> (return:list<bytearray>))',
			r'((self:str /\ sep:str+NoneType /\ maxsplit:SupportsIndex) -> (return:list<str>))',
			r'((self:bytes /\ sep:bytearray+NoneType+bytes+memoryview /\ maxsplit:SupportsIndex) -> (return:list<bytes>))',
	},
	'splitlines': {
			r'((self:str /\ keepends:bool) -> (return:list<str>))',
			r'((self:bytearray /\ keepends:bool) -> (return:list<bytearray>))',
			r'((self:bytes /\ keepends:bool) -> (return:list<bytes>))',
	},
	'startswith': {
			r'((self:bytearray /\ __prefix:bytearray+bytes+tuple<bytearray+bytes+memoryview>+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:bool))',
			r'((self:bytes /\ __prefix:bytearray+bytes+tuple<bytearray+bytes+memoryview>+memoryview /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:bool))',
			r'((self:str /\ __prefix:str+tuple<str> /\ __start:SupportsIndex+NoneType /\ __end:SupportsIndex+NoneType) -> (return:bool))',
	},
	'strip': {
			r'((self:bytes /\ __bytes:bytearray+NoneType+bytes+memoryview) -> (return:bytes))',
			r'((self:bytearray /\ __bytes:bytearray+NoneType+bytes+memoryview) -> (return:bytearray))',
			r'((self:str /\ __chars:str+NoneType) -> (return:str))',
	},
	'swapcase': {
			r'((self:bytes) -> (return:bytes))',
			r'((self:str) -> (return:str))',
			r'((self:bytearray) -> (return:bytearray))',
	},
	'title': {
			r'((self:bytes) -> (return:bytes))',
			r'((self:str) -> (return:str))',
			r'((self:bytearray) -> (return:bytearray))',
	},
	'translate': {
			r'((self:bytearray /\ __table:bytearray+NoneType+bytes+memoryview /\ delete:bytes) -> (return:bytearray))',
			r'((self:bytes /\ __table:bytearray+NoneType+bytes+memoryview /\ delete:bytes) -> (return:bytes))',
			r'((self:str /\ __table:dict<int, int+str>) -> (return:str))',
	},
	'upper': {
			r'((self:bytes) -> (return:bytes))',
			r'((self:str) -> (return:str))',
			r'((self:bytearray) -> (return:bytearray))',
	},
	'zfill': {
			r'((self:bytearray /\ __width:SupportsIndex) -> (return:bytearray))',
			r'((self:bytes /\ __width:SupportsIndex) -> (return:bytes))',
			r'((self:str /\ __width:SupportsIndex) -> (return:str))',
	},
	'maketrans': {
			r'((__x:str /\ __y:str /\ __z:str) -> (return:dict<int, int+NoneType>))',
			r'((__x:str /\ __y:str) -> (return:dict<int, int>))',
			r'((__x:dict<int+str, T?0>+dict<str, T?0>+dict<int, T?0>) -> (return:dict<int, T?0>))',
			r'((__frm:bytearray+bytes+memoryview /\ __to:bytearray+bytes+memoryview) -> (return:bytes))',
	},
	'__contains__': {
			r'((self:tuple<T?co> /\ __key:top) -> (return:bool))',
			r'((self:set<T?0> /\ __o:top) -> (return:bool))',
			r'((self:frozenset<T?co> /\ __o:top) -> (return:bool))',
			r'((self:list<T?0> /\ __key:top) -> (return:bool))',
			r'((self:bytearray /\ __key:bytearray+SupportsIndex+bytes+memoryview) -> (return:bool))',
			r'((self:str /\ __key:str) -> (return:bool))',
			r'((self:range<int> /\ __key:top) -> (return:bool))',
			r'((self:bytes /\ __key:bytearray+SupportsIndex+bytes+memoryview) -> (return:bool))',
	},
	'__iter__': {
			r'((self:list<T?0>) -> (return:Iterator<T?0>))',
			r'((self:set<T?0>) -> (return:Iterator<T?0>))',
			r'((self:str) -> (return:Iterator<str>))',
			r'((self:map<T?s>) -> (return:map<T?s>))',
			r'((self:reversed<T?0>) -> (return:reversed<T?0>))',
			r'((self:dict<T?K, T?V>) -> (return:Iterator<T?K>))',
			r'((self:bytearray) -> (return:Iterator<int>))',
			r'((self:zip<T?co>) -> (return:zip<T?co>))',
			r'((self:range<int>) -> (return:Iterator<int>))',
			r'((self:frozenset<T?co>) -> (return:Iterator<T?co>))',
			r'((self:filter<T?0>) -> (return:filter<T?0>))',
			r'((self:tuple<T?co>) -> (return:Iterator<T?co>))',
			r'((self:bytes) -> (return:Iterator<int>))',
	},
	'__len__': {
			r'((self:set<T?0>) -> (return:int))',
			r'((self:tuple<T?co>) -> (return:int))',
			r'((self:frozenset<T?co>) -> (return:int))',
			r'((self:bytearray) -> (return:int))',
			r'((self:range<int>) -> (return:int))',
			r'((self:str) -> (return:int))',
			r'((self:dict<T?K, T?V>) -> (return:int))',
			r'((self:bytes) -> (return:int))',
			r'((self:list<T?0>) -> (return:int))',
	},
	'decode': {
			r'((self:bytes /\ encoding:str /\ errors:str) -> (return:str))',
			r'((self:bytearray /\ encoding:str /\ errors:str) -> (return:str))',
	},
	'__getitem__': {
			r'((self:bytes /\ __key:SupportsIndex) -> (return:int))',
			r'((self:dict<T?K, T?V> /\ __key:T?K) -> (return:T?V))',
			r'((self:list<T?0> /\ __i:SupportsIndex) -> (return:T?0))',
			r'((self:bytearray /\ __key:SupportsIndex) -> (return:int))',
			r'((self:range<int> /\ __key:SupportsIndex) -> (return:int))',
			r'((self:tuple<T?co> /\ __key:SupportsIndex) -> (return:T?co))',
	},
	'__buffer__': {
			r'((self:bytearray /\ __flags:int) -> (return:memoryview))',
			r'((self:bytes /\ __flags:int) -> (return:memoryview))',
	},
	'__init__': {
			r'((self:slice /\ __start:top /\ __stop:top /\ __step:top) -> (return:NoneType))',
			r'((self:filter<T?0> /\ __function:NoneType /\ __iterable:Iterable<T?0+NoneType>) -> (return:NoneType))',
			r'((self:set<T?0> /\ __iterable:Iterable<T?0>) -> (return:NoneType))',
			r'((self:list<T?0>) -> (return:NoneType))',
			r'((self:dict<str, T?V> /\ __iterable:Iterable<tuple<str+T?V>> /\ __kw_kwargs:T?V) -> (return:NoneType))',
			r'((self:dict<T?K, T?V> /\ __iterable:Iterable<tuple<T?K+T?V>>) -> (return:NoneType))',
			r'((self:dict<str, T?V> /\ __kw_kwargs:T?V) -> (return:NoneType))',
			r'((self:BaseException /\ __va_args:top) -> (return:NoneType))',
			r'((self:bytearray) -> (return:NoneType))',
			r'((self:dict<str, T?V> /\ __map:dict<str, T?V> /\ __kw_kwargs:T?V) -> (return:NoneType))',
			r'((self:ImportError /\ __va_args:top /\ __ko_name:str+NoneType /\ __ko_path:str+NoneType) -> (return:NoneType))',
			r'((self:UnicodeDecodeError /\ __encoding:str /\ __object:bytearray+bytes+memoryview /\ __start:int /\ __end:int /\ __reason:str) -> (return:NoneType))',
			r'((self:dict<T?K, T?V>) -> (return:NoneType))',
			r'((self:range<int> /\ __stop:SupportsIndex) -> (return:NoneType))',
			r'((self:list<T?0> /\ __iterable:Iterable<T?0>) -> (return:NoneType))',
			r'((self:UnicodeEncodeError /\ __encoding:str /\ __object:str /\ __start:int /\ __end:int /\ __reason:str) -> (return:NoneType))',
			r'((self:reversed<T?0> /\ __sequence:SupportsLenAndGetItem<T?0>) -> (return:NoneType))',
			r'((self:dict<str, str> /\ __iterable:Iterable<list<str>>) -> (return:NoneType))',
			r'((self:set<T?0>) -> (return:NoneType))',
			r'((self:reversed<T?0> /\ __sequence:Reversible<T?0>) -> (return:NoneType))',
			r'((self:bytearray /\ __string:str /\ encoding:str /\ errors:str) -> (return:NoneType))',
			r'((self:bytearray /\ __ints:SupportsIndex+Iterable<SupportsIndex>+memoryview+bytearray+bytes) -> (return:NoneType))',
			r'((self:dict<T?K, T?V> /\ __map:dict<T?K, T?V>) -> (return:NoneType))',
			r'((self:UnicodeTranslateError /\ __object:str /\ __start:int /\ __end:int /\ __reason:str) -> (return:NoneType))',
			r'((self:range<int> /\ __start:SupportsIndex /\ __stop:SupportsIndex /\ __step:SupportsIndex) -> (return:NoneType))',
			r'((self:slice /\ __stop:top) -> (return:NoneType))',
			r'((self:dict<bytes, bytes> /\ __iterable:Iterable<list<bytes>>) -> (return:NoneType))',
	},
	'append': {
			r'((self:bytearray /\ __item:SupportsIndex) -> (return:NoneType))',
			r'((self:list<T?0> /\ __object:T?0) -> (return:NoneType))',
	},
	'copy': {
			r'((self:dict<T?K, T?V>) -> (return:dict<T?K, T?V>))',
			r'((self:frozenset<T?co>) -> (return:frozenset<T?co>))',
			r'((self:set<T?0>) -> (return:set<T?0>))',
			r'((self:list<T?0>) -> (return:list<T?0>))',
			r'((self:bytearray) -> (return:bytearray))',
	},
	'extend': {
			r'((self:bytearray /\ __iterable_of_ints:Iterable<SupportsIndex>) -> (return:NoneType))',
			r'((self:list<T?0> /\ __iterable:Iterable<T?0>) -> (return:NoneType))',
	},
	'insert': {
			r'((self:list<T?0> /\ __index:SupportsIndex /\ __object:T?0) -> (return:NoneType))',
			r'((self:bytearray /\ __index:SupportsIndex /\ __item:SupportsIndex) -> (return:NoneType))',
	},
	'pop': {
			r'((self:dict<T?K, T?V> /\ __key:T?K) -> (return:T?V))',
			r'((self:list<T?0> /\ __index:SupportsIndex) -> (return:T?0))',
			r'((self:dict<T?K, T?V> /\ __key:T?K /\ __default:T?0) -> (return:T?0+T?V))',
			r'((self:bytearray /\ __index:int) -> (return:int))',
			r'((self:dict<T?K, T?V> /\ __key:T?K /\ __default:T?V) -> (return:T?V))',
	},
	'remove': {
			r'((self:bytearray /\ __value:int) -> (return:NoneType))',
			r'((self:set<T?0> /\ __element:T?0) -> (return:NoneType))',
			r'((self:list<T?0> /\ __value:T?0) -> (return:NoneType))',
	},
	'__setitem__': {
			r'((self:list<T?0> /\ __key:SupportsIndex /\ __value:T?0) -> (return:NoneType))',
			r'((self:bytearray /\ __key:SupportsIndex /\ __value:SupportsIndex) -> (return:NoneType))',
			r'((self:dict<T?K, T?V> /\ __key:T?K /\ __value:T?V) -> (return:NoneType))',
	},
	'__iadd__': {
			r'((self:bytearray /\ __value:bytearray+bytes+memoryview) -> (return:bytearray))',
			r'((self:list<T?0> /\ __value:Iterable<T?0>) -> (return:list<T?0>))',
	},
	'__imul__': {
			r'((self:bytearray /\ __value:SupportsIndex) -> (return:bytearray))',
			r'((self:list<T?0> /\ __value:SupportsIndex) -> (return:list<T?0>))',
	},
	'__alloc__': {
			r'((self:bytearray) -> (return:int))',
	},
	'__release_buffer__': {
			r'((self:bytearray /\ __buffer:memoryview) -> (return:NoneType))',
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
			r'((cls:dict<T?K, T?V> /\ __iterable:Iterable<T?0> /\ __value:T?s) -> (return:dict<T?0, T?s>))',
			r'((cls:dict<T?K, T?V> /\ __iterable:Iterable<T?0> /\ __value:NoneType) -> (return:dict<T?0, top+NoneType>))',
	},
	'get': {
			r'((self:dict<T?K, T?V> /\ __key:T?K /\ __default:T?0) -> (return:T?0+T?V))',
			r'((self:dict<T?K, T?V> /\ __key:T?K) -> (return:T?V+NoneType))',
			r'((self:dict<T?K, T?V> /\ __key:T?K /\ __default:T?V) -> (return:T?V))',
	},
	'__delitem__': {
			r'((self:dict<T?K, T?V> /\ __key:T?K) -> (return:NoneType))',
	},
	'add': {
			r'((self:set<T?0> /\ __element:T?0) -> (return:NoneType))',
	},
	'difference': {
			r'((self:set<T?0> /\ __va_s:Iterable<top>) -> (return:set<T?0>))',
			r'((self:frozenset<T?co> /\ __va_s:Iterable<top>) -> (return:frozenset<T?co>))',
	},
	'difference_update': {
			r'((self:set<T?0> /\ __va_s:Iterable<top>) -> (return:NoneType))',
	},
	'discard': {
			r'((self:set<T?0> /\ __element:T?0) -> (return:NoneType))',
	},
	'intersection': {
			r'((self:set<T?0> /\ __va_s:Iterable<top>) -> (return:set<T?0>))',
			r'((self:frozenset<T?co> /\ __va_s:Iterable<top>) -> (return:frozenset<T?co>))',
	},
	'intersection_update': {
			r'((self:set<T?0> /\ __va_s:Iterable<top>) -> (return:NoneType))',
	},
	'isdisjoint': {
			r'((self:set<T?0> /\ __s:Iterable<top>) -> (return:bool))',
			r'((self:frozenset<T?co> /\ __s:Iterable<T?co>) -> (return:bool))',
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
			r'((self:frozenset<T?co> /\ __va_s:Iterable<T?s>) -> (return:frozenset<T?s+T?co>))',
			r'((self:set<T?0> /\ __va_s:Iterable<T?s>) -> (return:set<T?0+T?s>))',
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
			r'((self:map<T?s>) -> (return:T?s))',
			r'((self:zip<T?co>) -> (return:T?co))',
	},
	'__length_hint__': {
			r'((self:reversed<T?0>) -> (return:int))',
	},
	'__setstate__': {
			r'((self:BaseException /\ __state:dict<str, top>+NoneType) -> (return:NoneType))',
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
			r'((__number:SupportsIndex+int) -> (return:str))',
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
			r'((__x:SupportsDivMod<T?contra+T?co> /\ __y:T?contra) -> (return:T?co))',
			r'((__x:T?contra /\ __y:SupportsRDivMod<T?contra+T?co>) -> (return:T?co))',
	},
	'getattr': {
			r'((__o:top /\ __name:str /\ __default:NoneType) -> (return:top+NoneType))',
			r'((__o:top /\ name:str /\ __default:dict<top, top>) -> (return:dict<top, top>+top))',
			r'((__o:top /\ __name:str /\ __default:bool) -> (return:bool+top))',
			r'((__o:top /\ __name:str /\ __default:T?0) -> (return:T?0+top))',
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
			r'((__iterable:Iterable<SupportsRichComparisonT> /\ __ko_key:NoneType) -> (return:SupportsRichComparisonT))',
			r'((__arg1:SupportsRichComparisonT /\ __arg2:SupportsRichComparisonT /\ __va__args:SupportsRichComparisonT /\ __ko_key:NoneType) -> (return:SupportsRichComparisonT))',
			r'((__iterable:Iterable<SupportsRichComparisonT> /\ __ko_key:NoneType /\ __ko_default:T?0) -> (return:T?0+SupportsRichComparisonT))',
	},
	'min': {
			r'((__iterable:Iterable<SupportsRichComparisonT> /\ __ko_key:NoneType) -> (return:SupportsRichComparisonT))',
			r'((__arg1:SupportsRichComparisonT /\ __arg2:SupportsRichComparisonT /\ __va__args:SupportsRichComparisonT /\ __ko_key:NoneType) -> (return:SupportsRichComparisonT))',
			r'((__iterable:Iterable<SupportsRichComparisonT> /\ __ko_key:NoneType /\ __ko_default:T?0) -> (return:T?0+SupportsRichComparisonT))',
	},
	'next': {
			r'((__i:SupportsNext<T?0>) -> (return:T?0))',
			r'((__i:SupportsNext<T?0> /\ __default:T?V) -> (return:T?0+T?V))',
	},
	'oct': {
			r'((__number:SupportsIndex+int) -> (return:str))',
	},
	'ord': {
			r'((__c:bytearray+str+bytes) -> (return:int))',
	},
	'print': {
			r'((__va_values:top /\ __ko_sep:str+NoneType /\ __ko_end:str+NoneType /\ __ko_file:SupportsWrite<str>+NoneType /\ __ko_flush:bool) -> (return:NoneType))',
	},
	'repr': {
			r'((__obj:top) -> (return:str))',
	},
	'round': {
			r'((number:SupportsRound<T?0> /\ ndigits:NoneType) -> (return:T?0))',
			r'((number:SupportsRound<T?0> /\ ndigits:SupportsIndex) -> (return:T?0))',
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
