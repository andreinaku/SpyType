# Diff
```shell
42c42
<     partial_sum = 0
---
>     partial_sum = 'a'
```

# Results
- Mopsa: TypeError l44 detected, sound
- PEPM17: partial_sum type to top, and not bottom, *unsound*
- Pytype: no errors found, *unsound*
- Typpete: file unsupported
- NFM18: file unsupported

