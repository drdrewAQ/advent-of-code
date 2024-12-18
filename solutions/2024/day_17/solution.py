# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/17

import re
from ...base import TextSolution, answer

CODE = [ 'adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv' ]

class Compy:
    A: int
    B: int
    C: int
    # i: int
    # lf: int = 0
    # lt: int = 0
    program: list[int]
    ptr: int = 0
    output: list[str] = []

    def __init__(self, A: str, B: str, C: str, p: list[int], log):
        self.A = int(A)
        self.B = int(B)
        self.C = int(C)
        # self.i = int(A)
        self.program = p
        # self.progress: int = 0
        self.log = log

    def combo(self, n: int):
        if n < 4:
            return n
        elif n == 4:
            return self.A
        elif n == 5:
            return self.B
        elif n == 6:
            return self.C
        else:
            ValueError('RESERVED combo operand')

    def adv(self, n: int):
        numerator = self.A
        denominator = 2**self.combo(n)
        # self.log(f'ADV: {numerator} // {denominator} -> A')
        self.A = numerator // denominator
        # self.log(f'ADV: register A is {self.A}')
        return True

    def bxl(self, n: int):
        # self.log(f'BXL: {self.B} XOR {n} -> B')
        self.B = self.B ^ n
        # self.log(f'BXL: register B is {self.B}')
        return True

    def bst(self, n: int):
        # self.log(f'BST: {self.combo(n)} % 8 -> B')
        self.B = self.combo(n) % 8
        # self.log(f'BST: register B is {self.B}')
        return True

    def jnz(self, n: int):
        if self.A == 0:
            return True
        self.ptr = n
        return False

    def bxc(self, _: int):
        # self.log(f'BXC: {self.B} XOR {self.C} -> B')
        self.B = self.B ^ self.C
        # self.log(f'BXC: register B is {self.B}')
        return True

    def out(self, n: int):
        # self.log(f'OUT: {self.combo(n)} % 8')
        self.output.append(f'{self.combo(n)%8}')
        return True

    def bdv(self, n: int):
        numerator = self.A
        denominator = 2**self.combo(n)
        # self.log(f'BDV: {numerator} // {denominator} -> B')
        self.B = numerator // denominator
        # self.log(f'BDV: register B is {self.B}')
        return True

    def cdv(self, n: int):
        numerator = self.A
        denominator = 2**self.combo(n)
        # self.log(f'CDV: {numerator} // {denominator} -> C')
        self.C = numerator // denominator
        # self.log(f'CDV: register C is {self.C}')
        return True

    def run(self, part_two=False):
        while self.ptr < len(self.program):
            opcode = self.program[self.ptr]
            operand = self.program[self.ptr + 1]
            # self.log(f'{CODE[opcode]}({operand}): [A: {self.A}, B: {self.B}, C: {self.C}]')
            f = getattr(self, CODE[opcode])
            if f(operand):
                self.ptr += 2

        # # for pattern investigation
        # if part_two: # and len(self.output) <= len(self.program):
        #     my_output = ''.join(self.output)
        #     my_program = ''.join(map(str, self.program))
        #     if len(self.output) > len(self.program):
        #         return False
        #     if my_program[-self.progress:] == my_output[-self.progress:]:
        #         self.log(f'{self.i:018b}: candidate @{self.progress} "{my_output}" vs. {my_program}')
        #     while my_program[-self.progress-1:] == my_output[-self.progress-1:]:
        #         self.progress += 1
        #         self.log(f'{self.i:018b}: increase +{self.progress}, "{my_output}" vs {my_program}')
        #         if self.progress == len(my_program):
        #             break

        return self.output # if not part_two or my_output == my_program else False

    def reset(self, A: int):
        self.A = A
        self.B = 0
        self.C = 0
        # self.i = A
        self.output = []
        self.ptr = 0

class Solution(TextSolution):
    _year = 2024
    _day = 17

    @answer('6,5,4,7,1,6,0,3,1')
    def part_1(self) -> str:
        debugger = re.compile(r'Register A: (\d+)\s*Register B: (\d+)\s*Register C: (\d+)\s*Program: (.*)$')
        if (m := re.match(debugger, self.input)):
            (reg_a, reg_b, reg_c, program) = m.groups()

        # self.debug(f"A: {reg_a}\nB: {reg_b}\nC: {reg_c}\nProgram: {program}")
        compy = Compy(reg_a, reg_b, reg_c, list(map(int, program.split(','))), self.debug)
        out = compy.run()
        return ','.join(map(str, out))
        
    @answer(106086382266778)
    def part_2(self) -> int:
        debugger = re.compile(r'Register A: (\d+)\s*Register B: (\d+)\s*Register C: (\d+)\s*Program: (.*)$')
        if (m := re.match(debugger, self.input)):
            (reg_a, reg_b, reg_c, program) = m.groups()

        compy = Compy(reg_a, reg_b, reg_c, list(map(int, program.split(','))), self.debug)
        program_string = program.replace(',','')
        candidates = [0]
        i = 0
        for i in range(len(program_string)):
            round_candidates = []
            for candidate in candidates:
                for j in range(8):
                    k = 8*candidate+j
                    compy.reset(k)
                    result = compy.run()
                    result_string = ''.join(map(str, result))
                    if result_string[-i-1:] == program_string[-i-1:]:
                        round_candidates.append(k)
                        if len(result_string) == len(program_string):
                            return k
            candidates = sorted(round_candidates)
            self.debug(f'after round {i}, our candidates are {round_candidates}')

        return min(candidates)

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
