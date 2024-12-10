# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/10

from collections import Counter
from ...base import IntGridSolution, answer


class Solution(IntGridSolution):
    _year = 2024
    _day = 10

    # path is just for debugging, returns counter keyed by summits with rating values
    def look_around(self, location, path):
        i = location[0]
        j = location[1]
        c = self.input[i][j]
        if c == 9:
            # self.debug(path)
            return Counter({location: 1})

        h = len(self.input) - 1
        w = len(self.input[0]) - 1
        ratings = Counter()
        for delta_i, delta_j in [[0,1],[1,0],[0,-1],[-1,0]]:
            # don't leave the map, natch
            next_i = i + delta_i
            if next_i < 0 or next_i > h:
                continue

            next_j = j + delta_j
            if next_j < 0 or next_j > w:
                continue

            # see if we can keep climbing
            step = tuple([next_i, next_j])
            if self.input[next_i][next_j] == c+1:
                fork = path.copy()
                fork.append(step)
                summits = self.look_around(step, fork)
                ratings.update(summits)

        return ratings

    @answer(717)
    def part_1(self) -> int:
        trailheads = set()
        # find trailheads
        for i, row in enumerate(self.input):
            for j, c in enumerate(row):
                if c == 0:
                    trailheads.add(tuple([i,j]))
        self.debug(len(trailheads), trailheads)
        
        total_score = 0
        for head in sorted(trailheads):
            path = [head]
            summits = self.look_around(head, path)
            total_score += len(summits.keys())
            self.debug(head, summits)

        return total_score

    @answer(1686)
    def part_2(self) -> int:
        trailheads = set()
        # find trailheads
        for i, row in enumerate(self.input):
            for j, c in enumerate(row):
                if c == 0:
                    trailheads.add(tuple([i,j]))
        self.debug(len(trailheads), trailheads)
        
        total_score = 0
        for head in sorted(trailheads):
            path = [head]
            summits = self.look_around(head, path)
            total_score += summits.total()
            self.debug(head, summits)

        return total_score

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass 
