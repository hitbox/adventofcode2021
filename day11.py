from collections import deque

from util import input_filename
from util import iter_table_indexes

_day11_example = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

_day11_middle_octopus = """\
11111
19991
19191
19991
11111"""

def parse_octopus_energy(string):
    return [list(map(int, line)) for line in string.splitlines()]

def adjacent_octopuses(table, row, col):
    # top, top-right, right, bottom-right, bottom, bottom-left, left, top-left
    top = row-1 >= 0
    right = col+1 < len(table[0])
    bottom = row+1 < len(table)
    left = col-1 >= 0
    if top:
        yield row-1, col
    if top and right:
        yield row-1, col+1
    if right:
        yield row, col+1
    if bottom and right:
        yield row+1, col+1
    if bottom:
        yield row+1, col
    if bottom and left:
        yield row+1, col-1
    if left:
        yield row, col-1
    if top and left:
        yield row-1, col-1

def octopus_step(table):
    positions = deque(iter_table_indexes(table))
    flashed = set()
    while positions:
        r, c = positions.pop()
        if (r,c) not in flashed:
            table[r][c] = (table[r][c] + 1) % 10
            if table[r][c] == 0:
                flashed.add((r,c))
                for adjpos in adjacent_octopuses(table, r, c):
                    positions.appendleft(adjpos)

    return flashed

def octopus_flashes(string, steps):
    table = parse_octopus_energy(string)
    flashes = 0
    for _ in range(100):
        flashes += len(octopus_step(table))
    return flashes

def day11_part1():
    """
    Day 11 Part 1
    """
    # smaller example cosidering the middle elements
    middle = parse_octopus_energy(_day11_middle_octopus)
    for _ in range(2):
        octopus_step(middle)
    # copied from page and worked into list-lists
    expect = [[4,5,6,5,4],[5,1,1,1,5],[6,1,1,1,6],[5,1,1,1,5],[4,5,6,5,4]]
    assert middle == expect, f'{middle=} != {expect=}'
    # example
    flashes = octopus_flashes(_day11_example, 100)
    assert flashes == 1656, f'{flashes=} != 1656'
    # challenge
    string = open(input_filename(11)).read()
    flashes = octopus_flashes(string, 100)
    print(f'Day 11 Part 1 Solution: {flashes=}')

def octopus_allflash(table):
    step = 0
    while True:
        octopus_step(table)
        step += 1
        if all(cell == 0 for row in table for cell in row):
            return step

def day11_part2():
    """
    Day 11 Part 2
    """
    # example
    table = parse_octopus_energy(_day11_example)
    step = octopus_allflash(table)
    assert step == 195, f'{step=} != 195'
    # challenge
    string = open(input_filename(11)).read()
    table = parse_octopus_energy(string)
    step = octopus_allflash(table)
    print(f'Day 11 Part 2 Solution: {step=}')
