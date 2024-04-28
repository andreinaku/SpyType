import re
from copy import deepcopy
import sys


def find_same_contained(test_str):
    test_str = test_str.strip()
    if '->' not in test_str:
        return False
    if test_str.startswith('#'):
        return False
    _in, _out = test_str.split('->')
    _in = _in.strip()
    _out = _out.strip()
    pattern = re.compile(r'Iterable\[(.*?[_T0-9]+.*?)\]')
    m = re.findall(pattern, _in)
    for elem in m:
        splits = re.split(r',|;|\|', elem)
        input_typevars = set()
        for split_elem in splits:
            split_elem = split_elem.strip()
            if split_elem.startswith('_T'):
                input_typevars.add(deepcopy(split_elem))
        for tv in input_typevars:
            if tv in _out:
                return True
    return False


if __name__ == '__main__':
    lines = open('sheds/builtins.pyi', 'r').readlines()
    # lines = ['def __new__(cls, __iter1: Iterable[_T1, _T2]) -> zip[tuple[_T1]]: ...']
    for line in lines:
        if find_same_contained(line):
            print(line.strip())
