from utils.utils import BottomType, TopType


# builtin types according to the Python Library Reference: https://docs.python.org/3.11/library/stdtypes.html
# minus the iterator type, for now
builtin_types = [bool, int, float, complex, range, str, bytes, bytearray,
                 memoryview, type(None), object, BottomType, TopType]
builtin_seqs = [set, frozenset, list, tuple]
builtin_dicts = [dict]
builtins = [builtin_types, builtin_seqs, builtin_dicts]


def is_supported_type(tip, strict=True) -> bool:
    if strict and tip in builtin_types:
        return True
    if not strict and isinstance(tip, type):
        return True
    for _builtin in builtins:
        for btype in _builtin:
            try:
                if issubclass(btype, tip):
                    return True
            except TypeError:
                continue
    return False
