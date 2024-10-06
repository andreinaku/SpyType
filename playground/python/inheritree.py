from __future__ import annotations
import ast
from copy import deepcopy
from astor import to_source
import matplotlib.pyplot as plt
import networkx as nx


class InheriNode:
    def __init__(self, name: str, parents: list[InheriNode]=None, kids: list[InheriNode]=None):
        self.name = name
        self.parents = parents
        self.kids = kids
        if self.parents is None:
            self.parents = []
        if self.kids is None:
            self.kids = []

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other_node: InheriNode):
        return self.name == other_node.name
    
    def append_parent(self, new_parent: InheriNode):
        self.parents.append(new_parent)

    def append_kid(self, new_kid: InheriNode):
        self.kids.append(new_kid)

    def reset_kids(self):
        self.kids = []

    def reset_parents(self):
        self.parents = []
    

class InheriGraph:
    def __init__(self, inherinodes: list[InheriNode]=None):
        if inherinodes is None:
            self.inherinodes = []
        else:
            self.inherinodes = deepcopy(inherinodes)
    
    def __contains__(self, to_check: InheriNode):
        for inherinode in self.inherinodes:
            if inherinode == to_check:
                return True
        return False

    def __iter__(self):
        return iter(self.inherinodes)
    
    def __str__(self):
        return str(self.inherinodes)
    
    def __repr__(self):
        return str(self)

    def __add__(self, other_graph: InheriGraph) -> InheriGraph:
        new_graph = InheriGraph()
        new_graph.inherinodes = self.inherinodes + other_graph.inherinodes
        return new_graph

    def add_node(self, new_node: InheriNode):
        if new_node not in self:
            self.inherinodes.append(new_node)

    def get_node_subgraph(self, inherinode: InheriNode) -> InheriGraph:

        def _recurse_nodes(nod: InheriNode):
            new_graph = InheriGraph()
            new_graph.add_node(nod)
            for possible_parent in self:
                if possible_parent in nod.parents:
                    new_graph += _recurse_nodes(possible_parent)
            return new_graph

        new_graph = InheriGraph()
        new_node = deepcopy(inherinode)
        new_node.reset_kids()
        return _recurse_nodes(new_node)
    
    def get_node_by_name(self, name: str) -> InheriNode:
        for inherinode in self:
            if inherinode.name == name:
                return inherinode
        return None

    def get_node_subgraph_by_name(self, name: str) -> InheriGraph:
        node = self.get_node_by_name(name)
        return self.get_node_subgraph(node)

    def plot(self):
        G = nx.DiGraph()
        for node in self.inherinodes:
            G.add_node(node.name)
            for child in node.kids:
                G.add_edge(node.name, child.name)
        
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=10, font_weight="bold", arrows=True)
        plt.show()



class GetInheriGraph(ast.NodeVisitor):
    def __init__(self, filepath: str):
        self.tree = ast.parse(open(filepath).read())
        self.inherigraph = InheriGraph()

    def get_node_name(self, node: ast.AST):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return to_source(node.value).strip()
        elif isinstance(node, ast.Subscript):
            return self.get_node_name(node.value)
        raise RuntimeError(f"{to_source} name is not supported")

    def visit_ClassDef(self, node: ast.ClassDef):
        # todo: class x(y, z): ...
        # todo: class x(y[_T], z[_T]): ... 
        new_node = InheriNode(node.name)
        self.inherigraph.add_node(new_node)
        if len(node.bases) > 0:
            for basenode in node.bases:
                basename = self.get_node_name(basenode)
                for inherinode in self.inherigraph:
                    if basename == inherinode.name:
                        inherinode.append_kid(new_node)
                        new_node.append_parent(inherinode)

    def get_graph(self) -> list[InheriNode]:
        self.visit(self.tree)
        return self.inherigraph


if __name__ == "__main__":
    filepath = "playground\\python\\testclass.py"
    inherigraph = GetInheriGraph(filepath).get_graph()
    subgraph = inherigraph.get_node_subgraph_by_name("int")
    subgraph.plot()
