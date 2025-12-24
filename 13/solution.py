'''
Each point in an infinite (x>=0, y>=0) grid is either free space or a wall,
depending on a function of x and y. Starting from point (1, 1), we want to
calculate the shortest path towards another specified point, where only
grid movements between free space points are allowed (like moving in a maze).
For part two, we count the number of distinct free space points that we can
visit in at most 50 steps.
'''

from collections import namedtuple, deque
from itertools import chain
from functools import cache
from typing import Generator


FAVNUM = 1358


Point = namedtuple('Point', 'x, y')


@cache
def is_free(point: Point) -> bool:
    '''
    Return True/False depending on the number of 1's in the binary
    representation of the result of a function of a point's coordinates.
    '''
    x, y = point
    num = x*x + 3*x + 2*x*y + y + y*y + FAVNUM
    return bin(num).count('1') % 2 == 0


def is_valid(point: Point) -> bool:
    return point.x >= 0 and point.y >= 0


def _get_next(point: Point) -> Generator[Point, None, None]:
    '''
    Return list of neighboring and free points, for a given point.
    '''
    x, y = point
    for nb in (Point(x-1, y), Point(x+1, y), Point(x, y-1), Point(x, y+1)):
        if is_valid(nb) and is_free(nb):
            yield nb


def shortest_distance(initial: Point, goal: Point) -> int|None:
    '''
    Return the shortest grid distance between two points, provided
    that only movements along a path of free points are allowed.
    '''
    visited = {initial}
    queue = deque([(initial, 0)])

    while queue:
        curr, dist = queue.popleft()
        if curr == goal:
            return dist
        for nb in _get_next(curr):
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, dist + 1))

    return None


def count_points(initial: Point, numSteps: int) -> int:
    '''
    For an initial point and a given maximum number of steps, 
    calculate the number of distinct free points that are reachable 
    (considering all possible paths)
    '''
    visited = {initial}
    frontier = [initial]

    # NOTE: We could have followed a typical BFS implementation with
    # a deque as we did for shortest distance, skipping expansion when we
    # reach dist == numSteps. However, we chose to implement an iterative
    # frontier expansion, for practicing the use of chain.from_iterable.

    for _ in range(numSteps):
        frontier = [
            p for p in chain.from_iterable(map(_get_next, frontier)) 
            if p not in visited
            ]
        visited.update(frontier)

    return len(visited)


if __name__ == '__main__':

    initial, goal = Point(1, 1), Point(31, 39)

    # --------------- Part 1 -------------------- 
    if (result_1 := shortest_distance(initial, goal)) is not None:
        print(f'We can reach the goal node in {result_1} steps.')
    else:
        print('Goal node is unreachable.')

    # --------------- Part 2 --------------------
    print(f'In 50 steps we can visit {count_points(initial, 50)} locations.')