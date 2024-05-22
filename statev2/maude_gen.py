import os
import os.path
import maude
from statev2.transfer import *
from united_specs import unitedspecs, op_equiv


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


def dump_to_maude(expr: str, str_state_set: str, dump=False) -> str:
    current = Translator.translate_state_set(str_state_set)
    applied = get_states(current, expr)
    applied = applied.replace_superclasses()
    c_value = get_constraints_string_from_states(applied)
    maude_input = mod_generator('tempmod', c_value, dump_to_file=dump)
    return maude_input


def parse_result(maude_result: maude.Term) -> list[Relation]:
    relation_list = []
    m_res = str(maude_result).replace('[nil]', '')
    result_list = m_res.split('/\\')
    for elem in result_list:
        aux = elem.strip()
        aux = aux.replace('(', '')
        aux = aux.replace(')', '')
        rel = Translator.translate_relation(aux)
        relation_list.append(deepcopy(rel))
    return relation_list
