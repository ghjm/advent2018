points = set()

def read_data():
    with open("input25.txt", "r") as f:
        for line in f:
            line = line.strip()
            toks = line.split(',')
            points.add(tuple([int(t) for t in toks]))

def distance_between(a, b):
    return sum([abs(a[i]-b[i]) for i in range(min(len(a),len(b)))])

def explore(point):
    group = {point}
    open_list = {point}
    closed_list = set()
    while len(open_list) > 0:
        this_p = open_list.pop()
        if this_p not in closed_list:
            closed_list.add(this_p)
            for other_p in points:
                if other_p not in closed_list and distance_between(this_p, other_p) <= 3:
                    group.add(other_p)
                    open_list.add(other_p)
    return group

def explore_all():
    groups = list()
    unvisited = set(points)
    while len(unvisited) > 0:
        point = unvisited.pop()
        group = explore(point)
        groups.append(group)
        unvisited -= group
    return groups

def main():
    read_data()
    groups = explore_all()
    print "Part A:", len(groups)

if __name__ == '__main__':
    main()
