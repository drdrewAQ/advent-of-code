# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/2

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2024
    _day = 2

    def is_unsafe(self, levels, dampened = False):
        # relocate the decreasing logic in case we drop an extrema as first or last level
        if levels[-1] - levels[0] > 0:
            levels.reverse()

        for i in range(1, len(levels)):
            d = levels[i-1] - levels[i]
            if d < 1 or d > 3:
                if dampened:
                    return True

                # not ideal, but better here than brute forcing the whole list
                pared_left = levels.copy()
                del pared_left[i-1]
                pared_right = levels.copy()
                del pared_right[i]

                return self.is_unsafe(pared_left, dampened = True) and self.is_unsafe(pared_right, dampened = True)

        return False

    @answer(660)
    def part_1(self) -> int:
        safe_counter = 0
        for report in self.input:
            levels = list(map(int, report.split()))
            assert len(levels) > 1

            if self.is_unsafe(levels, dampened = True):
                continue

            safe_counter += 1

        return safe_counter

    @answer(689)
    def part_2(self) -> int:
        safe_counter = 0
        for report in self.input:
            levels = list(map(int, report.split()))
            assert len(levels) > 1

            if self.is_unsafe(levels):
                continue

            safe_counter += 1

        return safe_counter

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
