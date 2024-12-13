# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/13

import re
from ...base import TextSolution, answer


class Solution(TextSolution):
    _year = 2024
    _day = 13

    @answer(28887)
    def part_1(self) -> int:
        total = 0
        # 'Button A: X+94, Y+34\nButton B: X+22, Y+67\nPrize: X=8400, Y=5400'
        regex = re.compile(r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)')
        for machine in self.input.split("\n\n"):
            self.debug(machine)
            if m:= re.match(regex, machine):
                ax, ay, bx, by, prize_x, prize_y = map(int, m.groups())
            else:
                ValueError(f'Regex failed on this machine: {machine}')
            
            det = ax * by - ay * bx
            a = (by * prize_x - bx * prize_y) // det
            b = (ax * prize_y - ay * prize_x) // det

            self.debug([a,b], det)
            if a * ax + b * bx == prize_x and a * ay + b * by == prize_y:
                total += (3 * a + b)
            continue

        return total


    @answer(96979582619758)
    def part_2(self) -> int:
        total = 0
        regex = re.compile(r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)')
        for machine in self.input.split("\n\n"):
            if m:= re.match(regex, machine):
                ax, ay, bx, by, prize_x, prize_y = map(int, m.groups())
            else:
                ValueError(f'Regex failed on this machine: {machine}')

            prize_x += 10000000000000
            prize_y += 10000000000000

            det = ax * by - ay * bx
            a = (by * prize_x - bx * prize_y) // det
            b = (ax * prize_y - ay * prize_x) // det

            self.debug([a,b], det)
            if a * ax + b * bx == prize_x and a * ay + b * by == prize_y:
                total += (3 * a + b)
            continue
        return total


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
