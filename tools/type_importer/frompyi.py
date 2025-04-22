import os
import ast
import json
import typing
import types
import typing_extensions
import _typeshed
import collections.abc
from typing import get_type_hints
import inspect
import pickle
import networkx as nx
from pyvis.network import Network

# type -> string
# because some types are evalled with a different name
# for example: int -> 'FileDescriptor'
imported_types = dict()


def find_pyi_files(folder_path):
    """
    Recursively walks through the folder and finds all .pyi files.

    :param folder_path: Path to the root folder to search.
    :return: List of paths to .pyi files.
    """
    pyi_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.pyi'):
                pyi_files.append(os.path.join(root, file))
    return pyi_files

'''
name in ['typing', 'typing_extensions', '_typeshed', 'typeshed']
'''
class ImportVisitor(ast.NodeVisitor):
    def __init__(self, filepath: str):
        self.imports: dict[str, set[str]] = dict()
        self.tree = ast.parse(open(filepath, 'r').read())
        self.from_what = ['typing', 'typing_extensions', '_typeshed', 'typeshed']

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module in self.from_what:
            for alias in node.names:
                if not alias.name[:1].isupper():
                    # type names are usually capitalized
                    continue
                try:
                    to_eval = f'{node.module}.{alias.name}'
                    evalled = eval(to_eval)
                    if evalled == typing.Protocol:
                        continue
                    if evalled == _typeshed.SupportsAllComparisons:
                        # TODO: protocols that are computed simply using multiple inheritance
                        continue
                    if isinstance(evalled, bool):
                        # this is most likely a constant that evals to bool
                        continue
                    if isinstance(evalled, (typing.TypeVar, typing._SpecialForm,
                                            collections.abc._CallableGenericAlias, type(typing.NoDefault),
                                            typing._AnyMeta, typing._LiteralGenericAlias)):
                        # typing._SpecialForm are: Self, Literal, ClassVar etc.
                        # also, we do not need type variables now
                        continue
                    # if evalled in (bool, typing_extensions.CapsuleType):
                    if evalled == typing_extensions.CapsuleType:
                        # TODO: this type requires further research: https://docs.python.org/3/c-api/capsule.html
                        # used rarely
                        continue
                    if inspect.isroutine(evalled):
                        # we need only types, not functions
                        continue
                    imported_types[evalled] = alias.name
                    self.imports[node.module].add(alias.name)
                except KeyError:
                    self.imports[node.module] = {alias.name}
    
    def get_imports(self):
        self.visit(self.tree)
        return self.imports
    

def merge_dicts(dict1: dict[str, list[str]], dict2: dict[str, list[str]]) -> dict[str, list[str]]:
    merged_dict = dict1.copy()  # Start with a copy of the first dictionary

    for key, value_list in dict2.items():
        if key in merged_dict:
            merged_dict[key] += value_list
        else:
            merged_dict[key] = value_list  # Add new key-value pair

    dict_copy = merged_dict.copy()
    for key, value_list in dict_copy.items():
        merged_dict[key] = list(set(value_list))

    return merged_dict


def conforms_to_protocol_or_abc(subtype, protocol):
    # If protocol is a typing alias, get its origin
    # TODO: implement search within parent classes (except Protocol); e.g. SupportsAllComparisons
    origin = typing.get_origin(protocol)
    if origin is not None:
        protocol = origin
    
    # 1. Abstract methods from ABCs
    abstract_methods = getattr(protocol, '__abstractmethods__', set())

    # 2. Explicit methods/attrs declared in the Protocol
    explicit_methods = dict()
    for name, obj in vars(protocol).items():
        if (callable(obj) and name != '__init__') or isinstance(obj, (property,)):
            explicit_methods[name] = obj

    # 3. Annotations on Protocol attributes (not initialized vars)
    type_hints = get_type_hints(protocol)
    explicit_attrs = set(type_hints.keys())

    # Merge all required attributes/methods
    required_attrs = set(explicit_methods.keys()) | explicit_attrs | set(abstract_methods)

    if len(required_attrs) == 0:
        raise RuntimeError(f'the list of required attributes for {protocol} cannot be zero')

    # 4. Check whether subtype has all required attributes
    for _attr in required_attrs:
        if _attr not in subtype.__dict__:
            return False
        if subtype.__dict__[_attr] is None:
            return False
    return True
    # return all(hasattr(subtype, attr) for attr in required_attrs)


def lesser(t1, t2):
    if isinstance(t1, type) and typing.is_protocol(t2):
        return conforms_to_protocol_or_abc(t1, t2)
    elif isinstance(t1, type) and inspect.isabstract(t2):
        return conforms_to_protocol_or_abc(t1, t2)
    elif typing.is_protocol(t1) and typing.is_protocol(t2):
        return conforms_to_protocol_or_abc(t1, t2)
    elif inspect.isabstract(t1) and inspect.isabstract(t2):
        return conforms_to_protocol_or_abc(t1, t2)
    elif isinstance(t1, type) and isinstance(t2, (typing._UnionGenericAlias, types.UnionType)):
        for _arg in typing.get_args(t2):
            if lesser(t1, _arg):
                return True
        return False
    elif isinstance(t1, (typing._UnionGenericAlias, types.UnionType)) and \
            isinstance(t2, (typing._UnionGenericAlias, types.UnionType)):
        for _arg1 in typing.get_args(t1):
            for _arg2 in typing.get_args(t2):
                if not lesser(_arg1, _arg2):
                    return False
        return True
    elif isinstance(t1, typing._BaseGenericAlias) and isinstance(t2, typing._BaseGenericAlias):
        orig1 = typing.get_origin(t1)
        orig2 = typing.get_origin(t2)
        if not lesser(orig1, orig2):
            return False
        args1 = typing.get_args(t1)
        args2 = typing.get_args(t2)
        if len(args1) != len(args2):
            return False
        for i in range(0, len(args1)):
            if not lesser(args1[i], args2[i]):
                return False
        return True
    elif isinstance(t1, type) and isinstance(t2, typing._BaseGenericAlias):
        origin = typing.get_origin(t2)
        return lesser(t1, origin)
    elif isinstance(t1, type) and isinstance(t2, type):
        return issubclass(t1, t2)
    else:
        return False


def inject_graph(gpath: str):
    html_lines = open(gpath, 'r').readlines()
    to_inject = '''
  // Store the original data for reset purposes
  var allNodes = nodes.get();
  var allEdges = edges.get();

  network.on("selectNode", function (params) {
    var selectedNodeId = params.nodes[0];

    // Get all connected nodes from the edges
    var connectedNodeIds = new Set([selectedNodeId]);
    var connectedEdges = [];

    allEdges.forEach(function (edge) {
      if (edge.from === selectedNodeId || edge.to === selectedNodeId) {
        connectedNodeIds.add(edge.from);
        connectedNodeIds.add(edge.to);
        connectedEdges.push(edge);
      }
    });

    // Filter nodes to only the connected ones
    var filteredNodes = allNodes.filter(function (node) {
      return connectedNodeIds.has(node.id);
    });

    // Update the data shown on the graph
    nodes.clear();
    edges.clear();
    nodes.add(filteredNodes);
    edges.add(connectedEdges);
  });

  network.on("deselectNode", function () {
    // Reset to full graph when clicking on empty space
    nodes.clear();
    edges.clear();
    nodes.add(allNodes);
    edges.add(allEdges);
  });
'''
    with open(gpath, 'w') as f:
        for line in html_lines:
            f.write(f"{line}{os.linesep}")
            if "network = new vis.Network(container, data, options);" in line:
                f.write(to_inject)
                f.write(os.linesep)


def show_graph(pairs: list[tuple]):
    G = nx.DiGraph()
    G.add_edges_from(pairs)
    net = Network(notebook=False, directed=True)
    net.from_nx(G)
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "solver": "repulsion",
        "repulsion": {
          "nodeDistance": 200,
          "centralGravity": 0.2,
          "springLength": 200,
          "springConstant": 0.05,
          "damping": 0.09
        }
      }
    }
    """)
    # net.show_buttons(filter_=['physics'])  # optional: adds GUI controls
    net.show('graph.html', notebook=False)  # opens in a browser
    inject_graph('graph.html')


def generate_ops(builtins, imported, indent=0):
    tabs = "\t" * indent
    retstr = f"{tabs}ops "
    for t in builtins:
        retstr += f"{t.__name__} "
    for t, tstring in imported.items():
        retstr += f"{tstring} "
    retstr += f" : -> Type [ctor] .\n"
    retstr += (
        f"{tabs}op _<_> : Type Type -> Type [ctor prec 20] .\n"
        f"{tabs}op _x_ : Type Type -> Type [assoc ctor prec 25] .\n"
        f"{tabs}op leq : Type Type -> Bool .\n"
        f"{tabs}op _+_ : Type Type -> Type [assoc comm idem prec 30] .\n"
    )
    return retstr


def generate_eqs(ppairs, indent=0):
    tabs = "\t" * indent
    retstr = ""
    for p in ppairs:
        retstr += f"{tabs}eq leq({p[0]}, {p[1]}) = true .\n"
    retstr += (
        f"{tabs}var T T1 T2 T3 T4 : Type .\n"
        f"{tabs}eq T + T = T .\n"
        f"{tabs}eq leq(T, T) = true .\n"
        f"{tabs}eq leq(T1, T1 + T2) = true .\n"
        f"{tabs}ceq leq(T1, T2 + T3) = true if leq(T1, T2) or leq(T1, T3) .\n"
        f"{tabs}ceq leq(T1 x T2, T3 x T4) = true if leq(T1, T3) and leq(T2, T4) .\n"
        f"{tabs}ceq leq(T1 < T2 >, T3 < T4 >) = true if leq(T1, T3) and leq(T2, T4) .\n"
        f"{tabs}ceq leq(T1 < T2 >, T3) = true if leq(T1, T3) .\n"
        f"{tabs}eq leq(T1, T2) = false [owise] .\n")
    return retstr


def generate_fmod(builtins, imported, ppairs):
    spacing = "\t"
    retstr = f"fmod relly is{os.linesep}{spacing}sort Type .{os.linesep}"
    aux = generate_ops(builtins, imported, 1)
    retstr += f"{aux}{os.linesep}"
    aux = generate_eqs(ppairs, 1)
    retstr += f"{aux}{os.linesep}"
    retstr += "endfm"
    return retstr


# TODO: generate sorts from all_types
# TODO: can we separate Container types from the others? can Container types be used without args in annotations? is this necessary? 
if __name__ == "__main__":
    folder_to_search = "/Users/andrei/work/doctorat/typeshed"
    pyi_files = find_pyi_files(folder_to_search)
    imports = dict()
    for file in pyi_files:
        imports = merge_dicts(imports, ImportVisitor(file).get_imports())
    for k in imports:
        imports[k].sort()
        print(f'{k}: {len(imports[k])}')
    json_string = json.dumps(imports, indent=4)
    with open('imports.json', 'w') as f:
        f.write(json_string)
    all_builtins = [bool, int, float, complex, range, str, bytes, bytearray, memoryview, type(None), set, frozenset, list, tuple, dict]
    all_types = set(all_builtins) | set(imported_types.keys())
    pairs: set[tuple] = set()
    
    # use for all the types    
    type_pairs: set[tuple[type, type]] = set()
    for t1 in all_types:
        for t2 in all_types:
            if t1 == t2:
                continue
            if lesser(t1, t2):
                _t1 = imported_types[t1] if t1 in imported_types else t1.__name__ 
                _t2 = imported_types[t2] if t2 in imported_types else t2.__name__
                pairs.add((_t1, _t2))
                if t1 in all_builtins:
                    pairs.add((t1.__name__, _t2))
                type_pairs.add((t1, t2))
    auxxx = generate_fmod(all_builtins, imported_types, pairs)
    with open("test.maude", "w") as f:
        f.write(auxxx)
    print(f"We have {len(pairs)} relations over {len(all_types)} types/protocols/ABCs")
    with open('type_pairs.pkl', 'wb') as f:
        pickle.dump(type_pairs, f) 
    # show_graph(pairs)
