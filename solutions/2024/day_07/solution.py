# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/7

from functools import partial
from multiprocessing import Pool
from ...base import StrSplitSolution, answer

def process_string(string, concat: bool = False):
    result, values = string.split(': ')
    result = int(result)
    values = values.split(' ')
    init = int(values.pop(0))
    outputs = {}
    for i, v in enumerate(values):
        v = int(v)
        if i == 0:
            outputs['+'] = init + v
            outputs['*'] = init * v
            if concat:
                outputs['c'] = int(f'{init}{v}')

        else:
            prev_outputs = [k for k in outputs.keys() if len(k) == i]
            for po in prev_outputs:
                if outputs[po] + v <= result:
                    outputs[f'{po}+'] = outputs[po] + v
                if outputs[po] * v <= result:
                    outputs[f'{po}*'] = outputs[po] * v
                c = int(f'{outputs[po]}{v}')
                if concat and c <= result:
                    outputs[f'{po}c'] = c

    final_outputs = [outputs[k] for k in outputs.keys() if len(k) == len(values)]
    return result if result in final_outputs else 0

class Solution(StrSplitSolution):
    _year = 2024
    _day = 7

    @answer(4122618559853)
    def part_1(self) -> int:
        with Pool() as pool:
            return sum(pool.map(process_string, self.input))


    @answer(227615740238334)
    def part_2(self) -> int:
        with Pool() as pool:
            return sum(pool.map(partial(process_string, concat=True), self.input))

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
