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


if __name__ == "__main__":
    simple_expressions = [
        'a+b', 'a/b', 'a>>b', 'a*b', 'a-b'
    ]
    current = Translator.translate_state_set(r'(a:int+float /\ b:int+float+str)')
    for simple_expr in simple_expressions:
        print(f'{simple_expr}:\n')
        applied = get_states(current, simple_expr)
        for constraint in get_constraints_list(applied):
            retstr = str(constraint)
            for eq_in, eq_out in type_equiv.items():
                retstr = retstr.replace(eq_in, eq_out)
            print(retstr)
        print('\n')
