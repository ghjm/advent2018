import sys
import re
import z3

bots = list()

def read_data():
    global bots
    with open("input23.txt", "r") as f:
        for line in f:
            line = line.rstrip()
            toks = re.split('[=<,> ]', line)
            bots.append({'x': int(toks[2]), 'y': int(toks[3]), 'z': int(toks[4]), 'r': int(toks[8])})
    return bots

def longest_range_bot():
    global bots
    max_bot = {'r': -sys.maxint}
    for b in bots:
        if b['r'] > max_bot['r']:
            max_bot = b
    return max_bot

def bots_in_range(bot):
    global bots
    in_range = list()
    for b in bots:
        distance = sum([abs(b[dim] - bot[dim]) for dim in ['x', 'y', 'z']])
        if distance <= bot['r']:
            in_range.append(b)
    return in_range

def zabs(x):
    return z3.If(x >= 0, x, -x)

def z3_solver():
    global bots

    # z3 based solution shamelessly copied from reddit.com/u/mserrano

    # Create three z3 variables to bind to coordinates
    x, y, z = (z3.Int('x'), z3.Int('y'), z3.Int('z'))
    # Create a z3 variable named 'in_range_n' for all n bots
    in_ranges = [z3.Int('in_range_'+str(i)) for i in range(len(bots))]
    # Create a z3 variable that will be the count of points in range
    range_count = z3.Int('range_count')

    # Start a new optimization problem
    o = z3.Optimize()
    for i in range(len(bots)):
        # For all bots, 'in_range_n' is 1 if point (x,y,z) is in range, 0 otherwise
        o.add(in_ranges[i] ==
              z3.If(zabs(x - bots[i]['x']) + zabs(y - bots[i]['y']) + zabs(z - bots[i]['z']) <= bots[i]['r'], 1, 0))
    # range_count is the sum of all the in_range_n values, which is the count of bots in range
    o.add(range_count == sum(in_ranges))
    # Maximize the range count (this finds all points with the maximal range count)
    h1 = o.maximize(range_count)

    # Create a z3 variable to hold the distance from (0,0,0)
    dist_from_zero = z3.Int('dist_from_zero')
    # dist_from_zero is the Manhattan distance from (0,0,0)
    o.add(dist_from_zero == zabs(x) + zabs(y) + zabs(z))
    # Minimize the distance from zero
    h2 = o.minimize(dist_from_zero)

    # Check whether z3 could solve the problem
    if not o.check():
        print "z3 problem not satisfied"
        sys.exit(-1)

    # For a good solution, the lower and upper bounds should be equal
    if o.lower(h2).as_long() != o.upper(h2).as_long():
        print "solution did not converge to a single distance"
        sys.exit(-1)

    # Return the distance
    return o.lower(h2).as_long()

def main():
    read_data()
    max_bot = longest_range_bot()
    in_range = bots_in_range(max_bot)
    print 'Part A:', len(in_range)
    distance_to_best_point = z3_solver()
    print 'Part B:', distance_to_best_point

if __name__ == '__main__':
    main()
