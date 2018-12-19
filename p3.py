import re

r = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

claims = list()
with open('input3.txt', 'r') as f:
    for line in f:
        line = line.strip()
        m = r.match(line)
        claims.append(tuple([int(g) for g in m.groups()]))

cells = dict()
for cid, left, top, width, height in claims:
    for cell in [(x, y) for x in range(left, left + width) for y in range(top, top + height)]:
        if cell not in cells:
            cells[cell] = list()
        cells[cell].append(cid)

multiclaims = 0
for c in cells:
    if len(cells[c]) >= 2:
        multiclaims += 1
print "Multiclaims:", multiclaims

for cid, left, top, width, height in claims:
    solo_claim = True
    for cell in [(x, y) for x in range(left, left + width) for y in range(top, top + height)]:
        if len(cells[cell]) >= 2:
            solo_claim = False
            break
    if solo_claim:
        print "Solo claim:", cid
        break
