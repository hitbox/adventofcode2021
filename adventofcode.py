import argparse
import re

from pathlib import Path

def input_filename(day_number):
    path = Path('inputs') / f'day{day_number:02d}.input.txt'
    return path

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
    for window in range(len(numbers)):
        for index in range(window, window+3):
            if index >= len(numbers):
                break
            if window not in data:
                data[window] = 0
            data[window] += numbers[index]
    values = [data[key] for key in sorted(data)]
    n = nincreasing(values)
    assert n == 1789, f'{n} != 1789'
    print(f'Day 1 Part 2 Solution: {n}')

def day02_data():
    with open(input_filename(2)) as fp:
        instructions = (line.split() for line in fp)
        instructions = [(dir, int(num)) for dir, num in instructions]
        return instructions

def navigate_submarine(instructions):
    """
    Map instructions to attributes of position and apply magnitude.
    """
    pos = {'h': 0, 'd': 0}
    map = {'forward': ('h', 1), 'down': ('d', 1), 'up': ('d', -1)}
    for direction, magnitude in instructions:
        attr, scale = map[direction]
        pos[attr] += scale * magnitude
    return pos

_day02_test = [('forward', 5), ('down', 5), ('forward', 8), ('up', 3), ('down', 8), ('forward', 2)]

def day02_part1():
    "Day 2 part 1 sample and challenge."
    pos = navigate_submarine(_day02_test)
    n = pos['h'] * pos['d']
    assert n == 150, f'{n} != 105'

    pos = navigate_submarine(day02_data())
    n = pos['h'] * pos['d']
    assert n == 1692075
    print(f'Day 2 Part 1 Solution: {n}')

def navigate_submarine2(instructions):
    "More complicated submarine instruction application with 'aim' (a)."
    pos = {'h': 0, 'd': 0, 'a': 0}
    for direction, mag in instructions:
        if direction == 'down':
            pos['a'] += mag
        elif direction == 'up':
            pos['a'] -= mag
        elif direction == 'forward':
            pos['h'] += mag
            pos['d'] += pos['a'] * mag
        # NOTE: thought about the new match statement here, but all it does is
        #       add extra indent.
    return pos

def day02_part2():
    "Day 2 part 2 sample and challenge."
    pos = navigate_submarine2(_day02_test)
    n = pos['h'] * pos['d']
    assert n == 900, f'{n} != 900'

    pos = navigate_submarine2(day02_data())
    n = pos['h'] * pos['d']
    assert n == 1749524700
    print(f'Day 2 Part 1 Solution: {n}')

def day03_data():
    with open(input_filename(3)) as fp:
        return [int('0b' + line.strip(), base=2) for line in fp]

def count_of(iterable):
    d = {}
    for value in iterable:
        if value not in d:
            d[value] = 0
        d[value] += 1
    return d

def mkmasks(nbits):
    masks = [1 << shift for shift in range(nbits)]
    return masks

def power_consumption(bnums, nbits):
    masks = mkmasks(nbits)
    # "first bit" in challenge refers to least significant bit (right-most).
    as_rows = [[int((bnum & mask) != 0) for mask in masks] for bnum in bnums]
    as_cols = list(zip(*as_rows))
    as_cols_count = [count_of(col) for col in as_cols]

    gamma_bits = [max(counts, key=lambda key: counts[key]) for counts in as_cols_count]
    epsilon_bits = [min(counts, key=lambda key: counts[key]) for counts in as_cols_count]

    gamma = int('0b' + ''.join(map(str, reversed(gamma_bits))), base=2)
    epsilon = int('0b' + ''.join(map(str, reversed(epsilon_bits))), base=2)
    solution = gamma * epsilon
    return solution

def day03_part1():
    "Day 3 part 1"
    # sample
    bnums = [
        0b00100,
        0b11110,
        0b10110,
        0b10111,
        0b10101,
        0b01111,
        0b00111,
        0b11100,
        0b10000,
        0b11001,
        0b00010,
        0b01010,
    ]
    solution = power_consumption(bnums, 5)
    assert solution == 198, f'{solution} != 198'

    bnums = day03_data()
    solution = power_consumption(bnums, 12)
    assert solution == 4160394, f'{solution} != 4160394'
    print(f'Day 3 Part 1 Solution: {solution}')

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
