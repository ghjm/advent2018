import sys

dirs = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0),
}

opposites = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E',
}

doors = {
    'N': '-',
    'S': '-',
    'E': '|',
    'W': '|',
}

def opposite(xy):
    return tuple(-1 * z for z in xy)

def read_data():
    with open('input20.txt', 'r') as f:
        line = f.readline().rstrip()
    return line

empty_space = [
    (-1, -1, '#'),
    (-1, 1, '#'),
    (1, -1, '#'),
    (1, 1, '#'),
    (0, 1, '?'),
    (0, -1, '?'),
    (1, 0, '?'),
    (-1, 0, '?'),
]

def find_limits(nodes):
    min_x = min_y = sys.maxint
    max_x = max_y = -sys.maxint
    for k in nodes:
        x, y = k
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    return min_x, max_x, min_y, max_y


def print_nodes(nodes, final=True):
    min_x, max_x, min_y, max_y = find_limits(nodes)

    def xy_to_gridxy(xy):
        gx = (xy[0] - min_x) * 2 + 1
        gy = (xy[1] - min_y) * 2 + 1
        return gx, gy

    grid = [['.' for x in range((max_x-min_x+1)*2+1)] for y in range((max_y-min_y+1)*2+1)]
    x, y = xy_to_gridxy((0, 0))
    grid[y][x] = 'X'
    for n in nodes:
        x, y = xy_to_gridxy(n)
        for dx, dy, ch in empty_space:
            grid[y+dy][x+dx] = ch
    for n in nodes:
        x, y = xy_to_gridxy(n)
        for d in nodes[n]:
            dx, dy = dirs[d]
            grid[y+dy][x+dx] = doors[d]
    if final:
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == '?':
                    grid[y][x] = '#'

    for g in grid:
        print ''.join(g)


def find_furthest(nodes):
    min_x, max_x, min_y, max_y = find_limits(nodes)

    def xy_to_gridxy(xy):
        return xy[0] - min_x, xy[1] - min_y

    grid = [[None for x in range(min_x, max_x+1)] for y in range(min_y, max_y+1)]
    gx, gy = xy_to_gridxy((0, 0))
    grid[gy][gx] = 0
    open_list = [(0, 0)]
    while len(open_list) > 0:
        x, y = open_list.pop(0)
        gx, gy = xy_to_gridxy((x, y))
        dist = grid[gy][gx]
        for dx, dy in (dirs[d] for d in nodes[(x, y)]):
            nx = x + dx
            ny = y + dy
            ngx, ngy = xy_to_gridxy((nx, ny))
            if grid[ngy][ngx] is None or (dist+1) < grid[ngy][ngx]:
                grid[ngy][ngx] = dist + 1
                open_list.append((nx, ny))
    max_dist = 0
    num_1000 = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            g = grid[y][x]
            if g > max_dist:
                max_dist = g
            if g >= 1000:
                num_1000 += 1
    return max_dist, num_1000

def main():
    line = read_data()
    cur_pos = (0, 0)
    nodes = {cur_pos: set()}
    bases = [cur_pos]
    for ch in line:
        if ch in dirs:
            next_pos = tuple(cur_pos[i] + dirs[ch][i] for i in [0, 1])
            if next_pos not in nodes:
                nodes[next_pos] = set()
            nodes[cur_pos].add(ch)
            nodes[next_pos].add(opposites[ch])
            cur_pos = next_pos
        elif ch == '|':
            cur_pos = bases[-1]
        elif ch == '(':
            bases.append(cur_pos)
        elif ch == ')':
            bases.pop()
    print_nodes(nodes)
    print find_furthest(nodes)

if __name__ == '__main__':
    main()
