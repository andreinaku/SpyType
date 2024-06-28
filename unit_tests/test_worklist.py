from testbase import *
from type_inference.simple_inference import *


class WorklistTestCases(unittest.TestCase):
    def test_1(self):
        mfp_in, mfp_out = run_infer('type_inference/test_funcs.py', 'f1')
        print(f'{mfp_in}{os.linesep}{mfp_out}')
        self.assertEqual(True, True)
