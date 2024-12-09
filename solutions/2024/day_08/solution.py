# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/8

from ...base import GridSolution, answer


class Solution(GridSolution):
    _year = 2024
    _day = 8

    @answer(247)
    def part_1(self) -> int:
        h = len(self.input) - 1
        w = len(self.input[0]) - 1

        antennas = {}
        antinodes = set()
        for i, r in enumerate(self.input):
            for j, c in enumerate(r):
                if c != '.':
                    antennas.setdefault(c, set()).add(tuple([i,j]))

        for nodes in antennas.values():
            node1 = nodes.pop()
            while nodes:
                for node2 in nodes:
                    i_1 = node1[0]
                    j_1 = node1[1]
                    i_2 = node2[0]
                    j_2 = node2[1]
                    delta_i = i_2 - i_1
                    delta_j = j_2 - j_1
                    assert(delta_i != 0 or delta_j != 0)

                    # check 'below' node1
                    anti_i = i_1 - delta_i
                    anti_j = j_1 - delta_j
                    if not (anti_i < 0 or anti_j < 0 or anti_i > h or anti_j > w):
                        antinodes.add(f'{anti_i},{anti_j}')
                    
                    # check 'above' node2
                    anti_i = i_2 + delta_i
                    anti_j = j_2 + delta_j
                    if not (anti_i < 0 or anti_j < 0 or anti_i > h or anti_j > w):
                        antinodes.add(f'{anti_i},{anti_j}')
                node1 = nodes.pop()
        return len(antinodes)


    @answer(861)
    def part_2(self) -> int:
        h = len(self.input) - 1
        w = len(self.input[0]) - 1
        antennas = {}
        antinodes = set()
        for i, r in enumerate(self.input):
            for j, c in enumerate(r):
                if c != '.':
                    antennas.setdefault(c, set()).add(tuple([i,j]))

        for nodes in antennas.values():
            node1 = nodes.pop()
            # only if there are at least two nodes of the same frequency
            if nodes:
                antinodes.add(f'{node1[0]},{node1[1]}')
            while nodes:
                for node2 in nodes:
                    i_1 = node1[0]
                    j_1 = node1[1]
                    i_2 = node2[0]
                    j_2 = node2[1]
                    delta_i = i_2 - i_1
                    delta_j = j_2 - j_1
                    assert(delta_i != 0 or delta_j != 0)

                    # check 'below' node1
                    anti_i = i_1 - delta_i
                    anti_j = j_1 - delta_j
                    while not (anti_i < 0 or anti_j < 0 or anti_i > h or anti_j > w):
                        antinodes.add(f'{anti_i},{anti_j}')
                        anti_i -= delta_i
                        anti_j -= delta_j
                    
                    # check 'above' node2
                    anti_i = i_2 + delta_i
                    anti_j = j_2 + delta_j
                    while not (anti_i < 0 or anti_j < 0 or anti_i > h or anti_j > w):
                        antinodes.add(f'{anti_i},{anti_j}')
                        anti_i += delta_i
                        anti_j += delta_j
                node1 = nodes.pop()
                antinodes.add(f'{node1[0]},{node1[1]}')

        return len(antinodes)


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass 
