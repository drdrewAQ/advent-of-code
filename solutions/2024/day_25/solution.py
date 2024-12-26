# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/25

from itertools import product
from ...base import TextSolution, answer

def parse_input(s: str):
    schematics = {}
    for block in s.split('\n\n'):
        type_lk, schematic = parse_block(block)
        schematics.setdefault(type_lk, []).append(schematic)
    return schematics

def parse_block(b: str):
    rows = b.split('\n')
    if rows[0] == '#####':
        return ('locks', parse_lock(rows[1:]))
    else:
        return ('keys', parse_key(rows[:-1]))

def parse_lock(rows: list[str]):
    lock = [0]*5
    for i, r in enumerate(rows):
        for j, c in enumerate(r):
            if c == '#':
                lock[j] = i+1
    return lock

def parse_key(rows: list[str]):
    key = [0]*5
    for i, r in enumerate(reversed(rows)):
        for j, c in enumerate(r):
            if c == '#':
                key[j] = i+1
    return key

def valid_combo(lock: list[int], key: list[int]):
    for i in range(5):
        if lock[i] + key[i] > 5:
            return False
    return True

class Solution(TextSolution):
    _year = 2024
    _day = 25

    @answer(3338)
    def part_1(self) -> int:
        # schematics = parse_input(self.input)
        # valid_combos = 0
        # for lock, key in product(schematics['locks'], schematics['keys']):
        #     if valid_combo(lock, key):
        #         valid_combos += 1
        # return valid_combos

        locks = []
        keys = []
        valid_combos = 0
        for block in self.input.split('\n\n'):
            rows = block.split('\n')
            if rows[0] == '#####':
                #lock stuff
                these = locks
                those = keys
            else:
                #key stuff
                these = keys
                those = locks

            this = [0]*5
            for i, r in enumerate(rows):
                for j, c in enumerate(r):
                    if c == '#':
                        this[j] = i

            for that in those:
                if valid_combo(this, that):
                    valid_combos += 1

            these.append(this)
        return valid_combos


    # @answer(1234)
    def part_2(self) -> int:
        pass

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
