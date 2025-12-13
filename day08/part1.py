import argparse
import functools
import heapq
import itertools
from operator import mul
from pathlib import Path

import numpy as np
import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""
EXPECTED = 40


def compute(s: str, num_steps: int) -> int:
    # NOTE: for test do 10 steps of the connecting process
    #  For the actual attempt do 1000 steps.

    # create points
    points = {tuple(map(int, line.split(','))) for line in s.splitlines()}
    # add to heap (priority queue by distance)
    heap: list[tuple[float, tuple[int, ...], tuple[int, ...]]] = []
    for a, b in itertools.combinations(points, 2):
        a_arr = np.array(a)
        b_arr = np.array(b)
        dist = np.linalg.norm(a_arr - b_arr)
        heapq.heappush(heap, (dist, a, b))

    # create a set of sets
    junctions = [{p} for p in points]
    for _ in range(num_steps):
        dist, a, b = heapq.heappop(heap)

        # merge the two sets
        # find the sets containing a and b, add them together and back
        set_a = next(s for s in junctions if a in s)
        set_b = next(s for s in junctions if b in s)

        # only merge if they are different sets
        if set_a is not set_b:
            junctions.remove(set_a)
            junctions.remove(set_b)
            junctions.append(set_a | set_b)

    lens = sorted(map(len, junctions))

    return functools.reduce(mul, lens[-3:])


# @pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'num_steps', 'expected'),
    [(INPUT_S, 10, EXPECTED)],
)
def test(input_s: str, num_steps: int, expected: int) -> None:
    assert compute(input_s, num_steps) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with Path(args.data_file).open() as f, support.timing():
        print(compute(f.read(), 1_000))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
