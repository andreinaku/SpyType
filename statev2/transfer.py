from ast import Assign, If, Subscript, While
from typing import Any
from statev2.basetype import *
from united_specs import op_equiv, unitedspecs
from statev2.function_instance import FunctionInstance, ArgumentMismatchError


def state_apply_spec(state: State, spec: State, testmode=False) -> State:
    new_state = State()
    new_state.gen_id = state.gen_id
    new_state.constraints = deepcopy(state.constraints)
    for expr in spec.assignment:
        skip_new = False
        state_bt = state.assignment[expr]
        if len(state_bt) == 1 and isinstance(state_bt[0], VarType):
            skip_new = True
        if not skip_new:
            if testmode is False:
                new_basetype = Basetype({VarType(new_state.generate_id())})
            else:
                new_varname = f'T{expr}`'
                new_basetype = Basetype({VarType(new_varname)})
                if new_basetype == spec.assignment[expr]:
                    new_basetype = Basetype({VarType(new_varname + '`')})
            new_state.assignment[expr] = new_basetype
        else:
            new_basetype = deepcopy(state_bt)
        if not skip_new:
            new_rel = Relation(RelOp.LEQ, new_basetype, deepcopy(state.assignment[expr]))
            new_state.constraints.add(deepcopy(new_rel))
        new_rel = Relation(RelOp.LEQ, new_basetype, deepcopy(spec.assignment[expr]))
        new_state.constraints.add(deepcopy(new_rel))
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
        raise TypeError(f'{tosrc(node)} is not a BinOp or a Call')
    return raw_set


def get_specset(node: ast.BinOp | ast.Call) -> hset[FuncSpec]:
    if not isinstance(node, ast.BinOp) and not isinstance(node, ast.Call):
        raise TypeError(f'Node {tosrc(node)} not supported yet')
    raw_set = find_spec(node)
    spec_set = hset()
    for str_spec in raw_set:
        spec = FuncSpec.from_str(str_spec)
        # spec_state = spec_to_state(spec)
        # spec = spec.replace_superclasses()
        spec_set.add(deepcopy(spec))
    return spec_set


def substitute_state_arguments(node: ast.BinOp | ast.Call) -> hset[FuncSpec]:
    if not isinstance(node, ast.BinOp) and not isinstance(node, ast.Call):
        raise TypeError(f'Node {tosrc(node)} cannot have arguments (afaik)')
    
    interim_spec_set = hset()
    spec_set = get_specset(node)
    for spec in spec_set:
        fi = FunctionInstance(node, spec)
        try:
            interim_spec = fi.instantiate_spec(tosrc(node))
            interim_spec_set.add(deepcopy(interim_spec))
        except ArgumentMismatchError:
            continue
    if len(interim_spec_set) == 0:
        raise RuntimeError(f'Cannot apply {spec_set} to the call {tosrc(node)}')
    return interim_spec_set


def set_apply_specset(state_set: StateSet, node: ast.BinOp | ast.Call, testmode: bool = False) -> StateSet:
    if not isinstance(node, ast.BinOp) and not isinstance(node, ast.Call):
        raise TypeError(f'Node {tosrc(node)} cannot have specs to apply (afaik)')
    new_set = StateSet()
    for state in state_set:
        interim_spec_set = substitute_state_arguments(node)
        for spec in interim_spec_set:
            new_state = state_apply_spec(state, spec.in_state, testmode)
            for expr, bt in spec.out_state.assignment.items():
                new_state.assignment[expr] = deepcopy(bt)
            new_state = new_state.solve_constraints(strategy_str=strat3)
            if new_state != BottomState():
                # new_state = new_state.generate_fresh_vartypes()
                new_state.update_vt_index()
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
            new_state.assignment[str(node.value)] = Basetype({PyType(type(node.value))})
            new_set.add(new_state)
        self.state_set = deepcopy(new_set)

    def visit_BinOp(self, node: ast.BinOp):
        self.visit(node.left)
        self.state_set = self.state_set.solve_states()
        self.visit(node.right)
        self.state_set = self.state_set.solve_states()
        new_state_set = set_apply_specset(self.state_set, node, self.testmode)
        # new_state_set = new_state_set.solve_states()
        self.state_set = deepcopy(new_state_set)

    def visit_Call(self, node: ast.Call):
        for _arg in node.args:
            self.visit(_arg)
            self.state_set.solve_states()
        new_state_set = set_apply_specset(self.state_set, node, self.testmode)
        # new_state_set = new_state_set.solve_states()
        self.state_set = deepcopy(new_state_set)

    def container_visit(self, node):
        if not hasattr(node, 'elts'):
            raise TypeError(f'Node {astor.to_source(node).strip()} should have elts field and it does not')
        if isinstance(node, ast.Tuple):
            container_tip = tuple
        elif isinstance(node, ast.List):
            container_tip = list
        elif isinstance(node, ast.Set):
            container_tip = set
        else:
            raise TypeError(f'Node {node}:{astor.to_source(node).strip()} is of unknown container type')
        for elem in node.elts:
            self.visit(elem)
        node_name = astor.to_source(node).strip()
        new_set = StateSet()
        new_state: State
        state: State
        for state in self.state_set:
            contained_bt = Basetype()
            for elem in node.elts:
                elem_name = tosrc(elem)
                contained_bt |= deepcopy(state.assignment[elem_name])
            new_bt = Basetype({PyType(container_tip, contained_bt)})
            new_state = deepcopy(state)
            new_state.assignment[node_name] = deepcopy(new_bt)
            new_set.add(new_state)
        return new_set

    def visit_Tuple(self, node: ast.Tuple):
        new_set = self.container_visit(node)
        self.state_set = new_set

    def visit_List(self, node: ast.List):
        new_set = self.container_visit(node)
        self.state_set = new_set

    def visit_Set(self, node: ast.Set):
        new_set = self.container_visit(node)
        self.state_set = new_set

    def state_apply_assign(self, state: State, node: Assign):
        new_state = deepcopy(state)
        value_src = tosrc(node.value)
        for target in node.targets:
            lhs_is_container = isinstance(target, ast.List) or isinstance(target, ast.Tuple)
            rhs_is_container = isinstance(node.value, ast.List) or isinstance(node.value, ast.Tuple)
            target_src = tosrc(target)
            if lhs_is_container:
                if rhs_is_container:
                    # a, b = c, d
                    if len(target.elts) != len(node.value.elts):
                        raise TypeError(f'{tosrc(target)} and {tosrc(node.value)} have different lengths')
                    for i in range(0, len(target.elts)):
                        target_elem_src = tosrc(target.elts[i])
                        value_elem_src = tosrc(node.value.elts[i])
                        new_state.assignment[target_elem_src] = deepcopy(new_state.assignment[value_elem_src])
                else:
                    # a, b = expr
                    contained_bt = Basetype()
                    value_bt = new_state.assignment[value_src]
                    new_value_bt = Basetype()
                    value_typevars = set()
                    target_srcs = []
                    for target_elem_node in target.elts:
                        target_elem_src = tosrc(target_elem_node)
                        if target_elem_src not in target_srcs:
                            target_srcs.append(target_elem_src)
                    for target_elem_src in target_srcs:
                        if target_elem_src not in new_state.assignment:
                            new_bt = Basetype({VarType(new_state.generate_id())})
                            new_state.assignment[target_elem_src] = new_bt
                    for ptip in value_bt:
                        if isinstance(ptip, PyType) and ptip.keys is not None:
                            contained_bt |= ptip.keys
                            new_value_bt.add(deepcopy(ptip))
                        elif ptip in extra_sequences:
                            contained_bt |= extra_sequences[ptip]
                            new_value_bt.add(deepcopy(ptip))
                        elif isinstance(ptip, VarType):
                            value_typevars.add(deepcopy(ptip))
                            new_value_bt.add(deepcopy(ptip))
                    if len(contained_bt) > 0 or len(value_typevars) > 0:
                        # expr = container< ceva >
                        if len(contained_bt) > 0:
                            for target_elem_src in target_srcs:
                                new_state.assignment[target_elem_src] = deepcopy(contained_bt)
                        iterable_pytype = PyType(Iterable)
                        iterable_contained = Basetype()
                        for target_elem_src in target_srcs:
                            iterable_contained |= deepcopy(new_state.assignment[target_elem_src])
                        iterable_pytype.keys = iterable_contained
                        value_condition = Basetype({iterable_pytype})
                        if len(value_typevars) > 0: 
                            for tv in value_typevars:
                                aux_bt_tv = Basetype({deepcopy(tv)})
                                new_state.constraints.add(Relation(RelOp.LEQ, aux_bt_tv, value_condition))
                        new_state.assignment[value_src] = new_value_bt
            else:  # todo: a = b here (no tuples)
                new_state = deepcopy(state)
                new_state.assignment[target_src] = deepcopy(new_state.assignment[value_src])
        return new_state

    # def visit_Assign(self, node: Assign):
    #     new_state_set = StateSet()
    #     self.visit(node.targets[0])
    #     self.state_set.solve_states()
    #     self.visit(node.value)
    #     self.state_set.solve_states()
    #     for state in self.state_set:
    #         new_state = self.state_apply_assign(state, node)
    #         new_state_set.add(new_state)
    #     new_state_set = new_state_set.solve_states()
    #     self.state_set = deepcopy(new_state_set)
    
    def visit_Assign(self, node: Assign):
        self.visit(node.value)
        self.state_set.solve_states()
        for target in node.targets: 
            if not hasattr(target, 'elts'):
                new_call = ast.Call(ast.Name(id='simpleassign'), [target, node.value], [])
                self.visit(new_call)
                call_expr = tosrc(new_call)
                self.state_set = self.state_set.remove_expr_from_assign(call_expr)
            else:
                if not hasattr(node.value, 'elts'):
                    call_list = [node.value]
                    for elem in target.elts:
                        call_list.append(elem)
                    new_call = ast.Call(ast.Name(id='simpleassign'), call_list, [])
                    self.visit(new_call)
                    call_expr = tosrc(new_call)
                    self.state_set = self.state_set.remove_expr_from_assign(call_expr)
                else:
                    if len(target.elts) != len(node.value.elts):
                        raise RuntimeError(f'Assignment {tosrc(node)} has operands of different lengths')
                    for i in range(0, len(target.elts)):
                        new_call = ast.Call(ast.Name(id='simpleassign'), [target.elts[i], node.value.elts[i]], [])
                        self.visit(new_call)
                        call_expr = tosrc(new_call)
                        self.state_set = self.state_set.remove_expr_from_assign(call_expr)

    def visit_Return(self, node: ast.Return):
        new_set = StateSet()
        self.visit(node.value)
        value_expr = tosrc(node.value)
        return_expr = 'return'
        state: State
        for state in self.state_set:
            new_state = deepcopy(state)
            new_state.assignment[return_expr] = deepcopy(new_state.assignment[value_expr])
            new_set.add(new_state)
        self.state_set = deepcopy(new_set)

    def visit_While(self, node: While):
        pass

    def visit_If(self, node: If):
        pass

    def visit_Subscript(self, node: ast.Subscript):
        subscript_expr = tosrc(node)
        new_call = ast.Call(ast.Name(id='emerson'), [node.value, node.slice], [])
        new_call_expr = tosrc(new_call)
        self.visit(new_call)
        new_ss = StateSet()
        state: State
        for state in self.state_set:
            new_state = State()
            new_state.constraints = deepcopy(state.constraints)
            for expr, bt in state.assignment.items():
                if expr != new_call_expr:
                    new_state.assignment[expr] = deepcopy(bt)
                    continue
                new_state.assignment[subscript_expr] = deepcopy(bt)
            new_ss.add(deepcopy(new_state))
        self.state_set = new_ss
