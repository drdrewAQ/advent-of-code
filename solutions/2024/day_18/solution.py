# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/18

import re
from queue import Queue

from solutions.utils.grid import add_points
from ...base import StrSplitSolution, answer


FALL = 1024
DIRECTIONS = [ (1,0), (0, 1), (-1, 0), (0, -1) ]

class XYGrid:
    w: int
    h: int
    solution: list[tuple[int,int]] = []

    def __init__(self, w: int, h:int, to_omit: list[tuple[int,int]] = []):
        self.w = w
        self.h = h
        self.grid = {}
        for y in range(h+1):
            for x in range(w+1):
                if (x,y) in to_omit:
                    continue
                self.grid[x,y] = 1

    def path(self):
        if self.solution:
            return self.solution
        queue = Queue()
        visited = set()
        start = (0, 0)
        end = (self.w, self.h)
        queue.put((start, [start]))
        while not queue.empty():
            current, history = queue.get()
            for d in DIRECTIONS:
                step = add_points(current, d)
                if step not in self.grid:
                    continue
                if step in visited or step in history:
                    continue
                if step == end:
                    self.solution = history
                    return history
                queue.put((step, history + [step]))
                visited.add(step)
        return

    def remove(self, x:int, y:int):
        del self.grid[x,y]
        if (x,y) in self.solution:
            self.solution = []
            return self.path()
        else:
            return self.solution

class Solution(StrSplitSolution):
    _year = 2024
    _day = 18

    @answer(324)
    def part_1(self) -> int:
        # parse input
        coords = re.compile(r'(\d+),(\d+)')
        bytes = []
        w, h = 0, 0
        for line in self.input:
            x, y = map(int, re.match(coords, line).groups())
            if x > w:
                w = x
            if y > h:
                h = y
            bytes.append((x,y))

        # stash input list for part 2
        self.bytes = bytes

        fallen = bytes[:FALL]

        # stash grid for part 2
        self.grid = XYGrid(w, h, fallen)
        return len(self.grid.path())



    @answer((46,23))
    def part_2(self) -> tuple[int,int]:
        to_fall = self.bytes[FALL:]
        for (x,y) in to_fall:
            if self.grid.remove(x,y) is None:
                return x,y

        return 0,0


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
