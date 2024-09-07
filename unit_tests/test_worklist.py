from testbase import *
from spytype import *


def pprint_mfp(mfp_in, mfp_out):
    print(f'{os.linesep}MFP IN:{os.linesep}')
    for id, ss in mfp_in.items():
        print(f'\t{id}: {ss}')
    print(f'{os.linesep}MFP OUT:{os.linesep}')
    for id, ss in mfp_out.items():
        print(f'\t{id}: {ss}')


sourcepath = os.path.join(PROJECT_DIR, 'benchmarks/mine/benchfuncs.py')


class WorklistTestCases(unittest.TestCase):

    def test_0(self):
        os.chdir(PROJECT_DIR)
        mfp_in, mfp_out = run_infer(sourcepath, 'if_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_1(self):
        os.chdir(PROJECT_DIR)
        mfp_in, mfp_out = run_infer(sourcepath, 'assign_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_2(self):
        os.chdir(PROJECT_DIR)
        mfp_in, mfp_out = run_infer(sourcepath, 'add_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_3(self):
        os.chdir(PROJECT_DIR)
        mfp_in, mfp_out = run_infer(sourcepath, 'append_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_4(self):
        os.chdir(PROJECT_DIR)
        mfp_in, mfp_out = run_infer(sourcepath, 'append_2')
        pprint_mfp(mfp_in, mfp_out)

    def test_5(self):
        os.chdir(PROJECT_DIR)
        mfp_in, mfp_out = run_infer(sourcepath, 'append_3')
        pprint_mfp(mfp_in, mfp_out)

    def test_6(self):
        os.chdir(PROJECT_DIR)
        mfp_in, mfp_out = run_infer(sourcepath, 'for_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_7(self):
        os.chdir(PROJECT_DIR)
        mfp_in, mfp_out = run_infer(sourcepath, 'for_2')
        pprint_mfp(mfp_in, mfp_out)

    def test_8(self):
        os.chdir(PROJECT_DIR)
        mfp_in, mfp_out = run_infer(sourcepath, 'if_2')
        pprint_mfp(mfp_in, mfp_out)

    def test_9(self):
        os.chdir(PROJECT_DIR)
        mfp_in, mfp_out = run_infer(sourcepath, 'while_1')
        pprint_mfp(mfp_in, mfp_out)
 
    def test_10(self):
        os.chdir(PROJECT_DIR)
        mfp_in, mfp_out = run_infer(sourcepath, 'try_1')
        pprint_mfp(mfp_in, mfp_out)

    def test_11(self):
        os.chdir(PROJECT_DIR)
        init_ss = StateSet.from_str(r'(a:int /\ b:int)')
        code = 'c = a + b'
        tree = ast.parse(code)
        result = run_infer_on_tree(tree, init_ss, 5, 5)
        print(result)
