import argparse
import heapq
import itertools
from pathlib import Path

import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
EXPECTED = 50


def compute(s: str) -> int:
    points = {tuple(map(int, line.split(','))) for line in s.splitlines()}

    heap: list[tuple[int, tuple[int, ...], tuple[int, ...]]] = []
    for a, b in itertools.combinations(points, 2):
        area = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
        heapq.heappush(heap, (area, a, b))

    area, _max_a, _max_b = max(heap)
    return area


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
