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
        func_cfg.build_visual(f'inferfunc_{func_name}', 'png')
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


def run_infer_on_file(filepath, funclist=None):
    cfg = get_cfg(filepath, makepng=False)
    func_info = dict()    
    for funcname in cfg.func_asts:
        if funclist is not None and funcname not in funclist:
            continue
        func_info[funcname] = dict()
        func_info[funcname]['mfp_in'], func_info[funcname]['mfp_out'] = run_infer_on_func(cfg, funcname)
        func_cfg = get_func_cfg(cfg, funcname, True)
        final_id = func_cfg.finalblocks[0].id
        func_info[funcname]['final_state'] = func_info[funcname]['mfp_out'][final_id]
    return func_info


def state_as_spec(_st: State, params: list[str]):
    spec = FuncSpec()
    st = _st.vartypes_to_spectypes()    
    for expr, bt in st.assignment.items():
        if expr not in params:
            continue
        spec.in_state.assignment[expr] = deepcopy(bt)
    if RETURN_NAME not in st.assignment:
        spec.out_state.assignment[RETURN_NAME] = Basetype({PyType(type(None))})
        return spec
    spec.out_state.assignment[RETURN_NAME] = deepcopy(st.assignment[RETURN_NAME])
    #
    spec = spec.remove_irrelevant_vartypes() 
    #
    return spec


def states_lub(ss: StateSet) -> StateSet:
    st: State
    new_state = State()
    for st in ss:
        new_state = State.lub(new_state, st)
    return StateSet({new_state})


def stateset_as_spec(_ss: StateSet, cfg: CFG, fname: str, reduce_type):
    newset = set()
    func_cfg = get_func_cfg(cfg, fname, makepng=False)
    ss = states_lub(_ss)
    for st in ss:
        spec = state_as_spec(st, func_cfg.params, reduce_type)
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
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file containing Python functions')
    parser.add_argument('-f', '--functions', nargs='*', type=str, help='Optional list of functions to be inferred. If this is omitted, then all functions from the input file are inferred')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to the output file for writing results')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show information in every CFG node (inferfunc_* images)')
    parser.add_argument(
        '-r', '--reduce-type',
        choices=['restrictive', 'generic', 'default'],
        default='default',
        help='(EXPERIMENTAL) Specify how types for function parameters are reduced. Choices are restrictive, generic, or default (default is chosen if this argument is omitted).'
    )
    args = parser.parse_args()
    #
    if args.reduce_type == 'restrictive':
        reduce_type = ReduceTypes.RESTRICTIVE
    elif args.reduce_type == 'generic':
        reduce_type = ReduceTypes.GENERIC
    elif args.reduce_type == 'default':
        reduce_type = ReduceTypes.DEFAULT
    else:
        raise RuntimeError('Invalid reduce type')
    outpath = args.output
    start_time = time.time()
    # testpath = 'benchmarks/mine/benchfuncs_typpete.py'
    finfo = run_infer_on_file(args.input, args.functions)
    end_time = time.time()
    diff_time = end_time - start_time
    cfg = get_cfg(args.input, makepng=False)
    delim = '---------------------------------'
    to_print = ''
    for fname, info in finfo.items():
        if args.verbose:
            nodes = info['mfp_in'].keys()
            to_print += f'{delim}{os.linesep}{fname} program points{os.linesep}{delim}{os.linesep}'
            for nodeid in nodes:
                inlub = states_lub(info["mfp_in"][nodeid])
                outlub = states_lub(info["mfp_out"][nodeid])
                to_print += f'{nodeid} : {{{os.linesep}'
                to_print += f'\tinput:{os.linesep}{info["mfp_in"][nodeid].str_as_list()} = {inlub}{os.linesep}{os.linesep}'
                to_print += f'\toutput:{os.linesep}{info["mfp_out"][nodeid].str_as_list()} = {outlub}{os.linesep}'
                to_print += f'}}{os.linesep}{os.linesep}'
            to_print += f'{os.linesep}'
        to_print += f'{delim}{os.linesep}{fname} specs{os.linesep}{delim}{os.linesep}'
        specset = stateset_as_spec(info['final_state'], cfg, fname, reduce_type)
        to_print += pprint_set(specset)
        to_print += f'{os.linesep}{os.linesep}'
    to_print += f'Time: {diff_time:4f}s'
    open(outpath, 'w').write(to_print)
