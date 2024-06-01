from model.grammar import CFG
from model.nterm import Nonterminal
from reduce_grammar.generating_syms import find_generating_syms, filter_nongenerating_nterms


def test_find_generating():
    g = CFG.fromstring('''
    S -> A c
    A -> S D
    D -> a D
    A -> a
    ''')

    generating = find_generating_syms(g)

    assert generating == {
        Nonterminal('S'),
        Nonterminal('A'),
    }


def test_filter_nongenerating():
    g = CFG.fromstring('''
    S -> A c
    A -> S D
    D -> a D
    A -> a
    ''')

    target_grammar = CFG.fromstring('''
    S -> A c
    A -> a
    ''')

    filtered = filter_nongenerating_nterms(g)
    assert len(filtered.productions) == len(target_grammar.productions)
    assert set(filtered.productions) == set(target_grammar.productions)
