from __future__ import annotations
import sys
import os
sys.path.append(os.getcwd())
from utils.utils import *
from enum import Enum
from copy import deepcopy
from statev2.supported_types import is_supported_type, builtin_types, builtin_seqs, builtin_dicts, builtins
import maude
import re
import itertools


strat1 = 'one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; Step5 ! ; Step6 ! '
strat2 = 'one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; one(Step4) ! ; Step5 ! ; Step6 ! '
INIT_MAUDE_PATH = os.getcwd() + os.sep + 'init.maude'
DEFAULT_SOLVER_OUT = os.getcwd() + os.sep + 'solver.out'


def get_solutions_from_pairs(solution_len: int, pairs: set[tuple[Any]], domain_1: set[Any], 
                             domain_2: set[Any], index: int = 0):
    def temp_id(index: int) -> str:
            temp_vt = f'T`{index}'
            return temp_vt

    # solution_len = len(all_vt1)  # every vartype in one bt needs a match in the other
    combis = list(itertools.combinations(pairs, solution_len))
    solutions = set()
    for comb in combis:
        aux_vt1 = deepcopy(domain_1)
        aux_vt2 = deepcopy(domain_2)
        for pair in comb:
            if pair[0] in aux_vt1:
                aux_vt1.remove(pair[0])
            if pair[1] in aux_vt2:
                aux_vt2.remove(pair[1])
            if len(aux_vt1) == 0 and len(aux_vt2) == 0:
                solutions.add(deepcopy(comb))
    sol_dicts = []
    for sol in solutions:
        sol_dict1 = dict()
        sol_dict2 = dict()
        new_vt = VarType(temp_id(index))
        index += 1
        for pair in sol:
            sol_dict1[pair[0]] = deepcopy(new_vt)
            sol_dict2[pair[1]] = deepcopy(new_vt)
        sol_dicts.append((deepcopy(sol_dict1), deepcopy(sol_dict2)))
    return sol_dicts


def maude_vartype_generator(maxitems: int = 20) -> tuple[list[str], list[str]]:
        normals = []
        specs = []
        for i in range(0, maxitems):
            normals.append(f'T{i}')
            specs.append(f'T?{i}')
        return normals, specs


def mod_generator(mod_name: str, constraints: str, dump_file: str | None  = None, indent: int = 2) -> str:
    spaces = ' ' * indent
    maude_code = (f'mod {mod_name} is {os.linesep}'
                    f'{spaces}protecting CONSTR .{os.linesep}'
                    f'{spaces}ops ')
    normals, specs = maude_vartype_generator()
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
    if dump_file is not None:
        open(dump_file, 'w').write(maude_code)
    return maude_code


class RelOp(Enum):
    LEQ = '<='
    EQ = '=='


class GenericType:
    @classmethod
    def get_types_from_list(cls, instr: str, start_br, end_br, sep):
        # if contained between parantheses, remove them. (int) => int, (int+float) => int+float
        instr = elim_paren(instr)
        typelist = []
        newstr = ""
        in_contained = 0
        state = 0
        i = 0
        length = len(instr)
        if length == 0:
            return typelist
        while True:
            c = instr[i]
            if state == 0:
                if i == (length - 1):
                    break
                if c == sep or c == " ":
                    i += 1
                    continue
                state = 1
                continue
            if state == 1:
                if c == start_br:
                    in_contained += 1
                if c == end_br:
                    in_contained -= 1
                if c == sep and not in_contained:
                    state = 2
                    continue
                newstr += c
                if i == (length - 1):
                    state = 2
                    continue
                i += 1
                continue
            if state == 2:
                if len(newstr):
                    typelist.append(newstr)
                newstr = ""
                state = 0
                continue
        return typelist

    @classmethod
    def translate_type(cls, strtype: str, start_br="<", end_br=">", sep="+") -> PyType | VarType:
        def get_kvlist(strtypes):
            level = 0
            toadd = ''
            kvlist = []
            for c in strtypes:
                if c == '<':
                    level += 1
                    toadd += c
                elif c == '>':
                    level -= 1
                    toadd += c
                elif c == ',':
                    if level == 0:
                        kvlist.append(toadd)
                        toadd = ''
                    else:
                        toadd += c
                elif c == ' ':
                    continue
                else:
                    toadd += c
            if toadd != '':
                kvlist.append(toadd)
            return kvlist

        # for bottom type
        if strtype == 'bot':
            return PyType(BottomType)
        if strtype == 'err':
            return PyType(ErrorType)
        if strtype == 'top':
            return PyType(TopType)
        # for vartypes
        if strtype.startswith('T') and strtype != 'TopType':
            vartype_patt = r'^T[\?a-zA-Z0-9_`\.]+$'
            if re.match(vartype_patt, strtype):
                return VarType(strtype)
            raise RuntimeError('Vartype {} does not have a valid format'.format(strtype))
        # for simple types: int, str, float that eval to a type
        id_patt = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
        if re.match(id_patt, strtype):
            if strtype == 'NoneType':
                btip = type(None)
            else:
                btip = eval(strtype)
            # if not isinstance(btip, type):
            if not is_supported_type(btip, strict=False):
                raise RuntimeError('Type {} does not denote  a Python type'.format(strtype))
            return PyType(btip)
        # for containers: list[int, float, set[T_2, complex], bool] etc.
        container_patt = r'^([a-zA-Z_][a-zA-Z0-9_]*)\<([a-zA-Z0-9\+ ,_\<\?`\.\>]*)\>$'
        # container_patt = r'^([a-zA-Z_][a-zA-Z0-9_]*)\[([a-zA-Z0-9\{} _\{}\{}]+)\]$'.format(start_br, end_br, sep)
        foundlist = re.findall(container_patt, strtype)
        if len(foundlist) != 1:
            raise RuntimeError('Type {} does not represent a valid container type'.format(strtype))
        foundtuple = foundlist[0]

        btip = eval(foundtuple[0])
        # if type(btip) is not type:
        # if not isinstance(btip, type):
        if not is_supported_type(btip, strict=False):
            raise RuntimeError('Type {} does not eval to a type type'.format(type))

        kvlist = get_kvlist(foundtuple[1])
        if len(kvlist) > 2:
            raise TypeError(f'Contained types {kvlist} is not supported.')
        ll = []
        for strtip in kvlist:
            c_strtypes = cls.get_types_from_list(strtip, start_br, end_br, sep)
            # c_types = hset()
            c_types = Basetype()
            for c_strtype in c_strtypes:
                newtip = cls.translate_type(c_strtype, start_br, end_br, sep)
                c_types.add(newtip)
            ll.append(c_types)
        return PyType(btip, *ll)
    
    @classmethod
    def from_str(cls, input_str: str) -> GenericType:
        return cls.translate_type(input_str)


class PyType(GenericType):
    def __init__(self, ptype, keys=None, values=None):
        self.ptype = deepcopy(ptype)
        self.keys = deepcopy(keys)
        self.values = deepcopy(values)

    def __str__(self):
        if self.ptype == BottomType:
            retstr = 'bot'
        elif self.ptype == TopType:
            retstr = 'top'
        elif self.ptype == ErrorType:
            retstr = 'err'
        elif isinstance(self.ptype, VarType):
            retstr = self.ptype.varexp
        else:
            retstr = self.ptype.__name__
        if self.keys is not None and len(self.keys) > 0 and self.values is None:
            retstr += '< '
            retstr += str(self.keys)
            retstr += ' >'
        elif self.keys is not None and len(self.keys) > 0 and self.values is not None and len(self.values) > 0:
            retstr += '< '
            retstr += str(self.keys)
            retstr += ', '
            retstr += str(self.values)
            retstr += ' >'
        return retstr

    def __key(self):
        return self.ptype, self.keys, self.values

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return self.__str__()
    
    def get_builtin_from_pytype(self) -> Basetype:
        new_bt = Basetype()
        if isinstance(self, VarType):
            new_bt.add(deepcopy(self))
            return new_bt
        for blist in builtins:
            if self.ptype in blist:
                # if it is already a builtin type, just add it
                # only Protocols are replaced
                new_bt.add(deepcopy(self))
                return new_bt
        if self.keys is None or self.keys == Basetype({PyType(TopType)}):
            for btype in builtin_types:
                try:
                    if issubclass(btype, self.ptype):
                        new_bt.add(PyType(btype))
                except TypeError:
                    continue
        if (self.keys is not None and self.values is None) or (self.keys is None and self.values is None):
            for btype in builtin_seqs:
                contained_keys = Basetype({PyType(TopType)})
                if self.keys is not None and len(self.keys) != 0:
                    if len(self.keys) == 1:
                        # contained_keys = deepcopy(ptip.keys)
                        # contained_keys = self.get_builtin_from_bt(ptip.keys)
                        contained_keys = self.keys.get_builtin_from_bt()
                    else:
                        raise TypeError(f'We do not support {self} substitution yet')
                try:
                    if issubclass(btype, self.ptype):
                        new_bt.add(PyType(btype, contained_keys))
                except TypeError as te:
                    continue
        if (self.keys is not None and self.values is not None) or (self.keys is None and self.values is None):
            for btype in builtin_dicts:
                contained_keys = Basetype({PyType(TopType)})
                contained_values = Basetype({PyType(TopType)})
                if (self.keys is not None and len(self.keys) != 0) and (self.values is not None and len(self.values) != 0):
                    if len(self.keys) == 1 and len(self.values) == 1:
                        contained_keys = deepcopy(self.keys)
                        contained_values = deepcopy(self.values)
                    else:
                        raise TypeError(f'We do not support {self} substitution yet')
                try:
                    if issubclass(btype, self.ptype):
                        new_bt.add(PyType(btype, contained_keys, contained_values))
                except TypeError:
                    continue
        if len(new_bt) == 0:
            new_bt.add(deepcopy(self))
        return new_bt


class VarType(GenericType):
    def __init__(self, varexp: str):
        self.varexp = varexp

    def __str__(self):
        return self.varexp

    def __repr__(self):
        return self.__str__()

    def __key(self):
        return self.varexp

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return hash(self) == hash(other)


class Basetype(hset):
    def __str__(self):
        retstr = ''
        for elem in self.__iter__():
            retstr += str(elem) + ' + '
        retstr = retstr[:-3]
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return super().__hash__()
    
    @classmethod
    def lub(cls, bt1: Basetype, bt2: Basetype) -> Basetype:
        new_basetype = Basetype()
        already_added = set()
        for atom1 in bt1:
            if isinstance(atom1, VarType) or (isinstance(atom1, PyType) and atom1.keys is None):
                new_basetype.add(deepcopy(atom1))
                continue
            same_container = False
            for atom2 in bt2:
                if isinstance(atom2, PyType) and atom1.ptype == atom2.ptype:
                    same_container = True
                    break
            if same_container:
                new_atom = PyType(atom1.ptype, cls.lub(atom1.keys, atom2.keys))
                new_basetype.add(deepcopy(new_atom))
                already_added.add(atom2)
            else:
                new_basetype.add(deepcopy(atom1))
        for atom2 in bt2:
            if atom2 not in already_added:
                new_basetype.add(deepcopy(atom2))
        return new_basetype

    @classmethod
    def from_str(cls, input_str: str) -> Basetype:
        str_basetype = elim_paren(input_str)
        str_bt_split = GenericType.get_types_from_list(str_basetype, "<", ">", "+")
        bt_typelist = []
        new_bt = Basetype()
        for _cte_type in str_bt_split:
            cte_type = _cte_type.strip()
            bt_typelist.append(GenericType.translate_type(cte_type, "<", ">", "+"))
        new_bt = Basetype(bt_typelist)
        return new_bt

    def replace_vartype(self, to_replace: str, replace_with: str) -> Basetype:
        new_bt = Basetype()
        for tip in self:
            if isinstance(tip, VarType):
                if tip.varexp == to_replace:
                    new_tip = VarType(replace_with)
                    new_bt.add(new_tip)
                else:
                    new_bt.add(deepcopy(tip))
            elif isinstance(tip, PyType):
                # if tip.ptype not in container_ptypes and tip.ptype not in mapping_types:
                if tip.keys is None and tip.values is None:
                    new_bt.add(deepcopy(tip))
                # elif tip.ptype in mapping_types:
                elif tip.keys is not None and tip.values is not None:
                    new_keys = tip.keys.replace_vartype(to_replace, replace_with)
                    new_values = tip.values.replace_vartype(to_replace, replace_with)
                    newtip = PyType(tip.ptype, keys=new_keys, values=new_values)
                    new_bt.add(newtip)
                # elif tip.ptype in container_ptypes:
                elif tip.keys is not None:
                    new_keys = tip.keys.replace_vartype(to_replace, replace_with)
                    newtip = PyType(tip.ptype, keys=new_keys)
                    new_bt.add(newtip)
                else:
                    raise RuntimeError(f'What base type is this? f{tip.ptype}')
            else:
                raise RuntimeError(f'What type is this inside my basetype? {tip}')
        return new_bt

    def replace_vartype_with_basetype(self, to_replace: str, replace_with: Basetype) -> Basetype:
        new_bt = Basetype()
        for tip in self:
            if isinstance(tip, VarType):
                if tip.varexp == to_replace:
                    new_bt |= deepcopy(replace_with)
                else:
                    new_bt.add(deepcopy(tip))
            elif isinstance(tip, PyType):
                # if tip.ptype not in container_ptypes and tip.ptype not in mapping_types:
                if tip.keys is None and tip.values is None:
                    new_bt.add(deepcopy(tip))
                # elif tip.ptype in mapping_types:
                elif tip.keys is not None and tip.values is not None:
                    new_keys = tip.keys.replace_vartype_with_basetype(to_replace, replace_with)
                    new_values = tip.values.replace_vartype_with_basetype(to_replace, replace_with)
                    newtip = PyType(tip.ptype, keys=new_keys, values=new_values)
                    new_bt.add(newtip)
                # elif tip.ptype in container_ptypes:
                elif tip.keys is not None:
                    new_keys = tip.keys.replace_vartype_with_basetype(to_replace, replace_with)
                    newtip = PyType(tip.ptype, keys=new_keys)
                    new_bt.add(newtip)
                else:
                    raise RuntimeError(f'What base type is this? f{tip.ptype}')
            else:
                raise RuntimeError(f'What type is this inside my basetype? {tip}')
        return new_bt
    
    def simple_contains_atom(self, atom: PyType | VarType) -> bool:
        self_atom: PyType | VarType
        for self_atom in self:
            if (isinstance(self_atom, VarType) and isinstance(atom, VarType)) or \
                (isinstance(self_atom, PyType) and isinstance(atom, PyType)):
                if self_atom == atom:
                    return True
        return False
    
    def contains_atom(self, atom: PyType | VarType, recursive: bool = False) -> bool:
        non_rec_found = self.simple_contains_atom(atom)
        if non_rec_found is True:
            return True
        if not recursive:
            return False
        self_atom: PyType | VarType
        for self_atom in self:
            if not isinstance(self_atom, PyType):
                continue
            if self_atom.keys is None or len(self_atom.keys) == 0:
                continue
            found = self_atom.keys.contains_atom(atom, recursive)
            if found:
                return True
            if self_atom.values is None or len(self_atom.values) == 0:
                continue
            found = self_atom.values.contains_atom(atom, recursive)
            if found:
                return True
        return False
    
    def contains_basetype(self, other_bt: Basetype, recursive: bool = False) -> bool:
        other_atom: PyType | VarType
        for other_atom in other_bt:
            if not self.contains_atom(other_atom, recursive):
                return False
        return True

    def replace_basetype(self, to_replace: Basetype, replace_with: Basetype) -> Basetype:
        new_bt = Basetype()
        # check if we can replace
        if not self.contains_basetype(to_replace, True):
            return deepcopy(self)
        # replace on first level
        rest_bt = Basetype()
        if self.contains_basetype(to_replace):
            new_bt = deepcopy(replace_with)
            rest_bt = self - to_replace
        for self_atom in rest_bt:
            if not isinstance(self_atom, PyType):
                new_bt.add(deepcopy(self_atom))
                continue
            if self_atom.keys is None or len(self_atom.keys) == 0:
                new_bt.add(deepcopy(self_atom))
                continue
            aux_keys = self_atom.keys.replace_basetype(to_replace, replace_with)
            aux_values = None
            if self_atom.values is not None:
                aux_values = self_atom.values.replace_basetype(to_replace, replace_with)
            aux_pytype = PyType(self_atom.ptype, aux_keys, aux_values)
            new_bt.add(aux_pytype)
        return new_bt
    
    def __contains__(self, o: Basetype) -> bool:
        return self.contains_basetype(o)

    def __lt__(self, other_bt: Basetype) -> bool:
        return other_bt.contains_basetype(self) and not self.contains_basetype(other_bt)
        
    def __le__(self, other_bt: Basetype) -> bool:
        if len(self) == 1 and self[0] == PyType(BottomType):
            return True
        return other_bt.contains_basetype(self)

    def __sub__(self, other_bt: Basetype) -> bool:
        new_bt = Basetype()
        for self_atom in self:
            if other_bt.contains_atom(self_atom):
                continue
            new_bt.add(deepcopy(self_atom))
        return new_bt

    def __eq__(self, other_bt: Basetype) -> bool:
        return self.contains_basetype(other_bt) and other_bt.contains_basetype(self)

    def filter_pytypes(self, supported_list: list[type]) -> Basetype | None:
        new_bt = Basetype()
        if self is None:
            return None
        for tip in self:
            if isinstance(tip, VarType):
                new_bt.add(tip)
                continue
            elif isinstance(tip, PyType):
                # if tip.ptype not in supported_list:
                #     continue
                if not is_supported_type(tip.ptype):
                    continue
                new_keys = tip.keys.filter_pytypes(supported_list) if tip.keys is not None else None
                new_values = tip.values.filter_pytypes(supported_list) if tip.values is not None else None
                new_ptip = PyType(tip.ptype,
                                  keys=new_keys,
                                  values=new_values
                                  )
                new_bt.add(new_ptip)
            else:
                raise RuntimeError(f'This is not a supported element of Basetype: {tip}')
        return new_bt
    
    def get_builtin_from_bt(self) -> Basetype:
        new_bt = Basetype()
        for ptip in self:
            if not isinstance(ptip, PyType):
                if not isinstance(ptip, VarType):
                    raise RuntimeError(f'Type not supported: {ptip}')
                new_bt.add(ptip)
                continue
            new_bt |= ptip.get_builtin_from_pytype()
        return new_bt

    @classmethod
    def check_all_levels(cls, bt1: Basetype, bt2: Basetype) -> bool:
        vt1 = []
        vt2 = []
        for atom in bt1:
            if isinstance(atom, VarType):
                vt1.append(deepcopy(atom))
        for atom in bt2:
            if isinstance(atom, VarType):
                vt2.append(deepcopy(atom))
        if len(vt1) != len(vt2):
            return False
        for atom1 in bt1:
            if isinstance(atom1, PyType) and atom1.keys is not None:
                for atom2 in bt2:
                    if isinstance(atom2, PyType) and atom2.ptype == atom1.ptype:
                        keys_flag = cls.check_all_levels(atom1.keys, atom2.keys)
                        values_flag = True
                        if atom1.values is not None and atom2.values is not None:
                            values_flag = cls.check_all_levels(atom1.values, atom2.values)
                        return keys_flag and values_flag
        return True
    
    def get_all_vartypes(self) -> set[VarType]:
        vt_set = set()
        for atom in self:
            if isinstance(atom, VarType):
                if atom not in vt_set:
                    vt_set.add(deepcopy(atom))
            elif atom.keys is not None:
                vt_from_keys = atom.keys.get_all_vartypes()
                vt_set |= deepcopy(vt_from_keys)
                if atom.values is not None:
                    vt_from_values = atom.values.get_all_vartypes()
                    vt_set |= deepcopy(vt_from_values)
        return vt_set

    @classmethod
    def get_level_pairs(cls, bt1: Basetype, bt2: Basetype) -> None | set[tuple[VarType]]:
        vt1 = []
        vt2 = []
        for atom in bt1:
            if isinstance(atom, VarType):
                vt1.append(deepcopy(atom))
        for atom in bt2:
            if isinstance(atom, VarType):
                vt2.append(deepcopy(atom))
        pairs = itertools.product(vt1, vt2)
        return set(pairs)

    @classmethod
    def get_vartype_pairs(cls, bt1: Basetype, bt2: Basetype) -> set[tuple[VarType]]:
        pairs = cls.get_level_pairs(bt1, bt2)
        for atom1 in bt1:
            if isinstance(atom1, PyType) and atom1.keys is not None:
                for atom2 in bt2:
                    if isinstance(atom2, PyType) and atom2.ptype == atom1.ptype and atom2.keys is not None:
                        new_pairs = cls.get_vartype_pairs(atom1.keys, atom2.keys)
                        if atom1.values is not None and atom2.values is not None:
                            new_pairs += cls.get_vartype_pairs(atom1.values, atom2.values)
                        old_pairs = deepcopy(pairs)
                        pairs = old_pairs & new_pairs
                        visited = []
                        for pair in pairs:
                            visited.append(deepcopy(pair[0]))
                        for old_pair in old_pairs:
                            if old_pair[0] not in visited:
                                pairs.add(deepcopy(old_pair))
                        for new_pair in new_pairs:
                            if new_pair[0] not in visited:
                                pairs.add(deepcopy(new_pair))
        return pairs
    
    @classmethod
    def get_basetype_solutions(cls, bt1: Basetype, bt2: Basetype) -> set[tuple[tuple[VarType]]]:
        if not cls.check_all_levels(bt1, bt2):
            return None
        all_vt1 = bt1.get_all_vartypes()
        all_vt2 = bt2.get_all_vartypes()    
        if len(all_vt1) != len(all_vt2):
            return None
        pairs = cls.get_vartype_pairs(bt1, bt2)
        solution_len = len(all_vt1)  # every vartype in one bt needs a match in the other
        solutions = get_solutions_from_pairs(solution_len, pairs, all_vt1, all_vt2)
        return solutions
    
    @classmethod
    def get_solution_replacements(cls, bt1: Basetype, bt2: Basetype, index = 0) -> list[tuple[dict[VarType, VarType]]]:
        if not cls.check_all_levels(bt1, bt2):
            return None
        all_vt1 = bt1.get_all_vartypes()
        all_vt2 = bt2.get_all_vartypes()    
        if len(all_vt1) != len(all_vt2):
            return None
        pairs = cls.get_vartype_pairs(bt1, bt2)
        solution_len = len(all_vt1)  # every vartype in one bt needs a match in the other
        sol_dicts = get_solutions_from_pairs(solution_len, pairs, all_vt1, all_vt2, index)
        return sol_dicts

    def replace_vartype_from_solution(self, solution_dict: dict[VarType, VarType]):
        new_bt = deepcopy(self)
        for vt1, vt2 in solution_dict.items():
            new_bt = new_bt.replace_vartype(vt1.varexp, vt2.varexp)
        return new_bt

    @classmethod
    def _replace_from_solution(cls, bt1: Basetype, bt2: Basetype, solution, index = 0) -> tuple[Basetype]:
        
        def temp_id(index: int) -> str:
            temp_vt = f'T`{index}'
            return temp_vt
        
        for pair in solution:
            temp_varexp = temp_id(index)
            index += 1
            bt1 = bt1.replace_vartype(pair[0].varexp, temp_varexp)
            bt2 = bt2.replace_vartype(pair[1].varexp, temp_varexp)
        return bt1, bt2, index


class Assignment(hdict):
    def __str__(self):
        if len(self.items()) == 0:
            return ''
        retstr = ''
        for expr, btype in self.items():
            retstr += f'{expr}:{btype} /\\ '
        retstr = retstr[:-4]
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return super().__hash__()
    
    def __eq__(self, other_asig: Assignment) -> bool:
        for expr in self:
            if expr not in other_asig:
                return False
            if self[expr] != other_asig[expr]:
                return False
        for expr in other_asig:
            if expr not in self:
                return False
            if other_asig[expr] != self[expr]:
                return False
        return True

    def replace_basetype(self, to_replace: Basetype, replace_with: Basetype) -> Assignment:
        new_assign = Assignment()
        bt: Basetype
        for expr, bt in self.items():
            new_assign[expr] = bt.replace_basetype(to_replace, replace_with)
        return new_assign

    @classmethod
    def from_str(cls, input_str: str) -> Assignment:
        # (a:bt_a /\ b:bt_b /\ ...)
        assig = Assignment()
        to_translate = elim_paren(input_str)
        str_entries = to_translate.split('/\\')
        for _str_entry in str_entries:
            str_entry = _str_entry.strip()
            expr, str_basetype = str_entry.split(':')
            assig[expr] = Basetype.from_str(str_basetype)
        return assig

    def replace_vartype(self, to_replace: str, replace_with: str) -> Assignment:
        new_assignment = Assignment()
        expr: str
        bt: Basetype
        for expr, bt in self.items():
            new_bt = bt.replace_vartype(to_replace, replace_with)
            new_assignment[expr] = new_bt
        return new_assignment
    
    def replace_vartype_with_basetype(self, to_replace: str, replace_with: Basetype) -> Assignment:
        new_assignment = Assignment()
        expr: str
        bt: Basetype
        for expr, bt in self.items():
            new_bt = bt.replace_vartype_with_basetype(to_replace, replace_with)
            new_assignment[expr] = new_bt
        return new_assignment

    def filter_pytypes(self, supported_list: list[type]) -> Assignment:
        new_assignment = Assignment()
        expr: str
        bt: Basetype
        for expr, bt in self.items():
            new_bt = bt.filter_pytypes(supported_list)
            new_assignment[expr] = new_bt
        return new_assignment
    
    def replace_superclasses(self) -> Assignment:
        new_assignment = Assignment()
        expr: str
        bt: Basetype
        for expr, bt in self.items():
            new_bt = bt.get_builtin_from_bt()
            new_assignment[expr] = new_bt
        return new_assignment

    @classmethod
    def lub(cls, assign1: Assignment, assign2: Assignment) -> Assignment:
        new_assign = Assignment()
        visited = set()
        for expr, bt1 in assign1.items():
            if expr not in assign2:
                new_assign[expr] = deepcopy(bt1)
            else:
                new_assign[expr] = Basetype.lub(bt1, assign2[expr])
                visited.add(deepcopy(expr))
        for expr, bt2 in assign2.items():
            if expr not in visited:
                new_assign[expr] = deepcopy(bt2)
        return new_assign
    
    def get_all_vartypes(self) -> set[VarType]:
        all_vt = set()
        bt: Basetype
        for expr, bt in self.items():
            all_vt |= bt.get_all_vartypes()
        return all_vt

    @classmethod
    def get_vartype_pairs(cls, assign1: Assignment, assign2: Assignment) -> set[tuple[VarType]]:
        pairs = set()
        expr_set1 = set(assign1)
        expr_set2 = set(assign2)
        if expr_set1 != expr_set2:
            just1 = expr_set1 - expr_set2
            just2 = expr_set2 - expr_set1
            raise RuntimeError(f'Different expressions between assignments. {just1} in first and {just2} in second')
        for expr, bt1 in assign1.items():
            bt2 = assign2[expr]
            new_pairs = Basetype.get_vartype_pairs(bt1, bt2)
            old_pairs = deepcopy(pairs)
            pairs = old_pairs & new_pairs
            visited = []
            for pair in pairs:
                visited.append(deepcopy(pair[0]))
            for old_pair in old_pairs:
                if old_pair[0] not in visited:
                    pairs.add(deepcopy(old_pair))
            for new_pair in new_pairs:
                if new_pair[0] not in visited:
                    pairs.add(deepcopy(new_pair))
        return pairs

    @classmethod
    def get_vartype_solutions(cls, assign1: Assignment, assign2: Assignment) -> set[tuple[tuple[VarType]]]:
        all_vt1 = assign1.get_all_vartypes()
        all_vt2 = assign2.get_all_vartypes()
        if len(all_vt1) != len(all_vt2):
            return None
        pairs = cls.get_vartype_pairs(assign1, assign2)
        solution_len = len(all_vt1)  # every vartype in one bt needs a match in the other
        solutions = get_solutions_from_pairs(solution_len, pairs, all_vt1, all_vt2)
        return solutions
    
    @classmethod
    def replace_from_solution(cls, assign1: Assignment, assign2: Assignment, solution: tuple[VarType], index: int = 0) -> tuple[Assignment]:
        # def temp_id(index):
        #     # nonlocal index
        #     temp_vt = f'T`{index}'
        #     index += 1
        #     return temp_vt
        
        new_assign1 = Assignment()
        new_assign2 = Assignment()
        bt: Basetype
        for expr in assign1:
            new_bt1, new_bt2, index = Basetype.replace_from_solution(assign1[expr], assign2[expr], solution, index)
            new_assign1[expr] = deepcopy(new_bt1)
            new_assign2[expr] = deepcopy(new_bt2)
        return new_assign1, new_assign2, index


class Relation:
    def __init__(self, relop: RelOp = None, bt_left: Basetype = None, bt_right: Basetype = None):
        self.relop = relop
        self.bt_left = deepcopy(bt_left)
        self.bt_right = deepcopy(bt_right)

    def __str__(self):
        if self.relop == RelOp.LEQ:
            relstr = '<='
        elif self.relop == RelOp.EQ:
            relstr = '=='
        else:
            raise RuntimeError('Unsupported relation op')
        return f'{self.bt_left} {relstr} {self.bt_right}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: Relation):
        if self.relop.value == other.relop.value and self.bt_left == other.bt_left and self.bt_right == other.bt_right:
            return True
        return False

    def __hash__(self):
        # return -1
        return hash((self.bt_left, self.relop.value, self.bt_right))

    @classmethod
    def from_str(cls, input_str: str) -> Relation:
        to_translate = elim_paren(input_str.strip())
        # to_translate = str_relation
        found = False
        op = None
        for op in RelOp:
            if op.value in to_translate:
                found = True
                break
        if not found:
            raise RuntimeError(f'Operation for {to_translate} not supported')
        str_operands = to_translate.split(f'{op.value}')
        bt_left = Basetype.from_str(str_operands[0].strip())
        bt_right = Basetype.from_str(str_operands[1].strip())
        return Relation(op, bt_left, bt_right)

    def replace_vartype(self, to_replace: str, replace_with: str) -> Relation:
        new_bt_left = self.bt_left.replace_vartype(to_replace, replace_with)
        new_bt_right = self.bt_right.replace_vartype(to_replace, replace_with)
        new_rel = Relation(self.relop, new_bt_left, new_bt_right)
        return new_rel

    def filter_pytypes(self, supported_list: list[type]) -> Relation:
        new_bt_left = self.bt_left.filter_pytypes(supported_list)
        new_bt_right = self.bt_right.filter_pytypes(supported_list)
        new_rel = Relation(self.relop, new_bt_left, new_bt_right)
        return new_rel

    def replace_superclasses(self) -> Relation:
        new_bt_left = self.bt_left.get_builtin_from_bt()
        new_bt_right = self.bt_right.get_builtin_from_bt()
        new_rel = Relation(self.relop, new_bt_left, new_bt_right)
        return new_rel
    
    def replace_basetype(self, to_replace: Basetype, replace_with: Basetype) -> Relation:
        new_rel = Relation()
        new_rel.relop = deepcopy(self.relop)
        new_rel.bt_left = self.bt_left.replace_basetype(to_replace, replace_with)
        new_rel.bt_right = self.bt_right.replace_basetype(to_replace, replace_with)
        return new_rel


class AndConstraints(hset):
    def __str__(self):
        if len(self) == 0:
            return ''
        retstr = ''
        if not len(self):
            return retstr
        for rel in self:
            retstr += f'({rel}) /\\ '
        retstr = retstr[:-4]
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return super().__hash__()

    @classmethod
    def from_str(cls, input_str: str) -> AndConstraints:
        # ((bt_1 <= bt 2) /\ (bt_3 == bt_4))
        and_constr = AndConstraints()
        to_translate = elim_paren(input_str)
        str_entries = to_translate.split('/\\')
        for _str_relation in str_entries:
            str_relation = _str_relation.strip()
            rel = Relation.from_str(str_relation)
            and_constr.add(rel)
        return and_constr

    def replace_vartype(self, to_replace: str, replace_with: str) -> AndConstraints:
        new_andconstr = AndConstraints()
        rel: Relation
        for rel in self:
            new_rel = rel.replace_vartype(to_replace, replace_with)
            new_andconstr.add(new_rel)
        return new_andconstr

    def filter_pytypes(self, supported_list: list[type]) -> AndConstraints:
        new_andconstr = AndConstraints()
        rel: Relation
        for rel in self:
            new_rel = rel.filter_pytypes(supported_list)
            new_andconstr.add(new_rel)
        return new_andconstr

    def replace_superclasses(self) -> AndConstraints:
        new_andconstr = AndConstraints()
        rel: Relation
        for rel in self:
            new_rel = rel.replace_superclasses()
            new_andconstr.add(new_rel)
        return new_andconstr

    def replace_basetype(self, to_replace: Basetype, replace_with: Basetype) -> AndConstraints:
        new_andconstr = AndConstraints()
        rel: Relation
        for rel in self:
            new_rel = rel.replace_basetype(to_replace, replace_with)
            new_andconstr.add(new_rel)
        return new_andconstr
    
    @classmethod
    def lub(cls, andc1: AndConstraints, andc2: AndConstraints) -> AndConstraints:
        pass


class OrConstraints(hset):
    def __str__(self):
        if len(self) == 0:
            return ''
        retstr = ''
        if not len(self):
            return retstr
        for rel in self:
            retstr += f'{rel} \\/ '
        retstr = retstr[:-4]
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return super().__hash__()

    @classmethod
    def from_str(cls, input_str: str) -> OrConstraints:
        # ((bt_1 <= bt 2) /\ (bt_3 == bt_4))
        or_constr = OrConstraints()
        to_translate = elim_paren(input_str)
        str_entries = to_translate.split('\\/')
        for _str_relation in str_entries:
            str_relation = _str_relation.strip()
            rel = Relation.from_str(str_relation)
            or_constr.add(rel)
        return or_constr


class State:
    def __init__(self, assignment: Assignment = None, constraints: AndConstraints = None):
        self.gen_id = 1
        if assignment is None:
            self.assignment = Assignment()
        else:
            self.assignment = deepcopy(assignment)
        if constraints is None:
            self.constraints = AndConstraints()
        else:
            self.constraints = deepcopy(constraints)

    def __str__(self):
        if len(self.constraints) == 0:
            retstr = f'({self.assignment})'
        else:
            retstr = f'({self.assignment}) ^ ({self.constraints})'
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((hash(self.assignment), hash(self.constraints)))

    def __eq__(self, other: State):
        return hash(self) == hash(other)

    @classmethod
    def from_str(cls, input_str: str) -> State:
        # (assignment ^ constraints)
        delimiter = '^'
        to_translate = elim_paren(input_str)
        str_assignment = None
        str_constraints = None
        if delimiter not in to_translate:
            str_assignment = to_translate.strip()
        else:
            (str_assignment, str_constraints) = to_translate.split(delimiter)
            (str_assignment, str_constraints) = (str_assignment.strip(), str_constraints.strip())
        asgn = Assignment.from_str(str_assignment)
        if str_constraints is not None:
            constr = AndConstraints.from_str(str_constraints)
        else:
            constr = None
        st = State(asgn, constr)
        return st


    def replace_vartype(self, to_replace: str, replace_with: str) -> State:
        new_assignment = self.assignment.replace_vartype(to_replace, replace_with)
        new_constraints = self.constraints.replace_vartype(to_replace, replace_with)
        new_state = State(new_assignment, new_constraints)
        return new_state

    def filter_pytypes(self, supported_list: list[type]) -> State:
        new_assignment = self.assignment.filter_pytypes(supported_list)
        new_constraints = self.constraints.filter_pytypes(supported_list)
        new_state = State(new_assignment, new_constraints)
        return new_state
    
    def replace_superclasses(self) -> State:
        new_assignment = self.assignment.replace_superclasses()
        new_constraints = self.constraints.replace_superclasses()
        new_state = State(new_assignment, new_constraints)
        return new_state

    def generate_id(self):
        retstr = f'T{self.gen_id}'
        self.gen_id = self.gen_id + 1
        return retstr

    def replace_assignment_basetypes(self, to_replace: Basetype, replace_with: Basetype) -> State:
        new_state = State()
        new_state.constraints = deepcopy(self.constraints)
        bt: Basetype
        for expr, bt in self.assignment.items():
            new_state.assignment[expr] = bt.replace_basetype(to_replace, replace_with)
        return new_state
        
    @classmethod
    def parse_single_result_string(cls, case: str) -> list[Relation]:
        relations = []
        m_res = case.replace('[nil]', '')
        result_list = m_res.split('/\\')
        for elem in result_list:
            aux = elem.strip('() ')
            rel = Relation.from_str(aux)
            relations.append(deepcopy(rel))
        return relations

    def solve_constraints(self, strategy_str: str = strat1, dump_file: str | None = None, ofile: str = DEFAULT_SOLVER_OUT) -> State:
        maude.init()
        init_module = INIT_MAUDE_PATH
        if not maude.load(init_module):
            raise RuntimeError(f'Could not load {init_module}')
        modulename = 'tempmod'
        constr_module_name = 'CONSTR'
        constr_module = maude.getModule(constr_module_name)
        if constr_module is None:
            raise RuntimeError(f'Could not get module {constr_module}')
        if len(self.constraints) == 0:
            return deepcopy(self)
        c_value = str(self.constraints)
        m_input = mod_generator('tempmod', c_value, dump_file)
        if not maude.input(m_input):
            raise RuntimeError('Maude input operation failed')
        mod = maude.getModule(modulename)
        if mod is None:
            raise RuntimeError(f'Maude module {modulename} not found')
        term_str = 'c [nil]'
        term = mod.parseTerm(term_str)
        if term is None:
            raise RuntimeError(f'Cannot parse term {term_str}')
        strat = constr_module.parseStrategy(strategy_str)
        if not strat:
            raise RuntimeError(f'Cannot parse strategy {strategy_str}')
        srew = term.srewrite(strat)
        if srew is None:
            raise RuntimeError(f'Could not rewrite using {strategy_str}')
        aux_len = 0
        relations = None
        for result, nrew in srew:
            if aux_len > 0:
                raise RuntimeError('Too many maude results')
            aux_len += 1
            open(ofile, 'w').write(f'{result}')
            relations = self.parse_single_result_string(str(result))
        new_state = State()
        # new_state.assignment = deepcopy(self.assignment)
        if relations is None:
            raise RuntimeError(f'Empty relations for {str(result)}')
        new_state = deepcopy(self)
        for rel in relations:
            if len(rel.bt_left) != 1 or not isinstance(rel.bt_left[0], VarType):
                continue
            new_state = new_state.replace_basetype(rel.bt_left, rel.bt_right)
        new_state = new_state.remove_valid_relations()
        # if len(new_state.constraints) != 0:
        #     return BottomState()
        # for expr, bt in new_state.assignment.items():
        #     if bt == Basetype({PyType(BottomType)}):
        #         return BottomState()
        return new_state
    
    def remove_valid_relations(self):
        new_state = State()
        new_state.assignment = deepcopy(self.assignment)
        rel: Relation
        for rel in self.constraints:
            if rel.relop == RelOp.LEQ:
                comparator = rel.bt_left.__le__
            elif rel.relop == RelOp.EQ:
                comparator = rel.bt_left.__eq__
            else:
                raise RuntimeError(f'Relation {rel} has invalida comparator {rel.relop}')
            if not comparator(rel.bt_right):
                new_state.constraints.add(deepcopy(rel))
        return new_state

    def __eq__(self, other_state: State) -> bool:
        return (self.assignment == other_state.assignment) and (self.constraints == other_state.constraints)

    def is_same(self, other_state: State) -> bool:
        state1 = self.solve_constraints(strat1)
        state2 = other_state.solve_constraints(strat1)
        return state1 == state2
        
    def replace_basetype(self, to_replace: Basetype, replace_with: Basetype) -> State:
        new_state = State()
        new_state.assignment = self.assignment.replace_basetype(to_replace, replace_with)
        new_state.constraints = self.constraints.replace_basetype(to_replace, replace_with)
        return new_state 

    @classmethod
    def lub(cls, state1: State, state2: State) -> State:
        new_state = State()
        new_state.assignment = Assignment.lub(state1.assignment, state2. assignment)
        new_state.constraints = AndConstraints.lub(state1.constraints, state2.constraints)
        return new_state    

    @classmethod
    def get_vartype_pairs(cls, state1: State, state2: State) -> set[tuple[VarType]]:
        return Assignment.get_vartype_pairs(state1.assignment, state2.assignment)
    
    @classmethod
    def get_vartype_solutions(cls, state1: State, state2: State) -> set[tuple[tuple[VarType]]]:
        return Assignment.get_vartype_solutions(state1.assignment, state2.assignment)
    
    @classmethod
    #def replace_from_solution(cls, assign1: Assignment, assign2: Assignment, solution: tuple[VarType], index: int = 0) -> tuple[Assignment]:
    def replace_from_solution(cls, state1: State, state2: State, solution: tuple[VarType], index: int = 0) -> tuple[State]:
        state1 = State()
        state2 = State()
        bt: Basetype
        for expr in state1.assignment:
            new_bt1, new_bt2, index = Basetype.replace_from_solution(state1.assignment[expr], 
                                                                     state2.assignment[expr], 
                                                                     solution, 
                                                                     index)
            state1.constraints = state1.constraints.replace_vartype(state1.assignment[expr], new_bt1)
            state2.constraints = state2.constraints.replace_vartype(state2.assignment[expr], new_bt2)
            state1.assignment[expr] = deepcopy(new_bt1)
            state2.assignment[expr] = deepcopy(new_bt2)
        return state1, state2, index



class BottomState(State):
    pass


class StateSet(hset):
    def __str__(self):
        if len(self) == 0:
            return '()'
        retstr = ''
        for state in self:
            retstr += rf'{state} \/ '
        retstr = retstr[0:-4]
        return retstr

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return super().__hash__()

    @classmethod
    def from_str(cls, input_str: str) -> StateSet:
        delimiter = '\\/'
        to_translate = input_str
        str_states = to_translate.split(delimiter)
        state_set = StateSet()
        for _str_state in str_states:
            str_state = _str_state.strip()
            state = State.from_str(str_state)
            state_set.add(state)
        return state_set

    def replace_vartype(self, to_replace: str, replace_with: str) -> StateSet:
        new_state_set = StateSet()
        st: State
        for st in self:
            new_state = st.replace_vartype(to_replace, replace_with)
            new_state_set.add(new_state)
        return new_state_set

    def filter_pytypes(self, supported_list: list[type]) -> StateSet:
        new_state_set = StateSet()
        st: State
        for st in self:
            new_state = st.filter_pytypes(supported_list)
            new_state_set.add(new_state)
        return new_state_set
    
    def replace_superclasses(self) -> StateSet:
        new_state_set = StateSet()
        st: State
        for st in self:
            new_state = st.replace_superclasses()
            new_state_set.add(new_state)
        return new_state_set
    
    def replace_basetype(self, to_replace: Basetype, replace_with: Basetype) -> StateSet:
        new_state_set = StateSet()
        state: State
        for state in self:
            new_state = state.replace_basetype(to_replace, replace_with)
            new_state_set.add(deepcopy(new_state))
        return new_state_set

    def solve_states(self):
        solved_stateset = StateSet()
        state: State
        for state in self:
            solved_state = state.solve_constraints()
            # solved_state = solved_state.remove_valid_relations()
            if solved_state != BottomState():
                solved_stateset.add(deepcopy(solved_state))
        return solved_stateset

    def __or__(self, other_set: StateSet) -> StateSet:
        new_stateset = deepcopy(self)
        for other_state in other_set:
            new_stateset.add(deepcopy(other_state))
        return new_stateset


class FuncSpec:
    def __init__(self, _in: State = None, _out: State = None):
        if not _in:
            self.in_state = State()
        else:
            self.in_state = deepcopy(_in)
        if not _out:
            self.out_state = State()
        else:
            self.out_state = deepcopy(_out)

    def __str__(self):
        return f'({self.in_state} -> {self.out_state})'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((hash(self.in_state), hash(self.out_state)))

    def __eq__(self, other: FuncSpec):
        return hash(self) == hash(other)

    @classmethod
    def from_str(cls, input_str: str) -> FuncSpec:
        funcspec = FuncSpec()
        delimiter = r'->'
        to_translate = elim_paren(input_str)
        (str_in, str_out) = to_translate.split(delimiter)
        str_in = str_in.strip()
        str_out = str_out.strip()
        funcspec.in_state = State.from_str(str_in)
        funcspec.out_state = State.from_str(str_out)
        return funcspec

    def replace_vartype(self, to_replace: str, replace_with: str):
        new_in = self.in_state.replace_vartype(to_replace, replace_with)
        new_out = self.out_state.replace_vartype(to_replace, replace_with)
        new_funcspec = FuncSpec(new_in, new_out)
        return new_funcspec

    def filter_pytypes(self, supported_list: list[type]) -> FuncSpec:
        new_in = self.in_state.filter_pytypes(supported_list)
        new_out = self.out_state.filter_pytypes(supported_list)
        new_funcspec = FuncSpec(new_in, new_out)
        return new_funcspec
    
    def replace_superclasses(self) -> FuncSpec:
        new_in = self.in_state.replace_superclasses()
        new_out = self.out_state.replace_superclasses()
        new_funcspec = FuncSpec(new_in, new_out)
        return new_funcspec
    
    def replace_basetype(self, to_replace: Basetype, replace_with: Basetype) -> FuncSpec:
        new_funcspec = FuncSpec()
        new_funcspec.in_state = self.in_state.replace_basetype(to_replace, replace_with)
        new_funcspec.out_state = self.out_state.replace_basetype(to_replace, replace_with)
        return new_funcspec


# for later use, sequences with implicit types contained
extra_sequences = {
    PyType(range):      Basetype({PyType(int)}),
    PyType(str):        Basetype({PyType(str)}),
    PyType(bytes):      Basetype({PyType(int)}),
    PyType(bytearray):  Basetype({PyType(int)}),
    PyType(memoryview): Basetype({PyType(int)})
}
