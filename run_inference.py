from crackedcfg.builder import NameReplacer, ParamReplacer
from AbstractState import *
from copy import deepcopy
import ast
from crackedcfg import CFG, CFGBuilder
from ExpVisitor import ExpVisit
import fixpoint
import sys


class NameVisitor(ast.NodeVisitor):
    def __init__(self):
        self.names = set()

    def visit_Name(self, node: ast.Name):
        # nodesrc = tosrc(node)
        if not isinstance(node.ctx, ast.Load):
            self.names.add(deepcopy(node.id))

    def get_names(self):
        return self.names


class ASFlow:
    def __init__(self, params=None):
        self.params = params

    @staticmethod
    def merge(as1: AbsState, as2: AbsState):
        result = AbsState.lub(as1, as2)
        return result

    @staticmethod
    def transfer(nodecode, input_as):
        ev = ExpVisit(input_as)
        ev.visit(nodecode)
        return ev.current_as


def get_cfg(filepath, makepng=True):
    cfg = CFGBuilder(separate=True).build_from_file('testcfg', filepath)
    if makepng:
        cfg.build_visual(filepath + '.png', 'png')
    return cfg


def get_params_from_ast(func_ast: ast.FunctionDef):
    param_list = []
    for param in func_ast.args.args:
        param_list.append(param.arg)
    return param_list


def unique_names(func_ast: ast.AST, param_list: list):
    name_func = NameReplacer(param_list)
    name_func.visit(func_ast)


def build_func_cfg(func_name, func_ast, param_list, makepng=True):
    func_cfg = CFGBuilder(separate=True, args=param_list).build(
        name=func_name,
        tree=func_ast,
        add_pass=False
    )
    if makepng:
        func_cfg.build_visual('func.png', 'png')
    return func_cfg


def get_func_cfg(codecfg: CFG, func_name: str, makepng=True):
    func_ast = codecfg.func_asts[func_name]
    param_list = get_params_from_ast(func_ast)
    unique_names(func_ast, param_list)
    func_cfg = build_func_cfg(func_name, func_ast, param_list, makepng)
    return func_cfg


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
    func_cfg = get_func_cfg(cfg, funcname, False)
    # construct the initial abstract state
    init_as = AbsState()
    newva = VarAssign()
    newtc = TypeConstraint()
    functree = cfg.func_asts[funcname]
    names = get_variable_names(functree)
    for varname in func_cfg.params:
        newva[varname] = VarType('T_{}'.format(varname))
    for varname in names:
        newva[varname] = VarType('T_bot')
    init_as.va = newva
    init_as.tc = newtc
    # run the fixpoint algorithm
    entryblock = func_cfg.entryblock
    finalid = func_cfg.finalblocks[0].id
    rounds = fixpoint.analyze(func_cfg.cfgdict, init_as, ASFlow, func_cfg, dbg=True)
    # get the final abstract state
    _out = rounds[len(rounds) - 1]
    if len(func_cfg.finalblocks) != 1:
        raise RuntimeError('Multiple exit blocks not supported yet')
    final_as: AbsState
    final_as = _out[finalid].out_as
    return rounds, final_as


if __name__ == "__main__":
    (rounds, final_as) = run_infer(sys.argv[1], sys.argv[2])
    print(final_as)

