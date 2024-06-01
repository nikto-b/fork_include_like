# from nltk.grammar import CFG, Nonterminal, Production

from eps_erase.eps_eraser import filter_eps_rules, is_term_eps, is_eps_production
from model.grammar import CFG
from model.nterm import Nonterminal, EPSYLON_SYMBOL
from model.production import Production


def test_search_eps_sym():
    eps_syms = [
        Nonterminal('ε'),
        Nonterminal('EPS')
    ]

    for eps in eps_syms:
        assert is_term_eps(eps)


def test_search_eps_production():
    eps_productions = [
        Production(Nonterminal('ASDF'), (EPSYLON_SYMBOL,)),
        Production(Nonterminal('ASasDF'), (Nonterminal('ε'),)),
        Production(Nonterminal('ASDFdsad'), (Nonterminal('EPS'),)),
    ]

    for p in eps_productions:
        assert is_eps_production(p)


def test_erase():
    grammar = CFG.fromstring('''
    S -> A B C d
    A -> a | ε
    B -> A C
    C -> c | ε
    ''')

    target_grammar = CFG.fromstring('''
    S -> A d | A B d | A C d | A B C d | B d | B C d | C d | d
    A -> a
    B -> A | A C | C
    C -> c
    ''')
    target_productions = target_grammar.productions

    filtered_out = filter_eps_rules(grammar)

    assert len(filtered_out.productions) == len(target_productions)
    for production in filtered_out.productions:
        assert production in target_productions


def test_out_eps():
    grammar = CFG.fromstring('''
    S -> A B C d | ε
    A -> a | ε
    B -> A C
    C -> c | ε
    ''')

    target_grammar = CFG.fromstring('''
    S′ -> S | ε
    S -> A d | A B d | A C d | A B C d | B d | B C d | C d | d
    A -> a
    B -> A | A C | C
    C -> c
    ''')
    target_productions = target_grammar.productions

    filtered_out = filter_eps_rules(grammar)

    assert len(filtered_out.productions) == len(target_productions)
    for production in filtered_out.productions:
        assert production in target_productions


def test_start_eps():
    grammar = CFG.fromstring('''
    S -> ε
    ''')

    target_grammar = CFG.fromstring('''
    S′ -> S | ε
    ''')
    target_productions = target_grammar.productions
    filtered_out = filter_eps_rules(grammar)

    assert len(filtered_out.productions) == len(target_productions)
    for production in filtered_out.productions:
        assert production in target_productions
