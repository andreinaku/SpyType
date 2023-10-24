import ast
import builtins
import inspect


NAME_LITERAL = 'Literal'
NAME_SELF = 'Self'
ignore_list = ['slice', 'GenericAlias', 'Callable']
DEFAULT_TYPEVAR = '_T'
SPEC_DEFAULT_TYPEVAR = 'T?0'
param_prefix = ['__po_', '', '__va_', '__ko_', '__kw_']
PREFIX_POSONLY, PREFIX_ARGS, PREFIX_VARARG, PREFIX_KWONLY, PREFIX_KWARG = range(5)
TYPE_REPLACE = {'_T': 'T?0', '_PositiveInteger': 'int', '_NegativeInteger': 'int'}


class IgnoredTypeError(Exception):
    pass


class ClassDefParser(ast.NodeVisitor):

    def __init__(self):
        self.spec_dict = dict()

    @classmethod
    def parse_node_type(cls, node: ast.expr) -> str:
        if isinstance(node, ast.Name):
            open('types.txt', 'a').write(node.id + '\n')
            if node.id in TYPE_REPLACE:
                return TYPE_REPLACE[node.id]
            else:
                return node.id
        elif isinstance(node, ast.Constant):
            open('types.txt', 'a').write(type(node.value).__name__ + '\n')
            return type(node.value).__name__
        elif isinstance(node, ast.Subscript):
            contained = node.slice
            if not isinstance(node.value, ast.Name):
                raise TypeError(f'{type(node.value)} is not yet supported here')
            container = node.value.id
            open('types.txt', 'a').write(container + '\n')
            contained_str = ''
            if isinstance(contained, ast.Tuple):
                for aux in contained.elts:
                    contained_str += cls.parse_node_type(aux) + '+'
                contained_str = contained_str[:-1]
            else:
                contained_str = cls.parse_node_type(contained)
            if container == NAME_LITERAL:
                return contained_str
            else:
                return container + '<' + contained_str + '>'
        elif isinstance(node, ast.BinOp):
            if not isinstance(node.op, ast.BitOr):
                raise TypeError(f'{node.op} operation not supported for types')
            return cls.parse_node_type(node.left) + '+' + cls.parse_node_type(node.right)
        elif isinstance(node, ast.List):
            container = 'list'
            contained_str = ''
            for aux in node.elts:
                contained_str += cls.parse_node_type(aux) + '+'
            contained_str = contained_str[-1]
            return container + '<' + contained_str + '>'
        else:
            raise TypeError(f'{type(node)} is not supported')

    @staticmethod
    def is_ignored(_type: str):
        for ign in ignore_list:
            if _type.startswith(ign):
                return True
        return False

    @classmethod
    def parse_FunctionDef(cls, node: ast.FunctionDef, selftype: str) -> tuple[str, str, str]:

        def get_parameter_specs(param: ast.arg, param_nr: int, prefix: str=None) -> tuple[str, str]:
            # todo: tratat def __rpow__(self, __value: int, __mod: int | None = None) -> Any: ...
            # todo: tratat def __class_getitem__(cls, __item: Any) -> GenericAlias: ...
            tname = f'T?{param_nr}:'
            pname = f'{param.arg}:{tname[:-1]}'
            param_nr += 1
            if param.arg in ['self', 'cls'] and param.annotation is None:
                tname += f'{selftype}'
            else:
                # todo: aici putem avea si ast.Constant, de ex __mod: None
                # todo: aici putem avea si ast.BinOp, de ex __mod: int | None
                parsed_type = cls.parse_node_type(param.annotation)
                if cls.is_ignored(parsed_type):
                    raise IgnoredTypeError('ignored type (for now)')
                tname += cls.parse_node_type(param.annotation)
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
            if rtype == 'Any' or cls.is_ignored(rtype):
                raise IgnoredTypeError('return type ignored (for now)')
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
                        self_type += '<' + self.parse_node_type(base.slice) + '>'
                        past_slice = base.slice
                    else:
                        if past_slice.id != base.slice.id:
                            raise RuntimeError('slice mismatch')
            for func in node.body:
                if not isinstance(func, ast.FunctionDef):
                    continue
                try:
                    spec_tuple = self.parse_FunctionDef(func, self_type)
                except IgnoredTypeError:
                    continue
                _spec_list.append(spec_tuple)
            return _spec_list

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
        return new_dict

    def print_specs(self, indent=2):
        spex = self.get_specs()
        spaces = ' ' * indent
        with open('specs.txt', 'w') as f:
            for classname, funcdict in spex.items():
                f.write(f'{classname}\n')
                for funcname, spec_set in funcdict.items():
                    f.write(f'\t{funcname}\n')
                    for single_spec in spec_set:
                        f.write(f'\t\t{single_spec}\n')


if __name__ == "__main__":
    pp = ClassDefParser()
    tree = ast.parse(open('test.pyi', 'r').read())
    pp.visit(tree)
    # print(pp.get_specs())
    pp.print_specs()
    # pprint.pprint(pp.get_specs())
