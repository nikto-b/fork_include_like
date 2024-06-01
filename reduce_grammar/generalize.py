import logging

from eps_erase.eps_eraser import filter_eps_rules
from model.grammar import CFG
from reduce_grammar.generating_syms import filter_nongenerating_nterms
from reduce_grammar.reachable_syms import filter_unreachable_symbols
from util import repr_grammar


def generalize_grammar(grammar: CFG) -> CFG:
    grammar = filter_eps_rules(grammar)
    logging.debug('Removed ε-rules')
    logging.debug(repr_grammar(grammar, arrow_sep=' -> '))
    grammar = filter_nongenerating_nterms(grammar)
    logging.debug('Removed nongenerating nonterminals')
    logging.debug(repr_grammar(grammar, arrow_sep=' -> '))
    grammar = filter_unreachable_symbols(grammar)
    logging.debug('Removed unreachable symbols')
    logging.debug(repr_grammar(grammar, arrow_sep=' -> '))
    return grammar
