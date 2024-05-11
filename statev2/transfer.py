from ast import Assign
from typing import Any
from statev2.basetype import *
from united_specs import op_equiv, unitedspecs
from statev2.Translator import Translator
from statev2.function_instance import FunctionInstance


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
            