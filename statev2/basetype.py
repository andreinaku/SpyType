from __future__ import annotations
from utils import *
from enum import Enum
from copy import deepcopy


class RelOp(Enum):
    LEQ = '<='
    EQ = '=='


def generate_id(state):
    retstr = f'T{state.gen_id}'
    state.gen_id = state.gen_id + 1
    return retstr


class GenericType:
    pass


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
        if self.constraints is None:
            retstr = f'({self.assignment})'
        else:
            retstr = f'({self.assignment}) ^ ({self.constraints})'
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.assignment, self.constraints))

    def __eq__(self, other: State):
        return hash(self) == hash(other)


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
        return f'({self.in_state}) -> ({self.out_state})'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.in_state, self.out_state))

    def __eq__(self, other: FuncSpec):
        return hash(self) == hash(other)
