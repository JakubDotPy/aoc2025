import argparse
import itertools
import os.path

import pytest
import shapely
import support
from shapely.geometry import Point
from shapely.geometry import box

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S_1 = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
EXPECTED_1 = 24
INPUT_S_2 = """\
4,2
13,2
13,4
8,4
8,6
11,6
11,10
4,10
"""
EXPECTED_2 = 40
INPUT_S_3 = """\
3,2
13,2
13,4
8,4
8,6
11,6
11,11
7,11
7,8
5,8
5,10
3,10
"""
EXPECTED_3 = 35
INPUT_S_4 = """\
3,2
17,2
17,13
13,13
13,11
15,11
15,8
11,8
11,15
18,15
18,17
4,17
4,12
6,12
6,5
3,5
"""
EXPECTED_4 = 66


def _rect_area(rect: shapely.Polygon) -> int:
    x1, y1, x2, y2 = rect.bounds
    return int((abs(x2 - x1) + 1) * (abs(y2 - y1) + 1))


def compute(s: str) -> int:
    points = [
        Point(map(int, row.split(',')))
        for row in s.splitlines()
    ]
    polygon = shapely.Polygon(points)
    max_area = 0

    for p1, p2 in itertools.combinations(points, 2):
        rect = box(p1.x, p1.y, p2.x, p2.y)
        if shapely.contains(polygon, rect):
            max_area = max(max_area, _rect_area(rect))

    return max_area


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [
        (INPUT_S_1, EXPECTED_1),
        (INPUT_S_2, EXPECTED_2),
        (INPUT_S_3, EXPECTED_3),
        (INPUT_S_4, EXPECTED_4),
    ],
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
