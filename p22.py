import sys
import re
import heapq

#depth: 7740
#target: 12,763

def read_data():
    rd = re.compile('depth: (\d+)')
    rt = re.compile('target: (\d+),(\d+)')
    depth = None
    target = None
    with open('input22.txt', 'r') as f:
        for line in f:
            m = rd.match(line)
            if m:
                depth = int(m.groups()[0])
            m = rt.match(line)
            if m:
                target = (int(m.groups()[0]), int(m.groups()[1]))
    if depth is None or target is None:
        print "data is bad"
        sys.exit(-1)
    return depth, target

def calc_erosion(depth, target):
    extra_calc = 10
    erosion_grid = [[0 for x in range(target[0] + extra_calc + 1)] for y in range(target[1] + extra_calc + 1)]
    for y in range(target[1] + extra_calc + 1):
        for x in range(target[0] + extra_calc + 1):
            if x == 0 and y == 0:
                geo = 0
            elif x == target[0] and y == target[1]:
                geo = 0
            elif y == 0:
                geo = x * 16807
            elif x == 0:
                geo = y * 48271
            else:
                geo = erosion_grid[y][x-1] * erosion_grid[y-1][x]
            erosion_grid[y][x] = (geo + depth) % 20183
    return erosion_grid

typechars = {0: '.', 1: '=', 2: '|'}
usable_equip = {0: {'c', 't'}, 1: {'c', 'n'}, 2: {'t', 'n'}}
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_next_states(types_grid, cur_state):
    next_states = list()
    x, y, equip = cur_state
    for ne in usable_equip[types_grid[y][x]] - {equip}:
        next_states.append((7, (x, y, ne)))
    for m in moves:
        nx = x + m[0]
        ny = y + m[1]
        if 0 <= ny < len(types_grid) and 0 <= nx < len(types_grid[0]):
            if equip in usable_equip[types_grid[ny][nx]]:
                next_states.append((1, (nx, ny, equip)))
    return next_states

def find_shortest_path(type_grid, dest):
    start = (0, 0, 't')
    end = (dest[0], dest[1], 't')
    frontier = list()
    heapq.heappush(frontier, (0, start))
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while len(frontier) > 0:
        current = heapq.heappop(frontier)[1]
        if current == end:
            break

        for cost, next in get_next_states(type_grid, current):
            new_cost = cost_so_far[current] + cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + abs(dest[0] - next[0]) + abs(dest[1] - next[1])
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current
    if end not in came_from:
        return None
    from_path = [end]
    while from_path[0] != start:
        from_path = [came_from[from_path[0]]] + from_path
    return from_path, cost_so_far[end]


def main():
    depth, target = read_data()
    # depth = 510
    # target = (10, 10)
    erosion_grid = calc_erosion(depth, target)
    types_grid = [[erosion_grid[y][x] % 3 for x in range(len(erosion_grid[y]))] for y in range(len(erosion_grid))]
    risk = 0
    for y in range(target[1]+1):
        for x in range(target[0]+1):
            risk += types_grid[y][x]
    print 'Part A:', risk
    shortest_path, sp_cost = find_shortest_path(types_grid, target)
    print 'Part B:', sp_cost

if __name__ == '__main__':
    main()
