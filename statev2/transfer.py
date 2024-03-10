from statev2.basetype import *


def state_apply_spec(state: State, spec: State, testmode=False) -> State:
    new_state = State()
    new_state.constraints = deepcopy(state.constraints)
    for expr in spec.assignment:
        if testmode is False:
            new_basetype = Basetype({VarType(generate_id())})
        else:
            new_basetype = Basetype({VarType(f'T_{expr}`')})
        new_state.assignment[expr] = new_basetype
        rel1 = Relation(RelOp.LEQ, new_basetype, deepcopy(state.assignment[expr]))
        rel2 = Relation(RelOp.LEQ, new_basetype, deepcopy(spec.assignment[expr]))
        andconstr = AndConstraints()
        andconstr.add(rel1)
        andconstr.add(rel2)
        new_state.constraints |= deepcopy(andconstr)
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


def find_spec(expr: str) -> StateSet:
    pass