import sys
import os
aux = os.getcwd()
sys.path.append(aux)
from statev2.basetype import *
from statev2.Translator import *


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
    def __init__(self, ast_node: ast.Call | ast.BinOp, current_state: State, spec: FuncSpec):
        self.ast_node = ast_node
        self.current_state = current_state
        self.spec = spec
        self.call_str = astor.to_source(ast_node).strip()
    
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
            argname = astor.to_source(arg).strip()
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
            kw_actual = astor.to_source(kw.value).strip()
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
            raise TypeError(f'Node {astor.to_source(self.ast_node).strip()} is a BinOp with more than 2 operands?')
        param_link = {
            param_list[0]: astor.to_source(self.ast_node.left).strip(),
            param_list[1]: astor.to_source(self.ast_node.right).strip()
        }
        return param_link

    def param_to_args(self):
        if isinstance(self.ast_node, ast.Call):
            return self._param_to_args_call()
        elif isinstance(self.ast_node, ast.BinOp):
            return self._param_to_args_binop()
        else:
            raise TypeError(f'Node {astor.to_source(self.ast_node).strip()} is not Call or BinOp')
