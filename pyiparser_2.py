import ast
import astor
import logging
from statev2.basetype import *
from typing_extensions import *
from statev2.supported_types import builtin_types
import inspect
import types


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
WEIRD_SELF = 'type[_typeshed.Self]'
WEIRD_SELF_2 = '_typeshed.Self'
TYPE_SELF = 'type[Self]'
SELFS = [BIG_SELF, SMALL_SELF, SMALL_CLS, WEIRD_SELF, WEIRD_SELF_2, TYPE_SELF]
RETURN_VARNAME = 'return'
# ignore_list = ['slice', 'GenericAlias', 'Callable', 'ellipsis', 'TracebackType', '_SupportsWriteAndFlush', 'CodeType', '_ClassInfo', '_Opener', 'type', 'super', 'SupportsAbs']
ignore_list = [
    'slice',
    'GenericAlias', 
    'Callable',
    'ellipsis',
    'TracebackType',
    '_SupportsWriteAndFlush',
    'CodeType',
    '_ClassInfo',
    '_Opener',
    # 'type',
    'super',
    'SupportsAbs'
]
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
TYPE_REPLACE = {
    '_PositiveInteger': 'int',
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
    'FileDescriptorOrPath': 'str',
    '_SupportsSumNoDefaultT': 'int',
    'SupportsTrunc': 'int | float',
    WEIRD_SELF: 'Self',
}
VARTYPE_REPLACE = {
    '_T': 'T?0', '_KT': 'T?1', '_VT': 'T?2', '_T_co': 'T?3',
    '_S': 'T?4', '_P': 'T?5', '_R_co': 'T?6', '_T_contra': 'T?7'
}
# 0 - first typevar, 1 - second typevar, -1 - tuple<first, second>
DICT_SPECIFIC_TYPES = {'dict_keys': 0, 'dict_values': 1, 'dict_items': -1}
OUTPUT_FILE = 'specs_shed.py'
MAPPING_BASES = ['Mapping', 'MutableMapping', 'dict']


class WarningOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.WARNING
    

class InfoOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


def get_logger(
        LOG_FORMAT='%(levelname)-4s %(message)s',
        LOG_NAME='',
        LOG_FILE_INFO='test.log',
        LOG_FILE_WARN='test.warn',
        LOG_FILE_ERROR='test.err'):
    log = logging.getLogger(LOG_NAME)
    log_formatter = logging.Formatter(LOG_FORMAT)

    file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='w')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    file_handler_info.addFilter(InfoOnlyFilter())
    log.addHandler(file_handler_info)

    file_handler_warn = logging.FileHandler(LOG_FILE_WARN, mode='w')
    file_handler_warn.setFormatter(log_formatter)
    file_handler_warn.setLevel(logging.WARNING)
    file_handler_warn.addFilter(WarningOnlyFilter())
    log.addHandler(file_handler_warn)

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
        if isinstance(node.body[0].value, ast.Constant) and node.body[0].value.value == Ellipsis:
            self.func_count += 1
        self.func_list.append(tosrc(node))

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
            elif new_name in SELFS:
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
            if hasattr(node.slice, "elts"):
                slice_len = len(node.slice.elts)
                if slice_len != 2:
                    ss = f'{inspect.currentframe().f_lineno}: {tosrc(node)} is not yet supported'
                    mylogger.warning(ss)
                    raise TypeError(ss)
            if not isinstance(node.value, ast.Name):
                # todo: tosrc(node.value) daca nu e nume
                container = tosrc(node.value)
                # ss = f'{inspect.currentframe().f_lineno}: {tosrc(node.value)} is not yet supported'
                # mylogger.warning(ss)
                # raise TypeError(ss)
            else:
                container = TYPE_REPLACE[node.value.id] if node.value.id in TYPE_REPLACE else node.value.id
            # container = node.value.id
            if container in ignore_list:
                ss = f'{inspect.currentframe().f_lineno}: ignored type (for now) <<{container}>> for {tosrc(node.value)}'
                mylogger.warning(ss)
                raise TypeError(ss)
            contained = node.slice
            kvtuple = False
            if container in MAPPING_BASES or container in DICT_SPECIFIC_TYPES:
                kvtuple = True
            # if not isinstance(node.value, ast.Name):
            #     ss = f'{inspect.currentframe().f_lineno}: {type(node.value)} is not yet supported here'
            #     mylogger.warning(ss)
            #     raise TypeError(ss)
            contained_str = ''
            # todo: try except on eval
            container_ptip = PyType(eval(container))
            if isinstance(contained, ast.Name) or isinstance(contained, ast.BinOp):
                if kvtuple:
                    ss = f'Type {tosrc(node)} is not compatible with key-value pairs'
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
                        ss = f'{tosrc(node)} type not supported for key-value pairs'
                        mylogger.warning(ss)
                        raise TypeError(ss)
                    container_ptip.keys = self.parse_node_type(contained.elts[0])
                    container_ptip.values = self.parse_node_type(contained.elts[1])
                return Basetype({container_ptip})
            else:
                ss = f'{inspect.currentframe().f_lineno}: Slice for {tosrc(node).strip()} is not yet supported'
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
            # exceptions from the rule <3
            annotation_str = tosrc(node)
            if annotation_str in SELFS:  # return: Self and others like that
                return self.self_type
            ss = f'{inspect.currentframe().f_lineno}: {type(node)} is not yet supported here'
            mylogger.warning(ss)
            raise TypeError(ss)

    def parse_funcdef(self, node: ast.FunctionDef) -> FuncSpec:
        # mark positionals which have default values
        defaults_prefix = '__d_'
        args_list = deepcopy(node.args.args)
        posonly_list = deepcopy(node.args.posonlyargs)
        kwonly_list = deepcopy(node.args.kwonlyargs)
        default_args_list = []
        default_posonly_list = []
        default_kwonly_list = []
        
        if len(node.args.defaults) > 0:
            posdefaults = deepcopy(node.args.defaults)
            while len(posdefaults) > 0:
                # order is important here because the defaults field treats posonly and args together
                if len(args_list) > 0:
                    current_arg = args_list.pop()
                    current_arg.arg = defaults_prefix + current_arg.arg
                    default_args_list.insert(0, deepcopy(current_arg))
                    posdefaults.pop()
                elif len(posonly_list) > 0:
                    current_arg = posonly_list.pop()
                    current_arg.arg = defaults_prefix + current_arg.arg
                    default_posonly_list.insert(0, deepcopy(current_arg))
                    posdefaults.pop()
                else:
                    raise RuntimeError(f'More defaults than arguments for {tosrc(node)}')
        # add the remaining posonly/args, if any
        while len(args_list) > 0:
            current_arg = args_list.pop()
            default_args_list.insert(0, deepcopy(current_arg))
        while len(posonly_list) > 0:
            current_arg = posonly_list.pop()
            default_posonly_list.insert(0, deepcopy(current_arg))
        
        # mark keyword only parameters which have default values
        # similar to above, but with keyword only parameters
        if len(node.args.kw_defaults) > 0:
            kwdefaults = deepcopy(node.args.kw_defaults)
            while len(kwdefaults) > 0:
                if len(kwonly_list) > 0:
                    def_value = kwdefaults.pop()
                    current_arg = kwonly_list.pop()
                    if def_value is not None:    
                        current_arg.arg = defaults_prefix + current_arg.arg
                    default_kwonly_list.insert(0, deepcopy(current_arg))
        if len(kwonly_list) > 0:
            raise RuntimeError(f'Still have kwonly arguments, when I should not')
        # add the remaining kw only nodes, if any
        # while len(kwonly_list) > 0:
        #     current_arg = kwonly_list.pop()
        #     default_kwonly_list.insert(0, deepcopy(current_arg))

        # prefix with the corresponding parameter type
        param_lists = [default_posonly_list, default_args_list, [node.args.vararg],
                       default_kwonly_list, [node.args.kwarg]]
        param_prefix = ['__po_', '', '__va_', '__ko_', '__kw_']  # order is important here! 
        func_spec = FuncSpec()
        for i in range(0, len(param_lists)):
            parameters = param_lists[i]
            prefix = param_prefix[i]
            if len(parameters) == 0:
                continue
            if len(parameters) == 1 and parameters[0] is None:
                continue  # no vararg or kwarg
            for param in parameters:
                try:
                    if param.arg in [SMALL_SELF, SMALL_CLS]:  # and param.annotation is None:
                        param_basetype = self.self_type
                    else:
                        param_basetype = self.parse_node_type(param.annotation)
                except NameError:
                    ss = f'{inspect.currentframe().f_lineno}: This type is unsupported: {tosrc(param.annotation)}'
                    raise TypeError(ss)
                new_basetype = param_basetype.filter_pytypes(builtin_types)
                if len(new_basetype) == 0:
                    raise TypeError(f'This basetype ({tosrc(param.annotation)}) '
                                    f'is fully unsupported: {param_basetype}')
                param_basetype = new_basetype
                spec_param_name = f'{prefix}{param.arg}'
                func_spec.in_state.assignment[spec_param_name] = deepcopy(param_basetype)
        return_basetype = self.parse_node_type(node.returns)
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
                str_slice = tosrc(base.slice)
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
                    mylogger.warning(f"Function {node.name}.{body_node.name}: {str(te)}")
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
    all_roots = 0
    for node in stub_ast.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        try:
            all_roots += 1
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
    #
    counter = CountClassFuncs()
    counter.visit(tree)
    print(f'All {stub_file} funcs: {counter.get_func_count()}')
    #
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
    return replaced_dict


if __name__ == "__main__":
    spec_dict = generate_specs('sheds/builtins.pyi')
    # spec_dict = generate_specs('sheds/bugs.pyi')
    # number of translated specifications 
    nr_spec = 0
    for funcname, funcspec in spec_dict.items():
        nr_spec += len(funcspec)
    print(f'Translated: {nr_spec} specifications.')
    #
    # for testing purposes
    test_dict = generate_specs('sheds/test.pyi')
    for k, v in test_dict.items():
        spec_dict[k] = deepcopy(v)
    #

    # custom specifications for type inference
    spec_dict['simpleassign'] = {
        FuncSpec.from_str(r'((x:top /\ y:T?0) -> (x:T?0 /\ return:NoneType))'),
    }
    spec_dict['tupleassign'] = {
        FuncSpec.from_str(
            r'((__va_args:Iterable < top > /\ y:Iterable < T?0 > + str) -> (__va_args:Iterable < T?0 + str > /\ return:NoneType))',
        ),
    }
    spec_dict['seqassign'] = {
        FuncSpec.from_str(r'((x:top /\ y:Iterable < T?0 >) -> (x:T?0 /\ return:NoneType))'),
        FuncSpec.from_str(r'((x:top /\ y:str) -> (x:str /\ return:NoneType))')
    }
    spec_dict['simple_subscript'] = {
        FuncSpec.from_str(r'((a:Iterable < T?0 > /\ b:int) -> (return:T?0))'),
        FuncSpec.from_str(r'((a:dict< T?0, T?1 > /\ b:T?0) -> (return:T?1))')
    }
    spec_dict['subscriptassign'] = {
        FuncSpec.from_str(r'((x:list < T?0 > /\ y:T?1) -> (x:list < T?0 + T?1 > /\ return:NoneType))'),
        FuncSpec.from_str(r'((x:set < T?0 > /\ y:T?1) -> (x:set < T?0 + T?1 > /\ return:NoneType))'),
        FuncSpec.from_str(r'((x:frozenset < T?0 > /\ y:T?1) -> (x:frozenset < T?0 + T?1 > /\ return:NoneType))'),
        FuncSpec.from_str(r'((x:tuple < T?0 > /\ y:T?1) -> (x:tuple < T?0 + T?1 > /\ return:NoneType))'),
        FuncSpec.from_str(r'((x:dict < T?0, T?1 > /\ y:T?2) -> (x:dict < T?0, T?1 + T?2 > /\ return:NoneType))')
    }
    spec_dict['append'] = {\
        # FuncSpec.from_str(r'((self:list < T?0 > /\ __object:T?0) -> (return:NoneType))'),
        FuncSpec.from_str(r'((self:list < T?0 > /\ __object:T?1) -> (self:list < T?0 + T?1 > /\ return:NoneType))'),
        FuncSpec.from_str(r'((self:bytearray /\ __item:SupportsIndex) -> (return:NoneType))'),
        FuncSpec.from_str(r'((self:list < bot > /\ __object:T?0) -> (self:list < T?0 > /\ return:NoneType))'),
    }
    spec_dict['assign_1_prim'] = {
        FuncSpec.from_str(r'((c:str + tuple < T?0 + T?1 >) -> (return:tuple < T?0 + T?1 + str >))')
    }
    spec_dict['for_parse'] = {
        FuncSpec.from_str(r'((target:top /\ iter:Iterable < T?0 >) -> (target:T?0))'),
        FuncSpec.from_str(r'((target:top /\ iter:str) -> (target:str))'),
        FuncSpec.from_str(r'((target:top /\ iter:bytearray) -> (target:int))'),
        FuncSpec.from_str(r'((target:top /\ iter:bytes) -> (target:int))'),
        FuncSpec.from_str(r'((target:top /\ iter:range) -> (target:int))'),
        FuncSpec.from_str(r'((target:top /\ iter:memoryview) -> (target:int))'),
    }
    spec_dict['range'] = {
        FuncSpec.from_str(r'((stop:int) -> (return:range))'),
        FuncSpec.from_str(r'((start:int /\ stop:int) -> (return:range))'),
        FuncSpec.from_str(r'((start:int /\ stop:int /\ step:int) -> (return:range))')
    }
    #
    dump_specs('united_specs.py', spec_dict)
