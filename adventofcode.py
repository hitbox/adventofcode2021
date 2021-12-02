import argparse
import re

from pathlib import Path

def input_filename(day_number):
    return f'inputs/day{day_number:02d}.input.txt'

def nincreasing(numbers):
    "Return the number of increasing numbers"
    return sum(1 for n1, n2 in zip(numbers[:-1], numbers[1:]) if n2 > n1)

def day01_data():
    """
    Lines of text of integers to list of integers.
    """
    with open(input_filename(1)) as fp:
        numbers = [int(line.strip()) for line in fp]
        return numbers

def day01_part1():
    """
    Count of increasing numbers.
    """
    numbers = day01_data()
    n = nincreasing(numbers)
    assert n == 1754, f'{n} != 1754'
    print(f'Day 1 Part 1 Solution: {n}')

def day01_part2():
    """
    Chunk into groups of sliding windows of length three; and then perform
    previous count of increasing numbers.
    """
    numbers = day01_data()
    data = {}
    for offset in range(len(numbers)):
        for index in range(offset, offset+3):
            if index >= len(numbers):
                break
            if offset not in data:
                data[offset] = 0
            data[offset] += numbers[index]
    values = [data[key] for key in sorted(data)]
    n = nincreasing(values)
    assert n == 1789, f'{n} != 1789'
    print(f'Day 1 Part 2 Solution: {n}')

_day_re = re.compile('day\d{2}')

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('day')
    parser.add_argument('part', choices=[1, 2], type=int)
    args = parser.parse_args(argv)

    if not _day_re.match(args.day):
        parser.error(f'command must match pattern {_day_re.pattern}.')

    funcname = f'{args.day}_part{args.part}'
    try:
        func = globals()[funcname]
    except KeyError:
        parser.error(f'command {funcname} not found.')

    func()

if __name__ == '__main__':
    main()
