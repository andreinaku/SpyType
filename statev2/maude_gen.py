import os
import os.path
import maude
from statev2.transfer import *
from united_specs import unitedspecs, op_equiv


strat1 = 'one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; Step5 ! ; Step6 ! '
strat2 = 'one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; one(Step4) ! ; Step5 ! ; Step6 ! '


def vartype_generator(maxitems = 20):
    normals = []
    specs = []
    for i in range(0, maxitems):
        normals.append(f'T{i}')
        specs.append(f'T?{i}')
    return normals, specs


def mod_generator(mod_name: str, constraints: str, indent=2, dump_to_file=False) -> str:
    spaces = ' ' * indent
    maude_code = (f'mod {mod_name} is {os.linesep}'
                    f'{spaces}protecting CONSTR .{os.linesep}'
                    f'{spaces}ops ')
    normals, specs = vartype_generator()
    for n in normals:
        maude_code += f'{n} '
    maude_code += (f': -> VarType .{os.linesep}'
                     f'{spaces}ops ')
    for s in specs:
        maude_code += f'{s} '
    maude_code += (f': -> BoundVarType .{os.linesep}'
                     f'{spaces}op c : -> Disj .{os.linesep}'
                     f'{os.linesep}{spaces}eq c = {os.linesep}{constraints} .{os.linesep}'
                     f'{os.linesep}'
                     f'endm')
    if dump_to_file:
        open(mod_name + '.maude', 'w').write(maude_code)
    return maude_code


def get_states(state_set: StateSet, expr: str) -> StateSet:
    tree = ast.parse(expr)
    tf = TransferFunc(state_set)
    tf.visit(tree)
    return tf.state_set


def get_constraints_list(state_set: StateSet) -> list[AndConstraints]:
    ll = []
    for state in state_set:
        ll.append(state.constraints)
    return ll


def get_constraints_string_from_states(state_set: StateSet) -> str:
    print_str = ''
    constr_list = get_constraints_list(state_set)
    for constraint in constr_list:
        retstr = str(constraint)
        # for eq_in, eq_out in type_equiv.items():
        #     retstr = retstr.replace(eq_in, eq_out)
        print_str += f'({retstr}) \\/ {os.linesep}'
    print_str = print_str[:(-4 - len(os.linesep))]
    return print_str


def output_expressions(expr_list: list[str], str_state_set: str,
                       outc_file: str = 'out_constraints.txt', outs_file: str = 'out_states.txt'):
    current = Translator.translate_state_set(str_state_set)
    if os.path.exists(outc_file):
        os.remove(outc_file)
    if os.path.exists(outs_file):
        os.remove(outs_file)
    with open(outc_file, 'a') as f:
        for expr in expr_list:
            f.write(f'{'-' * (len(expr) + 4)}\n| {expr} |\n{'-' * (len(expr) + 4)}\n')
            applied = get_states(current, expr)
            print_str = get_constraints_string_from_states(applied)
            f.write(print_str + '\n\n')
    with open(outs_file, 'a') as f:
        for expr in expr_list:
            f.write(f'{'-' * (len(expr) + 4)}\n| {expr} |\n{'-' * (len(expr) + 4)}\n')
            applied = get_states(current, expr)
            print_str = ''
            for state in applied:
                retstr = str(state)
                # for eq_in, eq_out in type_equiv.items():
                #     retstr = retstr.replace(eq_in, eq_out)
                print_str += f'({retstr}) \\/ \n'
            f.write(print_str[:-5] + '\n\n')


def apply_spec_on_stateset(expr: str, state_set: StateSet):
    applied = get_states(state_set, expr)
    applied = applied.replace_superclasses()
    return applied


def dump_to_maude(state_set: StateSet, dump=False) -> str:
    c_value = get_constraints_string_from_states(state_set)
    maude_input = mod_generator('tempmod', c_value, dump_to_file=dump)
    return maude_input


def dump_single_state_to_maude(state:State, dump=False) -> str:
    c_value = str(state.constraints)
    maude_input = mod_generator('tempmod', c_value, dump_to_file=dump)
    return maude_input


def parse_result(maude_result: maude.Term) -> list[list[Relation]]:
    relations_list = []
    cases = str(maude_result).split('||')
    for case in cases:
        relations = []
        m_res = case.replace('[nil]', '')
        result_list = m_res.split('/\\')
        for elem in result_list:
            aux = elem.strip('() ')
            rel = Translator.translate_relation(aux)
            relations.append(deepcopy(rel))
        if len(relations) > 0:
            relations_list.append(deepcopy(relations))
    return relations_list


def _apply_and_solve(current_state_set: StateSet, expr: str, output_file):
    aux = maude.init()
    aux = maude.load('init.maude')
    modulename = 'tempmod'
    constr_module = maude.getModule('CONSTR')
    # strat = constr_module.parseStrategy('one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; Step5 ! ; Step6 ! ')
    strat2 = constr_module.parseStrategy('one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; one(Step4) ! ; Step5 ! ; Step6 ! ')
    rel_list = None
    with open(output_file, 'a') as f:
        # for expr in simple_expr:
        new_state_set = apply_spec_on_stateset(expr, current_state_set)
        m_input = dump_to_maude(new_state_set, dump=True)
        if not maude.input(m_input):
            raise RuntimeError('Maude input operation failed')
        mod = maude.getModule(modulename)
        if mod is None:
            raise RuntimeError(f'Maude module {modulename} not found')
        term = mod.parseTerm('c [nil]')
        f.write(f'{expr}{os.linesep}')
        # for result, nrew in term.srewrite(strat):
        #     f.write(f'{result}{os.linesep} in {nrew} rewrites{os.linesep}')
        srew_2 = term.srewrite(strat2)
        aux_len = 0
        for result, nrew in srew_2:
            if aux_len > 0:
                raise RuntimeError('Too many maude results')
            aux_len += 1
            f.write(f'{result}{os.linesep} in {nrew} rewrites{os.linesep}')
            rel_list = parse_result(result)
        f.write(os.linesep)
    return new_state_set, rel_list


def _apply_and_solve_2(current_state_set: StateSet, expr: str, output_file):
    aux = maude.init()
    aux = maude.load('init.maude')
    modulename = 'tempmod'
    constr_module = maude.getModule('CONSTR')
    strat = constr_module.parseStrategy('one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; Step5 ! ; Step6 ! ')
    strat2 = constr_module.parseStrategy('one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; one(Step4) ! ; Step5 ! ; Step6 ! ')
    rel_list = None
    with open(output_file, 'a') as f:
        # for expr in simple_expr:
        new_state_set = apply_spec_on_stateset(expr, current_state_set)
        for new_state in new_state_set:
            f.write(str(new_state) + os.linesep)
            m_input = dump_single_state_to_maude(new_state, dump=True)
            if not maude.input(m_input):
                raise RuntimeError('Maude input operation failed')
            mod = maude.getModule(modulename)
            if mod is None:
                raise RuntimeError(f'Maude module {modulename} not found')
            term = mod.parseTerm('c [nil]')
            f.write(f'{expr}{os.linesep}')
            # for result, nrew in term.srewrite(strat):
            #     f.write(f'{result}{os.linesep} in {nrew} rewrites{os.linesep}')
            srew_2 = term.srewrite(strat2)
            aux_len = 0
            for result, nrew in srew_2:
                if aux_len > 0:
                    raise RuntimeError('Too many maude results')
                aux_len += 1
                f.write(f'{result}{os.linesep} in {nrew} rewrites{os.linesep}')
                rel_list = parse_result(result)
            f.write(os.linesep)

        f.write(str(new_state_set))
        m_input = dump_to_maude(new_state_set, dump=True)
        if not maude.input(m_input):
            raise RuntimeError('Maude input operation failed')
        mod = maude.getModule(modulename)
        if mod is None:
            raise RuntimeError(f'Maude module {modulename} not found')
        term = mod.parseTerm('c [nil]')
        f.write(f'{expr}{os.linesep}')
        for result, nrew in term.srewrite(strat):
            f.write(f'{result}{os.linesep} in {nrew} rewrites{os.linesep}')
    return new_state_set, rel_list


def apply_and_solve(current_state_set: StateSet, expr: str, strategy_str: str, output_file: str) -> tuple[StateSet, list[list[Relation]]]:
    if not maude.init():
        raise RuntimeError('Could not properly initialize maude')
    init_module = 'init.maude'
    if not maude.load('init.maude'):
        raise RuntimeError(f'Could not load {init_module}')
    modulename = 'tempmod'
    constr_module_name = 'CONSTR'
    constr_module = maude.getModule(constr_module_name)
    if constr_module is None:
        raise RuntimeError(f'Could not get module {constr_module}')
    relation_groups = None
    with open(output_file, 'a') as f:
        # for expr in simple_expr:
        new_state_set = apply_spec_on_stateset(expr, current_state_set)
        m_input = dump_to_maude(new_state_set, dump=True)
        if not maude.input(m_input):
            raise RuntimeError('Maude input operation failed')
        mod = maude.getModule(modulename)
        if mod is None:
            raise RuntimeError(f'Maude module {modulename} not found')
        term_str = 'c [nil]'
        term = mod.parseTerm(term_str)
        if term is None:
            raise RuntimeError(f'Cannot parse term {term_str}')
        f.write(f'{expr}{os.linesep}')
        strat = constr_module.parseStrategy(strategy_str)
        if not strat:
            raise RuntimeError(f'Cannot parse strategy {strategy_str}')
        srew = term.srewrite(strat)
        if srew is None:
            raise RuntimeError(f'Could not rewrite using {strategy_str}')
        aux_len = 0
        for result, nrew in srew:
            if aux_len > 0:
                raise RuntimeError('Too many maude results')
            aux_len += 1
            f.write(f'{result}{os.linesep} in {nrew} rewrites{os.linesep}')
            relation_groups = parse_result(result)
        f.write(os.linesep)
    return new_state_set, relation_groups



def solve_state_constraints(state: State, strategy_str: str) -> State:
    new_state = State()
    if not maude.init():
        raise RuntimeError('Could not properly initialize maude')
    init_module = 'init.maude'
    if not maude.load('init.maude'):
        raise RuntimeError(f'Could not load {init_module}')
    modulename = 'tempmod'
    constr_module_name = 'CONSTR'
    constr_module = maude.getModule(constr_module_name)
    if constr_module is None:
        raise RuntimeError(f'Could not get module {constr_module}')
    relation_groups = None
    c_value = str(state.constraints)
    m_input = mod_generator('tempmod', c_value, dump_to_file=True)
    if not maude.input(m_input):
        raise RuntimeError('Maude input operation failed')
    mod = maude.getModule(modulename)
    if mod is None:
        raise RuntimeError(f'Maude module {modulename} not found')
    term_str = 'c [nil]'
    term = mod.parseTerm(term_str)
    if term is None:
        raise RuntimeError(f'Cannot parse term {term_str}')
    strat = constr_module.parseStrategy(strategy_str)
    if not strat:
        raise RuntimeError(f'Cannot parse strategy {strategy_str}')
    srew = term.srewrite(strat)
    if srew is None:
        raise RuntimeError(f'Could not rewrite using {strategy_str}')
    aux_len = 0
    for result, nrew in srew:
        if aux_len > 0:
            raise RuntimeError('Too many maude results')
        aux_len += 1
        relation_groups = parse_result(result)
    new_state.assignment = deepcopy(state.assignment)
    return new_state


def replace_from_relations(state: State, relations: list[Relation]) -> State:
    new_state = State()
    new_state.assignment = deepcopy(state.assignment)
    for rel in relations:
        if len(rel.bt_left) > 1 or not isinstance(rel.bt_left[0], VarType):
            raise TypeError(f'{rel.bt_left} should be a VarType')
        to_replace = rel.bt_left[0]
        new_state.assignment = new_state.assignment.replace_vartype_with_basetype(to_replace, rel.bt_right)
    return new_state


def get_new_state_set(current_state_set: StateSet, expr: str, output_file: str = 'solver.out') -> StateSet:
    applied_state_set, rel_groups = apply_and_solve(current_state_set, expr, strat1, output_file)
    replace_map = dict()
    for rel_group in rel_groups:
        skip_group = False
        for relation in rel_group:
            if relation.bt_right == Basetype({PyType(type(None))}):
                skip_group = True
        if skip_group:
            continue
        for relation in rel_group:
            if relation.bt_left not in replace_map:
                replace_map[relation.bt_left] = relation.bt_right
            else:
                replace_map[relation.bt_left] |= relation.bt_right
    new_state_set = StateSet()
    current_state: State
    for current_state in applied_state_set:
        # new_state = replace_from_relations(current_state, rel_groups)
        new_state = State()
        new_state.assignment = deepcopy(current_state.assignment)
        for to_replace, replace_with in replace_map.items():
            new_state = new_state.replace_assignment_basetypes(to_replace, replace_with)
        new_state_set.add(new_state)
    print(f'-------------{os.linesep}Unsolved: {applied_state_set}{os.linesep}-------------{os.linesep}Solved: {new_state_set}')
    return new_state_set
