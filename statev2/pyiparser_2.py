import ast
import astor
import logging
from statev2.basetype import *


BUILTIN_CATEGORY = 'builtins'
NAME_LITERAL = 'Literal'
BIG_SELF = 'Self'
SMALL_SELF = 'self'
SMALL_CLS = 'cls'
RETURN_VARNAME = 'return'
ignore_list = ['slice', 'GenericAlias', 'Callable', 'ellipsis', 'TracebackType', '_SupportsWriteAndFlush', 'CodeType',
               '_ClassInfo', '_Opener', 'type', 'super']
IGNORED_CLASSES = ['object', 'staticmethod', 'classmethod', 'ellipsis', '_FormatMapMapping',
                   '_TranslateTable', 'function', '_PathLike', '_SupportsSynchronousAnext',
                   '_GetItemIterable', '_SupportsWriteAndFlush', 'SupportsSomeKindOfPow',
                   '_SupportsPow2', '_SupportsPow3NoneOnly', '_SupportsPow3', '_SupportsRound1', '_SupportsRound2',
                   'BaseExceptionGroup', 'ExceptionGroup', '_SupportsSumWithNoDefaultGiven', 'type', 'super',
                   'memoryview']
DEFAULT_TYPEVAR = '_T'
SPEC_DEFAULT_TYPEVAR = 'T?0'
param_prefix = ['__po_', '', '__va_', '__ko_', '__kw_']
PREFIX_POSONLY, PREFIX_ARGS, PREFIX_VARARG, PREFIX_KWONLY, PREFIX_KWARG = range(5)
TYPE_REPLACE = {'_T': 'T?0', '_PositiveInteger': 'int', '_KT': 'T?K', '_VT': 'T?V', '_T_co': 'T?co',
                '_NegativeInteger': 'int', '_S': 'T?s',
                'object': 'TopType', 'ReadOnlyBuffer': 'bytes', 'Any': 'TopType',
                'WriteableBuffer': 'bytearray+memoryview', 'ReadableBuffer': 'bytes+bytearray+memoryview',
                '_TranslateTable': 'dict<int, str+int>', '_FormatMapMapping': 'dict<str, int>', 'LiteralString': 'str',
                'SupportsKeysAndGetItem': 'dict', 'AbstractSet': 'set', '_PathLike': 'str+bytes',
                '_GetItemIterable': 'GetItemIterable',
                '_SupportsPow2': 'SupportsSomeKindOfPow', '_SupportsPow3NoneOnly': 'SupportsSomeKindOfPow',
                '_SupportsPow3': 'SupportsSomeKindOfPow', '_SupportsRound1': 'SupportsRound',
                '_SupportsRound2': 'SupportsRound', '_T_contra': 'T?contra', 'SupportsIter': 'Iterable',
                '_SupportsNextT': 'SupportsNext', 'Sized': 'SupportsLen', 'FileDescriptorOrPath': 'str',
                '_SupportsSumNoDefaultT': 'int'}
# 0 - first typevar, 1 - second typevar, -1 - tuple<first, second>
DICT_SPECIFIC_TYPES = {'dict_keys': 0, 'dict_values': 1, 'dict_items': -1}
OUTPUT_FILE = 'specs_shed.py'
MAPPING_BASES = ['Mapping', 'MutableMapping', 'dict']


class IgnoredTypeError(Exception):
    pass


def get_logger(
        LOG_FORMAT='%(levelname)-4s %(message)s',
        LOG_NAME='',
        LOG_FILE_INFO='test.log',
        LOG_FILE_ERROR='test.err'):
    log = logging.getLogger(LOG_NAME)
    log_formatter = logging.Formatter(LOG_FORMAT)

    file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='w')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode='w')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    log.setLevel(logging.INFO)

    return log


mylogger = get_logger()


class CountClassFuncs(ast.NodeVisitor):
    def __init__(self):
        self.func_count = 0
        self.func_list = []

    def visit_FunctionDef(self, node):
        self.func_count += 1
        self.func_list.append(astor.to_source(node).strip())

    def get_func_count(self):
        return self.func_count


def is_ignored(_type: str, ignore_list):
    for ign in ignore_list:
        if _type.startswith(ign):
            return True
    return False


def parse_node_type(node: ast.expr) -> Basetype:
    if isinstance(node, ast.Name):
        # int, list, float, _T, ...
        new_name = TYPE_REPLACE[node.id] if node.id in TYPE_REPLACE else node.id
        if new_name.startswith('T'):
            ptip = VarType(new_name)
        else:
            ptip = PyType(eval(new_name))
        bt = Basetype({ptip})
        return bt
    elif isinstance(node, ast.Constant):
        # 3, 5.6, 'a', ...
        bt = Basetype({PyType(type(node.value))})
        return bt
    elif isinstance(node, ast.Subscript):
        # list[int], dict[int, float], list[int | float], ...
        if not isinstance(node.value, ast.Name):
            ss = f'{type(node.value)} is not yet supported'
            mylogger.warning(ss)
            raise TypeError(ss)
        container = TYPE_REPLACE[node.value.id] if node.value.id in TYPE_REPLACE else node.value.id
        if container in ignore_list:
            ss = f'ignored type (for now) <<{container}>> for {astor.to_source(node.value).strip()}'
            mylogger.warning(ss)
            raise TypeError(ss)
        contained = node.slice
        kvtuple = False
        if container in MAPPING_BASES or container in DICT_SPECIFIC_TYPES:
            kvtuple = True
        if not isinstance(node.value, ast.Name):
            ss = f'{type(node.value)} is not yet supported here'
            mylogger.warning(ss)
            raise TypeError(ss)
        contained_str = ''
        container_ptip = PyType(eval(container))
        if isinstance(contained, ast.Name) or isinstance(contained, ast.BinOp):
            if kvtuple:
                ss = f'Type {astor.to_source(node)} is not compatible with key-value pairs'
                mylogger.warning(ss)
                raise TypeError(ss)
            container_ptip.keys = parse_node_type(contained)
            return Basetype({container_ptip})
        elif isinstance(contained, ast.Tuple):
            if not kvtuple:
                contained_bt = Basetype()
                for elem in contained.elts:
                    contained_bt |= parse_node_type(elem)
                container_ptip.keys = deepcopy(contained_bt)
            else:
                if len(contained.elts) != 2:
                    ss = f'{astor.to_source(node)} type not supported for key-value pairs'
                    mylogger.warning(ss)
                    raise TypeError(ss)
                container_ptip.keys = parse_node_type(contained.elts[0])
                container_ptip.values = parse_node_type(contained.elts[1])
            return Basetype({container_ptip})
        else:
            ss = f'Slice for {astor.to_source(node)} is not yet supported'
            mylogger.warning(ss)
            raise TypeError(ss)
    elif isinstance(node, ast.BinOp):
        # int | float, complex | list[int], ...
        if not isinstance(node.op, ast.BitOr):
            ss = f'{node.op} operation not supported for types {node.left} and {node.right}'
            mylogger.warning(ss)
            raise TypeError(ss)
        bt = Basetype()
        bt |= parse_node_type(node.left)
        bt |= parse_node_type(node.right)
        return bt
    else:
        ss = f'{type(node)} is not yet supported here'
        mylogger.warning(ss)
        raise TypeError(ss)


def old_parse_node_type(node: ast.expr) -> str:

    def get_types_from_list(_elts: list):
        _type_list = []
        for _type in _elts:
            str_type = parse_node_type(_type)
            # if is_ignored(str_type):
            #     continue
            if str_type == '':
                continue
            _type_list.append(str_type)
        return _type_list

    if isinstance(node, ast.Name):
        open('types.txt', 'a').write(node.id + '\n')
        return_id = TYPE_REPLACE[node.id] if node.id in TYPE_REPLACE else node.id
        # if cls.is_ignored(return_id):
        #     ss = f'ignored type (for now) <<{return_id}>> for {node.id}'
        #     mylogger.warning(ss)
        #     raise TypeError(ss)
        #     # return ''
        return return_id
    elif isinstance(node, ast.Constant):
        open('types.txt', 'a').write(type(node.value).__name__ + '\n')
        return type(node.value).__name__
    elif isinstance(node, ast.Subscript):
        contained = node.slice
        if not isinstance(node.value, ast.Name):
            ss = f'{type(node.value)} is not yet supported'
            mylogger.warning(ss)
            raise TypeError(ss)
        # container = node.value.id
        container = TYPE_REPLACE[node.value.id] if node.value.id in TYPE_REPLACE else node.value.id
        if container in ignore_list:
            ss = f'ignored type (for now) <<{container}>> for {astor.to_source(node.value).strip()}'
            mylogger.warning(ss)
            raise TypeError(ss)
        kvtuple = False
        if container in MAPPING_BASES or container in DICT_SPECIFIC_TYPES:
            kvtuple = True
        if not isinstance(node.value, ast.Name):
            ss = f'{type(node.value)} is not yet supported here'
            mylogger.warning(ss)
            raise TypeError(ss)
        # open('types.txt', 'a').write(container + '\n')
        contained_str = ''
        if isinstance(contained, ast.Tuple):
            type_set = get_types_from_list(contained.elts)  # list here
            if not kvtuple:
                type_set = set(type_set)
                contained_str = '+'.join(type_set)
            else:
                if len(type_set) != 2:
                    ss = f'{type_set} types not supported for key-value pairs'
                    mylogger.warning(ss)
                    raise TypeError(ss)
                if container in DICT_SPECIFIC_TYPES:
                    if DICT_SPECIFIC_TYPES[container] == 0:
                        contained_str = type_set[0]
                    elif DICT_SPECIFIC_TYPES[container] == 1:
                        contained_str = type_set[1]
                    else:
                        contained_str = f'tuple<{type_set[0]}+{type_set[1]}>'
                else:
                    contained_str = ', '.join(type_set)
        else:
            contained_str = parse_node_type(contained)
        if container == NAME_LITERAL:
            return contained_str
        else:
            if container in DICT_SPECIFIC_TYPES:
                return 'list' + '< ' + contained_str + ' >'
            else:
                return container + '< ' + contained_str + ' >'
    elif isinstance(node, ast.BinOp):
        if not isinstance(node.op, ast.BitOr):
            ss = f'{node.op} operation not supported for types {node.left} and {node.right}'
            mylogger.warning(ss)
            raise TypeError(ss)
        type_set = set(get_types_from_list([node.left, node.right]))
        return '+'.join(type_set)
        # return cls.parse_node_type(node.left) + '+' + cls.parse_node_type(node.right)
    elif isinstance(node, ast.List):
        container = 'list'
        type_set = set(get_types_from_list(node.elts))
        contained_str = '+'.join(type_set)
        return container + '< ' + contained_str + ' >'
    elif isinstance(node, ast.Tuple):
        container = 'tuple'
        type_set = set(get_types_from_list(node.elts))
        contained_str = '+'.join(type_set)
        return container + '< ' + contained_str + ' >'
    else:
        ss = f'{type(node)} is not yet supported here'
        mylogger.warning(ss)
        raise TypeError(ss)


def get_basetype_from_classdef(node: ast.ClassDef):
    self_type = node.name
    past_slice = None
    ptip = PyType(eval(self_type))
    mapping_bases = ['Mapping', 'MutableMapping', 'dict']
    for base in node.bases:
        if isinstance(base, ast.Subscript):
            if not past_slice:
                parsed_type = self.parse_node_type(base)
                if parsed_type == '':
                    ss = f'Type for node {base} not supported'
                    mylogger.error(ss)
                    raise TypeError(ss)
                parsed_slice = '< ' + parsed_type.split('<', maxsplit=1)[1].strip()
                # self_type += '<' + self.parse_node_type(base.slice, True, kvtuple) + '>'
                self_type += parsed_slice
                past_slice = base.slice
            else:
                # if past_slice.id != base.slice.id:
                if astor.to_source(past_slice) != astor.to_source(base.slice):
                    ss = f'Inconsistent slice for {node.name}'
                    mylogger.warning(ss)
                    raise TypeError(ss)


class ClassdefToBasetypes(ast.NodeVisitor):

    def __init__(self):
        self.spec_dict = dict()
        self.specs = dict()
        self.total_funcdefs = 0
        self.parsed_funcdefs = 0
        self.class_stats = dict()
        self.current_class = None
        self.self_type = None

    # def get_from_base(self, base: ast.Name | ast.Subscript) -> Basetype:
    #     past_slice = None
    #     if isinstance(base, ast.Subscript):
    #         if not past_slice:
    #             # aux = self.parse_node_type(base)
    #             kvtuple = False
    #             if base.value.id in MAPPING_BASES:
    #                 kvtuple = True
    #             parsed_type = self.parse_node_type(base)
    #             if parsed_type == '':
    #                 ss = f'Type for node {base} not supported'
    #                 mylogger.error(ss)
    #                 raise TypeError(ss)
    #             parsed_slice = '< ' + parsed_type.split('<', maxsplit=1)[1].strip()
    #             # self_type += '<' + self.parse_node_type(base.slice, True, kvtuple) + '>'
    #             self_type += parsed_slice
    #             past_slice = base.slice
    #         else:
    #             # if past_slice.id != base.slice.id:
    #             if astor.to_source(past_slice) != astor.to_source(base.slice):
    #                 ss = f'Inconsistent slice for {node.name}'
    #                 mylogger.warning(ss)
    #                 raise TypeError(ss)

    def visit_ClassDef(self, node: ast.ClassDef):
        global mylogger
        str_type = node.name
        special_sequences = ['str', 'bytes', 'bytearray']
        for base in node.bases:
            if (not isinstance(base, ast.Subscript)) or (node.name in special_sequences):
                continue
            else:
                str_slice = astor.to_source(base.slice).strip()
                str_type += f'[{str_slice}]'
                break
        ast_type = ast.parse(str_type).body[0].value
        self.self_type = parse_node_type(ast_type)


def write_op_equivalences():
    equiv_dict = {
        'ast.UnaryOp':
            {
                'ast.UAdd': '__pos__',
                'ast.USub': '__neg__',
                'ast.Not': '__bool__',
                'ast.Invert': '__invert__',
            },
        'ast.BinOp':
            {
                'ast.Add': '__add__',
                'ast.Sub': '__sub__',
                'ast.Mult': '__mul__ ',
                'ast.Div': '__truediv__ ',
                'ast.FloorDiv': '__floordiv__',
                'ast.Mod': '__mod__',
                'ast.Pow': '__pow__',
                'ast.LShift': '__lshift__',
                'ast.RShift': '__rshift__',
                'ast.BitOr': '__or__',
                'ast.BitXor': '__xor__',
                'ast.BitAnd': '__and__',
                'ast.MatMult': '__matmul__',
            }
    }
    with open(OUTPUT_FILE, 'a') as f:
        f.write('op_equiv = {\n')
        for node, funcdict in equiv_dict.items():
            f.write(f'\t{node}: {{\n')
            for nodeop, funcname in funcdict.items():
                f.write(f'\t\t{nodeop}: \'{funcname}\',\n')
            f.write('\t},\n')
        f.write('}\n\n\n')


# def write_type_equivalences():
#     equiv = get_equivalences_dict()
#     with open(OUTPUT_FILE, 'a') as f:
#         f.write('type_equiv = {\n')
#         for node, typelist in equiv.items():
#             sum_string = '+'.join(typelist)
#             f.write(f'\t{node.__name__}: \'{sum_string}\',\n')
#         f.write('}\n\n\n')


def generate_specs(stub_file):
    ctb = ClassdefToBasetypes()
    tree = ast.parse(open(stub_file, 'r').read())
    ctb.visit(tree)


if __name__ == "__main__":
    generate_specs('../pyiparser/builtins.pyi')
