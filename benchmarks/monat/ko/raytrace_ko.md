# Diff
```shell
207c207
<         self.bytes[i + 1] = max(0, min(255, int(g * 255)))
---
>         self.bytes[i + 1] = max(0, min('a', int(g * 255)))
```

# Results
- Mopsa: TypeError l207 detected, sound
- PEPM17: non-bottom state, *unsound*
- Pytype: error detected (weird one though)
- Typpete: file unsupported
- NFM18: file unsupported

