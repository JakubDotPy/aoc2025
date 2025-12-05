import argparse
import os.path

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

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
    ranges, ingredients = s.split('\n\n')

    ranges = [tuple(map(int, num_range.split('-'))) for num_range in ranges.splitlines()]

    # Sort by start position
    ranges.sort()

    # Merge overlapping intervals
    merged = []
    for start, end in ranges:
        if merged and start <= merged[-1][1] + 1:
            # Overlaps or touches previous interval
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            # No overlap, add new interval
            merged.append((start, end))

    # Count total numbers (inclusive ranges)
    total = sum(end - start + 1 for start, end in merged)

    return total


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
