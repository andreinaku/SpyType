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


def substitute_state_arguments(node: ast.BinOp | ast.Call) -> hset[FuncSpec]:
    if not isinstance(node, ast.BinOp) and not isinstance(node, ast.Call):
        raise TypeError(f'Node {astor.to_source(node)} cannot have arguments (afaik)')
    
    interim_spec_set = hset()
    spec_set = get_specset(node)
    for spec in spec_set:
        fi = FunctionInstance(node, spec)
        interim_spec = fi.instantiate_spec(astor.to_source(node).strip())
        interim_spec_set.add(deepcopy(interim_spec))
    return interim_spec_set


def set_apply_specset(state_set: StateSet, node: ast.BinOp | ast.Call, testmode: bool = False) -> StateSet:
    if not isinstance(node, ast.BinOp) and not isinstance(node, ast.Call):
        raise TypeError(f'Node {astor.to_source(node)} cannot have specs to apply (afaik)')
    new_set = StateSet()
    for state in state_set:
        interim_spec_set = substitute_state_arguments(node)
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

    def state_apply_assign(self, state: State, node: Assign):
        new_state = deepcopy(state)
        for target in node.targets:
            lhs_is_container = isinstance(target, ast.List) or isinstance(target, ast.Tuple)
            rhs_is_container = isinstance(node.value, ast.List) or isinstance(node.value, ast.Tuple)
            if lhs_is_container and rhs_is_container:
                # a, b = c, d
                if len(target.elts) != len(node.value.elts):
                    raise TypeError(f'{astor.to_source(target.strip())} and {astor.to_source(node.value).strip()} have different lengths')
                for i in range(0, len(target.elts)):
                    # todo: these are ast nodes; be careful!
                    target_src = astor.to_source(target.elts[i]).strip()
                    value_src = astor.to_source(node.value.elts[i]).strip()
                    new_state.assignment[target_src] = deepcopy(new_state.assignment[value_src])
            elif lhs_is_container and not rhs_is_container:
                # a, b = expr
                self.visit(node.value)
                value_src = astor.to_source(node.value).strip()
                contained_bt = Basetype()
                value_bt = new_state.assignment[value_src]
                for ptip in value_bt:
                    if isinstance(ptip, PyType) and ptip.keys is not None:
                        contained_bt |= ptip.keys
                if len(contained_bt) > 0:
                    # expr = container< ceva >
                    for elem in target.elts:
                        elem_src = astor.to_source(elem).strip()
                        new_state.assignment[elem_src] = deepcopy(contained_bt)
                else:
                    # expr = not container
                    for elem in target.elts:
                        elem_src = astor.to_source(elem).strip()
                        if elem_src not in new_state.assignment:
                            new_bt = Basetype({VarType(new_state.generate_id())})
                            new_state.assignment[elem_src] = new_bt
                        else:
                            new_bt = deepcopy(new_state.assignment[elem_src])
                        new_contained |= deepcopy(new_bt)
                    expr_bt = Basetype({PyType(Iterable, new_contained)})
                    # todo: replace basetype in state?
                    raise RuntimeError('not supported yet')
            else:
                raise RuntimeError('not supported yet')
        return new_state

    def visit_Assign(self, node: Assign):
        new_state_set = StateSet()
        self.visit(node.value)
        for state in self.state_set:
            new_state = self.state_apply_assign(state, node)
            new_state_set.add(new_state)
        self.state_set = deepcopy(new_state_set)
