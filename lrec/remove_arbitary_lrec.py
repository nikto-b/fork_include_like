import logging

# from nltk import CFG, Production

from lrec.remove_direct_lrec import remove_direct_left_recursion
from model.grammar import CFG
from model.production import Production
from util import all_nterms, productions_lhs


def remove_arb_left_recursuion(in_grammar: CFG) -> CFG:
    nterms = all_nterms(in_grammar)
    productions = in_grammar.productions

    for i, nterm_i in enumerate(nterms):
        logging.debug(f'Watching for a recursions for an {nterm_i}')
        for j in range(i):
            nterm_j = nterms[j]
            logging.debug(f'Watching for recursion {nterm_i} -> {nterm_j}')
            prods_i = productions_lhs(productions, nterm_i)
            prods_j = productions_lhs(productions, nterm_j)

            for p in prods_i:
                if p.rhs[0] == nterm_j:
                    productions.remove(p)
                    logging.debug(f'Lookup {nterm_i} -> {nterm_j}...')
                    for subproduction in prods_j:
                        new = Production(p.lhs, subproduction.rhs + p.rhs[1:])
                        logging.debug(f'\tAdding {new}')
                        productions.append(new)
                    logging.debug(f'Removing {p}')
        productions = remove_direct_left_recursion(productions, nterm_i)

    return CFG(in_grammar.start, productions)
