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
EXPECTED = 13

MIN_ADJACENT_THRESHOLD = 4


def compute(s: str) -> int:
    total = 0
    grid = parse_coords_char(s)
    for coord in grid:
        if grid[coord] == '.':
            continue
        around_this = 0
        for adj_coord in adjacent_8(*coord):
            with contextlib.suppress(KeyError):
                around_this += grid[adj_coord] == '@'
        total += around_this < MIN_ADJACENT_THRESHOLD

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
