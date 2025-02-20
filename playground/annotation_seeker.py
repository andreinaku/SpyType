from __future__ import annotations
import ast
import astor
import typing
from typing import *
# from _fakeshed import *
import json
import _ast
from copy import deepcopy
import types
from typing_test import create_basetype, AbstractState, FunctionSpec
from collections import defaultdict


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


annotation_exceptions = {
    "_SupportsSomeKindOfPow": "_SupportsSomeKindOfPow: TypeAlias = _SupportsPow2[Any, Any] | _SupportsPow3NoneOnly[Any, Any] | _SupportsPow3[Any, Any, Any]",
}

selftypes = {"Self", "_typeshed.Self", "type[Self]", "type[_typeshed.Self]"}
skips = ["Callable"]

visited_nodes = []
class_stats = dict()
class_stats = {'indie': {'translatable': 0, 'total': 0}}


class ProtocolSeeker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST):
        self.tree = tree
        self.protocols = []
        self.parent_name = "Protocol"

    def visit_ClassDef(self, node: ast.ClassDef):
        if len(node.bases) < 1:
            return
        str_bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                str_bases.append(base.id)
            elif isinstance(base, ast.Subscript) and isinstance(base.value, ast.Name):
                str_bases.append(base.value.id)
            else:
                continue
        if self.parent_name not in str_bases:
            return
        def_str = astor.to_source(node).strip()
        def_str = f"@runtime_checkable\n{def_str}"
        exec(def_str, globals())
        # print(f"evalled {def_str}")
    
    def gather_protocols(self):
        self.visit(self.tree)


class TypeVarSeeker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST):
        self.tree = tree
        self.calls = []
        self.funcname = "TypeVar"
    
    def visit_Assign(self, node: ast.Assign):
        if len(node.targets) > 1:
            return
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
    def __init__(self, tree: ast.AST):
        self.tree = tree

    def visit_Assign(self, node: ast.Assign):
        if node in visited_nodes:
            return
        visited_nodes.append(node)
        if not isinstance(node.targets[0], ast.Name) and node.targets[0] not in annotation_exceptions:
            return
        node_src = astor.to_source(node).strip()
        try:
            exec(node_src, globals())
        except:
            print(f"possibly recursive: {node_src}")

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if node in visited_nodes:
            return
        visited_nodes.append(node)
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
    def __init__(self, tree: ast.AST):
        self.tree = tree
        self.problems = []
        self.goodies = []
        self.current_class = None
    
    def visit_ClassDef(self, node: ast.ClassDef):
        if node in visited_nodes:
            return
        visited_nodes.append(node)
        self.current_class = node
        class_stats[self.current_class.name] = {'translatable': 0, 'total': 0}
        self.generic_visit(node)
        self.current_class = None

    def parse_FunctionDef(self, node:ast.FunctionDef, collect_mode=True):
        if node in visited_nodes:
            return
        if self.current_class is None:
            stats_key = 'indie'
        else:
            stats_key = self.current_class.name
        class_stats[stats_key]['total'] += 1            
        visited_nodes.append(node)
        arg_lists = [node.args.posonlyargs, node.args.args, node.args.kwonlyargs]
        is_translatable = True
        as_in = AbstractState()
        as_out = AbstractState()
        for arg_list in arg_lists:
            if not collect_mode and not is_translatable:
                break
            for _arg in arg_list:
                if not hasattr(_arg, "annotation") or _arg.annotation is None:
                    continue
                try:
                    argstr = astor.to_source(_arg.annotation).strip()
                    if argstr in selftypes:  # the type is the class name, for self-ish annotations
                        argstr = self.current_class.name
                    for skip in skips:
                        if skip in argstr:
                            raise TypeError("(skipped)")
                    evalled = eval(argstr)
                    as_in[_arg.arg] = create_basetype(evalled)
                    self.goodies.append(argstr)
                except Exception as e:
                    self.problems.append(f"{argstr}: {str(e)}")
                    is_translatable = False
                    if not collect_mode:
                        break

        if is_translatable:
            class_stats[stats_key]['translatable'] += 1


    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.parse_FunctionDef(node, False)
        # if node in visited_nodes:
        #     return
        # if self.current_class is None:
        #     stats_key = 'indie'
        # else:
        #     stats_key = self.current_class.name
        # class_stats[stats_key]['total'] += 1            
        # visited_nodes.append(node)
        # arg_lists = [node.args.posonlyargs, node.args.args, node.args.kwonlyargs]
        # is_translatable = True
        # as_in = AbstractState()
        # as_out = AbstractState()
        # for arg_list in arg_lists:
        #     for _arg in arg_list:
        #         if not hasattr(_arg, "annotation") or _arg.annotation is None:
        #             continue
        #         try:
        #             argstr = astor.to_source(_arg.annotation).strip()
        #             if argstr in selftypes:  # the type is the class name, for self-ish annotations
        #                 argstr = self.current_class.name
        #             for skip in skips:
        #                 if skip in argstr:
        #                     raise TypeError("(skipped)")
        #             evalled = eval(argstr)
        #             as_in[_arg.arg] = create_basetype(evalled)
        #             # auxbt = create_basetype(evalled)
        #             self.goodies.append(argstr)
        #         except Exception as e:
        #             self.problems.append(f"{argstr}: {str(e)}")
        #             is_translatable = False
        # if is_translatable:
        #     class_stats[stats_key]['translatable'] += 1


    def collect(self) -> list[str]:
        self.visit(self.tree)
        return self.goodies, self.problems


def seek_from_stubs(fname: str) -> list[str]:
    with open(fname, 'r') as f:
        tree = ast.parse(f.read())
    good_annotations = []
    bad_annotations = []
    for _node in tree.body:
        if _node in visited_nodes:
            continue
        TypeAliasSeeker(_node).gather_typealiases()
        ProtocolSeeker(_node).gather_protocols()
        TypeVarSeeker(_node).gather_typevars()
        g, b = AnnotationSeeker(_node).collect()
        good_annotations += deepcopy(g)
        bad_annotations += deepcopy(b)
    good_annotations = list(set(good_annotations))
    bad_annotations = list(set(bad_annotations))
    return good_annotations, bad_annotations


def check_stats():
    for classname, stats in class_stats.items():
        if stats['total'] < stats['translatable']:
            raise RuntimeError('why?')


def parse_stats():
    check_stats()
    trans = 0
    total = 0
    for classname, stats in class_stats.items():
        total += stats['total']
        trans += stats['translatable']
    percent = trans/total * 100
    print(f"{percent:.2f}% function specifications are translatable")


if __name__ == "__main__":
    fname = "playground/fakeins.pyi"
    goodlist, badlist = seek_from_stubs(fname)
    parse_stats()
    print(f"good = {len(goodlist)} items\nbad = {len(badlist)} items")
    with open("badseeks.json", "w") as f:
        json.dump(badlist, f, indent=4)
    # good_dict = dict()
    # for goodstr in goodlist:
    #     _good = create_basetype(eval(goodstr))
    #     good_dict[goodstr] = str(_good)
    # with open("goodtypes.json", "w") as f:
    #     json.dump(good_dict, f, indent=4)
