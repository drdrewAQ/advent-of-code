# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/4

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2024
    _day = 4

    # misunderstood the assignment and looked for any (non-linear) path X-M-A-S
    def look_around(self, y, x, depth):
        w = len(self.input[0]) - 1
        h = len(self.input) - 1
        l = max(x-1,0)
        r = min(x+1,w)
        u = min(y+1,h)
        d = max(y-1,0)

        count = 0
        for col in range(l,r+1):
            for row in range(d,u+1):
                if self.input[row][col] != 'XMAS'[depth]:
                    continue
                else:
                    if depth == 3:
                        count += 1
                    else:
                        count += self.look_around(row, col, depth+1)
        return count

                
    @answer(2414)
    def part_1(self) -> int:
        w = len(self.input[0]) - 1
        h = len(self.input) - 1
        found = set()
        # count = 0
        for i, row in enumerate(self.input):
            for j, col in enumerate(row):
                # if col != 'X':
                if col == 'M' or col == 'A':
                    continue
                mods = [[0,1], [1,1], [1,0], [1,-1]]
                for i_mod, j_mod in mods:
                    i_tail = i + i_mod * 3
                    j_tail = j + j_mod * 3
                    if i_tail < 0 or j_tail < 0 or i_tail > h or j_tail > w:
                        continue
                    if self.input[i][j] == 'X' and self.input[i+i_mod][j+j_mod] == 'M' and self.input[i+2*i_mod][j+2*j_mod] == 'A' and self.input[i_tail][j_tail] == 'S':
                        # count += 1
                        found.add(f'{i},{j}-{i_tail},{j_tail}')
                        # print(f'({count}) at {i}, {j}')
                    elif self.input[i][j] == 'S' and self.input[i+i_mod][j+j_mod] == 'A' and self.input[i+2*i_mod][j+2*j_mod] == 'M' and self.input[i_tail][j_tail] == 'X':
                        # count += 1
                        found.add(f'{i_tail},{j_tail}-{i},{j}')
        return len(found)


    @answer(1871)
    def part_2(self) -> int:
        from collections import Counter
        count = 0
        h = len(self.input) - 1
        w = len(self.input[0]) - 1

        for i in range(1,h):
            for j in range(1,w):
                if self.input[i][j] == 'A':
                    cross = [self.input[i+1][j-1],self.input[i+1][j+1],self.input[i-1][j+1],self.input[i-1][j-1]]
                    c = Counter(cross)
                    if c['X'] or c['A'] or c['M'] != 2 or cross[0] == cross[2]:
                        continue
                    count += 1
        return count

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
