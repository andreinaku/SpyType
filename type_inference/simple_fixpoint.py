import os, sys
sys.path.append(os.getcwd())
from statev2.basetype import *
from crackedcfg import CFG


MAXROUNDS = 3


class NodeInfer:
    def __init__(self, _in: StateSet, _code: str):
        self.out_as = StateSet()
        self.in_as = _in
        self.code = _code


def dump_trounds(trounds: list[dict[int, NodeInfer]]):
    writestr = ''
    for i in range(0, len(trounds)):
        writestr += 'round = {}\n'.format(i)
        for k, v in trounds[i].items():
            writestr += '{}:\n\tin: {}\n{}\n\tout: {}\n\n\n'.format(k, v.in_as, v.code, v.out_as)
        writestr += '--------------------------------\n\n\n'
    open('trounds.txt', 'w').write(writestr)


def dump_roundineqs(round_ineqs: dict[int, dict[int, tuple[StateSet]]]):
    writestr = ''
    for round_id, dd in round_ineqs.items():
        writestr += 'round = {}\n'.format(round_id)
        for nodeid, ineq in dd.items():
            writestr += '\t{}:\n\t\t{}\n\t\t{}'.format(nodeid, ineq[0], ineq[1])
        writestr += '\n--------------------------------\n'
    open('troundineqs.txt', 'w').write(writestr)


def analyze(blockinfo: dict, init: StateSet, dataclass, cfg: CFG, dbg=False):
    Trounds: list[dict[int, NodeInfer]]
    Trounds = []
    round_ineqs: dict[int, dict[int, tuple[StateSet]]] = dict()
    init_TI = dict()
    blocks = deepcopy(list(blockinfo.keys()))
    for b in blocks:
        ni = NodeInfer(StateSet(), '')
        ni.out_as = deepcopy(init)
        init_TI[b] = deepcopy(ni)
    Trounds.append(init_TI)
    current_round = 1
    while True:
        prev_TI = Trounds[current_round-1]
        current_TI = dict()
        for b in blocks:
            parent_ids = blockinfo[b]['parents']
            nodecode = blockinfo[b]['statements'][0]
            # nodesrc = '\ncode:\n```\n' + tosrc(nodecode).strip() + '\n```\n'
            nodesrc = '\ncode:\n```\n' + astor.to_source(nodecode).strip() + '\n```\n'
            print(nodesrc)
            #
            auxcnt = 0
            for p in parent_ids:
                # print('as{} = {}'.format(str(auxcnt), str(prev_TI[p].out_as).strip()))
                auxcnt = auxcnt + 1
            # print('\n')
            #
            if len(parent_ids) > 0:
                _in = prev_TI[parent_ids[0]].out_as
                for p in parent_ids:
                    # print(_out[p])
                    with open('merges.txt', 'a') as f:
                        f.write(f'merging {_in} with {prev_TI[p].out_as}\n')
                        _in = dataclass.merge(_in, prev_TI[p].out_as)
                        f.write(f'result is {_in}\n\n')
            else:
                _in = init
            current_TI[b] = NodeInfer(_in, nodesrc)
            try:
                newout = dataclass.transfer(nodecode, _in)
                newout = newout.remove_no_names()
            except RuntimeError as rerr:
                dump_trounds(Trounds)
                dump_roundineqs(round_ineqs)
                raise rerr
            current_TI[b].in_as = _in
            current_TI[b].out_as = deepcopy(newout)
        Trounds.append(current_TI)
        stabilized = True
        round_ineqs[current_round] = dict()
        for b, b_tas in current_TI.items():
            if b_tas.out_as != prev_TI[b].out_as:
                round_ineqs[current_round][b] = (b_tas.out_as, prev_TI[b].out_as)
                stabilized = False
                break
        if stabilized:
            break
        if current_round == MAXROUNDS:
            dump_trounds(Trounds)
            dump_roundineqs(round_ineqs)
            raise RuntimeError('enough')
        current_round = current_round + 1
    dump_trounds(Trounds)
    return Trounds
