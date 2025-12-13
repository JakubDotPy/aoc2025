import argparse
from pathlib import Path

import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
EXPECTED = 14


def compute(s: str) -> int:
    ranges_s, _ingredients = s.split('\n\n')

    ranges = [tuple(map(int, num_range.split('-'))) for num_range in ranges_s.splitlines()]

    # Sort by start position
    ranges.sort()

    # Merge overlapping intervals
    merged: list[tuple[int, int]] = []
    for start, end in ranges:
        if merged and start <= merged[-1][1] + 1:
            # Overlaps or touches previous interval
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            # No overlap, add new interval
            merged.append((start, end))

    # Count total numbers (inclusive ranges)
    return sum(end - start + 1 for start, end in merged)


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
