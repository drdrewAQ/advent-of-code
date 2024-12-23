# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/23

from itertools import combinations
from ...base import StrSplitSolution, answer


def bron_kerbosch(R, P, X, graph):
    if not P and not X:
        yield R
    while P:
        v = P.pop()
        yield from bron_kerbosch(
            R.union({v}),
            P.intersection(graph[v]),
            X.intersection(graph[v]),
            graph
        )
        X.add(v)


class Solution(StrSplitSolution):
    _year = 2024
    _day = 23

    @answer(1218)
    def part_1(self) -> int:
        # v = set()
        conn = {}
        triads = set()
        count = 0
        for cx in self.input:
            c1, c2 = cx.split('-')
            # v.update([c1, c2])
            conn.setdefault(c1, set()).add(c2)
            conn.setdefault(c2, set()).add(c1)
        for c, linked in conn.items():
            if len(linked) == 1:
                continue
            for c1, c2 in combinations(linked, 2):
                if c1 in conn and c2 in conn[c1]:
                    triads.add(tuple(sorted([c,c1,c2])))
                    if c.startswith('t') or c1.startswith('t') or c2.startswith('t'):
                        # appearing with all three in the triad...
                        # self.debug(f'triad: {c}, {c1}, {c2}')
                        count += 1
        # self.v = v
        self.conn = conn
        # self.triads = triads
        return count // 3


    @answer('ah,ap,ek,fj,fr,jt,ka,ln,me,mp,qa,ql,zg')
    def part_2(self) -> str:
        all_cliques = list(bron_kerbosch(set(), set(self.conn.keys()), set(), self.conn))
        return ','.join(sorted(sorted(all_cliques, key=len, reverse=True)[0]))

        # # original naive
        # candidates = self.triads
        # while candidates:
        #     previous = candidates
        #     candidates = set()
        #     for complete in previous:
        #         for v in self.v:
        #             if v in complete:
        #                 continue
        #             include = True
        #             group = []
        #             for c in complete:
        #                 if v not in self.conn[c]:
        #                     include = False
        #                     break
        #                 group.append(c)
        #             if include:
        #                 group.append(v)
        #                 self.debug(f'extending {complete} to {group}')
        #                 candidates.add(tuple(sorted(group)))
        # return ','.join(previous.pop())


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
