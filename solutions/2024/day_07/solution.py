# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/7

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2024
    _day = 7

    @answer(4122618559853)
    def part_1(self) -> int:
        sum = 0
        for string in self.input:
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
                else:
                    prev_outputs = [k for k in outputs.keys() if len(k) == i]
                    for po in prev_outputs:
                        outputs[f'{po}+'] = outputs[po] + v
                        outputs[f'{po}*'] = outputs[po] * v

            final_outputs = {k: outputs[k] for k in outputs.keys() if len(k) == len(values)}
            if result in final_outputs.values():
                sum += result
        return sum



    # @answer(1234)
    def part_2(self) -> int:
        sum = 0
        for string in self.input:
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
                    outputs['c'] = int(f'{init}{v}')
                else:
                    prev_outputs = [k for k in outputs.keys() if len(k) == i]
                    for po in prev_outputs:
                        outputs[f'{po}+'] = outputs[po] + v
                        outputs[f'{po}*'] = outputs[po] * v
                        outputs[f'{po}c'] = int(f'{outputs[po]}{v}')

            final_outputs = {k: outputs[k] for k in outputs.keys() if len(k) == len(values)}
            if result in final_outputs.values():
                sum += result
        return sum


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
