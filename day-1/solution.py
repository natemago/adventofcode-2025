import pyxel

def read_input(inp):
    with open(inp) as f:
        rotations = []
        for line in f:
            steps = int(line[1:])
            if line.startswith('L'):
                steps *= -1
            rotations.append(steps)
        return rotations

def part1(rotations):
    zeroes = 0
    position = 50
    for steps in rotations:
        position = (position + steps) % 100
        if position == 0:
            zeroes += 1
    return zeroes


def part2(rotations):
    zeroes = 0
    position = 50
    for steps in rotations:
        inc = 1 if steps > 0 else -1
        for i in range(0, abs(steps)):
            position = (position + inc) % 100
            if position == 0:
                zeroes += 1

    return zeroes

def update():
    pass

def draw():
    pyxel.circ(60, 60, 60, 4)

pyxel.init(120, 120, title='Secret Entrance')

pyxel.run(update, draw)


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))