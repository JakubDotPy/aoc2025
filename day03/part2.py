import argparse
import os.path
from collections import deque

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = """\
987654321111111
811111111111119
234234234234278
818181911112111
"""
EXPECTED = 3121910778619


def largest_12_digit_number(s: str) -> int:
    batteries = list(map(int, s))
    queue = deque()
    result, count = 0, 0
    for idx, battery in enumerate(batteries):
        while queue and queue[-1] < battery:
            queue.pop()

        queue.append(battery)
        if queue[0] == 9 or len(batteries) - idx == 12 - count:
            count += 1
            result += pow(10, 12 - count) * queue.popleft()

            if count == 12:
                break
    return result


def compute(s: str) -> int:
    return sum(largest_12_digit_number(line) for line in s.splitlines())


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
