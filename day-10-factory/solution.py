from itertools import combinations
from collections import deque

def read_input(inpf):
    with open(inpf) as f:
        configs = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            state = [c for c in parts[0][1:-1]]
            buttons = []
            for b in parts[1:-1]:
                buttons.append(tuple([int(n.strip()) for n in b[1:-1].split(',')]))
            joltages = tuple([int(n.strip()) for n in parts[-1][1:-1].split(',')])
            configs.append((state, buttons, joltages))
        return configs

def press_buttons(state, buttons):
    state = ['.' for _ in state]
    for btn in buttons:
        for i in btn:
            state[i] = '#' if state[i] == '.' else '.'
    return tuple(state)

def fewer_presses(state, buttons):
    target = tuple(state)
    for k in range(len(buttons)):
        k = k + 1
        #print('Choose', k, 'from', buttons)
        for btns in combinations(buttons, k):
            new_state = press_buttons(state, btns)
            #print('Pressed:', btns, '->', new_state, '(target=',target,') state=', state)
            if new_state == target:
                return k
    return None



def part1(configs):
    total = 0
    for state, buttons, _ in configs:
        print('target:', state, '; buttons=', buttons)
        count = fewer_presses(state, buttons)
        print(' - count=', count)
        total += count
    return total



'''
Part 2:

Let b1, b2, ..., bn be the buttons, and y1, y2, y3, ... ym are the outputs.
We would have some system of linear equations like this

b1 +  0 +  0 + ... + bn  = y1
 0 + b2 +  0 + ... + 0   = y2
 0 +  0 +  0 + ... + 0   = y3
b1 + b2 + b3 + ... + bn  = y4
 0 +  0 +  0 + ... + bn  = y5
...
b1 +  0 +  0 + ....+ bn  = ym

We represent it in matrix form:
b1,  0,  0, ..., bn, y1 
 0, b2,  0, ...,  0, y2
 0,  0,  0, ...,  0, y3
b1, b2, b3, ..., bn, y4
....
b1,  0,  0, ..., bn, ym

All coefficients are 1; we augment the matrix with the outputs.

Then, we calculate the reduced row-echelon form of the matrix, and we end up with:

b1,  0,  0, ..., c1_1*b_n-1, c1_2*n, Y1
 0, b2,  0, ..., c2_1*b_n-1, c2_2*n, Y2
 0,  0, b3, ..., c3_1*b_n-1, c3_2*n, Y3
.. 
 0,  0,  0, ..., cm_1*b_n-1, cm_2*n, Ym

Note that because the matrix is in RREF, every row has exactly one button (b1, b2 etc), everything else is 0 - when the matrix
is square, or we have some parameters left over.
If the matrix is square, then we have a single solution - we just add up Y1 + Y2 + ... Ym.
If the matrix has more variables than row, we end up with some parameters left-over, each with some coefficient.
In that case we rewrite the system in parametric form, for example above:
b1 = Y1 - (c1_1*t1 + c1_2*t2 + ...+ c1_k*tk)
b2 = Y2 - (c2_1*t1 + c2_2*t2 + ...+ c2_k*tk)
b3 = Y3 - (c3_1*t1 + c3_2*t2 + ...+ c3_k*tk)
where b_n-k = t1, b_n-k-1 = t2,..., bn=tk (the parameters)
... etc

It's important to note that the parameters are the same foe every equation.
Another this is to note that there are some constraints on b1, b2, bn can be:
- b_n >= 0 (in general) - we cannot have negative clicks.
- b_n <= min(Y[button_index]) i.e given the outputs y1, y2, ..., ym, the button cannot be pressed more than the smallest output it affects.
  For example, lets say we have these outputs: [4, 5, 2, 7, 5], and b1 affects 0th, 3rd and 4th output i.e (4, 2, 7), then b1 cannot be
  pressed more than min(4, 2, 7) - 2 times. If it were, then the 3rd output would be greater than 2, which would be incorrect.

Next, we start checking combinations for the parameters for each equations starting from the first.
Lets say we have calcuated some equation like this:
b1 + c1*t1 + c2*t2 = Y1
We have 3 variables: b1, t1 and t2; but it's imporant to notice that b1 is completely defined by t1 and t2:
b1 = Y1 - (c1*t1 + c2*t2)
so we only need to calculate all valid combinations for t1 and t2:
 - c1, c2 might not be integers, but they must be rationals
 - t1, t2 have constraints
 - b1 also has constraints
So we calculate all pairs (p1, p2) in which p1 and p2 are integers, and also b1 is integer and also all constraints are satisfied.
We finally would generate all triplets: (b1, p1, p2), adding also the value for b1.

Next, we go to the second equation:
b2 + c3*t2 + c4*t1 = Y2
Similarly we calculate all possible t1 and t2 values within the constraints BUT we only use the valid pairs from the first equation.
We would end up with the same or less pairs as some may not fit the second one. We also calculate b2 and add to the tuples: (b1, b2, p1, p2)

We continue to do this for every equation, in each step decreasing (or keeping the same) the number of possible combinations.
After calcuating the final equations, we end up with tuples of all possible button values:
R = {(b1, b2, b3, ...., bn), ...}
We then find min(sum(t) for t in R)

'''

def part2(configs):
    pass


#print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('test_input')))