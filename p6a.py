coords = list()
with open('input6.txt', 'r') as f:
    for line in f:
        coords.append(tuple([int(l.strip()) for l in line.split(',')]))

max_x = 0
max_y = 0
for coord in coords:
    x, y = coord
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y

grid = list()
for y in range(max_y+1):
    row = list()
    for x in range(max_x+1):
        min_mh = 99999
        mh_c = None
        mh_count = 0
        for i in range(len(coords)):
            cx, cy = coords[i]
            mhdist = abs(cx-x) + abs(cy-y)
            if mhdist < min_mh:
                min_mh = mhdist
                mh_c = i
                mh_count = 1
            elif mhdist == min_mh:
                mh_count += 1
        if mh_count > 1:
            row.append(None)
        else:
            row.append(mh_c)
    grid.append(row)

invalid = set()
invalid.add(None)
for x in range(max_x+1):
    invalid.add(grid[0][x])
    invalid.add(grid[max_y][x])
for y in range(max_y+1):
    invalid.add(grid[y][0])
    invalid.add(grid[y][max_x])

counts = dict()
max_count = 0
max_v = None
for y in range(max_y+1):
    for x in range(max_x+1):
        v = grid[y][x]
        if v not in invalid:
            if v not in counts:
                counts[v] = 1
            else:
                counts[v] += 1
                if counts[v] > max_count:
                    max_count = counts[v]
                    max_v = v

print max_v
print max_count
