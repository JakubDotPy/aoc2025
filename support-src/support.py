"""Support functions for Advent of Code solutions."""

from __future__ import annotations

import argparse
import contextlib
import enum
import io
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from dataclasses import field
from functools import total_ordering
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

ENV_FILE = Path(__file__).parent.parent.parent / '.env'


@contextlib.contextmanager
def timing(name: str = '') -> Generator[None]:
    before = time.time()
    try:
        yield
    finally:
        after = time.time()
        t = (after - before) * 1000
        unit = 'ms'
        if t < 100:
            t *= 1000
            unit = 'μs'
        if name:
            name = f' ({name})'
        print(f'> {int(t)} {unit}{name}', file=sys.stderr, flush=True)


def _get_cookie_headers() -> dict[str, str]:
    with Path.open(ENV_FILE) as f:
        contents = f.read().strip()
    return {'Cookie': contents}


def get_input(year: int, day: int) -> str:
    url = f'https://adventofcode.com/{year}/day/{day}/input'
    req = urllib.request.Request(url, headers=_get_cookie_headers())
    return urllib.request.urlopen(req).read().decode()


def get_year_day() -> tuple[int, int]:
    cwd = Path.cwd()
    day_s = cwd.name
    year_s = cwd.parent.name

    if not day_s.startswith('day') or not year_s.startswith('aoc'):
        err_msg = f'unexpected working dir: {cwd}'
        raise AssertionError(err_msg)

    return int(year_s[len('aoc') :]), int(day_s[len('day') :])


TOO_QUICK = re.compile('You gave an answer too recently.*to wait.')
WRONG = re.compile(r"That's not the right answer.*?\.")
RIGHT = "That's the right answer!"
ALREADY_DONE = re.compile(r"You don't seem to be solving.*\?")


def _post_answer(year: int, day: int, part: int, answer: int) -> str:
    params = urllib.parse.urlencode({'level': part, 'answer': answer})
    req = urllib.request.Request(
        f'https://adventofcode.com/{year}/day/{day}/answer',
        method='POST',
        data=params.encode(),
        headers=_get_cookie_headers(),
    )
    resp = urllib.request.urlopen(req)

    return resp.read().decode()


def submit_solution() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', type=int, required=True)
    args = parser.parse_args()

    year, day = get_year_day()
    answer = int(sys.stdin.read())

    print(f'answer: {answer}')

    contents = _post_answer(year, day, args.part, answer)

    for error_regex in (WRONG, TOO_QUICK, ALREADY_DONE):
        error_match = error_regex.search(contents)
        if error_match:
            print(f'\033[41m{error_match[0]}\033[m')
            return 1

    if RIGHT in contents:
        print(f'\033[42m{RIGHT}\033[m')
        return 0
    else:
        # unexpected output?
        print(contents)
        return 1


def download_input() -> int:
    year, day = get_year_day()

    for _ in range(5):
        try:
            s = get_input(year, day)
        except urllib.error.URLError as e:
            print(f'zzz: not ready yet: {e}')
            time.sleep(1)
        else:
            break
    else:
        raise SystemExit('timed out after attempting many times')

    with open('input.txt', 'w') as f:
        f.write(s)

    lines = s.splitlines()
    if len(lines) > 10:
        for line in lines[:10]:
            print(line)
        print('...')
    else:
        print(lines[0][:80])
        print('...')

    return 0


def new_day() -> None:
    print(' Creating new advent day '.center(50, '-'))

    temp_dir = Path('day00').absolute()

    # find number of last day
    last_day = sorted(
        folder.name
        for folder in Path().iterdir()
        if folder.is_dir() and folder.name.startswith('day')
    )[-1]

    print(f'Last day is {last_day}.')

    # prepare the paths
    last_day_num = int(re.findall(r'\d+', last_day)[0])
    new_day_num = last_day_num + 1
    new_day_folder_name = f'day{new_day_num:02}'
    new_path = Path(new_day_folder_name).absolute()

    # copy folder
    print(f"Creating folder '{new_day_folder_name}'.")
    shutil.copytree(temp_dir, new_path)

    # replace template mark with commented solved
    old = r'@pytest.mark.template'
    new = r'# @pytest.mark.solved'
    pattern = re.compile(old)
    with Path.open(new_path / 'part1.py', 'r+') as f:
        contents = f.read()
        contents = pattern.sub(new, contents)
        f.seek(0)
        f.write(contents)

    # edit run configurations
    print('Editing run configuration.')
    for file in Path('.run').iterdir():
        print(f' - editing {file}')
        with Path.open(file) as f:
            contents = f.read()
            new_contents = re.sub(r'day\d\d', rf'{new_day_folder_name}', contents)
        with Path.open(file, 'w') as f:
            f.write(new_contents)

    print(' Finished '.center(50, '-'))


# --- helper functions and classes


def adjacent_4(x: int, y: int) -> Generator[tuple[int, int]]:
    yield x, y - 1
    yield x + 1, y
    yield x, y + 1
    yield x - 1, y


def adjacent_8(x: int, y: int) -> Generator[tuple[int, int]]:
    for y_d in (-1, 0, 1):
        for x_d in (-1, 0, 1):
            if y_d == x_d == 0:
                continue
            yield x + x_d, y + y_d


def parse_coords_char(s: str) -> dict[tuple[int, int], str]:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = c
    return coords


def parse_coords_int(s: str) -> dict[tuple[int, int], int]:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = int(c)
    return coords


def parse_coords_hash(s: str) -> set[tuple[int, int]]:
    coords = set()
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                coords.add((x, y))
    return coords


def parse_numbers_split(s: str) -> list[int]:
    return [int(x) for x in s.split()]


def parse_numbers_comma(s: str) -> list[int]:
    return [int(x) for x in s.strip().split(',')]


def format_coords_hash(coords: set[tuple[int, int]]) -> str:
    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)

    min_x = min_y = 0
    max_x = max_y = 9

    return '\n'.join(
        ''.join('#' if (x, y) in coords else '.' for x in range(min_x, max_x + 1))
        for y in range(min_y, max_y + 1)
    )


def print_coords_hash(coords: set[tuple[int, int]]) -> None:
    print(format_coords_hash(coords))


class OutOfBounds(Exception):
    pass


class Direction4(enum.Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    @property
    def _vals(self) -> tuple[Direction4, ...]:
        return tuple(type(self).__members__.values())

    @property
    def cw(self) -> Direction4:
        vals = self._vals
        return vals[(vals.index(self) + 1) % len(vals)]

    @property
    def ccw(self) -> Direction4:
        vals = self._vals
        return vals[(vals.index(self) - 1) % len(vals)]

    @property
    def opposite(self) -> Direction4:
        vals = self._vals
        return vals[(vals.index(self) + 2) % len(vals)]

    def apply(self, x: int, y: int, *, n: int = 1) -> tuple[int, int]:
        return self.x * n + x, self.y * n + y

    @property
    def chr(self) -> str:
        chr_map = {
            Direction4.UP: '^',
            Direction4.RIGHT: '>',
            Direction4.DOWN: 'v',
            Direction4.LEFT: '<',
        }
        return chr_map[self]


@total_ordering
@dataclass
class Pointer:
    x: int = 0
    y: int = 0
    direction: Direction4 = None
    grid: 'Grid' = field(init=False, repr=False)

    def move(self, n: int = 1) -> Pointer:
        if not self.direction:
            raise ValueError('pointer has no direction')
        dx, dy = self.direction.value
        self.x += n * dx
        self.y += n * dy
        return self

    def look(self, direction: Direction4 = None, n: int = 1) -> str:
        if not direction:
            direction = self.direction

        dx, dy = direction.value
        x = self.x + n * dx
        y = self.y + n * dy
        try:
            value = self.grid[(x, y)]
        except KeyError:
            raise OutOfBounds()
        else:
            return value

    @property
    def coords(self):
        return self.x, self.y

    def place_at(self, x, y):
        self.x = x
        self.y = y

    @property
    def value(self) -> str | None:
        return self.grid.get((self.x, self.y), None)

    @property
    def state(self):
        return self.coords, self.direction, self.value

    def __add__(self, other: Pointer) -> Pointer:
        return Pointer(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Pointer) -> Pointer:
        return Pointer(self.x - other.x, self.y - other.y)

    def __lt__(self, other: Pointer) -> bool:
        return self.x < other.x and self.y < other.y

    def __eq__(self, other: Pointer) -> bool:
        same_coords = self.x == other.x and self.y == other.y
        same_direction = self.direction == other.direction
        return same_coords and same_direction

    def __hash__(self):
        if not self.direction:
            return hash(self.coords + (0, 0))
        return hash(self.coords + self.direction.value)

    @staticmethod
    def adjacent_4(x: int, y: int) -> Generator[tuple[int, int], None, None]:
        yield x, y - 1
        yield x + 1, y
        yield x, y + 1
        yield x - 1, y

    @staticmethod
    def adjacent_8(x: int, y: int) -> Generator[tuple[int, int], None, None]:
        for y_d in (-1, 0, 1):
            for x_d in (-1, 0, 1):
                if y_d == x_d == 0:
                    continue
                yield x + x_d, y + y_d

    def __str__(self) -> str:
        dir_str = f', direction={self.direction.chr!r}' if self.direction else ''
        return f'Pointer(x={self.x}, y={self.y}{dir_str})'

    __repr__ = __str__


@dataclass
class Grid(dict):
    width: int = field(default=0, init=False)
    height: int = field(default=0, init=False)
    pointers: set[Pointer] = field(default_factory=set, init=False)

    def add_pointers(self, *pointers: Pointer) -> None:
        for pointer in pointers:
            pointer.grid = self
            self.pointers.add(pointer)

    @property
    def pointer(self):
        return min(self.pointers)

    @classmethod
    def from_string(cls, s: str, map_fn: callable = str) -> Grid:
        grid = cls()
        for y, line in enumerate(s.splitlines()):
            for x, char in enumerate(line):
                grid[(x, y)] = map_fn(char)
        grid.width, grid.height = x, y
        return grid

    @staticmethod
    def parse_coords_hash(s: str) -> set[tuple[int, int]]:
        """use for walls etc."""
        coords = set()
        for y, line in enumerate(s.splitlines()):
            for x, c in enumerate(line):
                if c == '#':
                    coords.add((x, y))
        return coords

    def __str__(self) -> str:
        with io.StringIO() as s_buff:
            for y in range(self.height + 1):
                for x in range(self.width + 1):
                    print(self[(x, y)], end='', file=s_buff)
                print(file=s_buff)
            return s_buff.getvalue()