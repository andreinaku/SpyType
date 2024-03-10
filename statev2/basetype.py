from __future__ import annotations
from utils import *
from enum import Enum
import time
from copy import deepcopy
from TypeExp import *


ID_NUMBER = 1


class RelOp(Enum):
    LEQ = '<='
    EQ = '=='


def generate_id():
    global ID_NUMBER
    retstr = f'T_{ID_NUMBER}'
    ID_NUMBER = ID_NUMBER + 1
    return retstr


class Basetype(hset):
    def __str__(self):
        retstr = ''
        for elem in self.__iter__():
            retstr += str(elem) + '+'
        retstr = retstr[:-1]
        return retstr

    def __repr__(self):
        return self.__str__()

    def __or__(self, other):
        return Basetype(super(Basetype, self).__or__(other))

    def has_vartype(self, vtip: VarType):
        for pt in self:
            if not isinstance(pt, VarType):
                continue
            if vtip == pt:
                return True
        return False

    def has_pytype(self, ptip: PyType):
        for pt in self:
            if not isinstance(pt, PyType):
                continue
            if ptip.ptype == pt.ptype:
                return True
        return False

    def has_tip(self, tip):
        if isinstance(tip, VarType):
            return self.has_vartype(tip)
        return self.has_pytype(tip)

    def add_to_tip(self, ptip, newcontains):
        newte = Basetype()
        if not isinstance(ptip, PyType):
            raise RuntimeError('Why?')
        if ptip.ptype not in container_ptypes:
            raise RuntimeError('How??')
        for tip in self:
            if tip.ptype != ptip.ptype:
                newte.add(tip)
                continue
            newtip = PyType(ptype=tip.ptype, keys=tip.keys + newcontains)
            newte.add(newtip)
        return Basetype(newte)

    def __add__(self, other):
        newte = deepcopy(self)
        for tip in other:
            if isinstance(tip, VarType):
                newte.add(tip)
                continue
            elif tip.ptype not in container_ptypes:
                newte.add(tip)
                continue
            elif not newte.has_pytype(tip):
                newte.add(tip)
                continue
            else:
                for ctype in newte:
                    if isinstance(ctype, PyType) and tip.ptype == ctype.ptype:
                        break
                ctype.keys = deepcopy(ctype.keys) + deepcopy(tip.keys)
        return Basetype(newte)

    def __and__(self, other):
        new_te = Basetype()
        p1: PyType
        p2: PyType
        for p1 in self:
            for p2 in other:
                pinter = p1 & p2
                if pinter is None:
                    continue
                new_te.add(pinter)
        if len(new_te) == 0:
            return None
        new_new_te = Basetype()
        new_vartype = PyType(VarType('T_{}'.format(id_generator())))
        new_vartype = VarType('T_{}'.format(id_generator()))
        for tip in new_te:
            if isinstance(tip, VarType):
                new_new_te.add(new_vartype)
            else:
                new_new_te.add(tip)
        return new_new_te
        # return new_te

    def get_all_vartypes(self) -> hset[VarType]:
        vtypes = hset()
        ptip: PyType
        for ptip in self:
            if isinstance(ptip, VarType):
                vtypes.add(ptip)
                continue
            if ptip.keys is None or len(ptip.keys) == 0:
                continue
            contained_te = ptip.keys
            vtypes |= contained_te.get_all_vartypes()
        return vtypes

    def vartype_replace_all(self, old_vtype: VarType, new_vtype: VarType):
        newte = Basetype()
        for ptip in self:
            if isinstance(ptip, VarType):
                ptip: VarType
                if ptip != old_vtype:
                    newte.add(deepcopy(ptip))
                    continue
                newte.add(deepcopy(new_vtype))
                continue
            ptip: PyType
            if ptip.keys is None or len(ptip.keys) == 0:
                new_keys = None
            else:
                new_keys = ptip.keys.vartype_replace_all(old_vtype, new_vtype)
            if ptip.values is None or len(ptip.values) == 0:
                new_values = None
            else:
                new_values = ptip.values.vartype_replace_all(old_vtype, new_vtype)
            newptip = PyType(ptip.ptype, new_keys, new_values)
            newte.add(newptip)
        return newte

    @staticmethod
    def glb(te1, te2):
        te1: Basetype
        te2: Basetype
        newte = Basetype()
        if not te1.contains_any_vartype() and not te2.contains_any_vartype():
            for tip1 in te1:
                for tip2 in te2:
                    newtip = PyType.glb(tip1, tip2)
                    if newtip is None:
                        continue
                    newte.add(newtip)
        return newte

    def is_spectype(self):
        if len(self) != 1:
            return False
        for tip in self:
            if isinstance(tip, VarType) and SPECTYPE_MARKER in tip.varexp:
                return True
        return False

    def is_vartype(self):
        if len(self) != 1:
            return False
        for tip in self:
            if isinstance(tip, VarType):
                return True
        return False

    def replace_vartype(self, repl):
        repl: hdict[VarType, Basetype]
        newte = Basetype()
        if len(repl) == 0:
            return deepcopy(self)
        for tip in self:
            if isinstance(tip, VarType) and tip in repl:
                newte = newte + repl[tip]
                continue
            if isinstance(tip, PyType) and tip.keys is not None:
                newtip = PyType(ptype=tip.ptype)
                newtip.keys = tip.keys.replace_vartype(repl)
                newte.add(newtip)
                continue
            newte.add(tip)
        return newte

    def is_single_container(self):
        if len(self) != 1:
            return False
        # tip: PyType
        tip = self[0]
        if not isinstance(tip, PyType):
            return False
        if tip.keys is None:
            return False
        return True

    def is_single_vartype(self):
        if len(self) != 1:
            return False
        tip = self[0]
        if not isinstance(tip, VarType):
            return False
        if SPECTYPE_MARKER in tip.varexp:
            return False
        return True

    # @staticmethod
    # def get_spectype_repl(te1, te2, vi_types: hset):
    #     te1: Basetype
    #     te2: Basetype
    #     ctx = CtxReplace()
    #     if te1.is_single_container() and te2.is_single_container():
    #         if te1[0].ptype == te2[0].ptype:
    #             return Basetype.get_spectype_repl(te1[0].keys, te2[0].keys, vi_types)
    #     if te1.is_spectype() and not te2.is_spectype():
    #         specte = te1
    #         otherte = te2
    #     elif not te1.is_spectype() and te2.is_spectype():
    #         specte = te2
    #         otherte = te1
    #     else:
    #         return ctx
    #     spectype = specte[0]
    #     if spectype in vi_types:
    #         ctx.te_repl[otherte] = deepcopy(specte)
    #         return ctx
    #     ctx.spec_repl[spectype] = deepcopy(otherte)
    #     return ctx

    def contains_vartype(self, vtype: VarType):
        for ptip in self:
            if isinstance(ptip, VarType):
                if ptip == vtype:
                    return True
                continue
            if ptip.keys is not None and len(ptip.keys) > 0:
                return ptip.keys.contains_vartype(vtype)
        return False

    def contains_any_vartype(self):
        for ptip in self:
            if isinstance(ptip, VarType):
                return True
            if ptip.keys is not None and len(ptip.keys) > 0:
                return ptip.keys.contains_any_vartype()
        return False

    def old_replace_te(self, to_replace, replace_with):
        to_replace: Basetype
        replace_with: Basetype
        if to_replace not in self:
            return deepcopy(self)
        if to_replace <= self:
            dif = self - to_replace
            newte = dif | replace_with
            return Basetype(newte)
        newte = Basetype()
        for t in self:
            if not isinstance(t, PyType):
                newte.add(deepcopy(t))
                continue
            if t.keys is None or len(t.keys) == 0:
                newte.add(deepcopy(t))
                continue
            newtip = PyType(ptype=t.ptype)
            newtip.keys = t.keys.old_replace_te(to_replace, replace_with)
            newte.add(newtip)
        return newte

    def get_level(self):
        lvset = set()
        for t in self:
            if isinstance(t, VarType):
                lvset.add(t)
                continue
            lvset.add(PyType(t.ptype))
        return lvset

    def get_by_type(self, _t):
        for t in self:
            if isinstance(t, VarType):
                continue
            if t.ptype == _t:
                return t
        return None

    def get_pytypes(self):
        pytypes = set()
        for t in self:
            if isinstance(t, PyType):
                pytypes.add(t.ptype)
        return pytypes

    def comparable(self: Basetype, other: Basetype, sign=None):
        lv1 = self.get_level()
        lv2 = other.get_level()
        if lv1 <= lv2:
            sign2 = SIGN_LE
        elif lv1 > lv2:
            sign2 = SIGN_GT
        else:
            return False
        if sign is not None and sign != sign2:
            return False
        # go to the next levels
        for t1 in self:
            if isinstance(t1, VarType):
                continue
            if not t1.keys:
                continue
            t2 = other.get_by_type(t1.ptype)
            te1 = t1.keys
            te2 = t2.keys
            if not te1.comparable(te2, sign2):
                return False
        return True

    def old_comparable(self, other, sign=None):
        # compare first levels
        lv1 = self.get_level()
        lv2 = other.get_level()
        has_vartype1 = any(isinstance(t, VarType) for t in lv1)
        has_vartype2 = any(isinstance(t, VarType) for t in lv2)
        if has_vartype1 and has_vartype2:
            ptypes1 = self.get_pytypes()
            ptypes2 = other.get_pytypes()
            if not ptypes1 and not ptypes2:
                sign2 = SIGN_LE
            elif ptypes1 >= ptypes2:
                sign2 = SIGN_LE
            else:
                sign2 = SIGN_GT
        elif has_vartype1:
            sign2 = SIGN_GT
        elif has_vartype2:
            sign2 = SIGN_LE
        else:
            if not lv1 <= lv2 and not lv1 > lv2:
                return False
            sign2 = SIGN_LE if lv1 <= lv2 else SIGN_GT
        # check if signs are consistent
        if sign is not None and sign != sign2:
            return False
        # go to the next levels
        for t1 in self:
            if isinstance(t1, VarType):
                continue
            if not t1.keys:
                continue
            t2 = other.get_by_type(t1.ptype)
            te1 = t1.keys
            te2 = t2.keys
            if not te1.comparable(te2, sign2):
                return False
        return True

    def __le__(self, other):
        if not self.comparable(other):
            return False
            # raise RuntimeError('Cannot compare types')
        lv1 = self.get_level()
        lv2 = other.get_level()
        return lv1 <= lv2

    def old__le__(self, other):
        if not self.comparable(other):
            return False
            # raise RuntimeError('Cannot compare types')
        lv1 = self.get_level()
        lv2 = other.get_level()
        has_vartype1 = any(isinstance(t, VarType) for t in lv1)
        has_vartype2 = any(isinstance(t, VarType) for t in lv2)
        if self == other:
            sign2 = SIGN_LE
        elif has_vartype1 and has_vartype2:
            ptypes1 = self.get_pytypes()
            ptypes2 = other.get_pytypes()
            if not ptypes1 and not ptypes2:
                sign2 = SIGN_LE
            elif ptypes1 > ptypes2:
                sign2 = SIGN_LE
            else:
                sign2 = SIGN_GT
        elif has_vartype1:
            sign2 = SIGN_GT
        elif has_vartype2:
            sign2 = SIGN_LE
        else:
            if not lv1 <= lv2 and not lv1 > lv2:
                return False
            sign2 = SIGN_LE if lv1 <= lv2 else SIGN_GT
        if sign2 == SIGN_LE:
            return True
        return False

    def __eq__(self, other):
        if not self.comparable(other):
            return False
            # raise RuntimeError('Cannot compare types')
        lv1 = self.get_level()
        lv2 = other.get_level()
        if lv1 != lv2:
            return False
        # go to the next levels
        for t1 in self:
            if isinstance(t1, VarType):
                continue
            if not t1.keys:
                continue
            t2 = other.get_by_type(t1.ptype)
            te1 = t1.keys
            te2 = t2.keys
            if te1 != te2:
                return False
        return True

    def old__eq__(self, other):
        if not self.comparable(other):
            return False
            # raise RuntimeError('Cannot compare types')
        lv1 = self.get_level()
        lv2 = other.get_level()
        has_vartype1 = any(isinstance(t, VarType) for t in lv1)
        has_vartype2 = any(isinstance(t, VarType) for t in lv2)
        if (has_vartype1 and has_vartype2) or (not has_vartype1 and not has_vartype2):
            ptypes1 = self.get_pytypes()
            ptypes2 = other.get_pytypes()
            if ptypes1 != ptypes2:
                return False
        else:
            return False
        return True

    def __hash__(self):
        return super().__hash__()

    # def __contains__(self, item):
    #     item: Basetype
    #     if item <= self:
    #         return True
    #     for t1 in item:
    #         found = False
    #         for t2 in self:
    #             if t1 in t2:
    #                 found = True
    #                 break
    #         if not found:
    #             return False
    #     return True

    # def __contains__(self, item: Union[VarType, PyType]):
    #     lv = self.get_level()
    #     if item not in lv:
    #         return True
    #     return False

    @staticmethod
    def get_vartype_repl(te1: Basetype, te2: Basetype):
        repl = dict()
        if te1.is_single_container() and te2.is_single_container():
            if te1[0].ptype == te2[0].ptype:
                return Basetype.get_vartype_repl(te1[0].keys, te2[0].keys)
        if te1.is_spectype() and not te2.is_spectype():
            specte = te1
            otherte = te2
        elif not te1.is_spectype() and te2.is_spectype():
            specte = te2
            otherte = te1
        elif te1.is_vartype() and not te2.is_vartype():
            specte = te1
            otherte = te2
        elif not te1.is_vartype() and te2.is_vartype():
            specte = te2
            otherte = te1
        else:
            return repl
        repl[specte] = otherte
        return repl

    def has_single_spectype(self):
        if len(self) != 1:
            return False
        ptip = self[0]
        if isinstance(ptip, VarType) and SPECTYPE_MARKER in ptip.varexp:
            return True
        if not isinstance(ptip, PyType):
            return False
        if ptip.keys is None:
            return False
        return ptip.keys.has_single_spectype()

    def has_single_vartype(self):
        if len(self) != 1:
            return False
        ptip = self[0]
        if isinstance(ptip, VarType):
            return True
        if not isinstance(ptip, PyType):
            return False
        if ptip.keys is None:
            return False
        return ptip.keys.has_single_vartype()

    def get_single_spectype(self: Basetype):
        ptip = self[0]
        ptip: PyType | VarType
        if isinstance(ptip, VarType) and SPECTYPE_MARKER in ptip.varexp:
            return Basetype({ptip})
        return ptip.keys.get_single_spectype()

    def get_single_vartype(self: Basetype):
        ptip = self[0]
        ptip: PyType | VarType
        if isinstance(ptip, VarType):
            return Basetype({ptip})
        return ptip.keys.get_single_vartype()

    def __contains__(self, other: Basetype):
        contains_flag = True
        for tip in other:
            found = False
            for tip2 in self:
                if hash(tip) == hash(tip2):
                    found = True
                    break
            if not found:
                contains_flag = False
                break
        if contains_flag:
            return True
        for tip2 in self:
            if (isinstance(tip2, PyType) and tip2.keys is None) or isinstance(tip2, VarType):
                continue
            contains_flag = tip2.keys.__contains__(other)
            if contains_flag:
                return True
        return False

    def replace_in_te(self, to_replace: Basetype, replace_with: Basetype):
        if to_replace not in self:
            return self
        new_te = Basetype()
        newself = deepcopy(self)
        for tip in self:
            if (isinstance(tip, PyType) and tip.keys is None) or isinstance(tip, VarType):
                continue
            aux_te = Basetype()
            newself = Basetype(newself - Basetype({tip}))
            new_pytype = PyType(tip.ptype)
            new_pytype.keys = tip.keys.replace_in_te(to_replace, replace_with)
            aux_te += Basetype({new_pytype})
            newself += aux_te
        if to_replace in newself:
            new_te = Basetype(newself - to_replace) + replace_with
        else:
            new_te = newself
        return new_te

    def replace_by_dict(self, repl: dict[Basetype, Basetype]):
        new_te = deepcopy(self)
        for k, v in repl.items():
            new_te = new_te.replace_in_te(k, v)
        return new_te


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
