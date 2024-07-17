from testbase import *
from simple_inference import *


def pprint_mfp(mfp_in, mfp_out):
    print(f'{os.linesep}MFP IN:{os.linesep}')
    for id, ss in mfp_in.items():
        print(f'\t{id}: {ss}')
    print(f'{os.linesep}MFP OUT:{os.linesep}')
    for id, ss in mfp_out.items():
        print(f'\t{id}: {ss}')


sourcepath = 'benchmarks/mine/benchfuncs.py'


class WorklistTestCases(unittest.TestCase):

    def test_0(self):
        mfp_in, mfp_out = run_infer(sourcepath, 'if_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_1(self):
        mfp_in, mfp_out = run_infer(sourcepath, 'assign_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_2(self):
        mfp_in, mfp_out = run_infer(sourcepath, 'add_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_3(self):
        mfp_in, mfp_out = run_infer(sourcepath, 'append_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_4(self):
        mfp_in, mfp_out = run_infer(sourcepath, 'append_2')
        pprint_mfp(mfp_in, mfp_out)

    def test_5(self):
        mfp_in, mfp_out = run_infer(sourcepath, 'append_3')
        pprint_mfp(mfp_in, mfp_out)

    def test_6(self):
        mfp_in, mfp_out = run_infer(sourcepath, 'for_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_7(self):
        mfp_in, mfp_out = run_infer(sourcepath, 'for_2')
        pprint_mfp(mfp_in, mfp_out)

    def test_8(self):
        mfp_in, mfp_out = run_infer(sourcepath, 'if_2')
        pprint_mfp(mfp_in, mfp_out)

    def test_9(self):
        mfp_in, mfp_out = run_infer(sourcepath, 'while_1')
        pprint_mfp(mfp_in, mfp_out)
 
    def test_10(self):
        mfp_in, mfp_out = run_infer(sourcepath, 'try_1')
        pprint_mfp(mfp_in, mfp_out)
