import ast
from type_equivalences import *


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
		ast.Div: '__truediv__ ',
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


type_equiv = {
	Iterable: 'bytearray+bytes+dict+frozenset+list+memoryview+range+set+str+tuple',
	SupportsRichComparisonT: 'bytearray+bytes+complex+dict+float+frozenset+int+list+memoryview+object+range+set+str+tuple',
	GetItemIterable: 'bytearray+bytes+dict+list+memoryview+range+str+tuple',
	SupportsLen: 'bytearray+bytes+dict+frozenset+list+memoryview+range+set+str+tuple',
	SupportsLenAndGetItem: 'bytearray+bytes+dict+list+memoryview+range+str+tuple',
	SupportsBytes: 'bytes',
	SupportsSomeKindOfPow: 'complex+float+int',
	SupportsAbs: 'complex+float+int',
	Reversible: 'dict+list+range',
	SupportsInt: 'float+int',
	SupportsFloat: 'float+int',
	SupportsTrunc: 'float+int',
	SupportsRound: 'float+int',
	SupportsDivMod: 'float+int',
	SupportsRDivMod: 'float+int',
	SupportsIndex: 'int',
}


funcspecs = {
	'int': {
		'__new__': {
			r'cls:T?1 /\ __x:T?2 /\ base:T?3 /\ return:T?r ^ (T?1:int /\ T?2:str+bytes+bytearray /\ T?3:SupportsIndex /\ T?r:int)',
			r'cls:T?1 /\ __x:T?2 /\ return:T?r ^ (T?1:int /\ T?2:SupportsInt+str+bytes+bytearray+memoryview+SupportsIndex+SupportsTrunc /\ T?r:int)',
		},
		'real': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'imag': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'numerator': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'denominator': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'conjugate': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'bit_length': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'__add__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__sub__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__mul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__floordiv__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__truediv__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:float)',
		},
		'__mod__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__divmod__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:tuple<int>)',
		},
		'__radd__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__rsub__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__rmul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__rfloordiv__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__rtruediv__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:float)',
		},
		'__rmod__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__rdivmod__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:tuple<int>)',
		},
		'__pow__': {
			r'self:T?1 /\ __value:T?2 /\ __mod:T?3 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?3:NoneType /\ T?r:int) \/ (T?1:int /\ T?2:int /\ T?3:NoneType /\ T?r:int) \/ (T?1:int /\ T?2:int /\ T?3:NoneType /\ T?r:float) \/ (T?1:int /\ T?2:int /\ T?3:int /\ T?r:int)',
			r'self:T?1 /\ __x:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__and__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__or__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__xor__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__lshift__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__rshift__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__rand__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__ror__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__rxor__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__rlshift__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__rrshift__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
		},
		'__neg__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'__pos__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'__invert__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'__trunc__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'__ceil__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'__floor__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'__round__': {
			r'self:T?1 /\ __ndigits:T?2 /\ return:T?r ^ (T?1:int /\ T?2:SupportsIndex /\ T?r:int)',
		},
		'__getnewargs__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:tuple<int>)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:TopType /\ T?r:bool)',
		},
		'__ne__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:TopType /\ T?r:bool)',
		},
		'__lt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:bool)',
		},
		'__le__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:bool)',
		},
		'__gt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:bool)',
		},
		'__ge__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:bool)',
		},
		'__float__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:float)',
		},
		'__int__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'__abs__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'__hash__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
		'__bool__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:bool)',
		},
		'__index__': {
			r'self:T?1 /\ return:T?r ^ (T?1:int /\ T?r:int)',
		},
	},
	'float': {
		'__new__': {
			r'cls:T?1 /\ __x:T?2 /\ return:T?r ^ (T?1:float /\ T?2:bytes+bytearray+memoryview+str+SupportsFloat+SupportsIndex /\ T?r:float)',
		},
		'as_integer_ratio': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:tuple<int>)',
		},
		'hex': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:str)',
		},
		'is_integer': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:bool)',
		},
		'fromhex': {
			r'cls:T?1 /\ __string:T?2 /\ return:T?r ^ (T?1:float /\ T?2:str /\ T?r:float)',
		},
		'real': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:float)',
		},
		'imag': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:float)',
		},
		'conjugate': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:float)',
		},
		'__add__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:float)',
		},
		'__sub__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:float)',
		},
		'__mul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:float)',
		},
		'__floordiv__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:float)',
		},
		'__truediv__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:float)',
		},
		'__mod__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:float)',
		},
		'__divmod__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:tuple<float>)',
		},
		'__pow__': {
			r'self:T?1 /\ __value:T?2 /\ __mod:T?3 /\ return:T?r ^ (T?1:float /\ T?2:int /\ T?3:NoneType /\ T?r:float)',
		},
		'__radd__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:float)',
		},
		'__rsub__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:float)',
		},
		'__rmul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:float)',
		},
		'__rfloordiv__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:float)',
		},
		'__rtruediv__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:float)',
		},
		'__rmod__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:float)',
		},
		'__rdivmod__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:tuple<float>)',
		},
		'__rpow__': {
			r'self:T?1 /\ __value:T?2 /\ __mod:T?3 /\ return:T?r ^ (T?1:float /\ T?2:int /\ T?3:NoneType /\ T?r:float) \/ (T?1:float /\ T?2:int /\ T?3:NoneType /\ T?r:complex)',
		},
		'__getnewargs__': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:tuple<float>)',
		},
		'__trunc__': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:int)',
		},
		'__round__': {
			r'self:T?1 /\ __ndigits:T?2 /\ return:T?r ^ (T?1:float /\ T?2:NoneType /\ T?r:int) \/ (T?1:float /\ T?2:SupportsIndex /\ T?r:float)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:TopType /\ T?r:bool)',
		},
		'__ne__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:TopType /\ T?r:bool)',
		},
		'__lt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:bool)',
		},
		'__le__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:bool)',
		},
		'__gt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:bool)',
		},
		'__ge__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:float /\ T?2:float /\ T?r:bool)',
		},
		'__neg__': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:float)',
		},
		'__pos__': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:float)',
		},
		'__int__': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:int)',
		},
		'__float__': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:float)',
		},
		'__abs__': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:float)',
		},
		'__hash__': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:int)',
		},
		'__bool__': {
			r'self:T?1 /\ return:T?r ^ (T?1:float /\ T?r:bool)',
		},
	},
	'complex': {
		'real': {
			r'self:T?1 /\ return:T?r ^ (T?1:complex /\ T?r:float)',
		},
		'imag': {
			r'self:T?1 /\ return:T?r ^ (T?1:complex /\ T?r:float)',
		},
		'conjugate': {
			r'self:T?1 /\ return:T?r ^ (T?1:complex /\ T?r:complex)',
		},
		'__add__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:complex /\ T?2:complex /\ T?r:complex)',
		},
		'__sub__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:complex /\ T?2:complex /\ T?r:complex)',
		},
		'__mul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:complex /\ T?2:complex /\ T?r:complex)',
		},
		'__pow__': {
			r'self:T?1 /\ __value:T?2 /\ __mod:T?3 /\ return:T?r ^ (T?1:complex /\ T?2:complex /\ T?3:NoneType /\ T?r:complex)',
		},
		'__truediv__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:complex /\ T?2:complex /\ T?r:complex)',
		},
		'__radd__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:complex /\ T?2:complex /\ T?r:complex)',
		},
		'__rsub__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:complex /\ T?2:complex /\ T?r:complex)',
		},
		'__rmul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:complex /\ T?2:complex /\ T?r:complex)',
		},
		'__rpow__': {
			r'self:T?1 /\ __value:T?2 /\ __mod:T?3 /\ return:T?r ^ (T?1:complex /\ T?2:complex /\ T?3:NoneType /\ T?r:complex)',
		},
		'__rtruediv__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:complex /\ T?2:complex /\ T?r:complex)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:complex /\ T?2:TopType /\ T?r:bool)',
		},
		'__ne__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:complex /\ T?2:TopType /\ T?r:bool)',
		},
		'__neg__': {
			r'self:T?1 /\ return:T?r ^ (T?1:complex /\ T?r:complex)',
		},
		'__pos__': {
			r'self:T?1 /\ return:T?r ^ (T?1:complex /\ T?r:complex)',
		},
		'__abs__': {
			r'self:T?1 /\ return:T?r ^ (T?1:complex /\ T?r:float)',
		},
		'__hash__': {
			r'self:T?1 /\ return:T?r ^ (T?1:complex /\ T?r:int)',
		},
		'__bool__': {
			r'self:T?1 /\ return:T?r ^ (T?1:complex /\ T?r:bool)',
		},
	},
	'str': {
		'__new__': {
			r'cls:T?1 /\ object:T?2 /\ return:T?r ^ (T?1:str /\ T?2:TopType /\ T?r:str)',
			r'cls:T?1 /\ object:T?2 /\ encoding:T?3 /\ errors:T?4 /\ return:T?r ^ (T?1:str /\ T?2:bytes+bytearray+memoryview /\ T?3:str /\ T?4:str /\ T?r:str)',
		},
		'capitalize': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:str) \/ (T?1:str /\ T?r:str)',
		},
		'casefold': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:str) \/ (T?1:str /\ T?r:str)',
		},
		'center': {
			r'self:T?1 /\ __width:T?2 /\ __fillchar:T?3 /\ return:T?r ^ (T?1:str /\ T?2:SupportsIndex /\ T?3:str /\ T?r:str) \/ (T?1:str /\ T?2:SupportsIndex /\ T?3:str /\ T?r:str)',
		},
		'count': {
			r'self:T?1 /\ x:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'encode': {
			r'self:T?1 /\ encoding:T?2 /\ errors:T?3 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?3:str /\ T?r:bytes)',
		},
		'endswith': {
			r'self:T?1 /\ __suffix:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:str /\ T?2:tuple<str>+str /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:bool)',
		},
		'find': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'format': {
			r'self:T?1 /\ __va_args:T?2 /\ __kw_kwargs:T?3 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?3:str /\ T?r:str) \/ (T?1:str /\ T?2:TopType /\ T?3:TopType /\ T?r:str)',
		},
		'format_map': {
			r'self:T?1 /\ map:T?2 /\ return:T?r ^ (T?1:str /\ T?2:dict<str, int> /\ T?r:str)',
		},
		'index': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'isalnum': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:bool)',
		},
		'isalpha': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:bool)',
		},
		'isascii': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:bool)',
		},
		'isdecimal': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:bool)',
		},
		'isdigit': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:bool)',
		},
		'isidentifier': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:bool)',
		},
		'islower': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:bool)',
		},
		'isnumeric': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:bool)',
		},
		'isprintable': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:bool)',
		},
		'isspace': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:bool)',
		},
		'istitle': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:bool)',
		},
		'isupper': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:bool)',
		},
		'join': {
			r'self:T?1 /\ __iterable:T?2 /\ return:T?r ^ (T?1:str /\ T?2:Iterable<str> /\ T?r:str) \/ (T?1:str /\ T?2:Iterable<str> /\ T?r:str)',
		},
		'ljust': {
			r'self:T?1 /\ __width:T?2 /\ __fillchar:T?3 /\ return:T?r ^ (T?1:str /\ T?2:SupportsIndex /\ T?3:str /\ T?r:str) \/ (T?1:str /\ T?2:SupportsIndex /\ T?3:str /\ T?r:str)',
		},
		'lower': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:str) \/ (T?1:str /\ T?r:str)',
		},
		'lstrip': {
			r'self:T?1 /\ __chars:T?2 /\ return:T?r ^ (T?1:str /\ T?2:str+NoneType /\ T?r:str) \/ (T?1:str /\ T?2:str+NoneType /\ T?r:str)',
		},
		'partition': {
			r'self:T?1 /\ __sep:T?2 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?r:tuple<str>) \/ (T?1:str /\ T?2:str /\ T?r:tuple<str>)',
		},
		'replace': {
			r'self:T?1 /\ __old:T?2 /\ __new:T?3 /\ __count:T?4 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?3:str /\ T?4:SupportsIndex /\ T?r:str) \/ (T?1:str /\ T?2:str /\ T?3:str /\ T?4:SupportsIndex /\ T?r:str)',
		},
		'rfind': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'rindex': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'rjust': {
			r'self:T?1 /\ __width:T?2 /\ __fillchar:T?3 /\ return:T?r ^ (T?1:str /\ T?2:SupportsIndex /\ T?3:str /\ T?r:str) \/ (T?1:str /\ T?2:SupportsIndex /\ T?3:str /\ T?r:str)',
		},
		'rpartition': {
			r'self:T?1 /\ __sep:T?2 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?r:tuple<str>) \/ (T?1:str /\ T?2:str /\ T?r:tuple<str>)',
		},
		'rsplit': {
			r'self:T?1 /\ sep:T?2 /\ maxsplit:T?3 /\ return:T?r ^ (T?1:str /\ T?2:str+NoneType /\ T?3:SupportsIndex /\ T?r:list<str>) \/ (T?1:str /\ T?2:str+NoneType /\ T?3:SupportsIndex /\ T?r:list<str>)',
		},
		'rstrip': {
			r'self:T?1 /\ __chars:T?2 /\ return:T?r ^ (T?1:str /\ T?2:str+NoneType /\ T?r:str) \/ (T?1:str /\ T?2:str+NoneType /\ T?r:str)',
		},
		'split': {
			r'self:T?1 /\ sep:T?2 /\ maxsplit:T?3 /\ return:T?r ^ (T?1:str /\ T?2:str+NoneType /\ T?3:SupportsIndex /\ T?r:list<str>) \/ (T?1:str /\ T?2:str+NoneType /\ T?3:SupportsIndex /\ T?r:list<str>)',
		},
		'splitlines': {
			r'self:T?1 /\ keepends:T?2 /\ return:T?r ^ (T?1:str /\ T?2:bool /\ T?r:list<str>) \/ (T?1:str /\ T?2:bool /\ T?r:list<str>)',
		},
		'startswith': {
			r'self:T?1 /\ __prefix:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:str /\ T?2:tuple<str>+str /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:bool)',
		},
		'strip': {
			r'self:T?1 /\ __chars:T?2 /\ return:T?r ^ (T?1:str /\ T?2:str+NoneType /\ T?r:str) \/ (T?1:str /\ T?2:str+NoneType /\ T?r:str)',
		},
		'swapcase': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:str) \/ (T?1:str /\ T?r:str)',
		},
		'title': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:str) \/ (T?1:str /\ T?r:str)',
		},
		'translate': {
			r'self:T?1 /\ __table:T?2 /\ return:T?r ^ (T?1:str /\ T?2:dict<int, str+int> /\ T?r:str)',
		},
		'upper': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:str) \/ (T?1:str /\ T?r:str)',
		},
		'zfill': {
			r'self:T?1 /\ __width:T?2 /\ return:T?r ^ (T?1:str /\ T?2:SupportsIndex /\ T?r:str) \/ (T?1:str /\ T?2:SupportsIndex /\ T?r:str)',
		},
		'maketrans': {
			r'__x:T?1 /\ return:T?r ^ (T?1:dict<int, T?0>+dict<str, T?0>+dict<str+int, T?0> /\ T?r:dict<int, T?0>)',
			r'__x:T?1 /\ __y:T?2 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?r:dict<int, int>)',
			r'__x:T?1 /\ __y:T?2 /\ __z:T?3 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?3:str /\ T?r:dict<int, int+NoneType>)',
		},
		'__add__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?r:str) \/ (T?1:str /\ T?2:str /\ T?r:str)',
		},
		'__contains__': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?r:bool)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:str /\ T?2:TopType /\ T?r:bool)',
		},
		'__ge__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?r:bool)',
		},
		'__gt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?r:bool)',
		},
		'__hash__': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:int)',
		},
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:Iterator<str>) \/ (T?1:str /\ T?r:Iterator<str>)',
		},
		'__le__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?r:bool)',
		},
		'__len__': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:int)',
		},
		'__lt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:str /\ T?2:str /\ T?r:bool)',
		},
		'__mod__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:str /\ T?2:tuple<str>+str /\ T?r:str) \/ (T?1:str /\ T?2:TopType /\ T?r:str)',
		},
		'__mul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:str /\ T?2:SupportsIndex /\ T?r:str) \/ (T?1:str /\ T?2:SupportsIndex /\ T?r:str)',
		},
		'__ne__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:str /\ T?2:TopType /\ T?r:bool)',
		},
		'__rmul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:str /\ T?2:SupportsIndex /\ T?r:str) \/ (T?1:str /\ T?2:SupportsIndex /\ T?r:str)',
		},
		'__getnewargs__': {
			r'self:T?1 /\ return:T?r ^ (T?1:str /\ T?r:tuple<str>)',
		},
	},
	'bytes': {
		'__new__': {
			r'cls:T?1 /\ __string:T?2 /\ encoding:T?3 /\ errors:T?4 /\ return:T?r ^ (T?1:bytes /\ T?2:str /\ T?3:str /\ T?4:str /\ T?r:bytes)',
			r'cls:T?1 /\ __o:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+SupportsBytes+Iterable<SupportsIndex>+SupportsIndex /\ T?r:bytes)',
			r'cls:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bytes)',
		},
		'capitalize': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bytes)',
		},
		'center': {
			r'self:T?1 /\ __width:T?2 /\ __fillchar:T?3 /\ return:T?r ^ (T?1:bytes /\ T?2:SupportsIndex /\ T?3:bytes /\ T?r:bytes)',
		},
		'count': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+SupportsIndex /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'decode': {
			r'self:T?1 /\ encoding:T?2 /\ errors:T?3 /\ return:T?r ^ (T?1:bytes /\ T?2:str /\ T?3:str /\ T?r:str)',
		},
		'endswith': {
			r'self:T?1 /\ __suffix:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+tuple<bytes+bytearray+memoryview> /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:bool)',
		},
		'find': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+SupportsIndex /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'index': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+SupportsIndex /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'isalnum': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bool)',
		},
		'isalpha': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bool)',
		},
		'isascii': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bool)',
		},
		'isdigit': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bool)',
		},
		'islower': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bool)',
		},
		'isspace': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bool)',
		},
		'istitle': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bool)',
		},
		'isupper': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bool)',
		},
		'join': {
			r'self:T?1 /\ __iterable_of_bytes:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:Iterable<bytes+bytearray+memoryview> /\ T?r:bytes)',
		},
		'ljust': {
			r'self:T?1 /\ __width:T?2 /\ __fillchar:T?3 /\ return:T?r ^ (T?1:bytes /\ T?2:SupportsIndex /\ T?3:bytearray+bytes /\ T?r:bytes)',
		},
		'lower': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bytes)',
		},
		'lstrip': {
			r'self:T?1 /\ __bytes:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+NoneType /\ T?r:bytes)',
		},
		'partition': {
			r'self:T?1 /\ __sep:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview /\ T?r:tuple<bytes>)',
		},
		'replace': {
			r'self:T?1 /\ __old:T?2 /\ __new:T?3 /\ __count:T?4 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview /\ T?3:bytes+bytearray+memoryview /\ T?4:SupportsIndex /\ T?r:bytes)',
		},
		'rfind': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+SupportsIndex /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'rindex': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+SupportsIndex /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'rjust': {
			r'self:T?1 /\ __width:T?2 /\ __fillchar:T?3 /\ return:T?r ^ (T?1:bytes /\ T?2:SupportsIndex /\ T?3:bytearray+bytes /\ T?r:bytes)',
		},
		'rpartition': {
			r'self:T?1 /\ __sep:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview /\ T?r:tuple<bytes>)',
		},
		'rsplit': {
			r'self:T?1 /\ sep:T?2 /\ maxsplit:T?3 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+NoneType /\ T?3:SupportsIndex /\ T?r:list<bytes>)',
		},
		'rstrip': {
			r'self:T?1 /\ __bytes:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+NoneType /\ T?r:bytes)',
		},
		'split': {
			r'self:T?1 /\ sep:T?2 /\ maxsplit:T?3 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+NoneType /\ T?3:SupportsIndex /\ T?r:list<bytes>)',
		},
		'splitlines': {
			r'self:T?1 /\ keepends:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bool /\ T?r:list<bytes>)',
		},
		'startswith': {
			r'self:T?1 /\ __prefix:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+tuple<bytes+bytearray+memoryview> /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:bool)',
		},
		'strip': {
			r'self:T?1 /\ __bytes:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+NoneType /\ T?r:bytes)',
		},
		'swapcase': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bytes)',
		},
		'title': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bytes)',
		},
		'translate': {
			r'self:T?1 /\ __table:T?2 /\ delete:T?3 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+NoneType /\ T?3:bytes /\ T?r:bytes)',
		},
		'upper': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:bytes)',
		},
		'zfill': {
			r'self:T?1 /\ __width:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:SupportsIndex /\ T?r:bytes)',
		},
		'fromhex': {
			r'cls:T?1 /\ __string:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:str /\ T?r:bytes)',
		},
		'maketrans': {
			r'__frm:T?1 /\ __to:T?2 /\ return:T?r ^ (T?1:bytes+bytearray+memoryview /\ T?2:bytes+bytearray+memoryview /\ T?r:bytes)',
		},
		'__len__': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:int)',
		},
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:Iterator<int>)',
		},
		'__hash__': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:int)',
		},
		'__getitem__': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:SupportsIndex /\ T?r:int)',
		},
		'__add__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview /\ T?r:bytes)',
		},
		'__mul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:SupportsIndex /\ T?r:bytes)',
		},
		'__rmul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:SupportsIndex /\ T?r:bytes)',
		},
		'__mod__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:TopType /\ T?r:bytes)',
		},
		'__contains__': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes+bytearray+memoryview+SupportsIndex /\ T?r:bool)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:TopType /\ T?r:bool)',
		},
		'__ne__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:TopType /\ T?r:bool)',
		},
		'__lt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes /\ T?r:bool)',
		},
		'__le__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes /\ T?r:bool)',
		},
		'__gt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes /\ T?r:bool)',
		},
		'__ge__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:bytes /\ T?r:bool)',
		},
		'__getnewargs__': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytes /\ T?r:tuple<bytes>)',
		},
		'__buffer__': {
			r'self:T?1 /\ __flags:T?2 /\ return:T?r ^ (T?1:bytes /\ T?2:int /\ T?r:memoryview)',
		},
	},
	'bytearray': {
		'__init__': {
			r'self:T?1 /\ __ints:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+Iterable<SupportsIndex>+SupportsIndex /\ T?r:NoneType)',
			r'self:T?1 /\ __string:T?2 /\ encoding:T?3 /\ errors:T?4 /\ return:T?r ^ (T?1:bytearray /\ T?2:str /\ T?3:str /\ T?4:str /\ T?r:NoneType)',
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:NoneType)',
		},
		'append': {
			r'self:T?1 /\ __item:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:SupportsIndex /\ T?r:NoneType)',
		},
		'capitalize': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bytearray)',
		},
		'center': {
			r'self:T?1 /\ __width:T?2 /\ __fillchar:T?3 /\ return:T?r ^ (T?1:bytearray /\ T?2:SupportsIndex /\ T?3:bytes /\ T?r:bytearray)',
		},
		'count': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+SupportsIndex /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'copy': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bytearray)',
		},
		'decode': {
			r'self:T?1 /\ encoding:T?2 /\ errors:T?3 /\ return:T?r ^ (T?1:bytearray /\ T?2:str /\ T?3:str /\ T?r:str)',
		},
		'endswith': {
			r'self:T?1 /\ __suffix:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+tuple<bytes+bytearray+memoryview> /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:bool)',
		},
		'extend': {
			r'self:T?1 /\ __iterable_of_ints:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:Iterable<SupportsIndex> /\ T?r:NoneType)',
		},
		'find': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+SupportsIndex /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'index': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+SupportsIndex /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'insert': {
			r'self:T?1 /\ __index:T?2 /\ __item:T?3 /\ return:T?r ^ (T?1:bytearray /\ T?2:SupportsIndex /\ T?3:SupportsIndex /\ T?r:NoneType)',
		},
		'isalnum': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bool)',
		},
		'isalpha': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bool)',
		},
		'isascii': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bool)',
		},
		'isdigit': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bool)',
		},
		'islower': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bool)',
		},
		'isspace': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bool)',
		},
		'istitle': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bool)',
		},
		'isupper': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bool)',
		},
		'join': {
			r'self:T?1 /\ __iterable_of_bytes:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:Iterable<bytes+bytearray+memoryview> /\ T?r:bytearray)',
		},
		'ljust': {
			r'self:T?1 /\ __width:T?2 /\ __fillchar:T?3 /\ return:T?r ^ (T?1:bytearray /\ T?2:SupportsIndex /\ T?3:bytearray+bytes /\ T?r:bytearray)',
		},
		'lower': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bytearray)',
		},
		'lstrip': {
			r'self:T?1 /\ __bytes:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+NoneType /\ T?r:bytearray)',
		},
		'partition': {
			r'self:T?1 /\ __sep:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview /\ T?r:tuple<bytearray>)',
		},
		'pop': {
			r'self:T?1 /\ __index:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:int /\ T?r:int)',
		},
		'remove': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:int /\ T?r:NoneType)',
		},
		'replace': {
			r'self:T?1 /\ __old:T?2 /\ __new:T?3 /\ __count:T?4 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview /\ T?3:bytes+bytearray+memoryview /\ T?4:SupportsIndex /\ T?r:bytearray)',
		},
		'rfind': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+SupportsIndex /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'rindex': {
			r'self:T?1 /\ __sub:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+SupportsIndex /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:int)',
		},
		'rjust': {
			r'self:T?1 /\ __width:T?2 /\ __fillchar:T?3 /\ return:T?r ^ (T?1:bytearray /\ T?2:SupportsIndex /\ T?3:bytearray+bytes /\ T?r:bytearray)',
		},
		'rpartition': {
			r'self:T?1 /\ __sep:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview /\ T?r:tuple<bytearray>)',
		},
		'rsplit': {
			r'self:T?1 /\ sep:T?2 /\ maxsplit:T?3 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+NoneType /\ T?3:SupportsIndex /\ T?r:list<bytearray>)',
		},
		'rstrip': {
			r'self:T?1 /\ __bytes:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+NoneType /\ T?r:bytearray)',
		},
		'split': {
			r'self:T?1 /\ sep:T?2 /\ maxsplit:T?3 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+NoneType /\ T?3:SupportsIndex /\ T?r:list<bytearray>)',
		},
		'splitlines': {
			r'self:T?1 /\ keepends:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bool /\ T?r:list<bytearray>)',
		},
		'startswith': {
			r'self:T?1 /\ __prefix:T?2 /\ __start:T?3 /\ __end:T?4 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+tuple<bytes+bytearray+memoryview> /\ T?3:SupportsIndex+NoneType /\ T?4:SupportsIndex+NoneType /\ T?r:bool)',
		},
		'strip': {
			r'self:T?1 /\ __bytes:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+NoneType /\ T?r:bytearray)',
		},
		'swapcase': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bytearray)',
		},
		'title': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bytearray)',
		},
		'translate': {
			r'self:T?1 /\ __table:T?2 /\ delete:T?3 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+NoneType /\ T?3:bytes /\ T?r:bytearray)',
		},
		'upper': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:bytearray)',
		},
		'zfill': {
			r'self:T?1 /\ __width:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:SupportsIndex /\ T?r:bytearray)',
		},
		'fromhex': {
			r'cls:T?1 /\ __string:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:str /\ T?r:bytearray)',
		},
		'maketrans': {
			r'__frm:T?1 /\ __to:T?2 /\ return:T?r ^ (T?1:bytes+bytearray+memoryview /\ T?2:bytes+bytearray+memoryview /\ T?r:bytes)',
		},
		'__len__': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:int)',
		},
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:Iterator<int>)',
		},
		'__getitem__': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:SupportsIndex /\ T?r:int)',
		},
		'__setitem__': {
			r'self:T?1 /\ __key:T?2 /\ __value:T?3 /\ return:T?r ^ (T?1:bytearray /\ T?2:SupportsIndex /\ T?3:SupportsIndex /\ T?r:NoneType)',
		},
		'__add__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview /\ T?r:bytearray)',
		},
		'__iadd__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview /\ T?r:bytearray)',
		},
		'__mul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:SupportsIndex /\ T?r:bytearray)',
		},
		'__rmul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:SupportsIndex /\ T?r:bytearray)',
		},
		'__imul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:SupportsIndex /\ T?r:bytearray)',
		},
		'__mod__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:TopType /\ T?r:bytes)',
		},
		'__contains__': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview+SupportsIndex /\ T?r:bool)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:TopType /\ T?r:bool)',
		},
		'__ne__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:TopType /\ T?r:bool)',
		},
		'__lt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview /\ T?r:bool)',
		},
		'__le__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview /\ T?r:bool)',
		},
		'__gt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview /\ T?r:bool)',
		},
		'__ge__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:bytes+bytearray+memoryview /\ T?r:bool)',
		},
		'__alloc__': {
			r'self:T?1 /\ return:T?r ^ (T?1:bytearray /\ T?r:int)',
		},
		'__buffer__': {
			r'self:T?1 /\ __flags:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:int /\ T?r:memoryview)',
		},
		'__release_buffer__': {
			r'self:T?1 /\ __buffer:T?2 /\ return:T?r ^ (T?1:bytearray /\ T?2:memoryview /\ T?r:NoneType)',
		},
	},
	'bool': {
		'__new__': {
			r'cls:T?1 /\ __o:T?2 /\ return:T?r ^ (T?1:bool /\ T?2:TopType /\ T?r:bool)',
		},
		'__and__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bool /\ T?2:bool /\ T?r:bool) \/ (T?1:bool /\ T?2:int /\ T?r:int)',
		},
		'__or__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bool /\ T?2:bool /\ T?r:bool) \/ (T?1:bool /\ T?2:int /\ T?r:int)',
		},
		'__xor__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bool /\ T?2:bool /\ T?r:bool) \/ (T?1:bool /\ T?2:int /\ T?r:int)',
		},
		'__rand__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bool /\ T?2:bool /\ T?r:bool) \/ (T?1:bool /\ T?2:int /\ T?r:int)',
		},
		'__ror__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bool /\ T?2:bool /\ T?r:bool) \/ (T?1:bool /\ T?2:int /\ T?r:int)',
		},
		'__rxor__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:bool /\ T?2:bool /\ T?r:bool) \/ (T?1:bool /\ T?2:int /\ T?r:int)',
		},
		'__getnewargs__': {
			r'self:T?1 /\ return:T?r ^ (T?1:bool /\ T?r:tuple<int>)',
		},
	},
	'slice': {
		'__init__': {
			r'self:T?1 /\ __stop:T?2 /\ return:T?r ^ (T?1:slice /\ T?2:TopType /\ T?r:NoneType)',
			r'self:T?1 /\ __start:T?2 /\ __stop:T?3 /\ __step:T?4 /\ return:T?r ^ (T?1:slice /\ T?2:TopType /\ T?3:TopType /\ T?4:TopType /\ T?r:NoneType)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:slice /\ T?2:TopType /\ T?r:bool)',
		},
		'indices': {
			r'self:T?1 /\ __len:T?2 /\ return:T?r ^ (T?1:slice /\ T?2:SupportsIndex /\ T?r:tuple<int>)',
		},
	},
	'tuple': {
		'__new__': {
			r'cls:T?1 /\ __iterable:T?2 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:Iterable<T?co> /\ T?r:tuple<T?co>)',
		},
		'__len__': {
			r'self:T?1 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?r:int)',
		},
		'__contains__': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:TopType /\ T?r:bool)',
		},
		'__getitem__': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:SupportsIndex /\ T?r:T?co)',
		},
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?r:Iterator<T?co>)',
		},
		'__lt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:tuple<T?co> /\ T?r:bool)',
		},
		'__le__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:tuple<T?co> /\ T?r:bool)',
		},
		'__gt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:tuple<T?co> /\ T?r:bool)',
		},
		'__ge__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:tuple<T?co> /\ T?r:bool)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:TopType /\ T?r:bool)',
		},
		'__hash__': {
			r'self:T?1 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?r:int)',
		},
		'__add__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:tuple<T?co> /\ T?r:tuple<T?co>) \/ (T?1:tuple<T?co> /\ T?2:tuple<T?0> /\ T?r:tuple<T?0+T?co>)',
		},
		'__mul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:SupportsIndex /\ T?r:tuple<T?co>)',
		},
		'__rmul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:SupportsIndex /\ T?r:tuple<T?co>)',
		},
		'count': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:TopType /\ T?r:int)',
		},
		'index': {
			r'self:T?1 /\ __value:T?2 /\ __start:T?3 /\ __stop:T?4 /\ return:T?r ^ (T?1:tuple<T?co> /\ T?2:TopType /\ T?3:SupportsIndex /\ T?4:SupportsIndex /\ T?r:int)',
		},
	},
	'list': {
		'__init__': {
			r'self:T?1 /\ return:T?r ^ (T?1:list<T?0> /\ T?r:NoneType)',
			r'self:T?1 /\ __iterable:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:Iterable<T?0> /\ T?r:NoneType)',
		},
		'copy': {
			r'self:T?1 /\ return:T?r ^ (T?1:list<T?0> /\ T?r:list<T?0>)',
		},
		'append': {
			r'self:T?1 /\ __object:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:T?0 /\ T?r:NoneType)',
		},
		'extend': {
			r'self:T?1 /\ __iterable:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:Iterable<T?0> /\ T?r:NoneType)',
		},
		'pop': {
			r'self:T?1 /\ __index:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?r:T?0)',
		},
		'index': {
			r'self:T?1 /\ __value:T?2 /\ __start:T?3 /\ __stop:T?4 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:T?0 /\ T?3:SupportsIndex /\ T?4:SupportsIndex /\ T?r:int)',
		},
		'count': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:T?0 /\ T?r:int)',
		},
		'insert': {
			r'self:T?1 /\ __index:T?2 /\ __object:T?3 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?3:T?0 /\ T?r:NoneType)',
		},
		'remove': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:T?0 /\ T?r:NoneType)',
		},
		'sort': {
			r'self:T?1 /\ __ko_key:T?2 /\ __ko_reverse:T?3 /\ return:T?r ^ (T?1:list<SupportsRichComparisonT> /\ T?2:NoneType /\ T?3:bool /\ T?r:NoneType)',
		},
		'__len__': {
			r'self:T?1 /\ return:T?r ^ (T?1:list<T?0> /\ T?r:int)',
		},
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:list<T?0> /\ T?r:Iterator<T?0>)',
		},
		'__getitem__': {
			r'self:T?1 /\ __i:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?r:T?0)',
		},
		'__setitem__': {
			r'self:T?1 /\ __key:T?2 /\ __value:T?3 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?3:T?0 /\ T?r:NoneType)',
		},
		'__add__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:list<T?0> /\ T?r:list<T?0>) \/ (T?1:list<T?0> /\ T?2:list<T?s> /\ T?r:list<T?0+T?s>)',
		},
		'__iadd__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:Iterable<T?0> /\ T?r:list<T?0>)',
		},
		'__mul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?r:list<T?0>)',
		},
		'__rmul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?r:list<T?0>)',
		},
		'__imul__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:SupportsIndex /\ T?r:list<T?0>)',
		},
		'__contains__': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:TopType /\ T?r:bool)',
		},
		'__reversed__': {
			r'self:T?1 /\ return:T?r ^ (T?1:list<T?0> /\ T?r:Iterator<T?0>)',
		},
		'__gt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:list<T?0> /\ T?r:bool)',
		},
		'__ge__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:list<T?0> /\ T?r:bool)',
		},
		'__lt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:list<T?0> /\ T?r:bool)',
		},
		'__le__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:list<T?0> /\ T?r:bool)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:list<T?0> /\ T?2:TopType /\ T?r:bool)',
		},
	},
	'dict': {
		'__init__': {
			r'self:T?1 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?r:NoneType)',
			r'self:T?1 /\ __map:T?2 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?2:dict<T?K, T?V> /\ T?r:NoneType)',
			r'self:T?1 /\ __map:T?2 /\ __kw_kwargs:T?3 /\ return:T?r ^ (T?1:dict<str, T?V> /\ T?2:dict<str, T?V> /\ T?3:T?V /\ T?r:NoneType)',
			r'self:T?1 /\ __iterable:T?2 /\ __kw_kwargs:T?3 /\ return:T?r ^ (T?1:dict<str, T?V> /\ T?2:Iterable<tuple<str+T?V>> /\ T?3:T?V /\ T?r:NoneType)',
			r'self:T?1 /\ __iterable:T?2 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?2:Iterable<tuple<T?K+T?V>> /\ T?r:NoneType) \/ (T?1:dict<str, str> /\ T?2:Iterable<list<str>> /\ T?r:NoneType) \/ (T?1:dict<bytes, bytes> /\ T?2:Iterable<list<bytes>> /\ T?r:NoneType)',
			r'self:T?1 /\ __kw_kwargs:T?2 /\ return:T?r ^ (T?1:dict<str, T?V> /\ T?2:T?V /\ T?r:NoneType)',
		},
		'__new__': {
			r'cls:T?1 /\ __va_args:T?2 /\ __kw_kwargs:T?3 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?2:TopType /\ T?3:TopType /\ T?r:dict<T?K, T?V>)',
		},
		'copy': {
			r'self:T?1 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?r:dict<T?K, T?V>)',
		},
		'keys': {
			r'self:T?1 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?r:list<T?K>)',
		},
		'values': {
			r'self:T?1 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?r:list<T?V>)',
		},
		'items': {
			r'self:T?1 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?r:list<tuple<T?K+T?V>>)',
		},
		'fromkeys': {
			r'cls:T?1 /\ __iterable:T?2 /\ __value:T?3 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?2:Iterable<T?0> /\ T?3:NoneType /\ T?r:dict<T?0, NoneType+TopType>) \/ (T?1:dict<T?K, T?V> /\ T?2:Iterable<T?0> /\ T?3:T?s /\ T?r:dict<T?0, T?s>)',
		},
		'get': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?2:T?K /\ T?r:T?V+NoneType)',
			r'self:T?1 /\ __key:T?2 /\ __default:T?3 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?2:T?K /\ T?3:T?V /\ T?r:T?V) \/ (T?1:dict<T?K, T?V> /\ T?2:T?K /\ T?3:T?0 /\ T?r:T?0+T?V)',
		},
		'pop': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?2:T?K /\ T?r:T?V)',
			r'self:T?1 /\ __key:T?2 /\ __default:T?3 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?2:T?K /\ T?3:T?V /\ T?r:T?V) \/ (T?1:dict<T?K, T?V> /\ T?2:T?K /\ T?3:T?0 /\ T?r:T?0+T?V)',
		},
		'__len__': {
			r'self:T?1 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?r:int)',
		},
		'__getitem__': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?2:T?K /\ T?r:T?V)',
		},
		'__setitem__': {
			r'self:T?1 /\ __key:T?2 /\ __value:T?3 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?2:T?K /\ T?3:T?V /\ T?r:NoneType)',
		},
		'__delitem__': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?2:T?K /\ T?r:NoneType)',
		},
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?r:Iterator<T?K>)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:dict<T?K, T?V> /\ T?2:TopType /\ T?r:bool)',
		},
	},
	'set': {
		'__init__': {
			r'self:T?1 /\ __iterable:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:Iterable<T?0> /\ T?r:NoneType)',
			r'self:T?1 /\ return:T?r ^ (T?1:set<T?0> /\ T?r:NoneType)',
		},
		'add': {
			r'self:T?1 /\ __element:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:T?0 /\ T?r:NoneType)',
		},
		'copy': {
			r'self:T?1 /\ return:T?r ^ (T?1:set<T?0> /\ T?r:set<T?0>)',
		},
		'difference': {
			r'self:T?1 /\ __va_s:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:Iterable<TopType> /\ T?r:set<T?0>)',
		},
		'difference_update': {
			r'self:T?1 /\ __va_s:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:Iterable<TopType> /\ T?r:NoneType)',
		},
		'discard': {
			r'self:T?1 /\ __element:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:T?0 /\ T?r:NoneType)',
		},
		'intersection': {
			r'self:T?1 /\ __va_s:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:Iterable<TopType> /\ T?r:set<T?0>)',
		},
		'intersection_update': {
			r'self:T?1 /\ __va_s:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:Iterable<TopType> /\ T?r:NoneType)',
		},
		'isdisjoint': {
			r'self:T?1 /\ __s:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:Iterable<TopType> /\ T?r:bool)',
		},
		'issubset': {
			r'self:T?1 /\ __s:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:Iterable<TopType> /\ T?r:bool)',
		},
		'issuperset': {
			r'self:T?1 /\ __s:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:Iterable<TopType> /\ T?r:bool)',
		},
		'remove': {
			r'self:T?1 /\ __element:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:T?0 /\ T?r:NoneType)',
		},
		'symmetric_difference': {
			r'self:T?1 /\ __s:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:Iterable<T?0> /\ T?r:set<T?0>)',
		},
		'symmetric_difference_update': {
			r'self:T?1 /\ __s:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:Iterable<T?0> /\ T?r:NoneType)',
		},
		'union': {
			r'self:T?1 /\ __va_s:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:Iterable<T?s> /\ T?r:set<T?0+T?s>)',
		},
		'update': {
			r'self:T?1 /\ __va_s:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:Iterable<T?0> /\ T?r:NoneType)',
		},
		'__len__': {
			r'self:T?1 /\ return:T?r ^ (T?1:set<T?0> /\ T?r:int)',
		},
		'__contains__': {
			r'self:T?1 /\ __o:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:TopType /\ T?r:bool)',
		},
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:set<T?0> /\ T?r:Iterator<T?0>)',
		},
		'__and__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:set<TopType> /\ T?r:set<T?0>)',
		},
		'__iand__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:set<TopType> /\ T?r:set<T?0>)',
		},
		'__or__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:set<T?s> /\ T?r:set<T?0+T?s>)',
		},
		'__ior__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:set<T?0> /\ T?r:set<T?0>)',
		},
		'__sub__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:set<T?0+NoneType> /\ T?r:set<T?0>)',
		},
		'__isub__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:set<TopType> /\ T?r:set<T?0>)',
		},
		'__xor__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:set<T?s> /\ T?r:set<T?0+T?s>)',
		},
		'__ixor__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:set<T?0> /\ T?r:set<T?0>)',
		},
		'__le__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:set<TopType> /\ T?r:bool)',
		},
		'__lt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:set<TopType> /\ T?r:bool)',
		},
		'__ge__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:set<TopType> /\ T?r:bool)',
		},
		'__gt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:set<TopType> /\ T?r:bool)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:set<T?0> /\ T?2:TopType /\ T?r:bool)',
		},
	},
	'frozenset': {
		'__new__': {
			r'cls:T?1 /\ __iterable:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:Iterable<T?co> /\ T?r:frozenset<T?co>)',
			r'cls:T?1 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?r:frozenset<T?co>)',
		},
		'copy': {
			r'self:T?1 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?r:frozenset<T?co>)',
		},
		'difference': {
			r'self:T?1 /\ __va_s:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:Iterable<TopType> /\ T?r:frozenset<T?co>)',
		},
		'intersection': {
			r'self:T?1 /\ __va_s:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:Iterable<TopType> /\ T?r:frozenset<T?co>)',
		},
		'isdisjoint': {
			r'self:T?1 /\ __s:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:Iterable<T?co> /\ T?r:bool)',
		},
		'issubset': {
			r'self:T?1 /\ __s:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:Iterable<TopType> /\ T?r:bool)',
		},
		'issuperset': {
			r'self:T?1 /\ __s:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:Iterable<TopType> /\ T?r:bool)',
		},
		'symmetric_difference': {
			r'self:T?1 /\ __s:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:Iterable<T?co> /\ T?r:frozenset<T?co>)',
		},
		'union': {
			r'self:T?1 /\ __va_s:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:Iterable<T?s> /\ T?r:frozenset<T?s+T?co>)',
		},
		'__len__': {
			r'self:T?1 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?r:int)',
		},
		'__contains__': {
			r'self:T?1 /\ __o:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:TopType /\ T?r:bool)',
		},
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?r:Iterator<T?co>)',
		},
		'__and__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:set<T?co> /\ T?r:frozenset<T?co>)',
		},
		'__or__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:set<T?s> /\ T?r:frozenset<T?s+T?co>)',
		},
		'__sub__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:set<T?co> /\ T?r:frozenset<T?co>)',
		},
		'__xor__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:set<T?s> /\ T?r:frozenset<T?s+T?co>)',
		},
		'__le__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:set<TopType> /\ T?r:bool)',
		},
		'__lt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:set<TopType> /\ T?r:bool)',
		},
		'__ge__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:set<TopType> /\ T?r:bool)',
		},
		'__gt__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:set<TopType> /\ T?r:bool)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?2:TopType /\ T?r:bool)',
		},
		'__hash__': {
			r'self:T?1 /\ return:T?r ^ (T?1:frozenset<T?co> /\ T?r:int)',
		},
	},
	'range': {
		'start': {
			r'self:T?1 /\ return:T?r ^ (T?1:range<int> /\ T?r:int)',
		},
		'stop': {
			r'self:T?1 /\ return:T?r ^ (T?1:range<int> /\ T?r:int)',
		},
		'step': {
			r'self:T?1 /\ return:T?r ^ (T?1:range<int> /\ T?r:int)',
		},
		'__init__': {
			r'self:T?1 /\ __stop:T?2 /\ return:T?r ^ (T?1:range<int> /\ T?2:SupportsIndex /\ T?r:NoneType)',
			r'self:T?1 /\ __start:T?2 /\ __stop:T?3 /\ __step:T?4 /\ return:T?r ^ (T?1:range<int> /\ T?2:SupportsIndex /\ T?3:SupportsIndex /\ T?4:SupportsIndex /\ T?r:NoneType)',
		},
		'count': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:range<int> /\ T?2:int /\ T?r:int)',
		},
		'index': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:range<int> /\ T?2:int /\ T?r:int)',
		},
		'__len__': {
			r'self:T?1 /\ return:T?r ^ (T?1:range<int> /\ T?r:int)',
		},
		'__eq__': {
			r'self:T?1 /\ __value:T?2 /\ return:T?r ^ (T?1:range<int> /\ T?2:TopType /\ T?r:bool)',
		},
		'__hash__': {
			r'self:T?1 /\ return:T?r ^ (T?1:range<int> /\ T?r:int)',
		},
		'__contains__': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:range<int> /\ T?2:TopType /\ T?r:bool)',
		},
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:range<int> /\ T?r:Iterator<int>)',
		},
		'__getitem__': {
			r'self:T?1 /\ __key:T?2 /\ return:T?r ^ (T?1:range<int> /\ T?2:SupportsIndex /\ T?r:int)',
		},
		'__reversed__': {
			r'self:T?1 /\ return:T?r ^ (T?1:range<int> /\ T?r:Iterator<int>)',
		},
	},
	'property': {
		'__set__': {
			r'self:T?1 /\ __instance:T?2 /\ __value:T?3 /\ return:T?r ^ (T?1:property /\ T?2:TopType /\ T?3:TopType /\ T?r:NoneType)',
		},
		'__delete__': {
			r'self:T?1 /\ __instance:T?2 /\ return:T?r ^ (T?1:property /\ T?2:TopType /\ T?r:NoneType)',
		},
	},
	'_NotImplementedType': {
	},
	'filter': {
		'__init__': {
			r'self:T?1 /\ __function:T?2 /\ __iterable:T?3 /\ return:T?r ^ (T?1:filter<T?0> /\ T?2:NoneType /\ T?3:Iterable<T?0+NoneType> /\ T?r:NoneType)',
		},
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:filter<T?0> /\ T?r:filter<T?0>)',
		},
		'__next__': {
			r'self:T?1 /\ return:T?r ^ (T?1:filter<T?0> /\ T?r:T?0)',
		},
	},
	'map': {
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:map<T?s> /\ T?r:map<T?s>)',
		},
		'__next__': {
			r'self:T?1 /\ return:T?r ^ (T?1:map<T?s> /\ T?r:T?s)',
		},
	},
	'reversed': {
		'__init__': {
			r'self:T?1 /\ __sequence:T?2 /\ return:T?r ^ (T?1:reversed<T?0> /\ T?2:Reversible<T?0> /\ T?r:NoneType) \/ (T?1:reversed<T?0> /\ T?2:SupportsLenAndGetItem<T?0> /\ T?r:NoneType)',
		},
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:reversed<T?0> /\ T?r:reversed<T?0>)',
		},
		'__next__': {
			r'self:T?1 /\ return:T?r ^ (T?1:reversed<T?0> /\ T?r:T?0)',
		},
		'__length_hint__': {
			r'self:T?1 /\ return:T?r ^ (T?1:reversed<T?0> /\ T?r:int)',
		},
	},
	'zip': {
		'__iter__': {
			r'self:T?1 /\ return:T?r ^ (T?1:zip<T?co> /\ T?r:zip<T?co>)',
		},
		'__next__': {
			r'self:T?1 /\ return:T?r ^ (T?1:zip<T?co> /\ T?r:T?co)',
		},
	},
	'BaseException': {
		'__init__': {
			r'self:T?1 /\ __va_args:T?2 /\ return:T?r ^ (T?1:BaseException /\ T?2:TopType /\ T?r:NoneType)',
		},
		'__setstate__': {
			r'self:T?1 /\ __state:T?2 /\ return:T?r ^ (T?1:BaseException /\ T?2:dict<str, TopType>+NoneType /\ T?r:NoneType)',
		},
	},
	'GeneratorExit': {
	},
	'KeyboardInterrupt': {
	},
	'SystemExit': {
	},
	'Exception': {
	},
	'StopIteration': {
	},
	'OSError': {
	},
	'ArithmeticError': {
	},
	'AssertionError': {
	},
	'AttributeError': {
	},
	'BufferError': {
	},
	'EOFError': {
	},
	'ImportError': {
		'__init__': {
			r'self:T?1 /\ __va_args:T?2 /\ __ko_name:T?3 /\ __ko_path:T?4 /\ return:T?r ^ (T?1:ImportError /\ T?2:TopType /\ T?3:str+NoneType /\ T?4:str+NoneType /\ T?r:NoneType)',
		},
	},
	'LookupError': {
	},
	'MemoryError': {
	},
	'NameError': {
	},
	'ReferenceError': {
	},
	'RuntimeError': {
	},
	'StopAsyncIteration': {
	},
	'SyntaxError': {
	},
	'SystemError': {
	},
	'TypeError': {
	},
	'ValueError': {
	},
	'FloatingPointError': {
	},
	'OverflowError': {
	},
	'ZeroDivisionError': {
	},
	'ModuleNotFoundError': {
	},
	'IndexError': {
	},
	'KeyError': {
	},
	'UnboundLocalError': {
	},
	'BlockingIOError': {
	},
	'ChildProcessError': {
	},
	'ConnectionError': {
	},
	'BrokenPipeError': {
	},
	'ConnectionAbortedError': {
	},
	'ConnectionRefusedError': {
	},
	'ConnectionResetError': {
	},
	'FileExistsError': {
	},
	'FileNotFoundError': {
	},
	'InterruptedError': {
	},
	'IsADirectoryError': {
	},
	'NotADirectoryError': {
	},
	'PermissionError': {
	},
	'ProcessLookupError': {
	},
	'TimeoutError': {
	},
	'NotImplementedError': {
	},
	'RecursionError': {
	},
	'IndentationError': {
	},
	'TabError': {
	},
	'UnicodeError': {
	},
	'UnicodeDecodeError': {
		'__init__': {
			r'self:T?1 /\ __encoding:T?2 /\ __object:T?3 /\ __start:T?4 /\ __end:T?5 /\ __reason:T?6 /\ return:T?r ^ (T?1:UnicodeDecodeError /\ T?2:str /\ T?3:bytes+bytearray+memoryview /\ T?4:int /\ T?5:int /\ T?6:str /\ T?r:NoneType)',
		},
	},
	'UnicodeEncodeError': {
		'__init__': {
			r'self:T?1 /\ __encoding:T?2 /\ __object:T?3 /\ __start:T?4 /\ __end:T?5 /\ __reason:T?6 /\ return:T?r ^ (T?1:UnicodeEncodeError /\ T?2:str /\ T?3:str /\ T?4:int /\ T?5:int /\ T?6:str /\ T?r:NoneType)',
		},
	},
	'UnicodeTranslateError': {
		'__init__': {
			r'self:T?1 /\ __object:T?2 /\ __start:T?3 /\ __end:T?4 /\ __reason:T?5 /\ return:T?r ^ (T?1:UnicodeTranslateError /\ T?2:str /\ T?3:int /\ T?4:int /\ T?5:str /\ T?r:NoneType)',
		},
	},
	'Warning': {
	},
	'UserWarning': {
	},
	'DeprecationWarning': {
	},
	'SyntaxWarning': {
	},
	'RuntimeWarning': {
	},
	'FutureWarning': {
	},
	'PendingDeprecationWarning': {
	},
	'ImportWarning': {
	},
	'UnicodeWarning': {
	},
	'BytesWarning': {
	},
	'ResourceWarning': {
	},
	'EncodingWarning': {
	},
	'builtins': {
		'abs': {
			r'__x:T?1 /\ return:T?r ^ (T?1:SupportsAbs<T?0> /\ T?r:T?0)',
		},
		'all': {
			r'__iterable:T?1 /\ return:T?r ^ (T?1:Iterable<TopType> /\ T?r:bool)',
		},
		'any': {
			r'__iterable:T?1 /\ return:T?r ^ (T?1:Iterable<TopType> /\ T?r:bool)',
		},
		'ascii': {
			r'__obj:T?1 /\ return:T?r ^ (T?1:TopType /\ T?r:str)',
		},
		'bin': {
			r'__number:T?1 /\ return:T?r ^ (T?1:int+SupportsIndex /\ T?r:str)',
		},
		'breakpoint': {
			r'__va_args:T?1 /\ __kw_kws:T?2 /\ return:T?r ^ (T?1:TopType /\ T?2:TopType /\ T?r:NoneType)',
		},
		'chr': {
			r'__i:T?1 /\ return:T?r ^ (T?1:int /\ T?r:str)',
		},
		'copyright': {
			r'return:T?r ^ (T?r:NoneType)',
		},
		'credits': {
			r'return:T?r ^ (T?r:NoneType)',
		},
		'delattr': {
			r'__obj:T?1 /\ __name:T?2 /\ return:T?r ^ (T?1:TopType /\ T?2:str /\ T?r:NoneType)',
		},
		'dir': {
			r'__o:T?1 /\ return:T?r ^ (T?1:TopType /\ T?r:list<str>)',
		},
		'divmod': {
			r'__x:T?1 /\ __y:T?2 /\ return:T?r ^ (T?1:T?contra /\ T?2:SupportsRDivMod<T?contra+T?co> /\ T?r:T?co)',
			r'__x:T?1 /\ __y:T?2 /\ return:T?r ^ (T?1:SupportsDivMod<T?contra+T?co> /\ T?2:T?contra /\ T?r:T?co)',
		},
		'format': {
			r'__value:T?1 /\ __format_spec:T?2 /\ return:T?r ^ (T?1:TopType /\ T?2:str /\ T?r:str)',
		},
		'getattr': {
			r'__o:T?1 /\ __name:T?2 /\ __default:T?3 /\ return:T?r ^ (T?1:TopType /\ T?2:str /\ T?3:NoneType /\ T?r:NoneType+TopType)',
			r'__o:T?1 /\ __name:T?2 /\ __default:T?3 /\ return:T?r ^ (T?1:TopType /\ T?2:str /\ T?3:bool /\ T?r:bool+TopType)',
			r'__o:T?1 /\ name:T?2 /\ __default:T?3 /\ return:T?r ^ (T?1:TopType /\ T?2:str /\ T?3:dict<TopType, TopType> /\ T?r:dict<TopType, TopType>+TopType)',
			r'__o:T?1 /\ name:T?2 /\ __default:T?3 /\ return:T?r ^ (T?1:TopType /\ T?2:str /\ T?3:list<TopType> /\ T?r:list<TopType>+TopType)',
			r'__o:T?1 /\ __name:T?2 /\ __default:T?3 /\ return:T?r ^ (T?1:TopType /\ T?2:str /\ T?3:T?0 /\ T?r:T?0+TopType)',
		},
		'globals': {
			r'return:T?r ^ (T?r:dict<str, TopType>)',
		},
		'hasattr': {
			r'__obj:T?1 /\ __name:T?2 /\ return:T?r ^ (T?1:TopType /\ T?2:str /\ T?r:bool)',
		},
		'hash': {
			r'__obj:T?1 /\ return:T?r ^ (T?1:TopType /\ T?r:int)',
		},
		'help': {
			r'request:T?1 /\ return:T?r ^ (T?1:TopType /\ T?r:NoneType)',
		},
		'hex': {
			r'__number:T?1 /\ return:T?r ^ (T?1:int+SupportsIndex /\ T?r:str)',
		},
		'id': {
			r'__obj:T?1 /\ return:T?r ^ (T?1:TopType /\ T?r:int)',
		},
		'input': {
			r'__prompt:T?1 /\ return:T?r ^ (T?1:TopType /\ T?r:str)',
		},
		'iter': {
			r'__iterable:T?1 /\ return:T?r ^ (T?1:GetItemIterable<T?0> /\ T?r:Iterator<T?0>)',
			r'__iterable:T?1 /\ return:T?r ^ (T?1:Iterable<SupportsNext> /\ T?r:SupportsNext)',
		},
		'len': {
			r'__obj:T?1 /\ return:T?r ^ (T?1:SupportsLen /\ T?r:int)',
		},
		'license': {
			r'return:T?r ^ (T?r:NoneType)',
		},
		'locals': {
			r'return:T?r ^ (T?r:dict<str, TopType>)',
		},
		'max': {
			r'__iterable:T?1 /\ __ko_key:T?2 /\ return:T?r ^ (T?1:Iterable<SupportsRichComparisonT> /\ T?2:NoneType /\ T?r:SupportsRichComparisonT)',
			r'__iterable:T?1 /\ __ko_key:T?2 /\ __ko_default:T?3 /\ return:T?r ^ (T?1:Iterable<SupportsRichComparisonT> /\ T?2:NoneType /\ T?3:T?0 /\ T?r:SupportsRichComparisonT+T?0)',
			r'__arg1:T?1 /\ __arg2:T?2 /\ __va__args:T?3 /\ __ko_key:T?4 /\ return:T?r ^ (T?1:SupportsRichComparisonT /\ T?2:SupportsRichComparisonT /\ T?3:SupportsRichComparisonT /\ T?4:NoneType /\ T?r:SupportsRichComparisonT)',
		},
		'min': {
			r'__iterable:T?1 /\ __ko_key:T?2 /\ return:T?r ^ (T?1:Iterable<SupportsRichComparisonT> /\ T?2:NoneType /\ T?r:SupportsRichComparisonT)',
			r'__iterable:T?1 /\ __ko_key:T?2 /\ __ko_default:T?3 /\ return:T?r ^ (T?1:Iterable<SupportsRichComparisonT> /\ T?2:NoneType /\ T?3:T?0 /\ T?r:SupportsRichComparisonT+T?0)',
			r'__arg1:T?1 /\ __arg2:T?2 /\ __va__args:T?3 /\ __ko_key:T?4 /\ return:T?r ^ (T?1:SupportsRichComparisonT /\ T?2:SupportsRichComparisonT /\ T?3:SupportsRichComparisonT /\ T?4:NoneType /\ T?r:SupportsRichComparisonT)',
		},
		'next': {
			r'__i:T?1 /\ __default:T?2 /\ return:T?r ^ (T?1:SupportsNext<T?0> /\ T?2:T?V /\ T?r:T?0+T?V)',
			r'__i:T?1 /\ return:T?r ^ (T?1:SupportsNext<T?0> /\ T?r:T?0)',
		},
		'oct': {
			r'__number:T?1 /\ return:T?r ^ (T?1:int+SupportsIndex /\ T?r:str)',
		},
		'ord': {
			r'__c:T?1 /\ return:T?r ^ (T?1:str+bytes+bytearray /\ T?r:int)',
		},
		'print': {
			r'__va_values:T?1 /\ __ko_sep:T?2 /\ __ko_end:T?3 /\ __ko_file:T?4 /\ __ko_flush:T?5 /\ return:T?r ^ (T?1:TopType /\ T?2:str+NoneType /\ T?3:str+NoneType /\ T?4:NoneType+SupportsWrite<str> /\ T?5:bool /\ T?r:NoneType)',
		},
		'repr': {
			r'__obj:T?1 /\ return:T?r ^ (T?1:TopType /\ T?r:str)',
		},
		'round': {
			r'number:T?1 /\ ndigits:T?2 /\ return:T?r ^ (T?1:SupportsRound<T?0> /\ T?2:NoneType /\ T?r:T?0)',
			r'number:T?1 /\ ndigits:T?2 /\ return:T?r ^ (T?1:SupportsRound<T?0> /\ T?2:SupportsIndex /\ T?r:T?0)',
		},
		'setattr': {
			r'__obj:T?1 /\ __name:T?2 /\ __value:T?3 /\ return:T?r ^ (T?1:TopType /\ T?2:str /\ T?3:TopType /\ T?r:NoneType)',
		},
		'sorted': {
			r'__iterable:T?1 /\ __ko_key:T?2 /\ __ko_reverse:T?3 /\ return:T?r ^ (T?1:Iterable<SupportsRichComparisonT> /\ T?2:NoneType /\ T?3:bool /\ T?r:list<SupportsRichComparisonT>)',
		},
		'sum': {
			r'__iterable:T?1 /\ return:T?r ^ (T?1:Iterable<int> /\ T?r:int)',
		},
		'vars': {
			r'__object:T?1 /\ return:T?r ^ (T?1:TopType /\ T?r:dict<str, TopType>)',
		},
	},

}
newspecs = {
	'int': {
		'__new__': {
			r'((cls: int /\ __x: bytearray+str+bytes /\ base: SupportsIndex) -> (return: int))',
			r'((cls: int /\ __x: SupportsIndex+SupportsTrunc+memoryview+str+bytearray+SupportsInt+bytes) -> (return: int))',
		},
		'real': {
			r'((self: int) -> (return: int))',
		},
		'imag': {
			r'((self: int) -> (return: int))',
		},
		'numerator': {
			r'((self: int) -> (return: int))',
		},
		'denominator': {
			r'((self: int) -> (return: int))',
		},
		'conjugate': {
			r'((self: int) -> (return: int))',
		},
		'bit_length': {
			r'((self: int) -> (return: int))',
		},
		'__add__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__sub__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__mul__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__floordiv__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__truediv__': {
			r'((self: int /\ __value: int) -> (return: float))',
		},
		'__mod__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__divmod__': {
			r'((self: int /\ __value: int) -> (return: tuple<int>))',
		},
		'__radd__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__rsub__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__rmul__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__rfloordiv__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__rtruediv__': {
			r'((self: int /\ __value: int) -> (return: float))',
		},
		'__rmod__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__rdivmod__': {
			r'((self: int /\ __value: int) -> (return: tuple<int>))',
		},
		'__pow__': {
			r'((self: int /\ __value: int /\ __mod: int) -> (return: int))',
			r'((self: int /\ __value: int /\ __mod: NoneType) -> (return: float))',
			r'((self: int /\ __value: int /\ __mod: NoneType) -> (return: int))',
			r'((self: int /\ __x: int) -> (return: int))',
		},
		'__and__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__or__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__xor__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__lshift__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__rshift__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__rand__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__ror__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__rxor__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__rlshift__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__rrshift__': {
			r'((self: int /\ __value: int) -> (return: int))',
		},
		'__neg__': {
			r'((self: int) -> (return: int))',
		},
		'__pos__': {
			r'((self: int) -> (return: int))',
		},
		'__invert__': {
			r'((self: int) -> (return: int))',
		},
		'__trunc__': {
			r'((self: int) -> (return: int))',
		},
		'__ceil__': {
			r'((self: int) -> (return: int))',
		},
		'__floor__': {
			r'((self: int) -> (return: int))',
		},
		'__round__': {
			r'((self: int /\ __ndigits: SupportsIndex) -> (return: int))',
		},
		'__getnewargs__': {
			r'((self: int) -> (return: tuple<int>))',
		},
		'__eq__': {
			r'((self: int /\ __value: top) -> (return: bool))',
		},
		'__ne__': {
			r'((self: int /\ __value: top) -> (return: bool))',
		},
		'__lt__': {
			r'((self: int /\ __value: int) -> (return: bool))',
		},
		'__le__': {
			r'((self: int /\ __value: int) -> (return: bool))',
		},
		'__gt__': {
			r'((self: int /\ __value: int) -> (return: bool))',
		},
		'__ge__': {
			r'((self: int /\ __value: int) -> (return: bool))',
		},
		'__float__': {
			r'((self: int) -> (return: float))',
		},
		'__int__': {
			r'((self: int) -> (return: int))',
		},
		'__abs__': {
			r'((self: int) -> (return: int))',
		},
		'__hash__': {
			r'((self: int) -> (return: int))',
		},
		'__bool__': {
			r'((self: int) -> (return: bool))',
		},
		'__index__': {
			r'((self: int) -> (return: int))',
		},
	},
	'float': {
		'__new__': {
			r'((cls: float /\ __x: SupportsIndex+SupportsFloat+memoryview+str+bytearray+bytes) -> (return: float))',
		},
		'as_integer_ratio': {
			r'((self: float) -> (return: tuple<int>))',
		},
		'hex': {
			r'((self: float) -> (return: str))',
		},
		'is_integer': {
			r'((self: float) -> (return: bool))',
		},
		'fromhex': {
			r'((cls: float /\ __string: str) -> (return: float))',
		},
		'real': {
			r'((self: float) -> (return: float))',
		},
		'imag': {
			r'((self: float) -> (return: float))',
		},
		'conjugate': {
			r'((self: float) -> (return: float))',
		},
		'__add__': {
			r'((self: float /\ __value: float) -> (return: float))',
		},
		'__sub__': {
			r'((self: float /\ __value: float) -> (return: float))',
		},
		'__mul__': {
			r'((self: float /\ __value: float) -> (return: float))',
		},
		'__floordiv__': {
			r'((self: float /\ __value: float) -> (return: float))',
		},
		'__truediv__': {
			r'((self: float /\ __value: float) -> (return: float))',
		},
		'__mod__': {
			r'((self: float /\ __value: float) -> (return: float))',
		},
		'__divmod__': {
			r'((self: float /\ __value: float) -> (return: tuple<float>))',
		},
		'__pow__': {
			r'((self: float /\ __value: int /\ __mod: NoneType) -> (return: float))',
		},
		'__radd__': {
			r'((self: float /\ __value: float) -> (return: float))',
		},
		'__rsub__': {
			r'((self: float /\ __value: float) -> (return: float))',
		},
		'__rmul__': {
			r'((self: float /\ __value: float) -> (return: float))',
		},
		'__rfloordiv__': {
			r'((self: float /\ __value: float) -> (return: float))',
		},
		'__rtruediv__': {
			r'((self: float /\ __value: float) -> (return: float))',
		},
		'__rmod__': {
			r'((self: float /\ __value: float) -> (return: float))',
		},
		'__rdivmod__': {
			r'((self: float /\ __value: float) -> (return: tuple<float>))',
		},
		'__rpow__': {
			r'((self: float /\ __value: int /\ __mod: NoneType) -> (return: complex))',
			r'((self: float /\ __value: int /\ __mod: NoneType) -> (return: float))',
		},
		'__getnewargs__': {
			r'((self: float) -> (return: tuple<float>))',
		},
		'__trunc__': {
			r'((self: float) -> (return: int))',
		},
		'__round__': {
			r'((self: float /\ __ndigits: NoneType) -> (return: int))',
			r'((self: float /\ __ndigits: SupportsIndex) -> (return: float))',
		},
		'__eq__': {
			r'((self: float /\ __value: top) -> (return: bool))',
		},
		'__ne__': {
			r'((self: float /\ __value: top) -> (return: bool))',
		},
		'__lt__': {
			r'((self: float /\ __value: float) -> (return: bool))',
		},
		'__le__': {
			r'((self: float /\ __value: float) -> (return: bool))',
		},
		'__gt__': {
			r'((self: float /\ __value: float) -> (return: bool))',
		},
		'__ge__': {
			r'((self: float /\ __value: float) -> (return: bool))',
		},
		'__neg__': {
			r'((self: float) -> (return: float))',
		},
		'__pos__': {
			r'((self: float) -> (return: float))',
		},
		'__int__': {
			r'((self: float) -> (return: int))',
		},
		'__float__': {
			r'((self: float) -> (return: float))',
		},
		'__abs__': {
			r'((self: float) -> (return: float))',
		},
		'__hash__': {
			r'((self: float) -> (return: int))',
		},
		'__bool__': {
			r'((self: float) -> (return: bool))',
		},
	},
	'complex': {
		'real': {
			r'((self: complex) -> (return: float))',
		},
		'imag': {
			r'((self: complex) -> (return: float))',
		},
		'conjugate': {
			r'((self: complex) -> (return: complex))',
		},
		'__add__': {
			r'((self: complex /\ __value: complex) -> (return: complex))',
		},
		'__sub__': {
			r'((self: complex /\ __value: complex) -> (return: complex))',
		},
		'__mul__': {
			r'((self: complex /\ __value: complex) -> (return: complex))',
		},
		'__pow__': {
			r'((self: complex /\ __value: complex /\ __mod: NoneType) -> (return: complex))',
		},
		'__truediv__': {
			r'((self: complex /\ __value: complex) -> (return: complex))',
		},
		'__radd__': {
			r'((self: complex /\ __value: complex) -> (return: complex))',
		},
		'__rsub__': {
			r'((self: complex /\ __value: complex) -> (return: complex))',
		},
		'__rmul__': {
			r'((self: complex /\ __value: complex) -> (return: complex))',
		},
		'__rpow__': {
			r'((self: complex /\ __value: complex /\ __mod: NoneType) -> (return: complex))',
		},
		'__rtruediv__': {
			r'((self: complex /\ __value: complex) -> (return: complex))',
		},
		'__eq__': {
			r'((self: complex /\ __value: top) -> (return: bool))',
		},
		'__ne__': {
			r'((self: complex /\ __value: top) -> (return: bool))',
		},
		'__neg__': {
			r'((self: complex) -> (return: complex))',
		},
		'__pos__': {
			r'((self: complex) -> (return: complex))',
		},
		'__abs__': {
			r'((self: complex) -> (return: float))',
		},
		'__hash__': {
			r'((self: complex) -> (return: int))',
		},
		'__bool__': {
			r'((self: complex) -> (return: bool))',
		},
	},
	'str': {
		'__new__': {
			r'((cls: str /\ object: top) -> (return: str))',
			r'((cls: str /\ object: bytearray+bytes+memoryview /\ encoding: str /\ errors: str) -> (return: str))',
		},
		'capitalize': {
			r'((self: str) -> (return: str))',
		},
		'casefold': {
			r'((self: str) -> (return: str))',
		},
		'center': {
			r'((self: str /\ __width: SupportsIndex /\ __fillchar: str) -> (return: str))',
		},
		'count': {
			r'((self: str /\ x: str /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'encode': {
			r'((self: str /\ encoding: str /\ errors: str) -> (return: bytes))',
		},
		'endswith': {
			r'((self: str /\ __suffix: str+tuple<str> /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: bool))',
		},
		'find': {
			r'((self: str /\ __sub: str /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'format': {
			r'((self: str /\ __va_args: str /\ __kw_kwargs: str) -> (return: str))',
			r'((self: str /\ __va_args: top /\ __kw_kwargs: top) -> (return: str))',
		},
		'format_map': {
			r'((self: str /\ map: dict<str, int>) -> (return: str))',
		},
		'index': {
			r'((self: str /\ __sub: str /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'isalnum': {
			r'((self: str) -> (return: bool))',
		},
		'isalpha': {
			r'((self: str) -> (return: bool))',
		},
		'isascii': {
			r'((self: str) -> (return: bool))',
		},
		'isdecimal': {
			r'((self: str) -> (return: bool))',
		},
		'isdigit': {
			r'((self: str) -> (return: bool))',
		},
		'isidentifier': {
			r'((self: str) -> (return: bool))',
		},
		'islower': {
			r'((self: str) -> (return: bool))',
		},
		'isnumeric': {
			r'((self: str) -> (return: bool))',
		},
		'isprintable': {
			r'((self: str) -> (return: bool))',
		},
		'isspace': {
			r'((self: str) -> (return: bool))',
		},
		'istitle': {
			r'((self: str) -> (return: bool))',
		},
		'isupper': {
			r'((self: str) -> (return: bool))',
		},
		'join': {
			r'((self: str /\ __iterable: Iterable<str>) -> (return: str))',
		},
		'ljust': {
			r'((self: str /\ __width: SupportsIndex /\ __fillchar: str) -> (return: str))',
		},
		'lower': {
			r'((self: str) -> (return: str))',
		},
		'lstrip': {
			r'((self: str /\ __chars: str+NoneType) -> (return: str))',
		},
		'partition': {
			r'((self: str /\ __sep: str) -> (return: tuple<str>))',
		},
		'replace': {
			r'((self: str /\ __old: str /\ __new: str /\ __count: SupportsIndex) -> (return: str))',
		},
		'rfind': {
			r'((self: str /\ __sub: str /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'rindex': {
			r'((self: str /\ __sub: str /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'rjust': {
			r'((self: str /\ __width: SupportsIndex /\ __fillchar: str) -> (return: str))',
		},
		'rpartition': {
			r'((self: str /\ __sep: str) -> (return: tuple<str>))',
		},
		'rsplit': {
			r'((self: str /\ sep: str+NoneType /\ maxsplit: SupportsIndex) -> (return: list<str>))',
		},
		'rstrip': {
			r'((self: str /\ __chars: str+NoneType) -> (return: str))',
		},
		'split': {
			r'((self: str /\ sep: str+NoneType /\ maxsplit: SupportsIndex) -> (return: list<str>))',
		},
		'splitlines': {
			r'((self: str /\ keepends: bool) -> (return: list<str>))',
		},
		'startswith': {
			r'((self: str /\ __prefix: str+tuple<str> /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: bool))',
		},
		'strip': {
			r'((self: str /\ __chars: str+NoneType) -> (return: str))',
		},
		'swapcase': {
			r'((self: str) -> (return: str))',
		},
		'title': {
			r'((self: str) -> (return: str))',
		},
		'translate': {
			r'((self: str /\ __table: dict<int, int+str>) -> (return: str))',
		},
		'upper': {
			r'((self: str) -> (return: str))',
		},
		'zfill': {
			r'((self: str /\ __width: SupportsIndex) -> (return: str))',
		},
		'maketrans': {
			r'((__x: dict<int+str, T?0>+dict<str, T?0>+dict<int, T?0>) -> (return: dict<int, T?0>))',
			r'((__x: str /\ __y: str) -> (return: dict<int, int>))',
			r'((__x: str /\ __y: str /\ __z: str) -> (return: dict<int, int+NoneType>))',
		},
		'__add__': {
			r'((self: str /\ __value: str) -> (return: str))',
		},
		'__contains__': {
			r'((self: str /\ __key: str) -> (return: bool))',
		},
		'__eq__': {
			r'((self: str /\ __value: top) -> (return: bool))',
		},
		'__ge__': {
			r'((self: str /\ __value: str) -> (return: bool))',
		},
		'__gt__': {
			r'((self: str /\ __value: str) -> (return: bool))',
		},
		'__hash__': {
			r'((self: str) -> (return: int))',
		},
		'__iter__': {
			r'((self: str) -> (return: Iterator<str>))',
		},
		'__le__': {
			r'((self: str /\ __value: str) -> (return: bool))',
		},
		'__len__': {
			r'((self: str) -> (return: int))',
		},
		'__lt__': {
			r'((self: str /\ __value: str) -> (return: bool))',
		},
		'__mod__': {
			r'((self: str /\ __value: str+tuple<str>) -> (return: str))',
			r'((self: str /\ __value: top) -> (return: str))',
		},
		'__mul__': {
			r'((self: str /\ __value: SupportsIndex) -> (return: str))',
		},
		'__ne__': {
			r'((self: str /\ __value: top) -> (return: bool))',
		},
		'__rmul__': {
			r'((self: str /\ __value: SupportsIndex) -> (return: str))',
		},
		'__getnewargs__': {
			r'((self: str) -> (return: tuple<str>))',
		},
	},
	'bytes': {
		'__new__': {
			r'((cls: bytes /\ __string: str /\ encoding: str /\ errors: str) -> (return: bytes))',
			r'((cls: bytes /\ __o: SupportsIndex+Iterable<SupportsIndex>+memoryview+SupportsBytes+bytearray+bytes) -> (return: bytes))',
			r'((cls: bytes) -> (return: bytes))',
		},
		'capitalize': {
			r'((self: bytes) -> (return: bytes))',
		},
		'center': {
			r'((self: bytes /\ __width: SupportsIndex /\ __fillchar: bytes) -> (return: bytes))',
		},
		'count': {
			r'((self: bytes /\ __sub: bytearray+SupportsIndex+bytes+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'decode': {
			r'((self: bytes /\ encoding: str /\ errors: str) -> (return: str))',
		},
		'endswith': {
			r'((self: bytes /\ __suffix: bytearray+bytes+tuple<bytearray+bytes+memoryview>+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: bool))',
		},
		'find': {
			r'((self: bytes /\ __sub: bytearray+SupportsIndex+bytes+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'index': {
			r'((self: bytes /\ __sub: bytearray+SupportsIndex+bytes+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'isalnum': {
			r'((self: bytes) -> (return: bool))',
		},
		'isalpha': {
			r'((self: bytes) -> (return: bool))',
		},
		'isascii': {
			r'((self: bytes) -> (return: bool))',
		},
		'isdigit': {
			r'((self: bytes) -> (return: bool))',
		},
		'islower': {
			r'((self: bytes) -> (return: bool))',
		},
		'isspace': {
			r'((self: bytes) -> (return: bool))',
		},
		'istitle': {
			r'((self: bytes) -> (return: bool))',
		},
		'isupper': {
			r'((self: bytes) -> (return: bool))',
		},
		'join': {
			r'((self: bytes /\ __iterable_of_bytes: Iterable<bytearray+bytes+memoryview>) -> (return: bytes))',
		},
		'ljust': {
			r'((self: bytes /\ __width: SupportsIndex /\ __fillchar: bytearray+bytes) -> (return: bytes))',
		},
		'lower': {
			r'((self: bytes) -> (return: bytes))',
		},
		'lstrip': {
			r'((self: bytes /\ __bytes: bytearray+NoneType+bytes+memoryview) -> (return: bytes))',
		},
		'partition': {
			r'((self: bytes /\ __sep: bytearray+bytes+memoryview) -> (return: tuple<bytes>))',
		},
		'replace': {
			r'((self: bytes /\ __old: bytearray+bytes+memoryview /\ __new: bytearray+bytes+memoryview /\ __count: SupportsIndex) -> (return: bytes))',
		},
		'rfind': {
			r'((self: bytes /\ __sub: bytearray+SupportsIndex+bytes+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'rindex': {
			r'((self: bytes /\ __sub: bytearray+SupportsIndex+bytes+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'rjust': {
			r'((self: bytes /\ __width: SupportsIndex /\ __fillchar: bytearray+bytes) -> (return: bytes))',
		},
		'rpartition': {
			r'((self: bytes /\ __sep: bytearray+bytes+memoryview) -> (return: tuple<bytes>))',
		},
		'rsplit': {
			r'((self: bytes /\ sep: bytearray+NoneType+bytes+memoryview /\ maxsplit: SupportsIndex) -> (return: list<bytes>))',
		},
		'rstrip': {
			r'((self: bytes /\ __bytes: bytearray+NoneType+bytes+memoryview) -> (return: bytes))',
		},
		'split': {
			r'((self: bytes /\ sep: bytearray+NoneType+bytes+memoryview /\ maxsplit: SupportsIndex) -> (return: list<bytes>))',
		},
		'splitlines': {
			r'((self: bytes /\ keepends: bool) -> (return: list<bytes>))',
		},
		'startswith': {
			r'((self: bytes /\ __prefix: bytearray+bytes+tuple<bytearray+bytes+memoryview>+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: bool))',
		},
		'strip': {
			r'((self: bytes /\ __bytes: bytearray+NoneType+bytes+memoryview) -> (return: bytes))',
		},
		'swapcase': {
			r'((self: bytes) -> (return: bytes))',
		},
		'title': {
			r'((self: bytes) -> (return: bytes))',
		},
		'translate': {
			r'((self: bytes /\ __table: bytearray+NoneType+bytes+memoryview /\ delete: bytes) -> (return: bytes))',
		},
		'upper': {
			r'((self: bytes) -> (return: bytes))',
		},
		'zfill': {
			r'((self: bytes /\ __width: SupportsIndex) -> (return: bytes))',
		},
		'fromhex': {
			r'((cls: bytes /\ __string: str) -> (return: bytes))',
		},
		'maketrans': {
			r'((__frm: bytearray+bytes+memoryview /\ __to: bytearray+bytes+memoryview) -> (return: bytes))',
		},
		'__len__': {
			r'((self: bytes) -> (return: int))',
		},
		'__iter__': {
			r'((self: bytes) -> (return: Iterator<int>))',
		},
		'__hash__': {
			r'((self: bytes) -> (return: int))',
		},
		'__getitem__': {
			r'((self: bytes /\ __key: SupportsIndex) -> (return: int))',
		},
		'__add__': {
			r'((self: bytes /\ __value: bytearray+bytes+memoryview) -> (return: bytes))',
		},
		'__mul__': {
			r'((self: bytes /\ __value: SupportsIndex) -> (return: bytes))',
		},
		'__rmul__': {
			r'((self: bytes /\ __value: SupportsIndex) -> (return: bytes))',
		},
		'__mod__': {
			r'((self: bytes /\ __value: top) -> (return: bytes))',
		},
		'__contains__': {
			r'((self: bytes /\ __key: bytearray+SupportsIndex+bytes+memoryview) -> (return: bool))',
		},
		'__eq__': {
			r'((self: bytes /\ __value: top) -> (return: bool))',
		},
		'__ne__': {
			r'((self: bytes /\ __value: top) -> (return: bool))',
		},
		'__lt__': {
			r'((self: bytes /\ __value: bytes) -> (return: bool))',
		},
		'__le__': {
			r'((self: bytes /\ __value: bytes) -> (return: bool))',
		},
		'__gt__': {
			r'((self: bytes /\ __value: bytes) -> (return: bool))',
		},
		'__ge__': {
			r'((self: bytes /\ __value: bytes) -> (return: bool))',
		},
		'__getnewargs__': {
			r'((self: bytes) -> (return: tuple<bytes>))',
		},
		'__buffer__': {
			r'((self: bytes /\ __flags: int) -> (return: memoryview))',
		},
	},
	'bytearray': {
		'__init__': {
			r'((self: bytearray /\ __ints: SupportsIndex+Iterable<SupportsIndex>+memoryview+bytearray+bytes) -> (return: NoneType))',
			r'((self: bytearray /\ __string: str /\ encoding: str /\ errors: str) -> (return: NoneType))',
			r'((self: bytearray) -> (return: NoneType))',
		},
		'append': {
			r'((self: bytearray /\ __item: SupportsIndex) -> (return: NoneType))',
		},
		'capitalize': {
			r'((self: bytearray) -> (return: bytearray))',
		},
		'center': {
			r'((self: bytearray /\ __width: SupportsIndex /\ __fillchar: bytes) -> (return: bytearray))',
		},
		'count': {
			r'((self: bytearray /\ __sub: bytearray+SupportsIndex+bytes+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'copy': {
			r'((self: bytearray) -> (return: bytearray))',
		},
		'decode': {
			r'((self: bytearray /\ encoding: str /\ errors: str) -> (return: str))',
		},
		'endswith': {
			r'((self: bytearray /\ __suffix: bytearray+bytes+tuple<bytearray+bytes+memoryview>+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: bool))',
		},
		'extend': {
			r'((self: bytearray /\ __iterable_of_ints: Iterable<SupportsIndex>) -> (return: NoneType))',
		},
		'find': {
			r'((self: bytearray /\ __sub: bytearray+SupportsIndex+bytes+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'index': {
			r'((self: bytearray /\ __sub: bytearray+SupportsIndex+bytes+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'insert': {
			r'((self: bytearray /\ __index: SupportsIndex /\ __item: SupportsIndex) -> (return: NoneType))',
		},
		'isalnum': {
			r'((self: bytearray) -> (return: bool))',
		},
		'isalpha': {
			r'((self: bytearray) -> (return: bool))',
		},
		'isascii': {
			r'((self: bytearray) -> (return: bool))',
		},
		'isdigit': {
			r'((self: bytearray) -> (return: bool))',
		},
		'islower': {
			r'((self: bytearray) -> (return: bool))',
		},
		'isspace': {
			r'((self: bytearray) -> (return: bool))',
		},
		'istitle': {
			r'((self: bytearray) -> (return: bool))',
		},
		'isupper': {
			r'((self: bytearray) -> (return: bool))',
		},
		'join': {
			r'((self: bytearray /\ __iterable_of_bytes: Iterable<bytearray+bytes+memoryview>) -> (return: bytearray))',
		},
		'ljust': {
			r'((self: bytearray /\ __width: SupportsIndex /\ __fillchar: bytearray+bytes) -> (return: bytearray))',
		},
		'lower': {
			r'((self: bytearray) -> (return: bytearray))',
		},
		'lstrip': {
			r'((self: bytearray /\ __bytes: bytearray+NoneType+bytes+memoryview) -> (return: bytearray))',
		},
		'partition': {
			r'((self: bytearray /\ __sep: bytearray+bytes+memoryview) -> (return: tuple<bytearray>))',
		},
		'pop': {
			r'((self: bytearray /\ __index: int) -> (return: int))',
		},
		'remove': {
			r'((self: bytearray /\ __value: int) -> (return: NoneType))',
		},
		'replace': {
			r'((self: bytearray /\ __old: bytearray+bytes+memoryview /\ __new: bytearray+bytes+memoryview /\ __count: SupportsIndex) -> (return: bytearray))',
		},
		'rfind': {
			r'((self: bytearray /\ __sub: bytearray+SupportsIndex+bytes+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'rindex': {
			r'((self: bytearray /\ __sub: bytearray+SupportsIndex+bytes+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: int))',
		},
		'rjust': {
			r'((self: bytearray /\ __width: SupportsIndex /\ __fillchar: bytearray+bytes) -> (return: bytearray))',
		},
		'rpartition': {
			r'((self: bytearray /\ __sep: bytearray+bytes+memoryview) -> (return: tuple<bytearray>))',
		},
		'rsplit': {
			r'((self: bytearray /\ sep: bytearray+NoneType+bytes+memoryview /\ maxsplit: SupportsIndex) -> (return: list<bytearray>))',
		},
		'rstrip': {
			r'((self: bytearray /\ __bytes: bytearray+NoneType+bytes+memoryview) -> (return: bytearray))',
		},
		'split': {
			r'((self: bytearray /\ sep: bytearray+NoneType+bytes+memoryview /\ maxsplit: SupportsIndex) -> (return: list<bytearray>))',
		},
		'splitlines': {
			r'((self: bytearray /\ keepends: bool) -> (return: list<bytearray>))',
		},
		'startswith': {
			r'((self: bytearray /\ __prefix: bytearray+bytes+tuple<bytearray+bytes+memoryview>+memoryview /\ __start: SupportsIndex+NoneType /\ __end: SupportsIndex+NoneType) -> (return: bool))',
		},
		'strip': {
			r'((self: bytearray /\ __bytes: bytearray+NoneType+bytes+memoryview) -> (return: bytearray))',
		},
		'swapcase': {
			r'((self: bytearray) -> (return: bytearray))',
		},
		'title': {
			r'((self: bytearray) -> (return: bytearray))',
		},
		'translate': {
			r'((self: bytearray /\ __table: bytearray+NoneType+bytes+memoryview /\ delete: bytes) -> (return: bytearray))',
		},
		'upper': {
			r'((self: bytearray) -> (return: bytearray))',
		},
		'zfill': {
			r'((self: bytearray /\ __width: SupportsIndex) -> (return: bytearray))',
		},
		'fromhex': {
			r'((cls: bytearray /\ __string: str) -> (return: bytearray))',
		},
		'maketrans': {
			r'((__frm: bytearray+bytes+memoryview /\ __to: bytearray+bytes+memoryview) -> (return: bytes))',
		},
		'__len__': {
			r'((self: bytearray) -> (return: int))',
		},
		'__iter__': {
			r'((self: bytearray) -> (return: Iterator<int>))',
		},
		'__getitem__': {
			r'((self: bytearray /\ __key: SupportsIndex) -> (return: int))',
		},
		'__setitem__': {
			r'((self: bytearray /\ __key: SupportsIndex /\ __value: SupportsIndex) -> (return: NoneType))',
		},
		'__add__': {
			r'((self: bytearray /\ __value: bytearray+bytes+memoryview) -> (return: bytearray))',
		},
		'__iadd__': {
			r'((self: bytearray /\ __value: bytearray+bytes+memoryview) -> (return: bytearray))',
		},
		'__mul__': {
			r'((self: bytearray /\ __value: SupportsIndex) -> (return: bytearray))',
		},
		'__rmul__': {
			r'((self: bytearray /\ __value: SupportsIndex) -> (return: bytearray))',
		},
		'__imul__': {
			r'((self: bytearray /\ __value: SupportsIndex) -> (return: bytearray))',
		},
		'__mod__': {
			r'((self: bytearray /\ __value: top) -> (return: bytes))',
		},
		'__contains__': {
			r'((self: bytearray /\ __key: bytearray+SupportsIndex+bytes+memoryview) -> (return: bool))',
		},
		'__eq__': {
			r'((self: bytearray /\ __value: top) -> (return: bool))',
		},
		'__ne__': {
			r'((self: bytearray /\ __value: top) -> (return: bool))',
		},
		'__lt__': {
			r'((self: bytearray /\ __value: bytearray+bytes+memoryview) -> (return: bool))',
		},
		'__le__': {
			r'((self: bytearray /\ __value: bytearray+bytes+memoryview) -> (return: bool))',
		},
		'__gt__': {
			r'((self: bytearray /\ __value: bytearray+bytes+memoryview) -> (return: bool))',
		},
		'__ge__': {
			r'((self: bytearray /\ __value: bytearray+bytes+memoryview) -> (return: bool))',
		},
		'__alloc__': {
			r'((self: bytearray) -> (return: int))',
		},
		'__buffer__': {
			r'((self: bytearray /\ __flags: int) -> (return: memoryview))',
		},
		'__release_buffer__': {
			r'((self: bytearray /\ __buffer: memoryview) -> (return: NoneType))',
		},
	},
	'bool': {
		'__new__': {
			r'((cls: bool /\ __o: top) -> (return: bool))',
		},
		'__and__': {
			r'((self: bool /\ __value: int) -> (return: int))',
			r'((self: bool /\ __value: bool) -> (return: bool))',
		},
		'__or__': {
			r'((self: bool /\ __value: int) -> (return: int))',
			r'((self: bool /\ __value: bool) -> (return: bool))',
		},
		'__xor__': {
			r'((self: bool /\ __value: int) -> (return: int))',
			r'((self: bool /\ __value: bool) -> (return: bool))',
		},
		'__rand__': {
			r'((self: bool /\ __value: int) -> (return: int))',
			r'((self: bool /\ __value: bool) -> (return: bool))',
		},
		'__ror__': {
			r'((self: bool /\ __value: int) -> (return: int))',
			r'((self: bool /\ __value: bool) -> (return: bool))',
		},
		'__rxor__': {
			r'((self: bool /\ __value: int) -> (return: int))',
			r'((self: bool /\ __value: bool) -> (return: bool))',
		},
		'__getnewargs__': {
			r'((self: bool) -> (return: tuple<int>))',
		},
	},
	'slice': {
		'__init__': {
			r'((self: slice /\ __stop: top) -> (return: NoneType))',
			r'((self: slice /\ __start: top /\ __stop: top /\ __step: top) -> (return: NoneType))',
		},
		'__eq__': {
			r'((self: slice /\ __value: top) -> (return: bool))',
		},
		'indices': {
			r'((self: slice /\ __len: SupportsIndex) -> (return: tuple<int>))',
		},
	},
	'tuple': {
		'__new__': {
			r'((cls: tuple<T?co> /\ __iterable: Iterable<T?co>) -> (return: tuple<T?co>))',
		},
		'__len__': {
			r'((self: tuple<T?co>) -> (return: int))',
		},
		'__contains__': {
			r'((self: tuple<T?co> /\ __key: top) -> (return: bool))',
		},
		'__getitem__': {
			r'((self: tuple<T?co> /\ __key: SupportsIndex) -> (return: T?co))',
		},
		'__iter__': {
			r'((self: tuple<T?co>) -> (return: Iterator<T?co>))',
		},
		'__lt__': {
			r'((self: tuple<T?co> /\ __value: tuple<T?co>) -> (return: bool))',
		},
		'__le__': {
			r'((self: tuple<T?co> /\ __value: tuple<T?co>) -> (return: bool))',
		},
		'__gt__': {
			r'((self: tuple<T?co> /\ __value: tuple<T?co>) -> (return: bool))',
		},
		'__ge__': {
			r'((self: tuple<T?co> /\ __value: tuple<T?co>) -> (return: bool))',
		},
		'__eq__': {
			r'((self: tuple<T?co> /\ __value: top) -> (return: bool))',
		},
		'__hash__': {
			r'((self: tuple<T?co>) -> (return: int))',
		},
		'__add__': {
			r'((self: tuple<T?co> /\ __value: tuple<T?co>) -> (return: tuple<T?co>))',
			r'((self: tuple<T?co> /\ __value: tuple<T?0>) -> (return: tuple<T?0+T?co>))',
		},
		'__mul__': {
			r'((self: tuple<T?co> /\ __value: SupportsIndex) -> (return: tuple<T?co>))',
		},
		'__rmul__': {
			r'((self: tuple<T?co> /\ __value: SupportsIndex) -> (return: tuple<T?co>))',
		},
		'count': {
			r'((self: tuple<T?co> /\ __value: top) -> (return: int))',
		},
		'index': {
			r'((self: tuple<T?co> /\ __value: top /\ __start: SupportsIndex /\ __stop: SupportsIndex) -> (return: int))',
		},
	},
	'list': {
		'__init__': {
			r'((self: list<T?0>) -> (return: NoneType))',
			r'((self: list<T?0> /\ __iterable: Iterable<T?0>) -> (return: NoneType))',
		},
		'copy': {
			r'((self: list<T?0>) -> (return: list<T?0>))',
		},
		'append': {
			r'((self: list<T?0> /\ __object: T?0) -> (return: NoneType))',
		},
		'extend': {
			r'((self: list<T?0> /\ __iterable: Iterable<T?0>) -> (return: NoneType))',
		},
		'pop': {
			r'((self: list<T?0> /\ __index: SupportsIndex) -> (return: T?0))',
		},
		'index': {
			r'((self: list<T?0> /\ __value: T?0 /\ __start: SupportsIndex /\ __stop: SupportsIndex) -> (return: int))',
		},
		'count': {
			r'((self: list<T?0> /\ __value: T?0) -> (return: int))',
		},
		'insert': {
			r'((self: list<T?0> /\ __index: SupportsIndex /\ __object: T?0) -> (return: NoneType))',
		},
		'remove': {
			r'((self: list<T?0> /\ __value: T?0) -> (return: NoneType))',
		},
		'sort': {
			r'((self: list<SupportsRichComparisonT> /\ __ko_key: NoneType /\ __ko_reverse: bool) -> (return: NoneType))',
		},
		'__len__': {
			r'((self: list<T?0>) -> (return: int))',
		},
		'__iter__': {
			r'((self: list<T?0>) -> (return: Iterator<T?0>))',
		},
		'__getitem__': {
			r'((self: list<T?0> /\ __i: SupportsIndex) -> (return: T?0))',
		},
		'__setitem__': {
			r'((self: list<T?0> /\ __key: SupportsIndex /\ __value: T?0) -> (return: NoneType))',
		},
		'__add__': {
			r'((self: list<T?0> /\ __value: list<T?0>) -> (return: list<T?0>))',
			r'((self: list<T?0> /\ __value: list<T?s>) -> (return: list<T?0+T?s>))',
		},
		'__iadd__': {
			r'((self: list<T?0> /\ __value: Iterable<T?0>) -> (return: list<T?0>))',
		},
		'__mul__': {
			r'((self: list<T?0> /\ __value: SupportsIndex) -> (return: list<T?0>))',
		},
		'__rmul__': {
			r'((self: list<T?0> /\ __value: SupportsIndex) -> (return: list<T?0>))',
		},
		'__imul__': {
			r'((self: list<T?0> /\ __value: SupportsIndex) -> (return: list<T?0>))',
		},
		'__contains__': {
			r'((self: list<T?0> /\ __key: top) -> (return: bool))',
		},
		'__reversed__': {
			r'((self: list<T?0>) -> (return: Iterator<T?0>))',
		},
		'__gt__': {
			r'((self: list<T?0> /\ __value: list<T?0>) -> (return: bool))',
		},
		'__ge__': {
			r'((self: list<T?0> /\ __value: list<T?0>) -> (return: bool))',
		},
		'__lt__': {
			r'((self: list<T?0> /\ __value: list<T?0>) -> (return: bool))',
		},
		'__le__': {
			r'((self: list<T?0> /\ __value: list<T?0>) -> (return: bool))',
		},
		'__eq__': {
			r'((self: list<T?0> /\ __value: top) -> (return: bool))',
		},
	},
	'dict': {
		'__init__': {
			r'((self: dict<T?K, T?V>) -> (return: NoneType))',
			r'((self: dict<T?K, T?V> /\ __map: dict<T?K, T?V>) -> (return: NoneType))',
			r'((self: dict<str, T?V> /\ __map: dict<str, T?V> /\ __kw_kwargs: T?V) -> (return: NoneType))',
			r'((self: dict<str, T?V> /\ __iterable: Iterable<tuple<str+T?V>> /\ __kw_kwargs: T?V) -> (return: NoneType))',
			r'((self: dict<bytes, bytes> /\ __iterable: Iterable<list<bytes>>) -> (return: NoneType))',
			r'((self: dict<T?K, T?V> /\ __iterable: Iterable<tuple<T?K+T?V>>) -> (return: NoneType))',
			r'((self: dict<str, str> /\ __iterable: Iterable<list<str>>) -> (return: NoneType))',
			r'((self: dict<str, T?V> /\ __kw_kwargs: T?V) -> (return: NoneType))',
		},
		'__new__': {
			r'((cls: dict<T?K, T?V> /\ __va_args: top /\ __kw_kwargs: top) -> (return: dict<T?K, T?V>))',
		},
		'copy': {
			r'((self: dict<T?K, T?V>) -> (return: dict<T?K, T?V>))',
		},
		'keys': {
			r'((self: dict<T?K, T?V>) -> (return: list<T?K>))',
		},
		'values': {
			r'((self: dict<T?K, T?V>) -> (return: list<T?V>))',
		},
		'items': {
			r'((self: dict<T?K, T?V>) -> (return: list<tuple<T?K+T?V>>))',
		},
		'fromkeys': {
			r'((cls: dict<T?K, T?V> /\ __iterable: Iterable<T?0> /\ __value: T?s) -> (return: dict<T?0, T?s>))',
			r'((cls: dict<T?K, T?V> /\ __iterable: Iterable<T?0> /\ __value: NoneType) -> (return: dict<T?0, top+NoneType>))',
		},
		'get': {
			r'((self: dict<T?K, T?V> /\ __key: T?K) -> (return: T?V+NoneType))',
			r'((self: dict<T?K, T?V> /\ __key: T?K /\ __default: T?0) -> (return: T?0+T?V))',
			r'((self: dict<T?K, T?V> /\ __key: T?K /\ __default: T?V) -> (return: T?V))',
		},
		'pop': {
			r'((self: dict<T?K, T?V> /\ __key: T?K) -> (return: T?V))',
			r'((self: dict<T?K, T?V> /\ __key: T?K /\ __default: T?0) -> (return: T?0+T?V))',
			r'((self: dict<T?K, T?V> /\ __key: T?K /\ __default: T?V) -> (return: T?V))',
		},
		'__len__': {
			r'((self: dict<T?K, T?V>) -> (return: int))',
		},
		'__getitem__': {
			r'((self: dict<T?K, T?V> /\ __key: T?K) -> (return: T?V))',
		},
		'__setitem__': {
			r'((self: dict<T?K, T?V> /\ __key: T?K /\ __value: T?V) -> (return: NoneType))',
		},
		'__delitem__': {
			r'((self: dict<T?K, T?V> /\ __key: T?K) -> (return: NoneType))',
		},
		'__iter__': {
			r'((self: dict<T?K, T?V>) -> (return: Iterator<T?K>))',
		},
		'__eq__': {
			r'((self: dict<T?K, T?V> /\ __value: top) -> (return: bool))',
		},
	},
	'set': {
		'__init__': {
			r'((self: set<T?0> /\ __iterable: Iterable<T?0>) -> (return: NoneType))',
			r'((self: set<T?0>) -> (return: NoneType))',
		},
		'add': {
			r'((self: set<T?0> /\ __element: T?0) -> (return: NoneType))',
		},
		'copy': {
			r'((self: set<T?0>) -> (return: set<T?0>))',
		},
		'difference': {
			r'((self: set<T?0> /\ __va_s: Iterable<top>) -> (return: set<T?0>))',
		},
		'difference_update': {
			r'((self: set<T?0> /\ __va_s: Iterable<top>) -> (return: NoneType))',
		},
		'discard': {
			r'((self: set<T?0> /\ __element: T?0) -> (return: NoneType))',
		},
		'intersection': {
			r'((self: set<T?0> /\ __va_s: Iterable<top>) -> (return: set<T?0>))',
		},
		'intersection_update': {
			r'((self: set<T?0> /\ __va_s: Iterable<top>) -> (return: NoneType))',
		},
		'isdisjoint': {
			r'((self: set<T?0> /\ __s: Iterable<top>) -> (return: bool))',
		},
		'issubset': {
			r'((self: set<T?0> /\ __s: Iterable<top>) -> (return: bool))',
		},
		'issuperset': {
			r'((self: set<T?0> /\ __s: Iterable<top>) -> (return: bool))',
		},
		'remove': {
			r'((self: set<T?0> /\ __element: T?0) -> (return: NoneType))',
		},
		'symmetric_difference': {
			r'((self: set<T?0> /\ __s: Iterable<T?0>) -> (return: set<T?0>))',
		},
		'symmetric_difference_update': {
			r'((self: set<T?0> /\ __s: Iterable<T?0>) -> (return: NoneType))',
		},
		'union': {
			r'((self: set<T?0> /\ __va_s: Iterable<T?s>) -> (return: set<T?0+T?s>))',
		},
		'update': {
			r'((self: set<T?0> /\ __va_s: Iterable<T?0>) -> (return: NoneType))',
		},
		'__len__': {
			r'((self: set<T?0>) -> (return: int))',
		},
		'__contains__': {
			r'((self: set<T?0> /\ __o: top) -> (return: bool))',
		},
		'__iter__': {
			r'((self: set<T?0>) -> (return: Iterator<T?0>))',
		},
		'__and__': {
			r'((self: set<T?0> /\ __value: set<top>) -> (return: set<T?0>))',
		},
		'__iand__': {
			r'((self: set<T?0> /\ __value: set<top>) -> (return: set<T?0>))',
		},
		'__or__': {
			r'((self: set<T?0> /\ __value: set<T?s>) -> (return: set<T?0+T?s>))',
		},
		'__ior__': {
			r'((self: set<T?0> /\ __value: set<T?0>) -> (return: set<T?0>))',
		},
		'__sub__': {
			r'((self: set<T?0> /\ __value: set<T?0+NoneType>) -> (return: set<T?0>))',
		},
		'__isub__': {
			r'((self: set<T?0> /\ __value: set<top>) -> (return: set<T?0>))',
		},
		'__xor__': {
			r'((self: set<T?0> /\ __value: set<T?s>) -> (return: set<T?0+T?s>))',
		},
		'__ixor__': {
			r'((self: set<T?0> /\ __value: set<T?0>) -> (return: set<T?0>))',
		},
		'__le__': {
			r'((self: set<T?0> /\ __value: set<top>) -> (return: bool))',
		},
		'__lt__': {
			r'((self: set<T?0> /\ __value: set<top>) -> (return: bool))',
		},
		'__ge__': {
			r'((self: set<T?0> /\ __value: set<top>) -> (return: bool))',
		},
		'__gt__': {
			r'((self: set<T?0> /\ __value: set<top>) -> (return: bool))',
		},
		'__eq__': {
			r'((self: set<T?0> /\ __value: top) -> (return: bool))',
		},
	},
	'frozenset': {
		'__new__': {
			r'((cls: frozenset<T?co> /\ __iterable: Iterable<T?co>) -> (return: frozenset<T?co>))',
			r'((cls: frozenset<T?co>) -> (return: frozenset<T?co>))',
		},
		'copy': {
			r'((self: frozenset<T?co>) -> (return: frozenset<T?co>))',
		},
		'difference': {
			r'((self: frozenset<T?co> /\ __va_s: Iterable<top>) -> (return: frozenset<T?co>))',
		},
		'intersection': {
			r'((self: frozenset<T?co> /\ __va_s: Iterable<top>) -> (return: frozenset<T?co>))',
		},
		'isdisjoint': {
			r'((self: frozenset<T?co> /\ __s: Iterable<T?co>) -> (return: bool))',
		},
		'issubset': {
			r'((self: frozenset<T?co> /\ __s: Iterable<top>) -> (return: bool))',
		},
		'issuperset': {
			r'((self: frozenset<T?co> /\ __s: Iterable<top>) -> (return: bool))',
		},
		'symmetric_difference': {
			r'((self: frozenset<T?co> /\ __s: Iterable<T?co>) -> (return: frozenset<T?co>))',
		},
		'union': {
			r'((self: frozenset<T?co> /\ __va_s: Iterable<T?s>) -> (return: frozenset<T?s+T?co>))',
		},
		'__len__': {
			r'((self: frozenset<T?co>) -> (return: int))',
		},
		'__contains__': {
			r'((self: frozenset<T?co> /\ __o: top) -> (return: bool))',
		},
		'__iter__': {
			r'((self: frozenset<T?co>) -> (return: Iterator<T?co>))',
		},
		'__and__': {
			r'((self: frozenset<T?co> /\ __value: set<T?co>) -> (return: frozenset<T?co>))',
		},
		'__or__': {
			r'((self: frozenset<T?co> /\ __value: set<T?s>) -> (return: frozenset<T?s+T?co>))',
		},
		'__sub__': {
			r'((self: frozenset<T?co> /\ __value: set<T?co>) -> (return: frozenset<T?co>))',
		},
		'__xor__': {
			r'((self: frozenset<T?co> /\ __value: set<T?s>) -> (return: frozenset<T?s+T?co>))',
		},
		'__le__': {
			r'((self: frozenset<T?co> /\ __value: set<top>) -> (return: bool))',
		},
		'__lt__': {
			r'((self: frozenset<T?co> /\ __value: set<top>) -> (return: bool))',
		},
		'__ge__': {
			r'((self: frozenset<T?co> /\ __value: set<top>) -> (return: bool))',
		},
		'__gt__': {
			r'((self: frozenset<T?co> /\ __value: set<top>) -> (return: bool))',
		},
		'__eq__': {
			r'((self: frozenset<T?co> /\ __value: top) -> (return: bool))',
		},
		'__hash__': {
			r'((self: frozenset<T?co>) -> (return: int))',
		},
	},
	'range': {
		'start': {
			r'((self: range<int>) -> (return: int))',
		},
		'stop': {
			r'((self: range<int>) -> (return: int))',
		},
		'step': {
			r'((self: range<int>) -> (return: int))',
		},
		'__init__': {
			r'((self: range<int> /\ __stop: SupportsIndex) -> (return: NoneType))',
			r'((self: range<int> /\ __start: SupportsIndex /\ __stop: SupportsIndex /\ __step: SupportsIndex) -> (return: NoneType))',
		},
		'count': {
			r'((self: range<int> /\ __value: int) -> (return: int))',
		},
		'index': {
			r'((self: range<int> /\ __value: int) -> (return: int))',
		},
		'__len__': {
			r'((self: range<int>) -> (return: int))',
		},
		'__eq__': {
			r'((self: range<int> /\ __value: top) -> (return: bool))',
		},
		'__hash__': {
			r'((self: range<int>) -> (return: int))',
		},
		'__contains__': {
			r'((self: range<int> /\ __key: top) -> (return: bool))',
		},
		'__iter__': {
			r'((self: range<int>) -> (return: Iterator<int>))',
		},
		'__getitem__': {
			r'((self: range<int> /\ __key: SupportsIndex) -> (return: int))',
		},
		'__reversed__': {
			r'((self: range<int>) -> (return: Iterator<int>))',
		},
	},
	'property': {
		'__set__': {
			r'((self: property /\ __instance: top /\ __value: top) -> (return: NoneType))',
		},
		'__delete__': {
			r'((self: property /\ __instance: top) -> (return: NoneType))',
		},
	},
	'_NotImplementedType': {
	},
	'filter': {
		'__init__': {
			r'((self: filter<T?0> /\ __function: NoneType /\ __iterable: Iterable<T?0+NoneType>) -> (return: NoneType))',
		},
		'__iter__': {
			r'((self: filter<T?0>) -> (return: filter<T?0>))',
		},
		'__next__': {
			r'((self: filter<T?0>) -> (return: T?0))',
		},
	},
	'map': {
		'__iter__': {
			r'((self: map<T?s>) -> (return: map<T?s>))',
		},
		'__next__': {
			r'((self: map<T?s>) -> (return: T?s))',
		},
	},
	'reversed': {
		'__init__': {
			r'((self: reversed<T?0> /\ __sequence: SupportsLenAndGetItem<T?0>) -> (return: NoneType))',
			r'((self: reversed<T?0> /\ __sequence: Reversible<T?0>) -> (return: NoneType))',
		},
		'__iter__': {
			r'((self: reversed<T?0>) -> (return: reversed<T?0>))',
		},
		'__next__': {
			r'((self: reversed<T?0>) -> (return: T?0))',
		},
		'__length_hint__': {
			r'((self: reversed<T?0>) -> (return: int))',
		},
	},
	'zip': {
		'__iter__': {
			r'((self: zip<T?co>) -> (return: zip<T?co>))',
		},
		'__next__': {
			r'((self: zip<T?co>) -> (return: T?co))',
		},
	},
	'BaseException': {
		'__init__': {
			r'((self: BaseException /\ __va_args: top) -> (return: NoneType))',
		},
		'__setstate__': {
			r'((self: BaseException /\ __state: dict<str, top>+NoneType) -> (return: NoneType))',
		},
	},
	'GeneratorExit': {
	},
	'KeyboardInterrupt': {
	},
	'SystemExit': {
	},
	'Exception': {
	},
	'StopIteration': {
	},
	'OSError': {
	},
	'ArithmeticError': {
	},
	'AssertionError': {
	},
	'AttributeError': {
	},
	'BufferError': {
	},
	'EOFError': {
	},
	'ImportError': {
		'__init__': {
			r'((self: ImportError /\ __va_args: top /\ __ko_name: str+NoneType /\ __ko_path: str+NoneType) -> (return: NoneType))',
		},
	},
	'LookupError': {
	},
	'MemoryError': {
	},
	'NameError': {
	},
	'ReferenceError': {
	},
	'RuntimeError': {
	},
	'StopAsyncIteration': {
	},
	'SyntaxError': {
	},
	'SystemError': {
	},
	'TypeError': {
	},
	'ValueError': {
	},
	'FloatingPointError': {
	},
	'OverflowError': {
	},
	'ZeroDivisionError': {
	},
	'ModuleNotFoundError': {
	},
	'IndexError': {
	},
	'KeyError': {
	},
	'UnboundLocalError': {
	},
	'BlockingIOError': {
	},
	'ChildProcessError': {
	},
	'ConnectionError': {
	},
	'BrokenPipeError': {
	},
	'ConnectionAbortedError': {
	},
	'ConnectionRefusedError': {
	},
	'ConnectionResetError': {
	},
	'FileExistsError': {
	},
	'FileNotFoundError': {
	},
	'InterruptedError': {
	},
	'IsADirectoryError': {
	},
	'NotADirectoryError': {
	},
	'PermissionError': {
	},
	'ProcessLookupError': {
	},
	'TimeoutError': {
	},
	'NotImplementedError': {
	},
	'RecursionError': {
	},
	'IndentationError': {
	},
	'TabError': {
	},
	'UnicodeError': {
	},
	'UnicodeDecodeError': {
		'__init__': {
			r'((self: UnicodeDecodeError /\ __encoding: str /\ __object: bytearray+bytes+memoryview /\ __start: int /\ __end: int /\ __reason: str) -> (return: NoneType))',
		},
	},
	'UnicodeEncodeError': {
		'__init__': {
			r'((self: UnicodeEncodeError /\ __encoding: str /\ __object: str /\ __start: int /\ __end: int /\ __reason: str) -> (return: NoneType))',
		},
	},
	'UnicodeTranslateError': {
		'__init__': {
			r'((self: UnicodeTranslateError /\ __object: str /\ __start: int /\ __end: int /\ __reason: str) -> (return: NoneType))',
		},
	},
	'Warning': {
	},
	'UserWarning': {
	},
	'DeprecationWarning': {
	},
	'SyntaxWarning': {
	},
	'RuntimeWarning': {
	},
	'FutureWarning': {
	},
	'PendingDeprecationWarning': {
	},
	'ImportWarning': {
	},
	'UnicodeWarning': {
	},
	'BytesWarning': {
	},
	'ResourceWarning': {
	},
	'EncodingWarning': {
	},
	'builtins': {
		'abs': {
			r'((__x: SupportsAbs<T?0>) -> (return: T?0))',
		},
		'all': {
			r'((__iterable: Iterable<top>) -> (return: bool))',
		},
		'any': {
			r'((__iterable: Iterable<top>) -> (return: bool))',
		},
		'ascii': {
			r'((__obj: top) -> (return: str))',
		},
		'bin': {
			r'((__number: SupportsIndex+int) -> (return: str))',
		},
		'breakpoint': {
			r'((__va_args: top /\ __kw_kws: top) -> (return: NoneType))',
		},
		'chr': {
			r'((__i: int) -> (return: str))',
		},
		'copyright': {
			r'(() -> (return: NoneType))',
		},
		'credits': {
			r'(() -> (return: NoneType))',
		},
		'delattr': {
			r'((__obj: top /\ __name: str) -> (return: NoneType))',
		},
		'dir': {
			r'((__o: top) -> (return: list<str>))',
		},
		'divmod': {
			r'((__x: T?contra /\ __y: SupportsRDivMod<T?contra+T?co>) -> (return: T?co))',
			r'((__x: SupportsDivMod<T?contra+T?co> /\ __y: T?contra) -> (return: T?co))',
		},
		'format': {
			r'((__value: top /\ __format_spec: str) -> (return: str))',
		},
		'getattr': {
			r'((__o: top /\ __name: str /\ __default: NoneType) -> (return: top+NoneType))',
			r'((__o: top /\ __name: str /\ __default: bool) -> (return: bool+top))',
			r'((__o: top /\ name: str /\ __default: dict<top, top>) -> (return: dict<top, top>+top))',
			r'((__o: top /\ name: str /\ __default: list<top>) -> (return: top+list<top>))',
			r'((__o: top /\ __name: str /\ __default: T?0) -> (return: T?0+top))',
		},
		'globals': {
			r'(() -> (return: dict<str, top>))',
		},
		'hasattr': {
			r'((__obj: top /\ __name: str) -> (return: bool))',
		},
		'hash': {
			r'((__obj: top) -> (return: int))',
		},
		'help': {
			r'((request: top) -> (return: NoneType))',
		},
		'hex': {
			r'((__number: SupportsIndex+int) -> (return: str))',
		},
		'id': {
			r'((__obj: top) -> (return: int))',
		},
		'input': {
			r'((__prompt: top) -> (return: str))',
		},
		'iter': {
			r'((__iterable: GetItemIterable<T?0>) -> (return: Iterator<T?0>))',
			r'((__iterable: Iterable<SupportsNext>) -> (return: SupportsNext))',
		},
		'len': {
			r'((__obj: SupportsLen) -> (return: int))',
		},
		'license': {
			r'(() -> (return: NoneType))',
		},
		'locals': {
			r'(() -> (return: dict<str, top>))',
		},
		'max': {
			r'((__iterable: Iterable<SupportsRichComparisonT> /\ __ko_key: NoneType) -> (return: SupportsRichComparisonT))',
			r'((__iterable: Iterable<SupportsRichComparisonT> /\ __ko_key: NoneType /\ __ko_default: T?0) -> (return: T?0+SupportsRichComparisonT))',
			r'((__arg1: SupportsRichComparisonT /\ __arg2: SupportsRichComparisonT /\ __va__args: SupportsRichComparisonT /\ __ko_key: NoneType) -> (return: SupportsRichComparisonT))',
		},
		'min': {
			r'((__iterable: Iterable<SupportsRichComparisonT> /\ __ko_key: NoneType) -> (return: SupportsRichComparisonT))',
			r'((__iterable: Iterable<SupportsRichComparisonT> /\ __ko_key: NoneType /\ __ko_default: T?0) -> (return: T?0+SupportsRichComparisonT))',
			r'((__arg1: SupportsRichComparisonT /\ __arg2: SupportsRichComparisonT /\ __va__args: SupportsRichComparisonT /\ __ko_key: NoneType) -> (return: SupportsRichComparisonT))',
		},
		'next': {
			r'((__i: SupportsNext<T?0> /\ __default: T?V) -> (return: T?0+T?V))',
			r'((__i: SupportsNext<T?0>) -> (return: T?0))',
		},
		'oct': {
			r'((__number: SupportsIndex+int) -> (return: str))',
		},
		'ord': {
			r'((__c: bytearray+str+bytes) -> (return: int))',
		},
		'print': {
			r'((__va_values: top /\ __ko_sep: str+NoneType /\ __ko_end: str+NoneType /\ __ko_file: SupportsWrite<str>+NoneType /\ __ko_flush: bool) -> (return: NoneType))',
		},
		'repr': {
			r'((__obj: top) -> (return: str))',
		},
		'round': {
			r'((number: SupportsRound<T?0> /\ ndigits: NoneType) -> (return: T?0))',
			r'((number: SupportsRound<T?0> /\ ndigits: SupportsIndex) -> (return: T?0))',
		},
		'setattr': {
			r'((__obj: top /\ __name: str /\ __value: top) -> (return: NoneType))',
		},
		'sorted': {
			r'((__iterable: Iterable<SupportsRichComparisonT> /\ __ko_key: NoneType /\ __ko_reverse: bool) -> (return: list<SupportsRichComparisonT>))',
		},
		'sum': {
			r'((__iterable: Iterable<int>) -> (return: int))',
		},
		'vars': {
			r'((__object: top) -> (return: dict<str, top>))',
		},
	},

}
