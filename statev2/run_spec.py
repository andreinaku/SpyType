from statev2.transfer import *
from statev2.specs import *


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


def output_expressions(expr_list: list[str], str_state_set: str):
    current = Translator.translate_state_set(str_state_set)
    with open('out_constraints.txt', 'a') as f:
        for expr in expr_list:
            f.write(f'{'-' * (len(expr) + 4)}\n| {expr} |\n{'-' * (len(expr) + 4)}\n')
            applied = get_states(current, expr)
            print_str = ''
            for constraint in get_constraints_list(applied):
                retstr = str(constraint)
                for eq_in, eq_out in type_equiv.items():
                    retstr = retstr.replace(eq_in, eq_out)
                print_str += f'({retstr}) \\/ \n'
            f.write(print_str[:-5] + '\n\n')

    with open('out_states.txt', 'a') as f:
        for expr in expr_list:
            f.write(f'{'-' * (len(expr) + 4)}\n| {expr} |\n{'-' * (len(expr) + 4)}\n')
            applied = get_states(current, expr)
            print_str = ''
            for state in applied:
                retstr = str(state)
                for eq_in, eq_out in type_equiv.items():
                    retstr = retstr.replace(eq_in, eq_out)
                print_str += f'({retstr}) \\/ \n'
            f.write(print_str[:-5] + '\n\n')


if __name__ == "__main__":
    start_set = r'(a:int+float /\ b:int+float+str)'
    simple_expr = ['a+b', 'a/b', 'a>>b', 'a*b', 'a-b']
    expr_1 = ['(a+b)/c']
    # output_expressions(simple_expr, start_set)
    start_set = r'(a:int+float /\ b:int+float+str /\ c:str)'
    output_expressions(expr_1, start_set)
