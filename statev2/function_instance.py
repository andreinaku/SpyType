from basetype import *


POSONLY_MARKER = '__po_'
VARARG_MARKER = '__va_'
KEYWORDONLY_MARKER = '__ko_'
KWARG_MARKER = '__kw_'
MARKERS = [POSONLY_MARKER, VARARG_MARKER, KEYWORDONLY_MARKER, KWARG_MARKER]
RETURN_VARNAME = 'return'


class ArgumentMismatchError(Exception):
    pass


# class SpecNotFoundError(Exception):
#     pass


class FunctionInstance:
    def __init__(self, call_node: ast.Call, current_state: State, spec: FuncSpec):
        self.call_node = call_node
        self.current_state = current_state
        self.spec = spec
        self.call_str = astor.to_source(call_node).strip()
    
    def param_to_args(self):
        param_link = dict()
        param_list = list(self.spec.in_state.assignment)
        vararg = None
        kwarg = None
        for param in param_list:
            if param.startswith(VARARG_MARKER): 
                vararg = param
            elif param.startswith(KWARG_MARKER):
                kwarg = param
            else:
                # posonly, normal parameters and keyword-only, in order
                param_link[param] = None
        arg_list = []
        for arg in self.call_node.args:
            # take only the args without keywords
            argname = astor.to_source(arg).strip()
            arg_list.append(argname)
        for i in range(0, len(param_list)):
            if param_list[i] in param_link:
                raise ArgumentMismatchError(f'{param_list[i]} already exists. Aborting!')
            try:
                param_link[param_list[i]] = arg_list.pop(0)  # pop the FIRST element
            except IndexError as inderr:
                raise ArgumentMismatchError(f'Ran out of arguments for {param_list[i]}')
        if len(arg_list) > 0:
            