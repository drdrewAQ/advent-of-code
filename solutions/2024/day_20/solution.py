# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/20

from collections import Counter
from solutions.utils.grid import add_points, taxi_distance
from ...base import GridSolution, answer

# GridSolution is in i,j format
DIRECTIONS = { (1,0): 'v', (0, 1): '>', (-1, 0): '^', (0, -1): '<' }
CHEATS = [ (2,0), (1,1), (0,2), (-1,1), (-2,0), (-1,-1), (0,-2), (1,-1) ]

# BIGCHEATS = []
# for raw_i in range(41):
#     for raw_j in range(41):
#         i = raw_i - 20
#         j = raw_j - 20
#         if abs(i) + abs(j) < 21:
#             BIGCHEATS.append((i,j))

THRESHOLD = 100

class Solution(GridSolution):
    _year = 2024
    _day = 20

    @answer(1358)
    def part_1(self) -> int:
        self.start = [l for l, c in self.input.items() if c == 'S'][0]
        self.end = [l for l, c in self.input.items() if c == 'E'][0]
        self.debug(f'racing from {self.start} to {self.end}')

        current = self.start
        timing = Counter({current: 0})
        self.course = [current]
        count = 0
        while current != self.end:
            for c in CHEATS:
                jump = add_points(current, c)
                # only jump to places we know the timing of (backwards)
                if jump not in timing:
                    continue
                if timing[current] - timing[jump] - 2 < THRESHOLD:
                    continue
                count += 1

            for d in DIRECTIONS:
                future = add_points(current, d)
                # follow the path, don't go backwards
                if self.input[future] != '#' and future not in timing:
                    timing[future] = timing[current] + 1
                    self.course.append(future)
                    current = future
                    break
                ValueError('maze broke at {current}')

        for c in CHEATS:
            jump = add_points(current, c)
            if jump not in timing:
                continue
            if timing[current] - timing[jump] - 2 < THRESHOLD:
                continue
            count += 1

        self.debug(f'course length: {timing[self.end]} picoseconds')

        # save for next round:
        self.timing = timing
        return count


    @answer(1005856)
    def part_2(self) -> int:
        shortcuts = 0
        self.debug('round two: START!')
        for current in self.course:
            # faster than enumerate -- why?
            i = self.timing[current]
            if i < THRESHOLD:
                continue
            for jump in self.course[:i - THRESHOLD]:
                if (cost := taxi_distance(jump,current)) > 20:
                    continue
                if i - self.timing[jump] - cost < THRESHOLD:
                    continue
                shortcuts += 1

        return shortcuts
 
    # @answer((1234, 4567)) 
    # def solve(self) -> tuple[int, int]:
    #     pass
