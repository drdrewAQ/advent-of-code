GridPoint = tuple[int, int]
IntGrid = dict[GridPoint, int]
StrGrid = dict[GridPoint, str]
Grid = IntGrid | StrGrid


def parse_grid(raw_grid: list[str], ignore_chars: str = "", int_values: bool = False) -> Grid:
    """
    returns 2-tuples of (row, col) with their value

    `ignore_chars` is for grid characters that aren't valid landing spots, like walls.

    `int_values` will parse grid entries as integers instead of strings (default)

    ```
    (0, 0) ------> (0, 9)
      |              |
      |              |
      |              |
      |              |
      V              V
    (9, 0) ------> (9, 9)
    ```
    """
    result = {}
    ignore = set(ignore_chars)

    for row, line in enumerate(raw_grid):
        for col, c in enumerate(line):
            if c in ignore:
                continue
            result[row, col] = int(c) if int_values else c

    return result


def add_points(a: GridPoint, b: GridPoint) -> GridPoint:
    """
    add a pair of 2-tuples together.
    """
    return a[0] + b[0], a[1] + b[1]


def subtract_points(a: GridPoint, b: GridPoint) -> GridPoint:
    """
    returns `a - b` for 2-tuples.
    """
    return a[0] - b[0], a[1] - b[1]
