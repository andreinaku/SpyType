import os


def vartype_generator(maxitems = 20):
    normals = []
    specs = []
    for i in range(0, maxitems):
        normals.append(f'T{i}')
        specs.append(f'T?{i}')
    return normals, specs


def mod_generator(mod_name: str, constraints: str, indent=2, dump_to_file=False) -> str:
    spaces = ' ' * indent
    maude_code = (f'mod {mod_name} is {os.linesep}'
                    f'{spaces}protecting CONSTR .{os.linesep}'
                    f'{spaces}ops ')
    normals, specs = vartype_generator()
    for n in normals:
        maude_code += f'{n} '
    maude_code += (f': -> VarType .{os.linesep}'
                     f'{spaces}ops ')
    for s in specs:
        maude_code += f'{s} '
    maude_code += (f': -> BoundVarType .{os.linesep}'
                     f'{spaces}op c : -> Disj .{os.linesep}'
                     f'{os.linesep}{spaces}eq c = {os.linesep}{constraints} .{os.linesep}'
                     f'{os.linesep}'
                     f'endm')
    if dump_to_file:
        open(mod_name + '.maude', 'w').write(maude_code)
    return maude_code
