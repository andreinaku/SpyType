import importlib
import types

module_code = '''
class foo:
    pass
'''

module_name = "dynamic_module"
module = types.ModuleType(module_name)
exec(module_code, module.__dict__)

# aux = importlib.import_module(exec(code))

print(eval("module.foo"))
