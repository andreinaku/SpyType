'''
Worklist algorithm implementation
Based on description from "Principles of Program Analysis" by Flemming N. et al.
'''

import os, sys
sys.path.append(os.getcwd())
from statev2.basetype import *
from statev2.transfer import TransferFunc
from crackedcfg import CFG


class WorklistAnalyzer:
    def __init__(self, cfg: CFG, init: StateSet):
        self.W = []
        self.Analysis = dict()
        for id, entry in cfg.cfgdict.items():
            children_list = entry['successors']
            for child in children_list:
                to_add = (id, child)
                if to_add not in self.W:
                    self.W.append(deepcopy(to_add))
        for id in cfg.cfgdict:
            self.Analysis[id] = StateSet()
        self.entryblock = cfg.entryblock.id
        self.Analysis[cfg.entryblock.id] = deepcopy(init)
        self.blockinfo = cfg.cfgdict
        self.init_ss = deepcopy(init)
        self.merge = StateSet.lub
 
    def f(self, l: int):
        node_code = self.blockinfo[l]['statements'][0]
        input_ss = self.Analysis[l]
        tf = TransferFunc(input_ss)
        tf.visit(node_code)
        ret_set = tf.state_set.remove_no_names()
        ret_set = ret_set.solve_states() 
        return deepcopy(ret_set)

    def Iteration(self):
        while len(self.W):
            pair = self.W.pop(0)
            l1 = pair[0]
            l2 = pair[1]
            l1_analyzed = self.f(l1)
            if not (l1_analyzed <= self.Analysis[l2]):
                self.Analysis[l2] = self.merge(self.Analysis[l2], l1_analyzed)
                for child in self.blockinfo[l2]['successors']:
                    to_add = (l2, child)
                    if to_add not in self.W:
                        self.W.append(deepcopy(to_add))

    def mfp_solution(self) -> tuple:
        mfp_in = self.Analysis
        mfp_out = dict()
        for l in self.Analysis:
            mfp_out[l] = self.f(l)
        return mfp_in, mfp_out
