# Diff
```shell
44c44
< g = f6({"st": 1})
---
> g = f6({"st": '1'})
```

# Results
- Mopsa: TypeError detected, sound
- PEPM17: g should have bottom type, *unsound*
- Pytype: error detected, sound
- Typpete: error detected, sound
- NFM18: file unsupported

