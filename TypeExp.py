from __future__ import annotations
from typing import Union
from utils import *
from copy import deepcopy


def vtype_exists(totest, vtypes):
    for vtype in vtypes:
        if totest == vtype.varexp:
            return True
    return False


def generate_new_vtype(base: VarType, all_vtypes: hset[VarType]):
    index = 0
    if not vtype_exists(base.varexp, all_vtypes):
        return deepcopy(base)
    while True:
        new_varexp = '{}_{}'.format(base.varexp, index)
        if vtype_exists(new_varexp, all_vtypes):
            index = index + 1
            continue
        break
    new_vtype = VarType(new_varexp)
    return new_vtype


class CtxReplace:
    def __init__(self):
        self.spec_repl = hdict()
        self.te_repl = hdict()


class GenericType:
    def __contains__(self, item):
        if item <= self:
            return True
        # if not isinstance(self, PyType) or not isinstance(item, PyType):
        #     return False
        if not isinstance(self, PyType):
            return False
        if not self.contains or len(self.contains) == 0:
            return False
        auxte = TypeExpression()
        auxte.add(item)  # between two TEs, not a GE and TE
        return auxte in self.contains

    def __le__(self, item):
        if isinstance(self, VarType) and isinstance(item, VarType):
            if self == item:
                return True
            return False
        if isinstance(self, PyType) and isinstance(item, PyType):
            if self == item:
                return True
            if self.ptype == item.ptype:
                if self.contains <= item.contains:
                    return True
                return False
        return False

    def __and__(self, other):
        if self == other:
            return deepcopy(self)
        if isinstance(self, VarType) and isinstance(other, VarType):
            vexp = 'T_{}'.format(id_generator())
            return VarType(vexp)
        if isinstance(self, VarType):
            return deepcopy(other)
        if isinstance(other, VarType):
            return deepcopy(self)
        if not isinstance(self, PyType) or not isinstance(other, PyType):
            return None
        if self.ptype != other.ptype:
            return None
        elif self.contains is None and other.contains is not None:
            return deepcopy(other)
        elif self.contains is not None and other.contains is None:
            return deepcopy(self)
        elif self.contains is None and other.contains is None:
            return deepcopy(other)
        if self.contains is not None and len(self.contains) == 0 and len(other.contains) != 0:
            return deepcopy(other)
        elif self.contains is not None and len(self.contains) != 0 and len(other.contains) == 0:
            return deepcopy(self)
        elif self.contains is not None and len(self.contains) != 0 and len(other.contains) != 0:
            inter = self.contains & other.contains
            if inter is None:
                return None
            return PyType(self.ptype, inter)
        else:
            raise RuntimeError('Intersection case not treated: {} & {}'.format(self, other))

    def same_as(self, other):
        return self == other


class PyType(GenericType):
    def __init__(self, ptype, contains=None):
        self.ptype = deepcopy(ptype)
        self.contains = deepcopy(contains)
        if (ptype in container_ptypes) and (self.contains is None):
            self.contains = TypeExpression()

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
            retstr = str(self.ptype).split("'")[1]
        if self.contains is not None:
            retstr += '<'
            # for c_type in self.contains:
            #     retstr += str(c_type) + ','
            retstr += str(self.contains)
            retstr += '>'
        return retstr

    def __key(self):
        return self.ptype, self.contains

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def glb(ptip1, ptip2):
        ptip1: PyType
        ptip2: PyType
        if ptip1.ptype != ptip2.ptype:
            return None
        new_ptip = PyType(ptip1.ptype)
        if ptip1.contains is None and ptip2.contains is None:
            return new_ptip
        new_ptip.contains = TypeExpression.glb(ptip1.contains, ptip2.contains)
        return new_ptip


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

    def is_dependency_of_bulk(self, deps, bulkset):
        bulkset: hset[VarType]
        for entry in bulkset:
            if self.is_dependency_of(deps, entry):
                return True
        return False

    def is_dependency_of(self, deps, v, visited=None) -> bool:
        if visited is None:
            visited = []
        if self == v:
            return True
        deps: hdict[VarType, hset[VarType]]
        v: VarType
        if v not in deps:
            return False
        if self in deps[v]:
            return True
        visited.append(self)
        for next_var in deps[v]:
            if next_var not in visited:
                return self.is_dependency_of(deps, next_var, visited)
        return False


class TypeExpression(hset):
    def __str__(self):
        retstr = ''
        for elem in self.__iter__():
            retstr += str(elem) + '+'
        retstr = retstr[:-1]
        return retstr

    def __repr__(self):
        return self.__str__()

    def __or__(self, other):
        return TypeExpression(super(TypeExpression, self).__or__(other))

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
        newte = TypeExpression()
        if not isinstance(ptip, PyType):
            raise RuntimeError('Why?')
        if ptip.ptype not in container_ptypes:
            raise RuntimeError('How??')
        for tip in self:
            if tip.ptype != ptip.ptype:
                newte.add(tip)
                continue
            newtip = PyType(ptype=tip.ptype, contains=tip.contains+newcontains)
            newte.add(newtip)
        return TypeExpression(newte)

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
                ctype.contains = deepcopy(ctype.contains) + deepcopy(tip.contains)
        return TypeExpression(newte)

    def __and__(self, other):
        new_te = TypeExpression()
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
        new_new_te = TypeExpression()
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
            if ptip.contains is None or len(ptip.contains) == 0:
                continue
            contained_te = ptip.contains
            vtypes |= contained_te.get_all_vartypes()
        return vtypes

    def vartype_replace_all(self, old_vtype: VarType, new_vtype: VarType):
        newte = TypeExpression()
        for ptip in self:
            if isinstance(ptip, VarType):
                ptip: VarType
                if ptip != old_vtype:
                    newte.add(deepcopy(ptip))
                    continue
                newte.add(deepcopy(new_vtype))
                continue
            ptip: PyType
            if ptip.contains is None or len(ptip.contains) == 0:
                newte.add(deepcopy(ptip))
                continue
            contained_te = ptip.contains
            newptip = PyType(ptip.ptype, contained_te.vartype_replace_all(old_vtype, new_vtype))
            newte.add(newptip)
        return newte

    @staticmethod
    def glb(te1, te2):
        te1: TypeExpression
        te2: TypeExpression
        newte = TypeExpression()
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
        repl: hdict[VarType, TypeExpression]
        newte = TypeExpression()
        if len(repl) == 0:
            return deepcopy(self)
        for tip in self:
            if isinstance(tip, VarType) and tip in repl:
                newte = newte + repl[tip]
                continue
            if isinstance(tip, PyType) and tip.contains is not None:
                newtip = PyType(ptype=tip.ptype)
                newtip.contains = tip.contains.replace_vartype(repl)
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
        if tip.contains is None:
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

    @staticmethod
    def get_spectype_repl(te1, te2, vi_types: hset):
        te1: TypeExpression
        te2: TypeExpression
        ctx = CtxReplace()
        if te1.is_single_container() and te2.is_single_container():
            if te1[0].ptype == te2[0].ptype:
                return TypeExpression.get_spectype_repl(te1[0].contains, te2[0].contains, vi_types)
        if te1.is_spectype() and not te2.is_spectype():
            specte = te1
            otherte = te2
        elif not te1.is_spectype() and te2.is_spectype():
            specte = te2
            otherte = te1
        else:
            return ctx
        spectype = specte[0]
        if spectype in vi_types:
            ctx.te_repl[otherte] = deepcopy(specte)
            return ctx
        ctx.spec_repl[spectype] = deepcopy(otherte)
        return ctx

    def contains_vartype(self, vtype: VarType):
        for ptip in self:
            if isinstance(ptip, VarType):
                if ptip == vtype:
                    return True
                continue
            if ptip.contains is not None and len(ptip.contains) > 0:
                return ptip.contains.contains_vartype(vtype)
        return False

    def contains_any_vartype(self):
        for ptip in self:
            if isinstance(ptip, VarType):
                return True
            if ptip.contains is not None and len(ptip.contains) > 0:
                return ptip.contains.contains_any_vartype()
        return False

    def replace_te(self, to_replace, replace_with):
        to_replace: TypeExpression
        replace_with: TypeExpression
        if to_replace not in self:
            return deepcopy(self)
        if to_replace <= self:
            dif = self - to_replace
            newte = dif | replace_with
            return TypeExpression(newte)
        newte = TypeExpression()
        for t in self:
            if not isinstance(t, PyType):
                newte.add(deepcopy(t))
                continue
            if t.contains is None or len(t.contains) == 0:
                newte.add(deepcopy(t))
                continue
            newtip = PyType(ptype=t.ptype)
            newtip.contains = t.contains.replace_te(to_replace, replace_with)
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

    def comparable(self, other, sign=None):
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
        # check if signs are consistent
        if sign is not None and sign != sign2:
            return False
        # go to the next levels
        for t1 in self:
            if isinstance(t1, VarType):
                continue
            if not t1.contains:
                continue
            t2 = other.get_by_type(t1.ptype)
            te1 = t1.contains
            te2 = t2.contains
            if not te1.comparable(te2, sign2):
                return False
        return True

    def __le__(self, other):
        if not self.comparable(other):
            raise RuntimeError('Cannot compare types')
        lv1 = self.get_level()
        lv2 = other.get_level()
        has_vartype1 = any(isinstance(t, VarType) for t in lv1)
        has_vartype2 = any(isinstance(t, VarType) for t in lv2)
        if has_vartype1 and has_vartype2:
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

    # def __contains__(self, item):
    #     item: TypeExpression
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
    def get_vartype_repl(te1: TypeExpression, te2: TypeExpression):
        repl = dict()
        if te1.is_single_container() and te2.is_single_container():
            if te1[0].ptype == te2[0].ptype:
                return TypeExpression.get_vartype_repl(te1[0].contains, te2[0].contains)
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
        if ptip.contains is None:
            return False
        return ptip.contains.has_single_spectype()

    def has_single_vartype(self):
        if len(self) != 1:
            return False
        ptip = self[0]
        if isinstance(ptip, VarType):
            return True
        if not isinstance(ptip, PyType):
            return False
        if ptip.contains is None:
            return False
        return ptip.contains.has_single_vartype()

    def get_single_spectype(self: TypeExpression):
        ptip = self[0]
        ptip: PyType | VarType
        if isinstance(ptip, VarType) and SPECTYPE_MARKER in ptip.varexp:
            return TypeExpression({ptip})
        return ptip.contains.get_single_spectype()

    def get_single_vartype(self: TypeExpression):
        ptip = self[0]
        ptip: PyType | VarType
        if isinstance(ptip, VarType):
            return TypeExpression({ptip})
        return ptip.contains.get_single_vartype()