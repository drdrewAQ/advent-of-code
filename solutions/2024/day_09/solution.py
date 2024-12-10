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
        idx = 0             # tracking file_id
        total = 0           # total size of all file blocks
        disk = []           # will be similar to example (None instead of '.')
        empty_idx = []      # indices for the start of each empty block
        pre = [int(c) for c in self.input]
        for size in pre:
            fill = None
            if file:
                total += size
                fill = idx
                idx += 1
            elif size:
                # not a file, but having size > 0, so record our current position
                empty_idx.append(len(disk))
            for _ in range(size):
                disk.append(fill)
            file = not file

        # start moving end blocks into empty block spaces
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
        pos = 0                 # record total length as we abandon 'disk'
        idx = 0                 # track file_id
        file_position = {}      # maps file id to position
        filesize_at = {}        # maps file position to size 
        emptyspace_at = {}      # maps empty position to size
        pre = [int(c) for c in self.input]
        for size in pre:
            if file:
                file_position[idx] = pos
                filesize_at[pos] = size
                idx += 1
            elif size:
                emptyspace_at[pos] = size
            file = not file
            pos += size

        # count backwards through the file indices
        for file_id in sorted(file_position.keys(), reverse=True):
            file_location = file_position[file_id]
            file_size = filesize_at[file_location]
            for empty_location in sorted(emptyspace_at):
                # only move to lower indices                 
                if empty_location > file_location:
                    break
                # is the empty space large enough?
                empty_size = emptyspace_at[empty_location]
                if empty_size >= file_size:
                    # update the location of this file_id
                    file_position[file_id] = empty_location
                    # relocate this file_id's file_size
                    del filesize_at[file_location]
                    filesize_at[empty_location] = file_size
                    # resize emptyspace and relocate if space remaining
                    del emptyspace_at[empty_location]
                    if (empty_remaining := empty_size - file_size):
                        emptyspace_at[empty_location+file_size] = empty_remaining
                    break

        result = 0
        for file_id, file_location in file_position.items():
            file_size = filesize_at[file_location]
            for i in range(file_size):
                result += file_id * (file_location + i)

        return result


    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
