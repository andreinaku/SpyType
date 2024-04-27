import ast
import typing

import astor
import logging
from statev2.basetype import *
from typing_extensions import *
from statev2.supported_types import builtin_types

# from typing_extensions import (
#     Concatenate,
#     Literal,
#     LiteralString,
#     ParamSpec,
#     Self,
#     SupportsIndex,
#     TypeAlias,
#     TypeGuard,
#     TypeVarTuple,
#     final,
# )

MAX_VARTYPE_LEN = 6
BUILTIN_CATEGORY = 'builtins'
NAME_LITERAL = 'Literal'
BIG_SELF = 'Self'
SMALL_SELF = 'self'
SMALL_CLS = 'cls'
RETURN_VARNAME = 'return'
ignore_list = ['slice', 'GenericAlias', 'Callable', 'ellipsis', 'TracebackType', '_SupportsWriteAndFlush', 'CodeType',
               '_ClassInfo', '_Opener', 'type', 'super', 'SupportsAbs']
IGNORED_CLASSES = ['object', 'staticmethod', 'classmethod', 'ellipsis', '_FormatMapMapping',
                   '_TranslateTable', 'function', '_PathLike', '_SupportsSynchronousAnext',
                   '_GetItemIterable', '_SupportsWriteAndFlush', 'SupportsSomeKindOfPow',
                   '_SupportsPow2', '_SupportsPow3NoneOnly', '_SupportsPow3', '_SupportsRound1', '_SupportsRound2',
                   'BaseExceptionGroup', 'ExceptionGroup', '_SupportsSumWithNoDefaultGiven', 'type', 'super',
                   'memoryview']
DEFAULT_TYPEVAR = '_T'
# SPEC_DEFAULT_TYPEVAR = 'T?0'
# param_prefix = ['__po_', '', '__va_', '__ko_', '__kw_']
PREFIX_POSONLY, PREFIX_ARGS, PREFIX_VARARG, PREFIX_KWONLY, PREFIX_KWARG = range(5)
TYPE_REPLACE = {'_PositiveInteger': 'int',
                '_NegativeInteger': 'int',
                'object': 'TopType',
                'ReadOnlyBuffer': 'bytes',
                'Any': 'TopType',
                'WriteableBuffer': 'bytearray | memoryview',
                'ReadableBuffer': 'bytes | bytearray | memoryview',
                '_TranslateTable': 'dict[int, str | int]',
                '_FormatMapMapping': 'dict[str, int]',
                'LiteralString': 'str',
                'SupportsKeysAndGetItem': 'dict',
                'AbstractSet': 'set',
                '_PathLike': 'str | bytes',
                # '_GetItemIterable': 'GetItemIterable',
                # '_SupportsPow2': 'SupportsSomeKindOfPow', '_SupportsPow3NoneOnly': 'SupportsSomeKindOfPow',
                # '_SupportsPow3': 'SupportsSomeKindOfPow', '_SupportsRound1': 'SupportsRound',
                # '_SupportsRound2': 'SupportsRound',
                # 'SupportsIter': 'Iterable',
                # '_SupportsNextT': 'SupportsNext', 'Sized': 'SupportsLen',
                'FileDescriptorOrPath': 'str',
                '_SupportsSumNoDefaultT': 'int'}
VARTYPE_REPLACE = {
    '_T': 'T?0', '_KT': 'T?1', '_VT': 'T?2', '_T_co': 'T?3',
    '_S': 'T?4', '_P': 'T?5', '_R_co': 'T?6', '_T_contra': 'T?7'
}
# 0 - first typevar, 1 - second typevar, -1 - tuple<first, second>
DICT_SPECIFIC_TYPES = {'dict_keys': 0, 'dict_values': 1, 'dict_items': -1}
OUTPUT_FILE = 'specs_shed.py'
MAPPING_BASES = ['Mapping', 'MutableMapping', 'dict']


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


class TypeReplacer(ast.NodeTransformer):
    def visit_Name(self, node):
        if node.id in TYPE_REPLACE:
            new_id = TYPE_REPLACE[node.id]
            if new_id.startswith('T?'):
                new_node = deepcopy(node)
                new_node.id = deepcopy(new_id)
            else:
                new_node = ast.parse(new_id).body[0].value
        else:
            new_node = deepcopy(node)
        return new_node


class ClassdefToBasetypes(ast.NodeVisitor):

    def __init__(self):
        self.spec_dict = dict()
        self.specs = dict()
        self.total_funcdefs = 0
        self.parsed_funcdefs = 0
        self.class_stats = dict()
        self.current_class = None
        self.self_type = Basetype({PyType(type(None))})

    @staticmethod
    def get_funcnode_from_name(classnode: ast.ClassDef, funcname: str) -> ast.FunctionDef:
        for node in classnode.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            if node.name == funcname:
                return node
        return None

    def parse_node_type(self, node: ast.expr) -> Basetype:
        if isinstance(node, ast.Name):
            # int, list, float, _T, ...
            new_name = TYPE_REPLACE[node.id] if node.id in TYPE_REPLACE else node.id
            # new_name = node.id
            if new_name.startswith('_') and len(new_name) <= MAX_VARTYPE_LEN:
                ptip = VarType(new_name)
                bt = Basetype({ptip})
            elif new_name == BIG_SELF:
                bt = deepcopy(self.self_type)
            elif new_name == 'TopType':
                bt = Basetype({PyType(TopType)})
            elif new_name == 'BottomType':
                bt = Basetype({PyType(BottomType)})
            else:
                ptip = PyType(eval(new_name))
                bt = Basetype({ptip})
                # bt = get_builtin_basetype(ptip)
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
            # container = node.value.id
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
            # todo: are there Protocol containers used anywhere? 
            container_ptip = PyType(eval(container))
            if isinstance(contained, ast.Name) or isinstance(contained, ast.BinOp):
                if kvtuple:
                    ss = f'Type {astor.to_source(node)} is not compatible with key-value pairs'
                    mylogger.warning(ss)
                    raise TypeError(ss)
                container_ptip.keys = self.parse_node_type(contained)
                return Basetype({container_ptip})
            elif isinstance(contained, ast.Tuple):
                if not kvtuple:
                    contained_bt = Basetype()
                    for elem in contained.elts:
                        contained_bt |= self.parse_node_type(elem)
                    container_ptip.keys = deepcopy(contained_bt)
                else:
                    if len(contained.elts) != 2:
                        ss = f'{astor.to_source(node)} type not supported for key-value pairs'
                        mylogger.warning(ss)
                        raise TypeError(ss)
                    container_ptip.keys = self.parse_node_type(contained.elts[0])
                    container_ptip.values = self.parse_node_type(contained.elts[1])
                return Basetype({container_ptip})
            else:
                ss = f'Slice for {astor.to_source(node).strip()} is not yet supported'
                mylogger.warning(ss)
                raise TypeError(ss)
        elif isinstance(node, ast.BinOp):
            # int | float, complex | list[int], ...
            if not isinstance(node.op, ast.BitOr):
                ss = f'{node.op} operation not supported for types {node.left} and {node.right}'
                mylogger.warning(ss)
                raise TypeError(ss)
            bt = Basetype()
            bt |= self.parse_node_type(node.left)
            bt |= self.parse_node_type(node.right)
            return bt
        else:
            ss = f'{type(node)} is not yet supported here'
            mylogger.warning(ss)
            raise TypeError(ss)

    def parse_funcdef(self, node: ast.FunctionDef) -> FuncSpec:
        param_lists = [node.args.posonlyargs, node.args.args, [node.args.vararg],
                       node.args.kwonlyargs, [node.args.kwarg]]
        param_prefix = ['__po_', '', '__va_', '__ko_', '__kw_']
        func_spec = FuncSpec()
        for i in range(0, len(param_lists)):
            # for parameters in param_lists:
            parameters = param_lists[i]
            prefix = param_prefix[i]
            if len(parameters) == 0:
                continue
            if len(parameters) == 1 and parameters[0] is None:
                continue  # no vararg or kwarg
            for param in parameters:
                try:
                    if param.arg == SMALL_SELF and param.annotation is None:
                        param_basetype = self.self_type
                    else:
                        param_basetype = self.parse_node_type(param.annotation)
                        param_basetype = get_builtin_from_bt(param_basetype)
                except NameError:
                    ss = f'This type is unsupported: {astor.to_source(param.annotation)}'
                    raise TypeError(ss)
                new_basetype = param_basetype.filter_pytypes(builtin_types)
                if len(new_basetype) == 0:
                    raise TypeError(f'This basetype ({astor.to_source(param.annotation).strip()}) '
                                    f'is fully unsupported: {param_basetype}')
                param_basetype = new_basetype
                spec_param_name = f'{prefix}{param.arg}'
                func_spec.in_state.assignment[spec_param_name] = deepcopy(param_basetype)
        return_basetype = self.parse_node_type(node.returns)
        return_basetype = get_builtin_from_bt(return_basetype)
        new_basetype = return_basetype.filter_pytypes(builtin_types)
        if len(new_basetype) == 0:
            raise TypeError(f'This basetype (return) is fully unsupported: {return_basetype}')
        return_basetype = new_basetype
        func_spec.out_state.assignment[RETURN_VARNAME] = deepcopy(return_basetype)
        return func_spec

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
        try:
            self.self_type = self.parse_node_type(ast_type)
            mylogger.info(f'Successfully parsed class {node.name}')
        except Exception as exc:
            ss = f'Cannot parse type for class {node.name} with exception {str(exc)}'
            mylogger.error(ss)
        for body_node in node.body:
            try:
                if not isinstance(body_node, ast.FunctionDef):
                    continue
                try:
                    func_spec = self.parse_funcdef(body_node)
                except TypeError as te:
                    mylogger.error(str(te))
                    continue
                funcname = body_node.name
                if funcname not in self.spec_dict:
                    self.spec_dict[funcname] = {func_spec}
                else:
                    self.spec_dict[funcname].add(func_spec)
            except Exception as exc:
                ss = f'Cannot parse type for function {body_node.name} in class {node.name} with exception {str(exc)}'
                mylogger.error(ss)
                continue


def dump_specs(filename: str, united: dict[str, set[FuncSpec]], indent=4):
    def write_op_equivalences(f: IO):
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
                    'ast.Mult': '__mul__',
                    'ast.Div': '__truediv__',
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
        f.write('op_equiv = {\n')
        spaces = ' ' * indent
        for node, funcdict in equiv_dict.items():
            f.write(f'{spaces}{node}: {{\n')
            for nodeop, funcname in funcdict.items():
                f.write(f'{spaces * 2}{nodeop}: \'{funcname}\',\n')
            f.write(f'{spaces}}},\n')
        f.write('}\n\n\n')

    def write_united_specs(f: IO):
        f.write('unitedspecs = {\n')
        spaces = ' ' * indent
        for funcname, spec_set in united.items():
            f.write(f'{spaces}\'{funcname}\': {{\n')
            for func_spec in spec_set:
                writestr = f'{spaces * 2}r\'{func_spec}\',\n'
                f.write(writestr)
            f.write(f'{spaces}}},\n')
        f.write('\n}\n')

    def write_headers(f: IO):
        f.write('import ast\n\n')

    with open(filename, 'w') as of:
        write_headers(of)
        write_op_equivalences(of)
        write_united_specs(of)


def filter_specs(spec_dict: dict[str, set[FuncSpec]]) -> dict[str, set[FuncSpec]]:
    replaced_dict = dict()
    for funcname, funcspecs in spec_dict.items():
        replaced_dict[funcname] = set()
        for funcspec in funcspecs:
            new_spec = deepcopy(funcspec)
            for to_replace, replace_with in VARTYPE_REPLACE.items():
                new_spec = new_spec.replace_vartype(to_replace, replace_with)
            replaced_dict[funcname].add(new_spec)
    return replaced_dict


def get_root_specs(stub_ast: ast.Module) -> dict[str, set[FuncSpec]]:
    spec_dict = dict()
    for node in stub_ast.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        try:
            funcspec = ClassdefToBasetypes().parse_funcdef(node)
        except TypeError as te:
            continue
        if node.name not in spec_dict:
            spec_dict[node.name] = {funcspec}
        else:
            spec_dict[node.name].add(funcspec)
    return spec_dict


def generate_specs(stub_file):
    ctb = ClassdefToBasetypes()
    tree = ast.parse(open(stub_file, 'r').read())
    tree = TypeReplacer().visit(tree)
    ctb.visit(tree)
    replaced_dict = filter_specs(ctb.spec_dict)
    if 'builtins' in replaced_dict:
        raise RuntimeError(f'Builtins class already exists in stub file. Aborting!')
    # replaced_dict['builtins'] = get_root_specs(tree)
    root_specs = get_root_specs(tree)
    for funcname, funcspecs in root_specs.items():
        if funcname not in replaced_dict:
            replaced_dict[funcname] = deepcopy(funcspecs)
        else:
            replaced_dict[funcname] |= funcspecs
    replaced_dict = filter_specs(replaced_dict)
    dump_specs('united_specs.py', replaced_dict)


if __name__ == "__main__":
    generate_specs('sheds/builtins.pyi')