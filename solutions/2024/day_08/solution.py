# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/8

from ...base import GridSolution, answer
from ...utils.grid import add_points, subtract_points


class Solution(GridSolution):
    _year = 2024
    _day = 8

    @answer(247)
    def part_1(self) -> int:
        antennas = {}
        antinodes = set()
        for loc, c in self.input.items():
            if c != '.':
                antennas.setdefault(c, set()).add(loc)

        for nodes in antennas.values():
            node1 = nodes.pop()
            while nodes:
                for node2 in nodes:
                    delta = subtract_points(node2, node1)
                    assert(delta[0] != 0 or delta[1] != 0)

                    for anti in subtract_points(node1, delta), add_points(node2, delta):
                        if anti in self.input:
                            antinodes.add(anti)
                    
                node1 = nodes.pop()
        return len(antinodes)


    @answer(861)
    def part_2(self) -> int:
        antennas = {}
        antinodes = set()
        for loc, c in self.input.items():
            if c != '.':
                antennas.setdefault(c, set()).add(loc)

        for nodes in antennas.values():
            node1 = nodes.pop()
            while nodes:
                for node2 in nodes:
                    delta = subtract_points(node2, node1)
                    assert(delta[0] != 0 or delta[1] != 0)

                    for anti, fn in (node2, add_points), (node1, subtract_points):
                        antinodes.add(anti)
                        while (next_anti := fn(anti, delta)) in self.input:
                            antinodes.add(next_anti)
                            anti = next_anti

                node1 = nodes.pop()

        return len(antinodes)


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass 
