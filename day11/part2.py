import argparse
from collections import defaultdict
from pathlib import Path

import networkx as nx
import pytest
import support

INPUT_TXT = Path(__file__).parent / 'input.txt'

# NOTE: paste test text here
INPUT_S = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""
EXPECTED = 2

ParsedDict = dict[str, list[str]]

FFT_BIT = 1  # 0b01
DAC_BIT = 2  # 0b10
BOTH = FFT_BIT | DAC_BIT


def parse_to_dict(s: str) -> ParsedDict:
    d: ParsedDict = {}
    for line in s.splitlines():
        name, others = line.split(': ')
        d[name] = others.split()
    return d


def compute(s: str) -> int:
    g = nx.DiGraph(parse_to_dict(s))

    def node_mask(n: str) -> int:
        m = 0
        if n == 'fft':
            m |= FFT_BIT
        if n == 'dac':
            m |= DAC_BIT
        return m

    ways: defaultdict[str, defaultdict[int, int]] = defaultdict(lambda: defaultdict(int))
    ways['svr'][node_mask('svr')] = 1

    for u in nx.topological_sort(g):
        for mask, cnt in ways[u].items():
            for v in g.successors(u):
                ways[v][mask | node_mask(v)] += cnt

    return ways['out'][BOTH]


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
