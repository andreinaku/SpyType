# SpyType - Simple Python Function Type Specification Generator
SpyType is a research project that aims to create specifications for Python functions. Inference is done using the following:
* a set of stubs snapshotted from the Typeshed project (https://github.com/python/typeshed) - found in the path `sheds/builtins.pyi` of the current project
* the Python Language Bindings for Maude (https://github.com/fadoss/maude-bindings)
* slightly modified versions of `model.py`, `builder.py` and `__init__.py` from the Staticfg project (https://github.com/coetaur0/staticfg/tree/master) - to build the control flow graph and add extra metadata to it

This project is a work in progress and the name SpyType has been chosen as a tribute to a very good and well-established type inference solution, namely Pytype (https://google.github.io/pytype/)

Worthy mentions:
- Mopsa Static Analyzer (shout-out to Raphael Monat for `mopsa-python-types`): https://gitlab.com/mopsa/mopsa-analyzer
- Typpete: https://github.com/caterinaurban/typpete

# Quickstart
SpyType has been tested on Python 3.11 and Python 3.12. The recommended way to use this is to create a virtual environment and install the required libraries using the `requirements.txt` file. To use the tool, use the following command line:
```
python spytype.py [-h] -i INPUT [-f [FUNCTIONS ...]] -o OUTPUT [-v]

A POC for Python function type inference using Maude solver.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file containing Python functions
  -f [FUNCTIONS ...], --functions [FUNCTIONS ...]
                        Optional list of functions to be inferred. If this is omitted, then all functions from the input file are inferred
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

# Simple Usage Examples:

## Example 1
```
python spytype.py -i benchmarks\mine\benchfuncs.py -f while_1 -o while_1.spytype
```
This will write the inferred specifications for the function named `while_1` from the `benchfuncs.py` file into `while_1.spytype`. The output has the following form:
```
---------------------------------
while_1 specs
---------------------------------
while_1 : {
	((x:int) -> (return:list < int >)),
}
```

## Example 2
```
python spytype.py -i benchmarks\mine\benchfuncs.py -o benchfuncs.spytype
```
This will write the inferred specifications for every function in the `benchfuncs.py` file into `benchfuncs.spytype`.
