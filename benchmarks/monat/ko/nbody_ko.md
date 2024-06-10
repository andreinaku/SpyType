# Diff
```shell
19a20
> 
133c134
<         advance(0.01, iterations)
---
>         advance('a', iterations)
153a155
> 
```

# Results
- Mopsa: TypeError detected, sound
- PEPM17: non-bottom state return, unsound
- Pytype: error detected, sound
- Typpete: file unsupported
- NFM18: file unsupported

