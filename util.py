from typing import Union, Optional, Callable, Iterable

from model.grammar import CFG
from model.nterm import Nonterminal
from model.production import Production


# from nltk import Nonterminal, CFG, Production


def all_nterms(grammar: Union[CFG, Iterable[Production]]) -> list[Nonterminal]:
    nterms = list()
    if isinstance(grammar, CFG):
        productions = grammar.productions
    else:
        productions = list(grammar)

    for p in productions:
        if p.lhs not in nterms:
            nterms.append(p.lhs)
        for r in p.rhs:
            if isinstance(r, Nonterminal) and r not in nterms:
                nterms.append(r)
    return nterms


def productions_lhs(grammar: Union[CFG, Iterable[Production]], nterm: Nonterminal,
                    filter_func: Optional[Callable] = None) -> set[Production]:
    ret = set()

    if isinstance(grammar, CFG):
        productions = grammar.productions
    else:
        productions = set(grammar)

    for p in productions:
        if p.lhs == nterm:
            ret.add(p)

    if filter_func is None:
        return ret
    return set(filter(filter_func, ret))


def add_postfix(nterm: Nonterminal, context: Union[CFG, Iterable[Production]], postfix: str = '′') -> Nonterminal:
    nterms = set(all_nterms(context))
    while (ret := Nonterminal(nterm.symbol + postfix)) in nterms:
        pass
    return ret


def repr_grammar(grammar: Union[CFG, Iterable[Production]],
                 prefix='',
                 postfix='',
                 end='\n',
                 arrow_sep='\t-> ',
                 eq_sep=' | ') -> str:
    nterms = set(all_nterms(grammar))
    ret = ''
    for nterm in nterms:
        productions = productions_lhs(grammar, nterm)
        if len(productions) == 0:
            continue

        ret += prefix + Production.repr_multiple(productions, arrow_sep, eq_sep) + postfix
        ret += end

    return ret


def print_grammar(grammar: Union[CFG, Iterable[Production]],
                  prefix='',
                  postfix='',
                  end='\n',
                  arrow_sep='\t-> ',
                  eq_sep=' | ') -> None:
    print(repr_grammar(grammar, prefix, postfix, end, arrow_sep, eq_sep))
