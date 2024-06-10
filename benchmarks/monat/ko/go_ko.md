# Diff
```shell
55c55
<         self.ledges = 0
---
>         self.ledges = 'a'
```

# Results
- Mopsa: TypeError detected line 60, sound
- PEPM17: no error detected, *unsound*
- Pytype: error detected, sound
- Typpete: internal error
- NFM18: internal error

