# Diff
```shell
419c419
<     x = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
---
>     x = "a"
```

# Results
- Mopsa: ValueError detected, sound
- PEPM17: infers that dt2 is an integer, while an exception should be raised (and thus, dt2 should be bottom). *unsound*
- Pytype: no errors found, *unsound*
- Typpete: returns unsat, sound
- NFM18: TypeError raised, *unsound*

