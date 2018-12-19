import sys
import re

r = re.compile('Step (.) must be finished before step (.) can begin')

deps = dict()
with open('input7.txt', 'r') as f:
    for line in f:
        m = r.match(line)
        if not m:
            print 'bad line', line.strip()
            sys.exit(1)
        for s in m.groups():
            if s not in deps:
                deps[s] = list()
        deps[m.groups()[1]].append(m.groups()[0])

steps = list()
kk = set(deps.keys())
while True:
    ss = set(steps)
    avail = kk - ss
    if len(avail) == 0:
        break
    ok = set()
    for a in avail:
        good = True
        for d in deps[a]:
            if d not in ss:
                good = False
                break
        if good:
            ok.add(a)
    steps.append(sorted(list(ok))[0])

print ''.join(steps)
