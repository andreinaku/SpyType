from __future__ import annotations
import maude
import os
import sys
sys.path.append(os.getcwd())
from copy import deepcopy
from statev2.Translator import *


strat1 = 'one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; Step5 ! ; Step6 ! '
strat2 = 'one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; one(Step4) ! ; Step5 ! ; Step6 ! '


class ConstraintSolver:
    def __init__(self, state: State):
        self.state = deepcopy(state)

    @staticmethod
    def maude_vartype_generator(maxitems: int = 20) -> tuple[list[str], list[str]]:
        normals = []
        specs = []
        for i in range(0, maxitems):
            normals.append(f'T{i}')
            specs.append(f'T?{i}')
        return normals, specs

    def mod_generator(self, mod_name: str, constraints: str, dump_file: str | None  = None, indent: int = 2) -> str:
        spaces = ' ' * indent
        maude_code = (f'mod {mod_name} is {os.linesep}'
                        f'{spaces}protecting CONSTR .{os.linesep}'
                        f'{spaces}ops ')
        normals, specs = self.maude_vartype_generator()
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
        if dump_file is not None:
            open(dump_file, 'w').write(maude_code)
        return maude_code

    @staticmethod
    def parse_single_result_string(case: str) -> list[Relation]:
        relations = []
        m_res = case.replace('[nil]', '')
        result_list = m_res.split('/\\')
        for elem in result_list:
            aux = elem.strip('() ')
            rel = Translator.translate_relation(aux)
            relations.append(deepcopy(rel))
        return relations

    def solve_state_constraints(self, strategy_str: str, dump_file: str | None = None) -> State:
        modulename = 'tempmod'
        constr_module_name = 'CONSTR'
        constr_module = maude.getModule(constr_module_name)
        if constr_module is None:
            raise RuntimeError(f'Could not get module {constr_module}')
        if len(self.state.constraints) == 0:
            return deepcopy(self.state)
        c_value = str(self.state.constraints)
        m_input = self.mod_generator('tempmod', c_value, dump_file)
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
        relations = None
        for result, nrew in srew:
            if aux_len > 0:
                raise RuntimeError('Too many maude results')
            aux_len += 1
            relations = self.parse_single_result_string(str(result))
        new_state = State()
        new_state.assignment = deepcopy(self.state.assignment)
        if relations is None:
            raise RuntimeError(f'Empty relations for {str(result)}')
        for rel in relations:
            if len(rel.bt_left) > 1 or not isinstance(rel.bt_left[0], VarType):
                raise TypeError(f'{rel.bt_left} should be a VarType')
            to_replace = rel.bt_left[0]
            new_state.assignment = new_state.assignment.replace_vartype_with_basetype(to_replace, rel.bt_right)
        return new_state 
