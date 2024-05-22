from statev2.maude_gen import *


if __name__ == "__main__":
    str_start_set = r'(a:int + float /\ b:int + float + str)'
    start_set = Translator.translate_state_set(str_start_set)
    simple_expr = ['a+b', 'a/b', 'a>>b', 'a*b', 'a-b']
    ofile = 'solver.out'
    if os.path.exists(ofile):
        os.remove(ofile)
    for expr in simple_expr:
        aux = get_new_state_set(start_set, expr, ofile)
        print(aux)
