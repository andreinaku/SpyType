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


strat1 = 'one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; Step5 ! ; Step6 ! '
strat2 = 'one(Step1) ! ; one(Step2) ! ; one(Step3) ! ; one(Step4) ! ; Step5 ! ; Step6 ! '
INIT_MAUDE_PATH = os.getcwd() + os.sep + 'init.maude'


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
    
    def __leq__(self, other_bt: Basetype) -> bool:
        return self.contains_basetype(other_bt)

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

    def solve_constraints(self, strategy_str: str, dump_file: str | None = None) -> State:
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
            relations = self.parse_single_result_string(str(result))
        new_state = State()
        new_state.assignment = deepcopy(self.assignment)
        if relations is None:
            raise RuntimeError(f'Empty relations for {str(result)}')
        for rel in relations:
            if len(rel.bt_left) > 1 or not isinstance(rel.bt_left[0], VarType):
                raise TypeError(f'{rel.bt_left} should be a VarType')
            to_replace = rel.bt_left[0]
            new_state.assignment = new_state.assignment.replace_vartype_with_basetype(to_replace, rel.bt_right)
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
