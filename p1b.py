import sys

sum = 0
freqs = set()
while True:
    print "pass", sum
    with open('input1.txt', 'r') as f:
        for line in f:
            line = line.strip()
            sum += int(line)
            if sum in freqs:
                print sum
                sys.exit(0)
            freqs.add(sum)