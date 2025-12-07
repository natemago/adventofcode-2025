def read_input(inpf):
    with open(inpf) as f:
        m = []
        for line in f:
            line = line.strip()
            if not line:
                break
            m.append([c for c in line])
        return m


def count_rolls_around(m, x, y):
    cnt = 0
    for xx, yy in ((x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)):
        if xx < 0 or xx >= len(m[0]) or yy < 0 or yy >= len(m):
            continue
        if m[yy][xx] == '@':
            cnt += 1
    return cnt


def part1(m):
    result = 0
    for y, row in enumerate(m):
        for x, c in enumerate(row):
            if c == '@':
                rolls_count = count_rolls_around(m, x, y)
                if rolls_count < 4:
                    result += 1
    return result

def remove_all_accessible(m):
    to_be_removed = set()
    for y, row in enumerate(m):
        for x, c in enumerate(row):
            if c == '@' and count_rolls_around(m, x, y) < 4:
                to_be_removed.add((x, y))
    
    if len(to_be_removed) == 0:
        return m, 0
    mm = []
    for y, row in enumerate(m):
        nrow = []
        for x, c in enumerate(row):
            if (x, y) in to_be_removed:
                nrow.append('.')
            else:
                nrow.append(c)
        mm.append(nrow)
    return mm, len(to_be_removed)

def part2(m):
    total = 0
    while True:
        m, removed = remove_all_accessible(m)
        print('removed:', removed)
        if removed == 0:
            break
        total += removed
    return total

print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))