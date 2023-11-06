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
        if not self.keys or len(self.keys) == 0:
            return False
        auxte = TypeExpression()
        auxte.add(item)  # between two TEs, not a GE and TE
        return auxte in self.keys

    def __le__(self, item):
        if isinstance(self, VarType) and isinstance(item, VarType):
            if self == item:
                return True
            return False
        if isinstance(self, PyType) and isinstance(item, PyType):
            if self == item:
                return True
            if self.ptype == item.ptype:
                if self.keys <= item.keys:
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
        elif self.keys is None and other.keys is not None:
            return deepcopy(other)
        elif self.keys is not None and other.keys is None:
            return deepcopy(self)
        elif self.keys is None and other.keys is None:
            return deepcopy(other)
        if self.keys is not None and len(self.keys) == 0 and len(other.keys) != 0:
            return deepcopy(other)
        elif self.keys is not None and len(self.keys) != 0 and len(other.keys) == 0:
            return deepcopy(self)
        elif self.keys is not None and len(self.keys) != 0 and len(other.keys) != 0:
            inter = self.keys & other.keys
            if inter is None:
                return None
            return PyType(self.ptype, inter)
        else:
            raise RuntimeError('Intersection case not treated: {} & {}'.format(self, other))


class PyType(GenericType):
    def __init__(self, ptype, keys=None, values=None):
        self.ptype = deepcopy(ptype)
        self.keys = deepcopy(keys)
        self.values = deepcopy(values)
        if (ptype in container_ptypes) and (self.keys is None):
            self.keys = TypeExpression()
        if (ptype in mapping_types) and (self.keys is None) and (self.values is None):
            self.keys = TypeExpression()
            self.values = TypeExpression()

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
            retstr += '<'
            # for c_type in self.contains:
            #     retstr += str(c_type) + ','
            retstr += str(self.keys)
            if self.values is not None:
                retstr += ', '
                retstr += str(self.values)
            retstr += '>'
        return retstr

    def __key(self):
        return self.ptype, self.keys, self.values

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
        if ptip1.keys is None and ptip2.keys is None:
            return new_ptip
        new_ptip.keys = TypeExpression.glb(ptip1.keys, ptip2.keys)
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
            newtip = PyType(ptype=tip.ptype, keys=tip.keys + newcontains)
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
                ctype.keys = deepcopy(ctype.keys) + deepcopy(tip.keys)
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
            if ptip.keys is None or len(ptip.keys) == 0:
                continue
            contained_te = ptip.keys
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

    @staticmethod
    def get_spectype_repl(te1, te2, vi_types: hset):
        te1: TypeExpression
        te2: TypeExpression
        ctx = CtxReplace()
        if te1.is_single_container() and te2.is_single_container():
            if te1[0].ptype == te2[0].ptype:
                return TypeExpression.get_spectype_repl(te1[0].keys, te2[0].keys, vi_types)
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

    def comparable(self: TypeExpression, other: TypeExpression, sign=None):
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
                return TypeExpression.get_vartype_repl(te1[0].keys, te2[0].keys)
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

    def get_single_spectype(self: TypeExpression):
        ptip = self[0]
        ptip: PyType | VarType
        if isinstance(ptip, VarType) and SPECTYPE_MARKER in ptip.varexp:
            return TypeExpression({ptip})
        return ptip.keys.get_single_spectype()

    def get_single_vartype(self: TypeExpression):
        ptip = self[0]
        ptip: PyType | VarType
        if isinstance(ptip, VarType):
            return TypeExpression({ptip})
        return ptip.keys.get_single_vartype()

    def __contains__(self, other: TypeExpression):
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

    def replace_in_te(self, to_replace: TypeExpression, replace_with: TypeExpression):
        if to_replace not in self:
            return self
        new_te = TypeExpression()
        newself = deepcopy(self)
        for tip in self:
            if (isinstance(tip, PyType) and tip.keys is None) or isinstance(tip, VarType):
                continue
            aux_te = TypeExpression()
            newself = TypeExpression(newself - TypeExpression({tip}))
            new_pytype = PyType(tip.ptype)
            new_pytype.keys = tip.keys.replace_in_te(to_replace, replace_with)
            aux_te += TypeExpression({new_pytype})
            newself += aux_te
        if to_replace in newself:
            new_te = TypeExpression(newself - to_replace) + replace_with
        else:
            new_te = newself
        return new_te

    def replace_by_dict(self, repl: dict[TypeExpression, TypeExpression]):
        new_te = deepcopy(self)
        for k, v in repl.items():
            new_te = new_te.replace_in_te(k, v)
        return new_te
