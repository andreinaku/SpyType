import os, sys
sys.path.append(os.getcwd())
from crackedcfg import CFG, CFGBuilder
from crackedcfg.builder import NameReplacer
from statev2.basetype import *
from statev2.transfer import *
# import type_inference.simple_fixpoint
import type_inference.worklist as worklist


class NameVisitor(ast.NodeVisitor):
    def __init__(self):
        self.names = set()

    def visit_Name(self, node: ast.Name):
        # nodesrc = tosrc(node)
        if not isinstance(node.ctx, ast.Load):
            self.names.add(deepcopy(node.id))

    def get_names(self):
        return self.names
    

class SSFlow:
    def __init__(self, params=None):
        self.params = params

    @staticmethod
    def merge(ss1: StateSet, ss2: StateSet) -> StateSet:
        result = StateSet.lub(ss1, ss2)
        return result

    @staticmethod
    def transfer(nodecode, input_as):
        tf = TransferFunc(input_as)
        tf.visit(nodecode)
        return tf.state_set


def get_cfg(filepath, makepng=True):
    cfg = CFGBuilder(separate=True).build_from_file('testcfg', filepath)
    if makepng:
        cfg.build_visual(filepath + '.png', 'png')
    return cfg


def build_func_cfg(func_name, func_ast, param_list, makepng=True):
    func_cfg = CFGBuilder(separate=True, args=param_list).build(
        name=func_name,
        tree=func_ast,
        add_pass=False
    )
    if makepng:
        func_cfg.build_visual('func.png', 'png')
    return func_cfg


def get_params_from_ast(func_ast: ast.FunctionDef):
    param_list = []
    for param in func_ast.args.args:
        param_list.append(param.arg)
    return param_list


def get_func_cfg(codecfg: CFG, func_name: str, makepng=True):
    func_ast = codecfg.func_asts[func_name]
    param_list = get_params_from_ast(func_ast)
    unique_names(func_ast, param_list)
    func_cfg = build_func_cfg(func_name, func_ast, param_list, makepng)
    return func_cfg


def unique_names(func_ast: ast.AST, param_list: list):
    name_func = NameReplacer(param_list)
    name_func.visit(func_ast)


def get_variable_names(node):
    variable_names = []
    # Check if the node is a variable definition
    if isinstance(node, ast.Assign):
        # Get the name of the variable
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            variable_names.append(target.id)
        return variable_names
    # Recursively search for variable definitions in child nodes
    for child_node in ast.iter_child_nodes(node):
        if not isinstance(child_node, ast.FunctionDef) and not isinstance(child_node, ast.ClassDef):
            variable_names += get_variable_names(child_node)
    return variable_names


def run_infer(filepath, funcname):
    # get the function CFG based on the function name
    cfg = get_cfg(filepath, makepng=False)
    func_cfg = get_func_cfg(cfg, funcname, True)
    # construct the initial abstract state
    init_ss = StateSet()
    new_state = State()
    functree = cfg.func_asts[funcname]
    names = get_variable_names(functree)
    for varname in func_cfg.params:
        new_state.assignment[varname] = new_state.generate_vartype_bt()
    for varname in names:
        new_state.assignment[varname] = Basetype.from_str('bot')
    init_ss.add(deepcopy(new_state))
    aux = worklist.WorklistAnalyzer(func_cfg, init_ss)
    aux.Iteration()
    mfp_in, mfp_out = aux.mfp_solution()
    return mfp_in, mfp_out


if __name__ == "__main__":
    mfp_in, mfp_out = run_infer('type_inference/test_funcs.py', 'test_add')
    # mfp_in, mfp_out = run_infer(sys.argv[1], sys.argv[2])
    print('---------------')
    print('MFP in' + os.linesep + '---------------')
    for id, ss in mfp_in.items():
        print(f'{id}: {ss}')
    print('---------------')
    print('MFP out' + os.linesep + '---------------')
    for id, ss in mfp_out.items():
        print(f'{id}: {ss}')
    print('---------------')
