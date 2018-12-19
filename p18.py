import sys

def read_data():
    grid = list()
    with open('input18.txt', 'r') as f:
        for line in f:
            grid.append(line.rstrip())
    return grid

def grid_step(grid):

    def adj_count(char):
        count = 0
        for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            ty = y + dy
            tx = x + dx
            if ty < 0 or tx < 0 or ty >= len(grid) or tx >= len(grid[ty]):
                continue
            if grid[ty][tx] == char:
                count += 1
        return count

    new_grid = list()
    for y in range(len(grid)):
        new_line = list()
        for x in range(len(grid[y])):
            c = grid[y][x]
            if c == '.':
                if adj_count('|') >= 3:
                    c = '|'
            elif c == '|':
                if adj_count('#') >= 3:
                    c = '#'
            elif c == '#':
                if adj_count('#') < 1 or adj_count('|') < 1:
                    c = '.'
            new_line.append(c)
        new_grid.append(new_line)
    return new_grid

def get_grid_value(grid):
    woods = 0
    lumber = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            c = grid[y][x]
            if c == '#':
                lumber += 1
            elif c == '|':
                woods += 1
    return woods * lumber

def main():
    grid = read_data()
    states = [get_grid_value(grid)]
    loop = None
    loopc = 0
    steps = 0
    while True:
        steps += 1
        grid = grid_step(grid)
        ggv = get_grid_value(grid)
        if steps == 10:
            print 'part A:', ggv
        if loop is not None:
            if ggv == loop[loopi]:
                loopi = (loopi + 1) % len(loop)
                if loopi == 0:
                    loopc += 1
                    if loopc >= 3:
                        print 'part B:', loop[(1000000000 - steps - 1) % len(loop)]
                        break
            else:
                loop = None
                loopc = 0
        elif ggv in states:
            loop = states[states.index(ggv):]
            if len(loop) > 1:
                loopi = 1
            else:
                loop = None
        states.append(ggv)

if __name__ == '__main__':
    main()
