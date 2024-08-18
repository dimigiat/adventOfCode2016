'''

'''

import numpy as np

XSIZE, YSIZE = 30, 35

grid = np.zeros([XSIZE, YSIZE, 2], dtype='u2')


def viableCount(grid):
    count = 0
    for i,v in np.ndenumerate(grid[:,:,0]):
        for j,w in np.ndenumerate(grid[:,:,1]):
            if (i != j) and (v > 0) and (v < w):
                count += 1
    return count

def neighbors(x, y):
    ret = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    ret = [it for it in ret if 
           it[0] >= 0 and
           it[1] >= 0 and
           it[0] < XSIZE and
           it[1] < YSIZE]
    return ret


with open("input.txt") as f:
    next(f)
    next(f)
    for ind, row in enumerate(f):
        used, avail = map(int, (it[:-1] for it in row.split()[2:4]))
        grid[divmod(ind, YSIZE)] = used, avail

# print(f"Part 1: {viableCount(grid)}")

goalData = grid[XSIZE-1, 0, 0]
minUsed = np.amin(grid[:,:,0][grid[:,:,0]>0])
maxAvail = np.amax(grid[:,:,1][grid[:,:,0]>0])
print(minUsed, maxAvail)

# Node data exceeds size of all of its neighbors
# unmovable = 

# Node too small to fit data of goal node
tooSmall = np.sum(grid, axis = 2) < goalData