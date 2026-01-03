import re


def read_input(inpf):
    with open(inpf) as f:
        shape = []
        shape_id = None
        polygons = []
        shapes = {}
        for line in f:
            line = line.strip()
            if not line:
                continue
            if re.match(r'^\d:$', line):
                shape_id = int(line[0])
            elif line[0] in '.#':
                shape.append(line)
                if len(shape) == len(shape[0]):
                    shapes[shape_id] = shape
                    shape_id = None
                    shape = []
            elif re.match(r'^\d+x\d+:.+$', line):
                p_size, amounts = line.split(':')
                m, n = p_size.split('x')
                m, n = int(m), int(n)
                amounts = [int(v) for v in amounts.split()]
                polygons.append(((m, n), amounts))
        return shapes, polygons


def shape_size(shape):
    count = 0
    for r in shape:
        for c in r:
            if c == '#':
                count += 1
    return count

def part1(shapes, polygons):
    does_not_fit = 0
    for (m, n), amounts in polygons:
        total_size = 0
        for i, v in enumerate(amounts):
            total_size += shape_size(shapes[i])*v
        if total_size > (m*n):
            does_not_fit += 1
    
    # Maybe lucky
    return len(polygons) - does_not_fit



print('Part 1:', part1(*read_input('input')))