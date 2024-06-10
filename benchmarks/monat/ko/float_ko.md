# Diff
```shell
17c17
<         self.x = x = sin(i)
---
>         self.x = x = sin('a')
```

# Results
- Mopsa: TypeError detected, sound
- PEPM17: no error detected, *unsound*
- Pytype: no error detected, *unsound*
- Typpete: error detected, sound
- NFM18: error detected, sound

