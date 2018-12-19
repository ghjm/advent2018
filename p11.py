import sys
import itertools
import numpy as np

def get_power_level(x, y, grid_serial_number=5093):
    rack_id = x+10
    power = rack_id * y
    power += grid_serial_number
    power *= rack_id
    power = (int(power) / 100) % 10
    power -= 5
    return power

def get_power_grid():
    return np.array([[get_power_level(x,y) for x in range(300)] for y in range(300)])

def search_power_grid(pg, size=3):
    best = -sys.maxint
    best_xy = None
    for xy in itertools.product(range(len(pg)-size+1), range(len(pg[0])-size+1)):
        x, y = xy
        fuel = np.sum(pg[y:y+size,x:x+size])
        if fuel > best:
            best = fuel
            best_xy = xy
    return best_xy, best

def search_sizes(pg):
    best = -sys.maxint
    best_xy = None
    best_size = None
    for size in range(1, len(pg)+1):
        xy, fuel = search_power_grid(pg, size)
        if fuel > best:
            best = fuel
            best_xy = xy
            best_size = size
    return best_xy, best_size, best

def main():
    pg = get_power_grid()
    print search_power_grid(pg)
    print search_sizes(pg)

if __name__ == '__main__':
    main()