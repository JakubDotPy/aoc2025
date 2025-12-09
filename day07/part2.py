import argparse
import os.path
from functools import cache
from typing import Generator

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
EXPECTED = 40

def load_splitters(s: str) -> Generator[set[int]]:
    yield from (
        set(idx for idx, char in enumerate(row) if char == '^')
        for row in s.splitlines()[2::2]
    )


def compute(s: str) -> int:
    splitters = tuple(frozenset(row) for row in load_splitters(s))
    start = s.find('S')

    @cache
    def count_timelines(level: int, position: int) -> int:
        if level == len(splitters): 
            return 1

        if position in splitters[level]:
            # Hit a splitter: particle splits into two timelines
            return (
                count_timelines(level + 1, position - 1) +
                count_timelines(level + 1, position + 1)
            )
        else:
            # No splitter: continue straight
            return count_timelines(level + 1, position)

    return count_timelines(0, start)


# @pytest.mark.solved
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
