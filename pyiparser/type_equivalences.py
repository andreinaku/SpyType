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
#
#
# class NoneType:
#     pass


rules = {
    ('__index__',): SupportsIndex,
    ('__iter__',): Iterable,
    ('__lt__', '__gt__'): SupportsRichComparison,
    ('__lt__', '__gt__'): SupportsRichComparisonT,
}
# builtin types according to the Python Library Reference: https://docs.python.org/3.11/library/stdtypes.html
builtin_types = ['int', 'float', 'complex', 'iterator', 'list', 'tuple', 'range', 'str', 'bytes', 'bytearray',
                 'memoryview', 'set', 'frozenset', 'dict', 'NoneType', 'object']


def get_dict():
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
    aux = get_dict()
    print(aux)
