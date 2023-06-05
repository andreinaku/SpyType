from specs import compute_funcspecs, compute_opspecs
from Translator import *
from zlib import crc32


class ExpVisit(ast.NodeVisitor):
    def __init__(self, current_as: AbsState):
        self.current_as = deepcopy(current_as)

    @staticmethod
    def get_param_list(node: ast.Call):
        param_list = []
        argnodes = []
        if isinstance(node.func, ast.Attribute):
            param_list.append(node.func.value.id)
        for argnode in node.args:
            argnodes.append(argnode)
            param_list.append(tosrc(argnode))
        return argnodes, param_list

    @staticmethod
    def get_func_name(node: ast.Call):
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        elif isinstance(node.func, ast.Name):
            return node.func.id
        else:
            raise RuntimeError('What is this function call?')

    @staticmethod
    def get_replacements(func_code, param_list):
        repl = dict()
        for i in range(len(param_list)):
            auxname = '__in_p{}'.format(i+1)
            repl[auxname] = param_list[i]
            auxname = '__out_p{}'.format(i+1)
            repl[auxname] = '__out_{}'.format(param_list[i])
        repl['return'] = func_code
        return repl

    def get_func_spec(self, node: ast.Call):
        funcname = self.get_func_name(node)
        strspecs = compute_funcspecs()
        strspec = strspecs[funcname]
        spec = Translator.translate_as(strspec)
        return spec

    @staticmethod
    def get_binop_spec(node: ast.BinOp):
        optype = type(node.op)
        strspecs = compute_opspecs()
        strspec = strspecs[ast.BinOp][optype]
        spec = Translator.translate_as(strspec)
        return spec

    def get_spec(self, node, operation=False):
        if operation:
            # todo: code for operation spec lookup
            return self.get_binop_spec(node)
        return self.get_func_spec(node)

    def replace_params(self, param_list: list[str], node: Union[ast.Call, ast.BinOp], spec: AbsState):
        newspec = AbsState()
        func_code = tosrc(node)
        repl = self.get_replacements(func_code, param_list)
        newspec.tc = deepcopy(spec.tc)
        for varname, te in spec.va.items():
            newspec.va[repl[varname]] = deepcopy(te)
        return newspec

    def visit_Constant(self, node: ast.Constant):
        nodesrc = tosrc(node)
        node_varexp = 'T_c_{}'.format(nodesrc)
        node_vartype = VarType(node_varexp)
        new_as: AbsState = deepcopy(self.current_as)
        # newte = TypeExpression()
        new_as.va[nodesrc] = node_vartype
        if len(new_as.tc) == 0:
            newctx = Context()
            newte = TypeExpression()
            newte.add(PyType(ptype=type(node.value)))
            newctx[node_vartype] = hset()
            newctx[node_vartype].add(newte)
            new_as.tc.add(newctx)
        for ctx in new_as.tc:
            newte = TypeExpression()
            newte.add(PyType(ptype=type(node.value)))
            ctx[node_vartype] = hset()
            ctx[node_vartype].add(newte)
        self.current_as = new_as

    def _visit_container(self, node: Union[ast.List, ast.Set, ast.Tuple]):
        if isinstance(node, ast.List):
            container_type = list
        elif isinstance(node, ast.Set):
            container_type = set
        elif isinstance(node, ast.Tuple):
            container_type = tuple
        else:
            raise RuntimeError('What kind of container is {}'.format(type(node)))
        elem_codes = set()
        for elem in node.elts:
            elem_codes.add(tosrc(elem))
            self.visit(elem)
        nodesrc = tosrc(node)
        nodecrc = hex(crc32(nodesrc.encode('utf-8')))[2:]
        node_varexp = 'T_{}'.format(nodecrc)
        node_vartype = VarType(node_varexp)
        new_as = deepcopy(self.current_as)
        try:
            new_as.va[nodesrc]
        except KeyError:
            new_as.va[nodesrc] = node_vartype
        # newte = TypeExpression()
        # newte.add(node_vartype)
        # new_as.vi[nodesrc].add(newte)
        newte = TypeExpression()
        for elemsrc in elem_codes:
            for va_te in self.current_as.va[elemsrc]:
                newte = newte + va_te
        if len(newte) == 0:
            new_vartype = gen_vtype_for_base(new_as, node_vartype)
            newte.add(new_vartype)
        contained_varexps = newte
        if len(new_as.tc) == 0:
            newctx = Context()
            newte = TypeExpression()
            newpytype = PyType(ptype=container_type, contains=contained_varexps)
            newte.add(newpytype)
            newctx[node_vartype] = hset()
            newctx[node_vartype].add(newte)
            new_as.tc.add(newctx)
            return new_as
        for ctx in new_as.tc:
            newpytype = PyType(ptype=container_type, contains=contained_varexps)
            newte = TypeExpression()
            newte.add(newpytype)
            ctx[node_vartype] = hset()
            ctx[node_vartype].add(newte)
        return new_as

    def visit_List(self, node: ast.List):
        self.current_as = self._visit_container(node)

    def visit_Set(self, node: ast.Set):
        self.current_as = self._visit_container(node)

    def visit_Tuple(self, node: ast.Tuple):
        self.current_as = self._visit_container(node)

    def get_tas(self):
        return self.current_as

    def visit_Assign(self, node: ast.Assign):
        self.visit(node.value)
        # nodesrc = tosrc(node)
        target_srcs = set()
        for target in node.targets:
            target_src = tosrc(target)
            target_srcs.add(target_src)
        valuesrc = tosrc(node.value)
        new_as: AbsState = deepcopy(self.current_as)
        changed = True
        for target_src in target_srcs:
            try:
                new_as.va[target_src] = deepcopy(self.current_as.va[valuesrc])
                # to_replace = self.current_tas.vi[target_src]
                # replace_with = self.current_tas.vi[valuesrc]
                # new_as.ti = new_as.ti.reassign_vartypes(to_replace, replace_with)
            except KeyError:
                changed = False
                break
                # raise RuntimeError('Assignment value {} not in our current tas'.format(valuesrc))
        if changed:
            self.current_as = new_as

    @staticmethod
    def _apply_spec(current_as: AbsState, spec_as: AbsState, nodecode: str):
        # spec_tas = _spec_tas.simplify_collect()
        in_va, out_va = spec_as.va.split_spec_va(nodecode)
        # newtc = TInfo.glb(current_tas.ti, spec_tas.ti)
        if not in_va.keys() <= current_as.va.keys():
            raise KeyError('The input parameters are not all found in the current Tas')
        newspec = AbsState()
        repl = dict()
        for k, v in spec_as.va.items():
            if k in current_as.va and current_as.va[k].varexp != BOTTOM:
                repl[v] = deepcopy(current_as.va[k])
        for k, v in spec_as.va.items():
            if v in repl:
                newspec.va[k] = repl[v]
                continue
            newspec.va[k] = deepcopy(spec_as.va[k])
        auxtc = spec_as.tc.vartype_replace_by_dict(repl)
        newspec.tc = deepcopy(auxtc)
        # print('spec` = {}'.format(newspec))
        # newva = newspec.va | current_tas.va
        # newva = VInfo.lub(newspec.va, current_tas.va)
        newva = VarAssign()
        for vname, vt in current_as.va.items():
            if vname not in newspec.va:
                newva[vname] = deepcopy(vt)
                continue
            if vt.varexp == BOTTOM:
                newva[vname] = deepcopy(newspec.va[vname])
                continue
            newva[vname] = deepcopy(vt)
        for vname, vt in newspec.va.items():
            if vname in current_as.va:
                continue
            newva[vname] = deepcopy(vt)
        newtc = TypeConstraint.glb(newspec.tc, current_as.tc)
        new_as = AbsState()
        new_as.va = VarAssign(deepcopy(newva))
        new_as.tc = deepcopy(newtc)
        # print('as` = {}'.format(new_as))
        return new_as

    # @staticmethod
    # def _apply_spec(current_tas: Tas, spec_tas: Tas, nodecode: str):
    #     in_vi, out_vi = spec_tas.vi.split_spec_vi(nodecode)
    #     # newti = TInfo.glb(current_tas.ti, spec_tas.ti)
    #     if not in_vi.keys() <= current_tas.vi.keys():
    #         raise KeyError('The input parameters are not all found in the current Tas')
    #     all_vtypes = current_tas.get_all_vartypes()
    #     newvi, r1, r2 = VInfo.lub(current_tas.vi, in_vi, all_vtypes)
    #     newtas = Tas()
    #     newtas.vi = VInfo(newvi | out_vi)
    #     ti1 = current_tas.ti.vartype_replace_by_dict(r1)
    #     ti2 = spec_tas.ti.vartype_replace_by_dict(r2)
    #     newti = TInfo.glb(ti1, ti2)
    #     newtas.ti = newti
    #     # newtas = newtas.vartype_replace_by_dict(repl)
    #     return newtas

    def _visit_spec(self, funcspec: AbsState, param_list: list[str], node: Union[ast.Call, ast.BinOp]):
        funcspec = self.replace_params(param_list, node, funcspec)
        nodecode = tosrc(node)
        # changed = True
        new_as = self._apply_spec(self.current_as, funcspec, nodecode)
        return new_as

    def visit_Call(self, node: ast.Call):
        funcspec = self.get_spec(node)
        argnodes, param_list = self.get_param_list(node)
        for argnode in argnodes:
            self.visit(argnode)
        changed = True
        new_as = None
        try:
            new_as = self._visit_spec(funcspec, param_list, node)
        except KeyError:
            changed = False
        if changed and new_as is not None:
            self.current_as = new_as

    def visit_BinOp(self, node: ast.BinOp):
        funcspec = self.get_spec(node, operation=True)
        self.visit(node.left)
        self.visit(node.right)
        leftsrc = tosrc(node.left)
        rightsrc = tosrc(node.right)
        self.current_as = self._visit_spec(funcspec, [leftsrc, rightsrc], node)

    def visit_Return(self, node: ast.Return):
        self.visit(node.value)
        target_src = 'return'
        valuesrc = tosrc(node.value)
        new_as: AbsState = deepcopy(self.current_as)
        changed = True
        try:
            new_as.va[target_src] = deepcopy(self.current_as.va[valuesrc])
        except KeyError:
            changed = False
        if changed:
            self.current_as = new_as

    def visit_While(self, node: ast.While):
        pass

    def visit_If(self, node: ast.If):
        pass
