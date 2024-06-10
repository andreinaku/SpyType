# Diff
```shell
48c48
< adj_list[4].append(Edge(2, -38))
---
> adj_list[4].append(Edge('a', -38))
```

# Results
- Mopsa: TypeError detected, sound
- PEPM17: finds non-bottom state, *unsound*
- Pytype: no errors found, *unsound*
- Typpete: returns unsat, sound
- NFM18: error detected, sound


