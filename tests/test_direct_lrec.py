# from nltk import CFG, Nonterminal

from lrec.remove_direct_lrec import remove_direct_left_recursion
from model.grammar import CFG
from model.nterm import Nonterminal


def test_basic_direct():
    grammar = CFG.fromstring('''
    A -> S a | A a
    S -> A b
    ''')

    target_grammar = CFG.fromstring('''
    A -> S a A′ | S a
    A′ -> a A′ | a
    S -> A b
    ''')
    target_productions = target_grammar.productions
    filtered_out = remove_direct_left_recursion(grammar.productions, Nonterminal('A'))

    assert len(filtered_out) == len(target_productions)
    for production in filtered_out:
        assert production in target_productions
