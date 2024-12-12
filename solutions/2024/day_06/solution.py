# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/6

from solutions.utils.grid import add_points
from ...base import GridSolution, answer


class Solution(GridSolution):
    _year = 2024
    _day = 6

    move: dict[str, tuple[int,int]] = {
            '^': tuple([-1, 0]),
            '<': tuple([0, -1]),
            '>': tuple([0, 1]),
            'v': tuple([1, 0])
            }
    rotate = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

    @answer(5153)
    def part_1(self) -> int:
        visited = set()

        loc, pointer = None, None
        for loc, pointer in self.input.items():
            if pointer in self.move.keys():
                break

        assert(loc is not None and pointer is not None)

        # look at next step
        next_loc = add_points(loc, self.move[pointer])

        # so long as we're not going to step off the board...
        while next_loc in self.input:
            self.debug(f'{pointer} to {next_loc}')

            # rotate or step forward
            if self.input[next_loc] == '#':
                pointer = self.rotate[pointer]
            else:
                visited.add(loc)
                loc = next_loc

            # and prepare for the next step
            next_loc = add_points(loc, self.move[pointer])

        # make sure we consider our final position
        visited.add(loc)
        return len(visited)

    @answer(1711)
    def part_2(self) -> int:
        visited = {}
        targets = set()

        loc, pointer = None, None
        for loc, pointer in self.input.items():
            if pointer in self.move.keys():
                break

        assert(loc is not None and pointer is not None)

        # look at next step
        next_loc = add_points(loc, self.move[pointer])

        # as long as we're not going to step off the board...
        while next_loc in self.input:
            # record where we've been (with the direction we're headed)
            visited.setdefault(loc, set()).add(pointer)

            # either rotate or step forward
            if self.input[next_loc] == '#':
                pointer = self.rotate[pointer]
            else:
                # before we step forward, look ahead to see what happens if we instead make a turn
                # but only do so if we haven't already been to the next square!
                if next_loc not in visited:
                    i_loop = False
                    i_visited = {}
                    i_loc = loc
                    i_pointer = self.rotate[pointer]
                    i_next = add_points(i_loc, self.move[i_pointer])
                    # same as before, loop until we're going to step off
                    while i_next in self.input:
                        # record location and direction in log of imaginary steps
                        i_visited.setdefault(i_loc, set()).add(i_pointer)

                        # if we hit any previously-visited square (heading in the same direction) either real or imagined, that's a loop
                        if i_next in visited and i_pointer in visited[i_next]:
                            i_loop = True
                            break

                        if i_next in i_visited and i_pointer in i_visited[i_next]:
                            i_loop = True
                            break

                        # rotate or step forward
                        # ensure that our imaginary barrier is treated like a 'real' barrier!
                        if self.input[i_next] == '#' or i_next == next_loc:
                            i_pointer = self.rotate[i_pointer]
                        else:
                            i_loc = i_next

                        # and look at next step
                        i_next = add_points(i_loc, self.move[i_pointer])

                    if i_loop:
                        targets.add(next_loc)

                # actually step forward like we were supposed to
                loc = next_loc

            # and predict our next move
            next_loc = add_points(loc, self.move[pointer])

        return len(targets)


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
