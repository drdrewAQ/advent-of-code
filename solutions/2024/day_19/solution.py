# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/19

import re
from collections import Counter
from ...base import StrSplitSolution, answer

class Solution(StrSplitSolution):
    _year = 2024
    _day = 19

    success = []

    @answer(216)
    def part_1(self) -> int:
        available = [pattern for pattern in self.input[0].split(', ')]
        regex = r'^(:?' + '|'.join(available) + ')+$'        
        for sequence in self.input[2:]:
            if re.match(regex, sequence):
                self.success.append(sequence)
        return len(self.success)


    @answer(603191454138773)
    def part_2(self) -> int:
        available = [pattern for pattern in self.input[0].split(', ')]
        available.sort(key=len, reverse=True)

        total = 0
        for sequence in self.success:
            self.debug(f'*** {sequence} ***')
            tails = Counter()
            for i in range(len(sequence)):
                tails[sequence[i:]] = 0
            tails[sequence] = 1
            tails[''] = 0
            for i in range(len(sequence)):
                pre = sequence[:i]
                post = sequence[i:] # if i+1 < len(sequence) else ''
                self.debug(f'!!! {pre} | {post}')
                precount = tails[post]
                if precount == 0:
                    continue
                for pattern in available:
                    if post.startswith(pattern):
                        posttail = post[len(pattern):]
                        tails[posttail] += precount 

            self.debug(f'{sequence}: {tails[""]}')
            total += tails['']
        return total


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
