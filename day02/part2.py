import argparse
import re
from collections.abc import Generator
from pathlib import Path

import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""
EXPECTED = 4174379265


def range_gen(s: str) -> Generator[range]:
    doubles = s.split(',')
    for double in doubles:
        low, high = double.split('-')
        yield range(int(low), int(high) + 1)


def compute(s: str) -> int:
    total = 0
    pattern = r'^(\d+)(\1)+$'
    for _range in range_gen(s):
        for n in _range:
            if re.match(pattern, str(n)):
                total += n
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
