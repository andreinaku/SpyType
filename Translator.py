from __future__ import annotations
from AbstractState import *
import re
from statev2.basetype import Basetype, Assignment, AndConstraints, Relation, RelOp, State, OrConstraints, StateSet, FuncSpec
from pyiparser import type_equivalences
from pyiparser.type_equivalences import *


NONE_TYPE = 'NoneType'


class Translator:
    @staticmethod
    def _elim_paren(foo: str) -> str:
        if foo.startswith('(') and foo.endswith(')'):
            return foo[1:-1]
        return foo

    @staticmethod
    def get_types_from_list(instr: str, start_br, end_br, sep):
        # if contained between parantheses, remove them. (int) => int, (int+float) => int+float
        instr = elim_paren(instr)
        typelist = []
        newstr = ""
        in_contained = 0
        state = 0
        i = 0
        length = len(instr)
        if length == 0:
            return typelist
        while True:
            c = instr[i]
            if state == 0:
                if i == (length - 1):
                    break
                if c == sep or c == " ":
                    i += 1
                    continue
                state = 1
                continue
            if state == 1:
                if c == start_br:
                    in_contained += 1
                if c == end_br:
                    in_contained -= 1
                if c == sep and not in_contained:
                    state = 2
                    continue
                newstr += c
                if i == (length - 1):
                    state = 2
                    continue
                i += 1
                continue
            if state == 2:
                if len(newstr):
                    typelist.append(newstr)
                newstr = ""
                state = 0
                continue
        return typelist

    @staticmethod
    def translate_type(strtype: str, start_br="<", end_br=">", sep="+"):

        def get_kvlist(strtypes):
            level = 0
            toadd = ''
            kvlist = []
            for c in strtypes:
                if c == '<':
                    level += 1
                    toadd += c
                elif c == '>':
                    level -= 1
                    toadd += c
                elif c == ',':
                    if level == 0:
                        kvlist.append(toadd)
                        toadd = ''
                    else:
                        toadd += c
                elif c == ' ':
                    continue
                else:
                    toadd += c
            if toadd != '':
                kvlist.append(toadd)
            return kvlist

        # for bottom type
        if strtype == 'bot':
            return PyType(BottomType)
        if strtype == 'err':
            return PyType(ErrorType)
        # for vartypes
        if strtype.startswith('T') and strtype != 'TopType':
            vartype_patt = r'^T[_\?][a-zA-Z0-9_`\.]+$'
            if re.match(vartype_patt, strtype):
                # return PyType(VarType(strtype))
                return VarType(strtype)
                # return BType(VarType, varexp=strtype)
            raise RuntimeError('Vartype {} does not have a valid format'.format(strtype))
        # for simple types: int, str, float that eval to a type
        id_patt = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
        if re.match(id_patt, strtype):
            if strtype == NONE_TYPE:
                btip = type(None)
            else:
                btip = eval(strtype)
            if not type(btip) == type:
                raise RuntimeError('Type {} does not denote  a Python type'.format(strtype))
            return PyType(btip)
        # for containers: list[int, float, set[T_2, complex], bool] etc.
        container_patt = r'^([a-zA-Z_][a-zA-Z0-9_]*)\<([a-zA-Z0-9\+ ,_\<\?`\.\>]*)\>$'
        # container_patt = r'^([a-zA-Z_][a-zA-Z0-9_]*)\[([a-zA-Z0-9\{} _\{}\{}]+)\]$'.format(start_br, end_br, sep)
        foundlist = re.findall(container_patt, strtype)
        if len(foundlist) != 1:
            raise RuntimeError('Type {} does not represent a valid container type'.format(strtype))
        foundtuple = foundlist[0]

        btip = eval(foundtuple[0])
        if type(btip) is not type:
            raise RuntimeError('Type {} does not eval to a type type'.format(type))

        kvlist = get_kvlist(foundtuple[1])
        if len(kvlist) > 2:
            raise TypeError(f'Contained types {kvlist} is not supported.')
        # c_strtypes = Translator.get_types_from_list(foundtuple[1], start_br, end_br, sep)
        ll = []
        for strtip in kvlist:
            c_strtypes = Translator.get_types_from_list(strtip, start_br, end_br, sep)
            # c_types = hset()
            c_types = TypeExpression()
            for c_strtype in c_strtypes:
                newtip = Translator.translate_type(c_strtype, start_br, end_br, sep)
                c_types.add(newtip)
            ll.append(c_types)
        # c_types = frozenset(c_types)
        # newtype = PyType(btip, c_types)
        # print(newtype)
        return PyType(btip, *ll)

    @staticmethod
    def translate_te(str_te):
        # str_te_split = str_te.split('+')
        str_te = elim_paren(str_te)
        str_te_split = Translator.get_types_from_list(str_te, "<", ">", "+")
        te_typelist = []
        for cte_type in str_te_split:
            te_typelist.append(Translator.translate_type(cte_type, "<", ">", "+"))
        new_te = TypeExpression(te_typelist)
        return new_te

    @staticmethod
    def translate_basetype(str_basetype) -> Basetype:
        str_basetype = elim_paren(str_basetype)
        str_bt_split = Translator.get_types_from_list(str_basetype, "<", ">", "+")
        bt_typelist = []
        for cte_type in str_bt_split:
            bt_typelist.append(Translator.translate_type(cte_type, "<", ">", "+"))
        new_te = Basetype(bt_typelist)
        return new_te

    @staticmethod
    def translate_assignment(str_assignment: str) -> Assignment:
        # (a:bt_a /\ b:bt_b /\ ...)
        assig = Assignment()
        to_translate = Translator._elim_paren(str_assignment)
        str_entries = to_translate.split(r' /\ ')
        for str_entry in str_entries:
            expr, str_basetype = str_entry.split(':')
            assig[expr] = Translator.translate_basetype(str_basetype)
        return assig

    @staticmethod
    def translate_relation(str_relation: str) -> Relation:
        # (bt_1 <= bt_2)
        # (bt_1 == bt_2)
        to_translate = Translator._elim_paren(str_relation)
        # to_translate = str_relation
        found = False
        op = None
        for op in RelOp:
            if op.value in to_translate:
                found = True
                break
        if not found:
            raise RuntimeError(f'Operation for {to_translate} not supported')
        str_operands = to_translate.split(f' {op.value} ')
        bt_left = Translator.translate_basetype(str_operands[0])
        bt_right = Translator.translate_basetype(str_operands[1])
        return Relation(op, bt_left, bt_right)

    @staticmethod
    def translate_or_constraints(str_constraints: str) -> OrConstraints:
        # ((bt_1 <= bt 2) /\ (bt_3 == bt_4))
        or_constr = OrConstraints()
        to_translate = Translator._elim_paren(str_constraints)
        str_entries = to_translate.split(r' \/ ')
        for str_relation in str_entries:
            rel = Translator.translate_relation(str_relation)
            or_constr.add(rel)
        return or_constr

    @staticmethod
    def translate_and_constraints(str_constraints: str) -> AndConstraints:
        # ((bt_1 <= bt 2) /\ (bt_3 == bt_4))
        and_constr = AndConstraints()
        to_translate = Translator._elim_paren(str_constraints)
        str_entries = to_translate.split(r' /\ ')
        for str_relation in str_entries:
            rel = Translator.translate_relation(str_relation)
            and_constr.add(rel)
        return and_constr

    @staticmethod
    def translate_state(str_state: str) -> State:
        # (assignment ^ constraints)
        delimiter = ' ^ '
        to_translate = Translator._elim_paren(str_state)
        str_assignment = None
        str_constraints = None
        if delimiter not in to_translate:
            str_assignment = to_translate
        else:
            (str_assignment, str_constraints) = to_translate.split(delimiter)
        asgn = Translator.translate_assignment(str_assignment)
        if str_constraints is not None:
            constr = Translator.translate_and_constraints(str_constraints)
        else:
            constr = None
        st = State(asgn, constr)
        return st

    @staticmethod
    def translate_state_set(str_set: str) -> StateSet:
        delimiter = r' \/ '
        to_translate = str_set
        str_states = to_translate.split(delimiter)
        state_set = StateSet()
        for str_state in str_states:
            state = Translator.translate_state(str_state)
            state_set.add(state)
        return state_set

    @staticmethod
    def translate_func_spec(str_spec: str) -> FuncSpec:
        funcspec = FuncSpec()
        delimiter = r' -> '
        to_translate = Translator._elim_paren(str_spec)
        (str_in, str_out) = to_translate.split(delimiter)
        funcspec._in = Translator.translate_state(str_in)
        funcspec._out = Translator.translate_state(str_out)
        return funcspec

    @staticmethod
    def translate_va(str_va):
        va = VarAssign()
        str_entries = str_va.split(r' /\ ')
        for str_entry in str_entries:
            varname, str_vtype = str_entry.split(':')
            if varname in va:
                raise RuntimeError('Multiple values for the same VarAssign key {}'.format(varname))
            va[varname] = Translator.translate_type(str_vtype)
        return va

    @staticmethod
    def translate_ctx(str_ctx):
        ctx = Context()
        str_entries = str_ctx.split(r' /\ ')
        for str_entry in str_entries:
            str_vartype, str_te = str_entry.split(':')
            vt = Translator.translate_type(str_vartype)
            te = Translator.translate_te(str_te)
            try:
                ctx[vt]
            except KeyError:
                ctx[vt] = hset()
            ctx[vt].add(te)
        return ctx

    @staticmethod
    def translate_tc(str_tc):
        tc = TypeConstraint()
        if str_tc == '' or str_tc == '()':
            return tc
        str_elems = str_tc.split(r' \/ ')
        for str_elem in str_elems:
            str_elem = elim_paren(str_elem)
            tdict = Translator.translate_ctx(str_elem)
            tc.add(tdict)
        return tc

    @staticmethod
    def translate_as(str_as):
        # a:Ta /\ b:Tb ^ ((Ta:int /\ Tb:int+float) \/ (Ta:str /\ Tb:str))
        if r'^' not in str_as:
            (str_va, str_tc) = (str_as, '')
        else:
            (str_va, str_tc) = str_as.split(r' ^ ')
        va = Translator.translate_va(str_va)
        tc = Translator.translate_tc(str_tc)
        return AbsState(va, tc)
