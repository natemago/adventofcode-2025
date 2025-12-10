def read_input(inpf):
    with open(inpf) as f:
        tiles = []
        for line in f:
            if not line.strip():
                continue
            x, y = [int(n.strip()) for n in line.split(',')]
            tiles.append(Point(x, y))
        return tiles

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rect_area(self, p):
        return (abs(self.x - p.x)+1) * (abs(self.y - p.y)+1)
    
    def rect_points(self, p):
        return (
            self,
            p,
            Point(self.x, p.y),
            Point(p.x, self.y),
        )
    
    def __repr__(self):
        return f'({self.x}, {self.y})'
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, o):
        if not isinstance(o, Point):
            return False
        return self.x == o.x and self.y == o.y
    
    def __hash__(self):
        return hash((self.x, self.y))

def within_rect(r1, r2, p):
    x1, x2 = min(r1.x, r2.x), max(r1.x, r2.x)
    y1, y2 = min(r1.y, r2.y), max(r1.y, r2.y)
    return p.x > x1 and p.x < x2 and p.y > y1 and p.y < y2


def part1(tiles):
    max_area = 0
    for i, p1 in enumerate(tiles[0:-1]):
        for p2 in tiles[i+1:]:
            area = p1.rect_area(p2)
            if area >= max_area:
                max_area = area
    return max_area




def part2(tiles):
    tiles = sorted(sorted(tiles, key=lambda p: p.x), key=lambda p: p.y)

    per_row = {}
    per_col = {}

    for t in tiles:
        per_row[t.y] = sorted(per_row.get(t.y, []) + [t], key=lambda p: p.x)
        per_col[t.x] = sorted(per_col.get(t.x, []) + [t], key=lambda p: p.y)

    def find_per_row(p, path):
        tls = per_row.get(p.y, [])
        if len(tls) == 0:
            return []
        i = 0
        while i < len(tls):
            if tls[i] not in path and p.x >= tls[i].x:
                break
            i += 1
        if i >= len(tls):
            return [tls[-1]]
        c = tls[i]
        results = []
        if c == p:
            if i > 0 and tls[i-1] not in path:
                results.append(tls[i-1])
            if i < len(tls) - 1 and tls[i+1] not in path:
                results.append(tls[i+1])
        else:
            if tls[i] not in path:
                results.append(tls[i])
            if i > 0 and tls[i-1] not in path:
                results.append(tls[i-1])
        return results
    
    def find_per_col(p, path):
        tls = per_col.get(p.x, [])
        if len(tls) == 0:
            return []
        i = 0
        while i < len(tls):
            if tls[i] not in path and p.y >= tls[i].y:
                break
            i += 1
        if i >= len(tls):
            return [tls[-1]]
        c = tls[i]
        results = []
        if c == p:
            if i > 0 and tls[i-1] not in path:
                results.append(tls[i-1])
            if i < len(tls) - 1 and tls[i+1] not in path:
                results.append(tls[i+1])
        else:
            if tls[i] not in path:
                results.append(tls[i])
            if i > 0 and tls[i-1] not in path:
                results.append(tls[i-1])
        return results
    
    def find_next(p, path):
        return find_per_col(p, path) + find_per_row(p, path)

    for t in tiles:
        print(t, '->', find_per_row(t, []), find_per_col(t, []))
        print('   -', find_next(t, []))
        print('   - per row:', per_row[t.y])
        print('   - per col:', per_col[t.x])
    
    #return
    start = tiles[0]
    q = [(start, [])]
    final_path = None
    while len(q):
        p, path = q[0]
        q = q[1:]
        candidates = find_next(p, path)
        #print(p, ' candidates:', candidates, '; path:', path, '; ', len(tiles), ', ', len(path))
        if len(path) == len(tiles) - 1:
            if p.x == start.x or p.y == start.y:
                #print('Found path:', path + [p])
                final_path = path + [p]
                break
        # if len(candidates) == 0:
        #     print('start:', start)
        #     print('path:', path)
        #     print('p=', p)
        #     print(' row:', per_row[p.y])
        #     for pp in per_row[p.y]:
        #         print('  ', pp, ' in path:', pp in path)
        #     print(' col:', per_col[p.x])
        #     for pp in per_col[p.x]:
        #         print('  ', pp, ' in path:', pp in path)
        #     input('[]')
        for n in candidates:
            #print('  - going from', p, '->', n)
            q.append((n, path + [p]))
    print('final path:', final_path)
    final_path += [start]
    rectangles = []
    max_area = 0
    for i, p1 in enumerate(final_path):
        p2 = final_path[(i+2)%len(final_path)]
        good = True
        for t in tiles:
            if p1 == t or p2 == t:
                continue
            if within_rect(p1, p2, t):
                good = False
                break
        if good:
            area = p1.rect_area(p2)
            if area > max_area:
                max_area = area

    xxs, yys = [],[]
    for t in tiles:
        xxs.append(t.x)
        yys.append(t.y)
    print(min(xxs), max(xxs), min(yys), max(yys), '; total area=', (max(xxs) - min(xxs)) *(max(yys) - min(yys)))

    return max_area
                


print('Part 1:', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))