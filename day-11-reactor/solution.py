from collections import deque

def read_input(inpf):
    with open(inpf) as f:
        devices = {}
        for line in f:
            line = line.strip()
            if not line:
                continue
            device, outputs = line.split(':')
            outputs = [n.strip() for n in outputs.split()]
            devices[device] = outputs
        return devices



def part1(devices):
    total = 0
    q = [('you', set())]
    while len(q):
        dev_name, path = q[0]
        q = q[1:]
        if dev_name == 'out':
            total += 1
            continue
        path = path.union(set(dev_name))
        for out_dev in devices[dev_name]:
            if out_dev in path:
                continue
            q.append((out_dev, path))
    
    return total


class G:

    def __init__(self):
        self.vertices = {}
        self.edges = set()
    
    def get(self, vertex):
        return self.vertices[vertex]
    
    def to_dot_file(self, filename):
        with open(filename, 'w') as f:
            f.write('digraph G {\n')
            for v in self.vertices.keys():
                if v in ('you', 'out', 'svr', 'dac', 'fft'):
                    f.write(f'{v} [fillcolor="red", style="filled"];\n')
                else:
                    f.write(f'{v};\n')
            for e in self.edges:
                f.write(f'{e.a.name}->{e.b.name};\n')
            f.write('}\n')


class V:
    
    def __init__(self, name):
        self.name = name
        self.in_edges = []
        self.out_edges = []
    
    def paths_count(self):
        if len(self.in_edges) == 0:
            return 1
        total = 0
        for e in self.in_edges:
            total += e.weight*e.a.paths_count()
        return total
    

class E:

    # Directed edge from a to b
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.weight = None
    

def to_graph(devices):
    g = G()
    for dev, outputs in devices.items():
        if dev not in g.vertices:
            g.vertices[dev] = V(dev)
        for o in outputs:
            if o not in g.vertices:
                g.vertices[o] = V(o)
    
    for dev, outputs in devices.items():
        dv = g.vertices[dev]
        for o in outputs:
            ov = g.vertices[o]
            e = E(dv, ov)
            g.edges.add(E(dv, ov))
            dv.out_edges.append(e)
            ov.in_edges.append(e)
    return g

def all_paths_count(g, start, end, terminals):
    total = 0
    q = deque()
    q.append((start, set()))
    while len(q):
        node, path = q.popleft()
        if node == end:
            total += 1
            continue
        if node in terminals:
            continue
        path = path.union(set([node]))
        for e in node.out_edges:
            nn = e.b
            if nn in path:
                continue
            q.append((nn, path))
    return total

def all_paths_counts_multiple(g, start_nodes, end_nodes, terminals):
    result = {}
    terminals = tuple([g.get(t) for t in terminals])
    for start in start_nodes:
        a = g.get(start)
        for end in end_nodes:
            b = g.get(end)
            count = all_paths_count(g, a, b, terminals)
            print(start, '->', end, '=', count)
            result[(start, end)] = count
    return result

def part2(devices):
    '''Impossible to solve in a generic way (?).
    Generate graphviz of the graph to see where is the bottleneck:
    '''
    g = to_graph(devices)
    g.to_dot_file('graph.dot')
    # Generate the graph PNG
    # dot -Tpng graph.dot > graph.png

    # Multiple bottlenecks present
    paths = {}
    res = all_paths_counts_multiple(g, ('svr',), ('row', 'ovq', 'yky'), ('row', 'ovq', 'yky'))
    print(res)
    paths.update(res)
    res = all_paths_counts_multiple(g, ('row', 'ovq', 'yky'), ('fft',), ('wup', 'izh', 'zap', 'udr'))
    print(res)
    paths.update(res)
    res = all_paths_counts_multiple(g, ('fft',), ('wup', 'izh', 'zap', 'udr'), ('wup', 'izh', 'zap', 'udr'))
    print(res)
    paths.update(res)
    res = all_paths_counts_multiple(g, ('wup', 'izh', 'zap', 'udr'), ('ynx','fqz', 'nrg', 'ebn'), ('ynx','fqz', 'nrg', 'ebn'))
    print(res)
    paths.update(res)
    res = all_paths_counts_multiple(g, ('ynx','fqz', 'nrg', 'ebn'), ('qov', 'lyu', 'keq'), ('qov', 'lyu', 'keq'))
    print(res)
    paths.update(res)
    res = all_paths_counts_multiple(g, ('qov', 'lyu', 'keq'), ('dac',), ('kcj', 'ccx', 'xia', 'rfh', 'you'))
    print(res)
    paths.update(res)
    res = all_paths_counts_multiple(g, ('dac',), ('kcj', 'ccx', 'xia', 'rfh', 'you'), ('kcj', 'ccx', 'xia', 'rfh', 'you'))
    print(res)
    paths.update(res)
    res = all_paths_counts_multiple(g, ('kcj', 'ccx', 'xia', 'rfh', 'you'), ('out',), ('out',))
    print(res)
    paths.update(res)

    # Build graph with paths lengths between bottlenecks
    
    g1 = G()
    for (a, b) in paths.keys():
        if a not in g1.vertices:
            g1.vertices[a] = V(a)
        if b not in g1.vertices:
            g1.vertices[b] = V(b)
    for (a, b), paths_count in paths.items():
        av = g1.get(a)
        bv = g1.get(b)
        e = E(av, bv)
        e.weight = paths_count
        g1.edges.add(e)
        av.out_edges.append(e)
        bv.in_edges.append(e)


    g1.to_dot_file('weights.dot')

    return g1.get('out').paths_count()





print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))