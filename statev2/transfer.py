import ast
import astor
from statev2.basetype import *
from statev2.specs import unitedspecs, op_equiv
from Translator import Translator


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


def find_spec_from_binop(binop_node: ast.BinOp) -> StateSet:
    spec_name = op_equiv[ast.BinOp][type(binop_node.op)]
    raw_set = unitedspecs[spec_name]
    return raw_set


def get_specset_from_binop(binop_node: ast.BinOp) -> hset[FuncSpec]:
    raw_set = find_spec_from_binop(binop_node)
    spec_set = hset()
    for str_spec in raw_set:
        spec = Translator.translate_func_spec(str_spec)
        # spec_state = spec_to_state(spec)
        spec_set.add(deepcopy(spec))
    return spec_set


def substitute_binop_state_arguments(state: State, binop_node: ast.BinOp) -> hset[FuncSpec]:
    return_name = 'return'
    spec_set = get_specset_from_binop(binop_node)
    op_args = (astor.to_source(binop_node.left).strip(), astor.to_source(binop_node.right).strip())
    new_set = hset()
    for spec in spec_set:
        new_spec = FuncSpec()
        i = 0
        for expr in spec.in_state.assignment:
            new_spec.in_state.assignment[op_args[i]] = deepcopy(spec.in_state.assignment[expr])
            i = i + 1
        op_expr = astor.to_source(binop_node).strip()
        new_spec.out_state.assignment[op_expr] = deepcopy(spec.out_state.assignment[return_name])
        new_set.add(deepcopy(new_spec))
    return new_set


def set_apply_binop_spec(state_set: StateSet, binop_node: ast.BinOp, testmode: bool = False) -> StateSet:
    new_set = StateSet()
    for state in state_set:
        interim_spec_set = substitute_binop_state_arguments(state, binop_node)
        for spec in interim_spec_set:
            new_state = state_apply_spec(state, spec.in_state, testmode)
            for expr, bt in spec.out_state.assignment.items():
                new_state.assignment[expr] = deepcopy(bt)
            new_set.add(new_state)
    return new_set
