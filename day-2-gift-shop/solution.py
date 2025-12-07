from math import ceil

def read_input(inpf):
    with open(inpf) as f:
        ranges = []
        for range_str in f.read().split(','):
            start,end = range_str.strip().split('-')
            start, end = int(start), int(end)
            ranges.append((start, end))
        return ranges

def only_repeating(part, num):
    for i in range(0, int(ceil(len(num)/len(part)))):
        if not num[i*len(part):].startswith(part):
            return False
    return True

def is_valid_id(num):
    num = str(num)
    if len(num) <= 1:
        return True
    for i in range(1, len(num)//2 + 1):
        if only_repeating(num[0: i], num):
            return False
    return True

def is_valid_id_not_repeated_twice(num):
    num = str(num)
    if len(num) % 2 == 1:
        return True
    return num[0:len(num)//2] != num[len(num)//2:]


def part1(ranges):
    total = 0
    for a, b in ranges:
        for i in range(a, b+1):
            if not is_valid_id_not_repeated_twice(i):
                print('Invalid:', i)
                total += i
    return total

def part2(ranges):
    total = 0
    for a, b in ranges:
        for i in range(a, b+1):
            if not is_valid_id(i):
                print('Invalid:', i)
                total += i
    return total

#print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))