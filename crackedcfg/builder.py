"""
Control flow graph builder.
"""
# Aurelien Coet, 2018.
# Modified by Andrei Nacu, 2020

import ast
import copy
from uuid import uuid4
import astor

import crackedcfg
from .model import Block, Link, CFG
from utils.utils import tosrc
from copy import deepcopy


class NameReplacer(ast.NodeTransformer):
    def __init__(self, args):
        self.params = copy.deepcopy(args)
        self.replacement = dict()
        self.index = 0

    def visit_Assign(self, node: ast.Assign):
        self.generic_visit(node)
        # print('Assign: {}'.format(astor.to_source(node)))
        for target in node.targets:
            if isinstance(target, ast.Name):
                if target.id in self.params:
                    # self.replacement[target.id] = target.id + '_' + str(uuid4()).replace('-', '')
                    self.replacement[target.id] = target.id + '`'
                    target.id = self.replacement[target.id]
        # self.generic_visit(node)
        return node

    def visit_AugAssign(self, node: ast.AugAssign):
        self.visit(node.value)
        binopnode = ast.BinOp(left=deepcopy(node.target), op=node.op, right=deepcopy(node.value))
        targets = [deepcopy(node.target)]
        newnode = ast.Assign(targets=targets, value=binopnode, lineno=node.lineno)
        return self.visit(newnode)

    def visit_Name(self, node: ast.Name):
        # print('Name: {}'.format(astor.to_source(node)))
        if node.id in self.replacement:
            node.id = self.replacement[node.id]
        self.generic_visit(node)
        return node


class ParamReplacer(ast.NodeTransformer):
    def __init__(self, args):
        self.params = copy.deepcopy(args)
        self.replacement = dict()
        index = 1
        for paramname in self.params:
            self.replacement[paramname] = '$p' + str(index)
            index += 1
        newparams = []
        for paramname in self.params:
            newparams.append(self.replacement[paramname])
        self.params = newparams

    def visit_Name(self, node: ast.Name):
        if node.id in self.replacement:
            node.id = self.replacement[node.id]
        self.generic_visit(node)
        return node

    def get_paramlist(self):
        return self.params


def invert(node):
    """
    Invert the operation in an ast node object (get its negation).

    Args:
        node: An ast node object.

    Returns:
        An ast node object containing the inverse (negation) of the input node.
    """
    inverse = {ast.Eq: ast.NotEq,
               ast.NotEq: ast.Eq,
               ast.Lt: ast.GtE,
               ast.LtE: ast.Gt,
               ast.Gt: ast.LtE,
               ast.GtE: ast.Lt,
               ast.Is: ast.IsNot,
               ast.IsNot: ast.Is,
               ast.In: ast.NotIn,
               ast.NotIn: ast.In}

    if type(node) == ast.Compare:
        op = type(node.ops[0])
        inverse_node = ast.Compare(left=node.left, ops=[inverse[op]()],
                                   comparators=node.comparators)
    elif isinstance(node, ast.BinOp) and type(node.op) in inverse:
        op = type(node.op)
        inverse_node = ast.BinOp(node.left, inverse[op](), node.right)
    elif type(node) == ast.Constant and node.value in [True, False]:
        inverse_node = ast.Constant(value=not node.value)
    else:
        inverse_node = ast.UnaryOp(op=ast.Not(), operand=node)

    return inverse_node


def merge_exitcases(exit1, exit2):
    """
    Merge the exitcases of two Links.

    Args:
        exit1: The exitcase of a Link object.
        exit2: Another exitcase to merge with exit1.

    Returns:
        The merged exitcases.
    """
    if exit1:
        if exit2:
            return ast.BoolOp(ast.And(), values=[exit1, exit2])
        return exit1
    return exit2


class CFGBuilder(ast.NodeVisitor):
    """
    Control flow graph builder.

    A control flow graph builder is an ast.NodeVisitor that can walk through
    a program's AST and iteratively build the corresponding CFG.
    """

    def __init__(self, separate=False, args=None):
        super().__init__()
        self.after_loop_block_stack = []
        self.curr_loop_guard_stack = []
        self.current_block = None
        self.separate_node_blocks = separate
        self.params = list()
        if args:
            for arg in args:
                self.params.append(arg)
        # for exception handling
        self.in_try = False
        self.try_info = None
        self.root = None

    # ---------- CFG building methods ---------- #
    def update_cfgdict(self, block: Block):
        self.cfg.cfgdict[block.id] = dict()
        self.cfg.cfgdict[block.id]['parents'] = list()
        self.cfg.cfgdict[block.id]['successors'] = list()
        self.cfg.cfgdict[block.id]['statements'] = block.statements
        self.cfg.cfgdict[block.id]['lineno'] = block.statements[0].lineno
        for predecessor in block.predecessors:
            self.cfg.cfgdict[block.id]['parents'].append(predecessor.source.id)
        for successor in block.exits:
            self.cfg.cfgdict[block.id]['successors'].append(successor.target.id)

    def visit_all_nodes(self, final_nodes, visited=None, curblock=None):
        if not visited:
            visited = []
        if not curblock:
            current_block = self.cfg.entryblock
        else:
            current_block = curblock
        if current_block.id in visited:
            return
        visited.append(current_block.id)
        self.update_cfgdict(current_block)
        if len(current_block.exits) == 0:
            final_nodes.append(current_block)
            return
        for iexit in current_block.exits:
            self.visit_all_nodes(final_nodes, visited, iexit.target)

    def build(self, name, tree, asynchr=False, entry_id=0, add_pass=True):
        """
        Build a CFG from an AST.

        Args:
            name: The name of the CFG being built.
            tree: The root of the AST from which the CFG must be built.
            async: Boolean indicating whether the CFG being built represents an
                   asynchronous function or not. When the CFG of a Python
                   program is being built, it is considered like a synchronous
                   'main' function.
            entry_id: Value for the id of the entry block of the CFG.

        Returns:
            The CFG produced from the AST.
        """
        self.cfg = CFG(name, self.params, asynchr=asynchr)
        # Tracking of the current block while building the CFG.
        self.current_id = entry_id
        self.current_block = self.new_block()
        self.cfg.entryblock = self.current_block
        # Actual building of the CFG is done here.
        self.root = tree
        self.visit(tree)
        visited_nodes = []
        self.clean_cfg(self.cfg.entryblock, visited_nodes)
        finalnodes = []
        self.visit_all_nodes(finalnodes)
        self.cfg.finalblocks = deepcopy(finalnodes)
        if add_pass:
            converging_parents = []
            converging_block = self.new_block()
            self.add_statement(converging_block, ast.Pass())
            self.cfg.cfgdict[converging_block.id] = dict()
            self.cfg.cfgdict[converging_block.id]['parents'] = converging_parents
            self.cfg.cfgdict[converging_block.id]['statements'] = converging_block.statements
            self.cfg.converging_id = converging_block.id
            for finalnode in finalnodes:
                self.add_exit(finalnode, converging_block)
                converging_parents.append(finalnode.id)
        return self.cfg

    def build_from_src(self, name, src):
        """
        Build a CFG from some Python source code.

        Args:
            name: The name of the CFG being built.
            src: A string containing the source code to build the CFG from.

        Returns:
            The CFG produced from the source code.
        """
        tree = ast.parse(src, mode='exec')
        return self.build(name, tree)

    def build_from_file(self, name, filepath):
        """
        Build a CFG from some Python source file.

        Args:
            name: The name of the CFG being built.
            filepath: The path to the file containing the Python source code
                      to build the CFG from.

        Returns:
            The CFG produced from the source file.
        """
        with open(filepath, 'r') as src_file:
            src = src_file.read()
            return self.build_from_src(name, src)

    # ---------- Graph management methods ---------- #
    def new_block(self):
        """
        Create a new block with a new id.

        Returns:
            A Block object with a new unique id.
        """
        self.current_id += 1
        return Block(self.current_id)

    def add_statement(self, block, statement):
        """
        Add a statement to a block.

        Args:
            block: A Block object to which a statement must be added.
            statement: An AST node representing the statement that must be
                       added to the current block.
        """
        block.statements.append(statement)

    def add_exit(self, block, nextblock, exitcase=None):
        """
        Add a new exit to a block.

        Args:
            block: A block to which an exit must be added.
            nextblock: The block to which control jumps from the new exit.
            exitcase: An AST node representing the 'case' (or condition)
                      leading to the exit from the block in the program.
        """
        newlink = Link(block, nextblock, exitcase)
        block.exits.append(newlink)
        nextblock.predecessors.append(newlink)

    def new_loopguard(self):
        """
        Create a new block for a loop's guard if the current block is not
        empty. Links the current block to the new loop guard.

        Returns:
            The block to be used as new loop guard.
        """
        if (self.current_block.is_empty() and
                len(self.current_block.exits) == 0):
            # If the current block is empty and has no exits, it is used as
            # entry block (condition test) for the loop.
            loopguard = self.current_block
        else:
            # Jump to a new block for the loop's guard if the current block
            # isn't empty or has exits.
            loopguard = self.new_block()
            self.add_exit(self.current_block, loopguard)
        return loopguard

    def new_functionCFG(self, node, asynchr=False):
        """
        Create a new sub-CFG for a function definition and add it to the
        function CFGs of the CFG being built.

        Args:
            node: The AST node containing the function definition.
            async: Boolean indicating whether the function for which the CFG is
                   being built is asynchronous or not.
        """
        self.current_id += 1
        # A new sub-CFG is created for the body of the function definition and
        # added to the function CFGs of the current CFG.
        func_body = ast.Module(body=node.body)
        func_builder = CFGBuilder(separate=True)
        for argument in node.args.args:
            func_builder.params.append(argument.arg)
        func_name = node.name + "("
        for parameter in func_builder.params:
            func_name += parameter + ", "
        if not len(func_builder.params):
            func_name = func_name + ")"
        else:
            func_name = func_name[:-2] + ")"
        new_func_body = copy.deepcopy(func_body)
        name_func = NameReplacer(func_builder.params)
        name_func.visit(new_func_body)
        self.cfg.functioncfgs[node.name] = func_builder.build(func_name,
                                                              new_func_body,
                                                              asynchr,
                                                              self.current_id)
        self.current_id = func_builder.current_id + 1

    def clean_cfg(self, block, visited, new_id=1):
        """
        Remove the useless (empty) blocks from a CFG.

        Args:
            block: The block from which to start traversing the CFG to clean
                   it.
            visited: A list of blocks that already have been visited by
                     clean_cfg (recursive function).
        """
        # Don't visit blocks twice.
        if block in visited:
            return
        visited.append(block)

        # Empty blocks are removed from the CFG.
        if block.is_empty():
            for pred in block.predecessors:
                for exit in block.exits:
                    self.add_exit(pred.source, exit.target,
                                  merge_exitcases(pred.exitcase,
                                                  exit.exitcase))
                    # Check if the exit hasn't yet been removed from
                    # the predecessors of the target block.
                    if exit in exit.target.predecessors:
                        exit.target.predecessors.remove(exit)
                # Check if the predecessor hasn't yet been removed from
                # the exits of the source block.
                if pred in pred.source.exits:
                    pred.source.exits.remove(pred)

            block.predecessors = []
            # as the exits may be modified during the recursive call, it is unsafe to iterate on block.exits
            # Created a copy of block.exits before calling clean cfg , and iterate over it instead.
            for exit in block.exits[:]:
                self.clean_cfg(exit.target, visited, new_id)
            block.exits = []
        else:
            block.new_id = new_id
            for exit in block.exits[:]:
                self.clean_cfg(exit.target, visited, new_id+1)

    # ---------- AST Node visitor methods ---------- #
    def goto_new_block(self, node):
        if self.separate_node_blocks:
            newblock = self.new_block()
            self.add_exit(self.current_block, newblock)
            if self.in_try:
                for hinfo in self.try_info['handlers_info']:
                    self.add_exit(self.current_block, hinfo['start_block'])
            self.current_block = newblock
        self.generic_visit(node)

    def visit_Expr(self, node):
        self.add_statement(self.current_block, node)
        self.goto_new_block(node)

    def visit_Call(self, node):
        def visit_func(node):
            if type(node) == ast.Name:
                return node.id
            elif type(node) == ast.Attribute:
                # Recursion on series of calls to attributes.
                func_name = visit_func(node.value)
                func_name += "." + node.attr
                return func_name
            elif type(node) == ast.Str:
                return node.s
            elif type(node) == ast.Subscript:
                return node.value.id
            elif type(node) == ast.Call:
                try:
                    return node.func.attr
                except:
                    return node.func.id
                # return node.func.id

        func = node.func
        func_name = visit_func(func)
        # self.current_block.func_calls.append(func_name)

    # def visit_Call(self, node):
    #     self.add_statement(self.current_block, node)
    #     self.goto_new_block(node)

    def visit_Assign(self, node):
        self.add_statement(self.current_block, node)
        self.goto_new_block(node)

    def visit_AnnAssign(self, node):
        self.add_statement(self.current_block, node)
        self.goto_new_block(node)

    def visit_AugAssign(self, node):
        self.add_statement(self.current_block, node)
        self.goto_new_block(node)

    def visit_Raise(self, node):
        # todo: see if it needs anything else here
        self.add_statement(self.current_block, node)
        self.goto_new_block(node)

    def visit_Assert(self, node):
        self.add_statement(self.current_block, node)
        # New block for the case in which the assertion 'fails'.
        failblock = self.new_block()
        self.add_exit(self.current_block, failblock, invert(node.test))
        # If the assertion fails, the current flow ends, so the fail block is a
        # final block of the CFG.
        self.cfg.finalblocks.append(failblock)
        # If the assertion is True, continue the flow of the program.
        successblock = self.new_block()
        self.add_exit(self.current_block, successblock, node.test)
        self.current_block = successblock
        self.goto_new_block(node)

    def visit_If(self, node):
        # Add the If statement at the end of the current block.
        self.add_statement(self.current_block, node)

        # Create a new block for the body of the if.
        if_block = self.new_block()
        self.add_exit(self.current_block, if_block, node.test)

        # Create a block for the code after the if-else.
        afterif_block = self.new_block()

        # New block for the body of the else if there is an else clause.
        if len(node.orelse) != 0:
            else_block = self.new_block()
            self.add_exit(self.current_block, else_block, invert(node.test))
            self.current_block = else_block
            # Visit the children in the body of the else to populate the block.
            for child in node.orelse:
                self.visit(child)
            # If encountered a break, exit will have already been added
            if not self.current_block.exits:
                self.add_exit(self.current_block, afterif_block)
        else:
            self.add_exit(self.current_block, afterif_block, invert(node.test))

        # Visit children to populate the if block.
        self.current_block = if_block
        for child in node.body:
            self.visit(child)
        if not self.current_block.exits:
            self.add_exit(self.current_block, afterif_block)

        # Continue building the CFG in the after-if block.
        self.current_block = afterif_block

    def visit_Try(self, node: ast.Try):
        backup_currentblock = self.current_block
        aftertry_block = self.new_block()
        finally_block = None
        if len(node.finalbody):
            finally_block = aftertry_block
        '''
        {
            'finally_block': CFG block of the finally node
            'handlers_info': [
                {
                  'name': name of error (FileNotFoundError, TypeError etc.)
                  'start_block': CFG start block for the handler
                  'end_block': CFG end block for the handler
                }, ...
            ]
        }
        '''
        try_info = dict()
        self.try_info = try_info
        try_info['finally_block'] = finally_block
        try_info['handlers_info'] = []
        handlers_info = try_info['handlers_info']
        # first compose all the handler blocks
        for handler in node.handlers:
            handler_block = self.new_block()
            new_handler_info = {
                'name': handler.type,
                'start_block': handler_block,
                'end_block': None
            }
            self.current_block = handler_block
            for handler_child in handler.body:
                self.visit(handler_child)
            new_handler_info['end_block'] = self.current_block
            handlers_info.append(new_handler_info)
        self.current_block = backup_currentblock
        # every instruction in the try-block is susceptible to an exception
        self.in_try = True
        self.try_info = try_info
        for trychild in node.body:
            self.visit(trychild)
        self.in_try = False
        self.try_info = None
        # add the exit after the try-block at the end of the try-block instructions
        self.add_exit(self.current_block, aftertry_block)
        # continue from there
        self.current_block = aftertry_block
        for finalchild in node.finalbody:
            self.visit(finalchild)
        for hinfo in handlers_info:
            self.add_exit(hinfo['end_block'], aftertry_block)
        self.try_info = None

    def visit_While(self, node):
        loop_guard = self.new_loopguard()
        self.current_block = loop_guard
        self.add_statement(self.current_block, node)
        self.curr_loop_guard_stack.append(loop_guard)
        # New block for the case where the test in the while is True.
        while_block = self.new_block()
        self.add_exit(self.current_block, while_block, node.test)

        # New block for the case where the test in the while is False.
        afterwhile_block = self.new_block()
        self.after_loop_block_stack.append(afterwhile_block)
        inverted_test = invert(node.test)
        # Skip shortcut loop edge if while True:
        # if not (isinstance(inverted_test, ast.Constant) and inverted_test.value is False):
        self.add_exit(self.current_block, afterwhile_block, inverted_test)

        # Populate the while block.
        self.current_block = while_block
        for child in node.body:
            self.visit(child)
        if not self.current_block.exits:
            # Did not encounter a break statement, loop back
            # psf: neeeeee, just get outta here
            self.add_exit(self.current_block, afterwhile_block)
            # todo: check this
            self.add_exit(self.current_block, loop_guard)

        # Continue building the CFG in the after-while block.
        self.current_block = afterwhile_block
        self.after_loop_block_stack.pop()
        self.curr_loop_guard_stack.pop()

    def visit_For(self, node):
        if isinstance(node.target, ast.Name):
            self.cfg.varset.add(node.target.id)
        loop_guard = self.new_loopguard()
        self.current_block = loop_guard
        self.add_statement(self.current_block, node)
        self.curr_loop_guard_stack.append(loop_guard)
        # New block for the body of the for-loop.
        for_block = self.new_block()
        self.add_exit(self.current_block, for_block, node.iter)

        # Block of code after the for loop.
        afterfor_block = self.new_block()
        self.add_exit(self.current_block, afterfor_block)
        self.after_loop_block_stack.append(afterfor_block)
        self.current_block = for_block

        # Populate the body of the for loop.
        for child in node.body:
            self.visit(child)
        if not self.current_block.exits:
            # Did not encounter a break
            # psf: neeeee, just get outta here
            self.add_exit(self.current_block, afterfor_block)

        # Continue building the CFG in the after-for block.
        self.current_block = afterfor_block
        # Popping the current after loop stack,taking care of errors in case of nested for loops
        self.after_loop_block_stack.pop()
        self.curr_loop_guard_stack.pop()

    def visit_Break(self, node):
        assert len(self.after_loop_block_stack), "Found break not inside loop"
        self.add_exit(self.current_block, self.after_loop_block_stack[-1])

    def visit_Continue(self, node):
        assert len(self.curr_loop_guard_stack), "Found continue outside loop"
        self.add_exit(self.current_block,self.curr_loop_guard_stack[-1])

    def visit_Import(self, node):
        self.add_statement(self.current_block, node)
        self.goto_new_block(node)

    def visit_ImportFrom(self, node):
        self.add_statement(self.current_block, node)
        self.goto_new_block(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.cfg.class_asts[node.name] = node
        dummy_node = copy.deepcopy(node)
        dummy_node.body = []
        self.add_statement(self.current_block, dummy_node)
        newblock = self.new_block()
        self.add_exit(self.current_block, newblock)
        self.current_block = newblock

    # def visit_FunctionDef(self, node: ast.FunctionDef):
    #     self.cfg.func_asts[node.name] = node
    #     self.add_statement(self.current_block, node)
    #     if self.separate_node_blocks:
    #         newblock = self.new_block()
    #         self.add_exit(self.current_block, newblock)
    #     self.new_functionCFG(node, asynchr=False)
    #     if self.separate_node_blocks:
    #         self.current_block = newblock

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node == self.root:
            self.generic_visit(node)
        else:
            self.cfg.func_asts[node.name] = node
            dummy_node = copy.deepcopy(node)
            dummy_node.body = []
            self.add_statement(self.current_block, dummy_node)
            newblock = self.new_block()
            self.add_exit(self.current_block, newblock)
            self.current_block = newblock

    def visit_AsyncFunctionDef(self, node):
        self.add_statement(self.current_block, node)
        self.new_functionCFG(node, asynchr=True)

    def visit_Await(self, node):
        afterawait_block = self.new_block()
        self.add_exit(self.current_block, afterawait_block)
        self.goto_new_block(node)
        self.current_block = afterawait_block

    def visit_Return(self, node):
        # Continue in a new block but without any jump to it -> all code after
        # the return statement will not be included in the CFG.
        if self.try_info and self.try_info['finally_block']:
            self.add_exit(self.current_block, self.try_info['finally_block'])
        else:
            self.add_statement(self.current_block, node)
            self.cfg.finalblocks.append(self.current_block)
        self.current_block = self.new_block()

    def visit_Yield(self, node):
        self.cfg.asynchr = True
        afteryield_block = self.new_block()
        self.add_exit(self.current_block, afteryield_block)
        self.current_block = afteryield_block

    def visit_Name(self, node):
        self.cfg.varset.add(node.id)
        # self.goto_new_block(node)

    def visit_Pass(self, node):
        self.add_statement(self.current_block, node)
        self.goto_new_block(node)
