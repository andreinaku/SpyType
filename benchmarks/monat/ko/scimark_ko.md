# Diff
```shell
150,151c150,151
<                 G[x, y] = (omega * 0.25 * (G[x, y - 1] + G[x, y + 1] + G[x - 1, y]
<                                            + G[x + 1, y])
---
>                 G[x, y] = (omega * 'a' * (G[x, y - 1] + G[x, y + 1] + G[x - 1, y]
>                               + G[x + 1, y])
```

# Results
- Mopsa: TypeError detected, sound
- PEPM17: no errors found, *unsound*
- Pytype: error detected, sound 
- Typpete: file unsupported
- NFM18: file unsupported

