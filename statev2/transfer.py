from ast import Assign, Compare, For, If, Subscript, While
from typing import Any
from statev2.basetype import *
from united_specs import op_equiv, unitedspecs
from class_specs import class_specs as cspecs
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


def find_spec_new(node: ast.BinOp | ast.Call) -> StateSet:
    if isinstance(node, ast.BinOp):
        funcname = op_equiv[ast.BinOp][type(node.op)]
    elif isinstance(node, ast.Call):\
        funcname = node.func.id
    else:
        raise TypeError(f'{tosrc(node)} is not a BinOp or a Call')
    ret_set = StateSet()
    for classname, specdict in cspecs.items():
        for fname, specset in specdict['methods'].items():
            if fname == funcname:
                ret_set |= deepcopy(specset)
    return ret_set


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


class GetNames(ast.NodeVisitor):
    def __init__(self):
        self.names = set()

    def visit_Name(self, node: ast.Name):
        self.names.add(node.id)

    def reset_names(self):
        self.names = set()

    def get_names(self):
        return self.names


class ReplaceNames(ast.NodeTransformer):
    def __init__(self, name_replace: dict):
        self.name_replace = name_replace

    def visit_Name(self, node:ast.Name):
        if node.id in self.name_replace:
            node.id = self.name_replace[node.id]
        return node


class TransferFunc(ast.NodeVisitor):
    def __init__(self, _state_set: StateSet, _testmode=False):
        self.state_set = deepcopy(_state_set)
        self.testmode = _testmode

    def visit_Constant(self, node: ast.Constant):
        new_set = StateSet()
        for state in self.state_set:
            new_state = deepcopy(state)
            # new_state.assignment[str(node.value)] = Basetype({PyType(type(node.value))})
            new_state.assignment[tosrc(node)] = Basetype({PyType(type(node.value))})
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
        # for testing purposes with static type checkers like mypy and pyright
        if isinstance(node.func, ast.Name) and node.func.id == 'reveal_type':
            return
        #
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
            if len(contained_bt) == 0:
                contained_bt = BOTTOM_BT
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
    
    def visit_Assign(self, _node: Assign):
        # common lhs and rhs names
        node = deepcopy(_node)
        gn = GetNames()
        gn.visit(node.value)
        rhs_names = deepcopy(gn.get_names())
        gn.reset_names()
        lhs_names = set()
        for target in node.targets:
            gn.visit(target)
            lhs_names |= deepcopy(gn.get_names())
            gn.reset_names()
        var_replace = dict()
        new_ss = StateSet()
        new_varnames = []
        auxiliary_expressions = []
        for state in self.state_set:
            new_state = deepcopy(state)
            for varname in rhs_names:
                if varname not in lhs_names:
                    continue
                new_varname = varname + '_temp'
                auxiliary_expressions.append(new_varname)
                new_varnames.append(new_varname)
                var_replace[varname] = deepcopy(new_varname)
                new_state.assignment[new_varname] = deepcopy(state.assignment[varname])
            new_ss.add(new_state)
        self.state_set = deepcopy(new_ss)
        # compose the new assign node
        rn = ReplaceNames(var_replace)
        rn.visit(node.value)
        #
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
                    auxiliary_expressions.append(call_expr)
                    # self.state_set = self.state_set.remove_expr_from_assign(call_expr)
            else:
                if not hasattr(node.value, 'elts'):                    
                    # spec with sequential assigns
                    call_list = []
                    new_expr_set = set()

                    # new start
                    for elem in target.elts:
                        new_call = ast.Call(ast.Name(id='seqassign'), [elem, node.value], [])
                        call_expr = tosrc(new_call)
                        target_src = tosrc(elem)
                        use_stateset = StateSet()
                        for state in self.state_set:
                            new_state = deepcopy(state)
                            new_state.assignment[target_src] = TOP_BT
                            use_stateset.add(deepcopy(new_state))
                        self.state_set = deepcopy(use_stateset)
                        self.visit(new_call)
                        auxiliary_expressions.append(call_expr)
                    # new end

                    # old start
                    # for elem in target.elts:
                    #     new_call = ast.Call(ast.Name(id='seqassign'), [elem, node.value], [])
                    #     new_expr_set.add(tosrc(elem))
                    #     call_list.append(new_call)
                    # current_ss = StateSet()
                    # for state in self.state_set:
                    #     current_state = deepcopy(state)
                    #     for new_expr in new_expr_set:
                    #         current_state.assignment[new_expr] = BOTTOM_BT
                    #     current_ss.add(deepcopy(current_state))
                    # new_ss = StateSet()
                    # for current_state in current_ss:
                    #     current_id = 1
                    #     to_lub = []
                    #     call_elem: ast.Call
                    #     for call_elem in call_list:
                    #         call_elem_src = tosrc(call_elem)
                    #         expr_src = tosrc(call_elem.args[0])
                    #         current_id = max(current_id, current_state.gen_id)
                    #         current_state.gen_id = current_id
                    #         interim_specset = substitute_state_arguments(call_elem)
                    #         interim_lub = []
                    #         for interim_spec in interim_specset:
                    #             use_state = deepcopy(current_state)
                    #             use_state.assignment[expr_src] = TOP_BT
                    #             new_st = state_apply_spec(use_state, interim_spec)
                    #             if new_st == BottomState():
                    #                 continue
                    #             current_id = max(current_id, new_st.gen_id)
                    #             del new_st.assignment[call_elem_src]
                    #             interim_lub.append(deepcopy(new_st))
                    #         interim_lubbed = State()
                    #         for interim_lub_elem in interim_lub:
                    #             interim_lubbed = State.lub(interim_lubbed, interim_lub_elem)
                    #         to_lub.append(deepcopy(interim_lubbed))
                    #     lubbed = State()
                    #     for lub_elem in to_lub:
                    #         lubbed = State.lub(lubbed, lub_elem)
                    #     new_ss.add(deepcopy(lubbed))
                    # self.state_set = deepcopy(new_ss)
                    # old end
                else:
                    if len(target.elts) != len(node.value.elts):
                        raise RuntimeError(f'Assignment {tosrc(node)} has operands of different lengths')
                    for i in range(0, len(target.elts)):
                        # #
                        # new_call = ast.Call(ast.Name(id='simpleassign'), [target, node.value], [])
                        # target_src = tosrc(target)
                        # use_stateset = StateSet()
                        # for state in self.state_set:
                        #     new_state = deepcopy(state)
                        #     new_state.assignment[target_src] = TOP_BT
                        #     use_stateset.add(deepcopy(new_state))
                        # self.state_set = deepcopy(use_stateset)
                        # self.visit(new_call)
                        # call_expr = tosrc(new_call)
                        # self.state_set = self.state_set.remove_expr_from_assign(call_expr)
                        # #

                        new_call = ast.Call(ast.Name(id='simpleassign'), [target.elts[i], node.value.elts[i]], [])
                        target_src = tosrc(target.elts[i])
                        use_stateset = StateSet()
                        for state in self.state_set:
                            new_state = deepcopy(state)
                            new_state.assignment[target_src] = TOP_BT
                            use_stateset.add(deepcopy(new_state))
                        self.state_set = deepcopy(use_stateset)
                        self.visit(new_call)
                        call_expr = tosrc(new_call)
                        auxiliary_expressions.append(call_expr)
        for aux_expr in auxiliary_expressions:
            self.state_set = self.state_set.remove_expr_from_assign(aux_expr)        

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
        self.visit(node.test)
        # self.generic_visit(node)

    def visit_If(self, node: If):
        self.visit(node.test)
        # self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript):
        subscript_expr = tosrc(node)
        new_call = ast.Call(ast.Name(id='simple_subscript'), [node.value, node.slice], [])
        new_call_expr = tosrc(new_call)
        self.visit(new_call)
        self.state_set = self.state_set.replace_expr(new_call_expr, subscript_expr)

    def visit_For(self, node: ast.For):
        self.visit(node.iter)
        targetsrc = tosrc(node.target)
        st: State
        for st in self.state_set:
            st.assignment[targetsrc] = TOP_BT
        new_call = ast.Call(
            ast.Name(id='for_parse'),
            [node.target, node.iter],
            []
        )
        new_call_expr = tosrc(new_call)
        self.visit(new_call)
        self.state_set = self.state_set.remove_expr_from_assign(new_call_expr)

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
                open(DEFAULT_SOLVER_OUT, 'a').write(
                    f'-----------------{os.linesep}State / Spec{os.linesep}{state}{os.linesep}{spec}{os.linesep}-----------------{os.linesep}'
                )
                new_state = state_apply_spec(state, spec, testmode)
                if new_state != BottomState():
                    new_set.add(deepcopy(new_state))
        return new_set
