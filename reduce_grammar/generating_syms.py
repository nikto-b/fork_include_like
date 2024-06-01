import logging
from typing import Union

from model.grammar import CFG
from model.nterm import Nonterminal, SYMBOL


def find_generating_syms(grammar: CFG) -> set[SYMBOL]:
    ret = set()

    productions = grammar.productions

    for p in productions:
        if not any(map(lambda x: isinstance(x, Nonterminal), p.rhs)):
            ret.add(p.lhs)

    prev_ret = set()
    while prev_ret != ret:
        prev_ret = ret
        for p in productions:
            if all(map(lambda x: isinstance(x, str) or x in ret, p.rhs)):
                ret.add(p.lhs)

    return ret


def filter_nongenerating_nterms(grammar: CFG) -> CFG:
    generating_syms = find_generating_syms(grammar)
    ret = []
    for p in grammar.productions:
        if all(map(lambda x: isinstance(x, str) or x in generating_syms, p.rhs)):
            ret.append(p)
        else:
            print(f'Filtered out production {p} (not generating anything)')

    return grammar.copy_with(productions=ret)
