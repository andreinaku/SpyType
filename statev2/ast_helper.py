import ast
import astpretty
from collections.abc import Awaitable, Callable, Iterable, Iterator, MutableSet, Reversible, Set as AbstractSet, Sized


# expr = 'class int(sometype[anothertype[_T]]): ...'
with open('ast.out', 'w') as f:
    f.write(astpretty.pformat(ast.parse('int')))
    f.write('\n-----------------\n')
    f.write(astpretty.pformat(ast.parse('list[int]')))
    f.write('\n-----------------\n')
    f.write(astpretty.pformat(ast.parse('dict[int,str]')))
    f.write('\n-----------------\n')
    f.write(astpretty.pformat(ast.parse('list[int | float]')))
    f.write('\n-----------------\n')
    f.write(astpretty.pformat(ast.parse('list[int, float]')))
    f.write('\n-----------------\n')
    f.write(astpretty.pformat(ast.parse('class int(sometype[anothertype[_T]]): ...')))
    f.write('\n-----------------\n')
    aux = '''
class int:
    def __add__(self, other: int) -> int: ...
    '''
    tree = ast.parse(aux)
    f.write(astpretty.pformat(tree))
    f.write('\n-----------------\n')
    # row, column = pos
    f.write(astpretty.pformat(ast.parse('row, column = pos')))
    f.write('\n-----------------\n')
    f.write(astpretty.pformat(ast.parse('x, *y, z = 1,2,3,4,5')))
    f.write('\n-----------------\n')
