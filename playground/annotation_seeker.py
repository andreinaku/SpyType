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

    def visit_AnnAssign(self, node: ast.AnnAssign):
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

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for arg in node.args.args:
            if not hasattr(arg, "annotation") or arg.annotation is None:
                continue
            try:
                argstr = astor.to_source(arg.annotation).strip()
                eval(argstr)
                self.goodies.append(argstr)
            except Exception as e:
                # print(f"not evalled {argstr}")
                self.problems.append(f"{argstr}: {str(e)}")

    def collect(self) -> list[str]:
        self.visit(self.tree)
        # self.goodies = list(set(self.goodies))
        # self.problems = list(set(self.problems))
        return self.goodies, self.problems


def seek_from_stubs(fname: str) -> list[str]:
    with open(fname, 'r') as f:
        tree = ast.parse(f.read())
    good_annotations = []
    bad_annotations = []
    for _node in tree.body:    
        TypeAliasSeeker(_node).gather_typealiases()
        ProtocolSeeker(_node).gather_protocols()
        TypeVarSeeker(_node).gather_typevars()
        g, b = AnnotationSeeker(_node).collect()
        good_annotations += deepcopy(g)
        bad_annotations += deepcopy(b)
    good_annotations = list(set(good_annotations))
    bad_annotations = list(set(bad_annotations))
    return good_annotations, bad_annotations


if __name__ == "__main__":
    fname = "playground/fakeins.pyi"
    goodlist, badlist = seek_from_stubs(fname)
    print(f"good = {len(goodlist)} items\nbad = {len(badlist)} items")
    with open("badseeks.json", "w") as f:
        json.dump(badlist, f, indent=4)
