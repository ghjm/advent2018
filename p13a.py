directions = {
    '^': (0, -1),
    'v': (0, 1),
    '>': (1, 0),
    '<': (-1, 0)
}

direct_next = {
    ('^', '|'): '^',
    ('^', '/'): '>',
    ('^', '\\'): '<',
    ('v', '|'): 'v',
    ('v', '/'): '<',
    ('v', '\\'): '>',
    ('>', '-'): '>',
    ('>', '/'): '^',
    ('>', '\\'): 'v',
    ('<', '-'): '<',
    ('<', '/'): 'v',
    ('<', '\\'): '^'
}

plus_dirs = [
    # left
    {
        '^': '<',
        'v': '>',
        '<': 'v',
        '>': '^'
    },
    # straight
    {
        '^': '^',
        'v': 'v',
        '<': '<',
        '>': '>'
    },
    # right
    {
        '^': '>',
        'v': '<',
        '<': '^',
        '>': 'v'
    }
]

base_map = list()
init_carts = list()

def get_data():
    global base_map
    global init_carts
    with open('input13.txt', 'r') as f:
        y = 0
        for line in f:
            line = line.rstrip()
            base_line = list()
            for x in range(len(line)):
                c = line[x]
                if c in directions:
                    init_carts.append({'xy': (x,y), 'direction': c})
                    if c in ['^','v']:
                        c = '|'
                    else:
                        c = '-'
                base_line.append(c)
            base_map.append(''.join(base_line))
            y += 1

def print_state(carts):
    y = 0
    for line in base_map:
        cart_line = list()
        for x in range(len(line)):
            c = line[x]
            for cart in carts:
                if cart['xy'] == (x,y):
                    c = cart['direction']
            cart_line.append(c)
        print ''.join(cart_line)
        y += 1

def update_state(carts):
    new_carts = list()
    carts_at = set()
    for cart in carts:
        carts_at.add(cart['xy'])
    for cart in sorted(carts, key=lambda c: (c['xy'][1], c['xy'][0])):
        x, y = cart['xy']
        d = cart['direction']
        plus_dir = cart['plus_dir']
        carts_at.remove((x,y))
        dx, dy = directions[d]
        new_x = x + dx
        new_y = y + dy
        if (new_x, new_y) in carts_at:
            return 'Crash', (new_x, new_y)
        carts_at.add((new_x, new_y))
        if base_map[new_y][new_x] == '+':
            new_direction = plus_dirs[plus_dir][d]
            plus_dir = (plus_dir + 1) % len(plus_dirs)
        else:
            new_direction = direct_next[(d, base_map[new_y][new_x])]
        new_carts.append({'xy': (new_x, new_y), 'direction': new_direction, 'plus_dir': plus_dir})
    return new_carts

def run_race(show=True):
    carts = list()
    for cart in init_carts:
        carts.append({'xy': cart['xy'], 'direction': cart['direction'], 'plus_dir': 0})
    step = 0
    while True:
        step += 1
        if show:
            print_state(carts)
        carts = update_state(carts)
        if carts[0] == 'Crash':
            print 'Crash at', carts[1], 'at step', step
            break

def main():
    get_data()
    run_race(show=False)

if __name__ == '__main__':
    main()
