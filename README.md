# SpyType - Simple Python Function Type Specification Generator
This is a research project that aims to create specifications for Python functions. Inference is done using the following:
* a set of stubs snapshotted from the Typeshed project (https://github.com/python/typeshed) - found in the path `sheds/builtins.pyi` of the current project
* the Maude language for rewriting logic (https://maude.cs.illinois.edu/wiki/The_Maude_System) and the Python Language Bindings for Maude (https://github.com/fadoss/maude-bindings)
* `model.py`, `builder.py` and `__init__.py` from the Staticfg project (https://github.com/coetaur0/staticfg/tree/master) - to build the control flow graph and add extra metadata to it

This project is a work in progress and the name SpyType has been chosen as a tribute to a very good and well-established type inference solution, namely Pytype (https://google.github.io/pytype/)

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

# Note
The set of specifications used as a basis for inference is the `united_specs.py` file found in the root of the project. To re-generate this file based on the information in the stubs found `sheds` folder, simply run:
```
python pyiparser_2.py
```
This creates the `united_specs.py` file by translating the stubs into SpyType's internal specification format. Also, some specifications are added that are used for parsing AST nodes from functions.

# Simple example:
```
python simple_inference.py -f benchmarks\mine\benchfuncs_typpete.py -o results.out
```
This will write the inferred specifications for every function in the `benchfuncs_typpete.py` file.
