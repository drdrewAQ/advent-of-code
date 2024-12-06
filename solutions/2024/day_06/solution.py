# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/6

from ...base import GridSolution, answer


class Solution(GridSolution):
    _year = 2024
    _day = 6

    move = {'^': [0, -1], '<': [-1, 0], '>': [1, 0], 'v': [0, 1]}
    rotate = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

    def print_merged(self, v, iv, ir, ic):
        for rc in v.keys():
            r, c = rc.split(',')
            self.input[int(r)][int(c)] = 'X'
        for rc in iv.keys():
            r, c = rc.split(',')
            self.input[int(r)][int(c)] = 'x'
        self.input[int(ir)][int(ic)] = '0'
        print("\n".join([''.join(r) for r in self.input]))

    @answer(5153)
    def part_1(self) -> int:
        h = len(self.input) - 1
        w = len(self.input[0]) - 1
        visited = set()

        # find initial pointer
        r, c, pointer = None, None, None
        for i, row in enumerate(self.input):
            if any((pointer := d) in row for d in self.move.keys()):
                c = row.index(pointer)
                r = i
                break

        assert(r is not None and c is not None and pointer is not None)

        # look at next step
        next = self.move[pointer]
        next_c = c + next[0]
        next_r = r + next[1]

        # so long as we're not going to step off the board...
        while next_r >= 0 and next_c >= 0 and next_r <= h and next_c <= w:
            # rotate or step forward
            if self.input[next_r][next_c] == '#':
                pointer = self.rotate[pointer]
            else:
                visited.add(f'{r},{c}')
                r, c = next_r, next_c

            # and prepare for the next step
            next = self.move[pointer]
            next_c = c + next[0]
            next_r = r + next[1]

        # make sure we consider our final position
        visited.add(f'{r},{c}')
        return len(visited)

    @answer(1711)
    def part_2(self) -> int:
        h = len(self.input) - 1
        w = len(self.input[0]) - 1
        visited = {}
        targets = set()

        # find initial pointer
        r, c, pointer = None, None, None
        for i, row in enumerate(self.input):
            if any((pointer := d) in row for d in self.move.keys()):
                c = row.index(pointer)
                r = i
                break

        assert(r is not None and c is not None and pointer is not None)

        # look at next step
        next = self.move[pointer]
        next_c = c + next[0]
        next_r = r + next[1]

        # as long as we're not going to step off the board...
        while next_r >= 0 and next_c >= 0 and next_r <= h and next_c <= w:
            # record where we've been (with the direction we're headed)
            visited.setdefault(f'{r},{c}', set()).add(pointer)

            # either rotate or step forward
            if self.input[next_r][next_c] == '#':
                pointer = self.rotate[pointer]
            else:
                # before we step forward, look ahead to see what happens if we instead make a turn
                # but only do so if we haven't already been to the next square!
                if f'{next_r},{next_c}' not in visited:
                    i_loop = False
                    i_visited = {}
                    i_pointer = self.rotate[pointer]
                    i_r, i_c = r, c
                    i_next = self.move[i_pointer]
                    i_next_r, i_next_c = i_r + i_next[1], i_c + i_next[0]
                    # same as before, loop until we're going to step off
                    while i_next_r >= 0 and i_next_c >= 0 and i_next_r <= h and i_next_c <= w:
                        # record location and direction in log of imaginary steps
                        i_visited.setdefault(f'{i_r},{i_c}', set()).add(i_pointer)

                        # if we hit any previously-visited square (heading in the same direction) either real or imagined, that's a loop
                        if f'{i_next_r},{i_next_c}' in visited and i_pointer in visited[f'{i_next_r},{i_next_c}']:
                            i_loop = True
                            break

                        if f'{i_next_r},{i_next_c}' in i_visited and i_pointer in i_visited[f'{i_next_r},{i_next_c}']:
                            i_loop = True
                            break

                        # rotate or step forward
                        # ensure that our imaginary barrier is treated like a 'real' barrier!
                        if self.input[i_next_r][i_next_c] == '#' or (i_next_r == next_r and i_next_c == next_c):
                            i_pointer = self.rotate[i_pointer]
                        else:
                            i_r, i_c = i_next_r, i_next_c

                        # and look at next step
                        i_next = self.move[i_pointer]
                        i_next_r, i_next_c = i_r + i_next[1], i_c + i_next[0]

                    if i_loop:
                        targets.add(f'{next_r},{next_c}')

                # actually step forward like we were supposed to
                r, c = next_r, next_c

            # and predict our next move
            next = self.move[pointer]
            next_c = c + next[0]
            next_r = r + next[1]

        return len(targets)


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
