# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/10

from collections import Counter

from solutions.utils.grid import add_points
from ...base import IntGridSolution, answer


class Solution(IntGridSolution):
    _year = 2024
    _day = 10

    # path is just for debugging, returns counter keyed by summits with rating values
    def look_around(self, location, path):
        elevation = self.input[location]
        if elevation == 9:
            # self.debug(path)
            return Counter({location: 1})

        ratings = Counter()
        for direction in tuple([0,1]), tuple([1,0]), tuple([0,-1]), tuple([-1,0]):
            # see if we can keep climbing
            step = add_points(location, direction)
            # don't leave the map, natch
            if step in self.input and self.input[step] == elevation + 1:
                fork = path.copy()
                fork.append(step)
                summits = self.look_around(step, fork)
                ratings.update(summits)

        return ratings

    @answer(717)
    def part_1(self) -> int:
        trailheads = set()
        # find trailheads
        for loc, elevation in self.input.items():
            if elevation == 0:
                trailheads.add(loc)
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
        for loc, elevation in self.input.items():
            if elevation == 0:
                trailheads.add(loc)
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
