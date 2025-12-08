def read_input(inpf):
    with open(inpf) as f:
        ranges = []
        ingredients = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if '-' in line:
                a, b = line.split('-')
                ranges.append((int(a), int(b)))
            else:
                ingredients.append(int(line))
        
        return ranges, ingredients


class Range:

    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def point_within(self, n):
        return n >= self.a and n <= self.b
    
    def mag(self):
        return self.b - self.a + 1
    
    def __repr__(self):
        return str([self.a, self.b])
    
    def __str__(self):
        return self.__repr__()
    

def can_merge(r1, r2):
    return r1.point_within(r2.a) or r1.point_within(r2.b) or r2.point_within(r1.a) or r2.point_within(r1.b)
    
def merge(r1, r2):
    return Range(min(r1.a, r2.a), max(r1.b, r2.b))

def part1(ranges, ingredients):
    ranges = [Range(a,b) for a,b in ranges]
    total = 0
    for n in ingredients:
        for r in ranges:
            if r.point_within(n):
                total += 1
                break
    return total


def part2(ranges, ingredients):
    ranges = sorted([Range(a,b) for a,b in ranges], key=lambda r: r.b)
    total = 0
    r1 = ranges[0]
    for r2 in ranges[1:]:
        if can_merge(r1, r2):
            r1 = merge(r1, r2)
        else:
            total += r1.mag()
            r1 = r2
    total += r1.mag()
    
    return total


print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))