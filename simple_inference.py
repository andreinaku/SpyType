import os, sys
import time
import argparse
sys.path.append(os.getcwd())
from crackedcfg import CFG, CFGBuilder
from crackedcfg.builder import NameReplacer
from statev2.basetype import *
from statev2.transfer import *
import worklist as worklist


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
    # variable_names = []
    # # Check if the node is a variable definition
    # if isinstance(node, ast.Assign):
    #     # Get the name of the variable
    #     for target in node.targets:
    #         if not isinstance(target, ast.Name):
    #             continue
    #         variable_names.append(target.id)
    #     return variable_names
    # # Recursively search for variable definitions in child nodes
    # for child_node in ast.iter_child_nodes(node):
    #     if not isinstance(child_node, ast.FunctionDef) and not isinstance(child_node, ast.ClassDef):
    #         variable_names += get_variable_names(child_node)
    # return variable_names
    nv = NameVisitor()
    nv.visit(node)
    return nv.get_names()


def run_infer_on_func(cfg, funcname):
    # get the function CFG based on the function name
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


def run_infer(filename, funcname):
    cfg = get_cfg(filename, makepng=False)
    return run_infer_on_func(cfg, funcname)


def run_infer_on_file(filepath):
    cfg = get_cfg(filepath, makepng=False)
    func_info = dict()    
    for funcname in cfg.func_asts:
        func_info[funcname] = dict()
        # print('---------------')
        # print(funcname)
        # print('---------------')
        func_info[funcname]['mfp_in'], func_info[funcname]['mfp_out'] = run_infer_on_func(cfg, funcname)
        func_cfg = get_func_cfg(cfg, funcname, True)
        final_id = func_cfg.finalblocks[0].id
        func_info[funcname]['final_state'] = func_info[funcname]['mfp_out'][final_id]
        # print('---------------')
        # print('MFP in' + os.linesep + '---------------')
        # for id, ss in mfp_in.items():
        #     print(f'{id}: {ss}')
        # print('---------------')
        # print('MFP out' + os.linesep + '---------------')
        # for id, ss in mfp_out.items():
        #     print(f'{id}: {ss}')
        # print('---------------')
    return func_info


def state_as_spec(st: State, params: list[str]):
    spec = FuncSpec()
    for expr, bt in st.assignment.items():
        if expr not in params:
            continue
        spec.in_state.assignment[expr] = deepcopy(bt)
    if RETURN_NAME not in st.assignment:
        spec.out_state.assignment[RETURN_NAME] = Basetype({PyType(type(None))})
        return spec
    spec.out_state.assignment[RETURN_NAME] = deepcopy(st.assignment[RETURN_NAME])
    return spec


def states_lub(ss: StateSet) -> StateSet:
    st: State
    new_state = State()
    for st in ss:
        new_state = State.lub(new_state, st)
    return StateSet({new_state})


def stateset_as_spec(_ss: StateSet, cfg: CFG, fname: str):
    newset = set()
    func_cfg = get_func_cfg(cfg, fname, makepng=False)
    ss = states_lub(_ss)
    for st in ss:
        spec = state_as_spec(st, func_cfg.params)
        newset.add(deepcopy(spec))
    return newset


def pprint_set(seth):
    to_print = f'{fname} : {{\n'
    for spec in seth:
        to_print += f'\t{spec},\n'
    to_print += f'}}\n'
    return to_print


if __name__ == "__main__":
    # arguments
    parser = argparse.ArgumentParser(description='A POC for Python function type inference using Maude solver.')
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the input file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to the output file')
    parser.add_argument('-v', '--verbose', type=bool, default=False, required=False, help='Path to the output file')
    args = parser.parse_args()
    #
    outpath = args.output
    start_time = time.time()
    # testpath = 'benchmarks/mine/benchfuncs_typpete.py'
    finfo = run_infer_on_file(args.file)
    end_time = time.time()
    diff_time = end_time - start_time
    cfg = get_cfg(args.file, makepng=False)
    delim = '---------------------------------'
    to_print = ''
    for fname, info in finfo.items():
        if args.verbose:
            nodes = info['mfp_in'].keys()
            to_print += f'{delim}\n{fname} program points\n{delim}\n'
            for nodeid in nodes:
                to_print += f'{nodeid} : {{\n'
                to_print += f'\tinput: {info['mfp_in'][nodeid]}\n\n'
                to_print += f'\toutput: {info['mfp_out'][nodeid]}\n'
                to_print += f'}}\n'
            to_print += '\n'
        to_print += f'{delim}\n{fname} specs\n{delim}\n'
        specset = stateset_as_spec(info['final_state'], cfg, fname)
        to_print += pprint_set(specset)
        to_print += '\n\n'
    to_print += f'Time: {diff_time:4f}s'
    open(outpath, 'w').write(to_print)
