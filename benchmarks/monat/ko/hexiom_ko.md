# Diff
```shell
504c504
<         ry = size - 1 + y
---
>         ry = size - 1 + 'a'
```

# Results
- Mopsa: TypeError detected line 504, sound
- PEPM17: file unsupported
- Pytype: error detected, sound
- Typpete: file unsupported
- NFM18: file unsupported

