from testbase import *
from type_inference.simple_inference import *


def pprint_mfp(mfp_in, mfp_out):
    print(f'{os.linesep}MFP IN:{os.linesep}')
    for id, ss in mfp_in.items():
        print(f'\t{id}: {ss}')
    print(f'{os.linesep}MFP OUT:{os.linesep}')
    for id, ss in mfp_out.items():
        print(f'\t{id}: {ss}')


class WorklistTestCases(unittest.TestCase):
    def test_1(self):
        mfp_in, mfp_out = run_infer('benchmarks/mine/benchfuncs.py', 'assign_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_2(self):
        mfp_in, mfp_out = run_infer('benchmarks/mine/benchfuncs.py', 'life_add_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_3(self):
        mfp_in, mfp_out = run_infer('benchmarks/mine/benchfuncs.py', 'add_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_4(self):
        mfp_in, mfp_out = run_infer('benchmarks/mine/benchfuncs.py', 'append_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_5(self):
        mfp_in, mfp_out = run_infer('benchmarks/mine/benchfuncs.py', 'append_2')
        pprint_mfp(mfp_in, mfp_out)
