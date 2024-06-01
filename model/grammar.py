from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from model.nterm import Nonterminal, EPSYLON_SYMBOL
from model.production import Production


@dataclass(frozen=True)
class CFG:
    _start: Nonterminal
    _productions: list[Production]

    @property
    def start(self) -> Nonterminal:
        return self._start

    @property
    def productions(self) -> list[Production]:
        return self._productions.copy()

    @classmethod
    def fromstring(cls, s: str, start: Optional[Nonterminal] = None) -> CFG:
        productions = list()
        start = None
        for line in s.split('\n'):
            line = line.strip()
            if len(line) == 0:
                continue

            p_s = Production.from_string(line)
            if start is None:
                start = p_s[0].lhs
            for p in p_s:
                productions.append(p)

        if start is None:
            start = Nonterminal('S')
            productions = {Production(start, (EPSYLON_SYMBOL,))}

        return CFG(start, productions)

    @property
    def nterms(self) -> set[Nonterminal]:
        ret = set()

        for p in self._productions:
            ret.add(p.lhs)
            ret |= set(p.rhs)

        return ret

    def copy_with(self,
                  start: Optional[Nonterminal] = None,
                  productions: Optional[list[Production]] = None) -> CFG:

        return CFG(start or self.start, productions or self.productions)

    def __eq__(self, __value: CFG):
        return self._start == __value._start \
            and len(self._productions) == len(__value._productions) \
            and set(self._productions) == set(__value._productions)
