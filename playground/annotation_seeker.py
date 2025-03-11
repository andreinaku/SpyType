from __future__ import annotations
import ast
import astor
from typing import *
import typing
from types import *
import types
# from _fakeshed import *
import json
from copy import deepcopy
from typing_test import *
from io import *
from dataclasses import dataclass
from pprint import pprint
import os
import logging


tv_declarations = []
logging.basicConfig(
    filename='seeker.err',  # Log file name
    level=logging.ERROR,        # Log level (ERROR logs exceptions)
    format='%(asctime)s - %(levelname)s - %(message)s'
)
translated_funcs = 0
not_translated_funcs = 0


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


class NotTranslatableException(Exception):
    pass


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


class AssignSeeker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST, visited_nodes: list[ast.AST]):
        self.tree = tree
        self.alias_exceptions = {
           "_SupportsSomeKindOfPow": "_SupportsSomeKindOfPow: TypeAlias = _SupportsPow2[Any, Any] | _SupportsPow3NoneOnly[Any, Any] | _SupportsPow3[Any, Any, Any]",
        }
        self.visited_nodes = visited_nodes

    def visit_Assign(self, node: ast.Assign):
        if node in self.visited_nodes:
            return
        if not isinstance(node.targets[0], ast.Name) and node.targets[0] not in self.alias_exceptions:
            return
        node_src = astor.to_source(node).strip()
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "TypeVar":
            tv_declarations.append(node_src)
        try:
            exec(node_src, globals())
            self.visited_nodes.append(node)
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


class AnnotationTranslator(ast.NodeVisitor):
    def __init__(self, tree: ast.AST):
        self.tree = tree
        self.selftypes = ["Self", "_typeshed.Self", "type[Self]", "type[_typeshed.Self]", "list[_typeshed.Self]"]
        self.skips = ["Callable"]
        self.class_dict: dict[str, dict[str, list[FunctionSpec]]] = dict()
        self.current_class = None
    
    def visit_ClassDef(self, node):
        if is_protocol_classdef(node):
            return
        self.current_class = node
        self.generic_visit(node)
        self.current_class = None
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        global translated_funcs
        global not_translated_funcs

        def add_to_class_dict(classname: str, funcname: str, funcspec: FunctionSpec):
            if classname in self.class_dict:
                if funcname in self.class_dict[classname]:
                    if funcspec not in self.class_dict[classname][funcname]:
                        self.class_dict[classname][funcname].append(funcspec)
                    # if (funcspec, astor.to_source(node).strip()) not in self.class_dict[classname][funcname]:
                    #     self.class_dict[classname][funcname].append((funcspec, astor.to_source(node).strip()))
                else:
                    self.class_dict[classname][funcname] = [funcspec]
                    # self.class_dict[classname][funcname] = [(funcspec, astor.to_source(node).strip())]
            else:
                self.class_dict[classname] = {funcname: [funcspec]}
                # self.class_dict[classname] = {funcname: [(funcspec, astor.to_source(node).strip())]}

        def has_annotation(_node: ast.arg):
            if not hasattr(_node, "annotation") or _node.annotation is None:
                return False
            return True
        
        def can_be_translated(_node: ast.arg):
            if not has_annotation(_node) and _node.arg != "self":
                return False
            return True

        def get_string_from_annotation(_annot: ast.AST):
            annot_str = astor.to_source(_annot).strip()
            if annot_str in self.selftypes:  # the type is the class name, for self-ish annotations
                annot_str = self.current_class.name
            for skip in self.skips:
                if skip in annot_str:
                    raise TypeError(f"{annot_str}: (skipped)")
            return annot_str

        def str_type_from_node(annot_node: ast.arg) -> str:
            if not has_annotation(annot_node) and annot_node.arg == "self":
                return self.current_class.name
            return get_string_from_annotation(annot_node.annotation)
        
        def annotation_to_basetype(argstr: str) -> BaseType | None:
            try:
                evalled = eval(argstr)
            except Exception as e:
                raise Exception(f"{argstr}: {str(e)}")
            return create_basetype(evalled)
        
        def parse_annotation(_arg: ast.arg) -> tuple[str, BaseType]:
            if not can_be_translated(_arg):
                raise RuntimeError(f"cannot translate {astor.to_source(_arg).strip()}")
            annot_str = str_type_from_node(_arg)
            arg_str = _arg.arg
            bt = annotation_to_basetype(annot_str)
            return arg_str, bt

        if self.current_class is None:
            stats_key = 'indie'
        else:
            stats_key = self.current_class.name
        as_in = AbstractState()
        as_out = AbstractState()

        try:
            arg_lists = [node.args.posonlyargs, node.args.args]
            for arg_list in arg_lists:
                for _arg in arg_list:
                    try:
                        argstr, bt = parse_annotation(_arg)
                        as_in[argstr] = bt
                    except Exception:
                        raise NotTranslatableException("not translatable")

            _arg = node.args.vararg
            try:
                if _arg is not None:
                    argstr, bt = parse_annotation(_arg)
                    as_in['*' + argstr] = bt
            except Exception as e:
                raise NotTranslatableException("not translatable")

            for _arg in node.args.kwonlyargs:
                try:
                    argstr, bt = parse_annotation(_arg)
                    as_in[argstr] = bt
                except Exception:
                    raise NotTranslatableException("not translatable")

            _arg = node.args.kwarg
            try:
                if _arg is not None:
                    argstr, bt = parse_annotation(_arg)
                    as_in['**' + argstr] = bt
            except Exception:
                raise NotTranslatableException("not translatable")
            
            _arg = node.returns
            try:
                if _arg is not None:
                    annot_str = get_string_from_annotation(_arg)
                    bt = annotation_to_basetype(annot_str)
                    as_out["return"] = bt
            except Exception:
                raise NotTranslatableException("not translatable")
        except NotTranslatableException:
            # add_to_class_dict(stats_key, node.name, FunctionSpec(AbstractState(), AbstractState()))
            logging.error(f"An exception occured for:{os.linesep}{astor.to_source(node).strip()}")
            not_translated_funcs += 1
        fs = FunctionSpec(first=as_in, second=as_out)
        add_to_class_dict(stats_key, node.name, fs)
        translated_funcs += 1

    def go_translate(self):
        self.visit(self.tree)
        return self.class_dict


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


def dump_to_pyfile(class_dict, outfile='class_dict.py'):
    with open(outfile, 'w') as f:
        f.write(f'import typing{os.linesep}')
        f.write(f'from typing import *{os.linesep}')
        f.write(f'import types{os.linesep}')
        f.write(f'from types import *{os.linesep}{os.linesep}')
        for tv_decl in tv_declarations:
            f.write(f"{tv_decl}{os.linesep}")
        f.write(os.linesep)
        pprint(class_dict, stream=f)


def parse_stub(stub_path: str, visited_nodes):
    with open(stub_path, 'r') as f:
        tree = ast.parse(f.read())
    for _node in tree.body:
        AssignSeeker(_node, visited_nodes).gather_typealiases()
        ProtocolSeeker(_node, visited_nodes).gather_protocols()
    class_dict = AnnotationTranslator(tree).go_translate()
    return class_dict


def parse_stub_code(code: str):
    tree = ast.parse(code)
    class_dict = AnnotationTranslator(tree).go_translate()
    return class_dict


if __name__ == "__main__":
    fname = "playground/fakeins.pyi"
    # fname = "playground/teststub.pyi"

    cd = parse_stub(fname, [])
    total_funcs = translated_funcs + not_translated_funcs
    print(f"Translated: {translated_funcs/total_funcs * 100:.2f}%")

    code = 'def foo(a: int, b: float) -> float: ...'
    cd2 = parse_stub_code(code)
    print(cd2)
