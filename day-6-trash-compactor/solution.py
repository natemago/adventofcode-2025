from functools import reduce

def read_input(inpf):
    with open(inpf) as f:
        rows = []
        operations = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if '+' in line or '*' in line:
                operations = line.split()
            else:
                rows.append([int(i) for i in line.split()])
        return rows, operations


OPS = {
    '+': (lambda a, n: a+n, 0),
    '*': (lambda a, n: a*n, 1),
}


class Spreadsheet:

    def __init__(self, rows, operations):
        self.rows = rows
        self.operations = operations
        row_len = len(self.rows[0])
        for row in rows:
            assert row_len == len(row)
        assert len(operations) == row_len
    
    def column(self, col):
        for row in self.rows:
            yield row[col]

    def reduce_column(self, col):
        op, initial = OPS[self.operations[col]]
        return reduce(op, self.column(col), initial)


def part1(rows, operations):
    sheet = Spreadsheet(rows, operations)
    total = 0
    for i in range(len(rows[0])):
        total += sheet.reduce_column(i)
    return total

def part2(inpf):
    matrix = []
    with open(inpf) as f:
        for line in f:
            if not line:
                break
            matrix.append(line)
    row_len = len(matrix[0])
    for row in matrix:
        assert row_len == len(row)

    total = 0
    i = row_len - 1
    numbers = []
    while i >= 0:
        number = ''
        op = None
        for r in range(len(matrix)):
            c = matrix[r][i]
            if c in ' \n\t\r':
                continue
            if c in '+*':
                op = c
                break
            number += c
        if number:
            numbers.append(int(number))
        if op is not None:
            opf, initial = OPS[op]
            total += reduce(opf, numbers, initial)
            numbers = []
            number = ''
            op = None
        i -= 1
    return total


print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2('input'))