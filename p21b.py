import sys

seen = set()
r0 = 0
count = 0
while True:
    r2 = r0 | 65536
    r0 = 10362650
    while True:
        r4 = r2 & 255
        r0 += r4
        r0 &= 16777215
        r0 *= 65899
        r0 &= 16777215
        if 256 > r2:
            if r0 in seen:
                sys.exit(0)
            count += 1
            print count, r0
            seen.add(r0)
            break
        r4 = 0
        r2 = r2 // 256
