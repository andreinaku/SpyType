from ast import Assign
from typing import Any
from statev2.basetype import *
from united_specs import op_equiv, unitedspecs
from statev2.Translator import Translator


POSONLY_MARKER = '__po_'
VARARG_MARKER = '__va_'
KEYWORDONLY_MARKER = '__ko_'
KWARG_MARKER = '__kw_'
MARKERS = [POSONLY_MARKER, VARARG_MARKER, KEYWORDONLY_MARKER, KWARG_MARKER]
RETURN_VARNAME = 'return'


class ArgumentMismatchError(Exception):
    pass


# class SpecNotFoundError(Exception):
#     pass

class FunctionInstance:
    def __init__(self, call_node: ast.Call, current_state: State, spec: FuncSpec):
        self.arglink = dict()
        self.current_state = deepcopy(current_state)
        self.spec = deepcopy(spec)
        self.pos_call_list = []
        self.keyword_call_dict = {}
        self.call_node = call_node
        for node in self.call_node.args:
            self.pos_call_list.append(astor.to_source(node).strip())
        for node in self.call_node.keywords:
            self.keyword_call_dict[node.arg] = node.value
        self.arg_list = deepcopy(list(self.spec.in_state.assignment))
        # self.arg_list.remove(RETURN_VARNAME)
        self._param_link()

    def _param_link(self):
        if (len(self.pos_call_list) > 0 or len(self.keyword_call_dict) > 0) and len(self.arg_list) == 0:
            raise ArgumentMismatchError('Too many arguments provided')
        if (len(self.pos_call_list) == 0 and len(self.keyword_call_dict) == 0) and len(self.arg_list) > 0:
            raise ArgumentMismatchError('Too few arguments provided')
        if len(self.arg_list) == 0 and len(self.pos_call_list) == 0 and len(self.keyword_call_dict) == 0:
            return
        param: str = self.arg_list.pop(0)
        if param.startswith(POSONLY_MARKER):
            if len(self.pos_call_list) == 0:
                raise ArgumentMismatchError('Too few positional arguments provided')
            call_entry = self.pos_call_list.pop(0)
            self.arglink[param] = call_entry
            self._param_link()
            # f(va_index+1)
        elif param.startswith(VARARG_MARKER):
            while len(self.pos_call_list) > 0:
                call_entry = self.pos_call_list.pop(0)
                if param not in self.arglink:
                    self.arglink[param] = (call_entry,)
                else:
                    self.arglink[param] = self.arglink[param] + (call_entry,)
            if param not in self.arglink:
                raise ArgumentMismatchError(f'Variable argument {param} is not populated')
            self._param_link()
        elif va_var.startswith(KEYWORDONLY_MARKER):
            if len(self.keyword_call_dict) == 0:
                raise ArgumentMismatchError('Too few keyword arguments provided')
            varname = va_var[len(KEYWORDONLY_MARKER):]
            if varname not in self.keyword_call_dict:
                raise ArgumentMismatchError(f'Keyword argument {varname} is not provided')
            self.arglink[va_var] = astor.to_source(self.keyword_call_dict.pop(varname)).strip()
            self._param_link()
        elif va_var.startswith(KWARG_MARKER):
            if len(self.keyword_call_dict) == 0:
                raise ArgumentMismatchError(f'No more keyword arguments for {va_var}')
            keyword_list = list(self.keyword_call_dict)
            while len(self.keyword_call_dict) > 0:
                ko_key = keyword_list.pop(0)
                call_entry = astor.to_source(self.keyword_call_dict.pop(ko_key)).strip()
                if va_var not in self.arglink:
                    self.arglink[va_var] = {ko_key: call_entry}
                else:
                    self.arglink[va_var].update({ko_key: call_entry})
            self._param_link()
        else:
            if len(self.pos_call_list) > 0:
                call_entry = self.pos_call_list.pop(0)
            elif len(self.keyword_call_dict) > 0:
                keyword_list = list(self.keyword_call_dict)
                ko_key = keyword_list.pop(0)
                call_entry = astor.to_source(self.keyword_call_dict.pop(ko_key)).strip()
            else:
                raise ArgumentMismatchError(f'No more arguments for {va_var}')
            self.arglink[va_var] = call_entry
            self._param_link()

    def get_param_link(self):
        return self.arglink

    def instantiate_function(self):
        new_as = AbsState()
        new_as.va = VarAssign()
        new_as.tc = TypeConstraint()
        var_entries = []
        repl = dict()
        for spec_var, state_var in self.arglink.items():
            if isinstance(state_var, str):
                new_as.va[state_var] = self.spec_state.va[spec_var]
                repl[self.spec_state.va[spec_var]] = self.current_state.va[state_var]
            elif isinstance(state_var, tuple):
                new_te = TypeExpression()
                spec_vartype = self.spec_state.va[spec_var]
                new_pytype = PyType(tuple)
                for sv in state_var:
                    new_as.va[sv] = self.current_state.va[sv]
                    new_pytype.keys.add(self.current_state.va[sv])
                new_te.add(new_pytype)
                var_entries.append((spec_vartype, hset({new_te})))
            elif isinstance(state_var, dict):
                new_te = TypeExpression()
                spec_vartype = self.spec_state.va[spec_var]
                new_pytype = PyType(dict)
                new_pytype.keys.add(PyType(str))
                for k, sv in state_var.items():
                    new_as.va[sv] = self.current_state.va[sv]
                    new_pytype.values.add(self.current_state.va[sv])
                new_te.add(new_pytype)
                var_entries.append((spec_vartype, hset({new_te})))
            else:
                raise RuntimeError(f'Unexpected type of {state_var}: {type(state_var)}')
        new_as.tc = deepcopy(self.spec_state.tc)
        for ctx in new_as.tc:
            for var_entry in var_entries:
                if var_entry[0] not in ctx:
                    raise RuntimeError(f'No variable entry in specs for {var_entry[0]}')
                ctx[var_entry[0]] |= var_entry[1]
        new_as = new_as.vartype_replace_by_dict(repl)
        new_as.va[RETURN_VARNAME] = self.spec_state.va[RETURN_VARNAME]
        return new_as


def state_apply_spec(state: State, spec: State, testmode=False) -> State:
    new_state = State()
    new_state.gen_id = state.gen_id
    new_state.constraints = deepcopy(state.constraints)
    for expr in spec.assignment:
        if testmode is False:
            new_basetype = Basetype({VarType(new_state.generate_id())})
        else:
            new_varname = f'T{expr}`'
            new_basetype = Basetype({VarType(new_varname)})
            if new_basetype == spec.assignment[expr]:
                new_basetype = Basetype({VarType(new_varname + '`')})
        new_state.assignment[expr] = new_basetype
        rel1 = Relation(RelOp.LEQ, new_basetype, deepcopy(state.assignment[expr]))
        rel2 = Relation(RelOp.LEQ, new_basetype, deepcopy(spec.assignment[expr]))
        andconstr = AndConstraints()
        andconstr.add(rel1)
        andconstr.add(rel2)
        new_state.constraints |= deepcopy(andconstr)
    for expr in state.assignment:
        if expr not in new_state.assignment:
            new_state.assignment[expr] = deepcopy(state.assignment[expr])
    return new_state


def set_apply_spec(state_set: StateSet, spec_set: StateSet, testmode=False) -> StateSet:
    new_set = StateSet()
    for state in state_set:
        for spec in spec_set:
            new_state = state_apply_spec(state, spec, testmode)
            new_set.add(new_state)
    return new_set


def spec_to_state(spec: FuncSpec) -> State:
    ret_state = deepcopy(spec.in_state)
    for expr in spec.out_state.assignment:
        ret_state.assignment[expr] = deepcopy(spec.out_state.assignment[expr])
    return ret_state


def find_spec(node: ast.BinOp | ast.Call) -> StateSet:
    if isinstance(node, ast.BinOp):
        spec_name = op_equiv[ast.BinOp][type(node.op)]
        raw_set = unitedspecs[spec_name]
    elif isinstance(node, ast.Call):
        funcname = node.func.id
        raw_set = unitedspecs[funcname]
    else:
        raise TypeError(f'{astor.to_source(node)} is not a BinOp or a Call')
    return raw_set


def get_specset(node: ast.BinOp | ast.Call) -> hset[FuncSpec]:
    if not isinstance(node, ast.BinOp) and not isinstance(node, ast.Call):
        raise TypeError(f'Node {astor.to_source(node)} not supported yet')
    raw_set = find_spec(node)
    spec_set = hset()
    for str_spec in raw_set:
        spec = Translator.translate_func_spec(str_spec)
        # spec_state = spec_to_state(spec)
        # spec = spec.replace_superclasses()
        spec_set.add(deepcopy(spec))
    return spec_set


def substitute_state_arguments(state: State, node: ast.BinOp | ast.Call) -> hset[FuncSpec]:
    if not isinstance(node, ast.BinOp) and not isinstance(node, ast.Call):
        raise TypeError(f'Node {astor.to_source(node)} cannot have arguments (afaik)')
    
    spec_set = get_specset(node)
    return_name = 'return'
    
    if isinstance(node, ast.BinOp):
        op_args = (astor.to_source(node.left).strip(), astor.to_source(node.right).strip())
    else:
        op_args = []  # todo
        for _arg in node.args:
            op_args.append(astor.to_source(_arg).strip())
        op_args = tuple(op_args)
    new_set = hset()
    for spec in spec_set:
        new_spec = FuncSpec()
        i = 0
        for expr in spec.in_state.assignment:
            new_spec.in_state.assignment[op_args[i]] = deepcopy(spec.in_state.assignment[expr])
            i = i + 1
        op_expr = astor.to_source(node).strip()
        new_spec.out_state.assignment[op_expr] = deepcopy(spec.out_state.assignment[return_name])
        new_set.add(deepcopy(new_spec))
    return new_set


def set_apply_specset(state_set: StateSet, node: ast.BinOp | ast.Call, testmode: bool = False) -> StateSet:
    if not isinstance(node, ast.BinOp) and not isinstance(node, ast.Call):
        raise TypeError(f'Node {astor.to_source(node)} cannot have specs to apply (afaik)')
    new_set = StateSet()
    for state in state_set:
        interim_spec_set = substitute_state_arguments(state, node)
        for spec in interim_spec_set:
            new_state = state_apply_spec(state, spec.in_state, testmode)
            for expr, bt in spec.out_state.assignment.items():
                new_state.assignment[expr] = deepcopy(bt)
            new_set.add(deepcopy(new_state))
    return new_set


class TransferFunc(ast.NodeVisitor):
    def __init__(self, _state_set: StateSet, _testmode=False):
        self.state_set = deepcopy(_state_set)
        self.testmode = _testmode

    def visit_Constant(self, node: ast.Constant):
        new_set = StateSet()
        for state in self.state_set:
            new_state = deepcopy(state)
            # new_state.assignment[astor.to_source(node).strip()] = Basetype({PyType(type(node.value))})
            new_state.assignment[str(node.value)] = Basetype({PyType(type(node.value))})
            new_set.add(new_state)
        self.state_set = deepcopy(new_set)

    def visit_BinOp(self, node: ast.BinOp):
        self.visit(node.left)
        self.visit(node.right)
        self.state_set = set_apply_specset(self.state_set, node, self.testmode)

    def visit_Call(self, node: ast.Call):
        for _arg in node.args:
            self.visit(_arg)
        self.state_set = set_apply_specset(self.state_set, node, self.testmode)

    def visit_Tuple(self, node: ast.Tuple):
        for elem in node.elts:
            self.visit(elem)
        node_name = astor.to_source(node).strip()
        new_set = StateSet()
        new_state: State
        state: State
        for state in self.state_set:
            contained_bt = Basetype()
            for elem in node.elts:
                elem_name = astor.to_source(elem).strip()
                contained_bt |= deepcopy(state.assignment[elem_name])
            new_bt = Basetype({PyType(tuple, contained_bt)})
            new_state = deepcopy(state)
            new_state.assignment[node_name] = deepcopy(new_bt)
            new_set.add(new_state)
        self.state_set = new_set

    def visit_Assign(self, node: Assign):
        self.visit(node.value)
        for target in node.targets:
            target_name = astor.to_source(target).strip()
            