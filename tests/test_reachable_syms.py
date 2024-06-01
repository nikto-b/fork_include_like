# from nltk import CFG, Nonterminal
from model.grammar import CFG
from model.nterm import Nonterminal
from reduce_grammar.reachable_syms import find_reachable_symbols, filter_unreachable_symbols


def test_find_reachable():
    grammar = CFG.fromstring('''
    S -> A B | C D
    A -> E F
    G -> A D
    C -> c
    ''')

    target_syms = {
        Nonterminal('S'),
        Nonterminal('A'),
        Nonterminal('B'),
        Nonterminal('C'),
        Nonterminal('D'),
        Nonterminal('E'),
        Nonterminal('F'),
        'c'
    }

    got_syms = find_reachable_symbols(grammar)

    assert target_syms == got_syms


def test_filter_unreachable():
    grammar = CFG.fromstring('''
    S -> A B | C D
    A -> E F
    G -> A D
    C -> c
    ''')

    target_grammar = CFG.fromstring('''
    S -> A B | C D
    A -> E F
    C -> c
    ''')

    filtered = filter_unreachable_symbols(grammar)

    assert len(target_grammar.productions) == len(filtered.productions)
    assert set(target_grammar.productions) == set(filtered.productions)
