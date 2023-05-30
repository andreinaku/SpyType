from __future__ import annotations
from TypeExp import *
from uuid import uuid4
import traceback


class VarAssign(hdict):
    def __str__(self):
        if len(self.items()) == 0:
            return ''
        retstr = ''
        for varname, vtype in self.items():
            retstr += '{}:{} /\\ '.format(varname, vtype)
        retstr = retstr[:-4]
        return retstr

    def __repr__(self):
        return self.__str__()

    def get_all_vartypes(self) -> hset[VarType]:
        vtypes = hset()
        for varname, vtype in self.items():
            vtypes.add(vtype)
        return vtypes

    def vartype_replace_all(self, old_vtype: VarType, new_vtype: VarType):
        newvi = VarAssign()
        for varname, vtype in self.items():
            if vtype != old_vtype:
                newvi[varname] = deepcopy(vtype)
                continue
            newvi[varname] = deepcopy(new_vtype)
        return newvi

    def vartype_replace_by_dict(self, repl: hdict[VarType, VarType]):
        newvi = deepcopy(self)
        for old_vtype, new_vtype in repl.items():
            newvi = newvi.vartype_replace_all(old_vtype, new_vtype)
        return newvi

    @staticmethod
    def _get_repl(vi1, vi2, _all_vtypes: hset[VarType]):
        repl1 = hdict()
        repl2 = hdict()
        all_vtypes = deepcopy(_all_vtypes)
        common_keys = vi1.keys() & vi2.keys()
        for varname in common_keys:
            if vi1[varname] == vi2[varname]:
                continue
            if vi1[varname].varexp == BOTTOM:
                new_vtype = deepcopy(vi2[varname])
            elif vi2[varname].varexp == BOTTOM:
                new_vtype = deepcopy(vi1[varname])
            elif SPECTYPE_MARKER in vi1[varname].varexp and SPECTYPE_MARKER not in vi2[varname].varexp:
                new_vtype = deepcopy(vi2[varname])
            elif SPECTYPE_MARKER not in vi1[varname].varexp and SPECTYPE_MARKER in vi2[varname].varexp:
                new_vtype = deepcopy(vi1[varname])
            else:
                new_vtype = generate_new_vtype(vi1[varname], all_vtypes)
            repl1[vi1[varname]] = deepcopy(new_vtype)
            repl2[vi2[varname]] = deepcopy(new_vtype)
            all_vtypes.add(new_vtype)
        return repl1, repl2, all_vtypes

    @staticmethod
    def unify(vi1, vi2, _all_vtypes: hset[VarType], mode):
        vi1: VarAssign
        vi2: VarAssign
        newvi = VarAssign()
        # repl = hdict()
        all_vtypes = deepcopy(_all_vtypes)
        common_keys = vi1.keys() & vi2.keys()

        r1, r2, av = VarAssign._get_repl(vi1, vi2, all_vtypes)
        vi1 = vi1.vartype_replace_by_dict(r1)
        vi2 = vi2.vartype_replace_by_dict(r2)

        if vi1.keys() != vi2.keys() and mode == LUB:
            just_v1 = vi1.keys() - vi2.keys()
            for v1key in just_v1:
                newvi[v1key] = deepcopy(vi1[v1key])
            just_v2 = vi2.keys() - vi1.keys()
            for v2key in just_v2:
                newvi[v2key] = deepcopy(vi2[v2key])
        for varname in common_keys:
            newvi[varname] = deepcopy(vi1[varname])
        return newvi, r1, r2

    @staticmethod
    def glb(vi1, vi2):
        vi1: VarAssign
        vi2: VarAssign
        all_vtypes = hset(vi1.get_all_vartypes() | vi2.get_all_vartypes())
        return VarAssign.unify(vi1, vi2, all_vtypes, GLB)

    @staticmethod
    def lub(vi1, vi2, all_vtypes):
        vi1: VarAssign
        vi2: VarAssign
        # all_vtypes = hset(vi1.get_all_vartypes() | vi2.get_all_vartypes())
        return VarAssign.unify(vi1, vi2, all_vtypes, LUB)

    def split_spec_vi(self, funcname: str):
        out_vi = VarAssign()
        in_vi = VarAssign()
        for varname, vtype in self.items():
            if varname.startswith('__out_') or varname == funcname:
                out_vi[varname] = deepcopy(vtype)
                continue
            in_vi[varname] = deepcopy(vtype)
        return in_vi, out_vi

    def _a_varname_has_it(self, vtype):
        for varname, vt in self.items():
            if is_varname(varname) and vt == vtype:
                return True
        return False

    def get_inter_types(self, intermediaries):
        inter_types = hset()
        for varname, vtype in self.items():
            if varname in intermediaries and not self._a_varname_has_it(vtype):
                inter_types.add(deepcopy(vtype))
        return inter_types

    def trim_entries(self, intermediaries):
        newvi = VarAssign()
        for varname, vtype in self.items():
            if varname in intermediaries:
                continue
            newvi[varname] = deepcopy(vtype)
        return newvi

    def ingest_output_vars(self, func_params):
        newvi = VarAssign()
        for varname, vtype in self.items():
            if not varname.startswith(OUTMARKER):
                continue
            auxname = varname[len(OUTMARKER):]
            newvi[auxname] = deepcopy(vtype)
            if auxname not in func_params:
                continue
            origname = '{}{}'.format(ORIGMARKER, auxname)
            if origname in self:
                newvi[origname] = deepcopy(self[origname])
            else:
                newvi[origname] = deepcopy(self[auxname])
        for varname, vtype in self.items():
            if varname in newvi or varname.startswith(OUTMARKER):
                continue
            newvi[varname] = deepcopy(vtype)
        return newvi

    def get_param_vtypes(self, param_list: hset[str]):
        param_vtypes = hset()
        for paramname in param_list:
            param_vtypes.add(self[paramname])
        return param_vtypes

    def keep_func_params(self, param_list: hset[str]):
        newvi = VarAssign()
        for varname, vtype in self.items():
            if varname not in param_list:
                continue
            newvi[varname] = deepcopy(vtype)
        return newvi

    def rename_to_funcspec(self) -> VarAssign:
        visited = hset()
        newvi = VarAssign()
        for varname, vtype in self.items():
            if varname in visited:
                continue
            if varname == 'return':
                newvi[varname] = deepcopy(vtype)
                continue
            if varname.startswith(ORIGMARKER):
                auxname = varname[len(ORIGMARKER):]
                in_name = INMARKER + auxname
                out_name = OUTMARKER + auxname
                newvi[in_name] = deepcopy(vtype)
                visited.add(varname)
                if auxname in visited:
                    continue
                newvi[out_name] = deepcopy(self[auxname])
                visited.add(auxname)
                continue
            else:
                origname = ORIGMARKER + varname
                in_name = INMARKER + varname
                out_name = OUTMARKER + varname
                if origname in self:
                    if origname not in visited:
                        newvi[in_name] = self[origname]
                        visited.add(origname)
                    newvi[out_name] = deepcopy(vtype)
                    visited.add(varname)
                else:
                    newvi[in_name] = deepcopy(vtype)
                    visited.add(varname)
        return newvi

    @staticmethod
    def get_uid_repl(vi1: VarAssign, vi2: VarAssign) -> tuple[hdict[VarType, VarType], hdict[VarType, VarType]]:
        r1 = hdict()
        r2 = hdict()
        if vi1.keys() != vi2.keys():
            raise RuntimeError('VInfo keys should be the same')
        for k in vi1:
            new_vtype = VarType(varexp='T_{}'.format(uuid4().hex))
            r1[vi1[k]] = new_vtype
            r2[vi2[k]] = new_vtype
        return r1, r2

    def replace_spectypes(self, repl: dict[VarType, hset[TypeExpression]]):
        newvi = VarAssign()
        ti_remove = set()
        for varname, vt in self.items():
            if vt not in repl:
                newvi[varname] = deepcopy(vt)
                continue
            if len(repl[vt]) != 1:
                newvi[varname] = deepcopy(vt)
                continue
            te: TypeExpression
            te = repl[vt][0]
            if not te.is_single_vartype():
                newvi[varname] = deepcopy(vt)
                continue
            newvt = repl[vt][0][0]
            newvi[varname] = newvt
            ti_remove.add(deepcopy(vt))
        return newvi, ti_remove


class TypeConstraint(hset):
    def __str__(self):
        if len(self) == 0:
            return ''
        retstr = ''
        for elem in self:
            retstr += r'{} \/ '.format(elem)
        retstr = retstr[:-4]
        return retstr

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def glb(ti1, ti2):
        newti = TypeConstraint()
        if len(ti1) == 0 and len(ti2) == 0:
            return newti
        elif len(ti2) == 0:
            return deepcopy(ti1)
        elif len(ti1) == 0:
            return deepcopy(ti2)
        for td1 in ti1:
            for td2 in ti2:
                newtd = hdict.meet(td1, td2)
                newtd = Context(newtd)
                newti.add(newtd)
        return newti

    @staticmethod
    def lub_1(ti1, ti2):
        # newti = TInfo(ti1 | ti2)
        if len(ti1) == 0 and len(ti2) == 0:
            return deepcopy(ti1)
        if len(ti1) == 0 and len(ti2) != 0:
            return deepcopy(ti2)
        if len(ti2) == 0 and len(ti1) != 0:
            return deepcopy(ti1)
        # if len(ti1) != 1 and len(ti2) != 1:
        #     raise RuntimeError('Why is not all data collected?')
        newti = TypeConstraint()
        for td1 in ti1:
            for td2 in ti2:
                newtd = Context.lub_1(td1, td2)
                newti.add(newtd)
        return newti

    @staticmethod
    def lub_2(ti1, ti2):
        newti = TypeConstraint(ti1 | ti2)
        return newti

    def get_all_vartypes(self):
        vtypes = hset()
        for td in self:
            vtypes |= td.get_all_vartypes()
        return vtypes

    def vartype_replace_all(self, old_vtype: VarType, new_vtype: VarType):
        newti = TypeConstraint()
        for td in self:
            newtd = td.vartype_replace_all(old_vtype, new_vtype)
            newti.add(newtd)
        return newti

    def vartype_replace_by_dict(self, repl: hdict[VarType, VarType]):
        newti = TypeConstraint()
        for td in self:
            newtd = td.vartype_replace_by_dict(repl)
            newti.add(newtd)
        return newti

    def _old_simplify_spectypes(self, vi_types: hset):
        newti = TypeConstraint()
        for td in self:
            newtd = td._old_simplify_spectypes(vi_types)
            newti.add(newtd)
        return newti

    def simplify_spectypes(self):
        newti = TypeConstraint()
        for td in self:
            newtd = td.simplify_spectypes()
            newti.add(newtd)
        return newti

    def simplify_elim_inconsistencies(self):
        newti = TypeConstraint()
        if len(self) == 0:
            return newti
        for td in self:
            if not td.is_consistent():
                continue
            newti.add(deepcopy(td))
        if len(newti) == 0:
            raise RuntimeError('Cannot infer further due to inconsistencies')
        return newti

    def trim_entries(self, inter_types):
        newti = TypeConstraint()
        for td in self:
            newtd = td.trim_entries(inter_types)
            newti.add(newtd)
        return newti

    def simplify_no_vartypes(self):
        newti = TypeConstraint()
        if len(self) == 0:
            return newti
        for td in self:
            newtd = td.simplify_no_vartypes()
            newti.add(newtd)
        return newti

    def simplify_redundant_vartypes(self, vi_types: hset[VarType]):
        newti = TypeConstraint()
        for td in self:
            newtd = td.simplify_redundant_vartypes(vi_types)
            newti.add(newtd)
        return newti

    def keep_param_vartypes(self, param_vtypes: hset[str]):
        newti = TypeConstraint()
        for td in self:
            newtd = td.keep_param_vartypes(param_vtypes)
            if len(newtd):
                newti.add(newtd)
        return newti

    def get_all_direct_replacements(self, vtype: VarType) -> hset[VarType]:
        repl = hset()
        for td in self:
            newrepl = td.get_direct_replacements(vtype)
            repl = hset(repl & newrepl)
        return repl

    def simplify_elim_selfinfo(self):
        newti = TypeConstraint()
        for td in self:
            newtd = td.simplify_elim_selfinfo()
            newti.add(newtd)
        return newti

    def simplify_unused_vartypes(self, vi_vtypes: hset[VarType]):
        newti = TypeConstraint()
        for td in self:
            newtd = td.simplify_unused_vartypes(vi_vtypes)
            newti.add(newtd)
        return newti

    def integrity_checks(self):
        for td in self:
            td.integrity_checks()

    def get_spectype_equalities(self):
        repl = dict()
        aux_list = []
        for td in self:
            aux_repl = td.get_spectype_equalities()
            aux_list.append(aux_repl)
        if not aux_list:
            return repl
        common_entries = set.intersection(*(set(d.items()) for d in aux_list))
        for c_entry in common_entries:
            repl[c_entry[0]] = deepcopy(c_entry[1])
        return repl

    def remove_by_keys(self, ti_remove: set[VarType]):
        newti = TypeConstraint()
        for td in self:
            newtd = td.remove_by_keys(ti_remove)
            newti.add(newtd)
        return newti

    def simplify_collect(self):
        newti = TypeConstraint()
        newtd = Context()
        for td in self:
            for vt, te_set in td.items():
                try:
                    newtd[vt]
                except KeyError:
                    newtd[vt] = hset()
                if len(te_set) != 1:
                    raise RuntimeError('Cannot collect when there is more than one Type Expression')
                te = te_set[0]
                if len(newtd[vt]) == 0:
                    newtd[vt].add(deepcopy(te))
                elif len(newtd[vt]) > 1:
                    raise RuntimeError('Should only have ONE element')
                else:
                    newtd[vt] = hset({newtd[vt][0] + deepcopy(te)})
        newti.add(newtd)
        return newti

    def get_ti_from_vartype(self, vtype):
        newti = TypeConstraint()
        for td in self:
            newtd = td.get_td_from_vartype(vtype)
            newti.add(newtd)
        return newti

    def reduce_vartypes(self, vtype: VarType):
        newti = TypeConstraint()
        for td in self:
            try:
                newtd = td.reduce_vartypes(vtype)
                newti.add(newtd)
            except KeyError:
                continue  # may not be a key in all TDicts
        return newti

    def replace_unconstrained(self):
        newti = TypeConstraint()
        for td in self:
            newtd = td.replace_unconstrained()
            newti.add(newtd)
        return newti

    def reassign_vartypes(self, to_replace: VarType, replace_with: VarType):
        newti = TypeConstraint()
        for td in self:
            newtd = td.reassign_vartypes(to_replace, replace_with)
            newti.add(newtd)
        return newti

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        for ctx in self:
            if ctx not in other:
                return False
        for ctx in other:
            if ctx not in self:
                return False
        return True

    def __le__(self, other):
        for ctx in self:
            if ctx not in other:
                return False
        return True

    def __contains__(self, item: Context):
        for ctx in self:
            if item <= ctx:
                return True
        return False


class Context(hdict):

    def __str__(self):
        expr: str
        cte_set: set
        retstr = '('
        for vtype, te_set in self.items():
            if len(te_set) > 1:
                retstr += '('
            for te in te_set:
                retstr += '{}:{} & '.format(vtype, te)
            retstr = retstr[:-3]
            if len(te_set) > 1:
                retstr += ')'
            retstr += ' /\\ '
        retstr = retstr[:-4]
        retstr += ')'
        return retstr

    def __repr__(self):
        return self.__str__()

    def get_all_vartypes(self):
        vtypes = hset()
        for vtype, te_set in self.items():
            vtypes.add(vtype)
            for te in te_set:
                vtypes |= te.get_all_vartypes()
        return vtypes

    def vartype_replace_all(self, old_vtype: VarType, new_vtype: VarType):
        newtd = Context()
        for vtype, te_set in self.items():
            for te in te_set:
                if vtype != old_vtype:
                    try:
                        newtd[vtype]
                    except KeyError:
                        newtd[vtype] = hset()
                    newtd[vtype].add(te.vartype_replace_all(old_vtype, new_vtype))
                    continue
                try:
                    newtd[new_vtype]
                except KeyError:
                    newtd[new_vtype] = hset()
                newtd[new_vtype].add(te.vartype_replace_all(old_vtype, new_vtype))
        return newtd

    def vartype_replace_by_dict(self, repl: hdict[VarType, VarType]):
        newtd = deepcopy(self)
        for old_vtype, new_vtype in repl.items():
            newtd = newtd.vartype_replace_all(old_vtype, new_vtype)
        return newtd

    @staticmethod
    def teset_contains_spectype(teset: hset):
        for te in teset:
            if te.is_spectype():
                return True
        return False

    def get_spectype_replacements(self, vi_types: hset):
        ctx = CtxReplace()
        ctx.spec_repl = hdict()
        for vtype, te_set in self.items():
            if len(te_set) != 2:
                continue  # one spectype and one te only for this simplification
            new_ctx = TypeExpression.get_spectype_repl(te_set[0], te_set[1], vi_types)
            ctx.spec_repl |= new_ctx.spec_repl
            ctx.te_repl |= new_ctx.te_repl
            # ctx.spec_repl |= TypeExpression.get_spectype_repl(te_set[0], te_set[1], vi_types)
        return ctx

    def _old_simplify_spectypes(self, vi_types: hset):
        ctx = self.get_spectype_replacements(vi_types)
        newtd = Context()
        for vtype, te_set in self.items():
            newset = hset()
            te: TypeExpression
            for te in te_set:
                found = False
                to_replace = TypeExpression()
                replace_with = TypeExpression()
                for to_replace, replace_with in ctx.te_repl.items():
                    if to_replace in te:
                        found = True
                        break
                if found:
                    newte = te.replace_te(to_replace, replace_with)
                else:
                    newte = te.replace_vartype(ctx.spec_repl)
                newset.add(newte)
            newtd[vtype] = newset
        for to_replace, replace_with in ctx.te_repl.items():
            vtype = replace_with[0]  # replace_with is a TE containing just one spectype
            newtd[vtype] = hset({deepcopy(to_replace)})  # to_replace is a TE
        return newtd

    def get_vartype_replacements(self):
        new_repl = dict()
        for vtype, te_set in self.items():
            if len(te_set) == 1:
                continue
            if len(te_set) != 2:
                raise RuntimeError('This case is not treated yet')
            new_repl = TypeExpression.get_vartype_repl(te_set[0], te_set[1])
        return new_repl

    def simplify_spectypes(self):
        repl = self.get_vartype_replacements()
        newtd = Context()
        for vtype, te_set in self.items():
            te_set: hset[TypeExpression]
            if len(te_set) == 1:
                newtd[vtype] = deepcopy(te_set)
                continue
            if len(te_set) != 2:
                raise RuntimeError('This case is not yet treated')
            if repl is None:
                raise RuntimeError('2 entries and no replacement. why?')
            for k, v in repl.items():
                newtd[vtype] = hset({deepcopy(k)})
                aux_vtype = k[0]
                newtd[aux_vtype] = hset({deepcopy(v)})
        return newtd

    def is_consistent(self):
        for vtype, te_set in self.items():
            ptip_list = []
            for te in te_set:
                ptips = set()
                for ptip in te:
                    if isinstance(ptip, VarType):
                        return True
                    ptips.add(ptip.ptype)
                ptip_list.append(ptips)
            if len(ptip_list) == 0:
                return True
            inter = set.intersection(*ptip_list)
            if len(inter) == 0:
                return False
        return True

    @staticmethod
    def teset_contains_any_vartype(te_set: hset[TypeExpression]):
        for te in te_set:
            if te.contains_any_vartype():
                return True
        return False

    @staticmethod
    def teset_contains_specific_vartype(te_set: hset[TypeExpression], vtype: VarType):
        for te in te_set:
            if te.contains_vartype(vtype):
                return True
        return False

    def _is_only_key(self, vtype: VarType):
        if vtype not in self:
            raise RuntimeError('what the hell is this?')
        for vt, te_set in self.items():
            if self.teset_contains_specific_vartype(te_set, vtype):
                return False
        return True

    def trim_entries(self, inter_types):
        newtd = Context()
        for vtype, te_set in self.items():
            if vtype in inter_types and self._is_only_key(vtype):
                continue
            newtd[vtype] = deepcopy(te_set)
        return newtd

    def simplify_no_vartypes(self):
        newtd = Context()
        for vtype, te_set in self.items():
            if self.teset_contains_any_vartype(te_set):
                newtd[vtype] = deepcopy(te_set)
                continue
            newte = te_set[0]
            for te in te_set:
                newte = TypeExpression.glb(newte, te)
            if len(newte) == 0:
                return newtd
            newtd[vtype] = hset({newte})
        return newtd

    def simplify_redundant_vartypes(self, vi_types: hset[VarType]):
        newtd = Context()
        repl = hdict()
        for vtype, te_set in self.items():
            newset = hset()
            for te in te_set:
                if not te.is_vartype():
                    newset.add(te)
                    continue
                aux_vtype = te[0]  # one element that is a VarType
                if aux_vtype in vi_types:
                    newset.add(te)
                    continue  # should not be a VI value
                if aux_vtype in self:
                    newset.add(te)
                    continue  # should not be a TD key
                repl[aux_vtype] = deepcopy(vtype)
            if len(newset) > 0:
                newtd[vtype] = newset
        for oldtype, newtype in repl.items():
            newtd = newtd.vartype_replace_all(oldtype, newtype)
        return newtd

    def get_vtype_dependencies(self) -> hdict[VarType, hset[VarType]]:
        deps = hdict()
        for vtype, te_set in self.items():
            for te in te_set:
                all_vartypes = te.get_all_vartypes()
                try:
                    deps[vtype]
                except KeyError:
                    deps[vtype] = hset()
                deps[vtype] |= all_vartypes
        return deps

    def keep_param_vartypes(self, param_vtypes: hset[VarType]) -> Context:
        newtd = Context()
        deps = self.get_vtype_dependencies()
        vtype: VarType
        te_set: hset[TypeExpression]
        for vtype, te_set in self.items():
            if vtype.is_dependency_of_bulk(deps, param_vtypes):
                newtd[vtype] = deepcopy(te_set)
                continue
        return newtd

    def get_direct_replacements(self, vtype: VarType):
        repl = hset()
        for vt, te_set in self.items():
            if vtype != vt:
                continue
            for te in te_set:
                if te.is_vartype():
                    repl.add(deepcopy(te[0]))
        return repl

    def simplify_elim_selfinfo(self):
        newtd = Context()
        for vt, te_set in self.items():
            newset = hset()
            for te in te_set:
                if not te.is_vartype():
                    newset.add(deepcopy(te))
                    continue
                if len(te) > 1:
                    newset.add(deepcopy(te))
                    continue
                other_vt = te[0]
                if vt != other_vt:
                    newset.add(deepcopy(te))
                    continue
            if len(newset) > 0:
                newtd[vt] = newset
        return newtd

    def _replace_vartypes(self, repl: hdict[VarType, TypeExpression]):
        newtd = Context()
        oldtd = self
        while True:
            for vt, te_set in self.items():
                newset = hset()
                for te in te_set:
                    newte = te.replace_vartype(repl)
                    newset.add(newte)
                newtd[vt] = newset
            if newtd == oldtd:
                break
            oldtd = deepcopy(newtd)
        return newtd

    def simplify_unused_vartypes(self, vi_vtypes: hset[VarType]):
        newtd = Context()
        repl = hdict()
        for vt, te_set in self.items():
            if vt in vi_vtypes:
                newtd[vt] = deepcopy(te_set)
                continue
            if len(te_set) > 1:
                newtd[vt] = deepcopy(te_set)
                continue
            te = te_set[0]
            repl[vt] = deepcopy(te)
        # print(repl)
        newtd = newtd._replace_vartypes(repl)
        return newtd

    def integrity_checks(self):
        for vt, te_set in self.items():
            if len(te_set) != 1:
                raise RuntimeError('A tas should not have more than one info for a VarType')

    def get_spectype_equalities(self):
        vt: VarType
        repl = dict()
        for vt, te_set in self.items():
            if SPECTYPE_MARKER not in vt.varexp:
                continue
            if len(te_set) != 1:
                continue
            te:TypeExpression
            te = te_set[0]
            repl[vt] = deepcopy(te_set)
        return repl

    def remove_by_keys(self, td_remove: set[VarType]):
        newtd = Context()
        for vt in self:
            if vt in td_remove:
                continue
            newtd[vt] = deepcopy(self[vt])
        return newtd

    @staticmethod
    def lub_1(td1: Context, td2: Context):
        newtd = Context()
        for k, v in td1.items():
            if len(v) != 1:
                raise RuntimeError('More than one TE')
        for k, v in td2.items():
            if len(v) != 1:
                raise RuntimeError('More than one TE')
        common_keys = td1.keys() & td2.keys()
        only_td1 = td1.keys() - td2.keys()
        only_td2 = td2.keys() - td1.keys()
        for ckey in common_keys:
            newtd[ckey] = hset()
            newte = td1[ckey][0] + td2[ckey][0]
            newtd[ckey].add(newte)
        for k1 in only_td1:
            newtd[k1] = deepcopy(td1[k1])
        for k2 in only_td2:
            newtd[k2] = deepcopy(td2[k2])
        return newtd

    def __le__(self, other: Context):
        if not (self.keys() <= other.keys()):
            return False
        for k, v in self.items():
            te1 = self.squash_te(v[0])
            te2 = other.squash_te(other[k][0])
            if not (te1 <= te2):
                return False
        return True

    def get_keys_for_vartype(self, vtype: VarType):
        key_set = set()
        if vtype not in self.keys():
            return key_set
        key_set.add(vtype)
        te_set = self[vtype]
        for te in te_set:
            te_vartypes = te.get_all_vartypes()
            for vt in te_vartypes:
                key_set |= self.get_keys_for_vartype(vt)
        return key_set

    def get_td_from_vartype(self, vtype: VarType):
        newtd = Context()
        vtype_keys = self.get_keys_for_vartype(vtype)
        for vt, te_set in self.items():
            if vt not in vtype_keys:
                continue
            newtd[vt] = deepcopy(te_set)
        return newtd

    def get_eq(self, vtype: VarType):
        vtype_te: TypeExpression = self[vtype][0]
        vtype_keys = self.get_keys_for_vartype(vtype) - {vtype}
        if not vtype_keys:
            return deepcopy(vtype_te)
        new_te = TypeExpression()
        te_vtypes = vtype_te.get_all_vartypes()
        for te_vt in te_vtypes:
            if te_vt not in vtype_keys:
                new_te.add(te_vt)
                continue
            new_te = new_te + self.get_eq(te_vt)
        return deepcopy(new_te)

    def reduce_vartypes(self, vtype: VarType):
        newtd = Context()
        newtd[vtype] = hset({self.get_eq(vtype)})
        return newtd

    def replace_unconstrained(self):
        newtd = Context()
        repl = dict()
        newvt = VarType('T_any')
        for vt, teset in self.items():
            te = teset[0]
            vtypes = te.get_all_vartypes()
            for vtype in vtypes:
                repl[vtype] = TypeExpression({deepcopy(newvt)})
            newte = te.replace_vartype(repl)
            newtd[vt] = hset({newte})
        return newtd

    def reassign_vartypes(self, to_replace: VarType, replace_with: VarType):
        newtd = Context()
        if to_replace not in self:
            newtd = deepcopy(self)
            newtd[to_replace] = deepcopy(self[replace_with])
            return newtd
        for vt, te_set in self.items():
            if vt != to_replace:
                newtd[vt] = deepcopy(te_set)
                continue
            newtd[vt] = deepcopy(self[replace_with])
        return newtd

    def squash_te(self, te: TypeExpression):
        # list<set<T_c>>, where, in context, we have T_c:str+float -> list<set<str+float>>
        newte = TypeExpression()
        for t in te:
            if isinstance(t, VarType):
                if t not in self:  # unconstrained vartype
                    # newte.add(t)
                    newte.add(VarType('T_any'))
                else:
                    newte |= self.squash_te(self[t][0])
            else:
                if t.contains:
                    newte.add(PyType(t.ptype, self.squash_te(t.contains)))
                else:
                    newte.add(t)
        return newte

    def __eq__(self, other):
        for vt, types in self.items():
            if vt not in other:
                return False
            if len(types) != 1 or len(other[vt]) != 1:
                raise RuntimeError('More than one TE not supported in __eq__')
            te1 = self.squash_te(types[0])
            te2 = self.squash_te(other[vt][0])
            if te1 != te2:
                return False
        return True

    def __hash__(self):
        return super().__hash__()


class AbsState:
    def __init__(self, va=None, tc=None):
        if not va:
            va = VarAssign()
        if not tc:
            tc = TypeConstraint()
        self.va = va
        self.tc = tc

    def __len__(self):
        return len(self.va) + len(self.tc)

    def __str__(self):
        if len(self) == 0:
            return ''
        retstr = '{} ^ \n'.format(self.va)
        if len(self.tc) == 0:
            return retstr
        for td in self.tc:
            retstr += '\t{} \\/ \n'.format(td)
        retstr = retstr[:-5] + '\n'
        # retstr = '{} ^ {}'.format(self.vi, self.ti)
        return retstr

    def __repr__(self):
        return self.__str__()

    def __key(self):
        return hash(self.va), hash(self.tc)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other: AbsState):
        if self.va.keys() != other.va.keys():
            return False
        r1, r2 = VarAssign.get_uid_repl(self.va, other.va)
        tc1 = self.tc.vartype_replace_by_dict(r1)
        tc2 = other.tc.vartype_replace_by_dict(r2)
        return tc1 == tc2

    def __le__(self, other: AbsState):
        if self.va.keys() != other.va.keys():
            return False
        r1, r2 = VarAssign.get_uid_repl(self.va, other.va)
        tc1 = self.tc.vartype_replace_by_dict(r1)
        tc2 = other.tc.vartype_replace_by_dict(r2)
        return tc1 <= tc2

    def old__eq__(self, other: AbsState):
        if self.va.keys() != other.va.keys():
            return False
        r1, r2 = VarAssign.get_uid_repl(self.va, other.va)
        tc1 = self.tc.vartype_replace_by_dict(r1)
        tc2 = other.tc.vartype_replace_by_dict(r2)
        newvi = self.va.vartype_replace_by_dict(r1)
        for varname, vt in newvi.items():
            newti1 = tc1.reduce_vartypes(vt)
            newti1 = newti1.replace_unconstrained()
            newti2 = tc2.reduce_vartypes(vt)
            newti2 = newti2.replace_unconstrained()
            if newti1 != newti2:
                return False
        return True

    def get_all_vartypes(self) -> hset:
        vtypes = hset()
        vtypes |= self.va.get_all_vartypes()
        vtypes |= self.tc.get_all_vartypes()
        return hset(vtypes)

    def vartype_replace_all(self, old_vtype: VarType, new_vtype: VarType):
        newtas = AbsState()
        newvi = self.va.vartype_replace_all(old_vtype, new_vtype)
        newti = self.tc.vartype_replace_all(old_vtype, new_vtype)
        newtas.va = newvi
        newtas.tc = newti
        return newtas

    def vartype_replace_by_dict(self, repl: dict[VarType, VarType]):
        newtas = deepcopy(self)
        for old_vtype, new_vtype in repl.items():
            newtas = newtas.vartype_replace_all(old_vtype, new_vtype)
        return newtas

    @staticmethod
    def glb(tas1, tas2):
        tas1: AbsState
        tas2: AbsState
        newtas = AbsState()
        newtas.va, r1, r2 = VarAssign.glb(tas1.va, tas2.va)
        t1 = tas1.tc.var()
        newtas.tc = TypeConstraint.glb(tas1.tc, tas2.tc)
        # newtas = newtas.vartype_replace_by_dict(repl)
        return newtas

    @staticmethod
    def lub_1(tas1, tas2):
        tas1: AbsState
        tas2: AbsState
        newtas = AbsState()
        all_vtypes = (tas1.get_all_vartypes() | tas2.get_all_vartypes())
        newtas.va, r1, r2 = VarAssign.lub(tas1.va, tas2.va, all_vtypes)
        ti1 = tas1.tc.vartype_replace_by_dict(r1)
        ti2 = tas2.tc.vartype_replace_by_dict(r2)
        newtas.tc = TypeConstraint.lub_1(ti1, ti2)
        # newtas = newtas.vartype_replace_by_dict(repl)
        return newtas

    @staticmethod
    def lub_2(tas1, tas2):
        tas1: AbsState
        tas2: AbsState
        newtas = AbsState()
        all_vtypes = (tas1.get_all_vartypes() | tas2.get_all_vartypes())
        newtas.va, r1, r2 = VarAssign.lub(tas1.va, tas2.va, all_vtypes)
        ti1 = tas1.tc.vartype_replace_by_dict(r1)
        ti2 = tas2.tc.vartype_replace_by_dict(r2)
        newtas.tc = TypeConstraint.lub_2(ti1, ti2)
        # newtas = newtas.vartype_replace_by_dict(repl)
        return newtas

    @staticmethod
    def lub_3(tas1, tas2):
        tas1: AbsState
        tas2: AbsState
        newtas = AbsState()
        tas1 = tas1.simplify_collect()
        tas2 = tas2.simplify_collect()
        all_vtypes = (tas1.get_all_vartypes() | tas2.get_all_vartypes())
        newtas.va, r1, r2 = VarAssign.lub(tas1.va, tas2.va, all_vtypes)
        ti1 = tas1.tc.vartype_replace_by_dict(r1)
        ti2 = tas2.tc.vartype_replace_by_dict(r2)
        newtas.tc = TypeConstraint.lub_2(ti1, ti2)
        newtas = newtas.simplify_collect()
        # newtas = newtas.vartype_replace_by_dict(repl)
        return newtas

    @staticmethod
    def lub(tas1, tas2):
        return AbsState.lub_2(tas1, tas2)

    def rename_spectypes(self):
        all_vtypes = self.get_all_vartypes()
        repl = hdict()
        vtype: VarType
        for vtype in all_vtypes:
            if SPECTYPE_MARKER not in vtype.varexp:
                continue
            rr = self.tc.get_all_direct_replacements(vtype)
            if len(rr) == 1:
                repl[vtype] = deepcopy(rr[0])
                continue
            possible_type = VarType(vtype.varexp.replace(SPECTYPE_MARKER, '_'))
            new_vtype = generate_new_vtype(possible_type, all_vtypes)
            repl[vtype] = new_vtype
        newtas = self.vartype_replace_by_dict(repl)
        return newtas

    def replace_spectypes(self):
        repl = self.tc.get_spectype_equalities()
        newvi, ti_remove = self.va.replace_spectypes(repl)
        newti = self.tc.remove_by_keys(ti_remove)
        newtas = AbsState()
        newtas.va = newvi
        newtas.tc = newti
        return newtas

    def _old_simplify_spectypes(self):
        newtas = AbsState()
        newtas.va = deepcopy(self.va)
        vi_types = self.va.get_all_vartypes()
        newtas.tc = self.tc._old_simplify_spectypes(vi_types)
        return newtas

    def simplify_spectypes(self):
        newtas = AbsState()
        newtas.va = deepcopy(self.va)
        # vi_types = self.vi.get_all_vartypes()
        newtas.tc = self.tc.simplify_spectypes()
        return newtas

    def simplify_elim_inconsistencies(self):
        newtas = AbsState()
        newtas.va = deepcopy(self.va)
        newtas.tc = self.tc.simplify_elim_inconsistencies()
        return newtas

    def _get_intermediaries(self):
        intermediaries = hset()
        for varname in self.va:
            if not is_varname(varname):
                intermediaries.add(varname)
        return intermediaries

    def simplify_trim_intermediaries(self):
        newtas = AbsState()
        intermediaries = self._get_intermediaries()
        if len(intermediaries) == 0:
            newtas = deepcopy(self)
            return newtas
        inter_types = self.va.get_inter_types(intermediaries)
        newtas.va = self.va.trim_entries(intermediaries)
        newtas.tc = self.tc.trim_entries(inter_types)
        return newtas

    def ingest_output_vars(self, func_params):
        newtas = AbsState()
        newtas.tc = deepcopy(self.tc)
        newtas.va = self.va.ingest_output_vars(func_params)
        return newtas

    def simplify_no_vartypes(self):
        newtas = AbsState()
        newtas.va = deepcopy(self.va)
        if len(self.tc) > 0:
            newtas.tc = self.tc.simplify_no_vartypes()
            if len(newtas.tc) == 0:
                raise RuntimeError('Cannot continue inferring due to inconsistencies')
        else:
            newtas.tc = deepcopy(self.tc)
        return newtas

    def simplify_redundant_vartypes(self):
        newtas = AbsState()
        newtas.va = deepcopy(self.va)
        vi_types = self.va.get_all_vartypes()
        newtas.tc = self.tc.simplify_redundant_vartypes(vi_types)
        return newtas

    def get_param_vtypes(self, param_list: hset[str]):
        param_vtypes = hset()
        param_vtypes |= self.va.get_param_vtypes(param_list)
        return param_vtypes

    def keep_func_params(self, param_list: hset[str]):
        newtas = AbsState()
        param_vtypes = self.get_param_vtypes(param_list)
        newtas.va = self.va.keep_func_params(param_list)
        newtas.tc = self.tc.keep_param_vartypes(param_vtypes)
        return newtas

    def rename_to_funcspec(self):
        newtas = AbsState()
        newtas.tc = deepcopy(self.tc)
        newtas.va = self.va.rename_to_funcspec()
        return newtas

    def simplify_elim_selfinfo(self):
        newtas = AbsState()
        newtas.va = deepcopy(self.va)
        newtas.tc = self.tc.simplify_elim_selfinfo()
        return newtas

    def simplify_unused_vartypes(self):
        newtas = AbsState()
        newtas.va = deepcopy(self.va)
        vi_vtypes = newtas.va.get_all_vartypes()
        newtas.tc = self.tc.simplify_unused_vartypes(vi_vtypes)
        return newtas

    def intermediary_simplifications(self, param_list: hset[str]):
        newtas = deepcopy(self)
        newtas = newtas.simplify_elim_inconsistencies()
        newtas = newtas.simplify_spectypes()
        newtas = newtas.replace_spectypes()
        newtas = newtas.rename_spectypes()
        newtas = newtas.simplify_trim_intermediaries()
        newtas = newtas.ingest_output_vars(param_list)
        newtas = newtas.simplify_unused_vartypes()
        return newtas

    def _intermediary_simplifications(self, param_list: hset[str]):
        newtas = deepcopy(self)
        oldtas = deepcopy(self)
        newtas = newtas.simplify_elim_inconsistencies()
        newtas.integrity_checks()
        oldtas = deepcopy(newtas)
        newtas = newtas._old_simplify_spectypes()
        newtas.integrity_checks()
        oldtas = deepcopy(newtas)
        newtas = newtas.rename_spectypes()
        newtas = newtas.simplify_elim_selfinfo()
        newtas.integrity_checks()
        oldtas = deepcopy(newtas)
        newtas = newtas.simplify_no_vartypes()
        newtas.integrity_checks()
        oldtas = deepcopy(newtas)
        newtas = newtas.simplify_redundant_vartypes()
        newtas.integrity_checks()
        oldtas = deepcopy(newtas)
        newtas = newtas.ingest_output_vars(param_list)
        newtas.integrity_checks()
        oldtas = deepcopy(newtas)
        newtas = newtas.simplify_trim_intermediaries()
        newtas.integrity_checks()
        oldtas = deepcopy(newtas)
        newtas = newtas.simplify_unused_vartypes()
        newtas.integrity_checks()
        return newtas

    def final_simplifications(self, param_list: hset[str]):
        newtas = deepcopy(self)
        newtas = newtas.keep_func_params(param_list)
        newtas = newtas.rename_to_funcspec()
        return newtas

    def get_func_spec(self, param_list: hset[str]):
        newtas = AbsState()
        hasorig: set[str] = set()
        newlist = set()
        for p in param_list:
            if ORIGMARKER in p:
                varname = p[len(ORIGMARKER):]
                hasorig.add(varname)
                continue
            newlist.add(p)
        repl: dict[str, str] = dict()
        index = 1
        for varname in newlist:
            if varname not in hasorig:
                if varname == RETURN_NAME:
                    newname = RETURN_NAME
                else:
                    newname = INMARKER + 'p{}'.format(index)
                repl[varname] = newname
                index = index + 1
                continue
            inputname = INMARKER + 'p{}'.format(index)
            outputname = OUTMARKER + 'p{}'.format(index)
            origname = ORIGMARKER + varname
            repl[origname] = inputname
            repl[varname] = outputname
            index = index + 1
        for varname in repl:
            vt = self.va[varname]
            newname = repl[varname]
            newtas.va[newname] = deepcopy(self.va[varname])
            newtas.tc = TypeConstraint(newtas.tc | self.tc.reduce_vartypes(vt))
        return newtas

    def integrity_checks(self):
        try:
            self.va.integrity_checks()
            self.tc.integrity_checks()
        except RuntimeError as _re:
            traceback.print_exc()
            print(self)
            raise _re

    def simplify_collect(self):
        newtas = AbsState()
        newtas.va = deepcopy(self.va)
        newtas.tc = self.tc.simplify_collect()
        return newtas
