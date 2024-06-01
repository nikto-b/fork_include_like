import logging
from typing import Union, Iterable

from model.grammar import CFG
from model.nterm import Nonterminal


# from nltk import CFG, Production, Nonterminal


def find_reachable_symbols(grammar: CFG) -> set[Union[str, Nonterminal]]:
    ret = {grammar.start}
    prev_ret = {}

    while ret != prev_ret:
        prev_ret = ret

        for p in grammar.productions:
            if p.lhs in ret:
                ret |= set(p.rhs)

    return ret


def filter_unreachable_symbols(grammar: CFG) -> CFG:
    reachable = find_reachable_symbols(grammar)

    new_prods = []
    for p in grammar.productions:
        if p.lhs in reachable:
            new_prods.append(p)
        else:
            print(f'Filtered out production {p} (unreachable)')

    return grammar.copy_with(productions=new_prods)
