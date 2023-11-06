import ast
from Translator import Translator
import astor
from copy import deepcopy
from AbstractState import AbsState, VarAssign, TypeConstraint, VarType, TypeExpression, PyType, Context, hset


POSONLY_MARKER = '__po_'
VARARG_MARKER = '__va_'
KEYWORDONLY_MARKER = '__ko_'
KWARG_MARKER = '__kw_'
MARKERS = [POSONLY_MARKER, VARARG_MARKER, KEYWORDONLY_MARKER, KWARG_MARKER]


class ArgumentMismatchError(Exception):
    pass


class FunctionInstance:
    def __init__(self, call_node: ast.Call, current_state: AbsState, spec_state: AbsState):
        self.arglink = dict()
        self.current_state = current_state
        self.spec_state = spec_state
        self.pos_call_list = []
        self.keyword_call_dict = {}
        self.call_node = call_node
        for node in self.call_node.args:
            self.pos_call_list.append(astor.to_source(node).strip())
        for node in self.call_node.keywords:
            self.keyword_call_dict[node.arg] = node.value
        self.arg_list = deepcopy(list(self.spec_state.va))
        self._param_link()

    def _param_link(self):
        if (len(self.pos_call_list) > 0 or len(self.keyword_call_dict) > 0) and len(self.arg_list) == 0:
            raise ArgumentMismatchError('Too many arguments provided')
        if (len(self.pos_call_list) == 0 and len(self.keyword_call_dict) == 0) and len(self.arg_list) > 0:
            raise ArgumentMismatchError('Too few arguments provided')
        if len(self.arg_list) == 0 and len(self.pos_call_list) == 0 and len(self.keyword_call_dict) == 0:
            return
        va_var: str = self.arg_list.pop(0)
        if va_var.startswith(POSONLY_MARKER):
            if len(self.pos_call_list) == 0:
                raise ArgumentMismatchError('Too few positional arguments provided')
            call_entry = self.pos_call_list.pop(0)
            self.arglink[va_var] = call_entry
            self._param_link()
            # f(va_index+1)
        elif va_var.startswith(VARARG_MARKER):
            while len(self.pos_call_list) > 0:
                call_entry = self.pos_call_list.pop(0)
                if va_var not in self.arglink:
                    self.arglink[va_var] = (call_entry,)
                else:
                    self.arglink[va_var] = self.arglink[va_var] + (call_entry,)
            if va_var not in self.arglink:
                raise ArgumentMismatchError(f'Variable argument {va_var} is not populated')
            self._param_link()
        elif va_var.startswith(KEYWORDONLY_MARKER):
            if len(self.keyword_call_dict) == 0:
                raise ArgumentMismatchError('Too few keyword arguments provided')
            varname = va_var[len(KEYWORDONLY_MARKER):]
            if varname not in self.keyword_call_dict:
                raise ArgumentMismatchError(f'Keyword argument {varname} is not provided')
            self.arglink[va_var] = astor.to_source(self.keyword_call_dict.pop(varname)).strip()
            self._param_link()
        elif va_var.startswith(KWARG_MARKER):
            if len(self.keyword_call_dict) == 0:
                raise ArgumentMismatchError(f'No more keyword arguments for {va_var}')
            keyword_list = list(self.keyword_call_dict)
            while len(self.keyword_call_dict) > 0:
                ko_key = keyword_list.pop(0)
                call_entry = astor.to_source(self.keyword_call_dict.pop(ko_key)).strip()
                if va_var not in self.arglink:
                    self.arglink[va_var] = {ko_key: call_entry}
                else:
                    self.arglink[va_var].update({ko_key: call_entry})
            self._param_link()
        else:
            if len(self.pos_call_list) > 0:
                call_entry = self.pos_call_list.pop(0)
            elif len(self.keyword_call_dict) > 0:
                keyword_list = list(self.keyword_call_dict)
                ko_key = keyword_list.pop(0)
                call_entry = astor.to_source(self.keyword_call_dict.pop(ko_key)).strip()
            else:
                raise ArgumentMismatchError(f'No more arguments for {va_var}')
            self.arglink[va_var] = call_entry
            self._param_link()

    def get_param_link(self):
        # self._param_link()
        return self.arglink

    def get_vartype_link(self):
        new_as = AbsState()
        new_as.va = VarAssign()
        new_as.tc = TypeConstraint()
        var_entries = []
        repl = dict()
        for spec_var, state_var in self.arglink.items():
            if isinstance(state_var, str):
                # variable argument types are not kept in the VA
                new_as.va[state_var] = self.spec_state.va[spec_var]
                repl[self.spec_state.va[spec_var]] = self.current_state.va[state_var]
            elif isinstance(state_var, tuple):
                new_te = TypeExpression()
                spec_vartype = self.spec_state.va[spec_var]
                new_pytype = PyType(tuple)
                for sv in state_var:
                    new_pytype.keys.add(self.current_state.va[sv])
                new_te.add(new_pytype)
                var_entries.append((spec_vartype, hset({new_te})))
            elif isinstance(state_var, dict):
                new_te = TypeExpression()
                spec_vartype = self.spec_state.va[spec_var]
                new_pytype = PyType(dict)
                new_pytype.keys.add(PyType(str))
                for k, sv in state_var.items():
                    new_pytype.values.add(self.current_state.va[sv])
                new_te.add(new_pytype)
                var_entries.append((spec_vartype, hset({new_te})))
        new_as.tc = deepcopy(self.spec_state.tc)
        for ctx in new_as.tc:
            for var_entry in var_entries:
                if var_entry[0] not in ctx:
                    raise RuntimeError(f'No variable entry in specs for {var_entry[0]}')
                ctx[var_entry[0]] |= var_entry[1]
        aux = new_as.vartype_replace_by_dict(repl)
        pass


if __name__ == '__main__':
    # tree = ast.parse('''
    # foo(1,2,3,4,5,6,7,e=8,f=9,x=10,y=11,z=12,k=13)
    # ''')
    # foo(1,2,3,4,5,6,7,x=8,k=9,f=10,y=11,z=12,e=13)
    tree = ast.parse('''
foo(h,i,j,k,l,m,n,e=o,f=p,w=q,x=r,y=s,z=t)
''')

    # def foo(a, b, /, c, *d, e, f, **g):
    spec = (r'__po_a:T?1 /\ __po_b:T?2 /\ c:T?3 /\ __va_d:T?4 /\ __ko_e:T?5 /\ __ko_f:T?6 /\ __kw_g:T?7 ^ '
            r'(T?1:int /\ T?2:int /\ T?3:int /\ T?4:TopType /\ T?5:int /\ T?6:int /\ T?7:TopType)')
    aux = Translator.translate_as(spec)
    str_state = (r'h:T_h /\ i:T_i /\ j:T_j /\ k:T_k /\ l:T_l /\ m:T_m /\ n:T_n /\ '
                 r'o:T_o /\ p:T_p /\ q:T_q /\ r:T_r /\ s:T_s /\ t:T_t ^ '
                 r'(T_h:int /\ T_i:float /\ T_j:int /\ T_k:float /\ T_l:int /\ T_m:float /\ T_n:int /\ '
                 r'T_o:float /\ T_p:int /\ T_q:float /\ T_r:int /\ T_s:float /\ T_t:int)')
    current_as = Translator.translate_as(str_state)
    # print(aux)
    f = FunctionInstance(tree.body[0].value, current_as, aux)
    print(f.get_param_link())
    f.get_vartype_link()
