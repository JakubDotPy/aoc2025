import argparse
import os.path
from collections.abc import Generator

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""
EXPECTED = 21


def load_splitters(s: str) -> Generator[set[int]]:
    yield from (
        set(idx for idx, char in enumerate(row) if char == '^') for row in s.splitlines()[2::2]
    )


def compute(s: str) -> int:
    splitters = load_splitters(s)
    beams = {s.find('S')}
    total_splits = 0
    for current_splitters in splitters:
        for splitter in current_splitters:
            if splitter in beams:
                total_splits += 1
            beams -= {splitter}
            beams.add(splitter - 1)
            beams.add(splitter + 1)

    return total_splits


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
