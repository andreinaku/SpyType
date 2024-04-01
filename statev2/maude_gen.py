import os


def vartype_generator(maxitems = 20):
    normals = []
    specs = []
    for i in range(0, maxitems):
        normals.append(f'T{i}')
        specs.append(f'T?{i}')
    return normals, specs


def mod_generator(mod_name: str, constraints: str, indent=2) -> str:
    filename = f'{mod_name}.maude'
    spaces = ' ' * indent
    with open(filename, 'w') as f:
        f.write(f'mod {mod_name} is {os.linesep}')
        f.write(f'{spaces}protecting CONSTR .{os.linesep}')
        f.write(f'{spaces}ops ')
        normals, specs = vartype_generator()
        for n in normals:
            f.write(f'{n} ')
        f.write(f': -> VarType .{os.linesep}')
        f.write(f'{spaces}ops ')
        for s in specs:
            f.write(f'{s} ')
        f.write(f': -> BoundVarType .{os.linesep}')
        f.write(f'{spaces}op c : -> Disj .{os.linesep}')
        f.write(f'{os.linesep}{spaces}eq c = {os.linesep}{constraints} .{os.linesep}')
        f.write(os.linesep)
        f.write('endm')
    return filename
