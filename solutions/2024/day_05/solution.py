# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/5

from ...base import TextSolution, answer


class Solution(TextSolution):
    _year = 2024
    _day = 5

    @answer(7074)
    def part_1(self) -> int:
        prereq, orders = self.input.split('\n\n')

        must_pre = {}
        for rule in prereq.split('\n'):
            pre, post = rule.split('|')
            if pre not in must_pre:
                must_pre[pre] = [post]
            else:
                must_pre[pre].append(post)

        sum = 0
        for order in orders.split('\n'):
            pages = order.split(',')
            middle = int(pages[int(len(pages)/2)])
            while pages:
                this = pages.pop(0)
                for p in pages:
                    if p in must_pre and this in must_pre[p]:
                        middle = 0
            sum += middle

        return sum

    # @answer(1234)
    def part_2(self) -> int:
        prereq, orders = self.input.split('\n\n')

        must_pre = {}
        for rule in prereq.split('\n'):
            pre, post = rule.split('|')
            if pre not in must_pre:
                must_pre[pre] = [post]
            else:
                must_pre[pre].append(post)

        sum = 0
        for order in orders.split('\n'):
            print(f'starting {order}')
            pages = order.split(',')
            in_order = True
            sorted = []
            while pages:
                this = pages.pop(0)
                for p in pages:
                    if p in must_pre and this in must_pre[p]:
                        print(f'{this} is not in order with {p}')
                        in_order = False
                        pages.insert(pages.index(p)+1, this)
                        break
                if this not in pages:
                    sorted.append(this)
            if not in_order:
                middle = int(sorted[int(len(sorted)/2)])
                print(f'{middle} found from {sorted}')
                sum += middle
        return sum

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
