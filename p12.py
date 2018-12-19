import sys
import re

init = None
rules = None

def get_data():
    global init
    global rules
    r_init = re.compile('initial state: ([.#]+)')
    r_rule = re.compile('([.#]{5}) => ([.#])')
    rules = dict()
    with open('input12.txt', 'r') as f:
        for line in f:
            m = r_init.match(line)
            if m:
                init = m.groups()[0]
                continue
            m = r_rule.match(line)
            if m:
                rules[m.groups()[0]] = m.groups()[1]
                continue
    return init, rules

def check_rules(s):
    if s in rules:
        return rules[s]
    else:
        return '.'

def next_gen(left, prev):
    prev_adj = '.....' + prev + '.....'
    left -= 3
    new = ''.join([check_rules(prev_adj[i:i+5]) for i in range(0, len(prev_adj)-5)])
    while len(new) >= 1 and new[0] == '.':
        new = new[1:]
        left += 1
    while len(new) >= 1 and new[len(new)-1] == '.':
        new = new[:-1]
    return left, new

def calc_pot_sum(left, pots):
    ps = 0
    for i in range(len(pots)):
        if pots[i] == '#':
            ps += i + left
    return ps

def main_parta(generations=20, show=True, ret_last=False):
    states = [(0, init)]
    for i in range(1, generations+1):
        left, pots = states[-1]
        left, pots = next_gen(left, pots)
        states.append((left, pots))
    if show:
        min_left = sys.maxint
        max_right = -sys.maxint
        for i in range(len(states)):
            left, pots = states[i]
            right = left + len(pots)
            if left < min_left:
                min_left = left
            if right > max_right:
                max_right = right
        for i in range(len(states)):
            left, pots = states[i]
            print '.' * (left - min_left) + pots + '.' * (max_right - left - len(pots))
    if ret_last:
        left, pots = states[-1]
        pot_sum = calc_pot_sum(left, pots)
        left, pots = states[-2]
        last_pot_sum = calc_pot_sum(left, pots)
        return pot_sum, last_pot_sum
    else:
        left, pots = states[-1]
        return calc_pot_sum(left, pots)

def main_partb():
    # Run to convergence
    converge_steps = 10000
    pot_sum, last_pot_sum = main_parta(generations=converge_steps, show=False, ret_last=True)
    # Interpolate the rest
    step_diff = pot_sum - last_pot_sum
    return pot_sum + (50000000000 - converge_steps) * step_diff

if __name__ == '__main__':
    get_data()
    print main_parta()
    print main_partb()
