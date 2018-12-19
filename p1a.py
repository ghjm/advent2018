with open('input1.txt', 'r') as f:
    sum = 0
    for line in f:
        line = line.strip()
        sum += int(line)
print sum