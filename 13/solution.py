'''
Each point in an infinite (x>=0, y>=0) grid is either free space or a wall,
depending on a function of x and y. Starting from point (1, 1), we want to
calculate the shortest path towards another specified point, where only
grid movements between free space points are allowed (like moving in a maze).
For part two, we count the number of distinct free space points that we can
visit in at most 50 steps.
'''

from collections import namedtuple

favNum = 1358
Point = namedtuple('Point', ['x', 'y'])


def isFree(point):
    x, y = point.x, point.y
    num = x*x + 3*x + 2*x*y + y + y*y + favNum
    return not bin(num).count('1') % 2

def isValid(point):
    return point.x >= 0 and point.y >= 0

def getNext(point):
    x, y = point.x, point.y
    neighbors = [Point(x-1,y), Point(x+1,y), Point(x,y-1), Point(x,y+1)]
    return [n for n in neighbors if isValid(n) and isFree(n)]

def shortestDistance(initial, goal):
    if initial == goal:
        return 0
    numSteps = 0
    paths = [[initial]]
    visited = {initial}
    while True:
        numSteps += 1
        for path in paths[:]:
            for point in getNext(path[-1]):
                if point == goal:
                    return numSteps
                # Avoid circles and longer paths to a point
                if point not in visited:
                    paths.append(path + [point])
                    visited.add(point)
            paths.remove(path)

def countPoints(initial, numSteps):
    paths = [[initial]]
    visited = {initial}
    for _ in range(numSteps):
        for path in paths[:]:
            for point in getNext(path[-1]):
                # Avoid circles and longer paths to a point
                if point not in visited:
                    paths.append(path + [point])
                    visited.add(point)
            paths.remove(path)
    return len(visited)

initial, goal = Point(1, 1), Point(31, 39)
print(f"We can reach the target in {shortestDistance(initial, goal)} steps.")
print(f"In 50 steps we can visit {countPoints(initial, 50)} locations.")