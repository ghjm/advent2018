import sys
import re

r1 = re.compile('^\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] (.+)$')
r2 = re.compile('Guard #(\d+) begins shift')

events = list()
with open('input4.txt', 'r') as f:
    for line in f:
        line = line.strip()
        m = r1.match(line)
        if m:
            events.append(tuple(m.groups()))
        else:
            print "FAIL"
            sys.exit(1)

guards = dict()
guard = None
awake = True
last_start = 0
date = None
for event in sorted(events):
    year, month, day, hour, minute, message = event
    date = year + '-' + month + '-' + day
    m = r2.match(message)
    if m:
        if not awake:
            guards[guard][date].extend(range(last_start, 60))
        guard = int(m.groups()[0])
        awake = True
        last_start = 0
        if guard not in guards:
            guards[guard] = dict()
    elif message == 'falls asleep':
        if date not in guards[guard]:
            guards[guard][date] = list()
        awake = False
        last_start = int(minute)
    elif message == 'wakes up':
        if date not in guards[guard]:
            guards[guard][date] = list()
        guards[guard][date].extend(range(last_start, int(minute)))
        awake = True
        last_start = int(minute)
if not awake:
    guards[guard][date].extend(range(last_start, 60))

max_total_asleep = 0
max_guard = None
for guard in guards:
    total_asleep = 0
    for date in guards[guard]:
        total_asleep += len(guards[guard][date])
    if total_asleep > max_total_asleep:
        max_total_asleep = total_asleep
        max_guard = guard
print 'max_guard', max_guard
print 'max_total_asleep', max_total_asleep

guard_minutes = dict()
for guard in guards:
    guard_minutes[guard] = dict()
    for date in guards[guard]:
        for minute in guards[guard][date]:
            if minute in guard_minutes[guard]:
                guard_minutes[guard][minute] += 1
            else:
                guard_minutes[guard][minute] = 1

max_minutes = dict()
for guard in guards:
    max_minute_val = 0
    for minute in guard_minutes[guard]:
        if guard_minutes[guard][minute] > max_minute_val:
            max_minute_val = guard_minutes[guard][minute]
            max_minute = minute
    max_minutes[guard] = (max_minute, max_minute_val)

print 'problem 1', max_minutes[max_guard][0] * max_minutes[max_guard][1]

max_max_minute_val = 0
max_max_minute = None
max_max_guard = None
for guard in max_minutes:
    max_minute, max_minute_val = max_minutes[guard]
    if max_minute_val > max_max_minute_val:
        max_max_minute_val = max_minute_val
        max_max_minute = max_minute
        max_max_guard = guard
print 'problem 2', max_max_guard * max_max_minute