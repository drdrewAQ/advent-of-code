# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/1

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2024
    _day = 1

    @answer(1341714)
    def part_1(self) -> int:
        list1 = []
        list2 = []

        for line in self.input:
            num1, num2 = map(int, line.split())
            list1.append(num1)
            list2.append(num2)

        list1.sort()
        list2.sort()

        total_difference = sum(abs(a - b) for a, b in zip(list1, list2))

        # print(f"The sum of absolute differences after sorting is: {total_difference}")
        return total_difference

    @answer(27384707)
    def part_2(self) -> int:
        from collections import Counter

        list1 = Counter()
        list2 = Counter()

        for line in self.input:
            num1, num2 = map(int, line.split())
            list1[num1] += 1
            list2[num2] += 1

        sum = 0
        for k,v in list1.items():
            if k not in list2:
                continue
            similarity = int(k)*v*list2[k]
            sum += similarity

        # print(f'the total similarity is {sum}')
        return sum

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
