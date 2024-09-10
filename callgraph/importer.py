import importlib.util
import sys


file_path = "/Users/andrei/work/doctorat/SpyType/callgraph/importee.py"
module_name = "modname"
spec = importlib.util.spec_from_file_location(module_name, file_path)
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)
print(module.CustomType)
print(issubclass(module.KidType, module.ParentType))
