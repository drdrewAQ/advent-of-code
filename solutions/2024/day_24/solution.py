# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/24

import re
from itertools import combinations, product
from ...base import TextSolution, answer

class FruitMonitor:
    x: dict[str,int] = {}
    y: dict[str,int] = {}
    states: dict[str,int] = {}
    rules: dict[str,list[str]] = {}
    z: list[int] = []
    correct_sum: int
    current_sum: int

    def __init__(self, state: str, rule: str):
        state_re = re.compile(r'([xy]\d{2}): ([01])')
        for s in state.split('\n'):
            if (m := re.match(state_re, s)):
                wire, value = m.groups()
                self.states[wire] = int(value)
            else:
                ValueError(f'{s} did not have the proper format')
        rule_re = re.compile(r'(\w{3}) ([XORAND]{2,3}) (\w{3}) -> (\w{3})')
        for r in rule.split('\n'):
            if (m := re.match(rule_re, r)):
                s1, op, s2, result = m.groups()
                self.rules[result] = (s1, op, s2)
                if result.startswith('z'):
                    num = int(result[1:])
                    if num + 1 > len(self.z):
                        self.z = [-1]*(num+1)
            else:
                ValueError(f'{r} did not have the proper format')

        self.x = {x: v for x,v in self.states.items() if x.startswith('x')}
        self.y = {y: v for y,v in self.states.items() if y.startswith('y')}
        self.valid_add()
        self.run_program()


    def update_inputs(self, x: int, y: int):
        self.states = {}
        for d in self.x:
            self.x[d] = 0
            self.states[d] = 0
        for d in self.y:
            self.y[d] = 0
            self.states[d] = 0

        for i, c in enumerate(f'{x:b}'):
            self.states[f'x{i:02}'] = int(c)
            self.x[f'x{i:02}'] = int(c)

        for i, c in enumerate(f'{y:b}'):
            self.states[f'y{i:02}'] = int(c)
            self.y[f'y{i:02}'] = int(c)

        self.valid_add()
        self.run_program()


    def reset(self):
        self.states = self.x.copy()
        for y, v in self.y.items():
            self.states[y] = v


    def swap(self, g1, g2):
        self.reset()
        self.rules[g1], self.rules[g2] = self.rules[g2], self.rules[g1]
        self.run_program()


    def test(self, n: int=46):
        k = 2**(n+1) - 1
        bad = set()
        self.update_inputs(0,0)
        bad.update(self.bad_outputs(n))
        self.update_inputs(k,0)
        bad.update(self.bad_outputs(n))
        self.update_inputs(k,1)
        bad.update(self.bad_outputs(n))
        self.update_inputs(k,k)
        bad.update(self.bad_outputs(n))
        return bad


    def range_test(self, n:int=46):
        bad = set()
        for i in range(n+1):
            k = 2**(i+1) - 1
            self.update_inputs(0,0)
            bad.update(self.bad_outputs(n+1))
            self.update_inputs(k,0)
            bad.update(self.bad_outputs(n+1))
            self.update_inputs(k,1)
            bad.update(self.bad_outputs(n+1))
            self.update_inputs(k,k)
            bad.update(self.bad_outputs(n+1))
        return bad


    def test_swap(self, g1, g2, n=46):
        success = True
        cache_state = self.states
        self.reset()
        self.rules[g1], self.rules[g2] = self.rules[g2], self.rules[g1]

        try:
            bad = self.range_test(n)
        except RecursionError:
            success = False

        self.rules[g2], self.rules[g1] = self.rules[g1], self.rules[g2]
        self.states = cache_state
        self.run_program()

        if not success:
            raise RecursionError

        return bad


    def bad_outputs(self, n:int = 46):
        correct_str = f'{self.correct_sum:046b}'
        swapped_str = f'{self.current_sum:046b}'
        bad = set()
        for i, c in enumerate(correct_str[::-1]):
            if i > n:
                break
            if c != swapped_str[45-i]:
                bad.add(f'z{i:02}')
        # if bad:
        #     print(f'mismatched output. got {swapped_str}, expecting {correct_str}')
        return bad
    
    def valid_add(self):
        a1 = 0
        for x, v in self.x.items():
            a1 += v * 2**int(x[1:])

        a2 = 0
        for y, v in self.y.items():
            a2 += v * 2**int(y[1:])
        
        self.correct_sum = a1 + a2
        return self.correct_sum

        
    def compute_state(self, x: str, gate: str, y: str):
        if x in self.states:
            s1 = self.states[x]
        else:
            s1 = self.compute_state(*self.rules[x])
            self.states[x] = s1

        if y in self.states:
            s2 = self.states[y]
        else:
            s2 = self.compute_state(*self.rules[y])
            self.states[y] = s2

        if gate == 'OR':
            return s1 | s2 # 1 if s1 or s2 else 0
        elif gate == 'XOR':
            return s1 ^ s2 # 1 if s1 != s2 else 0
        elif gate == 'AND':
            return s1 & s2 # 1 if s1 and s2 else 0
        else:
            ValueError(f'cannot compute {x} {gate} {y}')


    def run_program(self):
        number = 0
        for i in range(len(self.z)):
            bin_digit = self.compute_state(*self.rules[f'z{i:02}'])
            number += bin_digit * 2**i
        self.current_sum = number


class Solution(TextSolution):
    _year = 2024
    _day = 24

    # 30870876971726 is too low
    @answer(66055249060558)
    def part_1(self) -> int:
        state, rule = self.input.split('\n\n')
        self.detector = FruitMonitor(state, rule)
        return self.detector.current_sum


    @answer('fcd,fhp,hmk,rvf,tpc,z16,z20,z33')
    def part_2(self) -> str:
        previous_dependencies = set()
        dependencies = set()
        for_trade = set()
        executed_trades = []
        for i in range(45):
            self.debug(f'starting place {i} with {len(for_trade)} available for swapping')
            # check this digit for bad outputs
            bad_outputs = self.detector.test(i)

            # build list of dependencies
            previous_dependencies.update(dependencies)
            dependencies = set()
            queue = [f'z{i:02}']
            while queue:
                gate = queue.pop()
                if gate in previous_dependencies:
                    continue
                if gate in self.detector.rules:
                    check1, _, check2 = self.detector.rules[gate]
                    queue.extend([check1, check2])
                    dependencies.add(gate)


            # reset trading set if all bad outputs have been resolved
            if bad_outputs:
                self.debug(f'bad outputs at level {i}', sorted(bad_outputs))
            else:
                for_trade = set()
                continue

            # test internal swaps if there are no trading candidates
            if for_trade:
                candidates = product(for_trade, dependencies)
            else:
                candidates = combinations(dependencies, 2)

            # test all combinations
            for old, new in candidates:
                try:
                    result = self.detector.test_swap(old, new, i)
                except RecursionError:
                    continue

                if len(result) == 0:
                    self.debug(f'improvement by swapping {old} with {new}, result: {len(result)}')
                    self.detector.swap(old, new)
                    executed_trades.extend((old,new))
                    bad_outputs = []
                    break

            # if bad outputs remain, put our current dependencies up for trade
            if bad_outputs:
                for_trade.update(dependencies)

        return ','.join(sorted(executed_trades))


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
