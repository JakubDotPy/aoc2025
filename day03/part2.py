import argparse
from collections import deque
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
EXPECTED = 3121910778619

MAX_BATTERY_VALUE = 9
TARGET_DIGITS = 12


def largest_12_digit_number(s: str) -> int:
    batteries = list(map(int, s))
    queue: deque[int] = deque()
    result, count = 0, 0
    for idx, battery in enumerate(batteries):
        while queue and queue[-1] < battery:
            queue.pop()

        queue.append(battery)
        if queue[0] == MAX_BATTERY_VALUE or len(batteries) - idx == TARGET_DIGITS - count:
            count += 1
            result += pow(10, TARGET_DIGITS - count) * queue.popleft()

            if count == TARGET_DIGITS:
                break
    return result


def compute(s: str) -> int:
    return sum(largest_12_digit_number(line) for line in s.splitlines())


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
