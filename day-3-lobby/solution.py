def read_input(inpf):
    with open(inpf) as f:
        banks = []
        for line in f:
            banks.append([int(c) for c in line.strip()])
        return banks

def max_jolts(bank):
    res = 0

    for i, a in enumerate(bank):
        for b in bank[i+1:]:
            jolts = a*10 + b
            if jolts > res:
                res = jolts

    return res


def part1(banks):
    total = 0
    for bank in banks:
        mj = max_jolts(bank)
        total += mj
    return total

def find_max_jolts(sbank, bank_len, from_pos, ndigits, cache):
    if (from_pos, ndigits) in cache:
        return cache[(from_pos, ndigits)]
    for digit, positions in sbank:
        for p in positions:
            if p >= from_pos and p <= (bank_len - ndigits):
                if ndigits == 1:
                    cache[(from_pos, ndigits)] = digit
                    return digit
                
                value = find_max_jolts(sbank, bank_len, p + 1, ndigits - 1, cache)
                if value is not None:
                    best = digit*(10**(ndigits-1)) + value
                    cache[(from_pos, ndigits)] = best
                    return best
    return None

def find_max_jolts_for_bank(bank):
    m = {}
    for i, d in enumerate(bank):
        if m.get(d) is None:
            m[d] = []
        m[d].append(i)
    sbank = sorted(m.items(), reverse=True)
    return find_max_jolts(sbank, len(bank), 0, 12, dict())     

def part2(banks):
    tot = 0
    for bank in banks:
        v = find_max_jolts_for_bank(bank)
        tot += v
    return tot


print('Part 1:', part1(read_input('input')))
print('Part 1:', part2(read_input('input')))