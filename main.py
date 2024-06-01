import logging

from reduce_grammar.generalize import generalize_grammar

logging.basicConfig(level=logging.DEBUG)

from lrec.remove_arbitary_lrec import remove_arb_left_recursuion
from model.grammar import CFG

from util import print_grammar


def input_grammar() -> str:
    print('Pass grammar. End with `EOF`')
    grammar_string = ''
    while (line := input()) != 'EOF':
        grammar_string += line + '\n'
    if len(grammar_string) == 0:
        # Вариант 5 - преобразование к приведенной грамматике
        return '''
                S -> A | B
                A -> C | D
                B -> D | E
                C -> S | a | ε
                D -> S | b
                E -> S | c | ε
                '''
    return grammar_string


def main():
    grammar = CFG.fromstring(input_grammar())
    print('Input: ')
    print_grammar(grammar, '\t')

    no_lrec = remove_arb_left_recursuion(grammar)
    print(f'Removed left recursion:')
    print_grammar(no_lrec, '\t')

    g = generalize_grammar(grammar)

    print('\nOutput: ')
    print_grammar(g, '\t')


if __name__ == '__main__':
    main()
