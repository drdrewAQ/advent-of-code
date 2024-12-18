# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/16

from collections import Counter
from queue import Queue
from solutions.utils.grid import add_points
from ...base import GridSolution, answer


MOVE: dict[str, tuple[int,int]] = {
        '^': tuple([-1, 0]),
        '<': tuple([0, -1]),
        '>': tuple([0, 1]),
        'v': tuple([1, 0])
        }

VALID: dict[str, set[str]] = {
        '^': set(['<', '>', '^']),
        '<': set(['^', 'v', '<']),
        '>': set(['^', 'v', '>']),
        'v': set(['<', '>', 'v'])
        }

class Solution(GridSolution):
    _year = 2024
    _day = 16

    @answer(88416)
    def part_1(self) -> int:
        directions = {}
        start = None
        end = None
        for l, c in self.input.items():
            if c == '#':
                continue
            if c == 'S':
                start = l
            if c == 'E':
                end = l
            for d, v in MOVE.items():
                n = add_points(l, v)
                if self.input[n] in '.SE':
                    directions.setdefault(l, set()).add(d)

        assert(start is not None and end is not None)
        # start crawling
        to_check = Queue()
        visited_score = Counter()
        to_check.put((start, '>', [], 0))
        while not to_check.empty():
            (current, d_in, history, score) = to_check.get()
            for d_out in directions[current].intersection(VALID[d_in]):
                future = add_points(current, MOVE[d_out])
                increment = 1 if d_out == d_in else 1001
                if future not in visited_score or score + increment < visited_score[future]:
                    visited_score[future] = score + increment
                    if future != end:
                        to_check.put((future, d_out, history + [future], score + increment))
        return visited_score[end]


    @answer(442)
    def part_2(self) -> int:
        directions = {}
        start = None
        end = None
        for l, c in self.input.items():
            if c == '#':
                continue
            if c == 'S':
                start = l
            if c == 'E':
                end = l
            for d, v in MOVE.items():
                n = add_points(l, v)
                if self.input[n] in '.SE':
                    directions.setdefault(l, set()).add(d)

        self.debug('part two is beginning the crawl')
        assert(start is not None and end is not None)
        # start crawling
        to_check = Queue()
        visited_score = Counter()
        seat_location = set()
        to_check.put((start, '>', [start], 0))

        while not to_check.empty():
            (current, d_in, history, score) = to_check.get()
            for d_out in directions[current].intersection(VALID[d_in]):
                future = add_points(current, MOVE[d_out])
                
                # no loops
                if future in history:
                    continue
                new_score = score + 1 if d_out == d_in else score + 1001
                # we're already beat
                if end in visited_score and visited_score[end] < new_score:
                    continue

                if future not in visited_score or new_score < visited_score[future]:
                    visited_score[future] = new_score
                    if future == end:
                        seat_location = set(history + [future])
                        self.debug(f'reached the end with new high score {new_score} and {len(seat_location)} seats.')
                    else:
                        to_check.put((future, d_out, history + [future], new_score))
                    continue

                # all 'best' paths get seats
                if future == end and new_score == visited_score[future]:
                    seat_location.update(history)
                    self.debug(f'reached the end and updated to {len(seat_location)} seats.')
                    continue

                # this path might still be best if a rotation occurred on best visit
                if new_score < visited_score[future] + 1001:
                    to_check.put((future, d_out, history + [future], new_score))

        print(f'finished with score {visited_score[end]}')
        return len(seat_location)


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
