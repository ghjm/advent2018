with open('input2.txt', 'r') as f:
    twos = 0
    threes = 0
    for line in f:
        line = line.strip()
        counts = dict()
        for c in line:
            if c in counts:
                counts[c] += 1
            else:
                counts[c] = 1
        if 2 in counts.values():
            twos += 1
        if 3 in counts.values():
            threes += 1
    print twos
    print threes
    print twos * threes