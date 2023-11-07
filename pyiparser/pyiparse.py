import ast
import builtins
import inspect
from copy import deepcopy
import astor
import logging

BUILTIN_CATEGORY = 'builtins'
NAME_LITERAL = 'Literal'
RET_SELF = 'Self'
ignore_list = ['slice', 'GenericAlias', 'Callable']
DEFAULT_TYPEVAR = '_T'
SPEC_DEFAULT_TYPEVAR = 'T?0'
param_prefix = ['__po_', '', '__va_', '__ko_', '__kw_']
PREFIX_POSONLY, PREFIX_ARGS, PREFIX_VARARG, PREFIX_KWONLY, PREFIX_KWARG = range(5)
TYPE_REPLACE = {'_T': 'T?0', '_PositiveInteger': 'int', '_KT': 'T?K', '_VT': 'T?V',
                '_NegativeInteger': 'int', '_S': 'T?s',
                'object': 'TopType', 'ReadOnlyBuffer': 'bytes',
                'WriteableBuffer': 'bytearray+memoryview', 'ReadableBuffer': 'bytes+bytearray+memoryview'}
OUTPUT_FILE = 'specs_shed.py'
MAPPING_BASES = ['Mapping', 'MutableMapping', 'dict']


class IgnoredTypeError(Exception):
    pass


def get_logger(
        LOG_FORMAT='%(levelname)-4s %(message)s',
        LOG_NAME='',
        LOG_FILE_INFO='parser.log',
        LOG_FILE_ERROR='parser.err'):
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


class ClassDefParser(ast.NodeVisitor):

    def __init__(self):
        self.spec_dict = dict()
        self.specs = dict()

    @classmethod
    def parse_node_type(cls, node: ast.expr) -> str:

        def get_types_from_list(_elts: list):
            _type_list = []
            for _type in _elts:
                str_type = cls.parse_node_type(_type)
                if cls.is_ignored(str_type):
                    continue
                if str_type == '':
                    continue
                _type_list.append(str_type)
            return _type_list

        if isinstance(node, ast.Name):
            open('types.txt', 'a').write(node.id + '\n')
            return_id = TYPE_REPLACE[node.id] if node.id in TYPE_REPLACE else node.id
            if cls.is_ignored(return_id):
                ss = f'ignored type (for now) for {node.id}'
                mylogger.warning(ss)
                raise TypeError(ss)
                # return ''
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
            container = node.value.id
            kvtuple = False
            if container in MAPPING_BASES:
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
                    contained_str = ', '.join(type_set)
            else:
                contained_str = cls.parse_node_type(contained)
            if container == NAME_LITERAL:
                return contained_str
            else:
                return container + '<' + contained_str + '>'
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
            return container + '<' + contained_str + '>'
        elif isinstance(node, ast.Tuple):
            container = 'tuple'
            type_set = set(get_types_from_list(node.elts))
            contained_str = '+'.join(type_set)
            return container + '<' + contained_str + '>'
        else:
            ss = f'{type(node)} is not yet supported here'
            mylogger.warning(ss)
            raise TypeError(ss)

    @staticmethod
    def is_ignored(_type: str):
        for ign in ignore_list:
            if _type.startswith(ign):
                return True
        return False

    @classmethod
    def parse_FunctionDef(cls, node: ast.FunctionDef, selftype: str) -> tuple[str, str, str]:

        def get_parameter_specs(param: ast.arg, param_nr: int, prefix: str = None) -> tuple[str, str]:
            tname = f'T?{param_nr}:'
            pname = f'{param.arg}:{tname[:-1]}'
            param_nr += 1
            if param.arg in ['self', 'cls'] and param.annotation is None:
                tname += f'{selftype}'
            else:
                parsed_type = cls.parse_node_type(param.annotation)
                if parsed_type == '':
                    ss = f'ignored type (for now) for {astor.to_source(param.annotation).strip()}'
                    mylogger.warning(ss)
                    raise TypeError(ss)
                # tname += cls.parse_node_type(param.annotation)
                tname += parsed_type
            return pname, tname

        def get_abs_state():
            param_lists = [node.args.posonlyargs, node.args.args, [node.args.vararg],
                           node.args.kwonlyargs, [node.args.kwarg]]
            param_prefix = ['__po_', '', '__va_', '__ko_', '__kw_']
            # parameters = node.args.args
            param_nr = 1
            # ta = '('
            ta = ''
            tc = '('
            for i in range(0, len(param_lists)):
                # for parameters in param_lists:
                parameters = param_lists[i]
                prefix = param_prefix[i]
                if len(parameters) == 0:
                    continue
                if len(parameters) == 1 and parameters[0] is None:
                    continue  # no vararg or kwarg
                for param in parameters:
                    pname, tname = get_parameter_specs(param, param_nr)
                    param_nr += 1
                    ta += prefix + pname + r' /\ '
                    tc += tname + r' /\ '
            # rtype = get_returntype()
            rtype = cls.parse_node_type(node.returns)
            if rtype == 'Any' or rtype == '' or cls.is_ignored(rtype):
                ss = f'ignored type (for now) for {node.name}'
                mylogger.warning(ss)
                raise TypeError(ss)
            if rtype == RET_SELF:
                rtype = selftype
            tname = 'T?r:'
            pname = f'return:{tname[:-1]}'
            ta += pname + r' /\ '
            tname += rtype
            tc += tname + r' /\ '
            return ta, tc

        _ta, _tc = get_abs_state()
        return node.name, _ta[:-4], _tc[:-4] + ')'
        # return funcname + ')'

    def visit_ClassDef(self, node: ast.ClassDef):
        def add_to_spec_dict(_spec_list: list[tuple[str, str, str]]):
            self.spec_dict[node.name] = dict()
            class_dict = self.spec_dict[node.name]
            for k, ta, tc in _spec_list:
                if k not in class_dict:
                    class_dict[k] = dict()
                if ta not in class_dict[k]:
                    class_dict[k][ta] = tc
                else:
                    class_dict[k][ta] += rf' \/ {tc}'

        def get_spec_list():
            self_type = node.name
            _spec_list = []
            past_slice = None
            for base in node.bases:
                if isinstance(base, ast.Subscript):
                    if not past_slice:
                        # aux = self.parse_node_type(base)
                        kvtuple = False
                        if base.value.id in MAPPING_BASES:
                            kvtuple = True
                        parsed_type = self.parse_node_type(base)
                        if parsed_type == '':
                            ss = f'Type for node {base} not supported'
                            mylogger.error(ss)
                            raise TypeError(ss)
                        parsed_slice = '<' + parsed_type.split('<', maxsplit=1)[1]
                        # self_type += '<' + self.parse_node_type(base.slice, True, kvtuple) + '>'
                        self_type += parsed_slice
                        past_slice = base.slice
                    else:
                        # if past_slice.id != base.slice.id:
                        if astor.to_source(past_slice) != astor.to_source(base.slice):
                            ss = f'Inconsistent slice for {node.name}'
                            mylogger.error(ss)
                            raise RuntimeError(ss)
            for func in node.body:
                if not isinstance(func, ast.FunctionDef):
                    continue
                try:
                    spec_tuple = self.parse_FunctionDef(func, self_type)
                except TypeError:
                    mylogger.warning(f'Could not translate specs for {node.name}::{func.name}\n')
                    continue
                _spec_list.append(spec_tuple)
            return _spec_list

        if node.name not in ['staticmethod', 'classmethod', 'type', 'function']:
            spec_list = get_spec_list()
            add_to_spec_dict(spec_list)

    def get_specs(self):
        new_dict = dict()
        for classname, funcdict in self.spec_dict.items():
            new_dict[classname] = dict()
            working_class = new_dict[classname]
            for funcname, spec_d in funcdict.items():
                for ta, tc in spec_d.items():
                    abs_state = ta + ' ^ ' + tc
                    if funcname not in working_class:
                        working_class[funcname] = {abs_state}
                    else:
                        working_class[funcname].add(abs_state)
        self.specs = deepcopy(new_dict)
        # return new_dict

    def print_specs(self, indent=2):
        self.get_specs()
        spex = self.specs
        spaces = ' ' * indent
        with open(OUTPUT_FILE, 'a') as f:
            f.write('funcspecs = {\n')
            for classname, funcdict in spex.items():
                f.write(f'\t\'{classname}\': {{\n')
                for funcname, spec_set in funcdict.items():
                    f.write(f'\t\t\'{funcname}\': {{\n')
                    for single_spec in spec_set:
                        f.write(f'\t\t\tr\'{single_spec}\',\n')
                    f.write('\t\t},\n')
                f.write('\t},\n')
            f.write('\n}\n')

    def get_specs_dict(self):
        return self.specs


def op_equivalences():
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
        f.write('equiv_dict = {\n')
        for node, funcdict in equiv_dict.items():
            f.write(f'\t{node}: {{\n')
            for nodeop, funcname in funcdict.items():
                f.write(f'\t\t{nodeop}: \'{funcname}\',\n')
            f.write('\t},\n')
        f.write('}\n')


def generate_specs():
    def print_specs(spex, indent=2):
        # self.get_specs()
        # spex = self.specs
        spaces = ' ' * indent
        with open(OUTPUT_FILE, 'a') as f:
            f.write('funcspecs = {\n')
            for classname, funcdict in spex.items():
                f.write(f'\t\'{classname}\': {{\n')
                for funcname, spec_set in funcdict.items():
                    f.write(f'\t\t\'{funcname}\': {{\n')
                    for single_spec in spec_set:
                        f.write(f'\t\t\tr\'{single_spec}\',\n')
                    f.write('\t\t},\n')
                f.write('\t},\n')
            f.write('\n}\n')

    open(OUTPUT_FILE, 'w').write('import ast\n\n\n')
    op_equivalences()
    # class specs
    pp = ClassDefParser()
    tree = ast.parse(open('test.pyi', 'r').read())
    # tree = ast.parse(open('builtins.pyi', 'r').read())
    pp.visit(tree)
    pp.get_specs()
    spex = pp.specs
    # pp.print_specs()
    # function specs
    spex[BUILTIN_CATEGORY] = dict()
    builtin_spex = spex[BUILTIN_CATEGORY]
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        try:
            spec = pp.parse_FunctionDef(node, '')
        except TypeError:
            mylogger.warning(f'Could not translate specs for {BUILTIN_CATEGORY}::{node.name}\n')
            continue
        abs_state = spec[1] + ' ^ ' + spec[2]
        if spec[0] not in builtin_spex:
            builtin_spex[spec[0]] = {spec[1]}
        else:
            builtin_spex[spec[0]].add(spec[1])
    pass


if __name__ == "__main__":
    generate_specs()
