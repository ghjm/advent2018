import sys
import datetime
import re

def read_data():
    r = re.compile('([xy])=(\d+), ([xy])=(\d+)..(\d+)')
    clay = list()
    with open('input17.txt', 'r') as f:
        for line in f:
            m = r.match(line)
            dim1, dim1val, dim2, dim2min, dim2max = m.groups()
            c = dict()
            clay.append({
                dim1 + 'min': int(dim1val),
                dim1 + 'max': int(dim1val),
                dim2 + 'min': int(dim2min),
                dim2 + 'max': int(dim2max),
            })
    bounds = {
        'xmin': 500,
        'ymin': sys.maxint,
        'xmax': 500,
        'ymax': -sys.maxint,
    }
    for c in clay:
        for dim in ['x','y']:
            if c[dim+'min'] < bounds[dim+'min']:
                bounds[dim+'min'] = c[dim+'min']
            if c[dim + 'max'] > bounds[dim + 'max']:
                bounds[dim + 'max'] = c[dim + 'max']
    bounds['xmin'] -= 1
    bounds['xmax'] += 1
    return bounds, clay

def make_grid(bounds, clay):
    grid = [['.' for x in range(bounds['xmin'], bounds['xmax'] + 1)] for y in range(0, bounds['ymax'] + 1)]
    for c in clay:
        for y in range(c['ymin'], c['ymax']+1):
            for x in range(c['xmin'], c['xmax'] + 1):
                grid[y][x-bounds['xmin']] = '#'
    grid[0][500-bounds['xmin']] = '+'
    return grid

def print_grid(grid):
    for g in grid:
        print ''.join(g)
        
def c_single(grid, condition, x, y, results):
    tx = x + condition['dx']
    ty = y + condition['dy']
    if tx < 0 or ty < 0 or tx >= len(grid[y]) or ty >= len(grid):
        return False
    return grid[ty][tx] in condition['match']

def c_scanx(grid, condition, x, y, results):
    ty = y + condition['dy']
    if ty < 0 or ty >= len(grid):
        return False
    min_x = sys.maxint
    max_x = -sys.maxint
    for dx in [-1, +1]:
        px = x + dx
        while (px >= 0) and (px < len(grid[ty])):
            if 'end' in condition and grid[ty][px] in condition['end']:
                break
            if 'limits' in condition and px < results[condition['limits']]['min_x']:
                break
            if 'limits' in condition and px > results[condition['limits']]['max_x']:
                break
            if grid[ty][px] not in condition['skip']:
                return False
            if px < min_x:
                min_x = px
            if px > max_x:
                max_x = px
            px = px + dx
        else:
            return False
    return {'min_x': min_x, 'max_x': max_x}

def a_single(grid, action, x, y, results):
    tx = x + action['dx']
    ty = y + action['dy']
    if tx < 0 or ty < 0 or tx >= len(grid[y]) or ty >= len(grid):
        return
    if grid[ty][tx] == action['char']:
        return False
    grid[ty][tx] = action['char']
    return True

def a_fillx(grid, action, x, y, results):
    ty = y + action['dy']
    if ty < 0 or ty >= len(grid):
        return False
    min_x = results[action['scankey']]['min_x']
    max_x = results[action['scankey']]['max_x']
    any_changed = False
    for tx in range(min_x, max_x+1):
        if grid[ty][tx] != action['char']:
            any_changed = True
        grid[ty][tx] = action['char']
    return any_changed

def grid_pour(grid, show=False, progress=False):

    rules = [
        {
            'this_char': {'+', '|'},
            'conditions': [
                (c_single, {'dy': 1, 'dx': 0, 'match': {'.'}}),
            ],
            'actions': [(a_single, {'dy': 1, 'dx': 0, 'char': '|'})]
        },
        {
            'this_char': {'+', '|'},
            'conditions': [
                (c_single, {'dy': 0, 'dx': 1, 'match': {'.'}}),
                (c_single, {'dy': 1, 'dx': 0, 'match': {'#','~'}}),
            ],
            'actions': [(a_single, {'dy': 0, 'dx': 1, 'char': '|'})]
        },
        {
            'this_char': {'+', '|'},
            'conditions': [
                (c_single, {'dy': 0, 'dx': -1, 'match': {'.'}}),
                (c_single, {'dy': 1, 'dx': 0, 'match': {'#','~'}}),
            ],
            'actions': [(a_single, {'dy': 0, 'dx': -1, 'char': '|'})]
        },
        {
            'this_char': {'|'},
            'conditions': [
                (c_single, {'dy': 1, 'dx': 0, 'match': {'#', '~'}}),
                (c_scanx, {'dy': 0, 'skip': {'.', '|'}, 'end': {'#'}}, 'scan'),
                (c_scanx, {'dy': 1, 'skip': {'#', '~'}, 'limits': 'scan'}),
            ],
            'actions': [(a_fillx, {'dy': 0, 'char': '|', 'scankey': 'scan'})]
        },
        {
            'this_char': {'|'},
            'conditions': [
                (c_scanx, {'dy': 0, 'skip': {'|'}, 'end': {'#'}}, 'scan'),
                (c_scanx, {'dy': 1, 'skip': {'#','~'}, 'limits': 'scan'}),
            ],
            'actions': [
                (a_single, {'dy': 0, 'dx': 0, 'char': '~'}),
                (a_fillx, {'dy': 0, 'char': '~', 'scankey': 'scan'}),
            ]
        },
    ]

    changed = True
    progtime = datetime.datetime.now()
    while changed:
        changed = False
        chars_that_matter = set()
        for r in rules:
            chars_that_matter = chars_that_matter.union(r['this_char'])
        for y in range(len(grid)-1):
            for x in range(len(grid[y])):
                if grid[y][x] not in chars_that_matter:
                    continue
                for r in rules:
                    if grid[y][x] not in r['this_char']:
                        continue
                    results = {}
                    for c in r['conditions']:
                        res = c[0](grid, c[1], x, y, results)
                        if not res:
                            break
                        if len(c) == 3:
                            results[c[2]] = res
                    else:
                        for a in r['actions']:
                            if a[0](grid, a[1], x, y, results):
                                changed = True
        if show:
            print_grid(grid)
            print
        if progress and (show or ((datetime.datetime.now() - progtime) > datetime.timedelta(seconds=5))):
            mrr = 0
            for y in range(len(grid)):
                for x in range(len(grid[y])):
                    if grid[y][x] in {'~', '|'}:
                        mrr = y
            print "water has reached row", mrr, "of", len(grid)
            progtime = datetime.datetime.now()
    if progress and not show:
        print_grid(grid)
    return grid

def count_cells(grid, bounds, chars):
    count = 0
    for y in range(len(grid)):
        if y >= bounds['ymin']:
            for x in range(len(grid[y])):
                if grid[y][x] in chars:
                    count += 1
    return count

def main():
    bounds, clay = read_data()
    grid = make_grid(bounds, clay)
    grid_pour(grid, show=False, progress=True)
    print count_cells(grid, bounds, {'~','|'})
    print count_cells(grid, bounds, {'~'})

if __name__ == '__main__':
    main()
