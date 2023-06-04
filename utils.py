from __future__ import annotations
from copy import deepcopy
import ast
import astor
import string


id_index = 0
container_ptypes = [list, set, tuple]
SPECTYPE_MARKER = '?'
BOTTOM = 'T_bot'
OUTMARKER = '__out_'
ORIGMARKER = '__orig_'
INMARKER = '__in_'
RETURN_NAME = 'return'
GLB = 1
LUB = 2
SIGN_LE = "<="
SIGN_GT = ">"


class BottomType:
    pass


class TopType:
    pass


class ErrorType:
    pass


def is_varname(code):
    if '`' in code or code == 'return':
        return True
    astnode = ast.parse(code).body[0].value
    if isinstance(astnode, ast.Name):
        return True
    return False


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    global id_index
    ret = id_index + 1
    id_index = id_index + 1
    return ret
    # return ''.join(random.choice(chars) for _ in range(size))


class hset(set):
    def __getitem__(self, index):
        ll = list(self)
        return ll[index]

    def __key(self):
        ll = []
        for elem in self:
            ll.append(hash(elem))
        ll = sorted(ll)
        return tuple(ll)

    def __hash__(self):
        return hash(self.__key())

    def __or__(self, other):
        return hset(set(self) | set(other))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        res = '{'
        if len(self):
            for elem in self:
                res = res + str(elem) + ','
            res = res[:-1]
        res = res + '}'
        return res

    def __repr__(self):
        return str(self)

    def __mul__(self, other):
        # only for sets of type expressions
        retset = hset()
        if not len(self):
            return deepcopy(other)
        if not len(other):
            return deepcopy(self)
        for te1 in self:
            for te2 in other:
                retset.add(te1 + te2)
        return retset


class hdict(dict):
    def __key(self):
        llk = []
        keylist = []
        for k in self.keys():
            keylist.append(str(k))
        keylist.sort()
        for k in keylist:
            entryhash = hash((hash(k), hash(self[k])))
            llk.append(entryhash)
        tuple_key = tuple(llk)
        return tuple_key

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not (self == other)

    @staticmethod
    def meet(hd1, hd2):
        newhd = hdict()
        for varname in hd1:
            if varname not in hd2:
                newhd[varname] = deepcopy(hd1[varname])
            else:
                newhd[varname] = hd1[varname] | hd2[varname]
        for varname in hd2:
            if varname not in hd1:
                newhd[varname] = deepcopy(hd2[varname])
            else:
                newhd[varname] = hd1[varname] | hd2[varname]
        return newhd


def tosrc(node: ast.AST):
    try:
        delattr(node, '_pp')
    except AttributeError:
        pass
    if isinstance(node, ast.While):
        ret_string = 'while {}'.format(astor.to_source(node.test).strip())
    else:
        ret_string = astor.to_source(node).strip()
    ret_string.replace('\n', '')
    ret_string = elim_paren(ret_string)
    return ret_string


def elim_paren(foo):
    if foo.startswith('(') and foo.endswith(')'):
        return foo[1:-1]
    return foo
