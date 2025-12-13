import argparse
from pathlib import Path

import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
987654321111111
811111111111119
234234234234278
818181911112111
"""
EXPECTED = 357


# 1111121111151111


def largest_two_digit(s: str) -> int:
    digits = [int(c) for c in s]
    n = len(digits)

    def best(i: int) -> int:
        if i >= n - 1:  # not enough digits left
            return 0

        # 1. take digits[i] as tens digit → pair with every later digit
        with_current = max(10 * digits[i] + digits[j] for j in range(i + 1, n))

        # 2. skip digits[i] entirely
        without_current = best(i + 1)

        return max(with_current, without_current)

    return best(0)


def compute(s: str) -> int:
    return sum(largest_two_digit(line) for line in s.splitlines())


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
