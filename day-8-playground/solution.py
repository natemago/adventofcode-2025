def read_input(inpf):
    with open(inpf) as f:
        points = []
        for line in f:
            if not line.strip():
                continue
            x,y,z = [int(n.strip()) for n in line.split(',')]
            points.append(P(x,y,z))
        return points


class P:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def distance_squared(self, p):
        return (self.x - p.x)**2 + (self.y-p.y)**2 + (self.z-p.z)**2


def part1(points):
    print('points:', len(points))
    pairs = []
    for i, p1 in enumerate(points[0:-1]):
        for p2 in points[i+1:]:
            pairs.append((p1, p2, p1.distance_squared(p2)))
    pairs = sorted(pairs, key=lambda p: p[2])
    print('pairs:', len(pairs))

    circuits = []

    def find(p):
        for i, c in enumerate(circuits):
            if p in c:
                return i
        return None
    
    for (p1, p2, _) in pairs[0:1000]:
        p1i = find(p1)
        p2i = find(p2)
        if p1i is None and p2i is None:
            # new circuit
            circuits.append(set([p1, p2]))
        if p1i is not None and p2i is None:
            # add p2 to p1 circuit
            circuits[p1i].add(p2)
        if p2i is not None and p1i is None:
            # add p1 to p2 circuit
            circuits[p2i].add(p1)
        if p1i is not None and p2i is not None:
            # merge the two circuits
            if p1i == p2i:
                # same circuit - do nothing
                continue
            p2c = circuits[p2i]
            circuits[p1i] = circuits[p1i].union(p2c)
            circuits = circuits[0:p2i] + circuits[p2i+1:]
            
    print('circuits:', len(circuits))
    circuits = sorted(circuits, key=lambda c: len(c), reverse=True)
    return len(circuits[0]) * len(circuits[1]) * len(circuits[2])

def part2(points):
    print('points:', len(points))
    pairs = []
    for i, p1 in enumerate(points[0:-1]):
        for p2 in points[i+1:]:
            pairs.append((p1, p2, p1.distance_squared(p2)))
    pairs = sorted(pairs, key=lambda p: p[2])
    print('pairs:', len(pairs))

    circuits = []

    def find(p):
        for i, c in enumerate(circuits):
            if p in c:
                return i
        return None
    
    for (p1, p2, _) in pairs:
        p1i = find(p1)
        p2i = find(p2)
        if p1i is None and p2i is None:
            # new circuit
            circuits.append(set([p1, p2]))
        if p1i is not None and p2i is None:
            # add p2 to p1 circuit
            circuits[p1i].add(p2)
        if p2i is not None and p1i is None:
            # add p1 to p2 circuit
            circuits[p2i].add(p1)
        if p1i is not None and p2i is not None:
            # merge the two circuits
            if p1i == p2i:
                # same circuit - do nothing
                continue
            p2c = circuits[p2i]
            circuits[p1i] = circuits[p1i].union(p2c)
            circuits = circuits[0:p2i] + circuits[p2i+1:]
        if len(circuits) == 1 and len(circuits[0]) == len(points):
            return p1.x * p2.x

print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))