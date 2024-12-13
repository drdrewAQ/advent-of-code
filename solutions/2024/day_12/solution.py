# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/12

from collections import Counter
# from itertools import combinations
from ...utils.grid import add_points
from ...base import GridSolution, answer

# def possible_corners(directions):
#     possible = []
#     for v, w in combinations(directions, 2):
#         if v[0] * w[0] + v[1] * w[1] == 0:
#             possible.append(add_points(v,w))
#     return possible


class Solution(GridSolution):
    _year = 2024
    _day = 12

    @answer(1461752)
    def part_1(self) -> int:
        price = 0
        areas = Counter(self.input.values())
        # each crop may have multiple connected components
        # regions = { 'crop': [ neighbors, ... ]}
        regions: dict[str, list[Counter]] = {}
        # counting corners was actually slower
        # corners = Counter()
        for crop in areas:
            crop_map = [k for k,v in self.input.items() if v == crop]
            regions[crop] = []
            location = crop_map.pop()
            neighbors = Counter({location: 0})
            neighbor_queue = []

            while location:
                self.debug(f'checking {location}')
                directions = []
                for direction in tuple([0,1]), tuple([1,0]), tuple([-1,0]), tuple([0,-1]):
                    check = add_points(location, direction)
                    if check in self.input and self.input[check] == crop:
                        neighbors[location] += 1
                        directions.append(direction)
                        self.debug(f'{check} is a neighbor of {location}')
                        if check in crop_map:
                            self.debug(f'{check} has not been visited yet, queueing...')
                            del crop_map[crop_map.index(check)]
                            neighbor_queue.append(check)
                # # count corners for location (using neighbors[location])
                # # 0: 4
                # # 1: 2
                # # 2: 0 (opp) or 1 or 2 (perp)
                # # 3: 0, 1, or 2
                # # 4: 0 .. 4
                # if neighbors[location] == 0:
                #     corners[location] = 4
                # elif neighbors[location] == 1:
                #     corners[location] = 2
                # else:
                #     for direction in possible_corners(directions):
                #         # sneaky, we only get here for perp (min: 1) with second corner as maybe
                #         if neighbors[location] == 2:
                #             corners[location] += 1
                #         maybe = add_points(location, direction)
                #         if maybe in self.input and self.input[maybe] != crop:
                #             corners[location] += 1
                # self.debug(f'{location} has {neighbors[location]} neighbors and {corners[location]} corners')
                
                if neighbor_queue:
                    location = neighbor_queue.pop()
                    neighbors[location] = 0
                else:
                    # we have exhausted this connected component -- are there still crops of this type remaining?
                    regions[crop].append(neighbors)
                    if crop_map:
                        location = crop_map.pop()
                        neighbors = Counter({location: 0})
                        self.debug(f'queue for {crop} is empty... starting new region with {location}')
                    else:
                        location = None

            for region in regions[crop]:
                self.debug(f'crop {crop} has area {len(region)} and perimeter {4*len(region)-region.total()}')
                price += len(region) * (4*len(region) - region.total())
        
        # save this for part 2...
        self.regions = regions
        # self.corners = corners
        return price

    @answer(904114)
    def part_2(self) -> int:
        cost = 0
        # use our map of crops -> [connected components]
        for crop in self.regions.keys():
            self.debug(f'crop {crop} has costs:')
            for region in self.regions[crop]:
                # corners = 0
                # not a huge fan of this -- but it works
                # record edges along each side { row/column: [columns/rows] }
                top: dict[int, list[int]] = {}
                bottom: dict[int, list[int]] = {}
                left: dict[int, list[int]] = {}
                right: dict[int, list[int]] = {}
                for location in region.keys():
                    # corners += self.corners[location]
                    above = add_points(location, tuple([-1, 0]))
                    if above not in self.input or self.input[above] != crop:
                        top.setdefault(location[0], []).append(location[1])
                    below = add_points(location, tuple([1, 0]))
                    if below not in self.input or self.input[below] != crop:
                        bottom.setdefault(location[0], []).append(location[1])
                    before = add_points(location, tuple([0, -1]))
                    if before not in self.input or self.input[before] != crop:
                        left.setdefault(location[1], []).append(location[0])
                    after = add_points(location, tuple([0, 1]))
                    if after not in self.input or self.input[after] != crop:
                        right.setdefault(location[1], []).append(location[0])
                # horizontal edges happening in different rows must be separate sides
                # vertical edges happening in different columns must be separate sides
                # non-consecutive 'opposite'-coordinates must be separate sides
                sides = 0
                for line in top, bottom, left, right:
                    for vs in line.values():
                        sides += 1
                        vs = sorted(vs)
                        for i, v in enumerate(vs):
                            # check for separate connected components along the edge at this row/column
                            if i != 0 and v != vs[i-1]+1:
                                sides += 1
                self.debug(f'   cost: {sides * len(region)}')
                cost += sides * len(region)

        return cost


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
