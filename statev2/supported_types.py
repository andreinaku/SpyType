from utils import BottomType, TopType

# builtin types according to the Python Library Reference: https://docs.python.org/3.11/library/stdtypes.html
# minus the iterator type, for now
builtin_types = [bool, int, float, complex, list, tuple, range, str, bytes, bytearray,
                 memoryview, set, frozenset, dict, type(None), object, BottomType, TopType]


def is_supported_type(tip, strict=True) -> bool:
    if strict and tip in builtin_types:
        return True
    if not strict and isinstance(tip, type):
        return True
    for btype in builtin_types:
        try:
            if issubclass(btype, tip):
                return True
        except TypeError:
            continue
    return False
