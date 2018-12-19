import sys
import uuid
import heapq

def parse_map(elfmap):
    basemap = list()
    fighters = list()
    for y in range(len(elfmap)):
        new_line = list()
        for x in range(len(elfmap[y])):
            c = elfmap[y][x]
            if c == 'E' or c == 'G':
                fighters.append({
                    'id': uuid.uuid4(),
                    'type': c,
                    'xy': (x, y),
                    'hit_points': 200,
                    'attack_strength': 3
                })
                new_line.append('.')
            else:
                new_line.append(c)
        basemap.append(''.join(new_line))
    return basemap, fighters


def print_elfmap(basemap, fighters):
    for y in range(len(basemap)):
        line = list()
        stats = list()
        for x in range(len(basemap[y])):
            c = basemap[y][x]
            for fighter in fighters:
                if fighter['xy'] == (x, y) and 'dead' not in fighter:
                    c = fighter['type']
                    stats.append(fighter['type'] + '(' + str(fighter['hit_points']) + ')')
            line.append(c)
        print ''.join(line), ' ', ', '.join(stats)


def adjacent(xy):
    x, y = xy
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def is_empty(basemap, xy, blocklist):
    x, y = xy
    if y < 0 or y > len(basemap):
        return False
    if x < 0 or x > len(basemap[y]):
        return False
    if basemap[y][x] != '.':
        return False
    if xy in blocklist:
        return False
    return True


def is_adjacent(xy1, xy2):
    return xy1 in set(adjacent(xy2))


def find_closest(basemap, blocklist, start, dests):
    distances = dict()
    open_list = [p for p in adjacent(start) if is_empty(basemap, p, blocklist)]
    cur_dist = 1
    while len(open_list) > 0:
        ool = open_list
        open_list = list()
        for xy in ool:
            if xy not in distances:
                distances[xy] = cur_dist
                open_list.extend([p for p in adjacent(xy) if p not in distances and is_empty(basemap, p, blocklist)])
        cur_dist += 1
    dists = [distances[k] for k in dests if k in distances]
    if len(dists) == 0:
        return sys.maxint, None
    min_dist = min(dists)
    min_dist_dests = [k for k in dests if k in distances and distances[k] == min_dist]
    return min_dist, sorted(min_dist_dests, key=lambda p: (p[1], p[0]))[0]


def find_shortest_path(basemap, blocklist, start, dest):
    empty_set = set()
    for y in range(len(basemap)):
        for x in range(len(basemap[y])):
            if is_empty(basemap, (x,y), blocklist):
                empty_set.add((x,y))

    frontier = list()
    heapq.heappush(frontier, (0, start))
    came_from = dict()
    distances = dict()
    came_from[start] = None
    distances[start] = 0

    while len(frontier) > 0:
        current = heapq.heappop(frontier)[1]
        if current == dest:
            break
        for next_step in [p for p in adjacent(current) if p in empty_set]:
            new_distance = distances[current] + 1
            if next_step not in distances or new_distance < distances[next_step]:
                distances[next_step] = new_distance
                priority = new_distance + abs(dest[0]-next_step[0]) + abs(dest[1]-next_step[1])
                heapq.heappush(frontier, (priority, next_step))
                came_from[next_step] = current

    if dest not in came_from:
        return None
    from_path = [dest]
    while from_path[0] != start:
        from_path = [came_from[from_path[0]]] + from_path
    return from_path


def play(elfmap, show=False, elfdeath=False, elfstrength=None):
    basemap, fighters = parse_map(elfmap)
    if elfstrength is not None:
        for i in range(len(fighters)):
            if fighters[i]['type'] == 'E':
                fighters[i]['attack_strength'] = elfstrength
    if show:
        print_elfmap(basemap, fighters)

    step = 0
    finished = False
    while not finished:
        if show:
            print step
        fighters = sorted(fighters, key=lambda f: (f['xy'][1], f['xy'][0]))
        for i in range(len(fighters)):
            if 'dead' in fighters[i]:
                continue
            targets = [enemy for enemy in fighters if 'dead' not in enemy and enemy['type'] != fighters[i]['type']]
            if len(targets) == 0:
                finished = True
                break
            adjacent_targets = [enemy for enemy in targets if is_adjacent(fighters[i]['xy'], enemy['xy'])]
            if len(adjacent_targets) == 0:
                blocklist = set([f['xy'] for f in fighters if 'dead' not in f])
                open_squares = set()
                for target in targets:
                    for txy in adjacent(target['xy']):
                        if is_empty(basemap, txy, blocklist):
                            open_squares.add(txy)
                if len(open_squares) > 0:
                    min_dist, dest = find_closest(basemap, blocklist, fighters[i]['xy'], open_squares)
                    if dest is not None:
                        possible_first_steps = dict()
                        for nxy in adjacent(fighters[i]['xy']):
                            if nxy == dest:
                                possible_first_steps = {1: {nxy}}
                                break
                            if is_empty(basemap, nxy, blocklist):
                                path = find_shortest_path(basemap, blocklist, nxy, dest)
                                if path is not None:
                                    if len(path) not in possible_first_steps:
                                        possible_first_steps[len(path)] = {path[0]}
                                    else:
                                        possible_first_steps[len(path)].add(path[0])
                        if possible_first_steps:
                            min_k = min(possible_first_steps.keys())
                            first_step = sorted(possible_first_steps[min_k], key=lambda p: (p[1], p[0]))[0]
                            fighters[i]['xy'] = first_step
                            adjacent_targets = [enemy for enemy in targets if is_adjacent(fighters[i]['xy'], enemy['xy'])]
            if len(adjacent_targets) > 0:
                low_hp = min([enemy['hit_points'] for enemy in adjacent_targets])
                low_hp_targets = [enemy for enemy in adjacent_targets if enemy['hit_points'] == low_hp]
                selected_target = sorted(low_hp_targets, key=lambda f: (f['xy'][1], f['xy'][0]))[0]
                target_index = None
                for j in range(len(fighters)):
                    if fighters[j]['id'] == selected_target['id']:
                        target_index = j
                        break
                fighters[target_index]['hit_points'] -= fighters[i]['attack_strength']
                if fighters[target_index]['hit_points'] <= 0:
                    fighters[target_index]['dead'] = True
                    if elfdeath and fighters[target_index]['type'] == 'E':
                        return False
        else:
            step += 1
        if show:
            print_elfmap(basemap, fighters)
    remaining_hp = sum([f['hit_points'] for f in fighters if 'dead' not in f])
    return step * remaining_hp


def search_elfstrength(elfmap):
    estr = 3
    while True:
        estr += 1
        print "Trying", estr
        result = play(elfmap, show=False, elfdeath=True, elfstrength=estr)
        if result:
            break
    return result


def main():
    with open('input15.txt', 'r') as f:
        elfmap = list()
        for line in f:
            line = line.rstrip()
            if line == '---':
                play(elfmap)
                elfmap = list()
            else:
                elfmap.append(line)
        if len(elfmap) > 0:
            r = play(elfmap, show=True)
            print 'Part A:', r
            s = search_elfstrength(elfmap)
            print 'Part B:', s


if __name__ == '__main__':
    main()
