import argparse
import os.path

import matplotlib.pyplot as plt
import networkx
import networkx as nx
import pytest
import support
from networkx.algorithms.shortest_paths.generic import all_shortest_paths
from networkx.algorithms.simple_paths import all_simple_paths

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

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
    G = nx.DiGraph(parse_to_dict(s))
    return sum(1 for _ in all_simple_paths(G, 'you', 'out'))


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
