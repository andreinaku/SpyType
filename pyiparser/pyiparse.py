import ast
import builtins
import inspect
from copy import deepcopy
import astor
import logging
from type_equivalences import *
import math
import json
from Translator import Translator, AbsState, hdict, hset


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


class CountClassFuncs(ast.NodeVisitor):
    def __init__(self):
        self.func_count = 0
        self.func_list = []

    def visit_FunctionDef(self, node):
        self.func_count += 1
        self.func_list.append(astor.to_source(node).strip())

    def get_func_count(self):
        return self.func_count


class ClassDefParser(ast.NodeVisitor):

    def __init__(self):
        self.spec_dict = dict()
        self.specs = dict()
        self.total_funcdefs = 0
        self.parsed_funcdefs = 0
        self.class_stats = dict()
        self.current_class = None

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
                ss = f'ignored type (for now) <<{return_id}>> for {node.id}'
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
                contained_str = cls.parse_node_type(contained)
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

    @staticmethod
    def is_ignored(_type: str):
        for ign in ignore_list:
            if _type.startswith(ign):
                return True
        return False

    def parse_FunctionDef(self, node: ast.FunctionDef, selftype: str) -> tuple[str, str, str]:

        def get_parameter_specs(param: ast.arg, param_nr: int, prefix: str = None) -> tuple[str, str]:
            tname = f'T?{param_nr}:'
            pname = f'{param.arg}:{tname[:-1]}'
            param_nr += 1
            if param.arg in [SMALL_SELF, SMALL_CLS] and param.annotation is None:
                tname += f'{selftype}'
            else:
                parsed_type = self.parse_node_type(param.annotation)
                if parsed_type == '':
                    ss = f'ignored type (for now) <<{param.annotation}>> for {astor.to_source(param.annotation).strip()}'
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
            rtype = self.parse_node_type(node.returns).replace(BIG_SELF, selftype)
            if rtype == 'Any' or rtype == '' or self.is_ignored(rtype) or rtype == 'TopType':
                ss = f'ignored return type (for now) <<{rtype}>> for {node.name}'
                mylogger.warning(ss)
                raise TypeError(ss)
            if rtype == BIG_SELF:
                rtype = selftype
            tname = 'T?r:'
            pname = f'return:{tname[:-1]}'
            ta += pname + r' /\ '
            tname += rtype
            tc += tname + r' /\ '
            return ta, tc

        _ta, _tc = get_abs_state()
        self.parsed_funcdefs += 1
        self.class_stats[self.current_class]['translated'] += 1
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
            special_sequences = ['str', 'bytes', 'bytearray']
            self_type = node.name
            _spec_list = []
            past_slice = None
            for base in node.bases:
                if isinstance(base, ast.Subscript) and self_type not in special_sequences:
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
            for func in node.body:
                if not isinstance(func, ast.FunctionDef):
                    continue
                try:
                    spec_tuple = self.parse_FunctionDef(func, self_type)
                except TypeError as te:
                    self.class_stats[self.current_class]['not_translated_specs'].append((astor.to_source(func).strip(),
                                                                                         str(te)))
                    mylogger.warning(f'Could not translate specs for {node.name}::{func.name}\n')
                    continue
                _spec_list.append(spec_tuple)
            return _spec_list

        ccf = CountClassFuncs()
        ccf.visit(node)
        self.current_class = node.name
        self.class_stats[self.current_class] = dict()
        self.class_stats[self.current_class]['total'] = ccf.get_func_count()
        self.class_stats[self.current_class]['translated'] = 0
        self.class_stats[self.current_class]['not_translated_specs'] = []
        self.total_funcdefs += self.class_stats[self.current_class]['total']
        if self.current_class in IGNORED_CLASSES:
            mylogger.warning(f'Class {node.name} ignored for now\n')
            return
        try:
            spec_list = get_spec_list()
        except TypeError as te:
            mylogger.warning(f'Could not translate specs for class {node.name}\n')
            return
        add_to_spec_dict(spec_list)

    def get_parsed_funcs(self):
        return self.parsed_funcdefs, self.total_funcdefs

    def get_class_stats(self):
        return self.class_stats

    def increase_total_funcdefs(self):
        self.total_funcdefs += 1

    def increase_parsed_funcdefs(self):
        self.parsed_funcdefs += 1

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

    # def print_specs(self, indent=2):
    #     self.get_specs()
    #     spex = self.specs
    #     spaces = ' ' * indent
    #     with open(OUTPUT_FILE, 'a') as f:
    #         f.write('funcspecs = {\n')
    #         for classname, funcdict in spex.items():
    #             f.write(f'\t\'{classname}\': {{\n')
    #             for funcname, spec_set in funcdict.items():
    #                 f.write(f'\t\t\'{funcname}\': {{\n')
    #                 for single_spec in spec_set:
    #                     f.write(f'\t\t\tr\'{single_spec}\',\n')
    #                 f.write('\t\t},\n')
    #             f.write('\t},\n')
    #         f.write('\n}\n')

    def get_specs_dict(self):
        return self.specs


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


def write_type_equivalences():
    equiv = get_equivalences_dict()
    with open(OUTPUT_FILE, 'a') as f:
        f.write('type_equiv = {\n')
        for node, typelist in equiv.items():
            sum_string = '+'.join(typelist)
            f.write(f'\t{node.__name__}: \'{sum_string}\',\n')
        f.write('}\n\n\n')


def generate_specs(stub_file):

    def get_united_specs(_spex):
        united_dict = hdict()
        for _classname, funcdict in _spex.items():
            for funcname, spec_set in funcdict.items():
                for single_spec in spec_set:
                    new_form = transform_to_new_format(Translator.translate_as(single_spec))
                    if funcname in united_dict:
                        united_dict[funcname] |= new_form
                    else:
                        united_dict[funcname] = new_form
        return united_dict

    def print_united_specs(_spex):
        united = get_united_specs(_spex)
        # with open(OUTPUT_FILE, 'a') as f:
        with open('united_specs.py', 'w') as f:
            f.write('unitedspecs = {\n')
            for funcname, spec_set in united.items():
                f.write(f'\t\'{funcname}\': {{\n')
                for dict_tuple in spec_set:
                    writestr = '\t\t\tr\'(('
                    param_dict = dict_tuple[0]
                    ret_dict = dict_tuple[1]
                    no_params = (len(param_dict) == 0)
                    for k, v in param_dict.items():
                        writestr += rf'{k}:{v} /\ '
                    if no_params:
                        writestr += ') -> '
                    else:
                        writestr = writestr[:-4] + r') -> '
                    writestr += f'({RETURN_VARNAME}:{ret_dict[RETURN_VARNAME]}))\',\n'
                    f.write(writestr)
                f.write('\t},\n')
            f.write('\n}\n')

    def print_new_format(_spex):
        with open(OUTPUT_FILE, 'a') as f:
            f.write('newspecs = {\n')
            for _classname, funcdict in _spex.items():
                f.write(f'\t\'{_classname}\': {{\n')
                for funcname, spec_set in funcdict.items():
                    f.write(f'\t\t\'{funcname}\': {{\n')
                    for single_spec in spec_set:
                        new_form = transform_to_new_format(Translator.translate_as(single_spec))
                        for dict_tuple in new_form:
                            writestr = '\t\t\tr\'(('
                            param_dict = dict_tuple[0]
                            ret_dict = dict_tuple[1]
                            no_params = (len(param_dict) == 0)
                            for k, v in param_dict.items():  # vezi ca e set
                                writestr += rf'{k}: {v} /\ '
                            # writestr = writestr[:-4] + r') \/ ('
                            if no_params:
                                writestr += ') -> '
                            else:
                                writestr = writestr[:-4] + r') -> '
                            writestr += f'({RETURN_VARNAME}: {ret_dict[RETURN_VARNAME]}))\',\n'
                            f.write(writestr)
                    f.write('\t\t},\n')
                f.write('\t},\n')
            f.write('\n}\n')

    def print_old_format(_spex):
        with open(OUTPUT_FILE, 'a') as f:
            f.write('funcspecs = {\n')
            for _classname, funcdict in _spex.items():
                f.write(f'\t\'{_classname}\': {{\n')
                for funcname, spec_set in funcdict.items():
                    f.write(f'\t\t\'{funcname}\': {{\n')
                    for single_spec in spec_set:
                        f.write(f'\t\t\tr\'{single_spec}\',\n')
                    f.write('\t\t},\n')
                f.write('\t},\n')
            f.write('\n}\n')

    def print_specs(_spex):
        # spaces = ' ' * indent
        print_old_format(_spex)
        print_new_format(_spex)
        print_united_specs(_spex)

    def transform_to_new_format(abstate: AbsState):
        newset = hset()
        _va = abstate.va
        _tc = abstate.tc
        for ctx in _tc:
            paramdict = hdict()
            retdict = hdict()
            for vt, te_set in ctx.items():
                if len(te_set) > 1:
                    raise RuntimeError('More than one type expression for the same variable')
                te = list(te_set)[0]
                for varname, ta_vt in _va.items():
                    if ta_vt == vt and varname != RETURN_VARNAME:
                        paramdict[varname] = te
                    elif ta_vt == vt and varname == RETURN_VARNAME:
                        retdict[varname] = te
            newset.add((paramdict, retdict))
        return newset

    open(OUTPUT_FILE, 'w').write('import ast\nfrom type_equivalences import *\n\n\n')
    write_op_equivalences()
    write_type_equivalences()
    # class specs
    pp = ClassDefParser()
    tree = ast.parse(open(stub_file, 'r').read())
    pp.visit(tree)
    pp.get_specs()
    spex = pp.specs
    # pp.print_specs()
    # function specs
    spex[BUILTIN_CATEGORY] = dict()
    builtin_spex = spex[BUILTIN_CATEGORY]
    cstats = pp.get_class_stats()
    cstats['builtins'] = dict()
    cstats['builtins']['total'] = 0
    cstats['builtins']['translated'] = 0
    cstats['builtins']['not_translated_specs'] = []
    # aux1, aux2 = pp.get_parsed_funcs()
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        # aux2 += 1
        cstats['builtins']['total'] += 1
        try:
            spec = pp.parse_FunctionDef(node, '')
        except TypeError as te:
            mylogger.warning(f'Could not translate specs for {BUILTIN_CATEGORY}::{node.name}\n')
            cstats['builtins']['not_translated_specs'].append((astor.to_source(node).strip(),
                                                                str(te)))
            continue
        cstats['builtins']['translated'] += 1
        abs_state = spec[1] + ' ^ ' + spec[2]

        if spec[0] not in builtin_spex:
            builtin_spex[spec[0]] = {abs_state}
        else:
            builtin_spex[spec[0]].add(abs_state)
    print_specs(spex)
    translated = 0
    total = 0
    for classname, statdict in cstats.items():
        try:
            translated += statdict['translated']
        except KeyError:
            pass
        total += statdict['total']
    ss = json.dumps(cstats, indent=4)
    mylogger.info(f'Class stats: {ss}')
    with open('stats.json', 'w') as f:
        json.dump(cstats, f, indent=4)
    mylogger.info(f'Translated function specs: {translated}/{total}'
                  f' ~ {math.floor(translated/total * 100)}%\n'
                  f'Not translated function specs: {total - translated}\n')


if __name__ == "__main__":
    generate_specs('builtins.pyi')
