from ast import Assign, If, Subscript, While
from typing import Any
from statev2.basetype import *
from united_specs import op_equiv, unitedspecs
from statev2.function_instance import FunctionInstance, ArgumentMismatchError


BOTTOM_BT = Basetype({PyType(BottomType)})
TOP_BT = Basetype({PyType(TopType)})


def state_apply_spec(state: State, spec: FuncSpec, testmode=False) -> State:
    new_state = State()
    new_state.gen_id = state.gen_id
    new_state.constraints = deepcopy(state.constraints)
    for expr in spec.in_state.assignment:
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
                if new_basetype == spec.in_state.assignment[expr]:
                    new_basetype = Basetype({VarType(new_varname + '`')})
            new_state.assignment[expr] = new_basetype
        else:
            new_basetype = deepcopy(state_bt)
        if not skip_new:
            new_rel = Relation(RelOp.LEQ, new_basetype, deepcopy(state.assignment[expr]))
            new_state.constraints.add(deepcopy(new_rel))
        new_rel = Relation(RelOp.LEQ, new_basetype, deepcopy(spec.in_state.assignment[expr]))
        new_state.constraints.add(deepcopy(new_rel))
    for expr in state.assignment:
        if expr not in new_state.assignment:
            new_state.assignment[expr] = deepcopy(state.assignment[expr])

    for expr, bt in spec.out_state.assignment.items():
        new_state.assignment[expr] = deepcopy(bt)
    new_state = new_state.solve_constraints(strategy_str=strat3)
    new_state.update_vt_index()
    return new_state


def set_apply_spec(state_set: StateSet, spec_set: StateSet, testmode=False) -> StateSet:
    new_set = StateSet()
    state: State
    max_id = 1
    for state in state_set:
        for spec in spec_set:
            current_state = deepcopy(state)
            current_state.gen_id = max(max_id, current_state.gen_id)
            new_state = state_apply_spec(state, spec, testmode)
            max_id = new_state.gen_id
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
            # interim_spec = fi.instantiate_spec(tosrc(node))
            interim_spec = fi.instantiate_spec()
            interim_spec_set.add(deepcopy(interim_spec))
        except ArgumentMismatchError:
            continue
    if len(interim_spec_set) == 0:
        raise RuntimeError(f'Cannot apply {spec_set} to the call {tosrc(node)}')
    return interim_spec_set


def _set_apply_specset(state_set: StateSet, node: ast.BinOp | ast.Call, testmode: bool = False) -> StateSet:
    if not isinstance(node, ast.BinOp) and not isinstance(node, ast.Call):
        raise TypeError(f'Node {tosrc(node)} cannot have specs to apply (afaik)')
    new_set = StateSet()
    interim_spec_set = substitute_state_arguments(node)
    for state in state_set:
        current_state = deepcopy(state)
        for spec in interim_spec_set:
            new_state = state_apply_spec(current_state, spec, testmode)
            if new_state != BottomState():
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
        # new_state_set = set_apply_specset(self.state_set, node, self.testmode)
        new_state_set = self.set_apply_specset(node, self.testmode)
        # new_state_set = new_state_set.solve_states()
        self.state_set = deepcopy(new_state_set)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Attribute):
            new_args = [deepcopy(node.func.value)] + deepcopy(node.args)
            new_call = ast.Call(ast.Name(id=node.func.attr), new_args, deepcopy(node.keywords))
        else:
            new_call = node
        for _arg in new_call.args:
            self.visit(_arg)
            self.state_set.solve_states()
        # new_state_set = self.set_apply_specset(node, self.testmode)
        new_state_set = self.set_apply_specset(new_call, self.testmode)
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
        # node_name = astor.to_source(node).strip()
        node_name = tosrc(node)
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
    
    def visit_Assign(self, node: Assign):
        self.visit(node.value)
        self.state_set.solve_states()
        for target in node.targets: 
            if not hasattr(target, 'elts'):
                if isinstance(target, ast.Subscript):
                    self.visit(target)
                    new_call = ast.Call(
                        ast.Name(id='subscriptassign'), [target.value, node.value], []
                    )
                    self.visit(new_call)
                    call_expr = tosrc(new_call)
                    self.state_set = self.state_set.remove_expr_from_assign(call_expr)
                else:
                    new_call = ast.Call(ast.Name(id='simpleassign'), [target, node.value], [])
                    target_src = tosrc(target)
                    use_stateset = StateSet()
                    for state in self.state_set:
                        new_state = deepcopy(state)
                        new_state.assignment[target_src] = TOP_BT
                        use_stateset.add(deepcopy(new_state))
                    self.state_set = deepcopy(use_stateset)
                    self.visit(new_call)
                    call_expr = tosrc(new_call)
                    self.state_set = self.state_set.remove_expr_from_assign(call_expr)
            else:
                if not hasattr(node.value, 'elts'):                    
                    # spec with sequential assigns
                    call_list = []
                    new_expr_set = set()
                    for elem in target.elts:
                        new_call = ast.Call(ast.Name(id='seqassign'), [elem, node.value], [])
                        new_expr_set.add(tosrc(elem))
                        call_list.append(new_call)
                    current_ss = StateSet()
                    for state in self.state_set:
                        current_state = deepcopy(state)
                        for new_expr in new_expr_set:
                            current_state.assignment[new_expr] = BOTTOM_BT
                        current_ss.add(deepcopy(current_state))
                    new_ss = StateSet()
                    for current_state in current_ss:
                        current_id = 1
                        to_lub = []
                        call_elem: ast.Call
                        for call_elem in call_list:
                            call_elem_src = tosrc(call_elem)
                            expr_src = tosrc(call_elem.args[0])
                            current_id = max(current_id, current_state.gen_id)
                            current_state.gen_id = current_id
                            interim_specset = substitute_state_arguments(call_elem)
                            interim_lub = []
                            for interim_spec in interim_specset:
                                use_state = deepcopy(current_state)
                                use_state.assignment[expr_src] = TOP_BT
                                new_st = state_apply_spec(use_state, interim_spec)
                                if new_st == BottomState():
                                    continue
                                current_id = max(current_id, new_st.gen_id)
                                del new_st.assignment[call_elem_src]
                                interim_lub.append(deepcopy(new_st))
                            interim_lubbed = State()
                            for interim_lub_elem in interim_lub:
                                interim_lubbed = State.lub(interim_lubbed, interim_lub_elem)
                            to_lub.append(deepcopy(interim_lubbed))
                        lubbed = State()
                        for lub_elem in to_lub:
                            lubbed = State.lub(lubbed, lub_elem)
                        new_ss.add(deepcopy(lubbed))
                    self.state_set = deepcopy(new_ss)
                    #
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
        # if hasattr(node.slice, 'elts'):
        #     if len(node.slice.elts) != 2:
        #         raise RuntimeError(f'{subscript_expr} does not have a valid slice')
        #     new_call = ast.Call(ast.Name(id='simple_subscript'), [node.value, node.slice.elts[0], node.slice.elts[1]], []) 
        # else:
        new_call = ast.Call(ast.Name(id='simple_subscript'), [node.value, node.slice], [])
        new_call_expr = tosrc(new_call)
        self.visit(new_call)
        self.state_set = self.state_set.replace_expr(new_call_expr, subscript_expr)

    def set_apply_specset(self, node: ast.BinOp | ast.Call, testmode: bool = False) -> StateSet:
        if not isinstance(node, ast.BinOp) and not isinstance(node, ast.Call):
            raise TypeError(f'Node {tosrc(node)} cannot have specs to apply (afaik)')
        new_set = StateSet()
        interim_spec_set = substitute_state_arguments(node)
        for interim_spec in interim_spec_set:
            for expr in interim_spec.in_state.assignment:
                expr_node = ast.parse(expr)
                self.visit(expr_node)
        for state in self.state_set:
            # current_state = deepcopy(state)
            for spec in interim_spec_set:
                new_state = state_apply_spec(state, spec, testmode)
                if new_state != BottomState():
                    new_set.add(deepcopy(new_state))
        return new_set