def read_input(inpf):
    with open(inpf) as f:
        grid = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            grid.append([c for c in line])
        return grid

def print_grid(grid):
    for row in grid:
        print(''.join(row))


def part1(grid):
    beam_split = 0
    for y, row in enumerate(grid):
        if y == 0:
            continue
        for x, c in enumerate(row):
            if y == 1 and grid[y-1][x] == 'S':
                print('Start at', (x, y))
                grid[y][x] = '|'
                continue
            if c == '^' and grid[y-1][x] == '|':
                print('Beam split at:', (x, y))
                grid[y][x-1] = '|'
                grid[y][x+1] = '|'
                beam_split += 1
            if c == '.' and grid[y-1][x] == '|':
                grid[y][x] = '|'
    return beam_split


def part2(grid):
    beam_pos = {}
    for y, row in enumerate(grid):
        if y == 0:
            continue
        for x, c in enumerate(row):
            if y == 1 and grid[y-1][x] == 'S':
                beam_pos[(x,y)] = 1
            if c == '^' and (x, y-1) in beam_pos:
                beam_pos[(x-1, y)] = beam_pos.get((x-1, y), 0) + beam_pos[(x, y-1)]
                beam_pos[(x+1, y)] = beam_pos.get((x+1, y), 0) + beam_pos[(x, y-1)]
            if c == '.' and (x, y-1) in beam_pos:
                beam_pos[(x, y)] = beam_pos.get((x, y), 0) + beam_pos[(x, y-1)]
    total_worldlines = 0
    for (x,y), world_lines in beam_pos.items():
        if y == (len(grid) - 1):
            total_worldlines += world_lines
    return total_worldlines


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))