import argparse
import os.path
from collections import deque

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

INPUT_S = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""
EXPECTED = 3


def compute(s: str) -> int:
    dial = deque(range(100))
    total = 0
    dial.rotate(50)
    for line in s.splitlines():
        direction, distance = line[0], int(line[1:])
        dial.rotate(distance if direction == 'L' else -distance)
        if dial[0] == 0:
            total += 1

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
