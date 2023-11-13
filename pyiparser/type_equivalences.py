import builtins
import inspect
import typing


class SupportsIndex:
    pass


class Iterable:
    pass


class SupportsRichComparison:
    pass


class SupportsRichComparisonT:
    pass


class Iterator:
    pass


class SupportsInt:
    pass


class SupportsTrunc:
    pass


class SupportsFloat:
    pass


class SupportsBytes:
    pass


class SupportsSynchronousAnext:
    pass


class GetItemIterable:
    pass


class SupportsSomeKindOfPow:
    pass


class Reversible:
    pass


class SupportsLen:
    pass


class SupportsLenAndGetItem:
    pass


class SupportsRound:
    pass


class SupportsAbs:
    pass


class SupportsDivMod:
    pass


class SupportsRDivMod:
    pass


class SupportsNext:
    pass


class SupportsWrite:
    pass


class SupportsRead:
    pass
#
#
# class NoneType:
#     pass


rules = {
    ('__index__',): SupportsIndex,
    ('__iter__',): Iterable,
    ('__lt__', '__gt__'): SupportsRichComparison,
    ('__lt__', '__gt__'): SupportsRichComparisonT,
    ('__int__',): SupportsInt,
    ('__float__',): SupportsFloat,
    ('__trunc__',): SupportsTrunc,
    ('__bytes__',): SupportsBytes,
    ('__anext__',): SupportsSynchronousAnext,
    ('__getitem__',): GetItemIterable,
    ('__pow__',): SupportsSomeKindOfPow,
    ('__reversed__', '__iter__'): Reversible,
    ('__len__',): SupportsLen,
    ('__len__', '__getitem__'): SupportsLenAndGetItem,
    ('__round__',): SupportsRound,
    ('__abs__',): SupportsAbs,
    ('__divmod__',): SupportsDivMod,
    ('__rdivmod__',): SupportsRDivMod,
    ('__next__',): SupportsNext,
    ('write',): SupportsWrite,
    ('read',): SupportsRead,
}
# builtin types according to the Python Library Reference: https://docs.python.org/3.11/library/stdtypes.html
builtin_types = ['int', 'float', 'complex', 'iterator', 'list', 'tuple', 'range', 'str', 'bytes', 'bytearray',
                 'memoryview', 'set', 'frozenset', 'dict', 'NoneType', 'object']


def get_equivalences_dict():
    equiv_dict = dict()
    for name, obj in inspect.getmembers(builtins):
        if not inspect.isclass(obj):
            continue
        for conditions, sugar in rules.items():
            flag = True
            for funcname in conditions:
                if funcname not in obj.__dict__:
                    flag = False
                    break
            if not flag:
                continue
            if name not in builtin_types:
                continue
            if sugar in equiv_dict:
                equiv_dict[sugar].append(name)
            else:
                equiv_dict[sugar] = [name]
    return equiv_dict


if __name__ == '__main__':
    aux = get_equivalences_dict()
    print(aux)
