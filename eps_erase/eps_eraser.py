from typing import Union

from model.grammar import CFG
from model.nterm import Nonterminal, EPSYLON_SYMBOL, SYMBOL
from model.production import Production
# from nltk import Production, Nonterminal
# from nltk.grammar import CFG

from util import add_postfix


def is_term_eps(sym: SYMBOL) -> bool:
    return sym in {Nonterminal('EPS'), Nonterminal('ε'), EPSYLON_SYMBOL}


def is_eps_production(production: Production) -> bool:
    return len(production.rhs) == 1 and is_term_eps(production.rhs[0])


def is_eps_based_production(production: Production, eps_gen_terms: set[Nonterminal]) -> bool:
    if any(map(lambda x: isinstance(x, str), production.rhs)):
        # Если в правиле стоит нетерминал - оно не может быть сведено к eps-правилу
        return False

    for r in production.rhs:
        if r not in eps_gen_terms:
            # Проверяем каждый элемент, если его нет в правилах сведённых к eps -> итог не сведется к eps
            return False

    return True


def find_direct_eps_terms(in_grammar: CFG) -> set[Nonterminal]:
    eps_generating_terms = set()
    for production in in_grammar.productions:
        if is_eps_production(production):
            eps_generating_terms.add(production.lhs)

    return eps_generating_terms


def find_eps_rules(in_grammar: CFG) -> set[Nonterminal]:
    eps_generating_terms = find_direct_eps_terms(in_grammar)

    prev_gen_len = 0
    while len(eps_generating_terms) != prev_gen_len:
        prev_gen_len = len(eps_generating_terms)

        for production in in_grammar.productions:
            if is_eps_based_production(production, eps_generating_terms):
                eps_generating_terms.add(production.lhs)

    return eps_generating_terms


def eps_closure(rhs: list[Union[str, Nonterminal]], eps_terms: set[Nonterminal]) -> list[list[Union[str, Nonterminal]]]:
    if len(rhs) == 0:
        return [[]]

    ret = []

    for tail in eps_closure(rhs[1:], eps_terms):
        ret.append([rhs[0]] + tail)
        if rhs[0] in eps_terms:
            ret.append(tail)
    return ret


def is_start_eps(start_sym: Nonterminal, productions: list[Production]) -> bool:
    for p in productions:
        if p.lhs == start_sym:
            if is_eps_production(p):
                return True
    return False


def wrap_start_eps(start_sym: Nonterminal, productions: list[Production]) -> CFG:
    old_start_sym: Nonterminal = start_sym
    new_start_sym = add_postfix(old_start_sym, productions, '′')
    return CFG(new_start_sym, productions + [Production(new_start_sym, (old_start_sym,)),
                                             Production(new_start_sym, (Nonterminal('ε'),)), ])


def filter_eps_rules(in_grammar: CFG) -> CFG:
    out_productions = []
    start_sym = in_grammar.start

    # Находим все нетерминалы, ведущие к ε
    eps_gen_terms = find_eps_rules(in_grammar)

    for in_production in in_grammar.productions:
        # Для каждого правила готовим замыкание с нетерминалами, ведущими к ε
        lterm = in_production.lhs
        productions = eps_closure(list(in_production.rhs), eps_gen_terms)
        for prod in productions:
            if len(prod) == 0:
                continue
            out_productions.append(Production(lterm, tuple(prod)))

    # Удаляем из правил ε-правила
    out_productions = list(filter(lambda x: not is_eps_production(x), out_productions))

    # Проверяем выводилось ли ε напрямую из оригинальной грамматики
    if is_start_eps(start_sym, in_grammar.productions):
        return wrap_start_eps(start_sym, out_productions)

    return CFG(start_sym, out_productions)
