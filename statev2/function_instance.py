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
    
    def param_map(self):
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
                param_link[param] = None
        arg_list = []
        for arg in self.call_node.args:
            argname = astor.to_source(arg).strip()
            arg_list.append(argname)
        if len(param_list) > len(arg_list):
            raise ArgumentMismatchError(f'Too few arguments in call {self.call_str}')
        for i in range(0, len(param_list)):
            param_link[param_list[i]] = arg_list[i]