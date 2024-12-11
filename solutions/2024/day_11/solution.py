# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/11

from collections import Counter
from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2024
    _day = 11
    separator = ' '

    # LOL
    def blink(self, stones):
        i = 0
        while i < len(stones):
            stone = stones[i]
            if stone == '0':
                stones[i] = '1'
            elif (length := len(stone)) % 2 == 0:
                left = stone[:length//2]
                stones.insert(i, left)
                i += 1
                right = f'{int(stone[length//2:])}'
                stones[i] = right
            else:
                stones[i] = f'{2024*int(stone)}'
            i += 1
                
    # "order is preserved" is a red herring
    def blink_once(self, stones):
        new_round = Counter()
        for n, count in stones.items():
            if n == '0':
                new_round['1'] += count
            elif (i := len(n)) % 2 == 0:
                left = n[:i//2]
                new_round[left] += count
                right = f'{int(n[i//2:])}'
                new_round[right] += count
            else:
                new_round[f'{2024*int(n)}'] += count 
        return new_round


    @answer(183435)
    def part_1(self) -> int:
        stones = Counter(self.input)
        for _ in range(25):
            stones = self.blink_once(stones)
        return stones.total()


    @answer(218279375708592)
    def part_2(self) -> int:
        stones = Counter(self.input)
        for _ in range(75):
            stones = self.blink_once(stones)
        return stones.total()

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
