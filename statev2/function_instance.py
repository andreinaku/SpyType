import sys
import os
aux = os.getcwd()
sys.path.append(aux)
from statev2.basetype import *


POSONLY_MARKER = '__po_'
VARARG_MARKER = '__va_'
KEYWORDONLY_MARKER = '__ko_'
KWARG_MARKER = '__kw_'
DEFAULT_MARKER = '__d_'
MARKERS = [POSONLY_MARKER, VARARG_MARKER, KEYWORDONLY_MARKER, KWARG_MARKER]
RETURN_VARNAME = 'return'


class ArgumentMismatchError(Exception):
    pass


# class SpecNotFoundError(Exception):
#     pass


class FunctionInstance:
    def __init__(self, ast_node: ast.Call | ast.BinOp, spec: FuncSpec):
        self.ast_node = ast_node
        self.spec = spec
        self.call_str = tosrc(ast_node)
    
    def _param_to_args_call(self):
        param_link = dict()
        param_list = list(self.spec.in_state.assignment)
        vararg = None
        kwarg = None
        for param in param_list:
            if param.startswith(VARARG_MARKER): 
                vararg = param
                param_link[vararg] = []
            elif param.startswith(KWARG_MARKER):
                kwarg = param
                param_link[kwarg] = {}
            else:
                # posonly, normal parameters and keyword-only, in order
                param_link[param] = None
        arg_list = []
        for arg in self.ast_node.args:
            # take only the args without keywords
            argname = tosrc(arg)
            arg_list.append(argname)
        current_index = None
        for i in range(0, len(param_list)):
            if param_list[i].startswith(VARARG_MARKER) or param_list[i].startswith(KWARG_MARKER):
                continue
            if param_link[param_list[i]] is not None:
                raise ArgumentMismatchError(f'{param_list[i]} already exists. Aborting!')
            try:
                if param_list[i].startswith(KEYWORDONLY_MARKER):
                    current_index = i
                    break
                param_link[param_list[i]] = arg_list.pop(0)  # pop the FIRST element
            except IndexError as inderr:
                raise ArgumentMismatchError(f'Ran out of arguments for {param_list[i]}')
        if current_index is None:
            current_index = i + 1
        if len(arg_list) > 0:
            if vararg is None:
                raise ArgumentMismatchError(f'Too many positional arguments and no vararg for {arg_list}')
            vararg_list = []
            while len(arg_list) > 0:
                current_arg = arg_list.pop(0)
                vararg_list.append(deepcopy(current_arg))
            param_link[vararg] = vararg_list
        kw_dict = {}
        for kw in self.ast_node.keywords:
            kw_formal = deepcopy(kw.arg)
            kw_actual = tosrc(kw.value)
            if kw_formal in kw_dict:
                raise ArgumentMismatchError(f'Keyword parameter {kw_formal} already instantiated')
            kw_dict[kw_formal] = kw_actual
        # for i in range(0, len(param_list)):           
        for i in range(current_index, len(param_list)):
            if param_list[i].startswith(VARARG_MARKER) or param_list[i].startswith(KWARG_MARKER):
                continue
            if (not param_list[i].startswith(KEYWORDONLY_MARKER)) or (param_list[i].startswith(POSONLY_MARKER)):
                raise ArgumentMismatchError(f'What kind of parameter is this {param_list[i]}? Should be keyword')
            current_param = param_list[i]
            if current_param.startswith(KEYWORDONLY_MARKER):
                current_param = current_param[len(KEYWORDONLY_MARKER):]
            if current_param.startswith(DEFAULT_MARKER):
                current_param = current_param[len(DEFAULT_MARKER):]
            if current_param in kw_dict:
                param_link[param_list[i]] = deepcopy(kw_dict[current_param])
                del kw_dict[current_param]
        if len(kw_dict) > 0:
            if kwarg is None:
                 raise ArgumentMismatchError(f'Too many keyword arguments and no vararg for {kw_dict}')
            for k, v in kw_dict.items():
                new_k = KEYWORDONLY_MARKER + k
                param_link[kwarg][new_k] = deepcopy(v)
        return param_link
    
    def _param_to_args_binop(self):
        param_link = dict()
        param_list = list(self.spec.in_state.assignment)
        if len(param_list) != 2:
            raise TypeError(f'Node {tosrc(self.ast_node)} is a BinOp with more than 2 operands?')
        param_link = {
            param_list[0]: tosrc(self.ast_node.left),
            param_list[1]: tosrc(self.ast_node.right)
        }
        return param_link

    def param_to_args(self):
        if isinstance(self.ast_node, ast.Call):
            return self._param_to_args_call()
        elif isinstance(self.ast_node, ast.BinOp):
            return self._param_to_args_binop()
        else:
            raise TypeError(f'Node {tosrc(self.ast_node)} is not Call or BinOp')

    def instantiate_spec(self):  # , call_code: str):
        call_code = self.call_str
        param_link = self.param_to_args()
        param_link[RETURN_NAME] = call_code
        new_spec = FuncSpec()
    
        def replace_in_state(state):
            nonlocal param_link
            new_state = State()
            for param_name, bt in state.assignment.items():
                # todo: check issue #13
                if param_name not in param_link:
                    raise RuntimeError(f'Something went wrong. {param_name} does not have a link')
                if param_name.startswith(VARARG_MARKER) or param_name.startswith(KWARG_MARKER):
                    if len(bt) > 1:
                        raise TypeError(f'{bt} for the parameter {param_name} should be only one type, not a sum. Aborting!')
                    pt = bt[0]
                    if isinstance(pt, VarType):
                        # contained_bt = Basetype({deepcopy(pt)})
                        contained_bt = Basetype({PyType(TopType)})
                    elif isinstance(pt, PyType):
                        if pt.keys is not None:
                            if pt.values is not None:
                                raise TypeError(f'Mapping pairs not supported yet for {bt} for the parameter {param_name}')
                            contained_bt = deepcopy(pt.keys)
                        elif pt in extra_sequences:
                            contained_bt = deepcopy(extra_sequences[pt])
                        elif pt == PyType(TopType):
                            contained_bt = Basetype({deepcopy(pt)})
                        else:
                            raise TypeError(f'No type available for the contents of {param_name}')
                    else:
                        raise TypeError(f'{bt} is not PyType or VarType')
                    if param_name.startswith(VARARG_MARKER):
                        # for member in param_link[param_name]:
                        #     new_state.assignment[member] = deepcopy(contained_bt)
                        new_name = f"({', '.join(param_link[param_name])})"
                        new_bt = Basetype({PyType(tuple, deepcopy(contained_bt))})
                        new_state.assignment[new_name] = deepcopy(new_bt)
                    else:
                        # for koname, koinstance in param_link[param_name].items():
                        #     new_state.assignment[koinstance] = deepcopy(contained_bt)
                        new_name_list = []
                        for koname, koinstance in param_link[param_name].items():
                            new_name_list.append(koinstance)
                        new_name = f"({', '.join(new_name_list)})"
                        new_bt = Basetype({PyType(tuple, deepcopy(contained_bt))})
                        new_state.assignment[new_name] = deepcopy(new_bt)
                else:
                    new_state.assignment[param_link[param_name]] = deepcopy(bt)
            return new_state
        
        new_spec.in_state = replace_in_state(self.spec.in_state)
        new_spec.out_state = replace_in_state(self.spec.out_state)
        if RETURN_NAME in self.spec.out_state.assignment:
            new_spec.out_state.assignment[call_code] = deepcopy(self.spec.out_state.assignment[RETURN_NAME])
        else:
            new_spec.out_state.assignment[call_code] = Basetype({PyType(type(None))})
        return new_spec
    