import logging
from typing import Iterable

from model.nterm import Nonterminal
from model.production import Production
# from nltk import CFG, Nonterminal, Production

from util import add_postfix


def remove_direct_left_recursion(productions: Iterable[Production], nterm: Nonterminal) -> list[Production]:

    new_productions = list()

    new_nterm = add_postfix(nterm, productions, '′')
    has_recursion = False

    for p in productions:
        if p.lhs != nterm:
            new_productions.append(p)
        else:
            if p.rhs[0] == nterm:
                if not has_recursion:
                    logging.debug(f'Removing direct recursion of nterm {nterm}')
                has_recursion = True
                new = Production(new_nterm, p.rhs[1:] + (new_nterm,))
                logging.debug(f'Adding production {new}')
                new_productions.append(new)
                new = Production(new_nterm, p.rhs[1:])
                logging.debug(f'Adding production {new}')
                new_productions.append(new)
            else:
                new_productions.append(p)
                new = Production(nterm, p.rhs + (new_nterm,))
                new_productions.append(new)

    if has_recursion:
        return new_productions
    else:
        return list(productions)
