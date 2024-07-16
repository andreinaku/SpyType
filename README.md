# SpyType - a simple python function type specification generator
This is a research project that aims to create specifications for Python functions based on a set of stubs collected from the Typeshed project (https://github.com/python/typeshed).

# Quickstart
```
simple_inference.py [-h] -f FILE -o OUTPUT [-v]

A POC for Python function type inference using Maude solver.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input file containing Python functions
  -o OUTPUT, --output OUTPUT
                        Path to the output file for writing results
  -v, --verbose         Show information in every CFG node (inferfunc_* images)
```

Simple example:
```
python simple_inference.py -f benchmarks\mine\benchfuncs_typpete.py -o results.out
```
This will write the inferred specifications for every function in the `benchfuncs_typpete.py` file.
