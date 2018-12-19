with open('input5.txt', 'r') as f:
    polymer = list(f.readline().strip())

changed = True
lc = 0
while changed:
    changed = False
    for i in range(lc, len(polymer)-1):
        if (polymer[i] != polymer[i+1]) and (polymer[i].upper() == polymer[i+1].upper()):
            del polymer[i:i+2]
            changed = True
            lc = max(0, i-2)
            print i
            break
print len(polymer)
