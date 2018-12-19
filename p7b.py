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

done = set()
steps = set(deps.keys())
workers = [{'work': None, 'complete': 0} for i in range(5)]
time_now = 0
while True:
    lct = sys.maxint
    for w in workers:
        if w['work'] is not None and w['complete'] < lct:
            lct = w['complete']
            time_now = lct
    for w in workers:
        if w['work'] is not None and w['complete'] == time_now:
            done.add(w['work'])
            w['work'] = None
            w['complete'] = 0
    working = set([w['work'] for w in workers if w['work'] is not None])
    not_done = steps - done
    if len(not_done) == 0:
        break
    startable = set()
    for a in not_done:
        good = True
        for d in deps[a]:
            if d not in done:
                good = False
                break
        if good and a not in working:
            startable.add(a)
    for s in sorted(list(startable)):
        for w in workers:
            if w['work'] is None:
                w['work'] = s
                w['complete'] = time_now + 60 + ord(s) - ord('A') + 1
                break

    print 'time_now', time_now
    print 'done', ''.join(sorted(done)) if len(done) > 0 else '<none>'
    print 'startable', ''.join(sorted(startable)) if len(startable) > 0 else '<none>'
    print 'workers', workers
    print '---------------------------------'

print 'finished at', time_now
