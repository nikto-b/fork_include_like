from lrec.remove_arbitary_lrec import remove_arb_left_recursuion
from model.grammar import CFG


def test_indirect():
    grammar = CFG.fromstring('''
    A -> S α
    S -> S β | A γ | β
    ''')

    target_grammar = CFG.fromstring('''
    A -> S α
    S -> β S′ | β
    S′ -> β S′ | α γ S′ | β | α γ
    ''')

    fixed_grammar = remove_arb_left_recursuion(grammar)

    assert len(fixed_grammar.productions) == len(target_grammar.productions)
    assert set(fixed_grammar.productions) == set(target_grammar.productions)
