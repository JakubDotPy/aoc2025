import argparse
from collections import deque
from pathlib import Path

import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

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
EXPECTED = 6


def compute(s: str) -> int:
    dial = deque(range(100))
    total = 0
    dial.rotate(50)
    for line in s.splitlines():
        direction, distance = line[0], int(line[1:])
        for _ in range(distance):
            dial.rotate(-1 if direction == 'L' else 1)
            if dial[0] == 0:
                total += 1

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
