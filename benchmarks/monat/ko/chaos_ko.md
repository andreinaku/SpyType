# Diff
```shell
121c121
<                 index = ii - I + self.degree - ik - 1
---
>                 index = 'a'
```

# Results
- Mopsa: TypeError detected, sound
- PEPM17: finds non-bottom state, *unsound* 
- Pytype: error found, sound
- Typpete: file unsupported (internal crash)
- NFM18: file unsupported (internal crash)

