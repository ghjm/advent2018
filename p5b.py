from LinkedList import LinkedList


def figure_polymer(polymer):
    p = LinkedList(polymer)
    changed = True
    start = p.head
    while changed:
        changed = False
        n = start
        i = 0
        while n is not None:
            i += 1
            if n.prev is not None:
                cc = n.data
                pc = n.prev.data
                if (cc != pc) and (cc.upper() == pc.upper()):
                    if n.prev.prev is None:
                        start = p.head
                    else:
                        start = n.prev.prev
                    p.remove(n.prev)
                    p.remove(n)
                    changed = True
                    break
            n = n.next
    return len(p)


def main():
    with open('input5.txt', 'r') as f:
        polymer = list(f.readline().strip())
    types = set()
    for i in range(len(polymer)):
        types.add(polymer[i].upper())
    print types
    print len(types)
    min_size = len(polymer)
    best = None
    i = 0
    for t in types:
        i += 1
        print i, t
        psub = [c for c in polymer if c.upper() != t]
        pr = figure_polymer(psub)
        if pr < min_size:
            print 'new best', t, pr
            min_size = pr
            best = t
    print best, min_size


main()
