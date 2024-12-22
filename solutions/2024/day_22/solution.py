# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/22

from collections import Counter
from ...base import IntSplitSolution, answer

def next_price(a:int):
    n = a ^ (a << 6) & 16777215
    n ^= n >> 5
    return (n ^ (n << 11)) & 16777215

class Solution(IntSplitSolution):
    _year = 2024
    _day = 22

    @answer(18941802053)
    def part_1(self) -> int:
        sum = 0
        prices = Counter()
        for start in self.input:
            n = start
            prev = 0
            # cache holds the last four changes
            cache = []
            # map four change combo to price for this starting value
            these_prices = Counter()
            for _ in range(2000):
                n = next_price(n)
                price = n % 10
                cache.append(price - prev)
                prev = price
                if len(cache) > 4:
                    cache.pop(0)
                elif len(cache) < 4:
                    continue
                seq = tuple(cache)
                if seq in these_prices:
                    continue
                these_prices[seq] = price

            self.debug(f'{start} -> {n}')    
            prices.update(these_prices)
            sum += n
        self.prices = prices
        return sum

    @answer(2218)
    def part_2(self) -> int:
        return self.prices.most_common(1)[0][1]

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
