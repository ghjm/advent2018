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

mhtsize = 0
grid = list()
for y in range(max_y+1):
    row = list()
    for x in range(max_x+1):
        mhtotal = 0
        for i in range(len(coords)):
            cx, cy = coords[i]
            mhtotal += abs(cx-x) + abs(cy-y)
        row.append(mhtotal)
        if mhtotal < 10000:
            mhtsize += 1
    grid.append(row)

print mhtsize
