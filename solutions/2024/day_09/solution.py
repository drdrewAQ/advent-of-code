# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/9

from ...base import TextSolution, answer


class Solution(TextSolution):
    _year = 2024
    _day = 9
    separator = ""

    @answer(6395800119709)
    def part_1(self) -> int:
        file = True
        idx = 0
        total = 0
        disk = []
        empty_idx = []
        pre = [int(c) for c in self.input]
        for size in pre:
            fill = None
            if file:
                total += size
                fill = idx
                idx += 1
            elif size:
                empty_idx.append(len(disk))
            for _ in range(size):
                disk.append(fill)
            file = not file

        empty_ptr = empty_idx.pop(0)
        while len(disk) > total:
            last = disk.pop()
            if last is None:
                continue
            disk[empty_ptr] = last
            if disk[empty_ptr+1] is None:
                empty_ptr += 1
            else:
                empty_ptr = empty_idx.pop(0)

        sum = 0
        for i, f in enumerate(disk):
            sum += i * f
        return sum


    @answer(6418529470362)
    def part_2(self) -> int:
        file = True
        pos = 0
        idx = 0
        disk = {}               # maps file id to position
        files = {}              # maps file position to size 
        empty = {}              # maps empty position to size
        pre = [int(c) for c in self.input]
        for size in pre:
            if file:
                disk[idx] = pos
                files[pos] = size
                idx += 1
            elif size:
                empty[pos] = size
            file = not file
            pos += size

        # count backwards through the file indices
        for f_i in sorted(disk.keys(), reverse=True):
            f_p = disk[f_i]
            f_s = files[f_p]
            for e_p in sorted(empty):
                # only move to lower indices                 
                if e_p > f_p:
                    break
                e_s = empty[e_p]
                if e_s >= f_s:
                    del files[f_p]
                    files[e_p] = f_s
                    del empty[e_p]
                    if (e_r := e_s - f_s):
                        empty[e_p+f_s] = e_r
                    disk[f_i] = e_p
                    break

        result = 0
        for f_i, f_p in disk.items():
            f_s = files[f_p]
            for i in range(f_s):
                result += f_i * (f_p + i)

        return result


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
