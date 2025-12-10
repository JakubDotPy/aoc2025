import argparse
import os.path
import pulp

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
EXPECTED = 33


def parse_line(line: str):
    lights_s, *buttons_s, joltages_s = line.split(' ')

    lights = int(
        lights_s
        .strip('[]')
        .replace('.', '0')
        .replace('#', '1')
        [::-1]  # LSB
        , 2  # convert from binary
    )
    buttons = [
        map(int, button_s[1:-1].split(','))
        for button_s in buttons_s
    ]

    joltages = tuple(map(int, joltages_s.strip('{}').split(',')))

    return lights, buttons, joltages


def solve_one(buttons, joltages):
    """Solve minimum button presses needed to achieve target joltages."""
    button_effects = [list(button) for button in buttons]

    # create linear programming problem
    problem = pulp.LpProblem("MinimizeButtonPresses", pulp.LpMinimize)
    button_press_counts = [
        pulp.LpVariable(f"button_{i}_presses", lowBound=0, cat='Integer')
        for i in range(len(buttons))
    ]

    # objective: minimize total button presses
    problem += pulp.lpSum(button_press_counts)

    # constraints: each joltage target must be met exactly
    for joltage_idx, target_joltage in enumerate(joltages):
        buttons_affecting_joltage = pulp.lpSum(
            button_press_counts[button_idx]
            for button_idx, button_effect in enumerate(button_effects)
            if joltage_idx in button_effect
        )
        problem += buttons_affecting_joltage == target_joltage

    problem.solve(pulp.PULP_CBC_CMD(msg=0))
    return int(pulp.value(problem.objective))


def compute(s: str) -> int:
    total = 0
    for line in s.splitlines():
        _, buttons, joltages = parse_line(line)
        total += solve_one(buttons, joltages)
    return total


@pytest.mark.solved
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

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
