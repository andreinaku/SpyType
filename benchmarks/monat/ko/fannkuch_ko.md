# Diff
```shell
28c28
<             check += 1
---
>             check += 'a'
```

# Analysis
- Mopsa: TypeError detected, sound
- PEPM17: finds that check is bottom at program point 54. sound?
- Pytype: error detected, sound
- Typpete: file unsupported
- NFM18: file unsupported

