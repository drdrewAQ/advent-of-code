# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/3

from ...base import TextSolution, answer


class Solution(TextSolution):
    _year = 2024
    _day = 3

    @answer(174336360)
    def part_1(self) -> int:
        import re
        sum = 0
        mul = re.compile(r'mul\((\d+),(\d+)\)')
        for m in re.finditer(mul, self.input):
            sum += int(m.group(1)) * int(m.group(2))
        return sum


    @answer(88802350)
    def part_2(self) -> int:
        import re
        sum = 0
        mul = re.compile(r'mul\((\d+),(\d+)\)')
        do  = re.compile(r'do\(\)')
        no  = re.compile(r"don't\(\)")

        chunks = re.split(no, self.input)
        for m in re.finditer(mul, chunks.pop(0)):
            sum += int(m.group(1)) * int(m.group(2))

        for c in chunks:
            toggle = re.split(do, c, maxsplit=1)
            if len(toggle) == 1:
                continue

            for m in re.finditer(mul, toggle[1]):
                sum += int(m.group(1)) * int(m.group(2))

        return sum


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
