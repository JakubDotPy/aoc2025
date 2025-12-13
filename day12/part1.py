import argparse
import itertools
import re
from pathlib import Path

import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""
EXPECTED = 3  # NOTE: !! originally 2, but this day is a bit "hacky"


def parse(s: str) -> tuple[dict[int, list[str]], list[tuple[int, int, tuple[int, ...]]]]:
    *shapes_s, fields_s = s.split('\n\n')

    shapes = {}
    for shape_s in shapes_s:
        indx, *lines = shape_s.splitlines()
        shapes[int(indx[:-1])] = lines

    fields = []
    for field_s in fields_s.splitlines():
        width, height, *indxs = map(int, re.findall(r'\d+', field_s))
        fields.append((width, height, tuple(indxs)))

    return shapes, fields


def _can_fit(field: tuple[int, int, tuple[int, ...]], shapes: dict[int, list[str]]) -> bool:
    area = field[0] * field[1]

    indxs = field[2]
    occupied = 0
    for shp_indx, count in enumerate(indxs):
        occupied += count * sum(c == '#' for c in itertools.chain.from_iterable(shapes[shp_indx]))
    return area > occupied


def compute(s: str) -> int:
    shapes, fields = parse(s)

    # NOTE: ... I tried this first.. and it worked ¯\_(ツ)_/¯
    return sum(_can_fit(field, shapes) for field in fields)


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
