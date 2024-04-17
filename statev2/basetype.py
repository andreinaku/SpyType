from __future__ import annotations
from utils.utils import *
from enum import Enum
from copy import deepcopy
from statev2.supported_types import is_supported_type, builtin_types, builtin_seqs, builtin_dicts, builtins


class RelOp(Enum):
    LEQ = '<='
    EQ = '=='


def generate_id(state):
    retstr = f'T{state.gen_id}'
    state.gen_id = state.gen_id + 1
    return retstr


class GenericType:
    pass


def get_builtin_basetype(ptip: PyType) -> Basetype:
    new_bt = Basetype()
    if isinstance(ptip, VarType):
        new_bt.add(deepcopy(ptip))
        return new_bt
    for blist in builtins:
        if ptip.ptype in blist:
            # if it is already a builtin type, just add it
            # only protocol are replaced
            new_bt.add(deepcopy(ptip))
            return new_bt
    for btype in builtin_types:
        try:
            if issubclass(btype, ptip.ptype):
                new_bt.add(PyType(btype))
        except TypeError:
            continue
    for btype in builtin_seqs:
        try:
            if issubclass(btype, ptip.ptype):
                new_bt.add(PyType(btype, Basetype({PyType(TopType)})))
        except TypeError as te:
            continue
    for btype in builtin_dicts:
        try:
            if issubclass(btype, ptip.ptype):
                new_bt.add(PyType(btype, Basetype({PyType(TopType)}), Basetype({PyType(TopType)})))
        except TypeError:
            continue
    if len(new_bt) == 0:
        new_bt.add(deepcopy(ptip))
    return new_bt


class PyType(GenericType):
    def __init__(self, ptype, keys=None, values=None):
        self.ptype = deepcopy(ptype)
        self.keys = deepcopy(keys)
        self.values = deepcopy(values)
        if (ptype in container_ptypes) and (self.keys is None):
            self.keys = Basetype()
        if (ptype in mapping_types) and (self.keys is None) and (self.values is None):
            self.keys = Basetype()
            self.values = Basetype()

    def __str__(self):
        if self.ptype == BottomType:
            retstr = 'bot'
        elif self.ptype == TopType:
            retstr = 'top'
        elif self.ptype == ErrorType:
            retstr = 'err'
        elif isinstance(self.ptype, VarType):
            retstr = self.ptype.varexp
        else:
            # retstr = str(self.ptype).split("'")[1]
            retstr = self.ptype.__name__
        if self.keys is not None:
            retstr += '< '
            # for c_type in self.contains:
            #     retstr += str(c_type) + ','
            retstr += str(self.keys)
            if self.values is not None:
                retstr += ', '
                retstr += str(self.values)
            retstr += ' >'
        return retstr

    def __key(self):
        return self.ptype, self.keys, self.values

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return self.__str__()


class VarType(GenericType):
    def __init__(self, varexp: str):
        self.varexp = varexp

    def __str__(self):
        return self.varexp

    def __repr__(self):
        return self.__str__()

    def __key(self):
        return self.varexp

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return hash(self) == hash(other)


class Basetype(hset):
    def __str__(self):
        retstr = ''
        for elem in self.__iter__():
            retstr += str(elem) + ' + '
        retstr = retstr[:-3]
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return super().__hash__()

    def replace_vartype(self, to_replace: str, replace_with: str) -> Basetype:
        new_bt = Basetype()
        for tip in self:
            if isinstance(tip, VarType):
                if tip.varexp == to_replace:
                    new_tip = VarType(replace_with)
                    new_bt.add(new_tip)
                else:
                    new_bt.add(deepcopy(tip))
            elif isinstance(tip, PyType):
                if tip.ptype not in container_ptypes and tip.ptype not in mapping_types:
                    new_bt.add(deepcopy(tip))
                elif tip.ptype in mapping_types:
                    new_keys = tip.keys.replace_vartype(to_replace, replace_with)
                    new_values = tip.values.replace_vartype(to_replace, replace_with)
                    newtip = PyType(tip.ptype, keys=new_keys, values=new_values)
                    new_bt.add(newtip)
                elif tip.ptype in container_ptypes:
                    new_keys = tip.keys.replace_vartype(to_replace, replace_with)
                    newtip = PyType(tip.ptype, keys=new_keys)
                    new_bt.add(newtip)
                else:
                    raise RuntimeError(f'What base type is this? f{tip.ptype}')
            else:
                raise RuntimeError(f'What type is this inside my basetype? {tip}')
        return new_bt

    def filter_pytypes(self, supported_list: list[type]) -> Basetype | None:
        new_bt = Basetype()
        if self is None:
            return None
        for tip in self:
            if isinstance(tip, VarType):
                new_bt.add(tip)
                continue
            elif isinstance(tip, PyType):
                # if tip.ptype not in supported_list:
                #     continue
                if not is_supported_type(tip.ptype):
                    continue
                new_keys = tip.keys.filter_pytypes(supported_list) if tip.keys is not None else None
                new_values = tip.values.filter_pytypes(supported_list) if tip.values is not None else None
                new_ptip = PyType(tip.ptype,
                                  keys=new_keys,
                                  values=new_values
                                  )
                new_bt.add(new_ptip)
            else:
                raise RuntimeError(f'This is not a supported element of Basetype: {tip}')
        return new_bt


class Assignment(hdict):
    def __str__(self):
        if len(self.items()) == 0:
            return ''
        retstr = ''
        for expr, btype in self.items():
            retstr += f'{expr}:{btype} /\\ '
        retstr = retstr[:-4]
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return super().__hash__()

    def replace_vartype(self, to_replace: str, replace_with: str) -> Assignment:
        new_assignment = Assignment()
        expr: str
        bt: Basetype
        for expr, bt in self.items():
            new_bt = bt.replace_vartype(to_replace, replace_with)
            new_assignment[expr] = new_bt
        return new_assignment

    def filter_pytypes(self, supported_list: list[type]) -> Assignment:
        new_assignment = Assignment()
        expr: str
        bt: Basetype
        for expr, bt in self.items():
            new_bt = bt.filter_pytypes(supported_list)
            new_assignment[expr] = new_bt
        return new_assignment


class Relation:
    def __init__(self, relop: RelOp, bt_left: Basetype, bt_right: Basetype):
        self.relop = relop
        self.bt_left = deepcopy(bt_left)
        self.bt_right = deepcopy(bt_right)

    def __str__(self):
        if self.relop == RelOp.LEQ:
            relstr = '<='
        elif self.relop == RelOp.EQ:
            relstr = '=='
        else:
            raise RuntimeError('Unsupported relation op')
        return f'{self.bt_left} {relstr} {self.bt_right}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: Relation):
        if self.relop.value == other.relop.value and self.bt_left == other.bt_left and self.bt_right == other.bt_right:
            return True
        return False

    def __hash__(self):
        # return -1
        return hash((self.bt_left, self.relop.value, self.bt_right))

    def replace_vartype(self, to_replace: str, replace_with: str) -> Relation:
        new_bt_left = self.bt_left.replace_vartype(to_replace, replace_with)
        new_bt_right = self.bt_right.replace_vartype(to_replace, replace_with)
        new_rel = Relation(self.relop, new_bt_left, new_bt_right)
        return new_rel

    def filter_pytypes(self, supported_list: list[type]) -> Relation:
        new_bt_left = self.bt_left.filter_pytypes(supported_list)
        new_bt_right = self.bt_right.filter_pytypes(supported_list)
        new_rel = Relation(self.relop, new_bt_left, new_bt_right)
        return new_rel


class AndConstraints(hset):
    def __str__(self):
        if len(self) == 0:
            return ''
        retstr = ''
        if not len(self):
            return retstr
        for rel in self:
            retstr += f'({rel}) /\\ '
        retstr = retstr[:-4]
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return super().__hash__()

    def replace_vartype(self, to_replace: str, replace_with: str) -> AndConstraints:
        new_andconstr = AndConstraints()
        rel: Relation
        for rel in self:
            new_rel = rel.replace_vartype(to_replace, replace_with)
            new_andconstr.add(new_rel)
        return new_andconstr

    def filter_pytypes(self, supported_list: list[type]) -> AndConstraints:
        new_andconstr = AndConstraints()
        rel: Relation
        for rel in self:
            new_rel = rel.filter_pytypes(supported_list)
            new_andconstr.add(new_rel)
        return new_andconstr


class OrConstraints(hset):
    def __str__(self):
        if len(self) == 0:
            return ''
        retstr = ''
        if not len(self):
            return retstr
        for rel in self:
            retstr += f'{rel} \\/ '
        retstr = retstr[:-4]
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return super().__hash__()


class State:
    def __init__(self, assignment: Assignment = None, constraints: AndConstraints = None):
        self.gen_id = 1
        if assignment is None:
            self.assignment = Assignment()
        else:
            self.assignment = deepcopy(assignment)
        if constraints is None:
            self.constraints = AndConstraints()
        else:
            self.constraints = deepcopy(constraints)

    def __str__(self):
        if len(self.constraints) == 0:
            retstr = f'({self.assignment})'
        else:
            retstr = f'({self.assignment}) ^ ({self.constraints})'
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((hash(self.assignment), hash(self.constraints)))

    def __eq__(self, other: State):
        return hash(self) == hash(other)

    def replace_vartype(self, to_replace: str, replace_with: str) -> State:
        new_assignment = self.assignment.replace_vartype(to_replace, replace_with)
        new_constraints = self.constraints.replace_vartype(to_replace, replace_with)
        new_state = State(new_assignment, new_constraints)
        return new_state

    def filter_pytypes(self, supported_list: list[type]) -> State:
        new_assignment = self.assignment.filter_pytypes(supported_list)
        new_constraints = self.constraints.filter_pytypes(supported_list)
        new_state = State(new_assignment, new_constraints)
        return new_state


class StateSet(hset):
    def __str__(self):
        if len(self) == 0:
            return '()'
        retstr = ''
        for state in self:
            retstr += rf'{state} \/ '
        retstr = retstr[0:-4]
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return super().__hash__()

    def replace_vartype(self, to_replace: str, replace_with: str) -> StateSet:
        new_state_set = StateSet()
        st: State
        for st in self:
            new_state = st.replace_vartype(to_replace, replace_with)
            new_state_set.add(new_state)
        return new_state_set

    def filter_pytypes(self, supported_list: list[type]) -> StateSet:
        new_state_set = StateSet()
        st: State
        for st in self:
            new_state = st.filter_pytypes(supported_list)
            new_state_set.add(new_state)
        return new_state_set


class FuncSpec:
    def __init__(self, _in: State = None, _out: State = None):
        if not _in:
            self.in_state = State()
        else:
            self.in_state = deepcopy(_in)
        if not _out:
            self.out_state = State()
        else:
            self.out_state = deepcopy(_out)

    def __str__(self):
        return f'({self.in_state} -> {self.out_state})'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((hash(self.in_state), hash(self.out_state)))

    def __eq__(self, other: FuncSpec):
        return hash(self) == hash(other)

    def replace_vartype(self, to_replace: str, replace_with: str):
        new_in = self.in_state.replace_vartype(to_replace, replace_with)
        new_out = self.out_state.replace_vartype(to_replace, replace_with)
        new_funcspec = FuncSpec(new_in, new_out)
        return new_funcspec

    def filter_pytypes(self, supported_list: list[type]) -> FuncSpec:
        new_in = self.in_state.filter_pytypes(supported_list)
        new_out = self.out_state.filter_pytypes(supported_list)
        new_funcspec = FuncSpec(new_in, new_out)
        return new_funcspec
