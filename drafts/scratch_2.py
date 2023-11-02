import ast
from Translator import Translator
import astor
from copy import deepcopy


POSONLY_MARKER = '__po_'
VARARG_MARKER = '__va_'
KEYWORDONLY_MARKER = '__ko_'
KWARG_MARKER = '__kw_'
MARKERS = [POSONLY_MARKER, VARARG_MARKER, KEYWORDONLY_MARKER, KWARG_MARKER]

# tree = ast.parse('''
# foo(1,2,3,4,5,6,7,e=8,f=9,x=10,y=11,z=12,k=13)
# ''')
tree = ast.parse('''
foo(1,2,3,4,5,6,7,x=8,k=9,f=10,y=11,z=12,e=13)
''')

# def foo(a, b, /, c, *d, e, f, **g):
spec = (r'__po_a:T?1 /\ __po_b:T?2 /\ c:T?3 /\ __va_d:T?4 /\ __ko_e:T?5 /\ __ko_f:T?6 /\ __kw_g:T?7 ^ '
        r'(T?1:int /\ T?2:int /\ T?3:int /\ T?4:TopType /\ T?5:int /\ T?6:int /\ T?7:TopType)')
aux = Translator.translate_as(spec)
print(aux)

va = deepcopy(list(aux.va))
callnode = tree.body[0].value
pos_call_list = []
keyword_call_dict = {}
for node in callnode.args:
    pos_call_list.append(astor.to_source(node).strip())
for node in callnode.keywords:
    # keyword_call_dict.append(node.arg)
    keyword_call_dict[node.arg] = node.value
print(ast.dump(tree, indent=4))


dd = dict()


def f():
    if (len(pos_call_list) > 0 or len(keyword_call_dict) > 0) and len(va) == 0:
        return False
    if (len(pos_call_list) == 0 and len(keyword_call_dict) == 0) and len(va) > 0:
        return False
    if len(va) == 0 and len(pos_call_list) == 0 and len(keyword_call_dict) == 0:
        return True
    va_var: str = va.pop(0)
    if va_var.startswith(POSONLY_MARKER):
        if len(pos_call_list) == 0:
            return False
        call_entry = pos_call_list.pop(0)
        dd[va_var] = call_entry
        f()
        # f(va_index+1)
    elif va_var.startswith(VARARG_MARKER):
        while len(pos_call_list) > 0:
            call_entry = pos_call_list.pop(0)
            if va_var not in dd:
                dd[va_var] = (call_entry,)
            else:
                dd[va_var] = dd[va_var] + (call_entry,)
        if va_var not in dd:
            return False
        f()
    elif va_var.startswith(KEYWORDONLY_MARKER):
        if len(keyword_call_dict) == 0:
            return False
        varname = va_var[len(KEYWORDONLY_MARKER):]
        if varname not in keyword_call_dict:
            return False
        dd[va_var] = astor.to_source(keyword_call_dict.pop(varname)).strip()
        f()
    elif va_var.startswith(KWARG_MARKER):
        if len(keyword_call_dict) == 0:
            return False
        keyword_list = list(keyword_call_dict)
        while len(keyword_call_dict) > 0:
            ko_key = keyword_list.pop(0)
            call_entry = astor.to_source(keyword_call_dict.pop(ko_key)).strip()
            if va_var not in dd:
                dd[va_var] = {ko_key: call_entry}
            else:
                dd[va_var].update({ko_key: call_entry})
        f()
    else:
        if len(pos_call_list) > 0:
            call_entry = pos_call_list.pop(0)
        elif len(keyword_call_dict) > 0:
            call_entry = keyword_call_dict.pop(0)
        else:
            return False
        dd[va_var] = call_entry
        f()


f()
print(dd)
