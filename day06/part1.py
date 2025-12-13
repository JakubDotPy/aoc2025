import argparse
import functools
from operator import add
from operator import mul
from pathlib import Path

import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

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
    columns = zip(*(row.split() for row in rows), strict=False)

    total = 0
    for column in columns:
        *nums, op_char = column
        operator = mul if op_char == '*' else add
        nums_iter = map(int, nums)
        total += functools.reduce(operator, nums_iter)

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
