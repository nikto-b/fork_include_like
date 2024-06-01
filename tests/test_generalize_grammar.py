import logging

logging.basicConfig(level=logging.DEBUG)

from model.grammar import CFG
from reduce_grammar.generalize import generalize_grammar


def test_generalize():
    grammar = CFG.fromstring('''
    S -> A S | B S | s
    E -> E F | F F 
    A -> a 
    F -> f
    ''')

    target_grammar = CFG.fromstring('''
    S -> A S | s
    A -> a
    ''')

    generalized = generalize_grammar(grammar)
    assert len(target_grammar.productions) == len(generalized.productions)
    assert set(target_grammar.productions) == set(generalized.productions)


def test_generalize_book(caplog):
    caplog.set_level(logging.DEBUG)

    grammar = CFG.fromstring('''
    S -> A | B
    A -> C | D
    B -> D | E
    C -> S | a | ε
    D -> S | b
    E -> S | c | ε
    ''')

    target_grammar = CFG.fromstring('''
    S -> A | B
    A -> C | D
    B -> D | E
    C -> a
    D -> b
    E -> c
    ''')

    generalized = generalize_grammar(grammar)
    assert set(target_grammar.productions) == set(generalized.productions)
    assert len(target_grammar.productions) == len(generalized.productions)
