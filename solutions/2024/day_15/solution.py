# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/15

import re
from collections import Counter
from ...utils.grid import add_points, parse_grid
from ...base import TextSolution, answer


MOVE: dict[str, tuple[int,int]] = {
        '^': tuple([-1, 0]),
        '<': tuple([0, -1]),
        '>': tuple([0, 1]),
        'v': tuple([1, 0])
        }


class Robot:
    i: int
    j: int

    def __init__(self, i:int, j:int):
        self.i = i
        self.j = j

    def position(self) -> tuple[int,int]:
        return tuple([self.i, self.j])

    def look(self, direction: str, n=1):
        if direction not in MOVE:
            ValueError(f'unrecognized direction {direction}')
        return add_points(self.position(), tuple([c * n for c in MOVE[direction]]))

    def step(self, direction: str):
        if direction not in MOVE:
            ValueError(f'unrecognized direction {direction}')
        self.i, self.j = add_points(self.position(), MOVE[direction])


class Box:
    i: int
    j: int

    def __init__(self, i: int, j:int):
        self.i, self.j = i, j

    def covers(self, loc: tuple[int,int]):
        return True if self.i == loc[0] and (self.j == loc[1] or self.j + 1 == loc[1]) else False

    def look(self, direction:str) -> set[tuple[int,int]]:
        if direction not in MOVE:
            ValueError(f'unrecognized direction {direction}')
        left: tuple[int,int] = add_points(self.position()[0], MOVE[direction])
        right: tuple[int,int] = add_points(self.position()[1], MOVE[direction])
        if direction == '<' or direction == '>':
            return set([left]) if direction == '<' else set([right])
        return set([left, right])

    def push(self, direction:str):
        if direction not in MOVE:
            ValueError(f'unrecognized direction {direction}')
        self.i, self.j = add_points(self.position()[0], MOVE[direction])

    def position(self):
        return tuple([tuple([self.i, self.j]), tuple([self.i, self.j + 1])])

    def gps(self):
        return 100 * self.i + self.j

def do_not_overlap(boxes: list[Box]) -> bool:
    locations = set()
    for box in boxes:
        locations.update([loc for loc in box.position()])
    return len(locations) == 2*len(boxes)

def do_not_hit_wall(boxes: list[Box], valid_locations: set[tuple[int,int]]) -> bool:
    for box in boxes:
        for loc in box.position():
            if loc not in valid_locations:
                return False 
    return True

class Solution(TextSolution):
    _year = 2024
    _day = 15


    @answer(1511865)
    def part_1(self) -> int:
        grid, moves = self.input.split('\n\n', maxsplit=1)
        grid = parse_grid(grid.split('\n'), ignore_chars='#')
        robot_x, robot_y = next((location for location, obj in grid.items() if obj == '@'), None)
        assert(robot_x is not None and robot_y is not None)
        robot = Robot(robot_x, robot_y)
        grid[robot.position()] = '.'

        moves = re.sub('\n', '', moves)
        for direction in moves:
            ahead = robot.look(direction)
            if ahead not in grid:
                continue
            if grid[ahead] == '.':
                robot.step(direction)
                continue
            i = 2
            farther = robot.look(direction, i)
            while farther in grid and grid[farther] == 'O':
                i += 1
                farther = robot.look(direction, i)
            if farther in grid:
                grid[ahead] = '.'
                grid[farther] = 'O'
                robot.step(direction)

        gps_total = 0
        for loc, obj in grid.items():
            if obj == 'O':
                gps_total += 100 * loc[0] + loc[1]
        return gps_total



    @answer(1519991)
    def part_2(self) -> int:
        grid, moves = self.input.split('\n\n', maxsplit=1)
        grid = parse_grid(grid.split('\n'), ignore_chars='#')
        robot_i, robot_j = next((location for location, obj in grid.items() if obj == '@'), None)
        assert(robot_i is not None and robot_j is not None)
        robot = Robot(robot_i, 2*robot_j)

        # translate from grid to double-wide
        wide_grid: set[tuple[int,int]] = set()
        boxes: list[Box] = []
        # walls were already ignored during grid parsing
        for loc, c in grid.items():
            i, j = loc
            wide_grid.update([tuple([i, 2*j]), tuple([i, 2*j+1])])
            # if we see a box, create it and add to the list of boxes
            if c == 'O':
                boxes.append(Box(i, 2*j))

        original_counts = Counter(grid.values())
        assert(len(boxes) == original_counts['O'])
        assert(len(wide_grid) == 2 * (original_counts['.'] + len(boxes) +1))

        # start looping through the moveset
        moves = re.sub('\n', '', moves)
        for direction in moves:
            ahead = robot.look(direction)
            if ahead not in wide_grid:
                self.debug(f'{direction}: robot encountered wall at {ahead}')
                continue

            # this is significantly slower than set([box in boxes if box.covers(...)])!
            # box_map = {}
            # for box in boxes:
            #     for loc in box.position():
            #         box_map[loc] = box

            # wave = set([box_map[ahead]]) if ahead in box_map else set()
            wave = set([box for box in boxes if box.covers(ahead)])
            if len(wave) == 0:
                self.debug(f'{direction}: free space {ahead}')
                robot.step(direction)
                continue

            self.debug(f'{direction}: pushing a box at {ahead}')
            affected = set()
            blocked = False
            while wave and not blocked:
                box = wave.pop()
                affected.add(box)
                for loc in box.look(direction):
                    if loc not in wide_grid:
                        self.debug(f'{direction}: box at {box.position()} blocked by wall at {loc}')
                        blocked = True
                        break

                    wave.update([box for box in boxes if box.covers(loc)])
                    # if loc in box_map:
                    #     wave.add(box_map[loc])
                    #     self.debug(f'{direction}: pushing another box at {loc}')

            if blocked:
                continue

            robot.step(direction)
            self.debug(f'{direction}: all clear, pushing {len(affected)} boxes')
            for box in affected:
                box.push(direction)
                self.debug(f'*** box moved to {box.position()}')

            # these assertions are expensive to check
            # assert(do_not_overlap(boxes))
            # assert(do_not_hit_wall(boxes, wide_grid))

        self.debug(f'final robot location: {robot.position()}')

        gps_total = 0
        for box in boxes:
            gps_total += box.gps()
        return gps_total


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
