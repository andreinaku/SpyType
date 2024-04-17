import os.path
import os
import ast
import maude
from statev2.maude_gen import mod_generator
from statev2.transfer import *
from statev2.united_specs import unitedspecs, op_equiv


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
    print_str = print_str[:-5]
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
    c_value = get_constraints_string_from_states(applied)
    maude_input = mod_generator('tempmod', c_value, dump_to_file=dump)
    return maude_input


if __name__ == "__main__":
    start_set = r'(a:int + float /\ b:int + float + str)'
    simple_expr = ['a+b', 'a/b', 'a>>b', 'a*b', 'a-b']
    expr_1 = ['(a+b)/c']
    # output_expressions(simple_expr, start_set)
    # start_set = r'(a:int+float /\ b:int+float+str /\ c:str)'
    # output_expressions(expr_1, start_set)
    start_set = r'(a:list< int + str > /\ b:list< float >)'
    # simple_expr = ['a+b']
    aux = maude.init()
    aux = maude.load('init.maude')
    constr_module = maude.getModule('CONSTR')
    strat = constr_module.parseStrategy('one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; Step5 ! ; Step6 ! ')
    strat2 = constr_module.parseStrategy('one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; one(Step4) ! ; Step5 ! ; Step6 ! ')
    with open('solver.out', 'w') as f:
        for expr in simple_expr:
            m_input = dump_to_maude(expr, start_set, dump=False)
            aux = maude.input(m_input)
            mod = maude.getModule('tempmod')
            term = mod.parseTerm('c [nil]')
            f.write(f'{expr}{os.linesep}')
            for result, nrew in term.srewrite(strat):
                f.write(f'{result}{os.linesep} in {nrew} rewrites{os.linesep}')
            for result, nrew in term.srewrite(strat2):
                f.write(f'{result}{os.linesep} in {nrew} rewrites{os.linesep}')
            f.write(os.linesep)
