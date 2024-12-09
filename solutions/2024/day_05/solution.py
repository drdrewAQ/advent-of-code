# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/5

from ...base import TextSolution, answer


class Solution(TextSolution):
    _year = 2024
    _day = 5

    @answer(7074)
    def part_1(self) -> int:
        prereq, orders = self.input.split('\n\n')

        must_follow = {}
        for rule in prereq.split('\n'):
            pre, post = rule.split('|')
            must_follow.setdefault(pre, set()).add(post)

        sum = 0
        for order in orders.split('\n'):
            pages = order.split(',')
            middle = int(pages[len(pages)//2])
            while pages and middle:
                this = pages.pop(0)
                for p in pages:
                    if p in must_follow and this in must_follow[p]:
                        middle = 0
            sum += middle

        return sum

    @answer(4828)
    def part_2(self) -> int:
        prereq, orders = self.input.split('\n\n')

        must_follow = {}
        for rule in prereq.split('\n'):
            pre, post = rule.split('|')
            must_follow.setdefault(pre, set()).add(post)

        sum = 0
        for order in orders.split('\n'):
            pages = order.split(',')

            # build the partial order topology
            topo = {p: 0 for p in pages}
            for p in topo:
                for q in must_follow:
                    if q in pages and p in must_follow[q]:
                        topo[p] += 1

            in_order = True
            sorted = []
            while pages:
                if in_order:
                    this = pages.pop(0)
                else:
                    # we're not in order, so sort (take first 0-deg node)
                    for i, p in enumerate(pages):
                        if topo[p] == 0:
                            break
                    this = pages.pop(i)

                # this has no remaining predecessors
                if topo[this] == 0:
                    # put it into sorted
                    sorted.append(this)
                    # and remove it as a predecessor
                    for p in pages:
                        if p in must_follow[this]:
                            topo[p] -= 1
                else:
                    # otherwise put node back and finish with sort
                    in_order = False
                    pages.insert(0, this)
            if not in_order:
                middle = sorted[len(sorted)//2]
                sum += int(middle)
        return sum

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
