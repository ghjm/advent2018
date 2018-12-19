import sys
import re

def get_step_limits(step):
    min_x = min_y = sys.maxint
    max_x = max_y = -sys.maxint
    step_set = set()
    for i in range(len(step)):
        x, y = step[i]
        step_set.add(step[i])
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
    return min_x, max_x, min_y, max_y

def step_limit_size(step_limits):
    return (step_limits[1] - step_limits[0]) * (step_limits[3] - step_limits[2])

def print_step(step, step_limits):
    min_x, max_x, min_y, max_y = step_limits
    step_set = set()
    for s in step:
        step_set.add(s)
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x,y) in step_set:
                sys.stdout.write('#')
            else:
                sys.stdout.write(' ')
        print ""
    sys.stdout.flush()

points = list()
with open('input10.txt', 'r') as f:
    r = re.compile('position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>')
    for line in f:
        m = r.match(line)
        if not m:
            print "Bad line"
            sys.exit(1)
        points.append(tuple([int(s) for s in m.groups()]))

prev_step = [(p[0], p[1]) for p in points]
prev_step_limits = get_step_limits(prev_step)
time_now = 0

while True:
    new_step = [(prev_step[i][0] + points[i][2], prev_step[i][1] + points[i][3]) for i in range(len(prev_step))]
    new_step_limits = get_step_limits(new_step)
    if step_limit_size(new_step_limits) > step_limit_size(prev_step_limits):
        print_step(prev_step, prev_step_limits)
        print ""
        print time_now
        break
    time_now += 1
    prev_step = new_step
    prev_step_limits = new_step_limits


