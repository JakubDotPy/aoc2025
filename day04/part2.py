import argparse
import contextlib
from pathlib import Path

import pytest
import support
from support import adjacent_8
from support import parse_coords_char

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
EXPECTED = 43

MIN_ADJACENT_THRESHOLD = 4


def do_step(
    grid: dict[tuple[int, int], str],
) -> tuple[dict[tuple[int, int], str], set[tuple[int, int]]]:
    to_remove = set()
    for coord, value in grid.items():
        if value != '@':
            continue
        around_this = 0
        for adj_coord in adjacent_8(*coord):
            with contextlib.suppress(KeyError):
                around_this += grid[adj_coord] == '@'
        if around_this < MIN_ADJACENT_THRESHOLD:
            to_remove.add(coord)

    for c in to_remove:
        grid.pop(c)

    return grid, to_remove


def compute(s: str) -> int:
    total = 0
    grid = parse_coords_char(s)
    removed: set[tuple[int, int]] = {(0, 0)}  # dummy value to start the loop

    while removed:
        grid, removed = do_step(grid)
        total += len(removed)

    return total


# @pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [(INPUT_S, EXPECTED)],
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with Path(args.data_file).open() as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
