from statev2.maude_gen import *


if __name__ == "__main__":
    start_set = r'(a:int + float /\ b:int + float + str)'
    simple_expr = ['a+b', 'a/b', 'a>>b', 'a*b', 'a-b']
    # simple_expr = ['(a+b)/c']
    # simple_expr = ['len(a)']
    # output_expressions(simple_expr, start_set)
    # start_set = r'(a:int+float /\ b:int+float+str /\ c:str)'
    # output_expressions(expr_1, start_set)
    # start_set = r'(c:Tc + list< float >)'
    # simple_expr = ['a+b']
    # simple_expr = ['b = c']
    aux = maude.init()
    aux = maude.load('init.maude')
    constr_module = maude.getModule('CONSTR')
    strat = constr_module.parseStrategy('one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; Step5 ! ; Step6 ! ')
    strat2 = constr_module.parseStrategy('one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; one(Step4) ! ; Step5 ! ; Step6 ! ')
    with open('solver.out', 'w') as f:
        for expr in simple_expr:
            m_input = dump_to_maude(expr, start_set, dump=True)
            aux = maude.input(m_input)
            mod = maude.getModule('tempmod')
            term = mod.parseTerm('c [nil]')
            f.write(f'{expr}{os.linesep}')
            # for result, nrew in term.srewrite(strat):
            #     f.write(f'{result}{os.linesep} in {nrew} rewrites{os.linesep}')
            for result, nrew in term.srewrite(strat2):
                f.write(f'{result}{os.linesep} in {nrew} rewrites{os.linesep}')
                aux = parse_result(result)
                print(aux)
            f.write(os.linesep)
