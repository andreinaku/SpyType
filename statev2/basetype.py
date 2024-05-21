from __future__ import annotations
from utils.utils import *
from enum import Enum
from copy import deepcopy
from statev2.supported_types import is_supported_type, builtin_types, builtin_seqs, builtin_dicts, builtins


class RelOp(Enum):
    LEQ = '<='
    EQ = '=='


class GenericType:
    pass


# def get_builtin_from_pytype(ptip: PyType) -> Basetype:
#     new_bt = Basetype()
#     if isinstance(ptip, VarType):
#         new_bt.add(deepcopy(ptip))
#         return new_bt
#     for blist in builtins:
#         if ptip.ptype in blist:
#             # if it is already a builtin type, just add it
#             # only Protocols are replaced
#             new_bt.add(deepcopy(ptip))
#             return new_bt
#     if ptip.keys is None or ptip.keys == Basetype({PyType(TopType)}):
#         for btype in builtin_types:
#             try:
#                 if issubclass(btype, ptip.ptype):
#                     new_bt.add(PyType(btype))
#             except TypeError:
#                 continue
#     if (ptip.keys is not None and ptip.values is None) or (ptip.keys is None and ptip.values is None):
#         for btype in builtin_seqs:
#             contained_keys = Basetype({PyType(TopType)})
#             if ptip.keys is not None and len(ptip.keys) != 0:
#                 if len(ptip.keys) == 1:
#                     # contained_keys = deepcopy(ptip.keys)
#                     contained_keys = get_builtin_from_bt(ptip.keys)
#                 else:
#                     raise TypeError(f'We do not support {ptip} substitution yet')
#             try:
#                 if issubclass(btype, ptip.ptype):
#                     new_bt.add(PyType(btype, contained_keys))
#             except TypeError as te:
#                 continue
#     if (ptip.keys is not None and ptip.values is not None) or (ptip.keys is None and ptip.values is None):
#         for btype in builtin_dicts:
#             contained_keys = Basetype({PyType(TopType)})
#             contained_values = Basetype({PyType(TopType)})
#             if (ptip.keys is not None and len(ptip.keys) != 0) and (ptip.values is not None and len(ptip.values) != 0):
#                 if len(ptip.keys) == 1 and len(ptip.values) == 1:
#                     contained_keys = deepcopy(ptip.keys)
#                     contained_values = deepcopy(ptip.values)
#                 else:
#                     raise TypeError(f'We do not support {ptip} substitution yet')
#             try:
#                 if issubclass(btype, ptip.ptype):
#                     new_bt.add(PyType(btype, contained_keys, contained_values))
#             except TypeError:
#                 continue
#     if len(new_bt) == 0:
#         new_bt.add(deepcopy(ptip))
#     return new_bt


# def get_builtin_from_bt(bt: Basetype) -> Basetype:
#     new_bt = Basetype()
#     for ptip in bt:
#         if not isinstance(ptip, PyType):
#             if not isinstance(ptip, VarType):
#                 raise RuntimeError(f'Type not supported: {ptip}')
#             new_bt.add(ptip)
#             continue
#         new_bt |= get_builtin_from_pytype(ptip)
#     return new_bt


class PyType(GenericType):
    def __init__(self, ptype, keys=None, values=None):
        self.ptype = deepcopy(ptype)
        self.keys = deepcopy(keys)
        self.values = deepcopy(values)
        # if (ptype in container_ptypes) and (self.keys is None):
        #     self.keys = Basetype()
        # if (ptype in mapping_types) and (self.keys is None) and (self.values is None):
        #     self.keys = Basetype()
        #     self.values = Basetype()

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
        # if self.keys is not None:
        # if self.ptype in container_ptypes:
        if self.keys is not None and len(self.keys) > 0 and self.values is None:
            retstr += '< '
            # for c_type in self.contains:
            #     retstr += str(c_type) + ','
            retstr += str(self.keys)
            # if self.values is not None:
            #     retstr += ', '
            #     retstr += str(self.values)
            retstr += ' >'
        elif self.keys is not None and len(self.keys) > 0 and self.values is not None and len(self.values) > 0:
            retstr += '< '
            retstr += str(self.keys)
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
    
    def get_builtin_from_pytype(self) -> Basetype:
        new_bt = Basetype()
        if isinstance(self, VarType):
            new_bt.add(deepcopy(self))
            return new_bt
        for blist in builtins:
            if self.ptype in blist:
                # if it is already a builtin type, just add it
                # only Protocols are replaced
                new_bt.add(deepcopy(self))
                return new_bt
        if self.keys is None or self.keys == Basetype({PyType(TopType)}):
            for btype in builtin_types:
                try:
                    if issubclass(btype, self.ptype):
                        new_bt.add(PyType(btype))
                except TypeError:
                    continue
        if (self.keys is not None and self.values is None) or (self.keys is None and self.values is None):
            for btype in builtin_seqs:
                contained_keys = Basetype({PyType(TopType)})
                if self.keys is not None and len(self.keys) != 0:
                    if len(self.keys) == 1:
                        # contained_keys = deepcopy(ptip.keys)
                        # contained_keys = self.get_builtin_from_bt(ptip.keys)
                        contained_keys = self.keys.get_builtin_from_bt()
                    else:
                        raise TypeError(f'We do not support {self} substitution yet')
                try:
                    if issubclass(btype, self.ptype):
                        new_bt.add(PyType(btype, contained_keys))
                except TypeError as te:
                    continue
        if (self.keys is not None and self.values is not None) or (self.keys is None and self.values is None):
            for btype in builtin_dicts:
                contained_keys = Basetype({PyType(TopType)})
                contained_values = Basetype({PyType(TopType)})
                if (self.keys is not None and len(self.keys) != 0) and (self.values is not None and len(self.values) != 0):
                    if len(self.keys) == 1 and len(self.values) == 1:
                        contained_keys = deepcopy(self.keys)
                        contained_values = deepcopy(self.values)
                    else:
                        raise TypeError(f'We do not support {self} substitution yet')
                try:
                    if issubclass(btype, self.ptype):
                        new_bt.add(PyType(btype, contained_keys, contained_values))
                except TypeError:
                    continue
        if len(new_bt) == 0:
            new_bt.add(deepcopy(self))
        return new_bt


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
                # if tip.ptype not in container_ptypes and tip.ptype not in mapping_types:
                if tip.keys is None and tip.values is None:
                    new_bt.add(deepcopy(tip))
                # elif tip.ptype in mapping_types:
                elif tip.keys is not None and tip.values is not None:
                    new_keys = tip.keys.replace_vartype(to_replace, replace_with)
                    new_values = tip.values.replace_vartype(to_replace, replace_with)
                    newtip = PyType(tip.ptype, keys=new_keys, values=new_values)
                    new_bt.add(newtip)
                # elif tip.ptype in container_ptypes:
                elif tip.keys is not None:
                    new_keys = tip.keys.replace_vartype(to_replace, replace_with)
                    newtip = PyType(tip.ptype, keys=new_keys)
                    new_bt.add(newtip)
                else:
                    raise RuntimeError(f'What base type is this? f{tip.ptype}')
            else:
                raise RuntimeError(f'What type is this inside my basetype? {tip}')
        return new_bt

    def replace_vartype_with_basetype(self, to_replace: str, replace_with: Basetype) -> Basetype:
        new_bt = Basetype()
        for tip in self:
            if isinstance(tip, VarType):
                if tip.varexp == to_replace:
                    new_bt |= deepcopy(replace_with)
                else:
                    new_bt.add(deepcopy(tip))
            elif isinstance(tip, PyType):
                # if tip.ptype not in container_ptypes and tip.ptype not in mapping_types:
                if tip.keys is None and tip.values is None:
                    new_bt.add(deepcopy(tip))
                # elif tip.ptype in mapping_types:
                elif tip.keys is not None and tip.values is not None:
                    new_keys = tip.keys.replace_vartype_with_basetype(to_replace, replace_with)
                    new_values = tip.values.replace_vartype_with_basetype(to_replace, replace_with)
                    newtip = PyType(tip.ptype, keys=new_keys, values=new_values)
                    new_bt.add(newtip)
                # elif tip.ptype in container_ptypes:
                elif tip.keys is not None:
                    new_keys = tip.keys.replace_vartype_with_basetype(to_replace, replace_with)
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
    
    def get_builtin_from_bt(self) -> Basetype:
        new_bt = Basetype()
        for ptip in self:
            if not isinstance(ptip, PyType):
                if not isinstance(ptip, VarType):
                    raise RuntimeError(f'Type not supported: {ptip}')
                new_bt.add(ptip)
                continue
            new_bt |= ptip.get_builtin_from_pytype()
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
    
    def replace_superclasses(self) -> Assignment:
        new_assignment = Assignment()
        expr: str
        bt: Basetype
        for expr, bt in self.items():
            new_bt = bt.get_builtin_from_bt()
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

    def replace_superclasses(self) -> Relation:
        new_bt_left = self.bt_left.get_builtin_from_bt()
        new_bt_right = self.bt_right.get_builtin_from_bt()
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

    def replace_superclasses(self) -> AndConstraints:
        new_andconstr = AndConstraints()
        rel: Relation
        for rel in self:
            new_rel = rel.replace_superclasses()
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
    
    def replace_superclasses(self) -> State:
        new_assignment = self.assignment.replace_superclasses()
        new_constraints = self.constraints.replace_superclasses()
        new_state = State(new_assignment, new_constraints)
        return new_state

    def generate_id(self):
        retstr = f'T{self.gen_id}'
        self.gen_id = self.gen_id + 1
        return retstr


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
    
    def replace_superclasses(self) -> StateSet:
        new_state_set = StateSet()
        st: State
        for st in self:
            new_state = st.replace_superclasses()
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
    
    def replace_superclasses(self) -> FuncSpec:
        new_in = self.in_state.replace_superclasses()
        new_out = self.out_state.replace_superclasses()
        new_funcspec = FuncSpec(new_in, new_out)
        return new_funcspec


# for later use, sequences with implicit types contained
extra_sequences = {
    PyType(range):      Basetype({PyType(int)}),
    PyType(str):        Basetype({PyType(str)}),
    PyType(bytes):      Basetype({PyType(int)}),
    PyType(bytearray):  Basetype({PyType(int)}),
    PyType(memoryview): Basetype({PyType(int)})
}
