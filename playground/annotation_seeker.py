from __future__ import annotations
import ast
import astor
from typing import *
import typing
from types import *
import types
# from _fakeshed import *
import json
import _ast
from copy import deepcopy
# from typing_test import create_basetype, AbstractState, FunctionSpec
from typing_test import *
from io import *
import re


from _fakeshed import (
    AnyStr_co,
    ConvertibleToFloat,
    ConvertibleToInt,
    FileDescriptorOrPath,
    MaybeNone,
    OpenBinaryMode,
    OpenBinaryModeReading,
    OpenBinaryModeUpdating,
    OpenBinaryModeWriting,
    OpenTextMode,
    ReadableBuffer,
    SupportsAdd,
    SupportsAiter,
    SupportsAnext,
    SupportsDivMod,
    SupportsFlush,
    SupportsIter,
    SupportsKeysAndGetItem,
    SupportsLenAndGetItem,
    SupportsNext,
    SupportsRAdd,
    SupportsRDivMod,
    SupportsRichComparison,
    SupportsRichComparisonT,
    SupportsWrite
)


def is_protocol_classdef(node: ast.ClassDef) -> bool:
    protocol_base = "Protocol"
    if len(node.bases) < 1:
        return False
    str_bases = []
    for base in node.bases:
        if isinstance(base, ast.Name):
            str_bases.append(base.id)
        elif isinstance(base, ast.Subscript) and isinstance(base.value, ast.Name):
            str_bases.append(base.value.id)
        else:
            continue
    if protocol_base not in str_bases:
        return False
    return True


class ProtocolSeeker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST, visited_nodes: list[ast.AST]):
        self.tree = tree
        self.protocols = []
        self.parent_name = "Protocol"
        self.visited_nodes = visited_nodes

    def visit_ClassDef(self, node: ast.ClassDef):
        if node in self.visited_nodes:
            return
        if not is_protocol_classdef(node):
            return
        def_str = astor.to_source(node).strip()
        def_str = f"@runtime_checkable\n{def_str}"
        exec(def_str, globals())
        self.visited_nodes.append(node)
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self.visited_nodes.append(item)
    
    def gather_protocols(self):
        self.visit(self.tree)


class TypeVarSeeker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST, visited_nodes: list[ast.AST]):
        self.tree = tree
        self.calls = []
        self.funcname = "TypeVar"
        self.visited_nodes = visited_nodes
    
    def visit_Assign(self, node: ast.Assign):
        if len(node.targets) > 1:
            return
        if node in self.visited_nodes:
            return
        self.visited_nodes.append(node)
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            return
        if not isinstance(node.value, ast.Call):
            return
        if not isinstance(node.value.func, ast.Name) and node.value.func.id != self.funcname:
            return
        if len(node.value.args) < 1 and not isinstance(node.value.args[0], ast.Constant):
            return
        assign_str = astor.to_source(node).strip()
        exec(assign_str, globals())
        # print(f"execced {assign_str}")

    def gather_typevars(self):
        self.visit(self.tree)


class TypeAliasSeeker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST, visited_nodes: list[ast.AST]):
        self.tree = tree
        self.alias_exceptions = {
           "_SupportsSomeKindOfPow": "_SupportsSomeKindOfPow: TypeAlias = _SupportsPow2[Any, Any] | _SupportsPow3NoneOnly[Any, Any] | _SupportsPow3[Any, Any, Any]",
        }
        self.visited_nodes = visited_nodes

    def visit_Assign(self, node: ast.Assign):
        if node in self.visited_nodes:
            return
        self.visited_nodes.append(node)
        if not isinstance(node.targets[0], ast.Name) and node.targets[0] not in self.alias_exceptions:
            return
        node_src = astor.to_source(node).strip()
        try:
            exec(node_src, globals())
        except:
            print(f"possibly recursive: {node_src}")

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if node in self.visited_nodes:
            return
        self.visited_nodes.append(node)
        if not hasattr(node.annotation, "id"):
            return
        if node.annotation.id != "TypeAlias":
            return
        node_src = astor.to_source(node).strip()
        try:
            exec(node_src, globals())
        except:
            print(f"possibly recursive: {node_src}")

    def gather_typealiases(self):
        self.visit(self.tree)


class AnnotationSeeker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST,
                 visited_nodes: list[ast.AST],
                 class_stats: dict[str, dict[str, int]],
                 class_dict: dict[str, dict[str, list[FunctionSpec]]],
                 collect_mode: bool
                 ):
        self.tree = tree
        self.problems = []
        self.goodies = []
        self.current_class = None
        self.selftypes = {"Self", "_typeshed.Self", "type[Self]", "type[_typeshed.Self]", "list[_typeshed.Self]"}
        self.skips = ["Callable"]
        self.visited_nodes = visited_nodes
        self.class_stats = class_stats
        self.class_dict = class_dict
        self.collect_mode = collect_mode

    def visit_ClassDef(self, node: ast.ClassDef):
        if is_protocol_classdef(node):
            return
        if node in self.visited_nodes:
            return
        self.visited_nodes.append(node)
        self.current_class = node
        self.class_stats[self.current_class.name] = {'translatable': 0, 'total': 0}
        self.generic_visit(node)
        self.current_class = None

    def add_to_class_dict(self, classname: str, funcname: str, funcspec: FunctionSpec):
        if classname in self.class_dict:
            if funcname in self.class_dict[classname]:
                self.class_dict[classname][funcname].append(funcspec)
            else:
                self.class_dict[classname][funcname] = [funcspec]
        else:
            self.class_dict[classname] = {funcname: [funcspec]}

    def visit_FunctionDef(self, node:ast.FunctionDef):

        def annotation_to_basetype(annot_node: ast.AST) -> BaseType:
            argstr = astor.to_source(annot_node).strip()
            if argstr in self.selftypes:  # the type is the class name, for self-ish annotations
                argstr = self.current_class.name
            for skip in self.skips:
                if skip in argstr:
                    raise TypeError(f"{argstr}: (skipped)")
            try:
                evalled = eval(argstr)
            except Exception as e:
                raise Exception(f"{argstr}: {str(e)}")
            return argstr, create_basetype(evalled)

        if node in self.visited_nodes:
            return
        if self.current_class is None:
            stats_key = 'indie'
        else:
            stats_key = self.current_class.name
        self.class_stats[stats_key]['total'] += 1   
        self.visited_nodes.append(node)
        arg_lists = [node.args.posonlyargs, node.args.args]
        is_translatable = True
        as_in = AbstractState()
        as_out = AbstractState()
        for arg_list in arg_lists:
            if not self.collect_mode and not is_translatable:
                break
            for _arg in arg_list:
                if not hasattr(_arg, "annotation") or _arg.annotation is None:
                    continue
                try:
                    argstr, bt = annotation_to_basetype(_arg.annotation)
                    as_in[_arg.arg] = bt
                    self.goodies.append(argstr)
                except Exception as e:
                    self.problems.append(str(e))
                    is_translatable = False
                    if not self.collect_mode:
                        break
        if not is_translatable and not self.collect_mode:
            return
        
        _arg = node.args.vararg
        if hasattr(_arg, "annotation") and _arg.annotation is not None:
            try:
                argstr, bt = annotation_to_basetype(_arg.annotation)
                as_in["*" + _arg.arg] = bt
            except Exception as e:
                self.problems.append(str(e))
                is_translatable = False
                if not self.collect_mode:
                    return
        if not is_translatable and not self.collect_mode:
            return
        

        for _arg in node.args.kwonlyargs:
            if hasattr(_arg, "annotation") and _arg.annotation is not None:
                try:
                    argstr, bt = annotation_to_basetype(_arg.annotation)
                    as_in["**" + _arg.arg] = bt
                except Exception as e:
                    self.problems.append(str(e))
                    is_translatable = False
                    if not self.collect_mode:
                        return
        if not is_translatable and not self.collect_mode:
            return

        _arg = node.args.kwarg
        if hasattr(_arg, "annotation") and _arg.annotation is not None:
            try:
                argstr, bt = annotation_to_basetype(_arg.annotation)
                as_in["**" + _arg.arg] = bt
            except Exception as e:
                self.problems.append(str(e))
                is_translatable = False
                if not self.collect_mode:
                    return
        if not is_translatable and not self.collect_mode:
            return
        
        try:
            ret_str = astor.to_source(node.returns).strip()
            if ret_str in self.selftypes:  # the type is the class name, for self-ish annotations
                ret_str = self.current_class.name
            for skip in self.skips:
                if skip in ret_str:
                    raise TypeError("(skipped)")
            evalled = eval(ret_str)
            as_out['return'] = create_basetype(evalled)
        except Exception as e: 
            self.problems.append(f"{ret_str}: {str(e)}")
            is_translatable = False
            if not self.collect_mode:
                return
        if not is_translatable:
            return
        fs = FunctionSpec(as_in, as_out)
        self.add_to_class_dict(stats_key, node.name, fs)
        self.class_stats[stats_key]['translatable'] += 1

    def collect(self) -> list[str]:
        self.visit(self.tree)
        return self.goodies, self.problems
    

def seek_from_stubs(fname: str,
                    visited_nodes: list[ast.AST],
                    class_stats: dict[str, dict[str, int]],
                    class_dict: dict[str, list[FunctionSpec]],
                    collect_mode: bool) -> list[str]:
    with open(fname, 'r') as f:
        tree = ast.parse(f.read())
    good_annotations = []
    bad_annotations = []
    for _node in tree.body:
        if _node in visited_nodes:
            continue
        TypeAliasSeeker(_node, visited_nodes).gather_typealiases()
        ProtocolSeeker(_node, visited_nodes).gather_protocols()
        TypeVarSeeker(_node, visited_nodes).gather_typevars()
        g, b = AnnotationSeeker(_node, visited_nodes, class_stats, class_dict, collect_mode).collect()
        good_annotations += deepcopy(g)
        bad_annotations += deepcopy(b)
    good_annotations = list(set(good_annotations))
    bad_annotations = list(set(bad_annotations))
    return good_annotations, bad_annotations


def check_stats(class_stats: dict[str, dict[str, int]]):
    for classname, stats in class_stats.items():
        if stats['total'] < stats['translatable']:
            raise RuntimeError('why?')


def parse_stats(class_stats: dict[str, dict[str, int]]):
    check_stats(class_stats)
    trans = 0
    total = 0
    for classname, stats in class_stats.items():
        total += stats['total']
        trans += stats['translatable']
    percent = trans/total * 100
    print(f"{percent:.2f}% function specifications are translatable")


def serialize_class_dict(cd):
    serialized = {class_name: {funcname: [str(fs) for fs in fs_list] for funcname, fs_list in func_info.items()} for class_name, func_info in cd.items()}
    return serialized


if __name__ == "__main__":
    fname = "playground/fakeins.pyi"
    visited_nodes = []
    class_stats = dict()
    class_stats = {'indie': {'translatable': 0, 'total': 0}}
    class_dict = dict()

    goodlist, badlist = seek_from_stubs(fname, visited_nodes, class_stats, class_dict, False)
    parse_stats(class_stats)
    print(f"good = {len(goodlist)} items\nbad = {len(badlist)} items")
    with open("badseeks.json", "w") as f:
        json.dump(badlist, f, indent=4)
    with open("class_dict.json", "w") as f:
        json.dump(serialize_class_dict(class_dict), f, indent=4)
