from code2flow import engine
from anytree import Node, RenderTree, LevelOrderGroupIter, PostOrderIter
from io import StringIO
import logging
import json


def foo(raw_source_paths, language=None,
              exclude_namespaces=None, exclude_functions=None,
              include_only_namespaces=None, include_only_functions=None,
              no_grouping=False, no_trimming=False, skip_parse_errors=False,
              lang_params=None, level=logging.INFO):
    
    if not isinstance(raw_source_paths, list):
        raw_source_paths = [raw_source_paths]
    lang_params = lang_params or engine.LanguageParams()

    exclude_namespaces = exclude_namespaces or []
    assert isinstance(exclude_namespaces, list)
    exclude_functions = exclude_functions or []
    assert isinstance(exclude_functions, list)
    include_only_namespaces = include_only_namespaces or []
    assert isinstance(include_only_namespaces, list)
    include_only_functions = include_only_functions or []
    assert isinstance(include_only_functions, list)

    logging.basicConfig(format="Code2Flow: %(message)s", level=level)

    sources, language = engine.get_sources_and_language([path], language)
    file_groups, all_nodes, edges = engine.map_it(sources, language, no_trimming,
                                        exclude_namespaces, exclude_functions,
                                        include_only_namespaces, include_only_functions,
                                        skip_parse_errors, lang_params)
    file_groups.sort()
    all_nodes.sort()
    edges.sort()
    
    content = engine.generate_json(all_nodes, edges)
    return content


path = 'callgraph/test5.py'
bar = foo(path, language="py", no_trimming=True)
open('out.json', 'w').write(bar)
js = json.loads(bar)
# print(js)

root_node = Node('root')

node_dict = dict()

for nodeid, nodeinfo in js['graph']['nodes'].items():
    node_dict[nodeid] = dict()
    newnode = Node(nodeinfo['name'])
    node_dict[nodeid]['node'] = newnode
    node_dict[nodeid]['kids'] = set()
    node_dict[nodeid]['parent'] = None
    for edge in js['graph']['edges']:
        if edge['source'] == nodeid:
            node_dict[nodeid]['kids'].add(edge['target'])
        if edge['target'] == nodeid:
            node_dict[nodeid]['parent'] = edge['source']

for nodeid, nodeinfo in node_dict.items():
    kid_nodes = set()
    for kid_id in nodeinfo['kids']:
        kid_nodes.add(node_dict[kid_id]['node'])
    parent_node = root_node
    if nodeinfo['parent'] is not None:
        parent_node = node_dict[nodeinfo['parent']]['node']
    nodeinfo['node'].children = kid_nodes
    nodeinfo['node'].parent = parent_node


for pre, fill, node in RenderTree(root_node):
    print(f'{pre}{node.name}')

for grup in reversed(list(LevelOrderGroupIter(root_node))):
    print([node.name for node in grup])
