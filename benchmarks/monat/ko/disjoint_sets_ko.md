# Diff
```shell
37c37
< d = DisjointSets(3)
---
> d = DisjointSets('a')
```

# Results
- Mopsa: TypeError detected, sound
- PEPM17: no error detected, *unsound*
- Pytype: error detected, sound
- Typpete: error detected, sound
- NFM18: fie unsupported

