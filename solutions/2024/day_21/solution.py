# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/21
# 'v<<A>>^A<vA<A>>^AAvAA<^A>Av<<A>>^AvA^Av<<A>>^A<vA>A^AA<A>Av<<A>A^>AAA<Av>A^A'
#     <   A  v <   AA >>  ^ A   <   A > A   <   A  v > AA ^ A   < v  AAA ^  > A
#         ^        <<       A       ^   A       ^      >>   A        vvv      A
# 'v<<A>>^A<vA<A>>^AAvAA<^A>Av<<A>>^AvA^Av<<A>>^A<vA>A^A*<A>Av<<A>A^>AAA<Av>A^A'
#     <   A  v <   AA >>  ^ A   <   A > A   <   A  v > A* ^ A   < v  AAA ^  > A
#         ^        <<       A       ^   A       ^      >>   A        vvv      A

from collections import Counter
from itertools import permutations, product
from solutions.utils.grid import parse_grid, subtract_points
from ...base import StrSplitSolution, answer

ROBOTS = 25

NUMPAD = parse_grid(['789', '456', '123', '#0A'], ignore_chars='#')
NUMLOC = {v: k for k,v in NUMPAD.items()}
NUMNA = {'70': 'vvv>', '7A': 'vvv>>', '40': 'vv>', '4A': 'vv>>', '10': 'v>', '1A': 'v>>',
         '07': '<^^^', 'A7': '<<^^^', '04': '<^^', 'A4': '<<^^', '01': '<^', 'A1': '<<^'
         }
NUMPATHS = {}
for f, t in permutations(NUMLOC, 2):
    i, j = subtract_points(NUMLOC[t],NUMLOC[f])

    lr = '>'*j if j > 0 else '<'*abs(j)
    ud = 'v'*i if i > 0 else '^'*abs(i)

    if i == 0 or j == 0:
        NUMPATHS[f+t] = lr + ud + 'A'
        continue

    if f+t in NUMNA:
        NUMPATHS[f+t] = lr + ud + 'A' if ud+lr == NUMNA[f+t] else ud + lr + 'A'
        continue
    
    if j < 0:
        NUMPATHS[f+t] = lr + ud + 'A'
    else:
        NUMPATHS[f+t] = ud + lr + 'A'


DPAD = parse_grid(['#^A', '<v>'], ignore_chars='#')
DLOC = {v: k for k,v in DPAD.items()}
DNA = {'<^': '^>', '<A': '^>>', '^<': '<v', 'A<': '<<v'}
DIRPATHS = {}
for f, t in product(DLOC, repeat=2):
    i, j = subtract_points(DLOC[t],DLOC[f])

    lr = '>'*j if j > 0 else '<'*abs(j)
    ud = 'v'*i if i > 0 else '^'*abs(i)

    if i == 0 or j == 0:
        DIRPATHS[f+t] = lr + ud + 'A'
        continue

    if f+t in DNA:
        DIRPATHS[f+t] = lr + ud + 'A' if ud+lr == DNA[f+t] else ud + lr + 'A'
        continue
    
    if j < 0:
        DIRPATHS[f+t] = lr + ud + 'A'
    else:
        DIRPATHS[f+t] = ud + lr + 'A'


class Solution(StrSplitSolution):
    _year = 2024
    _day = 21

    @answer(203734)
    def part_1(self) -> int:
        sum = 0
        current_kp = 'A'
        current_d = 'A'
        for code in self.input:
            self.debug('*'*10+f' {code} '+'*'*10)
            # handle the keypad
            iput = ''
            for c in code:
                iput += NUMPATHS[current_kp+c]
                current_kp = c

            # start looping through the robots
            for _ in range(2):
                oput = iput
                self.debug(f'at step {_} our candidate has length {len(oput)}')
                iput = ''
                for c in oput:
                    iput += DIRPATHS[current_d+c]
                    current_d = c

            self.debug(f'final step, our candidate has length {len(iput)}')
            self.debug(iput)
            sum += len(iput) * int(code[:-1])
        self.debug(f'***** FINAL SCORE: {sum}')
        return sum

    @answer(246810588779586)
    def part_2(self) -> int:
        sum = 0
        current_kp = 'A'
        for code in self.input:
            self.debug('*'*10+f' {code} '+'*'*10)
            iput = Counter()
            # handle the keypad
            for c in code:
                seq = 'A' + NUMPATHS[current_kp+c]
                for i in range(len(seq)-1):
                    iput[seq[i:i+2]] += 1
                current_kp = c
            self.debug(f'keypad sequence has length {iput.total()}')

            # start looping through the robots
            for _ in range(ROBOTS):
                oput = iput
                iput = Counter()
                # these are transitions {from}{to}, pressing from means we ended at 'A'
                for combo, count in oput.items():
                    seq = 'A' + DIRPATHS[combo] 
                    for i in range(len(seq)-1):
                        iput[seq[i:i+2]] += count
                self.debug(f'at step {_} our candidate has length {iput.total()}')


                # cache_out = ''
                # cache_in = ''
                # current_d = 'A'
                # self.debug(f'at step {_} our candidate has length {len(oput)}')

                # for c in oput:
                #     iput += DIRPATHS[current_d+c]
                #     current_d = c
                # while oput:
                #     if cache_in:
                #         c = oput[0]
                #         oput = oput[1:]
                #     else:
                #         for i in reversed(range(len(oput)+1)):
                #             if i == 0:
                #                 ValueError('i reached 0')
                #             # self.debug(f'{current_d+oput[:i]}')
                #             if (chomp := current_d + oput[:i]) in DIRPATHS:
                #                 cache_out += chomp # current_d + oput[:i]
                #                 cache_in += DIRPATHS[chomp] # cache_out]
                #
                #                 if i < len(oput):
                #                     c = oput[i]
                #                     oput = oput[i+1:]
                #                 else:
                #                     c, oput = '', ''
                #
                #                 current_d = cache_out[-1:]
                #                 break
                #
                #     cache_out += c if c else ''
                #     cache_in += DIRPATHS[current_d+c] if c else ''
                #
                #     # we always end on 'A'
                #     if not c or c == 'A':
                #         if cache_out in DIRPATHS:
                #             assert(DIRPATHS[cache_out] == cache_in)
                #         else:
                #             DIRPATHS[cache_out] = cache_in
                #         iput += cache_in
                #         # reset
                #         cache_out = ''
                #         cache_in = ''
                #     current_d = c

            self.debug(f'final step, our candidate has length {iput.total()}')
            sum += iput.total() * int(code[:-1])
        self.debug(f'***** FINAL SCORE: {sum}')
        return sum

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
