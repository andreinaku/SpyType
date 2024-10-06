from __future__ import annotations
from types import *
from typing import *
from copy import deepcopy
import ast
import _ast
from astor import to_source
import logging
import sys

from collections.abc import Awaitable, Callable, Iterable, Iterator, MutableSet, Reversible, Set as AbstractSet, Sized
from io import BufferedRandom, BufferedReader, BufferedWriter, FileIO, TextIOWrapper
from types import CodeType, TracebackType


_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)
_R_co = TypeVar("_R_co", covariant=True)
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_S = TypeVar("_S")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")
_T4 = TypeVar("_T4")
_T5 = TypeVar("_T5")
_SupportsNextT = TypeVar("_SupportsNextT", covariant=True)
_SupportsAnextT = TypeVar("_SupportsAnextT", covariant=True)
_AwaitableT = TypeVar("_AwaitableT", bound=Awaitable[Any])
_AwaitableT_co = TypeVar("_AwaitableT_co", bound=Awaitable[Any], covariant=True)
_P = ParamSpec("_P")
_E = TypeVar("_E", contravariant=True)
_M = TypeVar("_M", contravariant=True)
_AddableT1 = TypeVar("_AddableT1")
_AddableT2 = TypeVar("_AddableT2")
_BaseExceptionT_co = TypeVar("_BaseExceptionT_co", bound=BaseException, covariant=True)
_BaseExceptionT = TypeVar("_BaseExceptionT", bound=BaseException)
_ExceptionT_co = TypeVar("_ExceptionT_co", bound=Exception, covariant=True)
_ExceptionT = TypeVar("_ExceptionT", bound=Exception)

_PositiveInteger = int
_SupportsRound2 = int | float
SupportsKeysAndGetItem = dict
SupportsIndex = int
Buffer = bytes | bytearray | memoryview
ReadableBuffer = Sized
_GetItemIterable = str | bytes | bytearray | memoryview | range | tuple | list | dict
SupportsRichComparisonT = int | float | str | bytes | list | set | frozenset | bytearray | tuple


class WarningOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.WARNING
    

class InfoOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


def get_logger(
        LOG_FORMAT='%(levelname)-4s %(message)s',
        LOG_NAME='',
        LOG_FILE_INFO='test.log',
        LOG_FILE_WARN='test.warn',
        LOG_FILE_ERROR='test.err'):
    log = logging.getLogger(LOG_NAME)
    log_formatter = logging.Formatter(LOG_FORMAT)

    file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='w')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    file_handler_info.addFilter(InfoOnlyFilter())
    log.addHandler(file_handler_info)

    file_handler_warn = logging.FileHandler(LOG_FILE_WARN, mode='w')
    file_handler_warn.setFormatter(log_formatter)
    file_handler_warn.setLevel(logging.WARNING)
    file_handler_warn.addFilter(WarningOnlyFilter())
    log.addHandler(file_handler_warn)

    file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode='w')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    log.setLevel(logging.INFO)

    return log


mylogger = get_logger()


class TestVisit(ast.NodeVisitor):
    def __init__(self):
        self.unknowns = set()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for argnode in node.args.args:
            if argnode.annotation is None:
                continue
            annot_src = to_source(argnode.annotation).strip()
            try:
                eval(annot_src)
            except:
                self.unknowns.add(annot_src)


if __name__ == "__main__":
    filepath = "sheds\\builtins.pyi" 
    tree = ast.parse(open(filepath).read())
    tv = TestVisit()
    tv.visit(tree)
    for elem in tv.unknowns:
        mylogger.warning(elem)
    # todo: translate function from genericaliases to basetypes!