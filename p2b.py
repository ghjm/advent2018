import sys

with open('input2.txt', 'r') as f:
    prevs = list()
    for line in f:
        line = line.strip()
        for p in prevs:
            if len(p) != len(line):
                continue
            diffs = 0
            for i in range(len(line)):
                if line[i] != p[i]:
                    diffs += 1
                if diffs > 1:
                    break
            if diffs == 1:
                print line
                print p
                common = ''
                for i in range(len(line)):
                    if line[i] == p[i]:
                        common += line[i]
                print common
                sys.exit(0)
        prevs.append(line)
print "not found"
