import argparse
from pathlib import Path

import networkx as nx
import pytest
import support
from networkx.algorithms.simple_paths import all_simple_paths

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""
EXPECTED = 5

ParsedDict = dict[str, list[str]]


def parse_to_dict(s: str) -> ParsedDict:
    d: ParsedDict = {}
    for line in s.splitlines():
        name, others = line.split(': ')
        d[name] = others.split()
    return d


def compute(s: str) -> int:
    g = nx.DiGraph(parse_to_dict(s))
    return sum(1 for _ in all_simple_paths(g, 'you', 'out'))


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
