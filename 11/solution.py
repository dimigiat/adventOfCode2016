'''
We have 2 types of objects, microchips and generators, scattered
across 3 floors. Each microchip and each generator are characterized 
by a radioactive material (e.g. thulium) and the following restriction
applies: we can't leave a particular microchip at the same floor with
generators of different materials, unless a generator of the same
material as the microchip is also present at the floor. There is an
elevator connecting the floors with each other and with an initially
empty 4th floor. The elevator can move 1 floor at a time, we can only
use it if we're carrying 1 or 2 objects with us, and at each stop we
have to take the objects we're carrying into the corresponding floor
before we're allowed to use the elevator again.

Part 1: Starting from the initial object placement (described in the
input) and with the elevator at the first floor, what is the minimum
number of elevator moves, subject to the constraints laid out, for
bringing all objects to the 4th floor?

Part 2: Same as part 1, but with 4 additional objects (microchips and
generators for 2 additional elements), initially located at 1st floor.
'''

from itertools import combinations
from time import time

from more_itertools import locate


NUM_FLOORS = 4


'''
We model the problem as a shortest path problem on the graph of
valid object placements at any given moment. We don't calculate
all the vertices and edges of the graph in advance. Instead, we
begin from the initial placement and, using a function which
returns the neighboring vertices of a vertex, we perform a
breadth-first search until we hit the intended final placement.

For N elements, a vertex is a list of (2*N + 1) integers in 
the range [0:NUM_FLOORS-1], stating the floor at which the 
objects and the elevator are at:
[chip_1 ... chip_N | gen_1 ... gen_N | elevator]

There are a few properties of the problem, which we can exploit
to prune the search-space and speed up the solution process.
The most important is that elements are interchangeable. We can
exchange the positions of a microchip and generator of element A
with the corresponding ones of element B; the shortest distances
of the two placements to the goal vertex of having all objects
in the top floor are exactly the same.
'''


def is_valid(vertex):
    '''
    Returns True if vertex satisfies problem constraints, else False.
    '''
    n_types = (len(vertex) - 1) // 2
    chips, generators = vertex[:n_types], vertex[n_types:-1]
    for elem, floor in enumerate(chips):
        # If the generator of the same element is not present in
        # the same floor as the chip, and there is at least one
        # generator in the floor, then vertex is invalid.
        if generators[elem] != floor and floor in generators:
            return False
    return True


def get_neighbors(vertex):
    '''
    Given a vertex, return list of all vertices to which we can move 
    '''
    neighbors = []
    level = vertex[-1]
    # Locate objects present at current elevator level
    # (Converting to tuple, to consume the iterable twice)
    objects = tuple(locate(vertex[:-1], lambda x: x == level))
    # One object moves
    for obj in objects:
        if level < NUM_FLOORS - 1:
            nb = list(vertex)
            nb[obj], nb[-1] = (level + 1,) * 2
            neighbors.append(tuple(nb))
        if level > 0:
            # Don't move nothing downstairs if lower floors empty
            if not any(floor in vertex for floor in range(level)):
                continue
            nb = list(vertex)
            nb[obj], nb[-1] = (level - 1,) * 2
            neighbors.append(tuple(nb))
    # Two object moves
    for obj_1, obj_2 in combinations(objects, 2):
        if level < NUM_FLOORS - 1:
            nb = list(vertex)
            nb[obj_1], nb[obj_2], nb[-1] = (level + 1,) * 3
            neighbors.append(tuple(nb))
        if level > 0:
            if not any(floor in vertex for floor in range(level)):
                continue
            nb = list(vertex)
            nb[obj_1], nb[obj_2], nb[-1] = (level - 1,) * 3
            neighbors.append(tuple(nb))
    return neighbors


def get_equivalent(vertex):
    '''
    Given a vertex, return list of equivalent vertices via
    interchanging combinations of pairs of elements.
    NOTE: To get an exhaustive list of equivalents, we should use 
    permutations. But while this would prune the search space more 
    drastically, it's computationally expensive (factorial of the
    number of elements), so we choose a more conservative approach
    which just considers interchanging 2 elements from the vertex.
    '''
    n_types = (len(vertex) - 1) // 2
    equivalent = []
    for i, j in combinations(range(n_types), 2):
        veq = list(vertex)
        veq[i], veq[j] = veq[j], veq[i]
        veq[n_types + i], veq[n_types + j] = veq[n_types + j], veq[n_types + i]
        equivalent.append(tuple(veq))
    return equivalent


def shortest_path(initial, goal):
    path_list = [[initial]]
    path_index = 0
    # Vertices visited
    visited = {initial}

    if initial == goal:
        return path_list[0]
    
    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_vertex = current_path[-1]

        # In an arbitrary graph, we get a vertex's neighbors from
        # a graph dictionary (graph(4) = {3, 7}) or an adjacency 
        # matrix ({i[0] for i in enumerate(adj[4]) if i[1]}).
        # Here we use the problem constraints, via the functions
        # is_valid and get_neighbors to get them on the go
        # whenever we encounter a new vertex in a path.

        # We cast to a list, as we iterate over the neighbors twice,
        # once to check for goal vertex, and once to add new paths.
        next_vertices = list(filter(is_valid, get_neighbors(last_vertex)))
        # Search goal vertex
        if goal in next_vertices:
            current_path.append(goal)
            return current_path
        # Add new paths
        for next_vertex in next_vertices:
            if not tuple(next_vertex) in visited:
                path_list.append(current_path + [next_vertex])
                visited.add(next_vertex)
                # Crucial speeding-up optimization: Elements are
                # interchangable, we can switch any two and get
                # a completely equivalent object arrangement.
                for equivalent in get_equivalent(next_vertex):
                    visited.add(equivalent)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return []


# -------- Part 1 ----------

# The initial vertex for an element ordering of
# (thulium, plutonium, promethium, strontium, ruthenium).
# The order doesn't matter, as long as it is the same
# for the microchips and the generators.
initial = (0, 1, 2, 1, 2, 0, 0, 2, 0, 2, 0)

# Goal vertex is: all objects and elevator are on top floor
goal = (3,) * 11

start_1 = time()

ans = shortest_path(initial, goal)
msg = ('The least amount of moves to get all the ' +
       f'objects on the top floor is: {len(ans) - 1}')

print(msg)
print()
print(f'Time elapsed for part 1: {time() - start_1}')


# -------- Part 2 ---------

# Add microchips and generators for 2 more elements at 1st floor
initial = (0, 1, 2, 1, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0)
goal = (3,) * 15

start_2 = time()

ans = shortest_path(initial, goal)
msg = ('The least amount of moves to get all the ' +
       f'objects on the top floor is: {len(ans) - 1}')

print(msg) 
print()
print(f'Time elapsed for part 2: {time() - start_2}')