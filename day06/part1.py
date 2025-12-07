import argparse
import functools
import os.path
from operator import add
from operator import mul

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = """\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""
EXPECTED = 4277556


def compute(s: str) -> int:
    rows = s.splitlines()
    columns = zip(*(row.split() for row in rows))

    total = 0
    for column in columns:
        *nums, op_char = column
        operator = mul if op_char == '*' else add
        nums = map(int, nums)
        total += functools.reduce(operator, nums)

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
