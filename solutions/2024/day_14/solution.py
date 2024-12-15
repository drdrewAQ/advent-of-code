# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/14

import re
from collections import Counter
from functools import reduce
# from time import sleep
from ...base import StrSplitSolution, answer

WIDTH = 101
HEIGHT = 103

class Robot:
    x: int
    y: int
    # position: tuple[int,int]
    velocity: tuple[int,int]

    def __init__(self, x:int, y:int, v:tuple[int,int]):
        self.x = x
        self.y = y
        self.velocity = v

    def step(self, n=1):
        v_x, v_y = self.velocity
        return (self.x + n * v_x) % WIDTH, (self.y + n * v_y) % HEIGHT
    

def view(robots: list[Robot], step=0):
    loc = Counter()
    for r in robots:
        loc[r.step(step)] += 1

    row = [' ' for _ in range(WIDTH)]
    grid = [row.copy() for _ in range(HEIGHT)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            grid[y][x] = f'{loc[x,y]}' if loc[x,y] else '.'

    print('\n'.join([''.join(row) for row in grid]))
    print(f'step: {step}')
    print()



class Solution(StrSplitSolution):
    _year = 2024
    _day = 14

    @answer(226236192)
    def part_1(self) -> int:
        regex = re.compile(r'p=(\d+),(\d+) v=([\d\-]+),([\d\-]+)')
        MOVES = 100
        X_AXIS = WIDTH // 2
        Y_AXIS = HEIGHT // 2
        quadrant_count = Counter()

        for line in self.input:
            if m := re.match(regex, line):
                px, py, vx, vy = map(int, m.groups())
            else:
                ValueError(f'regex failed on line {line}')
            self.debug([px, py], [vx, vy])
            robot = Robot(px, py, tuple([vx, vy]))
            x, y = robot.step(MOVES)
            if x == X_AXIS or y == Y_AXIS:
                continue

            quadrant = 0
            if x > WIDTH // 2:
                quadrant += 1
            if y > HEIGHT // 2:
                quadrant += 2
            quadrant_count[quadrant] += 1

        return reduce(lambda a, b: a * b, quadrant_count.values())

    @answer(8168)
    def part_2(self) -> int:
        regex = re.compile(r'p=(\d+),(\d+) v=([\d\-]+),([\d\-]+)')
        robots: list[Robot] = []
        for line in self.input:
            if m := re.match(regex, line):
                px, py, vx, vy = map(int, m.groups())
            else:
                ValueError(f'regex failed on line {line}')
            self.debug([px, py], [vx, vy])
            robots.append(Robot(px, py, tuple([vx, vy])))

        # view(robots)
        # print(f'step: {steps}')
        devx = []
        devy = []
        for n in range(max(WIDTH, HEIGHT)):
            # view(robots, steps)
            xs, ys = [], []
            for r in robots:
                rx, ry = r.step(n)
                if n < WIDTH:
                    xs.append(rx)
                if n < HEIGHT:
                    ys.append(ry)

            if xs:
                meanx = sum(xs, 0)/len(xs)
                devx.append(sum(map(lambda x: (x - meanx)*(x - meanx), xs), 0)/(len(xs) - 1))
            if ys:
                meany = sum(ys, 0)/len(ys)
                devy.append(sum(map(lambda y: (y - meany)*(y - meany), ys), 0)/(len(ys) - 1))

        self.debug(f'x-clustering at {devx.index(min(devx))}')
        self.debug(f'y-clustering at {devy.index(min(devy))}')

        x_frame = devx.index(min(devx))
        y_frame = devy.index(min(devy))

        # the above resulted in the following observations:
        # y-clustering at step 31, height: 103
        # x-clustering at step 88, width: 101
        # step: 88 + 101x = 31 + 103y
        t = x_frame
        while t % HEIGHT != y_frame:
            t += WIDTH 

        view(robots, t)
        return t


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
