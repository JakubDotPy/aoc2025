import argparse
from collections import deque
from pathlib import Path

import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
EXPECTED = 7


def parse_line(line: str) -> tuple[int, list[int], tuple[int, ...]]:
    lights_s, *buttons_s, joltages_s = line.split(' ')

    lights = int(
        lights_s.strip('[]').replace('.', '0').replace('#', '1')[::-1],  # LSB
        2,  # convert from binary
    )
    buttons = []
    for button_s in buttons_s:
        idxs = map(int, button_s[1:-1].split(','))
        buttons.append(sum(1 << i for i in idxs))

    joltages = tuple(map(int, joltages_s.strip('{}').split(',')))

    return lights, buttons, joltages


def solve_one(lights_target: int, buttons: list[int], _joltages: tuple[int, ...]) -> int:
    # BFS to find shortest path (DFS wouldn't guarantee minimum steps)
    queue = deque([(0, 0)])  # (current_result, steps)
    visited = {0}

    while queue:
        current, steps = queue.popleft()

        if current == lights_target:
            return steps

        # Try XORing with each button
        for button in buttons:
            next_val = current ^ button
            if next_val not in visited:
                visited.add(next_val)
                queue.append((next_val, steps + 1))

    return 0


def compute(s: str) -> int:
    total = 0
    for line in s.splitlines():
        lights_target, buttons, joltages = parse_line(line)
        total += solve_one(lights_target, buttons, joltages)
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
